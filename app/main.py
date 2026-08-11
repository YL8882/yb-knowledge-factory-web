import asyncio
import queue as pyqueue
import shutil
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.background import BackgroundTask

import error_messages
import gemini_client
import history_store
import knowledge_outline
import knowledge_package
import queue_store
import study_note
import transcript as transcript_service
import youtube
from observability import cache_metrics, error_metrics, runtime_metrics, usage_quota

load_dotenv()

app = FastAPI()

# Lets the Chrome extension's content script (running on youtube.com) call
# this local API — content-script fetch is bound by the same CORS rules as
# a page script, so without this the browser blocks the request before it
# ever reaches FastAPI. Scoped to youtube.com + POST only, not "*", since
# this is a local single-user backend rather than a public API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.youtube.com"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

# Serve static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class AddVideoRequest(BaseModel):
    url: str


class CaptureRequest(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
async def home():
    html_path = Path(__file__).parent / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/history", response_class=HTMLResponse)
async def history_page():
    html_path = Path(__file__).parent / "templates" / "history.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/api/queue")
async def get_queue():
    """Queue list — items augmented (Sprint 5, Task 5) with derived
    transcript_exists / study_note_exists flags, same pattern as
    GET /api/history (Task 3), so the Queue page can gate the "download
    package" button on actual disk state rather than trusting queue_store's
    possibly-stale path fields. queue_store.py itself is untouched — this is
    a read-time augmentation only, identical in shape to get_history() above.
    """
    items = []
    for item in queue_store.list_items():
        items.append({
            **item,
            "transcript_exists": transcript_service.find_cached_transcript(item["video_id"]) is not None,
            "study_note_exists": study_note.find_cached_study_note(item["video_id"]) is not None,
        })
    return {"items": items}


@app.get("/api/history")
async def get_history():
    """Knowledge Library (Sprint 5, Task 3): augments each history_store entry
    with derived (not stored) transcript_exists / study_note_exists flags, so
    the History page can show per-video status without history_store.py
    tracking file paths itself. Builds new dicts rather than mutating the
    entries history_store.list_entries() returns, since those are the same
    objects held in its live in-memory list.
    """
    items = []
    for entry in history_store.list_entries():
        items.append({
            **entry,
            "transcript_exists": transcript_service.find_cached_transcript(entry["video_id"]) is not None,
            "study_note_exists": study_note.find_cached_study_note(entry["video_id"]) is not None,
        })
    return {"items": items}


@app.post("/api/capture")
async def capture_video(request: CaptureRequest):
    """Used by the Chrome extension's "YB Learn" button. Validates the URL
    only — deliberately does not touch queue_store, history_store, or the
    transcript/study-note pipeline; that wiring is a later sprint's job.
    """
    try:
        video_id = youtube.extract_video_id(request.url)
    except youtube.InvalidYouTubeURLError:
        raise HTTPException(status_code=400, detail="無效的 YouTube 網址")
    return {"status": "success", "video_id": video_id}


@app.post("/api/queue")
async def add_to_queue(request: AddVideoRequest):
    try:
        video_id = youtube.extract_video_id(request.url)
    except youtube.InvalidYouTubeURLError:
        raise HTTPException(status_code=400, detail="無效的 YouTube 網址")

    try:
        metadata = youtube.fetch_video_metadata(video_id)
    except youtube.VideoMetadataError:
        raise HTTPException(status_code=400, detail="無法取得影片資訊")

    try:
        item = queue_store.add_item(
            video_id=video_id,
            title=metadata["title"],
            url=request.url.strip(),
        )
    except queue_store.DuplicateVideoError:
        raise HTTPException(status_code=409, detail="此影片已存在 Queue")
    except queue_store.QueueFullError:
        raise HTTPException(status_code=400, detail="Queue 已滿，請先完成或刪除部分項目")

    # Recorded independently of the (ephemeral) Queue so it's still traceable back
    # to the YB channel after the user deletes it from the Queue to free up space.
    # request_id mirrored from the Queue item (Sprint 8.5A Correlation ID).
    history_store.add_entry(
        video_id=video_id, title=metadata["title"], url=request.url.strip(),
        request_id=item.get("request_id"),
    )

    # Auto-start: added items join the single sequential pipeline queue immediately
    # (see _enqueue_for_processing below) instead of waiting for a manual click.
    _enqueue_for_processing(video_id, kind="full")
    return item


@app.delete("/api/queue/{video_id}")
async def remove_from_queue(video_id: str):
    try:
        queue_store.remove_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")
    return {"status": "removed"}


class TranscriptGenerationError(Exception):
    pass


# Stage Guard: a linear rank over the pipeline's real states, used to make
# POST /transcript and POST /study-note idempotent and Forward Only — a repeat
# call once a stage is already reached must return the existing result, never
# pull the Job backward into Downloading/Transcribing/Generating again.
# "Study Note Ready" is the terminal state; there is no separate "Completed"
# status string anywhere in the backend.
_STAGE_RANK = {
    "Queued": 0,
    "Downloading": 1,
    "Transcribing": 2,
    "Transcript Ready": 3,
    "Generating": 4,
    "Study Note Ready": 5,
}


def _stage_rank(status: str) -> int:
    return _STAGE_RANK.get(status, 0)


