import shutil
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import gemini_client
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


@app.get("/api/queue")
async def get_queue():
    return {"items": queue_store.list_items()}


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

    return item


@app.delete("/api/queue/{video_id}")
async def remove_from_queue(video_id: str):
    try:
        queue_store.remove_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")
    return {"status": "removed"}


@app.post("/api/queue/{video_id}/transcript")
def generate_transcript(video_id: str):
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    queue_store.update_item(video_id, status="Transcribing")

    tmp_dir = Path(tempfile.mkdtemp(prefix="ybkf_"))
    try:
        audio_path = transcript_service.download_audio(video_id, tmp_dir)
        text = transcript_service.transcribe_audio(audio_path)
    except (transcript_service.AudioDownloadError, transcript_service.TranscriptionError) as exc:
        queue_store.update_item(video_id, status="Queued")
        raise HTTPException(status_code=500, detail=f"Transcript 產生失敗: {exc}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    output_path = transcript_service.save_transcript(
        video_id=video_id, title=item["title"], url=item["url"], transcript_text=text
    )

    queue_store.update_item(
        video_id, status="Transcript Ready", transcript_path=str(output_path)
    )

    return {
        "video_id": video_id,
        "status": "Transcript Ready",
        "transcript": text,
        "file_path": str(output_path),
    }


@app.post("/api/queue/{video_id}/study-note")
def generate_study_note(video_id: str):
    try:
        item = queue_store.get_item(video_id)
    except queue_store.QueueItemNotFoundError:
        raise HTTPException(status_code=404, detail="項目不存在")

    transcript_path = item.get("transcript_path")
    if not transcript_path:
        raise HTTPException(status_code=400, detail="請先產生 Transcript")

    try:
        transcript_content = study_note.read_transcript(transcript_path)
    except study_note.TranscriptNotFoundError:
        raise HTTPException(status_code=404, detail="Transcript 檔案不存在")

    transcript_body = study_note.extract_transcript_body(transcript_content)

    queue_store.update_item(video_id, status="Generating")

    try:
        result = gemini_client.generate_study_note_body(
            title=item["title"], url=item["url"], transcript_text=transcript_body
        )
    except gemini_client.GeminiConfigError as exc:
        queue_store.update_item(video_id, status="Transcript Ready")
        raise HTTPException(status_code=500, detail=str(exc))
    except gemini_client.GeminiGenerationError as exc:
        queue_store.update_item(video_id, status="Transcript Ready")
        raise HTTPException(status_code=500, detail=f"Study Note 產生失敗: {exc}")

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
