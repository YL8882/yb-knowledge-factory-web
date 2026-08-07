"""Product Intelligence Foundation — Phase 3 (Cache Intelligence).

Records one line per cache check (hit or miss) to outputs/logs/cache.jsonl,
then folds it into outputs/reports/daily_report.json via daily_report.py.

Estimated Cost Saved on a hit uses today's real running average cost for
that artifact_type (from cost_metrics/daily_report's usage.by_artifact_type,
Sprint 8.5A Task 2) when available, falling back to the MVP-period averages
already recorded in docs/Product_Strategy/Cost_Analysis.md for a day with no
usage data yet. A miss saves nothing.
"""

from . import daily_report, logger

# Fallback only — used before any real gemini_usage data exists yet today.
# Source: docs/Product_Strategy/Cost_Analysis.md Section 5 (Study Note) plus
# a rough split of its Transcript figure across quick_summary vs. the 5
# optional Learning Model artifacts, none of which had a baseline yet.
_FALLBACK_COST_ESTIMATE = {
    "transcript": 0.30,
    "quick_summary": 0.02,
    "study_note": 0.44,
    "knowledge_outline": 0.05,
    "learning_blueprint": 0.05,
    "teach_back": 0.05,
    "action_list": 0.03,
    "review": 0.05,
}


def _estimate_saved_cost(artifact_type: str) -> float:
    try:
        average = daily_report.average_cost_for_artifact_type(artifact_type)
        if average is not None:
            return average
    except Exception:
        pass
    return _FALLBACK_COST_ESTIMATE.get(artifact_type, 0.0)


def log_cache_event(*, request_id, video_id, artifact_type: str, hit: bool) -> None:
    """Best-effort — never raises, per Sprint 8.5A Engineering Rule #4
    (observability must never interrupt the normal pipeline).
    """
    try:
        estimated_cost_saved = round(_estimate_saved_cost(artifact_type), 6) if hit else 0.0

        record = {
            "request_id": request_id,
            "video_id": video_id,
            "artifact_type": artifact_type,
            "result": "hit" if hit else "miss",
            "estimated_cost_saved": estimated_cost_saved,
            "currency": logger.CURRENCY,
            "logged_at": logger.now_iso(),
        }

        logger.append_jsonl("cache.jsonl", record)
        daily_report.apply_cache_event(record)
    except Exception:
        pass
