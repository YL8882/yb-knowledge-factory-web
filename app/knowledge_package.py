import re
import zipfile
from pathlib import Path

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def build_package(dest_dir: Path, title: str, video_id: str, transcript_path: str, study_note_path: str) -> Path:
    """Zips the already-generated Transcript.md + Study_Note.md for one video
    into a single archive laid out as `<Video Title>/Transcript.md` +
    `<Video Title>/Study_Note.md` — the Knowledge Package Export shape.
    Export Layer only: reads existing output files, does not regenerate or
    otherwise touch the Transcript / Study Note pipeline.
    """
    safe_title = _sanitize_filename(title)
    zip_path = dest_dir / f"{safe_title}_{video_id}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(transcript_path, arcname=f"{safe_title}/Transcript.md")
        zf.write(study_note_path, arcname=f"{safe_title}/Study_Note.md")

    return zip_path
