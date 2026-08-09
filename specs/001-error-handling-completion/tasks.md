---

description: "Task list for Feature 001: Transcript / Learning Blueprint Error Handling Completion"

---

# Tasks: Transcript / Learning Blueprint Error Handling Completion

**Input**: Design documents from `/specs/001-error-handling-completion/` (spec.md, plan.md,
research.md, quickstart.md)

**Prerequisites**: plan.md (required, done), spec.md (required, human-approved), research.md
(done), quickstart.md (done). No data-model.md / contracts/ — not applicable to this feature.

**Tests**: This project has no automated test suite (Constitution Principle VI). "Tests" below
means the explicit Human Test scenarios from `quickstart.md`, run manually against the real
server — not unit/integration test code.

**Organization**: Tasks are grouped by user story (US1 = Transcript, P1; US2 = Learning
Blueprint, P2) so each can be implemented and verified independently, per spec.md.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: Which user story this task belongs to (US1 or US2)
- Every task lists its exact file path(s)

## Path Conventions

Single existing project. All production paths are under `app/` (repository root), matching
plan.md's Project Structure. No new directories.

---

## Phase 1: Setup

**Not applicable.** This feature reuses the existing FastAPI application, existing
`error_messages.py` module, and existing frontend — no new project initialization, no new
dependency, no new configuration. (Constitution I: no speculative scaffolding.)

---

## Phase 2: Foundational

**Not applicable — no blocking prerequisites.** US1 (Transcript) and US2 (Learning Blueprint)
touch disjoint code paths and share no new infrastructure; both reuse `classify_error()` and
the existing inline error/retry UX completely unmodified. Either story can start first.

---

## Phase 3: User Story 1 - Correct attribution when subtitle download is rate-limited (Priority: P1) 🎯 MVP

**Goal**: When YouTube subtitle fetch fails with 429/rate-limit and the Whisper fallback also
fails, the user sees a temporary/retry-able message instead of the misleading generic
"找不到可用的逐字稿內容".

**Independent Test**: Force a subtitle-fetch 429 with Whisper fallback also failing; confirm
the Queue Card shows `_SERVICE_UNAVAILABLE_SOURCE` wording, not `_NO_TRANSCRIPT`. Fully
testable and deliverable without any Learning Blueprint change (spec.md, User Story 1).

### Implementation for User Story 1

- [x] T001 [US1] Capture the `SubtitleFetchError` text instead of discarding it in
  `_do_generate_transcript_for_item()`, `app/main.py` (currently lines 312-315) — add a local
  variable (e.g. `subtitle_fetch_error_text`), `None` unless the exception was actually caught,
  set to `str(exc)` inside the existing `except` block. `subtitle_text` itself still becomes
  `None` on failure — no change to the existing fall-through-to-Whisper control flow. See
  research.md Decision 1.
- [x] T002 [US1] Inside the existing `except transcript_service.TranscriptionError as exc:`
  block in `app/main.py` (currently lines 390-403), add the "prefer subtitle message"
  conditional: compute `whisper_message` as today, and — only if a subtitle error was captured
  in T001 — compute `subtitle_message` via the same, unmodified `classify_error()`; use
  `subtitle_message` in place of `whisper_message` only when `subtitle_message ==
  error_messages._SERVICE_UNAVAILABLE_SOURCE` AND `whisper_message ==
  error_messages._NO_TRANSCRIPT`; otherwise leave `whisper_message` unchanged as today.
  `last_error_stage` stays `"transcript"` in all cases. Depends on T001. See research.md
  Decision 2.

### Human Test for User Story 1 (quickstart.md Scenarios 1-5)

- [x] T003 [US1] Human Test — quickstart.md Scenario 1: subtitle 429 + Whisper fallback also
  fails → confirm message names the temporary/rate-limit cause, not the generic "no transcript"
  message. Depends on T002.
- [x] T004 [US1] Human Test — quickstart.md Scenario 2: subtitle fails, Whisper succeeds →
  confirm no error is shown at all (non-regression). Depends on T002.
