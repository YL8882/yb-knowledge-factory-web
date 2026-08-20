import json
from datetime import datetime, timezone
from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "outputs" / "history.json"

LOCAL_TESTER_ID = "local"


def _write_history_file(data: dict[str, list[dict]]) -> None:
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _load_history() -> dict[str, list[dict]]:
    if not HISTORY_FILE.exists():
        return {}
    try:
        raw = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    # T4.1: data predating per-tester isolation is a flat list. It was all
    # written before Beta Testers existed, so it belongs entirely to Local
    # Mode (tester_id "local") — never surfaced to an authenticated tester.
    return {LOCAL_TESTER_ID: raw} if isinstance(raw, list) else raw


_history: dict[str, list[dict]] = _load_history()


def add_entry(tester_id: str, video_id: str, title: str, url: str, request_id: str | None = None) -> None:
    """Records that a video was processed, independent of the (ephemeral) Queue —
    an item stays in history even after the user deletes it from the Queue to free
    up staging-area space, so it can still be traced back to the YB channel later.

    request_id (Sprint 8.5A, optional for backward compatibility): mirrors the
    Correlation ID queue_store.add_item() generated for this run, so Product
    Intelligence's Download-stage logging can still resolve it via History
    after the item is removed from the Queue. Always overwritten on a repeat
    call, same as title/url, since a repeat add starts a new processing run.

    Overwrite-on-repeat (T4.1) is scoped to this tester only — Tester A and
    Tester B each keep their own independent history entry for the same
    video_id, never overwriting each other's.
    """
    tester_entries = _history.setdefault(tester_id, [])

    for entry in tester_entries:
        if entry["video_id"] == video_id:
            entry["title"] = title
            entry["url"] = url
            entry["request_id"] = request_id
            _write_history_file(_history)
            return

    tester_entries.append(
        {
            "video_id": video_id,
            "title": title,
            "url": url,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
        }
    )
    _write_history_file(_history)


def list_entries(tester_id: str) -> list[dict]:
    return sorted(_history.get(tester_id, []), key=lambda entry: entry["added_at"], reverse=True)
