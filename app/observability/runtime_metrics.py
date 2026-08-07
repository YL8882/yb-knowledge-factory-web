"""Product Intelligence Foundation — Phase 1 (Runtime Intelligence).

Records one line per pipeline stage completion to outputs/logs/runtime.jsonl,
then folds it into outputs/reports/daily_report.json via daily_report.py.

Stages (Sprint 8.5A Task 1 scope): "queue" (time spent in the internal
pipeline work queue before a worker picks it up), "transcript", "study_note",
"download" (a user downloading a completed Transcript/Study Note file).
"""

from datetime import datetime

from . import daily_report, logger


def _isoformat(value) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def log_stage(*, request_id, video_id: str, stage: str, start_time, end_time, status: str) -> None:
    """Best-effort — never raises, per Sprint 8.5A Engineering Rule #4
    (observability must never interrupt the normal pipeline).
    """
    try:
        duration_seconds = None
        if isinstance(start_time, datetime) and isinstance(end_time, datetime):
            duration_seconds = round((end_time - start_time).total_seconds(), 3)

        record = {
            "request_id": request_id,
            "video_id": video_id,
            "stage": stage,
            "start_time": _isoformat(start_time),
            "end_time": _isoformat(end_time),
            "duration_seconds": duration_seconds,
            "status": status,
            "logged_at": logger.now_iso(),
        }

        logger.append_jsonl("runtime.jsonl", record)
        daily_report.apply_runtime_event(record)
    except Exception:
        pass