- [x] T005 [US1] Human Test — quickstart.md Scenario 3: subtitle fails for a non-429 reason
  (e.g. no captions) and Whisper also fails → confirm the existing generic "no transcript"
  message is unchanged (non-regression). Depends on T002.
- [x] T006 [US1] Human Test — quickstart.md Scenario 4: retry after a rate-limit failure →
  confirm the existing Retry action works unchanged and succeeds once the condition clears.
  Depends on T002.
- [x] T007 [US1] Human Test — quickstart.md Scenario 5: regression spot-check against
  `Acceptance_Test.md`'s existing Transcript success scenarios (with and without subtitles).
  Depends on T002.

**Checkpoint**: User Story 1 is fully functional and independently verified. Learning Blueprint
is untouched at this point.

---

## Phase 4: User Story 2 - Correctly-attributed, distinguishable Learning Blueprint failure message (Priority: P2)

**Goal**: Learning Blueprint Gemini failures are classified and displayed as Learning Blueprint
failures, not Study Note failures, reusing the existing inline error/retry UX unchanged.

**Independent Test**: Force a Learning Blueprint `GeminiGenerationError`; confirm the inline
message names Learning Blueprint and the existing retry button works. Fully testable and
deliverable without the Transcript change (spec.md, User Story 2).

### Implementation for User Story 2

- [x] T008 [P] [US2] In `app/error_messages.py`: add the `_SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT`
  constant (placed after the existing `_SERVICE_UNAVAILABLE` constant), then extend
  `classify_error()`'s Gemini-aware branching — (a) the quota/429 return at the current
  `stage == "studynote"` check becomes a three-way check adding `"learning_blueprint"` →
  `_SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT`, and (b) the routing condition `if stage ==
  "studynote":` becomes `if stage in ("studynote", "learning_blueprint"):` so non-quota
  Learning Blueprint failures (safety/unknown) also route correctly instead of falling through
  to YouTube-oriented buckets. Reuse the existing `_CONTENT_FILTERED`/`_UNKNOWN` constants
  as-is for those sub-cases (no new wording for them — see research.md Decision 3 scoping
  note). No dependency on Phase 3 — different file, can run in parallel with T001/T002.
- [x] T009 [US2] In `generate_learning_blueprint()`, `app/main.py` (currently line 982): change
  `error_messages.classify_error(str(exc), stage="studynote")` to
  `error_messages.classify_error(str(exc), stage="learning_blueprint")`. No other line in this
  endpoint changes — `GeminiConfigError` handling (lines 977-978) stays untouched. Depends on
  T008.

### Human Test for User Story 2 (quickstart.md Scenarios 6-9)

- [x] T010 [US2] Human Test — quickstart.md Scenario 6: force a Learning Blueprint
  `GeminiGenerationError` → confirm the inline message (same location as Sprint 8 Task 1) names
  Learning Blueprint, not Study Note wording. Depends on T009.
- [x] T011 [US2] Human Test — quickstart.md Scenario 7: retry after that failure → confirm the
  existing reclick-to-retry pattern (no new button) succeeds once the condition clears. Depends
  on T009.
- [x] T012 [US2] Human Test — quickstart.md Scenario 8: force the same kind of Gemini failure
  independently on Teach Back, Action List, and Review → confirm all three remain completely
  unchanged. Depends on T009.
- [x] T013 [US2] Human Test — quickstart.md Scenario 9: missing/invalid Gemini API key →
  confirm the existing `GeminiConfigError` path is unaffected. Depends on T009.

**Checkpoint**: User Stories 1 AND 2 both work independently. `app/static/script.js` has not
been touched by any task above (confirmed unnecessary — research.md Decision 4).

---

## Final Phase: Polish & Cross-Cutting Concerns

- [x] T014 [P] Cross-cutting Human Test — quickstart.md "Gemini/API call count" check (SC-005):
  during the success-path checks in T004, T007, and T013, confirm via
  `outputs/logs/runtime.jsonl` / `outputs/logs/gemini_usage.jsonl` (or manual counting) that
  Gemini call counts for a successful Transcript run and a successful Learning Blueprint run
  match the pre-change baseline. No file modified — read-only verification.