def _generate_transcript_for_item(video_id: str) -> dict:
    """Runtime Intelligence wrapper (Sprint 8.5A Task 1): times the whole
    Transcript stage (including an idempotent Stage-Guard repeat call, which
    still counts as a real "transcript" event, just a near-zero-duration one)
    and logs it via runtime_metrics — the actual pipeline logic is unchanged,
    just moved into _do_generate_transcript_for_item() below.
    """
    item = queue_store.get_item(video_id)
    request_id = item.get("request_id")
    stage_start = datetime.now(timezone.utc)
    try:
        result = _do_generate_transcript_for_item(video_id)
    except Exception:
        runtime_metrics.log_stage(
            request_id=request_id, video_id=video_id, stage="transcript",
            start_time=stage_start, end_time=datetime.now(timezone.utc), status="error",
        )
        raise
    runtime_metrics.log_stage(
        request_id=request_id, video_id=video_id, stage="transcript",
        start_time=stage_start, end_time=datetime.now(timezone.utc), status="success",
    )
    return result


def _do_generate_transcript_for_item(video_id: str) -> dict:
    item = queue_store.get_item(video_id)

    # Stage Guard: Transcript already reached or passed — return the existing
    # result instead of re-running the pipeline. Regeneration is intentionally
    # out of scope here; a future POST /transcript/regenerate or ?force=true is
    # where that would live, not here.
    if _stage_rank(item.get("status", "")) >= 3 and item.get("transcript_path"):
        return {
            "video_id": video_id,
            "status": item["status"],
            "transcript": Path(item["transcript_path"]).read_text(encoding="utf-8"),
            "file_path": item["transcript_path"],
            "summary": item.get("summary", ""),
        }

    # Processing cache: reuse existing output files for this video instead of
    # re-downloading audio / re-running Whisper. Only applies the first time this
    # item is processed in the current session (no transcript_path yet).
    if not item.get("transcript_path"):
        cached_transcript_path = transcript_service.find_cached_transcript(video_id)

        # Cache Intelligence (Sprint 8.5A Task 3).
        cache_metrics.log_cache_event(
            request_id=item.get("request_id"), video_id=video_id,
            artifact_type="transcript", hit=cached_transcript_path is not None,
        )

        if cached_transcript_path:
            text = cached_transcript_path.read_text(encoding="utf-8")

            # The Transcript file is the single source of truth for a legacy
            # (pre-Feature-003) embedded summary — reuse it if present, then the
            # in-memory value. Feature 003: no Gemini fallback here anymore: a
            # video with neither shows no teaser until the user generates Study
            # Note, whose own Summary section becomes the teaser (see below).
            summary = transcript_service.extract_summary(text) or item.get("summary") or ""

            fields = {
                "status": "Transcript Ready",
                "transcript_path": str(cached_transcript_path),
                "summary": summary,
                "last_error": "",
                "last_error_stage": "",
            }

            # Study Note cached too → wire it up in the same pass so the item is
            # immediately ready to download both ("skip processing, enable
            # download immediately" per the cache spec), still without ever
            # touching yt-dlp/Whisper/Gemini for content generation.
            cached_study_note_path = study_note.find_cached_study_note(video_id)
            if cached_study_note_path:
                fields["status"] = "Study Note Ready"
                fields["study_note_path"] = str(cached_study_note_path)

                # Feature 003: Study Note's own Summary section is the teaser
                # once Study Note exists, taking priority over any legacy
                # Transcript-embedded summary.
                study_note_summary = study_note.extract_summary(
                    cached_study_note_path.read_text(encoding="utf-8")
                )
                if study_note_summary:
                    fields["summary"] = study_note_summary
                    summary = study_note_summary

                # Cache Intelligence (Sprint 8.5A Task 3): a hit here means
                # _do_generate_study_note()'s own cache check below is never
                # reached at all (Stage Guard short-circuits it), so this is
                # the only place this hit would ever be recorded. Misses are
                # deliberately NOT logged here — the authoritative miss for
                # "study_note" is _do_generate_study_note()'s own check,
                # reached moments later for every video that misses here, so
                # logging both would double-count the same miss.
                cache_metrics.log_cache_event(
                    request_id=item.get("request_id"), video_id=video_id,
                    artifact_type="study_note", hit=True,
                )

            queue_store.update_item(video_id, **fields)

            return {
                "video_id": video_id,
                "status": fields["status"],
                "transcript": text,
                "file_path": str(cached_transcript_path),
                "summary": summary,
            }

    # Subtitle-first: reuse a caption track YouTube already has (manual or
    # auto-generated) instead of downloading audio and running Whisper. A fetch
    # failure (network hiccup, region block on the captions endpoint, etc.) is
    # swallowed here rather than failing the item — it just falls through to the
    # normal download+transcribe path below, same as "no captions available".
    # The failure text itself is kept (not discarded) so that if the Whisper
    # fallback below also fails, its cause isn't lost — see the
    # TranscriptionError handler, which prefers this reason over a generic
    # "no transcript" result when it's more informative (e.g. a temporary
    # YouTube rate limit).
    subtitle_fetch_error_text: str | None = None
    try:
        subtitle_text = transcript_service.fetch_subtitle_transcript(video_id)
    except transcript_service.SubtitleFetchError as exc:
        subtitle_text = None
        subtitle_fetch_error_text = str(exc)

    if subtitle_text:
        # Feature 003: Transcript no longer calls Gemini for a summary —
        # the Queue Card teaser is populated later from Study Note's own
        # Summary section, once the user generates it.
        summary = ""

        output_path = transcript_service.save_transcript(
            video_id=video_id, title=item["title"], url=item["url"],
            transcript_text=subtitle_text, summary=summary,
        )

        queue_store.update_item(
            video_id,
            status="Transcript Ready",
            transcript_path=str(output_path),
            summary=summary,
            last_error="",
            last_error_stage="",
            progress_percent=None,
            eta_seconds=None,
        )

        return {
            "video_id": video_id,
            "status": "Transcript Ready",
            "transcript": output_path.read_text(encoding="utf-8"),
            "file_path": str(output_path),
            "summary": summary,
        }

    # No usable captions — fall back to downloading audio and transcribing it
    # locally with Whisper. "Downloading" and "Transcribing" are reported as two
    # distinct, real statuses (not simulated), and a failure records exactly which
    # of the two stages it happened in — so the frontend's processing panel can
    # honestly show which stage is active, and which stage failed, without guessing.
    queue_store.update_item(
        video_id, status="Downloading", last_error="", last_error_stage="",
        progress_percent=None, eta_seconds=None,
    )

    def _report_progress(fraction: float, eta_seconds: float | None) -> None:
        queue_store.update_item(
            video_id,
            progress_percent=round(fraction * 100),
            eta_seconds=round(eta_seconds) if eta_seconds is not None else None,
        )

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_"))
    try:
        try:
            audio_path = transcript_service.download_audio(video_id, tmp_dir, on_progress=_report_progress)
        except transcript_service.AudioDownloadError as exc:
            queue_store.update_item(
                video_id,
                status="Queued",
                last_error=error_messages.classify_error(str(exc), stage="download"),
                last_error_stage="download",
                progress_percent=None,
                eta_seconds=None,
            )
            error_metrics.log_error(
                request_id=item.get("request_id"), video_id=video_id, stage="download",
                exception=f"AudioDownloadError: {exc}",
            )
            raise TranscriptGenerationError(str(exc)) from exc

        queue_store.update_item(video_id, status="Transcribing", progress_percent=None, eta_seconds=None)

        try:
            text = transcript_service.transcribe_audio(audio_path, on_progress=_report_progress)
        except transcript_service.TranscriptionError as exc:
            whisper_message = error_messages.classify_error(str(exc), stage="transcript")

            # If the subtitle fetch also failed earlier (captured above) and its
            # cause was a temporary rate limit, prefer that reason over Whisper's
            # own generic "no transcript" result — but only in that exact
            # collision, so every other failure combination (a non-rate-limit
            # subtitle failure, or a Whisper failure that's already specific)
            # is completely unchanged. The message shown in that collision is
            # the subtitle-specific wording (not the generic
            # _SERVICE_UNAVAILABLE_SOURCE text also used by other stages/call
            # sites) so the user sees a concrete, actionable YouTube-subtitle
            # cause instead of a generic "service unavailable".
            final_message = whisper_message
            if subtitle_fetch_error_text is not None:
                subtitle_message = error_messages.classify_error(subtitle_fetch_error_text, stage="transcript")
                if (
                    subtitle_message == error_messages._SERVICE_UNAVAILABLE_SOURCE
                    and whisper_message == error_messages._NO_TRANSCRIPT
                ):
                    final_message = error_messages._SUBTITLE_TEMPORARILY_UNAVAILABLE

            queue_store.update_item(
                video_id,
                status="Queued",
                last_error=final_message,
                last_error_stage="transcript",
                progress_percent=None,
                eta_seconds=None,
            )
            error_metrics.log_error(
                request_id=item.get("request_id"), video_id=video_id, stage="transcript",
                exception=f"TranscriptionError: {exc}",
            )
            raise TranscriptGenerationError(str(exc)) from exc
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Feature 003: Transcript no longer calls Gemini for a summary — the
    # Queue Card teaser is populated later from Study Note's own Summary
    # section, once the user generates it.
    summary = ""

    output_path = transcript_service.save_transcript(
        video_id=video_id, title=item["title"], url=item["url"], transcript_text=text, summary=summary
    )

    queue_store.update_item(
        video_id,
        status="Transcript Ready",
        transcript_path=str(output_path),
        summary=summary,
        progress_percent=None,
        eta_seconds=None,
    )

    return {
        "video_id": video_id,
        "status": "Transcript Ready",
        "transcript": output_path.read_text(encoding="utf-8"),
        "file_path": str(output_path),
        "summary": summary,
    }


