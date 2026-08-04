import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "knowledge_outlines"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def find_cached_knowledge_outline(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Knowledge Outline already on
    disk for this video_id (matched by the `_{video_id}.md` filename suffix),
    so callers can reuse it instead of calling Gemini again.
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.md"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def save_knowledge_outline(video_id: str, title: str, body: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    output_path = OUTPUT_DIR / f"KO_{safe_title}_{video_id}.md"

    output_path.write_text(body.strip() + "\n", encoding="utf-8")
    return output_path
