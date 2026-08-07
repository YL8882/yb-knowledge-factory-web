"""Shared low-level infrastructure for the Product Intelligence Foundation
(Sprint 8.5A). Every observability module (runtime_metrics, cost_metrics,
cache_metrics, error_metrics, daily_report) writes through this module —
never directly through `open()` — so the feature flag, locking and
failure-swallowing rules only need to be implemented once.

Engineering Rules (Sprint 8.5A, approved):
- Feature Flag Friendly: set PRODUCT_INTELLIGENCE_ENABLED=false to disable
  all observability writes without touching call sites elsewhere in the app.
- Observability must never interrupt the normal pipeline: every public
  function here swallows its own failures instead of raising.
"""

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

_OUTPUTS_DIR = Path(__file__).parent.parent.parent / "outputs"
_LOGS_DIR = _OUTPUTS_DIR / "logs"
_REPORTS_DIR = _OUTPUTS_DIR / "reports"

# Shared here (rather than in cost_metrics.py) so daily_report.py can also
# reference it without an observability-internal circular import.
CURRENCY = "USD"

_locks: dict[str, threading.Lock] = {}
_locks_guard = threading.Lock()


def is_enabled() -> bool:
    return os.environ.get("PRODUCT_INTELLIGENCE_ENABLED", "true").strip().lower() not in (
        "0", "false", "no", "off",
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _lock_for(path: Path) -> threading.Lock:
    key = str(path)
    with _locks_guard:
        lock = _locks.get(key)
        if lock is None:
            lock = threading.Lock()
            _locks[key] = lock
        return lock


def append_jsonl(filename: str, record: dict) -> None:
    """Best-effort append of one JSON record as a line under outputs/logs/.
    Never raises — a logging failure must never interrupt the pipeline.
    """
    if not is_enabled():
        return
    path = _LOGS_DIR / filename
    lock = _lock_for(path)
    try:
        with lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8", newline="") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_jsonl(filename: str) -> list[dict]:
    """Best-effort read of every line in a JSONL file under outputs/logs/.
    Returns [] if the file doesn't exist, is disabled, or can't be read.
    Malformed individual lines are skipped rather than failing the whole
    read. Unlocked — same read-only-snapshot trade-off as read_json_file().
    """
    if not is_enabled():
        return []
    path = _LOGS_DIR / filename
    rows = []
    try:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception:
        return []
    return rows


def read_json_file(filename: str) -> dict:
    """Best-effort read of a JSON object file under outputs/reports/. Returns
    {} if the file doesn't exist, is disabled, or can't be parsed. Unlocked —
    a snapshot read that may (rarely) race a concurrent update_json_file()
    write; acceptable for this package's read-only lookups (e.g.
    cache_metrics estimating cost saved from today's running average).
    """
    if not is_enabled():
        return {}
    path = _REPORTS_DIR / filename
    try:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def update_json_file(filename: str, mutate) -> None:
    """Best-effort locked read-modify-write of a JSON object file under
    outputs/reports/. `mutate(data: dict) -> dict` receives the current
    contents (empty dict if the file doesn't exist yet or is unreadable) and
    returns the updated contents to persist. The lock covers the entire
    read-modify-write so concurrent callers can't lose each other's updates.
    Never raises.
    """
    if not is_enabled():
        return
    path = _REPORTS_DIR / filename
    lock = _lock_for(path)
    try:
        with lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            data = {}
            if path.exists():
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    data = {}
            data = mutate(data)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
