<!--
Sync Impact Report
Version change: [TEMPLATE] → 1.0.0 (initial ratification — first concrete fill of the constitution)
Modified principles: N/A (first fill; no prior named principles existed)
Added sections:
  - Core Principles I–VIII (Product, Delivery, Mission, Engineering, Documentation)
  - Section 2: Existing Governance Documents — Responsibility Boundaries
  - Section 3: Spec Kit Scope for YB Learn (Brownfield Adoption)
  - Governance (amendment procedure, versioning policy, compliance review)
Removed sections: None
Deferred / TODO placeholders: None. All template tokens filled.
Source documents consulted: Why.md, CLAUDE.md, docs/00_Project_Management/Development_Workflow_Standard.md,
  TODO.md, Acceptance_Test.md, Knowledge_Structure_Engine_v1.0.md
Templates requiring follow-up review (not modified in this change):
  - .specify/templates/plan-template.md — should reference this constitution's principles when first used
  - .specify/templates/spec-template.md — no constitution-specific placeholders detected
  - .specify/templates/tasks-template.md — no constitution-specific placeholders detected
-->

# YB Learn Constitution

## Core Principles

### I. MVP First, Reduce Friction, Keep It Simple
YB Learn development MUST prioritize the smallest working increment over speculative
completeness. Every feature MUST reduce, not add, friction in the user's learning workflow
(YouTube → Transcript → Study Note → Learning Model). Implementations MUST favor the simplest
design that satisfies the current Sprint's Task — no speculative abstraction, no unused
configurability.
Source: `Why.md` ("降低操作成本，讓收集與學習幾乎沒有摩擦"); `CLAUDE.md` Rules.
Rationale: Confirmed across Sprints 1–8.5A — friction-adding designs (e.g. manual per-item
Transcript/Study Note generation) were identified and removed (Sprint 4.1 Workflow
Stabilization); premature complexity was explicitly rejected (Sprint 7 Task 3 initial version
was retired for not being simpler than existing output).

