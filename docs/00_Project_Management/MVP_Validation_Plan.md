---
Version: v1.0
Status: Final
Owner: Claude Code
Document: MVP Validation Plan
Category: Quality Assurance
Purpose: Define the test matrix and methodology for systematic MVP validation using real YouTube URLs.
Scope: YB Knowledge Factory MVP v0.1
Priority: Critical
Last Updated: 2026-07-30
Related Documents:
  - MVP_Test_Report.md
  - Sprint_1_1_Report.md
---

# MVP Validation Plan

> Validates the existing MVP end-to-end against real YouTube videos. No application code will be changed unless a critical bug blocks testing itself.

---

# 1. Preflight Checks (completed before test execution)

| Check | Result |
|---|---|
| Network reachability to YouTube | ✅ `curl https://www.youtube.com` → HTTP 200 |
| `GEMINI_API_KEY` configured in `.env` | ✅ Present (value not inspected/printed) |
| Required Python packages import (`fastapi`, `uvicorn`, `yt_dlp`, `faster_whisper`, `google.genai`) | ✅ All OK |
| `ffmpeg` installed | ❌ Not found — known pre-existing issue (`MVP_Test_Report.md` §5), tests proceed anyway since the app doesn't hard-require it |

---

# 2. Test Matrix

Real, verifiable video IDs were selected via `yt-dlp` metadata lookups (not guessed), chosen to cover every category requested while overlapping categories efficiently (each video satisfies more than one dimension where possible, to keep total real transcription + Gemini calls to a practical number).

| ID | Category Coverage | Video | Duration | Language | Notes |
|---|---|---|---|---|---|
| TC-1 | Short, English | "Me at the zoo" (`jNQXAC9IVRw`) | ~19 sec | English | The famous first-ever YouTube video; already used in prior acceptance testing |
| TC-2 | Chinese, medium-length, normal URL | `C_X_rV_3YcM` | ~5–8 min (est.) | Chinese | Reused from a prior sprint's manual test; re-run fresh here for timed metrics |
| TC-3 | Chinese, Shorts URL format | `o1BUsURZX8A` | short (Shorts) | Chinese | Tests `/shorts/` URL handling |
| TC-4 | Long, English | TEDx talk "The first 20 hours" (`5MgBikgcWnY`) | 1167 sec (~19.5 min) | English | Found via `yt-dlp ytsearch`; ~60× longer than TC-1 |
| TC-5 | No official subtitles | `bvz_zK5ZxpM` | 347 sec (~5.8 min) | English | Confirmed via `yt-dlp --list-subs` → "has no subtitles" (no manual/official track; only auto-captions exist, which the app ignores anyway — see §4 caveat) |
| TC-6 | Invalid URL — empty | `""` | — | — | |
| TC-7 | Invalid URL — non-YouTube | `https://example.com/foo` | — | — | |
| TC-8 | Invalid URL — well-formed but nonexistent video ID | `https://www.youtube.com/watch?v=zzzzzzzzzzz` | — | — | |

---

# 3. Methodology

For each of TC-1–TC-5, executed against the locally running app (`python run.py`, `http://127.0.0.1:8000`) via its real HTTP API — the same endpoints the browser UI calls:

1. `POST /api/queue` — add video, record wall-clock time and whether metadata (title) is returned correctly.
2. `POST /api/queue/{id}/transcript` — generate transcript, record wall-clock time, HTTP status, and inspect the saved `outputs/transcripts/*.md` file for format correctness (title line, URL line, non-empty transcript body) and a qualitative read of transcription accuracy.
3. `POST /api/queue/{id}/study-note` — generate Study Note, record wall-clock time, HTTP status, and inspect the saved `outputs/study_notes/*.md` file against the current Output Schema (Metadata block + 9 sections), plus a qualitative read of content quality (does it reflect the actual video, no fabrication, Executive Summary ≤100 characters, etc).
4. `GET /api/queue/{id}/transcript/download` and `.../study-note/download` — confirm both downloads return the correct file with `Content-Disposition: attachment`.

For TC-6–TC-8: `POST /api/queue` only, confirming the correct HTTP 400 and error message, and that the server doesn't crash.

**Metrics recorded per case:** success/fail per step, execution time per step, transcript quality (qualitative), study note quality (qualitative), download verification (pass/fail), and full failure detail where applicable.

---

# 4. Known Scope Limitation (superseded)

As of 2026-08-01, `app/transcript.py` now tries YouTube's caption track first
(`fetch_subtitle_transcript`, manual then auto-generated, via `yt-dlp`) and only
falls back to downloading audio and transcribing via Faster Whisper when no usable
caption track exists. "Video without subtitles" (TC-5) therefore does exercise a
different code path than a captioned video — TC-5 should fall through to the
download+Whisper path, while other cases with captions should skip audio download
entirely.

---

# 5. Out of Scope for This Validation

- Private videos (would require an account-authenticated test video, not attempted here without one on hand).
- Age-restricted / region-locked videos.
- Videos longer than ~20 minutes (kept TC-4 at ~19.5 min to keep total CPU-bound Whisper transcription time practical for this session; this is still ~60× the baseline short-video case).
- Load/concurrency testing (multiple simultaneous requests) — this MVP is explicitly single-user, non-concurrent by design (`Technical_Decision.md`).
