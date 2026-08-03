import re
import zipfile
from pathlib import Path

# Allowlist-based sanitize: keeps CJK ideographs, Latin letters, digits,
# whitespace, and a small set of structurally-safe punctuation (-, _, (), []).
# Everything else — emoji, control characters, Windows-reserved characters
# (\/:*?"<>|), zero-width joiners, and any other symbol — is dropped rather
# than replaced, since Windows Explorer's built-in zip extractor treats an
# entire archive as invalid if any internal path contains a character outside
# the Basic Multilingual Plane (most emoji), even though the zip itself is
# spec-valid (confirmed via zipfile.testzip() and WinRAR opening it fine).
_DISALLOWED_FILENAME_CHARS = re.compile(
    r'[^一-鿿㐀-䶿A-Za-z0-9 \-_()\[\]]'
)


class IncompletePackageError(Exception):
    """Raised by build_bulk_package() when any candidate item is missing its
    Transcript.md or Study_Note.md on disk. Carries a list of
    (video_id, title, missing_filename) tuples as args[0].
    """
    pass


def _sanitize_filename(name: str) -> str:
    return _DISALLOWED_FILENAME_CHARS.sub("", name).strip()


def _write_video_folder(zf: zipfile.ZipFile, folder_name: str, transcript_path: str, study_note_path: str) -> None:
    zf.write(transcript_path, arcname=f"{folder_name}/Transcript.md")
    zf.write(study_note_path, arcname=f"{folder_name}/Study_Note.md")


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
        _write_video_folder(zf, safe_title, transcript_path, study_note_path)

    return zip_path


def build_bulk_package(dest_dir: Path, items: list[dict]) -> Path:
    """Zips multiple videos' Transcript.md + Study_Note.md into ONE archive,
    each video under its own `<Video Title>_<video_id>/` folder — the
    video_id suffix (unlike the single-video build_package() above) guards
    against two videos with the same or similar title overwriting each
    other's folder inside the shared zip.

    All-or-nothing: verifies every item's transcript_path/study_note_path
    actually exists on disk BEFORE writing anything, and raises
    IncompletePackageError instead of producing a zip missing some folders
    if any item turns out to be incomplete.
    """
    missing = []
    for item in items:
        transcript_path = item.get("transcript_path")
        study_note_path = item.get("study_note_path")
        if not transcript_path or not Path(transcript_path).exists():
            missing.append((item["video_id"], item["title"], "Transcript.md"))
        if not study_note_path or not Path(study_note_path).exists():
            missing.append((item["video_id"], item["title"], "Study_Note.md"))

    if missing:
        raise IncompletePackageError(missing)

    zip_path = dest_dir / "YB_Knowledge_Packages.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items:
            folder_name = f"{_sanitize_filename(item['title'])}_{item['video_id']}"
            _write_video_folder(zf, folder_name, item["transcript_path"], item["study_note_path"])

    return zip_path