class StudyNoteGenerationError(Exception):
    pass


def _generate_study_note_for_item(video_id: str) -> dict:
    """Workflow Recovery: thin wrapper around _do_generate_study_note()
    guaranteeing that ANY exception — not just the ones _do_generate_study_note()
    already anticipates — gets recorded on the item before it propagates. Without
    this, an unexpected exception here would have been swallowed silently by
    _auto_generate_transcript()'s `except StudyNoteGenerationError: pass`, leaving
    the item frozen at "Transcript Ready" forever with zero trace of what
    happened (the bug that caused the stuck-Job investigation).

    Also times the whole Study Note stage for Runtime Intelligence
    (Sprint 8.5A Task 1) — same request_id as the Transcript stage that
    preceded it, since both are read from the same queue_store item.
    """
    item = queue_store.get_item(video_id)
    request_id = item.get("request_id")
    stage_start = datetime.now(timezone.utc)

    def _log(status: str) -> None:
        runtime_metrics.log_stage(
            request_id=request_id, video_id=video_id, stage="study_note",
            start_time=stage_start, end_time=datetime.now(timezone.utc), status=status,
        )

    try:
        result = _do_generate_study_note(video_id)
    except StudyNoteGenerationError:
        _log("error")
        raise
    except Exception as exc:
        # Genuinely unexpected — not one of the specific error types
        # _do_generate_study_note() already handles and records itself. Record
        # the real exception type/message as-is rather than running it through
        # error_messages.classify_error(), so the true cause stays visible.
        queue_store.update_item(
            video_id,
            status="Transcript Ready",
            last_error="未預期錯誤（" + type(exc).__name__ + "）：" + str(exc),
            last_error_stage="studynote",
        )
        error_metrics.log_error(
            request_id=request_id, video_id=video_id, stage="study_note",
            exception=f"{type(exc).__name__}: {exc}",
        )
        _log("error")
        raise StudyNoteGenerationError(str(exc)) from exc
    _log("success")
    return result


