# Feature Specification: Transcript / Learning Blueprint Error Handling Completion

**Feature Branch**: `001-error-handling-completion` (spec directory only — no git branch was created; no `before_specify` git hook is configured in `.specify/extensions.yml`, so this feature continues to be developed directly on `main`, consistent with this project's existing convention)

**Created**: 2026-08-08

**Status**: Draft

**Input**: User description: "改善 YB Learn 現有錯誤處理，使使用者看到真正且可行動的錯誤原因，而不是被誤導成影片本身無法處理。(1) Transcript：當 YouTube subtitle fetch 遇到 429 / rate limit，且 Whisper fallback 也失敗時，不應把真正的暫時性錯誤覆蓋成一般「找不到逐字稿」。(2) Learning Blueprint：GeminiGenerationError / HTTP 500 等暫時性 Gemini 錯誤，應沿用既有 inline error + retry UX，並提供一致、可理解、可行動的錯誤訊息。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Correct attribution when subtitle download is rate-limited (Priority: P1)

A user submits a YouTube video whose subtitle download is temporarily rate-limited by
YouTube (HTTP 429). The system falls back to audio download + local transcription, but that
fallback also fails (e.g. audio unavailable, transient network issue). Today the user sees a
generic "找不到可用的逐字稿內容" (no transcript content found) message, which reads as a
permanent, video-specific failure. In reality, simply retrying a short time later succeeds,
because the underlying cause was a temporary rate limit — but the user has no way to know
that from the message shown.

**Why this priority**: This is not a hypothetical scenario — it is a real, recorded incident
(TODO.md, Sprint 8 Task 4 Human Test) where the user hit exactly this condition and only
understood the true cause after RCA by the assistant. It directly misleads the user about
whether the product can process their video at all.

**Independent Test**: Can be fully tested by forcing a subtitle-fetch 429 response (or using a
real video during an active YouTube rate-limit window) with Whisper fallback also failing, and
confirming the message shown names the temporary/rate-limit cause rather than the generic
"no transcript" message. Delivers value independently of any Learning Blueprint change.

**Acceptance Scenarios**:

1. **Given** a video whose subtitle download fails with a 429/rate-limit response, **When**
   the Whisper fallback also fails to produce a transcript, **Then** the user sees a message
   that identifies the condition as temporary and suggests retrying, distinct from the
   existing generic "no transcript content found" message.
2. **Given** a video whose subtitle download fails with a 429/rate-limit response, **When**
   the Whisper fallback succeeds, **Then** the user sees no error at all — the existing
   successful-fallback behavior is unchanged.
3. **Given** a video whose subtitle download fails for a reason unrelated to rate-limiting
   (e.g. no captions exist for the video) and Whisper fallback also fails, **When** the
   failure is reported, **Then** the existing generic "no transcript content found" message
   continues to be shown unchanged (this case is not misleading today and is not regressed).
4. **Given** the user retries a Transcript that failed due to temporary rate-limiting, **When**
   the retry succeeds, **Then** the existing "Retry" action works exactly as it does for every
   other Transcript failure today (no new retry mechanism is introduced).

---

### User Story 2 - Correctly-attributed, distinguishable Learning Blueprint failure message (Priority: P2)

A user triggers Learning Blueprint generation and the underlying Gemini call fails (rate
limit, quota, or transient service error). Today the failure is already shown inline next to
the triggering Queue Card and the existing control already allows retry (Sprint 8 Task 1) —
but the error is internally classified using the Study Note failure stage, so the message the
user sees is worded as a Study Note failure rather than a Learning Blueprint failure. The user
needs the message to correctly identify Learning Blueprint as the source of the failure.

**Why this priority**: Lower priority than User Story 1 because this is a narrower,
already-scoped correctness fix (confirmed via `LB-01` resolution, Human Review 2026-08-08,
Option B) rather than a missing capability — Sprint 8 Task 1 already built the inline
error/retry mechanism this story reuses unchanged.

**Independent Test**: Can be tested independently of User Story 1 by forcing a Learning
Blueprint Gemini failure and confirming (a) the message is attributed to Learning Blueprint,
not Study Note, and (b) the existing inline display and retry control continue to work
unchanged.

**Acceptance Scenarios**:

1. **Given** a Learning Blueprint generation request fails because of a transient Gemini
   error, **When** the failure is classified, **Then** it is classified using a
   Learning-Blueprint-specific stage identifier, not the Study Note stage identifier.
2. **Given** a Learning Blueprint generation request fails because of a transient Gemini
   error, **When** the message is shown to the user, **Then** it is worded as a Learning
   Blueprint failure and is shown inline next to the Learning Blueprint control on the
   triggering Queue Card (unchanged location from Sprint 8 Task 1).
3. **Given** a Learning Blueprint generation request has failed, **When** the user retries,
   **Then** the retry uses the existing control (no new retry button, no new retry
   architecture) and succeeds once the underlying Gemini condition clears.
4. **Given** Teach Back, Action List, or Review encounter a Gemini failure, **When** their
   errors are classified and displayed, **Then** their behavior is unchanged by this feature —
   only the Learning Blueprint stage identifier and message are corrected.

---

### Edge Cases

- What happens when subtitle fetch fails with 429 but the Whisper fallback succeeds? The
  fallback succeeds transparently and no error is ever shown to the user — unchanged from
  today.
- What happens when subtitle fetch fails for a non-rate-limit reason (no captions available)
  and Whisper also fails? The existing generic message remains correct and unchanged; this
  feature only changes the rate-limit-specific case.
- What happens if the user retries a rate-limited Transcript multiple times in quick
  succession? Each attempt is independent; the message is shown identically each time until
  the underlying condition clears or a different failure occurs. No new debouncing or
  cooldown logic is introduced.
- What happens when Learning Blueprint fails due to a missing Gemini API key
  (`GeminiConfigError`) rather than a transient `GeminiGenerationError`? Out of scope — this
  is a documented, separate Known Limitation (TODO.md, Sprint 8.5A Task 4) and is not changed
  by this feature.
- What happens to Queue/History items that already failed before this feature ships? They are
  not retroactively reprocessed; the improved message applies to failures occurring after this
  feature ships.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST preserve the original subtitle-fetch failure reason instead of
  discarding it when falling back to audio download + local transcription.
- **FR-002**: System MUST classify a subtitle-fetch failure caused by YouTube rate-limiting
  (429) into a distinct, specific user-facing message that identifies the condition as
  temporary and suggests retrying — distinct from the existing generic "no transcript content
  found" message.
- **FR-003**: When the Whisper fallback also fails after a subtitle-fetch rate-limit failure,
  the message shown to the user MUST reflect the original rate-limit cause, not only the
  generic fallback failure.
- **FR-004**: Subtitle failures unrelated to rate-limiting, and the existing successful-
  fallback path, MUST continue to behave exactly as they do today (no regression).
- **FR-005**: The existing Transcript "Retry" action MUST continue to work unchanged for this
  and every other Transcript failure cause — no new retry mechanism is introduced for
  Transcript.
- **FR-006**: System MUST classify Learning Blueprint Gemini failures using a
  Learning-Blueprint-specific stage identifier, distinct from the Study Note stage identifier
  currently used, so the failure is correctly attributed.
- **FR-007**: System MUST show a Learning-Blueprint-specific user-facing message for Learning
  Blueprint Gemini failures, distinct from the existing Study Note failure message, so the
  user does not mistake a Learning Blueprint failure for a Study Note failure.
- **FR-008**: Learning Blueprint failure display and retry MUST continue to use the existing
  inline error display and existing retry control already established in Sprint 8 Task 1 — no
  new retry architecture and no new UI component are introduced.
- **FR-009**: This feature MUST NOT expand investigation into Learning Blueprint retry
  behavior beyond the confirmed stage-identifier and message gap. Any additional, independent
  issue discovered during implementation MUST be recorded as a Product Backlog item in
  `TODO.md` and MUST NOT be folded into this feature's scope.
- **FR-010**: Successful Transcript and Learning Blueprint generation flows MUST NOT change
  behavior, response shape, or the number of Gemini/API calls made, as a result of this
  feature.
- **FR-011**: All existing, correctly-functioning `classify_error()` branches (non-429
  subtitle failures, non-Gemini Transcript/Download failures, and Teach Back/Action
  List/Review) MUST NOT be altered by this feature.

### Resolved Clarification — `LB-01`

**Resolution (Human Review, 2026-08-08): Option B.** The mislabeled `stage="studynote"`
argument is corrected, and a Learning-Blueprint-specific user-facing message is added,
distinct from the Study Note message. No new retry architecture or UI is introduced, and no
further investigation into Learning Blueprint retry behavior beyond this confirmed gap is
performed as part of this feature — any newly-discovered, independent issue is recorded to
the Product Backlog instead (see FR-009).

### Key Entities

*(Not applicable — this feature changes error classification and message content on existing
failure paths; it does not introduce or modify any persisted data entity.)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: When a subtitle download is rate-limited by YouTube and the Whisper fallback
  also fails, the user sees a message naming the temporary/rate-limit cause, instead of the
  generic "no transcript content found" message, in 100% of such cases.
- **SC-002**: A user who retries a Transcript that failed due to temporary rate-limiting can
  do so using the existing Retry action, without needing to self-diagnose the cause.
- **SC-003**: Learning Blueprint Gemini failures are shown with a message that correctly
  identifies Learning Blueprint (not Study Note) as the source, in 100% of such failures, with
  zero regression to the existing inline display and retry standard established for Teach
  Back/Action List/Review.
- **SC-004**: Zero regressions against existing Sprint 1–8.5A Acceptance Test scenarios for
  Transcript and Learning Blueprint success paths, verified via Human Test (this project has
  no automated test suite; Human Test is the sole verification gate per the Constitution).
- **SC-005**: No increase in the number of Gemini/API calls made during a normal, successful
  Transcript or Learning Blueprint generation, compared to current behavior.

## Assumptions

- The existing Transcript "Retry" action (re-triggering Transcript generation for a Queue
  item) is reused as-is; this feature does not design a new retry UI for Transcript.
- The existing inline error/retry pattern established in Sprint 8 Task 1 (Teach Back, Action
  List, Review) is the reference standard for Learning Blueprint; this feature does not design
  a new UI pattern.
- This feature does not retroactively reprocess Queue or History items that already failed
  before it ships.
- `GeminiConfigError` (missing API key) remains explicitly out of scope, as already documented
  in TODO.md's Sprint 8.5A Known Limitations.
- Any Learning Blueprint retry-behavior issue discovered during implementation that is
  independent of the stage-identifier/message gap is not fixed as part of this feature; it is
  recorded as a new `TODO.md` Product Backlog item instead (per `LB-01` resolution, Option B).
