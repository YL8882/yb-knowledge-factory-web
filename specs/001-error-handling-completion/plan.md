# Implementation Plan: Transcript / Learning Blueprint Error Handling Completion

**Branch**: `001-error-handling-completion` (spec directory only — no git branch; work stays on `main`, see spec.md) | **Date**: 2026-08-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-error-handling-completion/spec.md`

## Summary

Two independent, small correctness fixes to existing (already-shipped) error handling, with
zero new architecture:

1. **Transcript**: stop discarding the YouTube subtitle-fetch failure reason, and — only in
   the specific case where the Whisper fallback also fails with a generic "empty transcript"
   result — prefer the subtitle failure's classified message (already producible by the
   existing, unmodified `classify_error()`) so the user sees a temporary/retry-able cause
   instead of a misleading "no transcript found" message.
2. **Learning Blueprint**: correct the hardcoded `stage="studynote"` argument passed to
   `classify_error()` when a Learning Blueprint Gemini call fails, so the failure is attributed
   to Learning Blueprint (new stage + new message constant, following the exact
   `_SERVICE_UNAVAILABLE` / `_SERVICE_UNAVAILABLE_SOURCE` differentiation pattern already
   established in Sprint 8 Task 4) instead of Study Note.

Two files change (`app/main.py`, `app/error_messages.py`), four call-site-level edits total.
No frontend changes — `app/static/script.js` already generically renders whatever `detail`
string the backend returns and already supports retry (Sprint 8 Task 1).

## Technical Context

**Language/Version**: Python 3.x (FastAPI backend, existing `app/` package) + vanilla JS
(existing `app/static/script.js`, unchanged by this feature)

**Primary Dependencies**: None added. Reuses existing `app/error_messages.py`
(`classify_error()`), existing `app/transcript.py` (`SubtitleFetchError`), existing
`app/gemini_client.py` (`GeminiGenerationError`) — all already in the dependency graph.

**Storage**: N/A — no persisted data entity introduced or changed. `last_error` /
`last_error_stage` fields on the in-memory/`outputs/queue.json`-backed Queue item already
exist (Sprint 8.5A / earlier); this feature only changes which string value is written to
`last_error` in one specific case, and which `stage` argument is passed at one call site.

**Testing**: Manual Human Test only (this project has no automated test suite by design —
Constitution Principle VI, `Development_Workflow_Standard.md` §5–6). See
[quickstart.md](./quickstart.md) for the full scenario list.

**Target Platform**: Existing YB Learn local FastAPI server (Windows, `python run.py`),
unchanged.

**Project Type**: Existing single-project web application (FastAPI backend + static
HTML/CSS/JS frontend). Not a new project type.

**Performance Goals**: N/A — this feature does not touch a hot path; it only affects
already-failing requests (error-classification code, no I/O, no additional network/Gemini
calls per spec FR-010 and SC-005).

**Constraints**: Reuse-first, minimal-diff (Constitution I, IV); no new retry architecture
(spec FR-005, FR-008); no increase in Gemini/API call count (spec FR-010, SC-005); no
regression to any existing `classify_error()` branch or other Learning Model module's error
handling (spec FR-009, FR-011).

**Scale/Scope**: 2 production files, 4 call-site-level edits, 0 new files, 0 new UI, 0 new
dependencies, 0 schema/storage changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design — see below.*

| Principle | Check | Result |
|---|---|---|
| I. MVP First, Reduce Friction, Keep It Simple | Fixes a real, already-shipped correctness gap; no speculative abstraction (plain conditional, no new function/class) | PASS |
| II. One Sprint = One Deliverable | 2 files, 4 edits, independently testable per User Story — confirmed small enough for a single Sprint | PASS |
| III. Structure Knowledge, Make It Stick | Not directly applicable (this feature is error-handling correctness, not a Learning Model capability) — no conflict | PASS (N/A) |
| IV. Feature First, Refactor Later | No cross-cutting refactor introduced; the one adjacent issue found (Knowledge Outline endpoint sharing the same `stage="studynote"` mislabeling) is explicitly deferred, not folded in | PASS |
| V. RCA Before Fix | Both root causes verified by direct code reading (not assumption) before this plan was written — `main.py:312-315`, `main.py:982`, `error_messages.py`'s stage-gated branching | PASS |
| VI. Test First, Human Test Required | No automated suite; [quickstart.md](./quickstart.md) defines concrete Human Test scenarios per Acceptance Scenario; no PASS is pre-filled | PASS |
| VII. Human Review Before Commit, No Automatic Push | This plan itself requires Human Review before `/speckit-tasks`; implementation will require Commit Scope Review before any `git add` | PASS (procedural, enforced outside this document) |
| VIII. Documentation Discipline | No new planning documents beyond Spec Kit's own required artifacts (plan.md, research.md, quickstart.md); existing `TODO.md`/`Acceptance_Test.md` remain untouched and authoritative for Sprint tracking / acceptance record | PASS |

**No violations. Complexity Tracking table below is empty (nothing to justify).**

## Project Structure

### Documentation (this feature)

```text
specs/001-error-handling-completion/
├── spec.md               # Already exists — human-approved
├── plan.md               # This file
├── research.md           # Phase 0 output (this command)
├── quickstart.md         # Phase 1 output (this command)
└── tasks.md              # Phase 2 output (/speckit-tasks command — NOT created by this command)
```

No `data-model.md` — this feature introduces no persisted data entity (spec's own "Key
Entities: Not applicable"). No `contracts/` — no new external interface; existing endpoint
request/response *shapes* are unchanged, only the text content of `detail` / `last_error`
changes for specific failure cases.

### Source Code (repository root)

```text
app/
├── main.py              # MODIFIED — Part A (subtitle-fetch capture + conditional, inside
│                         #   _do_generate_transcript_for_item()) and Part B (one stage-string
│                         #   argument change, inside generate_learning_blueprint())
├── error_messages.py     # MODIFIED — Part B only (one new constant, one broadened condition)
├── transcript.py         # UNCHANGED — SubtitleFetchError already raised with the needed text;
│                         #   no change to how/when it's raised
├── gemini_client.py       # UNCHANGED
└── static/
    ├── script.js          # UNCHANGED — already generically renders `detail` inline and
    │                       #   already supports retry (Sprint 8 Task 1)
    └── style.css           # UNCHANGED
```

**Structure Decision**: This is an existing single-project FastAPI + static-frontend
application (not a new library/CLI/mobile structure). The feature fits entirely inside the
existing `app/` package with no new top-level directories, matching the "Option 1: Single
project" shape already in use by the rest of YB Learn.

## Constitution Check (post-design re-check)

Re-checked after Phase 1 design (research.md, quickstart.md): no new violations introduced by
the concrete design (see research.md for the exact conditional logic and constant names).
Still PASS on all applicable principles above.

## Complexity Tracking

*(Empty — Constitution Check has no violations to justify.)*
