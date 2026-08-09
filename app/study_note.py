import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "study_notes"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')
_TRANSCRIPT_MARKER = "## Transcript"
_SUMMARY_HEADER = re.compile(r"^#\s*Summary\s*$", re.MULTILINE)
_NEXT_HEADER = re.compile(r"^#\s+\S", re.MULTILINE)


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


def extract_summary(body: str) -> str:
    """Reads the "# Summary" section back out of a generated Study Note
    (Feature 003, decision 1-A): once Study Note exists, its own Summary
    section becomes the Queue Card teaser — no separate quick_summary Gemini
    call is made just to produce that one line. Returns "" if the section
    isn't present (shouldn't happen for a real Gemini response, but this must
    never raise on unexpected input).
    """
    match = _SUMMARY_HEADER.search(body)
    if not match:
        return ""
    start = match.end()
    next_header = _NEXT_HEADER.search(body, start)
    end = next_header.start() if next_header else len(body)
    return body[start:end].strip()


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