### II. One Sprint = One Deliverable
Each Sprint MUST ship exactly one coherent, independently testable increment. Within a Sprint,
Tasks MUST be implemented one at a time, followed by STOP and human verification, before the
next Task begins.
Source: `CLAUDE.md` Workflow ("Implement ONE task → STOP"); `Development_Workflow_Standard.md`
§2 (Scope Freeze).
Rationale: Every completed Task recorded in `TODO.md` documents an explicit file-change scope
and a Human Test result before the next Task started. Documented regressions (e.g. Sprint 8
Task 3's event-loop-blocking bug) trace back to violations of this discipline, not to the
discipline itself.

### III. Structure Knowledge, Make It Stick
YB Learn's purpose is not summarization but helping the user build a retrievable Knowledge
Structure (Mental Model) and verifying retention through active recall, not passive reading.
Source: `Why.md` Product Principles ("Structure Knowledge. Make It Stick. Reduce Friction.
Start Learning."); `Knowledge_Structure_Engine_v1.0.md`.
Rationale: This is the frozen product mission (`Why.md`: "Mission 的穩定性... 除非規劃 v2.0，不再
修改"). Any new feature MUST answer: "Does it help the user build a knowledge structure and
retain it?" — if not, it MUST NOT be added to the product.

### IV. Feature First, Refactor Later
New functionality MUST be shipped before cross-cutting refactors are attempted. Shared
abstractions MUST NOT be extracted preemptively — only once a third real caller justifies the
extraction.
Source: `TODO.md` Sprint 7 "Decisions Made" (confirmed 2026-08-05); `Development_Workflow_
Standard.md` §2.
Rationale: Validated across Sprint 7's five independently-shipped Learning Model modules
(Knowledge Outline, Learning Blueprint, Teach Back, Action List, Review), each kept
intentionally uncoupled to reduce regression risk.

### V. RCA Before Fix
Every bug MUST be root-caused before a fix is proposed or implemented. Fixes MUST NOT be
applied on the basis of speculation about the cause.
Source: `Development_Workflow_Standard.md` §7 (Bug Management); operating practice documented
throughout Sprint 8 (Tasks 1, 3, 4).
Rationale: `TODO.md` records multiple cases where an initial guess about root cause was wrong
(e.g. Sprint 8 Task 3's parallel-processing bug was first suspected to be a Single Worker
Queue design constraint, then correctly root-caused as a blocking synchronous Gemini call
inside an `async def` endpoint). Skipping RCA has a documented cost in this project.

### VI. Test First, Human Test Required
No Task is complete without a Human Test performed by the user in the real environment
(browser, real API calls against real data). Automated, mock, or Node-level checks MAY
supplement but MUST NOT substitute for Human Test. `Acceptance_Test.md` MUST NOT be pre-filled
with an assumed PASS.
Source: `Development_Workflow_Standard.md` §5–6 ("Test First → Record Second"); `Acceptance_
Test.md`'s recorded structure (Test Date + Test Result per Sprint).
Rationale: This project has no automated test suite by design; Human Test is the sole
verification gate. `Acceptance_Test.md`'s integrity depends on results being observed, never
predicted.

### VII. Human Review Before Commit, No Automatic Push
Every commit MUST be preceded by an explicit Commit Scope Review — the exact files to be
staged listed and confirmed by the human — before `git add`. `git push` MUST NOT occur
without separate, explicit human confirmation, even after a commit has already been approved.
Source: `Development_Workflow_Standard.md` §9–11 (Commit Scope Review → Git Commit → Git
Push); `CLAUDE.md` Stop Rule.
Rationale: This is the operating pattern already in continuous use for this project's
governance and runtime-output cleanup work — every recent commit was preceded by an explicit
scope confirmation and followed by a status report, never an automatic push.

### VIII. Documentation Discipline
New planning documents MUST NOT be created unless no existing document can hold the content.
Every document keeps a single, named responsibility; when two documents could plausibly hold
the same fact, one MUST be designated authoritative and the other MUST NOT duplicate it.
Source: `CLAUDE.md` Documents ("Do not create new planning documents"); this project's own
governance cleanup history (e.g. `Engineering_Backlog.md` superseded by `TODO.md`'s Product
Backlog after the two diverged).
Rationale: This project has direct, documented cost from undeclared duplicate sources of
truth (root-level doc duplicates found and archived; `Engineering_Backlog.md` vs `TODO.md`
divergence). This principle exists to prevent recurrence.

## Section 2: Existing Governance Documents — Responsibility Boundaries

This Constitution does not supersede the following documents for the responsibilities
assigned to them here. Spec Kit artifacts (this Constitution, future `spec.md` / `plan.md` /
`tasks.md`) MUST reference these documents rather than restate or replace their content:

- **`TODO.md`** — single source of truth for Sprint/Task tracking and the Product Backlog.
- **`Acceptance_Test.md`** — single source of truth for human acceptance test records
  (PASS/FAIL, test dates).
- **`docs/00_Project_Management/Development_Workflow_Standard.md`** — single source of truth
  for the detailed, step-by-step development procedure (Proposal → Scope Freeze →
  Implementation → Self Test → Human Test → Acceptance → Documentation Update → Commit Scope
  Review → Git Commit → Git Push). This Constitution restates only the stable, durable
  principles that Spec Kit's own tooling (`/speckit-plan`, `/speckit-analyze`, etc.) needs to
  check compliance against — it does not duplicate or replace the procedural detail.
- **`Why.md`** — single source of truth for product Mission, Vision, and Product Principles.
- **`Knowledge_Structure_Engine_v1.0.md`** — single source of truth for the Knowledge
  Structure Engine architecture and the frozen three-phase Learning Model design.
- **`CLAUDE.md`** — the concise AI operating entry point. It references `Development_
  Workflow_Standard.md` for procedural detail rather than restating it, and references this
  Constitution for durable principles.

## Section 3: Spec Kit Scope for YB Learn (Brownfield Adoption)

- Spec Kit commands (`/speckit-specify`, `/speckit-plan`, `/speckit-tasks`,
  `/speckit-implement`) apply only to future, not-yet-started work. Sprint 1 through Sprint
  8.5A are already complete, tested, and recorded in `TODO.md` / `Acceptance_Test.md`; they
  MUST NOT be retroactively rewritten as Spec Kit specs.
- No planning documents beyond what Spec Kit's own templates require MUST be created.
  Existing YB Learn documents keep the responsibilities assigned in Section 2.
- Before any future `/speckit-specify` invocation, the target feature MUST be a feature the
  human has explicitly approved for Spec Kit treatment — never silently assumed from Product
  Backlog entries in `TODO.md`.

## Governance

This Constitution supersedes ad hoc practice for any principle it states, but does not
supersede the specific existing documents listed in Section 2 for the responsibilities
assigned to them there.

Amendments require: (1) explicit human approval, (2) a version bump following semantic
versioning — MAJOR for incompatible principle removal or redefinition, MINOR for a new
principle or materially expanded guidance, PATCH for wording or clarification — and (3) a
Sync Impact Report recorded as an HTML comment at the top of this file.

All Spec Kit-driven work (`/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`) MUST verify
compliance with these principles. Any complexity or deviation MUST be explicitly justified in
the relevant `plan.md`. This Constitution itself is subject to Principle VII: no amendment is
committed without the same Human Review and Commit Scope Review gate as any other change.

**Version**: 1.0.0 | **Ratified**: 2026-08-08 | **Last Amended**: 2026-08-08
