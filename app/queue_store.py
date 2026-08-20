import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

MAX_QUEUE_SIZE = 100

QUEUE_FILE = Path(__file__).parent.parent / "outputs" / "queue.json"

LOCAL_TESTER_ID = "local"


class QueueFullError(Exception):
    pass


class DuplicateVideoError(Exception):
    pass


class QueueItemNotFoundError(Exception):
    pass


def _write_queue_file(data: dict[str, list[dict]]) -> None:
    try:
        QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        QUEUE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _load_queue() -> dict[str, list[dict]]:
    if not QUEUE_FILE.exists():
        return {}
    try:
        raw = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    # T4.1: data predating per-tester isolation is a flat list. It was all
    # written before Beta Testers existed, so it belongs entirely to Local
    # Mode (tester_id "local") — never surfaced to an authenticated tester.
    data = {LOCAL_TESTER_ID: raw} if isinstance(raw, list) else raw

    # Recover items left frozen mid-"Transcribing"/"Generating" by a server restart
    # that killed the background task doing the work — otherwise nothing will ever
    # move them again, and the UI shows a progress bar forever with no file produced.
    # Reset to the last known-good, retryable state (same states the live error
    # handlers already fall back to when a request fails outright).
    changed = False
    for tester_items in data.values():
        for item in tester_items:
            if item.get("status") in ("Downloading", "Transcribing"):
                item["status"] = "Queued"
                changed = True
            elif item.get("status") == "Generating":
                item["status"] = "Transcript Ready"
                changed = True

    if changed:
        _write_queue_file(data)

    return data


def _save_queue() -> None:
    _write_queue_file(_queue)


_queue: dict[str, list[dict]] = _load_queue()


def add_item(tester_id: str, video_id: str, title: str, url: str) -> dict:
    tester_items = _queue.setdefault(tester_id, [])

    if any(item["video_id"] == video_id for item in tester_items):
        raise DuplicateVideoError(f"Video already in queue: {video_id}")

    if len(tester_items) >= MAX_QUEUE_SIZE:
        raise QueueFullError("Queue is full")

    item = {
        "video_id": video_id,
        "title": title,
        "url": url,
        "status": "Queued",
        "created_at": datetime.now(timezone.utc).isoformat(),
        # Correlation ID (Sprint 8.5A): shared by every Product Intelligence
        # event for this processing run — Queue, Transcript, Gemini, Study
        # Note, Download — so they can all be traced back to one journey.
        # Mirrored into history_store.add_entry() so it's still resolvable
        # after the item is removed from this (ephemeral) queue.
        "request_id": str(uuid.uuid4()),
    }
    tester_items.append(item)
    _save_queue()
    return item


def list_items(tester_id: str) -> list[dict]:
    return sorted(_queue.get(tester_id, []), key=lambda item: item["created_at"], reverse=True)


def get_item(tester_id: str, video_id: str) -> dict:
    for item in _queue.get(tester_id, []):
        if item["video_id"] == video_id:
            return item
    raise QueueItemNotFoundError(f"Item not found in queue: {video_id}")


def update_item(tester_id: str, video_id: str, **fields) -> dict:
    item = get_item(tester_id, video_id)
    item.update(fields)
    _save_queue()
    return item


def remove_item(tester_id: str, video_id: str) -> None:
    tester_items = _queue.get(tester_id, [])
    for i, item in enumerate(tester_items):
        if item["video_id"] == video_id:
            del tester_items[i]
            _save_queue()
            return
    raise QueueItemNotFoundError(f"Item not found in queue: {video_id}")
