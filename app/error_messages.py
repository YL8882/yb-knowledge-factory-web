"""Translates raw exception text (yt-dlp, Whisper, Gemini) into a small set of
user-friendly, non-technical cause messages. The raw exception text is only ever
used here, as classification input — it must never be stored or returned as-is.
"""

_NO_TRANSCRIPT = "找不到可用的逐字稿內容，可能是影片沒有語音內容。"
_PRIVATE_OR_UNAVAILABLE = "這支影片是私人影片或已下架，無法存取。"
_YOUTUBE_RESTRICTED = "YouTube 限制存取這支影片（可能是地區限制、年齡限制或版權限制）。"
_NETWORK_ISSUE = "網路連線發生問題，請檢查網路狀態後再試一次。"
_SERVICE_UNAVAILABLE = "AI 處理服務目前無法使用或過於忙碌，請稍後再試。"
_UNKNOWN = "處理過程發生未預期的問題，請重試。"


def classify_error(raw_message: str) -> str:
    text = (raw_message or "").lower()

    if not text.strip() or "empty transcript" in text:
        return _NO_TRANSCRIPT

    if any(keyword in text for keyword in (
        "private video", "video unavailable", "video is unavailable",
        "no longer available", "removed", "does not exist", "video not found",
    )):
        return _PRIVATE_OR_UNAVAILABLE

    if any(keyword in text for keyword in (
        "sign in", "age", "region", "not available in your country",
        "blocked", "copyright",
    )):
        return _YOUTUBE_RESTRICTED

    if any(keyword in text for keyword in (
        "network", "timed out", "timeout", "connection", "resolve", "dns", "unreachable",
        "getaddrinfo", "socket", "max retries exceeded", "failed to establish",
    )):
        return _NETWORK_ISSUE

    if any(keyword in text for keyword in (
        "quota", "429", "resource_exhausted", "503", "overloaded", "rate limit",
        "api key", "permission", "unauthorized", "401", "403",
    )):
        return _SERVICE_UNAVAILABLE

    return _UNKNOWN
