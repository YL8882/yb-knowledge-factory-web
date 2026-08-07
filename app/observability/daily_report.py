"""Product Intelligence Foundation — Phase 5 (Runtime Report).

Unlike a batch job that recomputes from the raw logs once a day, this module
is updated incrementally: every apply_*_event() call folds one just-logged
event straight into outputs/reports/daily_report.json (Sprint 8.5A
Architecture Review decision — see Engineering Kickoff Sprint 8.5). Each
metrics module (runtime_metrics.py first; cost/cache/error_metrics.py in
later Sprint 8.5A tasks) calls the matching apply_*_event() right after it
logs its own event.

The report always reflects "today" (UTC) — if the stored date doesn't match
today, the aggregate resets before applying the new event. Historical days
are not retained here; the JSONL logs under outputs/logs/ are the durable
source of truth if a past day's numbers are ever needed.
"""

from datetime import datetime, timezone

from . import logger


def _ensure_today(data: dict) -> dict:
    today = datetime.now(timezone.utc).date().isoformat()
    if data.get("date") != today:
        return {"date": today}
    return data


def apply_runtime_event(event: dict) -> None:
    """event: the same record runtime_metrics.log_stage() just appended to
    runtime.jsonl (stage / status / duration_seconds).
    """
    def mutate(data: dict) -> dict:
        data = _ensure_today(data)

        stage = event.get("stage") or "unknown"
        status = event.get("status") or "unknown"
        duration = event.get("duration_seconds")

        runtime = data.setdefault("runtime", {})
        bucket = runtime.setdefault(stage, {
            "count": 0,
            "success": 0,
            "error": 0,
            "total_duration_seconds": 0.0,
            "average_duration_seconds": None,
        })

        bucket["count"] += 1
        if status == "success":
            bucket["success"] += 1
        elif status == "error":
            bucket["error"] += 1

        if isinstance(duration, (int, float)):
            bucket["total_duration_seconds"] += duration
            bucket["average_duration_seconds"] = round(
                bucket["total_duration_seconds"] / bucket["count"], 3
            )

        data["transcript_generated"] = runtime.get("transcript", {}).get("success", 0)
        data["study_notes_generated"] = runtime.get("study_note", {}).get("success", 0)

        # Study Package cost (Sprint 8.5A Task 2 follow-up): finalizes on
        # every "study_note" success — same trigger as study_notes_generated
        # above, so the two counts always stay equal by construction, incl.
        # idempotent Stage-Guard repeat calls counting again (same accepted
        # behavior as study_notes_generated; not deduplicated per video).
        # Pulls whatever cost apply_usage_event() below has accumulated for
        # this request_id (quick_summary + study_note calls only) and clears
        # it — 0.0 if nothing accumulated (e.g. a fully cache-served run).
        if stage == "study_note" and status == "success":
            request_id = event.get("request_id")
            pending = data.setdefault("_pending_package_cost", {})
            package_cost = pending.pop(request_id, 0.0) if request_id else 0.0

            study_package = data.setdefault("study_package", {
                "count": 0, "total_cost": 0.0, "average_cost": 0.0, "currency": logger.CURRENCY,
            })
            study_package["count"] += 1
            study_package["total_cost"] = round(study_package["total_cost"] + package_cost, 6)
            study_package["average_cost"] = round(
                study_package["total_cost"] / study_package["count"], 6
            )

        data["updated_at"] = logger.now_iso()
        return data

    logger.update_json_file("daily_report.json", mutate)


