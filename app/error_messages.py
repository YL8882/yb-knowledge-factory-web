"""Translates raw exception text (yt-dlp, Whisper, Gemini) into a small set of
user-friendly, non-technical cause messages. The raw exception text is only ever
used here, as classification input — it must never be stored or returned as-is.
"""

_NO_TRANSCRIPT = "找不到可用的逐字稿內容，可能是影片沒有語音內容。"
_PRIVATE_OR_UNAVAILABLE = "這支影片是私人影片或已下架，無法存取。"
_YOUTUBE_RESTRICTED = "YouTube 限制存取這支影片（可能是地區限制、年齡限制或版權限制）。"
_NETWORK_ISSUE = "網路連線發生問題，請檢查網路狀態後再試一次。"
_SERVICE_UNAVAILABLE = "AI 處理服務目前無法使用或過於忙碌，請稍後再試（可能是 Gemini API 額度已用完）。"
_SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT = "Learning Blueprint 服務目前無法使用或過於忙碌，請稍後再試（可能是 Gemini API 額度已用完）。"
_SERVICE_UNAVAILABLE_SOURCE = "服務目前無法使用或過於忙碌，請稍後再試。"
_CONTENT_FILTERED = "Gemini 判定這段逐字稿內容不適合產生 Study Note（可能觸發安全過濾），請嘗試其他影片。"
_UNKNOWN = "處理過程發生未預期的問題，請重試。"


def classify_error(raw_message: str, stage: str = "") -> str:
    """`stage` narrows which cause buckets are even considered — e.g. "studynote"
    errors come from the Gemini API, never from YouTube, so YouTube-specific
    buckets are skipped entirely for that stage rather than relying on keyword
    matching alone to keep them apart (a Gemini error's own JSON always contains
    a "message" field, and "message" contains the substring "age" — matching a
    naive "age" keyword meant for YouTube's age-restriction message).
    """
    text = (raw_message or "").lower()

    if not text.strip() or "empty transcript" in text:
        return _NO_TRANSCRIPT

    # Quota / rate-limit / auth errors can come from either yt-dlp or the Gemini
    # API — check these before the YouTube-specific buckets below so a Gemini
    # error is never misread as a YouTube restriction. Only "studynote" (Gemini
    # calls) gets the Gemini-specific wording — "download"/"transcript" never
    # touch Gemini (yt-dlp and local faster_whisper respectively), so a 429/403
    # from YouTube itself (e.g. subtitle download rate-limited) must not be
    # blamed on Gemini quota.
    if any(keyword in text for keyword in (
        "quota", "429", "resource_exhausted", "503", "overloaded", "rate limit",
        "api key", "unauthorized", "401", "403",
    )):
        if stage == "studynote":
            return _SERVICE_UNAVAILABLE
        if stage == "learning_blueprint":
            return _SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT
        return _SERVICE_UNAVAILABLE_SOURCE

    if stage in ("studynote", "learning_blueprint"):
        if any(keyword in text for keyword in ("safety", "blocked", "recitation", "prohibited_content")):
            return _CONTENT_FILTERED
        return _UNKNOWN

    if any(keyword in text for keyword in (
        "private video", "video unavailable", "video is unavailable",
        "no longer available", "removed", "does not exist", "video not found",
    )):
        return _PRIVATE_OR_UNAVAILABLE

    if any(keyword in text for keyword in (
        "sign in to confirm", "age-restrict", "age restrict",
        "not available in your country", "geo-restrict", "copyright claim", "blocked it in your country",
    )):
        return _YOUTUBE_RESTRICTED

    if any(keyword in text for keyword in (
        "network", "timed out", "timeout", "connection", "resolve", "dns", "unreachable",
        "getaddrinfo", "socket", "max retries exceeded", "failed to establish",
    )):
        return _NETWORK_ISSUE

    return _UNKNOWN
