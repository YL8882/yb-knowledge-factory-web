---
Version: 2.0
Status: Current
Document Type: Engineering Reference
Document: Engineering Understanding Report
Category: Project Management
Purpose: Current Engineering Understanding / Codebase Truth for YB Learn (YB Knowledge Lite).
Update Policy: Only update after (1) a Major Milestone or (2) a Significant Architecture Change. Do NOT update for every Sprint.
Scope: YB Knowledge Factory MVP v0.1 (product name: YB Learn / YB Knowledge Lite)
Priority: High
Last Updated: 2026-08-08
Source Priority: Actual Code > CLAUDE.md > TODO.md / Acceptance_Test.md > other documentation
---

# Engineering Understanding Report

> This document describes what is actually implemented in the codebase today. It is not a Sprint log — Sprint-by-Sprint history lives in `TODO.md`; acceptance criteria live in `Acceptance_Test.md`. This report is superseded only by re-reading the code, never by another planning document.

---

## 1. System Overview

YB Learn turns a YouTube video into a set of durable Markdown/JSON knowledge artifacts, driven from a one-click Chrome Extension button on the YouTube page itself.

```text
YouTube video
  → Chrome Extension ("YB Learn" button)
  → FastAPI backend (Queue)
  → Transcript (subtitle fetch, or yt-dlp audio + faster-whisper fallback)
  → Study Note (Gemini)
  → optional, on-demand: Knowledge Outline / Learning Blueprint / Teach Back / Action List / Review
  → Markdown / JSON files on disk, downloadable individually or as a Knowledge Package (.zip)
```

Single-user, single-machine, no login, no database, no cloud sync. State lives in JSON files under `outputs/`.

---

## 2. Current Architecture

```text
extension/           Chrome Extension (Manifest V3) — capture + open/focus Workspace tab
app/                 FastAPI application — the only backend code
  main.py            All HTTP routes, the single-worker pipeline, Stage Guard
  queue_store.py      In-memory queue, mirrored to outputs/queue.json
  history_store.py    Append/update log of processed videos, mirrored to outputs/history.json
  youtube.py          URL validation + yt-dlp metadata fetch
  transcript.py        Subtitle fetch / audio download / faster-whisper transcription / OpenCC
  gemini_client.py     All Gemini calls, one interception point, 7 generate_* functions
  study_note.py, knowledge_outline.py, learning_blueprint.py,
  teach_back.py, action_list.py, review.py
                       Per-artifact file assembly + persistence (one module per artifact type)
  knowledge_package.py Zip export (single video and bulk)
  error_messages.py    Maps raw exception text → user-facing Traditional Chinese messages
  observability/        Best-effort JSONL logging + daily_report.json aggregation
  templates/, static/   Single-page HTML/CSS/JS frontend (no frontend framework/build step)
outputs/              All generated artifacts + queue.json / history.json + logs/
```

There is no database, no ORM, no message broker, and no separate frontend build — `static/script.js` talks directly to the FastAPI JSON API and re-renders the page by polling.

---

