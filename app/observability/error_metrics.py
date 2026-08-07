"""Product Intelligence Foundation — Phase 4 (Error Intelligence).

Records one line per pipeline failure to outputs/logs/errors.jsonl, then
folds it into outputs/reports/daily_report.json via daily_report.py.

retry_count is computed at log time from errors.jsonl itself — how many
prior errors already exist today for the same (video_id, stage) combo —
rather than adding a new counter field to queue_store, per the Sprint 8.5A
Architecture Review (Task 4 Proposal decision).
"""

from datetime import datetime, timezone

from . import daily_report, logger


def _prior_error_count_today(video_id, stage) -> int:
    if not video_id or not stage:
        return 0
    today = datetime.now(timezone.utc).date().isoformat()
    count = 0
    for row in logger.read_jsonl("errors.jsonl"):
        if row.get("video_id") != video_id or row.get("stage") != stage:
            continue
        if str(row.get("logged_at") or "").startswith(today):
            count += 1
    return count


def log_error(
    *, request_id, video_id, stage: str, exception: str, artifact_type: str | None = None,
) -> None:
    """Best-effort — never raises, per Sprint 8.5A Engineering Rule #4
    (observability must never interrupt the normal pipeline).
    """
    try:
        retry_count = _prior_error_count_today(video_id, stage)

        record = {
            "request_id": request_id,
            "video_id": video_id,
            "stage": stage,
            "artifact_type": artifact_type,
            "exception": exception,
            "retry_count": retry_count,
            "logged_at": logger.now_iso(),
        }

        logger.append_jsonl("errors.jsonl", record)
        daily_report.apply_error_event(record)
    except Exception:
        pass