def _do_generate_study_note(video_id: str) -> dict:
    item = queue_store.get_item(video_id)

    # Stage Guard: Study Note already reached — return the existing result
    # instead of re-running the pipeline. Regeneration is intentionally out of
    # scope here; a future POST /study-note/regenerate or ?force=true is where
    # that would live, not here.
    if _stage_rank(item.get("status", "")) >= 5 and item.get("study_note_path"):
        return {
            "video_id": video_id,
            "status": item["status"],
            "study_note": Path(item["study_note_path"]).read_text(encoding="utf-8"),
            "file_path": item["study_note_path"],
        }

    transcript_path = item.get("transcript_path")
    if not transcript_path:
        queue_store.update_item(
            video_id, last_error="請先產生 Transcript", last_error_stage="studynote"
        )
        raise StudyNoteGenerationError("請先產生 Transcript")

    try:
        transcript_content = study_note.read_transcript(transcript_path)
    except study_note.TranscriptNotFoundError as exc:
        queue_store.update_item(
            video_id, last_error="Transcript 檔案不存在", last_error_stage="studynote"
        )
        raise StudyNoteGenerationError("Transcript 檔案不存在") from exc

    transcript_body = study_note.extract_transcript_body(transcript_content)

    # Processing cache: first-time generation only (the Stage Guard above already
    # handles "study_note_path already set" by returning early) — this covers a
    # Study_Note.md that exists on disk from an earlier run but isn't reflected
    # on this queue item yet (e.g. queue.json was reset but outputs/ wasn't).
    if not item.get("study_note_path"):
        cached_study_note_path = study_note.find_cached_study_note(video_id)

        # Cache Intelligence (Sprint 8.5A Task 3): the authoritative
        # hit/miss check for "study_note" — see the comment at the earlier
        # opportunistic check in _do_generate_transcript_for_item() for why
        # that one only logs hits, never misses.
        cache_metrics.log_cache_event(
            request_id=item.get("request_id"), video_id=video_id,
            artifact_type="study_note", hit=cached_study_note_path is not None,
        )

        if cached_study_note_path:
            cached_body = cached_study_note_path.read_text(encoding="utf-8")
            queue_store.update_item(
                video_id,
                status="Study Note Ready",
                study_note_path=str(cached_study_note_path),
                summary=study_note.extract_summary(cached_body),
                last_error="",
                last_error_stage="",
            )
            return {
                "video_id": video_id,
                "status": "Study Note Ready",
                "study_note": cached_body,
                "file_path": str(cached_study_note_path),
            }

    queue_store.update_item(video_id, status="Generating", last_error="", last_error_stage="")

    try:
        body = gemini_client.generate_study_note(
            title=item["title"], url=item["url"], transcript_text=transcript_body,
            request_id=item.get("request_id"), video_id=video_id,
        )
    except gemini_client.GeminiConfigError as exc:
        queue_store.update_item(
            video_id,
            status="Transcript Ready",
            last_error=error_messages.classify_error(str(exc), stage="studynote"),
            last_error_stage="studynote",
        )
        raise StudyNoteGenerationError(str(exc)) from exc
    except gemini_client.GeminiGenerationError as exc:
        queue_store.update_item(
            video_id,
            status="Transcript Ready",
            last_error=error_messages.classify_error(str(exc), stage="studynote"),
            last_error_stage="studynote",
        )
        raise StudyNoteGenerationError(str(exc)) from exc

    output_path = study_note.save_study_note(
        video_id=video_id,
        title=item["title"],
        body=body,
    )

    queue_store.update_item(
        video_id,
        status="Study Note Ready",
        study_note_path=str(output_path),
        summary=study_note.extract_summary(body),
    )

    return {
        "video_id": video_id,
        "status": "Study Note Ready",
        "study_note": output_path.read_text(encoding="utf-8"),
        "file_path": str(output_path),
    }


