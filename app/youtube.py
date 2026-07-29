import re

import yt_dlp

_VIDEO_ID_PATTERN = re.compile(
    r"^(?:https?://)?(?:www\.)?"
    r"(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)"
    r"([a-zA-Z0-9_-]{11})"
)


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
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
    except Exception as exc:
        raise VideoMetadataError(str(exc)) from exc

    return {
        "video_id": info.get("id", video_id),
        "title": info.get("title", "Untitled"),
    }
