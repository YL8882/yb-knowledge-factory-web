import re
from pathlib import Path

import yt_dlp
from faster_whisper import WhisperModel

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "transcripts"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')

_model: WhisperModel | None = None


class AudioDownloadError(Exception):
    pass


class TranscriptionError(Exception):
    pass


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model


def download_audio(video_id: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(dest_dir / f"{video_id}.%(ext)s")

    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
    }

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


def transcribe_audio(audio_path: Path) -> str:
    try:
        model = _get_model()
        segments, _info = model.transcribe(str(audio_path))
        text = "".join(segment.text for segment in segments).strip()
    except Exception as exc:
        raise TranscriptionError(str(exc)) from exc

    return text


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def save_transcript(video_id: str, title: str, url: str, transcript_text: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    output_path = OUTPUT_DIR / f"{safe_title}_{video_id}.md"

    content = (
        f"# {title}\n"
        f"{url}\n"
        "\n"
        "---\n"
        "\n"
        "## Transcript\n"
        "\n"
        f"{transcript_text}\n"
    )

    output_path.write_text(content, encoding="utf-8")
    return output_path
