import re
from datetime import date
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


def build_metadata_block(title: str, url: str, tags: str = "") -> str:
    generated_date = date.today().isoformat()
    return (
        "# Study Note\n\n"
        f"Title: {title}\n\n"
        f"Source: {url}\n\n"
        "Author: 未提供\n\n"
        f"Date: {generated_date}\n\n"
        "Language: 繁體中文\n\n"
        f"Tags: {tags}\n\n"
        "Version: v1.0\n"
    )


def save_study_note(video_id: str, title: str, url: str, body: str, tags: str = "") -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    output_path = OUTPUT_DIR / f"{safe_title}_{video_id}.md"

    metadata = build_metadata_block(title, url, tags)
    content = f"{metadata}\n---\n\n{body}\n"

    output_path.write_text(content, encoding="utf-8")
    return output_path
