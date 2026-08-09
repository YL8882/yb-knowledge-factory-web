# Phase 0 Research: Transcript / Learning Blueprint Error Handling Completion

No `[NEEDS CLARIFICATION]` markers exist in `plan.md`'s Technical Context (this is a small,
already-scoped bug-fix feature with no unknown technology choices). This document instead
records the concrete design decisions needed to implement the spec's requirements with
minimal, reuse-first changes, based on direct reading of the current production code.

## Decision 1: How to stop discarding the subtitle-fetch failure reason (FR-001)

**Decision**: In `app/main.py`, `_do_generate_transcript_for_item()`, replace the bare
`except transcript_service.SubtitleFetchError: subtitle_text = None` (currently lines 312-315)
with a version that also captures the exception text into a new local variable (e.g.
`subtitle_fetch_error_text`), initialized to `None` before the `try` and set to `str(exc)`
inside the `except` block. `subtitle_text` itself still becomes `None` on failure — the
existing fall-through-to-Whisper control flow is unchanged.

**Rationale**: Matches the exact pattern already used a few lines below for
`AudioDownloadError`/`TranscriptionError`, where `exc` is captured and passed to
`classify_error()`. No new capture mechanism is invented.

**Alternatives considered**: Storing the raw exception object instead of `str(exc)` — rejected
because every other `classify_error()` call site in this file already normalizes to `str(exc)`
first; keeping the same convention avoids a special case.

## Decision 2: When to prefer the subtitle-derived message over the Whisper-derived message (FR-002, FR-003, FR-004)

**Decision**: Only inside the existing `except transcript_service.TranscriptionError as exc:`
block (currently lines 390-403) — not the `AudioDownloadError` block. Compute
`whisper_message = classify_error(str(exc), stage="transcript")` (as today) and, only if a
subtitle error was captured, `subtitle_message = classify_error(subtitle_fetch_error_text,
stage="transcript")` (reusing `classify_error()` completely unmodified for this part — any
non-`"studynote"` stage already routes quota/429/rate-limit keywords to the existing
`_SERVICE_UNAVAILABLE_SOURCE` constant, so passing `stage="transcript"` for the subtitle text
is sufficient; no new stage or bucket is needed for Part A).

Use `subtitle_message` instead of `whisper_message` **only when both**:
1. `subtitle_message == _SERVICE_UNAVAILABLE_SOURCE` (the captured subtitle failure text
   actually matched the quota/429/rate-limit keyword group).
2. `whisper_message == _NO_TRANSCRIPT` (the Whisper-side failure is the exact generic/masking
   "empty transcript" case that today hides the true cause).

Otherwise, behavior is byte-for-byte unchanged from today. `last_error_stage` stays
`"transcript"` in all cases (the failing stage genuinely is still the Whisper step) — only the
message *text* changes, so the existing Retry action (`POST /api/queue/{video_id}/retry`)
needs no changes.

**Rationale**: This is the exact, narrowly-scoped condition matching the real, documented
incident (TODO.md, Sprint 8 Task 4 Human Test): subtitle 429 *and* Whisper's own
`TranscriptionError("empty transcript")` colliding. Scoping the fix to only the
`TranscriptionError` branch (not `AudioDownloadError`) avoids extending behavior beyond what
the spec's Acceptance Scenarios and Edge Cases actually describe — `AudioDownloadError` is
already a distinct, already-specific failure that doesn't collide with `_NO_TRANSCRIPT` the
same way.

**Alternatives considered**:
- *Always prefer the subtitle-derived message whenever one exists* — rejected: would regress
  Acceptance Scenario 3 (subtitle fails for a non-rate-limit reason, e.g. no captions available
  — today's generic message is correct there and must stay unchanged).
- *Add a new "subtitle" stage to `classify_error()` with its own dedicated message constant*
  (e.g. "YouTube 暫時限制字幕下載，請稍後再試。", as originally sketched in `TODO.md`'s Product
  Backlog entry) — rejected for this minimal-diff pass: `_SERVICE_UNAVAILABLE_SOURCE` already
  exists, is already correctly worded ("服務目前無法使用或過於忙碌，請稍後再試。" — temporary,
  suggests retry), and reusing it requires zero changes to `error_messages.py` for Part A,
  which better satisfies "reuse existing `classify_error()`" than adding a new bucket. A more
  specific subtitle-only message string can be a future, separately-scoped refinement if
  desired — not required by the approved spec's FR-002 wording ("a distinct, specific
  user-facing message" — `_SERVICE_UNAVAILABLE_SOURCE` already satisfies this by being distinct
  from `_NO_TRANSCRIPT`).

## Decision 3: How to correct the Learning Blueprint stage mislabeling (FR-006, FR-007)

**Decision**: In `app/error_messages.py`:
1. Add `_SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT` as a new constant, placed immediately after
   the existing `_SERVICE_UNAVAILABLE` constant, with the same "temporary, retry, likely Gemini
   quota" framing but naming Learning Blueprint instead of Study Note.
2. Broaden the quota/429 branch (currently `return _SERVICE_UNAVAILABLE if stage ==
   "studynote" else _SERVICE_UNAVAILABLE_SOURCE`) into a three-way check: `"studynote"` →
   `_SERVICE_UNAVAILABLE`; `"learning_blueprint"` → `_SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT`;
   any other stage → `_SERVICE_UNAVAILABLE_SOURCE` (unchanged for every existing non-Gemini
   stage).
