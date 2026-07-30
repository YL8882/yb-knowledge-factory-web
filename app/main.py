import shutil
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import error_messages
import gemini_client
import history_store
import queue_store
import study_note
import transcript as transcript_service
import youtube

load_dotenv()

app = FastAPI()

# Serve static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class AddVideoRequest(BaseModel):
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


@app.post("/api/queue")
async def add_to_queue(request: AddVideoRequest, background_tasks: BackgroundTasks):
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

    # Auto-start Transcript generation (+ quick summary) in the background so the
    # one-line summary appears under the title without the user having to click
    # "產生 Transcript" first. Runs after the response is sent; failures just leave
    # the item back at "Queued" so the manual button still works as a retry.
    background_tasks.add_task(_auto_generate_transcript, video_id)

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


def _generate_transcript_for_item(video_id: str) -> dict:
    item = queue_store.get_item(video_id)

    # Processing cache: reuse existing output files for this video instead of
    # re-downloading audio / re-running Whisper. Only applies the first time this
    # item is processed in the current session (no transcript_path yet) — an
    # explicit "重新產生 Transcript" click already has transcript_path set on the
    # item and always falls through to the real reprocessing below.
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

    # "Downloading" and "Transcribing" are reported as two distinct, real statuses
    # (not simulated), and a failure records exactly which of the two stages it
    # happened in — so the frontend's processing panel can honestly show which
    # stage is active, and which stage failed, without guessing.
    queue_store.update_item(video_id, status="Downloading", last_error="", last_error_stage="")

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_"))
    try:
        try:
            audio_path = transcript_service.download_audio(video_id, tmp_dir)
        except transcript_service.AudioDownloadError as exc:
            queue_store.update_item(
                video_id,
                status="Queued",
                last_error=error_messages.classify_error(str(exc)),
                last_error_stage="download",
            )
            raise TranscriptGenerationError(str(exc)) from exc

        queue_store.update_item(video_id, status="Transcribing")

        try:
            text = transcript_service.transcribe_audio(audio_path)
        except transcript_service.TranscriptionError as exc:
            queue_store.update_item(
                video_id,
                status="Queued",
                last_error=error_messages.classify_error(str(exc)),
                last_error_stage="transcript",
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
    item = queue_store.get_item(video_id)

    transcript_path = item.get("transcript_path")
    if not transcript_path:
        raise StudyNoteGenerationError("請先產生 Transcript")

    try:
        transcript_content = study_note.read_transcript(transcript_path)
    except study_note.TranscriptNotFoundError as exc:
        raise StudyNoteGenerationError("Transcript 檔案不存在") from exc

    transcript_body = study_note.extract_transcript_body(transcript_content)

    # Processing cache: only applies to a first-time generation (no study_note_path
    # on the item yet). An explicit "重新產生 Study Note" call already has
    # study_note_path set on the item and always falls through to a real Gemini
    # call below — regeneration must never be silently skipped by the cache.
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
        result = gemini_client.generate_study_note_body(
            title=item["title"], url=item["url"], transcript_text=transcript_body
        )
    except gemini_client.GeminiConfigError as exc:
        queue_store.update_item(
            video_id,
            status="Transcript Ready",
            last_error=error_messages.classify_error(str(exc)),
            last_error_stage="studynote",
        )
        raise StudyNoteGenerationError(str(exc)) from exc
    except gemini_client.GeminiGenerationError as exc:
        queue_store.update_item(
            video_id,
            status="Transcript Ready",
            last_error=error_messages.classify_error(str(exc)),
            last_error_stage="studynote",
        )
        raise StudyNoteGenerationError(str(exc)) from exc

    output_path = study_note.save_study_note(
        video_id=video_id,
        title=item["title"],
        url=item["url"],
        body=result["body"],
        tags=result["tags"],
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
    Fully automatic pipeline: Transcript, then (on success) straight into Study
    Note, with no manual click in between. Swallows failures instead of raising an
    HTTP error — there is no request left to respond to. A failure leaves the item
    at its last real status with last_error/last_error_stage set, so the UI can
    report exactly what failed and offer a Retry action.
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
    """Background-task entry point for /retry when Transcript already succeeded
    and only Study Note needs another attempt — skips re-downloading/re-transcribing
    entirely rather than routing back through the full pipeline.
    """
    try:
        _generate_study_note_for_item(video_id)
    except StudyNoteGenerationError:
        pass


@app.post("/api/queue/{video_id}/retry")
async def retry_processing(video_id: str, background_tasks: BackgroundTasks):
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
        background_tasks.add_task(_retry_study_note_only, video_id)
    else:
        background_tasks.add_task(_auto_generate_transcript, video_id)

    return {"status": "retrying"}


@app.post("/api/queue/{video_id}/transcript")
def generate_transcript(video_id: str):
    try:
        queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    try:
        return _generate_transcript_for_item(video_id)
    except TranscriptGenerationError as exc:
        raise HTTPException(status_code=500, detail=error_messages.classify_error(str(exc)))


@app.post("/api/queue/{video_id}/study-note")
def generate_study_note(video_id: str):
    try:
        queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    try:
        return _generate_study_note_for_item(video_id)
    except StudyNoteGenerationError as exc:
        detail = str(exc)
        if detail == "請先產生 Transcript":
            raise HTTPException(status_code=400, detail=detail)
        if detail == "Transcript 檔案不存在":
            raise HTTPException(status_code=404, detail=detail)
        raise HTTPException(status_code=500, detail=error_messages.classify_error(detail))


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