## 3. Core Modules & Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Route definitions, request validation, the single background worker thread that runs the automatic Transcript→Study Note pipeline, Stage Guard (forward-only state checks so a finished stage never re-runs) |
| `queue_store.py` | In-memory list of queue items (add/list/remove, 100-item cap, duplicate-`video_id` rejection — `video_id` is parsed from the URL by `youtube.py` before reaching `queue_store`, not a raw URL string comparison), persisted to `outputs/queue.json` on every write; on load, items frozen mid-"Downloading"/"Transcribing"/"Generating" by a prior crash are reset to the last retryable state |
| `history_store.py` | Append-only-by-video_id record of every processed video, independent of the Queue's lifecycle (an item removed from the Queue stays in History), persisted to `outputs/history.json` |
| `youtube.py` | Validates a YouTube URL (including `/shorts/`) and extracts `video_id` / metadata via `yt-dlp` |
| `transcript.py` | Tries `fetch_subtitle_transcript()` (YouTube captions, language-preference ordered) first; on failure, falls back to `download_audio()` + `transcribe_audio()` (faster-whisper, `base` model, CPU int8); converts output to Traditional Chinese via `OpenCC("s2twp")` |
| `gemini_client.py` | One private `_generate_content()` call site used by all 7 `generate_*()` functions (study_note, quick_summary, knowledge_outline, learning_blueprint, teach_back, action_list, review); each has its own hard-coded system-instruction prompt |
| `study_note.py` | Assembles the Study Note Markdown (metadata block + Gemini content) and saves it |
| `knowledge_outline.py` / `learning_blueprint.py` / `teach_back.py` / `action_list.py` / `review.py` | One module per Learning Model artifact type; each is triggered independently by its own API call, reads existing upstream artifacts (not the raw transcript) as input, and persists its own output file |
| `knowledge_package.py` | Builds a `.zip` (single video or bulk-all) containing `Transcript.md` + `Study_Note.md`; sanitizes folder/file names (CJK-safe allowlist, 50-char truncation) to avoid Windows extraction failures |
| `error_messages.py` | `classify_error(raw_message, stage)` maps raw exception text to a fixed set of Traditional Chinese user-facing messages, disambiguating Gemini-quota errors from non-Gemini (download/transcription) service errors by `stage` |
| `observability/` | `logger.py` (JSONL writer, gated by `PRODUCT_INTELLIGENCE_ENABLED`), `runtime_metrics.py`, `cost_metrics.py`, `cache_metrics.py`, `error_metrics.py`, `daily_report.py` (incremental aggregation into `outputs/logs/daily_report.json`) |

---

## 4. Core Data Flow

```text
1. User clicks "YB Learn" on a YouTube tab (extension/content.js)
2. content.js → POST /api/capture → main.py validates URL, adds to queue_store,
   generates a request_id (uuid4)
3. content.js → chrome.runtime message → background.js opens/focuses the single
   Workspace browser tab at http://127.0.0.1:8000/?url=<captured_url>
4. Workspace page load → static/script.js reads ?url= → POST /api/queue →
   item enters the automatic pipeline (transcript → study note)
5. main.py's single worker thread (_pipeline_worker_loop, backed by a stdlib
   Queue) processes one job at a time: Transcript stage, then Study Note
   stage. The Transcript stage itself makes its own Gemini call
   (gemini_client.generate_quick_summary()) to produce the one-line summary
   saved into the Transcript file, skipped when an existing summary can be
   reused; the Study Note stage separately calls generate_study_note()
6. Stage Guard checks the item's current status before doing work — a stage
   already reached or passed is never re-run; re-requesting it just returns
   the existing result
7. script.js polls GET /api/queue every 1.5s and re-renders the Queue list
8. Once Study Note exists, the user may independently trigger any of the 5
   Learning Model endpoints per Queue Card — these do NOT go through
   _pipeline_queue / the single worker thread; each runs on its own request,
   off the event loop via asyncio.to_thread()
9. Downloads: individual file downloads, or a Knowledge Package (.zip) via
   knowledge_package.py, built from files verified to exist on disk (not
   trusted from stored path fields)
10. History page (GET /api/history) reads history_store.py, independent of
    the Queue's contents
```

---

## 5. State & Persistence

- **No database.** All state is JSON files under `outputs/`: `queue.json`, `history.json`, plus generated artifact files (`.md` / `.json`) under their respective subfolders and JSONL logs under `outputs/logs/`.
- **Queue** (`queue_store.py`) is the in-memory source of truth during a server run, written to `outputs/queue.json` after every mutation. On restart, `queue.json` is reloaded and any item frozen in a non-terminal in-progress status is reset to the last retryable status.
- **History** (`history_store.py`) is a separate, longer-lived record keyed by `video_id`; removing an item from the Queue does not remove it from History.
- **Correlation ID**: `queue_store.add_item()` generates a `request_id` (uuid4) that is mirrored into the History entry, so a run can be traced across Runtime / Gemini-usage / Cache / Error logs even after the Queue item is gone.
- **Artifact files are the real completeness signal.** Several endpoints (Queue Card download button, History card, bulk export) verify a Transcript/Study Note exists on disk rather than trusting a stored path field, because a path field can point to a file that was later deleted or never fully written.
- **Feature flag:** `PRODUCT_INTELLIGENCE_ENABLED` (env var, default true) disables all observability writes without touching the main pipeline; observability writes are all best-effort (failures are swallowed, never raised).

