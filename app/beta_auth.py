"""Beta Token Authentication Foundation (T1 of the External Beta Deployment
Architecture — Closed Beta, 5-10 invited testers, no login/account/database).

This module only resolves *who is asking* (`tester_id`) from a pre-shared
Beta Token. It intentionally does not touch queue_store / history_store /
usage_quota storage paths, and this dependency is not wired into any
existing route yet — that wiring is T3's job. T1 only introduces this
module plus one new, isolated diagnostic endpoint (`GET /api/beta/whoami`
in main.py) so the whole flow can be exercised independently.

Local dev backward compatibility: when BETA_TOKENS isn't set (the normal
case on this machine today), get_tester_id() always returns LOCAL_TESTER_ID
without looking at cookies/query params at all — no behavior change, no
possibility of a 403, for anyone running `python run.py` without opting
into Beta mode.
"""

import os

from fastapi import HTTPException, Request, Response

LOCAL_TESTER_ID = "local"
COOKIE_NAME = "ownlearn_beta_token"

# ~180 days — long-lived on purpose: there is no login to fall back on, so
# losing this cookie means asking the Main Developer to resend the original
# invite link (see Architecture Design, "Beta Token 遺失時如何處理").
_COOKIE_MAX_AGE_SECONDS = 180 * 24 * 60 * 60


def _parse_beta_tokens() -> set[str]:
    """BETA_TOKENS is a comma-separated list, each entry either a bare token
    or `token:nickname` (nickname is for the operator's own reference only,
    e.g. distinguishing testers in support conversations — never compared
    against or exposed). Missing/empty/whitespace-only -> empty set, which
    is what is_beta_mode_enabled() treats as "Beta mode off".
    """
    raw = os.environ.get("BETA_TOKENS", "")
    tokens: set[str] = set()
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        token = entry.split(":", 1)[0].strip()
        if token:
            tokens.add(token)
    return tokens


def is_beta_mode_enabled() -> bool:
    return bool(_parse_beta_tokens())


def get_tester_id(request: Request, response: Response) -> str:
    """FastAPI dependency. Resolution order: local-mode bypass -> valid
    cookie -> valid `?beta=` query param (bootstraps/refreshes the cookie)
    -> 403. tester_id is never accepted from a client-supplied path/body
    param anywhere — this function is the only source of truth for it.
    """
    allowed_tokens = _parse_beta_tokens()
    if not allowed_tokens:
        return LOCAL_TESTER_ID

    cookie_token = request.cookies.get(COOKIE_NAME)
    if cookie_token and cookie_token in allowed_tokens:
        return cookie_token

    query_token = request.query_params.get("beta")
    if query_token and query_token in allowed_tokens:
        response.set_cookie(
            key=COOKIE_NAME,
            value=query_token,
            max_age=_COOKIE_MAX_AGE_SECONDS,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return query_token

    raise HTTPException(status_code=403, detail="Invalid or missing beta token")