3. Broaden the Gemini-aware routing condition (currently `if stage == "studynote":`, which
   also handles the safety/`_CONTENT_FILTERED` and fallback/`_UNKNOWN` cases) to
   `if stage in ("studynote", "learning_blueprint"):` — required so a *non-quota* Learning
   Blueprint Gemini failure (safety filter, or a genuinely unknown Gemini error) still routes
   into the Gemini-aware bucket instead of incorrectly falling through to the YouTube-oriented
   buckets below it in the function (which would be wrong for a pure-Gemini-calling endpoint).

Then in `app/main.py`, `generate_learning_blueprint()`: change the single argument at the
`except gemini_client.GeminiGenerationError` handler from `classify_error(str(exc),
stage="studynote")` to `classify_error(str(exc), stage="learning_blueprint")`. No other line
in this endpoint changes — `GeminiConfigError` handling stays untouched (out of scope per
spec Edge Cases).

**Scoping decision, called out explicitly**: reuse the existing `_CONTENT_FILTERED` /
`_UNKNOWN` constants as-is for Learning Blueprint's safety/unknown sub-cases — no new wording
for those. The approved spec's Acceptance Scenarios (2.1, 2.2) and the `LB-01` resolution
(Option B) only exercise the quota/rate-limit ("transient Gemini error") path; adding
Learning-Blueprint-specific safety/unknown wording is not required by FR-006/FR-007 as written
and would expand scope beyond what Human Review approved.

**Rationale**: This mirrors, call for call, the differentiation pattern Sprint 8 Task 4 already
established for `_SERVICE_UNAVAILABLE` vs `_SERVICE_UNAVAILABLE_SOURCE` — no new mechanism is
invented, only a new instance of an already-proven pattern.

**Alternatives considered**:
- *Just change the stage string without broadening `classify_error()`'s condition* — rejected:
  verified by reading the function that this would actually break classification (a Learning
  Blueprint failure would stop being recognized as Gemini-originating and fall through to
  YouTube/network-oriented buckets that don't apply), which would be a regression, not a fix.
- *Introduce a `Stage` enum/type instead of string literals* — rejected as unrelated refactor;
  every existing stage value in this codebase is an ad-hoc string literal, and introducing a
  type here would touch call sites this feature has no reason to touch (Constitution IV,
  Feature First — no premature abstraction).

## Decision 4: Frontend changes required

**Decision**: None. `app/static/script.js`'s `startLearningBlueprint()` (lines 985-1013)
already does `const message = data.detail || '產生 Learning Blueprint 失敗';
showInlineError(button, message); button.disabled = false;` on any non-OK response — i.e. it
already generically renders whatever `detail` text the backend sends, inline next to the
Learning Blueprint control, and already re-enables the button for retry (Sprint 8 Task 1,
identical pattern used for Teach Back/Action List/Review). The Transcript side surfaces
`last_error` through the existing Queue Card status/error display, also already generic.

**Rationale**: Confirmed by direct reading, not assumption — satisfies constraint "app/static/
script.js must remain unchanged unless a contradiction is discovered." No contradiction was
found.

## Regression risk review (all `classify_error()` / `SubtitleFetchError` call sites re-checked)

- `main.py:375` (`download` stage) — untouched, Part A only touches the `transcript`-stage
  except block.
- `main.py:394` (`transcript` stage) — the Part A target; behavior for every case except the
  narrow "subtitle 429 + Whisper empty transcript" collision is bit-for-bit identical to today.
- `main.py:570/578` (Study Note), `864` (Study Note retry-status), `1046/1119/1192` (Teach
  Back/Action List/Review) — all untouched; Part B only *adds* a new `stage in (...)` branch,
  it does not alter existing `"studynote"` behavior.
- `main.py:916` (**Knowledge Outline endpoint**) — **found, and deliberately NOT fixed here.**
  This call site hardcodes the identical `stage="studynote"` mislabeling pattern as the
  pre-fix Learning Blueprint bug. It is outside this spec's scope (the spec names only
  Transcript and Learning Blueprint). Per FR-009, recorded here as a **future backlog
  candidate** rather than fixed now or written into `TODO.md` by this planning step: *"Knowledge
  Outline endpoint (`generate_knowledge_outline`, `app/main.py` ~line 916) hardcodes
  `stage='studynote'` identically to the pre-fix Learning Blueprint bug — same root cause, not
  yet confirmed as user-impacting, not in this spec's scope; candidate for a future,
  independently-scoped fix using the same `LB-01`-style resolution."*
- `transcript.py:113` (`SubtitleFetchError(str(exc))`, the only raise site) — untouched; Part A
  only changes how `main.py` handles the exception after it's raised.
- `main.py:312-315` (the only `except transcript_service.SubtitleFetchError:` in the codebase)
  — the Part A target.

**Conclusion**: no other call site is affected by either change.

## Gemini/API call count impact

**Zero increase, confirmed.** Both changes execute only in exception-handling / message-
classification code paths that run *after* a Gemini or yt-dlp call has already failed.
`classify_error()` is a pure, local string-matching function with no I/O or network call — Part
A calls it one additional time in the failure path only (never in the success path). The
success path (three existing `generate_quick_summary` call sites for Transcript's summary, one
`generate_learning_blueprint` call site) is completely untouched in both count and location.
Satisfies spec FR-010 and SC-005.