---

## 6. AI / Transcript / Learning Pipeline

**Transcript:** `fetch_subtitle_transcript()` (YouTube captions, `zh-Hant`/`zh-TW`/`zh-Hans`/`zh-CN`/`zh`/`en` preference order) is tried first; on failure, falls back to `yt-dlp` audio download + `faster-whisper` (`base`, CPU, int8) transcription. Output is normalized to Traditional Chinese via `OpenCC("s2twp")` regardless of which path produced it.

**Quick Summary (Gemini, Transcript stage):** once transcript text is obtained (from a cached Transcript file, subtitles, or Whisper), `main.py` calls `gemini_client.generate_quick_summary()` to produce the one-line summary saved into the Transcript file's `## Summary` block. This call is skipped when a summary can already be reused (from the transcript file itself or the in-memory queue item); if it fails (`GeminiConfigError`/`GeminiGenerationError`), the summary is left empty rather than failing the Transcript stage. This is a distinct Gemini call from Study Note generation, made during the Transcript stage.

**Study Note (Gemini):** a separate Gemini call, using a fixed system-instruction prompt inlined in `gemini_client.py` (`generate_study_note`), producing a metadata block + structured Markdown sections. Whether a given video ends up making one or two Gemini calls in the automatic pipeline depends on cache state (e.g. an already-cached Transcript with an already-embedded summary skips the Quick Summary call) — the code does not guarantee a fixed call count per video.

**Learning Model (5 independent, on-demand artifacts, triggered per Queue Card after Study Note exists):**

| Artifact | Reads | Produces |
|---|---|---|
| Knowledge Outline | Transcript | One Sentence + Knowledge Outline |
| Learning Blueprint | Transcript | Structured Knowledge JSON (`structure_type` + shape-specific `content`, via a two-step Structure Detection → Knowledge Extraction Gemini call, `temperature=0`) |
| Teach Back | existing Learning Blueprint (not raw transcript) | Per-learning-point explain/self-check/practice prompts + a fixed 4-question reflection template |
| Action List | existing Learning Blueprint | 3–5 "do today" actions |
| Review | existing Learning Blueprint | Recall questions, workflow recall, optional blank-filling, fixed 4-question reflection template |

All 5 are cache-first: re-requesting an already-generated artifact returns the saved file instead of calling Gemini again. All 5 run off the main pipeline's single-worker queue and off FastAPI's event loop (`asyncio.to_thread`), so they don't block each other or the automatic Transcript/Study Note pipeline.

**Gemini call interception:** every `generate_*()` function routes through one private `_generate_content()` call site, which is the single point where token usage, cost estimate, and error classification are recorded (see `observability/`).

---

## 7. Chrome Extension

Manifest V3, 4 files (`manifest.json`, `background.js`, `content.js`, `content.css`). Host permission scoped to `http://127.0.0.1:8000/*`.

