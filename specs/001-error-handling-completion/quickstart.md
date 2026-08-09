# Quickstart Validation Guide: Transcript / Learning Blueprint Error Handling Completion

This project has no automated test suite (Constitution Principle VI). Validation is exclusively
manual Human Test, run against the real local server. This guide lists the runnable scenarios
that prove the feature works end-to-end, mapped to `spec.md`'s Acceptance Scenarios and Success
Criteria. It does not include implementation code — see `research.md` for the design and
`tasks.md` (once generated) for the implementation steps.

## Prerequisites

- Local YB Learn server running (`python run.py`), same as any other Human Test in this
  project.
- A valid `GEMINI_API_KEY` configured (`.env`), same as normal operation.
- Access to `outputs/logs/runtime.jsonl` and `outputs/logs/gemini_usage.jsonl` for the
  cross-cutting Gemini-call-count check (optional but recommended).

## Part A — Transcript subtitle 429 misattribution (User Story 1)

### Scenario 1 — Subtitle 429 + Whisper fallback also fails (Acceptance Scenario 1.1, SC-001)

**Setup**: A video where subtitle download fails with a 429/rate-limit response *and* the
Whisper fallback also fails to produce a transcript (e.g. during an observed YouTube
rate-limit window, matching the real incident recorded in `TODO.md` Sprint 8 Task 4; or a
controlled substitute where the Whisper fallback is forced to fail, e.g. a silent/near-empty
test clip).

**Run**: Submit the video through the normal capture flow; wait for the pipeline to reach a
failed Transcript state.

**Expected outcome**: The Queue Card shows a message identifying the condition as temporary
and suggesting a retry (`_SERVICE_UNAVAILABLE_SOURCE`, "服務目前無法使用或過於忙碌，請稍後再
試。") — **not** the generic "找不到可用的逐字稿內容" message.

### Scenario 2 — Subtitle fails, Whisper succeeds (Acceptance Scenario 1.2, FR-004)

**Setup**: A video where subtitle fetch fails for any reason but the Whisper fallback succeeds
normally.

**Run**: Submit the video; wait for the pipeline to complete.

**Expected outcome**: Transcript completes normally, status reaches "Transcript Ready", and no
error is ever shown — identical to pre-change behavior.

### Scenario 3 — Non-429 subtitle failure + Whisper also fails (Acceptance Scenario 1.3, FR-004, non-regression)

**Setup**: A video with no captions available at all (subtitle failure text contains no
quota/429/rate-limit keyword) where the Whisper fallback also produces an empty transcript.

**Run**: Submit the video; wait for the pipeline to reach a failed Transcript state.

**Expected outcome**: The existing generic "找不到可用的逐字稿內容" message is shown, unchanged
from today.

### Scenario 4 — Retry after a rate-limit failure (Acceptance Scenario 1.4, FR-005, SC-002)

**Setup**: Continue from Scenario 1's failed state (or any Transcript failure state).

**Run**: Click the existing Retry action.

**Expected outcome**: Retry re-triggers Transcript generation exactly as it does for every
other Transcript failure today; once the underlying condition clears, Transcript (and the
downstream pipeline) completes successfully without the user needing to self-diagnose the
cause.

### Scenario 5 — Regression spot-check (SC-004)

**Setup**: A normal video with available subtitles, and a normal video without subtitles
(clean Whisper path).

**Run**: Submit both through the normal flow.

**Expected outcome**: Both complete with correct Transcript output and summary, matching
`Acceptance_Test.md`'s existing Sprint scenarios — no behavioral difference from before this
feature.

## Part B — Learning Blueprint stage mislabeling (User Story 2)

### Scenario 6 — Learning Blueprint Gemini failure attribution (Acceptance Scenario 2.1/2.2, SC-003)

**Setup**: A Queue item with a completed Transcript. Force a `GeminiGenerationError` on the
Learning Blueprint call (e.g. a temporarily exhausted/misconfigured Gemini quota, reverted
before commit).

**Run**: Click "建立知識架構" (the Learning Blueprint trigger) on the Queue Card.

**Expected outcome**: An inline error message appears next to the Learning Blueprint control
(same location Sprint 8 Task 1 established), worded to name Learning Blueprint — not the
Study Note quota wording.

### Scenario 7 — Retry after Learning Blueprint failure (Acceptance Scenario 2.3)

**Setup**: Continue from Scenario 6's failed state.

**Run**: Click the same Learning Blueprint trigger button again (no new button — existing
reclick-to-retry pattern).

**Expected outcome**: The retry succeeds once the underlying Gemini condition clears, using the
existing control unchanged.

### Scenario 8 — No regression to Teach Back / Action List / Review (Acceptance Scenario 2.4)

**Setup**: A Queue item with a completed Learning Blueprint. Force the same kind of Gemini
failure independently on Teach Back, Action List, and Review.

**Run**: Trigger each of the three modules in turn.

**Expected outcome**: All three show their existing Study-Note-stage-classified message and
existing inline/retry behavior, completely unchanged by this feature.

### Scenario 9 — `GeminiConfigError` path unaffected (Edge Case, out-of-scope confirmation)

**Setup**: A missing or invalid `GEMINI_API_KEY`.

**Run**: Trigger Learning Blueprint generation.

**Expected outcome**: The existing raw-detail `GeminiConfigError` path (lines 977-978,
untouched by this feature) behaves exactly as before.

## Cross-cutting — Gemini/API call count (SC-005)

During Scenarios 2, 5, and 9 above (the success-path checks), confirm via
`outputs/logs/runtime.jsonl` / `outputs/logs/gemini_usage.jsonl` (or manual counting) that the
number of Gemini API calls for a successful Transcript run (one `generate_quick_summary` call)
and a successful Learning Blueprint run (one `generate_learning_blueprint` call) matches the
pre-change baseline — no extra calls introduced by either fix.

## Definition of Done for this feature

All 9 scenarios above run against the real local server with the expected outcomes observed
and recorded (PASS/FAIL, per this project's Test First → Record Second discipline — no
scenario is marked PASS without being actually run). `Acceptance_Test.md` is updated with the
results as a new entry once implementation is approved and complete (not part of this
Spec Kit documentation — `Acceptance_Test.md` remains the single source of truth for
acceptance records per the Constitution).
