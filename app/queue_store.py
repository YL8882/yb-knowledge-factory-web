from datetime import datetime, timezone

MAX_QUEUE_SIZE = 100


class QueueFullError(Exception):
    pass


class DuplicateVideoError(Exception):
    pass


class QueueItemNotFoundError(Exception):
    pass


_queue: list[dict] = []


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
    return item


def list_items() -> list[dict]:
    return sorted(_queue, key=lambda item: item["created_at"], reverse=True)


def remove_item(video_id: str) -> None:
    for i, item in enumerate(_queue):
        if item["video_id"] == video_id:
            del _queue[i]
            return
    raise QueueItemNotFoundError(f"Item not found in queue: {video_id}")