def _auto_generate_transcript(video_id: str) -> None:
    """Background-task entry point used right after a video is added to the queue,
    and also by /retry for an item that failed before Transcript ever succeeded.
    Transcript-only (Feature 003): Study Note is no longer auto-chained after
    Transcript succeeds — Study Note is now a separate, user-triggered step
    (POST /study-note, same Freemium cost-control pattern as Rapid Learning /
    Learning Blueprint), part of keeping Transcript itself Gemini-free.
    Swallows failure instead of raising an HTTP error — there is no request
    left to respond to. A failure leaves the item at its last real status
    with last_error/last_error_stage set, so the UI can report exactly what
    failed and offer a Retry action.
    """
    try:
        _generate_transcript_for_item(video_id)
    except TranscriptGenerationError:
        return


def _retry_study_note_only(video_id: str) -> None:
    """Worker entry point for a queue item where Transcript already succeeded and
    only Study Note needs another attempt — skips re-downloading/re-transcribing
    entirely rather than routing back through the full pipeline.
    """
    try:
        _generate_study_note_for_item(video_id)
    except StudyNoteGenerationError:
        pass


# Single sequential pipeline queue: every item (whether just added, manually
# started, or retried) is processed one at a time, in the order it was enqueued,
# by one dedicated worker thread. This is what makes "在暫存區的影片，自動按照順序，
# 一個一個接著轉錄" true — without it, adding several videos back-to-back would fire
# off several concurrent background tasks (FastAPI's BackgroundTasks run on the
# thread pool, not serialized), which would contend over the single Whisper model
# instance and violate the single-user/non-concurrent design.
_pipeline_queue: "pyqueue.Queue[tuple[str, str, datetime]]" = pyqueue.Queue()
_worker_started = False
_worker_start_lock = threading.Lock()

# Single Execution Path (方案 A): lets a synchronous HTTP handler submit a job
# through the exact same _pipeline_queue / worker thread every other job uses,
# and block until that specific job finishes — used by the manual /transcript
# and /study-note endpoints below, which previously called
# _generate_*_for_item() directly on FastAPI's own thread pool, bypassing the
# single-worker guarantee entirely. This is not a second lock: nothing here
# guards concurrent execution — it only lets a caller wait for a result that
# the one real worker thread produces.
_job_events: dict[str, threading.Event] = {}
_job_outcomes: dict[str, tuple[bool, object]] = {}
_job_registry_lock = threading.Lock()


def _record_job_outcome(video_id: str, success: bool, payload: object) -> None:
    with _job_registry_lock:
        event = _job_events.get(video_id)
        if event is not None:
            _job_outcomes[video_id] = (success, payload)
            event.set()


def _await_job(video_id: str, kind: str, timeout: float = 600.0):
    event = threading.Event()
    with _job_registry_lock:
        _job_events[video_id] = event
    _enqueue_for_processing(video_id, kind=kind)

    finished = event.wait(timeout=timeout)
    with _job_registry_lock:
        _job_events.pop(video_id, None)
        success, payload = _job_outcomes.pop(video_id, (False, None))

    if not finished:
        raise TimeoutError(f"處理逾時：{video_id} 未在 {timeout} 秒內完成")
    if success:
        return payload
    raise payload


def _pipeline_worker_loop() -> None:
    while True:
        video_id, kind, enqueued_at = _pipeline_queue.get()

        # Runtime Intelligence (Sprint 8.5A Task 1): "queue" stage — how long
        # this job actually waited on _pipeline_queue before a worker picked
        # it up. Best-effort: an item removed from queue_store between being
        # enqueued and being picked up (e.g. user deleted it) is skipped
        # silently rather than failing the job.
        try:
            _item = queue_store.get_item(video_id)
            runtime_metrics.log_stage(
                request_id=_item.get("request_id"), video_id=video_id, stage="queue",
                start_time=enqueued_at, end_time=datetime.now(timezone.utc), status="success",
            )
        except Exception:
            pass

        try:
            if kind == "study_note_only":
                _retry_study_note_only(video_id)
            elif kind == "transcript_only_sync":
                # Manual /transcript endpoint — same _generate_transcript_for_item()
                # as before, just now only ever invoked from this one worker
                # thread. Caught broadly (not just TranscriptGenerationError) so
                # _await_job()'s waiter always gets *something* back instead of
                # timing out on a bug here; whichever exception type it is gets
                # re-raised on the waiting side exactly as it would have been
                # before this change.
                try:
                    result = _generate_transcript_for_item(video_id)
                except Exception as exc:
                    _record_job_outcome(video_id, False, exc)
                else:
                    _record_job_outcome(video_id, True, result)
            elif kind == "study_note_only_sync":
                # Manual /study-note endpoint — same _generate_study_note_for_item()
                # as before, same reasoning as transcript_only_sync above.
                try:
                    result = _generate_study_note_for_item(video_id)
                except Exception as exc:
                    _record_job_outcome(video_id, False, exc)
                else:
                    _record_job_outcome(video_id, True, result)
            else:
                _auto_generate_transcript(video_id)
        except Exception as exc:
            # Workflow Recovery: a single job's unexpected failure must never
            # kill this thread — without a top-level catch here, an uncaught
            # exception propagates out of the `while True` loop entirely, the
            # thread dies, `_worker_started` never resets, and every job added
            # afterward sits in _pipeline_queue forever with nothing consuming
            # it, until the process is restarted. Best-effort record it on the
            # item so it isn't silently invisible in the UI either.
            error_stage = "study_note" if kind == "study_note_only" else "transcript"
            try:
                queue_store.update_item(
                    video_id,
                    last_error="Worker 發生未預期錯誤（" + type(exc).__name__ + "）：" + str(exc),
                    last_error_stage="studynote" if kind == "study_note_only" else "transcript",
                )
            except Exception:
                pass
            try:
                error_metrics.log_error(
                    request_id=queue_store.get_item(video_id).get("request_id"),
                    video_id=video_id, stage=error_stage,
                    exception=f"Worker: {type(exc).__name__}: {exc}",
                )
            except Exception:
                pass
        finally:
            _pipeline_queue.task_done()