- [x] T015 Record this feature's Human Test results as a new entry in `Acceptance_Test.md`
  (append only — per Constitution Section 2, `Acceptance_Test.md` is the acceptance-record
  SSOT; this task MUST NOT modify any existing Sprint 1–8.5A entry). Depends on T003-T007,
  T010-T013, T014 all being run and recorded.

**Not included in this task list** (explicitly out of scope, per spec.md and the approved
plan): fixing the separately-discovered Knowledge Outline `stage="studynote"` mislabeling
(`app/main.py` ~line 916) — recorded only as a note in research.md, not as a task here, and not
written into `TODO.md` by this planning stage (per constraint: do not modify Sprint 1–8.5
historical records; the relationship between future Spec Kit `tasks.md` work and `TODO.md` is
an open governance question not yet decided).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup / Foundational**: N/A — nothing blocks either user story.
- **User Story 1 (Phase 3)**: No dependency on User Story 2. Can start immediately.
- **User Story 2 (Phase 4)**: No dependency on User Story 1 (T008 has no incomplete
  dependency). T009-T013 depend only on T008 within this phase.
- **Polish (Final Phase)**: T014 depends on the success-path Human Tests (T004, T007, T013)
  having been run. T015 depends on all Human Test tasks (T003-T007, T010-T013, T014) being
  complete.

### Within Each User Story

- T001 → T002 (same file, same function, sequential; T002 needs the variable T001 introduces).
- T002 → T003, T004, T005, T006, T007 (Human Test tasks verify the code change; no fixed order
  among T003-T007 themselves, but all require T002 done first).
- T008 → T009 (same reasoning: T009's stage value only classifies correctly once T008's
  broadened condition exists).
- T009 → T010, T011, T012, T013 (Human Test tasks; no fixed order among themselves).

### Parallel Opportunities

- T008 [US2] can run in parallel with T001/T002 [US1] — different files (`error_messages.py`
  vs `main.py`'s transcript function), no shared dependency.
- T014 is otherwise independent of T015 order-wise, but T015 should be last since it records
  the outcome of everything before it.
- No two tasks touch the same file concurrently except T001→T002 and T008→T009, both of which
  are explicitly sequential (not marked [P]).

---

## Production Files Touched (summary)

| File | Tasks | Change type |
|---|---|---|
| `app/main.py` | T001, T002 (US1), T009 (US2) | Modified — 3 call-site-level edits, no new function/class |
| `app/error_messages.py` | T008 (US2) | Modified — 1 new constant, 1 broadened condition |
| `app/static/script.js` | none | **Unchanged** — confirmed unnecessary (research.md Decision 4) |
| `Acceptance_Test.md` | T015 | Appended (new entry only, no historical edits) |
| `TODO.md`, `Why.md`, `CLAUDE.md`, any Sprint 1–8.5A record | none | **Untouched by any task** |

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. T001 → T002 → T003-T007 (Human Test). This alone closes the higher-priority, real recorded
   incident (TODO.md Sprint 8 Task 4) and is independently shippable.

### Incremental Delivery

1. User Story 1 (T001-T007) → verify → optionally stop here as a complete, valid increment.
2. User Story 2 (T008-T013) → verify → adds the Learning Blueprint correctness fix.
3. Polish (T014-T015) → close out cross-cutting verification and record results.

Each story adds value without depending on or breaking the other.

---

## Notes

- No `[P]` marker on Human Test tasks (T003-T007, T010-T013) — they are manual verification
  steps run in one sitting against the same server, not independent file edits; sequencing
  them arbitrarily "in parallel" adds no real value.
- Every implementation task (T001, T002, T008, T009) stays within the two files approved for
  production changes (`app/main.py`, `app/error_messages.py`) — no other production file is
  touched by this task list.
- Per Constitution Principle VII / this project's standing convention: no task in this list is
  to be followed by `git add`/commit without a separate, explicit Commit Scope Review — that
  gate applies at `/speckit-implement` time, not to this task list itself.
