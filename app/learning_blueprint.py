import json
import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "learning_blueprints"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def find_cached_learning_blueprint(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Knowledge JSON already on
    disk for this video_id (matched by the `_{video_id}.json` filename
    suffix), so callers can reuse it instead of calling Gemini again.
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def load_learning_blueprint(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_learning_blueprint(video_id: str, title: str, data: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    output_path = OUTPUT_DIR / f"LB_{safe_title}_{video_id}.json"

    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