def _enqueue_for_processing(video_id: str, kind: str = "full") -> None:
    global _worker_started
    with _worker_start_lock:
        if not _worker_started:
            threading.Thread(target=_pipeline_worker_loop, daemon=True, name="ybkf-pipeline-worker").start()
            _worker_started = True
    _pipeline_queue.put((video_id, kind, datetime.now(timezone.utc)))


@app.on_event("startup")
async def _resume_pending_queue_items() -> None:
    """Re-joins the sequential pipeline queue for anything left unfinished by a
    previous run (the in-memory _pipeline_queue itself doesn't survive a restart).
    Oldest-added first, so resumed items keep the same order they'd have processed
    in originally. Items with a recorded last_error are left alone — retry is a
    deliberate user action (POST /retry), not something that should auto-loop on a
    video that's known to be broken (e.g. region-locked).
    """
    items = sorted(queue_store.list_items(), key=lambda item: item["created_at"])
    for item in items:
        if item.get("last_error") or item.get("study_note_path"):
            continue
        if item.get("transcript_path"):
            _enqueue_for_processing(item["video_id"], kind="study_note_only")
        else:
            _enqueue_for_processing(item["video_id"], kind="full")


@app.post("/api/queue/{video_id}/start")
async def start_processing(video_id: str):
    """Manual fallback for an item that isn't already moving through the pipeline
    (e.g. it errored out earlier without being retried, or the in-memory queue was
    lost some other way). Normally items start automatically on add.
    """
    try:
        queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    _enqueue_for_processing(video_id, kind="full")
    return {"status": "started"}


@app.post("/api/queue/{video_id}/retry")
async def retry_processing(video_id: str):
    """Recovery action for a failed item — resumes from wherever it actually left
    off (Transcript from scratch, or just Study Note if Transcript already
    succeeded), using the video's already-known URL, so the user never has to
    paste the YouTube URL again.
    """
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    queue_store.update_item(video_id, last_error="", last_error_stage="")

    if item.get("transcript_path") and not item.get("study_note_path"):
        _enqueue_for_processing(video_id, kind="study_note_only")
    else:
        _enqueue_for_processing(video_id, kind="full")

    return {"status": "retrying"}


@app.post("/api/queue/{video_id}/transcript")
def generate_transcript(video_id: str):
    """Single Execution Path (方案 A): submits through the same
    _pipeline_queue / single worker thread as every other job instead of
    calling _generate_transcript_for_item() directly — the actual work and
    error handling are unchanged, only how it's dispatched.
    """
    try:
        queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    try:
        return _await_job(video_id, kind="transcript_only_sync")
    except TranscriptGenerationError as exc:
        # _generate_transcript_for_item already recorded the correct stage
        # (download vs transcript) on the item before raising — reuse it instead
        # of re-guessing from the raw exception text here.
        stage = queue_store.get_item(video_id).get("last_error_stage", "")
        raise HTTPException(status_code=500, detail=error_messages.classify_error(str(exc), stage=stage))


@app.post("/api/queue/{video_id}/study-note")
def generate_study_note(video_id: str):
    """Single Execution Path (方案 A): submits through the same
    _pipeline_queue / single worker thread as every other job instead of
    calling _generate_study_note_for_item() directly — the actual work and
    error handling are unchanged, only how it's dispatched.
    """
    try:
        queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    try:
        return _await_job(video_id, kind="study_note_only_sync")
    except StudyNoteGenerationError as exc:
        detail = str(exc)
        if detail == "請先產生 Transcript":
            raise HTTPException(status_code=400, detail=detail)
        if detail == "Transcript 檔案不存在":
            raise HTTPException(status_code=404, detail=detail)
        raise HTTPException(status_code=500, detail=error_messages.classify_error(detail, stage="studynote"))


