import json
from datetime import datetime, timezone
from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "outputs" / "history.json"


def _write_history_file(entries: list[dict]) -> None:
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


_history: list[dict] = _load_history()


def add_entry(video_id: str, title: str, url: str) -> None:
    """Records that a video was processed, independent of the (ephemeral) Queue —
    an item stays in history even after the user deletes it from the Queue to free
    up staging-area space, so it can still be traced back to the YB channel later.
    """
    for entry in _history:
        if entry["video_id"] == video_id:
            entry["title"] = title
            entry["url"] = url
            _write_history_file(_history)
            return

    _history.append(
        {
            "video_id": video_id,
            "title": title,
            "url": url,
            "added_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    _write_history_file(_history)


def list_entries() -> list[dict]:
    return sorted(_history, key=lambda entry: entry["added_at"], reverse=True)
