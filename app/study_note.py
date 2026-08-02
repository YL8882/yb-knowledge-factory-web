import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "study_notes"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')
_TRANSCRIPT_MARKER = "## Transcript"


class TranscriptNotFoundError(Exception):
    pass


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def read_transcript(transcript_path: str) -> str:
    path = Path(transcript_path)
    if not path.exists():
        raise TranscriptNotFoundError(f"Transcript file not found: {transcript_path}")
    return path.read_text(encoding="utf-8")


def extract_transcript_body(transcript_content: str) -> str:
    idx = transcript_content.find(_TRANSCRIPT_MARKER)
    if idx == -1:
        return transcript_content.strip()
    return transcript_content[idx + len(_TRANSCRIPT_MARKER):].strip()


def find_cached_study_note(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Study_Note.md already on disk for
    this video_id (matched by the `_{video_id}.md` filename suffix), so callers can
    reuse it instead of calling Gemini again.
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.md"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def save_study_note(video_id: str, title: str, body: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    output_path = OUTPUT_DIR / f"SN_{safe_title}_{video_id}.md"

    output_path.write_text(body.strip() + "\n", encoding="utf-8")
    return output_path