@app.post("/api/queue/{video_id}/knowledge-outline")
async def generate_knowledge_outline(video_id: str):
    """Rapid Learning Engine (Sprint 7, Task 1): manual "🧠 開始快速學習"
    trigger for One Sentence + Knowledge Outline. Deliberately NOT routed
    through _pipeline_queue / the single worker thread (unlike /transcript
    and /study-note) — this doesn't touch `status` or participate in Stage
    Guard's state machine at all, it's an independent additive artifact, so
    it follows the same direct-async-handler pattern the Export/History
    endpoints already use instead. Reads the existing cached Transcript only
    — does not touch the Transcript / Study Note pipeline.
    """
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    # Processing cache: avoids a duplicate Gemini call (and duplicate token
    # spend) if this has already been generated for this video_id — same
    # find_cached_* pattern Transcript/Study Note already use.
    cached_path = knowledge_outline.find_cached_knowledge_outline(video_id)
    cache_metrics.log_cache_event(
        request_id=item.get("request_id"), video_id=video_id,
        artifact_type="knowledge_outline", hit=cached_path is not None,
    )
    if cached_path:
        return {
            "video_id": video_id,
            "knowledge_outline": cached_path.read_text(encoding="utf-8"),
            "file_path": str(cached_path),
        }

    transcript_path = item.get("transcript_path")
    if not transcript_path or not Path(transcript_path).exists():
        raise HTTPException(status_code=400, detail="請先產生 Transcript")

    transcript_content = Path(transcript_path).read_text(encoding="utf-8")
    transcript_body = study_note.extract_transcript_body(transcript_content)

    try:
        body = await asyncio.to_thread(
            gemini_client.generate_knowledge_outline,
            title=item["title"], url=item["url"], transcript_text=transcript_body,
            request_id=item.get("request_id"), video_id=video_id,
        )
    except gemini_client.GeminiConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except gemini_client.GeminiGenerationError as exc:
        raise HTTPException(
            status_code=500,
            detail=error_messages.classify_error(str(exc), stage="studynote"),
        )

    # Feature 004 — Usage Quota Foundation: counts only a real, successful
    # Gemini call (never a cache hit, never a failed call — both handled
    # above without reaching this line). Counted here rather than after the
    # save below because the Gemini cost is already incurred at this point,
    # regardless of whether the subsequent local save succeeds. Measurement
    # only — never blocks or limits this call.
    usage_quota.record_knowledge_outline_success()

    output_path = knowledge_outline.save_knowledge_outline(
        video_id=video_id, title=item["title"], body=body
    )

    # Additive field only — no `status` change, so this never interacts with
    # _stage_rank() / Stage Guard's forward-only state machine.
    queue_store.update_item(video_id, knowledge_outline_path=str(output_path))

    return {
        "video_id": video_id,
        "knowledge_outline": body,
        "file_path": str(output_path),
    }


@app.get("/api/usage/knowledge-outline")
async def get_knowledge_outline_usage():
    """Feature 004 — Usage Quota Foundation: read-only lifetime usage
    snapshot for 30秒快速學習 (Knowledge Outline). Informational only — not
    yet wired into any UI, and calling this endpoint never itself counts as
    usage or affects any other endpoint's behavior.
    """
    return usage_quota.get_knowledge_outline_usage()


@app.get("/api/queue/{video_id}/transcript/download")
async def download_transcript(video_id: str):
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    transcript_path = item.get("transcript_path")
    if not transcript_path or not Path(transcript_path).exists():
        raise HTTPException(status_code=404, detail="Transcript 檔案不存在")

    # Runtime Intelligence (Sprint 8.5A Task 1): "download" stage.
    _now = datetime.now(timezone.utc)
    runtime_metrics.log_stage(
        request_id=item.get("request_id"), video_id=video_id, stage="download",
        start_time=_now, end_time=_now, status="success",
    )

    return FileResponse(
        transcript_path,
        media_type="text/markdown",
        filename=Path(transcript_path).name,
    )


@app.get("/api/queue/{video_id}/study-note/download")
async def download_study_note(video_id: str):
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    study_note_path = item.get("study_note_path")
    if not study_note_path or not Path(study_note_path).exists():
        raise HTTPException(status_code=404, detail="Study Note 檔案不存在")

    # Runtime Intelligence (Sprint 8.5A Task 1): "download" stage.
    _now = datetime.now(timezone.utc)
    runtime_metrics.log_stage(
        request_id=item.get("request_id"), video_id=video_id, stage="download",
        start_time=_now, end_time=_now, status="success",
    )

    return FileResponse(
        study_note_path,
        media_type="text/markdown",
        filename=Path(study_note_path).name,
    )


@app.get("/api/queue/{video_id}/export")
async def export_package(video_id: str):
    """Knowledge Package Export (Sprint 5, Task 1): zips the already-generated
    Transcript.md + Study_Note.md into one `<Video Title>/` package. Export
    Layer only — reads existing output files, does not touch the Transcript /
    Study Note pipeline.
    """
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    transcript_path = item.get("transcript_path")
    if not transcript_path or not Path(transcript_path).exists():
        raise HTTPException(status_code=404, detail="Transcript 檔案不存在")

    study_note_path = item.get("study_note_path")
    if not study_note_path or not Path(study_note_path).exists():
        raise HTTPException(status_code=404, detail="Study Note 檔案不存在")

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_export_"))
    zip_path = knowledge_package.build_package(
        dest_dir=tmp_dir,
        title=item["title"],
        video_id=video_id,
        transcript_path=transcript_path,
        study_note_path=study_note_path,
    )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_path.name,
        background=BackgroundTask(shutil.rmtree, tmp_dir, ignore_errors=True),
    )


