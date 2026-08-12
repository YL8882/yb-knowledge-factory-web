import re

import requests

_VIDEO_ID_PATTERN = re.compile(
    r"^(?:https?://)?(?:www\.)?"
    r"(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)"
    r"([a-zA-Z0-9_-]{11})"
)

_OEMBED_URL = "https://www.youtube.com/oembed"
_OEMBED_TIMEOUT_SECONDS = 10


class InvalidYouTubeURLError(Exception):
    pass


class VideoMetadataError(Exception):
    pass


def extract_video_id(url: str) -> str:
    match = _VIDEO_ID_PATTERN.match(url.strip())
    if not match:
        raise InvalidYouTubeURLError(f"Invalid YouTube URL: {url}")
    return match.group(1)


def fetch_video_metadata(video_id: str) -> dict:
    # oEmbed is YouTube's public, unauthenticated embed-info endpoint — unlike
    # yt-dlp's player API it doesn't trigger YouTube's bot-check on datacenter IPs
    # (e.g. Railway), which is what fetch_video_metadata previously hit in production.
    watch_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        response = requests.get(
            _OEMBED_URL,
            params={"url": watch_url, "format": "json"},
            timeout=_OEMBED_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        info = response.json()
    except Exception as exc:
        raise VideoMetadataError(str(exc)) from exc

    return {
        "video_id": video_id,
        "title": info.get("title", "Untitled"),
    }