- `content.js` runs on `www.youtube.com`, injects a "▶ YB Learn" button on `/watch` and `/shorts/*` pages, re-syncing visibility on YouTube's `yt-navigate-finish` SPA navigation event (YouTube doesn't reload the document between videos).
- On click: `POST /api/capture` to the backend, then a `chrome.runtime` message to the background service worker to open/focus the Workspace tab — done as two independent steps so a Workspace-opening failure (e.g. stale extension context) isn't misreported as a capture failure.
- `background.js` implements the **Single Workspace** principle: it reuses one existing Workspace tab (navigating it to the new `?url=` and re-triggering the page's own load-time auto-start) instead of opening a new tab per capture; only creates a new tab if none exists.
- The extension itself holds no pipeline logic — all processing happens after the Workspace page loads and calls the backend API.

---

## 8. Testing Strategy

There is no automated test suite (no `pytest`, no `test_*.py`, no CI config) anywhere in the repository. Verification is exclusively manual: each implemented task is validated by a human via the browser and recorded as a Human Test result in `Acceptance_Test.md`. `TODO.md` records the RCA and manual verification steps behind each completed task. This is a deliberate, unchanged project convention, not a gap awaiting automation.

---

## 9. External Dependencies

From `requirements.txt`:

| Package | Role |
|---|---|
| `fastapi`, `uvicorn[standard]` | Web framework / ASGI server |
| `yt-dlp` | YouTube metadata + audio download |
| `faster-whisper` | Local speech-to-text fallback |
| `opencc-python-reimplemented` | Simplified → Traditional Chinese normalization (`s2twp`) |
| `google-genai` | Gemini API client |
| `python-dotenv` | Loads `GEMINI_API_KEY` and other env vars from `.env` |

No database driver, no task queue library, no frontend build tooling — `static/` is served as-is.

---

## 10. Known Technical Constraints

- **Single worker thread** for the automatic Transcript→Study Note pipeline (`_pipeline_queue` / `_pipeline_worker_loop`): jobs for different videos are processed one at a time, in order. The 5 Learning Model endpoints deliberately bypass this queue.
- **Stage Guard is forward-only**: once a stage is reached, re-requesting it never re-runs the work — this trades "can't force a re-run via the API" for "can never accidentally duplicate a finished stage."
- **In-process queue is not durable across a crash mid-job**: `outputs/queue.json` is written after each mutation, but the stdlib `Queue` of pending jobs itself doesn't survive a restart — only the item's last-persisted status does, and that status is reset to a retryable state on load.
- **Windows path-length limits**: Knowledge Package zip folder/file names are truncated to 50 characters and stripped of non-BMP characters (emoji) because Windows Explorer's built-in extractor both enforces `MAX_PATH=260` and rejects otherwise-valid zips containing non-BMP path characters.
- **No login / no multi-user**: `queue_store` and `history_store` are single-process, single-user, file-backed state; nothing in the codebase supports concurrent independent users.
- **Gemini calls are synchronous SDK calls** wrapped in `asyncio.to_thread()` at each call site that needs to avoid blocking the single uvicorn event loop; `gemini_client.py` itself does not use an async client.
- **`GeminiConfigError`** (missing `GEMINI_API_KEY`) is raised before the observability interception point, so it is not captured by Error Intelligence — a one-time environment setup failure, not a runtime error.

---

## 11. Existing Engineering Conventions

- **One artifact type, one module.** Each Learning Model output (`knowledge_outline.py`, `learning_blueprint.py`, `teach_back.py`, `action_list.py`, `review.py`) follows the same shape: a Gemini system-instruction prompt in `gemini_client.py`, a persistence module, and its own API route(s) — not a shared generic "artifact generator."
- **Cache-first generation.** Every on-demand artifact checks for an existing file before calling Gemini again; this pattern is copied module-to-module rather than centralized.
- **Downstream artifacts read upstream artifacts, not raw transcripts.** Teach Back / Action List / Review all read the already-generated Learning Blueprint rather than re-reading the transcript or re-deriving structure.
- **Disk state over stored-path trust.** Completeness checks (download buttons, bulk export candidacy) verify the file exists on disk rather than trusting a stored path field, after this caused a real bug (stale path pointing to a deleted file).
- **Best-effort, non-blocking observability.** Every write in `observability/` swallows its own failures; nothing in that module is allowed to raise into the main request path.
- **Minimal-diff task scoping.** Each implemented task is scoped to touch only the files it needs to; unrelated refactors are explicitly deferred rather than bundled in (e.g. a known duplicated helper function was left in place until a third caller would justify moving it).
