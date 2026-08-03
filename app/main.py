import queue as pyqueue
import shutil
import tempfile
import threading
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.background import BackgroundTask

import error_messages
import gemini_client
import history_store
import knowledge_package
import queue_store
import study_note
import transcript as transcript_service
import youtube

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
    return {"items": queue_store.list_items()}


@app.get("/api/history")
async def get_history():
    return {"items": history_store.list_entries()}


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
    history_store.add_entry(video_id=video_id, title=metadata["title"], url=request.url.strip())

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
        if cached_transcript_path:
            text = cached_transcript_path.read_text(encoding="utf-8")

            # The Transcript file is the single source of truth for the summary —
            # reuse it from there first (works even for a brand-new queue item that
            # never held it in memory), then the in-memory value, and only call
            # Gemini as a last resort for a pre-cache-feature file that has neither.
            summary = transcript_service.extract_summary(text) or item.get("summary") or ""
            if not summary:
                try:
                    summary = gemini_client.generate_quick_summary(
                        title=item["title"],
                        url=item["url"],
                        transcript_text=study_note.extract_transcript_body(text),
                    )
                except (gemini_client.GeminiConfigError, gemini_client.GeminiGenerationError):
                    summary = ""

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
    try:
        subtitle_text = transcript_service.fetch_subtitle_transcript(video_id)
    except transcript_service.SubtitleFetchError:
        subtitle_text = None

    if subtitle_text:
        try:
            summary = gemini_client.generate_quick_summary(
                title=item["title"], url=item["url"], transcript_text=subtitle_text
            )
        except (gemini_client.GeminiConfigError, gemini_client.GeminiGenerationError):
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
            raise TranscriptGenerationError(str(exc)) from exc

        queue_store.update_item(video_id, status="Transcribing", progress_percent=None, eta_seconds=None)

        try:
            text = transcript_service.transcribe_audio(audio_path, on_progress=_report_progress)
        except transcript_service.TranscriptionError as exc:
            queue_store.update_item(
                video_id,
                status="Queued",
                last_error=error_messages.classify_error(str(exc), stage="transcript"),
                last_error_stage="transcript",
                progress_percent=None,
                eta_seconds=None,
            )
            raise TranscriptGenerationError(str(exc)) from exc
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Best-effort one-sentence summary so the queue item shows a quick "what is this
    # video about" preview without the user having to generate the full Study Note.
    # A failure here (e.g. missing Gemini key) must not fail the Transcript step itself.
    # Generated before save_transcript() so it can be stored inside the Transcript
    # file itself (single source of truth) — a future cache hit reads it straight
    # back out instead of calling Gemini again.
    try:
        summary = gemini_client.generate_quick_summary(
            title=item["title"], url=item["url"], transcript_text=text
        )
    except (gemini_client.GeminiConfigError, gemini_client.GeminiGenerationError):
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
    """
    try:
        return _do_generate_study_note(video_id)
    except StudyNoteGenerationError:
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
        raise StudyNoteGenerationError(str(exc)) from exc


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
        if cached_study_note_path:
            queue_store.update_item(
                video_id,
                status="Study Note Ready",
                study_note_path=str(cached_study_note_path),
                last_error="",
                last_error_stage="",
            )
            return {
                "video_id": video_id,
                "status": "Study Note Ready",
                "study_note": cached_study_note_path.read_text(encoding="utf-8"),
                "file_path": str(cached_study_note_path),
            }

    queue_store.update_item(video_id, status="Generating", last_error="", last_error_stage="")

    try:
        body = gemini_client.generate_study_note(
            title=item["title"], url=item["url"], transcript_text=transcript_body
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
        video_id, status="Study Note Ready", study_note_path=str(output_path)
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
    Fully automatic pipeline (Sprint 4): Transcript, then (on success) straight
    into Study Note, with no manual click in between. Swallows failures instead
    of raising an HTTP error — there is no request left to respond to. A failure
    leaves the item at its last real status with last_error/last_error_stage
    set, so the UI can report exactly what failed and offer a Retry action.
    """
    try:
        _generate_transcript_for_item(video_id)
    except TranscriptGenerationError:
        return

    try:
        _generate_study_note_for_item(video_id)
    except StudyNoteGenerationError:
        pass


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
_pipeline_queue: "pyqueue.Queue[tuple[str, str]]" = pyqueue.Queue()
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
        video_id, kind = _pipeline_queue.get()
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
            try:
                queue_store.update_item(
                    video_id,
                    last_error="Worker 發生未預期錯誤（" + type(exc).__name__ + "）：" + str(exc),
                    last_error_stage="studynote" if kind == "study_note_only" else "transcript",
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
    _pipeline_queue.put((video_id, kind))


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


@app.get("/api/queue/{video_id}/transcript/download")
async def download_transcript(video_id: str):
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    transcript_path = item.get("transcript_path")
    if not transcript_path or not Path(transcript_path).exists():
        raise HTTPException(status_code=404, detail="Transcript 檔案不存在")

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
    """Bulk Knowledge Package Export (Sprint 5, Task 2): packages every
    completed (Study Note Ready) item into one zip, one
    `<Video Title>_<video_id>/` folder per video. Export Layer only — reads
    existing queue_store items and output files, does not touch the
    Transcript / Study Note pipeline.
    """
    candidates = [
        item for item in queue_store.list_items()
        if item.get("transcript_path") and item.get("study_note_path")
    ]

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