def apply_usage_event(event: dict) -> None:
    """event: the same record cost_metrics.log_usage() just appended to
    gemini_usage.jsonl (model / artifact_type / estimated_cost).
    """
    def mutate(data: dict) -> dict:
        data = _ensure_today(data)

        cost = event.get("estimated_cost")
        model = event.get("model") or "unknown"
        artifact_type = event.get("artifact_type") or "unknown"
        request_id = event.get("request_id")

        usage = data.setdefault("usage", {
            "api_calls": 0, "estimated_cost": 0.0, "currency": logger.CURRENCY,
            "by_model": {}, "by_artifact_type": {},
        })
        usage["api_calls"] += 1
        if isinstance(cost, (int, float)):
            usage["estimated_cost"] = round(usage["estimated_cost"] + cost, 6)

        for key, bucket_name in ((model, "by_model"), (artifact_type, "by_artifact_type")):
            bucket = usage[bucket_name].setdefault(
                key, {"api_calls": 0, "estimated_cost": 0.0, "currency": logger.CURRENCY}
            )
            bucket["api_calls"] += 1
            if isinstance(cost, (int, float)):
                bucket["estimated_cost"] = round(bucket["estimated_cost"] + cost, 6)

        # Study Package cost (Sprint 8.5A Task 2 follow-up): only the two
        # Gemini calls that happen automatically as part of the core MVP
        # pipeline (quick_summary during Transcript, study_note during Study
        # Note) accumulate here — the 5 optional Learning Model artifacts are
        # user-triggered independently and may run much later or never, so
        # including them would make "cost per package" unpredictable rather
        # than a stable MVP baseline. Finalized in apply_runtime_event() above
        # when the study_note stage succeeds.
        if request_id and artifact_type in ("quick_summary", "study_note") and isinstance(cost, (int, float)):
            pending = data.setdefault("_pending_package_cost", {})
            pending[request_id] = round(pending.get(request_id, 0.0) + cost, 6)

        # Top-level convenience fields — same pattern as
        # transcript_generated/study_notes_generated in apply_runtime_event().
        data["api_calls"] = usage["api_calls"]
        data["estimated_cost"] = usage["estimated_cost"]
        data["currency"] = logger.CURRENCY
        data["updated_at"] = logger.now_iso()
        return data

    logger.update_json_file("daily_report.json", mutate)


def average_cost_for_artifact_type(artifact_type: str):
    """Today's running average estimated_cost for one artifact_type, read
    from usage.by_artifact_type (populated by apply_usage_event() above).
    Returns None if there's no usage data yet for it today — cache_metrics.py
    falls back to a static estimate in that case. Read-only, unlocked
    snapshot (see logger.read_json_file()).
    """
    data = logger.read_json_file("daily_report.json")
    bucket = data.get("usage", {}).get("by_artifact_type", {}).get(artifact_type)
    if not bucket or not bucket.get("api_calls"):
        return None
    return round(bucket["estimated_cost"] / bucket["api_calls"], 6)


def apply_cache_event(event: dict) -> None:
    """event: the same record cache_metrics.log_cache_event() just appended
    to cache.jsonl (artifact_type / result / estimated_cost_saved).
    """
    def mutate(data: dict) -> dict:
        data = _ensure_today(data)

        artifact_type = event.get("artifact_type") or "unknown"
        result = event.get("result")
        saved = event.get("estimated_cost_saved")

        cache = data.setdefault("cache", {
            "hits": 0, "misses": 0, "hit_rate": None,
            "estimated_cost_saved": 0.0, "currency": logger.CURRENCY,
            "by_artifact_type": {},
        })

        bucket = cache["by_artifact_type"].setdefault(artifact_type, {"hits": 0, "misses": 0})

        if result == "hit":
            cache["hits"] += 1
            bucket["hits"] += 1
            if isinstance(saved, (int, float)):
                cache["estimated_cost_saved"] = round(cache["estimated_cost_saved"] + saved, 6)
        elif result == "miss":
            cache["misses"] += 1
            bucket["misses"] += 1

        total = cache["hits"] + cache["misses"]
        cache["hit_rate"] = round(cache["hits"] / total, 4) if total else None

        data["updated_at"] = logger.now_iso()
        return data

    logger.update_json_file("daily_report.json", mutate)


def apply_error_event(event: dict) -> None:
    """event: the same record error_metrics.log_error() just appended to
    errors.jsonl (stage / artifact_type / retry_count).
    """
    def mutate(data: dict) -> dict:
        data = _ensure_today(data)

        stage = event.get("stage") or "unknown"

        errors = data.setdefault("errors", {"count": 0, "by_stage": {}})
        errors["count"] += 1
        errors["by_stage"][stage] = errors["by_stage"].get(stage, 0) + 1

        data["error_count"] = errors["count"]
        data["updated_at"] = logger.now_iso()
        return data

    logger.update_json_file("daily_report.json", mutate)
