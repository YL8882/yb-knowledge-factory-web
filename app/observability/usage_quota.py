"""Feature 004 — 30秒快速學習 Usage Quota Foundation (Non-Blocking Usage
Counter).

Tracks a lifetime count — never reset by UTC date rollover or server
restart — of successful Knowledge Outline (30秒快速學習) generations.
Pure measurement: nothing in this module blocks or limits a call;
enforcement (a paywall) is explicitly out of scope for this Feature.

T4.1 (Per-Tester Data Isolation): the counter is scoped per `tester_id`
(Local Mode always passes "local") rather than shared across the whole
installation — each Beta Tester's usage must be visible independently and
must never consume or affect another tester's quota. `instance_id` is now
generated once per tester (first successful call) rather than once per
installation.

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

LOCAL_TESTER_ID = "local"


def _migrate_legacy(data: dict) -> dict:
    """Data predating per-tester isolation has the counter fields directly
    at the top level (one shared installation-wide counter). It was all
    written before Beta Testers existed, so it belongs entirely to Local
    Mode (tester_id "local") — never surfaced to an authenticated tester.
    """
    if _KNOWLEDGE_OUTLINE_KEY in data or "instance_id" in data:
        return {LOCAL_TESTER_ID: data}
    return data


def record_knowledge_outline_success(tester_id: str) -> None:
    """Call exactly once per successful (cache-miss, Gemini-succeeded)
    Knowledge Outline generation. Best-effort — never raises.
    """
    def mutate(data: dict) -> dict:
        data = _migrate_legacy(data)
        tester_data = data.setdefault(tester_id, {})
        if "instance_id" not in tester_data:
            tester_data["instance_id"] = str(uuid.uuid4())
            tester_data["created_at"] = logger.now_iso()
        tester_data[_KNOWLEDGE_OUTLINE_KEY] = tester_data.get(_KNOWLEDGE_OUTLINE_KEY, 0) + 1
        tester_data["last_updated"] = logger.now_iso()
        return data

    logger.update_json_file(_FILENAME, mutate)


def get_knowledge_outline_usage(tester_id: str) -> dict:
    """Read-only snapshot for the usage API. Zeros/None if this tester has
    never had a successful Knowledge Outline generation yet — never
    inherits another tester's (or Local Mode's) count.
    """
    data = _migrate_legacy(logger.read_json_file(_FILENAME))
    tester_data = data.get(tester_id, {})
    return {
        "instance_id": tester_data.get("instance_id"),
        "knowledge_outline_lifetime_count": tester_data.get(_KNOWLEDGE_OUTLINE_KEY, 0),
        "last_updated": tester_data.get("last_updated"),
    }
