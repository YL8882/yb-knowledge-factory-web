---
Version: v1.0
Status: Final
Owner: Claude Code
Document: Sprint 1-1 Report
Category: Project Management
Purpose: Record that Sprint 1-1's objective (a runnable MVP skeleton with mock backend) is already satisfied by the existing implementation, and propose the next Sprint.
Scope: YB Knowledge Factory MVP v0.1
Priority: High
Last Updated: 2026-07-30
Related Documents:
  - MVP_Test_Report.md
  - Engineering_Understanding_Report.md
  - Project_Dashboard.md
---

# Sprint 1-1 Report

> Sprint 1-1 asked for a runnable skeleton: a simple web UI (URL input, Generate button, status area), a full frontend→backend request round-trip, and a runnable local app — explicitly with mock data, deferring real Transcript/Study Note generation. The repository already contains a working, tested implementation that covers every one of these points and goes further (real generation, not mock). Per your direction, this Sprint is being closed as already-complete rather than downgraded to a mock version. No code was changed to produce this report.

---

# 1. Requirement-by-Requirement Status

| Sprint 1-1 Requirement | Status | Evidence |
|---|---|---|
| 1. Simple web interface | ✅ Done | `app/templates/index.html` + `app/static/style.css`, served at `GET /` |
| 2. YouTube URL input, Generate button, status area | ✅ Done | `index.html` / `static/script.js`: URL input (`#youtube-url`), Generate button (`#generate-btn`), status area (`#status`, shows info/success/error states) |
| 3. Button click triggers full frontend→backend flow | ✅ Done — **and real, not mock** | `script.js`'s `addToQueue()` → `POST /api/queue` → `app/main.py` validates the URL (`youtube.py`) and fetches real video metadata via yt-dlp, returns it to the UI, which re-renders the queue |
| 4. Application runnable locally | ✅ Verified today | `python run.py` → `uvicorn` on `127.0.0.1:8000`. Just confirmed live: server boots cleanly, `GET /` returns HTTP 200 with the actual home page HTML, then the dev server was stopped cleanly (no leftover process) |
| 5. Transcript / Study Note NOT implemented yet (mock only) | ⚠️ Exceeded, not matched | Both are fully implemented and real: Transcript via yt-dlp + Faster Whisper (`app/transcript.py`), Study Note via Gemini 2.5 Flash (`app/gemini_client.py`, `app/study_note.py`). Per your instruction, these are being **kept as-is, not downgraded to mock** |
| 6. Working project structure + end-to-end request flow | ✅ Done — full pipeline, not just skeleton | Queue add/list/remove/duplicate-detection (`queue_store.py`) → Transcript generation + download → Study Note generation + download, all wired through real FastAPI routes in `main.py` |

**Deliverables:**

- Runnable application — already exists (see above).
- Local startup instructions — already documented in `README.md` §「安裝與執行」:
  1. `pip install -r requirements.txt`
  2. Copy `.env.example` → `.env`, set `GEMINI_API_KEY`
  3. `python run.py`
  4. Open `http://localhost:8000`
- This report.

---

# 2. Why This Is Being Closed As "Already Complete," Not "Redone as Mock"

Sprint 1-1's mock-data framing is a standard "start from zero" bootstrap step. This repository isn't at zero: Milestone 02 (Build MVP v0.1) was already built, tested (`MVP_Test_Report.md`, full workflow + 5 error scenarios, PASS), and formally closed earlier today, followed by a repository cleanup (`Repository_Cleanup_Report.md`). Reverting working Transcript/Study Note calls to mock data would be a real regression against an already-accepted, working product — not a step forward. Per your explicit instruction, no existing functionality was removed or simplified to produce this report.

---

# 3. Proposed Next Sprint (for your review — not started)

Since Sprint 1-1's premise doesn't match where the project actually is, here are the concrete options that *do* match current repository state, in order of recommendation:

## Option A (recommended): Sprint 1-2 — Close the spec/implementation gaps already on record

Small, contained, mostly documentation + one narrow code decision. These were identified in `Engineering_Understanding_Report.md` §4.1 and are still open:

1. `PRD.md`, both `Workflow_Specification.md` copies, and `Prompt_Specification.md` still describe the old 5-section Chinese Study Note structure, while the actual implementation (and the Template/Output Schema updated this morning) uses the 9-section English structure. These three "Final" docs were never reconciled with that decision.
2. The OpenCC (Simplified→Traditional Chinese) conversion step required by `Technical_Decision.md` and `docs/03_Workflows/Workflow_Specification.md` is not implemented anywhere in code.

Rationale: these are pre-existing, known inconsistencies between frozen governance docs and the real product. Building new features (UI/UX, browser extension) on top of unresolved contradictions makes them harder to untangle later.

## Option B — Sprint 1-2 — Harden the MVP backlog items already logged as deferred

From `MVP_Test_Report.md` §6 (explicitly deferred, not yet started):

- Queue persistence (currently in-memory only, cleared on restart)
- Gemini automatic retry on failure (currently fails once, no retry)
- Frontend auto-polling / auto-pipeline (currently requires a manual click per stage per queue item, rather than one Generate triggering the whole pipeline automatically — this was also flagged as a deviation from `Application Architecture Blueprint.md`'s "Auto Pipeline" principle)

Rationale: strengthens the existing, already-accepted MVP before layering new UI/UX work on top of it.

## Option C — Begin Milestone 03 (Improve UI/UX) per `Project_Dashboard.md`'s existing roadmap

Rationale: follows the roadmap as already written, but starting new UI/UX work while the Option A/B items remain open risks compounding the existing drift.

---

# Stop Condition

Sprint 1-1 is closed. No code was changed. Waiting for your decision on which option (A, B, C, or something else) becomes Sprint 1-2 before any implementation begins.
