import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Callable

import yt_dlp
from faster_whisper import WhisperModel
from opencc import OpenCC

# (fraction_done: 0..1, eta_seconds: float | None) -> None
ProgressCallback = Callable[[float, float | None], None]

# Minimum wall-clock gap between progress callbacks, so a fast-moving download or
# a transcript with many short segments doesn't turn into a queue.json write storm.
_PROGRESS_THROTTLE_SECONDS = 1.0

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "transcripts"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')
_SUMMARY_MARKER = "## Summary"
_TRANSCRIPT_MARKER = "## Transcript"

# Preference order when a video has captions in more than one language — Taiwan
# Traditional Chinese first, then other Chinese variants, then English. If none of
# these are available, fetch_subtitle_transcript() falls back to whatever single
# language YouTube actually offers.
_SUBTITLE_LANG_PRIORITY = ["zh-Hant", "zh-TW", "zh-Hans", "zh-CN", "zh", "en"]

_VTT_TAG_PATTERN = re.compile(r"<[^>]+>")
_VTT_TIMESTAMP_LINE = re.compile(r"^\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->")
_VTT_CUE_NUMBER = re.compile(r"^\d+$")

_model: WhisperModel | None = None
_traditional_converter: OpenCC | None = None


def _get_traditional_converter() -> OpenCC:
    global _traditional_converter
    if _traditional_converter is None:
        _traditional_converter = OpenCC("s2twp")
    return _traditional_converter


class AudioDownloadError(Exception):
    pass


class TranscriptionError(Exception):
    pass


class SubtitleFetchError(Exception):
    pass


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model


def _vtt_to_text(vtt_content: str) -> str:
    """Strips a WebVTT caption file down to plain spoken text: drops the header,
    cue numbers, timestamp lines and inline `<...>` timing tags, and collapses the
    rolling-caption duplication YouTube's auto-generated tracks produce (each cue
    repeats the tail of the previous one) by skipping a line identical to the one
    just emitted.
    """
    pieces: list[str] = []
    for raw_line in vtt_content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE")):
            continue
        if "-->" in line or _VTT_TIMESTAMP_LINE.match(line) or _VTT_CUE_NUMBER.match(line):
            continue

        text = _VTT_TAG_PATTERN.sub("", line).strip()
        if not text or (pieces and pieces[-1] == text):
            continue
        pieces.append(text)

    return " ".join(pieces).strip()


def fetch_subtitle_transcript(video_id: str) -> str | None:
    """Reuses a caption track YouTube already has (manual first, then
    auto-generated) as the transcript, so the pipeline can skip downloading audio
    and running Whisper entirely — reuse before recompute. Returns None (not an
    error) when the video simply has no captions in any usable language; callers
    should fall back to download_audio()/transcribe_audio() in that case.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_sub_"))
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": _SUBTITLE_LANG_PRIORITY,
            "subtitlesformat": "vtt",
            "outtmpl": str(tmp_dir / f"{video_id}.%(ext)s"),
            "noplaylist": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
        except Exception as exc:
            raise SubtitleFetchError(str(exc)) from exc

        for lang in _SUBTITLE_LANG_PRIORITY:
            matches = sorted(tmp_dir.glob(f"{video_id}.{lang}.vtt"))
            if matches:
                text = _vtt_to_text(matches[0].read_text(encoding="utf-8"))
                if text:
                    return _get_traditional_converter().convert(text)

        # None of the preferred languages were available — accept whatever single
        # language YouTube actually wrote (e.g. a video with only Japanese captions).
        any_match = sorted(tmp_dir.glob(f"{video_id}.*.vtt"))
        if any_match:
            text = _vtt_to_text(any_match[0].read_text(encoding="utf-8"))
            if text:
                return _get_traditional_converter().convert(text)

        return None
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def download_audio(video_id: str, dest_dir: Path, on_progress: ProgressCallback | None = None) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(dest_dir / f"{video_id}.%(ext)s")

    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
    }

    if on_progress:
        last_call = 0.0

        def _hook(d: dict) -> None:
            nonlocal last_call
            if d.get("status") != "downloading":
                return
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes")
            if not total or downloaded is None:
                return
            now = time.monotonic()
            if now - last_call < _PROGRESS_THROTTLE_SECONDS:
                return
            last_call = now
            on_progress(min(downloaded / total, 1.0), d.get("eta"))

        ydl_opts["progress_hooks"] = [_hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=True
            )
            audio_path = Path(ydl.prepare_filename(info))
    except Exception as exc:
        raise AudioDownloadError(str(exc)) from exc

    if not audio_path.exists():
        raise AudioDownloadError(f"Audio file not found after download: {audio_path}")

    return audio_path


def transcribe_audio(audio_path: Path, on_progress: ProgressCallback | None = None) -> str:
    try:
        model = _get_model()
        segments, info = model.transcribe(str(audio_path))

        # faster_whisper already decodes and transcribes in successive windows,
        # yielding one segment at a time as it goes — that's the "chunking" a long
        # video needs, for free. We just read progress off it: each segment carries
        # the audio timestamp it ends at, so segment.end / total duration is the
        # real fraction complete, and eta is extrapolated from how long that
        # fraction has actually taken so far.
        total_duration = info.duration if info and info.duration else None
        start_time = time.monotonic()
        last_call = 0.0
        pieces = []

        for segment in segments:
            pieces.append(segment.text)

            if on_progress and total_duration:
                now = time.monotonic()
                if now - last_call >= _PROGRESS_THROTTLE_SECONDS:
                    last_call = now
                    fraction = min(segment.end / total_duration, 1.0)
                    elapsed = now - start_time
                    eta_seconds = (elapsed / fraction) - elapsed if fraction > 0.01 else None
                    on_progress(fraction, eta_seconds)

        text = "".join(pieces).strip()
        text = _get_traditional_converter().convert(text)
    except Exception as exc:
        raise TranscriptionError(str(exc)) from exc

    if not text.strip():
        raise TranscriptionError("empty transcript")

    return text


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def find_cached_transcript(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Transcript.md already on disk for
    this video_id (matched by the `_{video_id}.md` filename suffix, not by title, so
    it still matches even if the fetched title text has since changed slightly),
    so callers can reuse it instead of re-downloading audio and re-running Whisper.
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.md"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def extract_summary(transcript_content: str) -> str:
    """Reads the one-sentence summary back out of a saved Transcript.md — the
    Transcript file is the single source of truth for it, so a cache hit never
    needs to call Gemini again to get it. Returns "" if the file predates this
    field (no "## Summary" section) so the caller can fall back to generating one.
    """
    start = transcript_content.find(_SUMMARY_MARKER)
    if start == -1:
        return ""
    start += len(_SUMMARY_MARKER)
    end = transcript_content.find(_TRANSCRIPT_MARKER, start)
    section = transcript_content[start:end] if end != -1 else transcript_content[start:]
    return section.strip()


def save_transcript(video_id: str, title: str, url: str, transcript_text: str, summary: str = "") -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    output_path = OUTPUT_DIR / f"TN_{safe_title}_{video_id}.md"

    content = (
        f"# {title}\n"
        f"{url}\n"
        "\n"
        "---\n"
        "\n"
        "## Summary\n"
        "\n"
        f"{summary}\n"
        "\n"
        "## Transcript\n"
        "\n"
        f"{transcript_text}\n"
    )

    output_path.write_text(content, encoding="utf-8")
    return output_path
