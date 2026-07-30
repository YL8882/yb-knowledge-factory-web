import json
from datetime import datetime, timezone
from pathlib import Path

MAX_QUEUE_SIZE = 100

QUEUE_FILE = Path(__file__).parent.parent / "outputs" / "queue.json"


class QueueFullError(Exception):
    pass


class DuplicateVideoError(Exception):
    pass


class QueueItemNotFoundError(Exception):
    pass


def _write_queue_file(items: list[dict]) -> None:
    try:
        QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        QUEUE_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _load_queue() -> list[dict]:
    if not QUEUE_FILE.exists():
        return []
    try:
        items = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    # Recover items left frozen mid-"Transcribing"/"Generating" by a server restart
    # that killed the background task doing the work — otherwise nothing will ever
    # move them again, and the UI shows a progress bar forever with no file produced.
    # Reset to the last known-good, retryable state (same states the live error
    # handlers already fall back to when a request fails outright).
    changed = False
    for item in items:
        if item.get("status") in ("Downloading", "Transcribing"):
            item["status"] = "Queued"
            changed = True
        elif item.get("status") == "Generating":
            item["status"] = "Transcript Ready"
            changed = True

    if changed:
        _write_queue_file(items)

    return items


def _save_queue() -> None:
    _write_queue_file(_queue)


_queue: list[dict] = _load_queue()


def add_item(video_id: str, title: str, url: str) -> dict:
    if any(item["video_id"] == video_id for item in _queue):
        raise DuplicateVideoError(f"Video already in queue: {video_id}")

    if len(_queue) >= MAX_QUEUE_SIZE:
        raise QueueFullError("Queue is full")

    item = {
        "video_id": video_id,
        "title": title,
        "url": url,
        "status": "Queued",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _queue.append(item)
    _save_queue()
    return item


def list_items() -> list[dict]:
    return sorted(_queue, key=lambda item: item["created_at"], reverse=True)


def get_item(video_id: str) -> dict:
    for item in _queue:
        if item["video_id"] == video_id:
            return item
    raise QueueItemNotFoundError(f"Item not found in queue: {video_id}")


def update_item(video_id: str, **fields) -> dict:
    item = get_item(video_id)
    item.update(fields)
    _save_queue()
    return item


def remove_item(video_id: str) -> None:
    for i, item in enumerate(_queue):
        if item["video_id"] == video_id:
            del _queue[i]
            _save_queue()
            return
    raise QueueItemNotFoundError(f"Item not found in queue: {video_id}")
