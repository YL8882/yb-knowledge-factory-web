import json
import re
from pathlib import Path

# extract_blueprint_items() stays in teach_back.py per user decision (Feature
# First, Refactor Later) — main.py already imports teach_back and calls
# teach_back.extract_blueprint_items() directly, no re-export needed here.

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "action_lists"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def find_cached_action_list(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Action List Knowledge JSON
    already on disk for this video_id, so callers can reuse it instead of
    calling Gemini again (Persistence — Knowledge_Structure_Engine_v1.0.md §7).
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def load_action_list(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_cached_action_list_markdown(video_id: str) -> Path | None:
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.md"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def save_action_list(video_id: str, title: str, data: dict) -> Path:
    """Persists both the structured Knowledge JSON (source of truth, used to
    re-render the HTML Preview) and the formatted .md (generated once here,
    served directly via FileResponse for download) — same pattern as
    teach_back.save_teach_back().
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    json_path = OUTPUT_DIR / f"AL_{safe_title}_{video_id}.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = OUTPUT_DIR / f"AL_{safe_title}_{video_id}.md"
    md_path.write_text(format_action_list_markdown(title, data), encoding="utf-8")

    return json_path


def format_action_list_markdown(title: str, data: dict) -> str:
    lines = [f"# Action List — {title}", ""]
    for action in data.get("actions", []):
        lines.append(f"- [ ] {action}")
    return "\n".join(lines).strip() + "\n"