@app.get("/api/queue/export-all")
async def export_all_packages():
    """Bulk Knowledge Package Export (Sprint 5, Task 2; disk-verification
    parity added in Task 5): packages every Queue item whose Transcript.md
    and Study_Note.md both still exist on disk into one zip, one
    `<Video Title>_<video_id>/` folder per video. Items missing a file on
    disk are silently excluded rather than aborting the whole batch — same
    auto-exclude semantics as /api/history/export-all (Task 4), since one
    stale queue_store record shouldn't block everyone else's download.
    Export Layer only — reads existing queue_store items and output files
    via the same find_cached_* lookups GET /api/queue and GET /api/history
    already use, and reuses knowledge_package.build_bulk_package() unchanged;
    does not touch the Transcript / Study Note pipeline.
    """
    candidates = []
    for item in queue_store.list_items():
        transcript_path = transcript_service.find_cached_transcript(item["video_id"])
        study_note_path = study_note.find_cached_study_note(item["video_id"])
        if transcript_path and study_note_path:
            candidates.append({
                "video_id": item["video_id"],
                "title": item["title"],
                "transcript_path": str(transcript_path),
                "study_note_path": str(study_note_path),
            })

    if not candidates:
        raise HTTPException(status_code=404, detail="目前沒有已完成的知識包可匯出")

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_export_all_"))
    try:
        zip_path = knowledge_package.build_bulk_package(dest_dir=tmp_dir, items=candidates)
    except knowledge_package.IncompletePackageError as exc:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        missing_desc = "、".join(
            f"{title}（缺少 {filename}）" for _, title, filename in exc.args[0]
        )
        raise HTTPException(
            status_code=422,
            detail=f"以下影片的知識包不完整，已取消匯出：{missing_desc}",
        )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_path.name,
        background=BackgroundTask(shutil.rmtree, tmp_dir, ignore_errors=True),
    )


@app.get("/api/history/{video_id}/export")
async def export_history_package(video_id: str):
    """Knowledge Library (Sprint 5, Task 3): single-video Knowledge Package
    download from the History page — video_id may no longer be in
    queue_store at all (e.g. removed from the Queue to free up space), so
    this looks the files up on disk via the same find_cached_* functions the
    pipeline's own processing cache already uses, and reuses the existing
    knowledge_package.build_package() Task 1 already built. Export/History
    Layer only — does not touch queue_store or history_store's write paths.
    """
    entry = next(
        (e for e in history_store.list_entries() if e["video_id"] == video_id), None
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="歷史紀錄中找不到這支影片")

    transcript_path = transcript_service.find_cached_transcript(video_id)
    study_note_path = study_note.find_cached_study_note(video_id)
    if not transcript_path or not study_note_path:
        raise HTTPException(status_code=404, detail="知識包不完整，Transcript 或 Study Note 檔案缺失")

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_history_export_"))
    zip_path = knowledge_package.build_package(
        dest_dir=tmp_dir,
        title=entry["title"],
        video_id=video_id,
        transcript_path=str(transcript_path),
        study_note_path=str(study_note_path),
    )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_path.name,
        background=BackgroundTask(shutil.rmtree, tmp_dir, ignore_errors=True),
    )


@app.get("/api/history/export-all")
async def export_all_history_packages():
    """History Bulk Export (Sprint 5, Task 4): packages every History entry
    whose Transcript.md and Study_Note.md both still exist on disk into one
    zip, one `<Video Title>_<video_id>/` folder per video. Unlike
    /api/queue/export-all (which trusts queue_store's path fields), this
    looks files up on disk the same way export_history_package() above does,
    so it works for entries no longer present in queue_store and doesn't
    inherit the Queue page's known path-vs-disk gap (see TODO.md Product
    Backlog). Export/History Layer only — does not touch queue_store,
    history_store's write paths, or the Transcript / Study Note pipeline.
    """
    candidates = []
    for entry in history_store.list_entries():
        transcript_path = transcript_service.find_cached_transcript(entry["video_id"])
        study_note_path = study_note.find_cached_study_note(entry["video_id"])
        if transcript_path and study_note_path:
            candidates.append({
                "video_id": entry["video_id"],
                "title": entry["title"],
                "transcript_path": str(transcript_path),
                "study_note_path": str(study_note_path),
            })

    if not candidates:
        raise HTTPException(status_code=404, detail="目前沒有已完成的知識包可匯出")

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_history_export_all_"))
    try:
        zip_path = knowledge_package.build_bulk_package(dest_dir=tmp_dir, items=candidates)
    except knowledge_package.IncompletePackageError as exc:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        missing_desc = "、".join(
            f"{title}（缺少 {filename}）" for _, title, filename in exc.args[0]
        )
        raise HTTPException(
            status_code=422,
            detail=f"以下影片的知識包不完整，已取消匯出：{missing_desc}",
        )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_path.name,
        background=BackgroundTask(shutil.rmtree, tmp_dir, ignore_errors=True),
    )


@app.get("/api/history/{video_id}/transcript", response_class=PlainTextResponse)
async def view_history_transcript(video_id: str):
    """Knowledge Library (Sprint 5, Task 3): "開啟 Transcript" — returns the
    raw content with no Content-Disposition header, so the browser displays
    it in a new tab instead of forcing a download (unlike the existing Queue
    page's /transcript/download, which is deliberately an attachment).
    """
    transcript_path = transcript_service.find_cached_transcript(video_id)
    if not transcript_path:
        raise HTTPException(status_code=404, detail="Transcript 檔案不存在")
    return transcript_path.read_text(encoding="utf-8")


@app.get("/api/history/{video_id}/study-note", response_class=PlainTextResponse)
async def view_history_study_note(video_id: str):
    """Knowledge Library (Sprint 5, Task 3): "開啟 Study Note" — same reasoning
    as view_history_transcript() above.
    """
    study_note_path = study_note.find_cached_study_note(video_id)
    if not study_note_path:
        raise HTTPException(status_code=404, detail="Study Note 檔案不存在")
    return study_note_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
