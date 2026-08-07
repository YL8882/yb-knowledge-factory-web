"""Product Intelligence Foundation — Phase 2 (Cost Intelligence).

Records one line per Gemini API call to outputs/logs/gemini_usage.jsonl,
then folds it into outputs/reports/daily_report.json via daily_report.py.

Pricing constants below are Gemini 2.5 Flash's published per-1,000,000-token
rates at the time this was written — NOT pulled live from Google Cloud
Billing. Cost_Analysis.md (docs/Product_Strategy/) already flags exact rate
confirmation against the Billing console as an open item; if the actual
billed rate differs, correct these two constants directly — nothing else in
this module needs to change.
"""

from . import daily_report, logger

# USD per 1,000,000 tokens.
INPUT_COST_PER_MILLION_TOKENS = 0.30
# Includes "thinking" tokens — gemini_client._generate_content() already
# folds thoughts_token_count into the output_tokens it passes to
# log_usage() below, since Gemini bills thinking tokens at the output rate.
OUTPUT_COST_PER_MILLION_TOKENS = 2.50


def estimate_cost(input_tokens, output_tokens):
    try:
        return round(
            (input_tokens or 0) / 1_000_000 * INPUT_COST_PER_MILLION_TOKENS
            + (output_tokens or 0) / 1_000_000 * OUTPUT_COST_PER_MILLION_TOKENS,
            6,
        )
    except Exception:
        return None


def log_usage(
    *, request_id, video_id, model: str, artifact_type: str,
    input_tokens, output_tokens, processing_time_seconds,
) -> None:
    """Best-effort — never raises, per Sprint 8.5A Engineering Rule #4
    (observability must never interrupt the normal pipeline).
    """
    try:
        estimated_cost = estimate_cost(input_tokens, output_tokens)

        record = {
            "request_id": request_id,
            "video_id": video_id,
            "artifact_type": artifact_type,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost": estimated_cost,
            "currency": logger.CURRENCY,
            "processing_time_seconds": processing_time_seconds,
            "logged_at": logger.now_iso(),
        }

        logger.append_jsonl("gemini_usage.jsonl", record)
        daily_report.apply_usage_event(record)
    except Exception:
        pass
