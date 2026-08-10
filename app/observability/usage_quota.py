"""Feature 004 — 30秒快速學習 Usage Quota Foundation (Non-Blocking Usage
Counter).

Tracks a lifetime count — never reset by UTC date rollover or server
restart — of successful Knowledge Outline (30秒快速學習) generations for
this local installation. Pure measurement: nothing in this module blocks or
limits a call; enforcement (a paywall) is explicitly out of scope for this
Feature.

`instance_id` identifies "this local installation", not an individual human
user — the product has no login/account system yet. Multiple browser tabs
or devices hitting the same local server share one instance_id and one
counter by design.

Stored separately from daily_report.json (outputs/reports/usage_quota.json)
because daily_report.json resets every UTC day (see daily_report.py's
_ensure_today()) and this counter must never reset. Reuses logger.py's
locked read-modify-write and feature-flag/failure-swallowing behavior —
same Sprint 8.5A Engineering Rule as the rest of app/observability/.
"""

import uuid

from . import logger

_FILENAME = "usage_quota.json"
_KNOWLEDGE_OUTLINE_KEY = "knowledge_outline_lifetime_count"


def record_knowledge_outline_success() -> None:
    """Call exactly once per successful (cache-miss, Gemini-succeeded)
    Knowledge Outline generation. Best-effort — never raises.
    """
    def mutate(data: dict) -> dict:
        if "instance_id" not in data:
            data["instance_id"] = str(uuid.uuid4())
            data["created_at"] = logger.now_iso()
        data[_KNOWLEDGE_OUTLINE_KEY] = data.get(_KNOWLEDGE_OUTLINE_KEY, 0) + 1
        data["last_updated"] = logger.now_iso()
        return data

    logger.update_json_file(_FILENAME, mutate)


def get_knowledge_outline_usage() -> dict:
    """Read-only snapshot for the usage API. Zeros/None if no Knowledge
    Outline has ever succeeded yet (file doesn't exist).
    """
    data = logger.read_json_file(_FILENAME)
    return {
        "instance_id": data.get("instance_id"),
        "knowledge_outline_lifetime_count": data.get(_KNOWLEDGE_OUTLINE_KEY, 0),
        "last_updated": data.get("last_updated"),
    }
