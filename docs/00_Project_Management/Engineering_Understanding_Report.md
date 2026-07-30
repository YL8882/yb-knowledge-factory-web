---
Version: v1.0
Status: Draft
Owner: Claude Code
Document: Engineering Understanding Report
Category: Project Management
Purpose: Record engineering onboarding understanding of YB Knowledge Factory MVP before Sprint 1 development.
Scope: YB Knowledge Factory MVP v0.1
Priority: High
Last Updated: 2026-07-30
Related Documents:
  - Product_Index.md
  - PRD.md
  - Product_Architecture.md
  - Workflow_Specification.md
  - Technical_Decision.md
  - Project_Dashboard.md
  - MVP_Test_Report.md
---

# Engineering Understanding Report

> Pre-Sprint 1 onboarding report. No production code was written or modified while producing this report.

---

# 0. Note on Reading Order

The kickoff instructions asked me to read, in order: `Documentation_Standard.md`, `CLAUDE.md`, `README.md`, `Product_Blueprint.md`, `PRD.md`, `Product_Architecture.md`, `AI_Pipeline_Architecture.md`, `Runtime_Specification.md`, `Workflow_Specification.md`, `Output_Specification.md`, `Wireframe_Specification.md`, `UI_Component_Specification.md`, `Repository_Governance.md`.

I searched the entire repository and **four of those files do not exist anywhere**: `Documentation_Standard.md`, `Product_Blueprint.md`, `AI_Pipeline_Architecture.md`, `Repository_Governance.md`. A stray `CHANGELOG.md.md` at the repo root (front matter: `Owner: AI Product Factory`, `Category: Product Template`) suggests this repo was bootstrapped from a generic "AI Product Factory" template, and the kickoff prompt is that template's generic onboarding script — not one written specifically for this repo's current file layout. I read every document from the list that does exist, plus the documents those files themselves point to (PRD, Product Architecture, Technical Decision, Runtime/Output/Workflow/Prompt/UI specs, Queue System Design, Application Architecture Blueprint, Milestone docs, `CLAUDE.md`, `README.md`, and the full `app/` source), rather than stop at the first missing file. Details in §5.

---

# 1. Project Understanding

**Product:** YB Knowledge Factory MVP v0.1 — a web tool that turns a YB YouTube teaching video into two durable Markdown knowledge assets in one pass.

**Core loop (per PRD.md / Workflow_Specification.md):**

```text
Paste YouTube URL → Queue → Download Audio → Transcript (Faster Whisper)
→ Study Note (Gemini 2.5 Flash) → Download Transcript.md + Study_Note.md
```

**Why it exists:** YB's teaching videos run 20–60 minutes; manually re-watching and note-taking is slow and lossy. The product's success definition (PRD §13) is narrow and concrete: one YouTube URL in, `Transcript.md` + `Study_Note.md` out, no manual cleanup required.

**Explicit MVP boundaries (PRD §9 / Technical_Decision.md §8):** no login, no database, no cloud sync, no Knowledge Card / SOP / Prompt Library / RAG / AI Chat / multi-user. These are deferred to v0.2+.

**Chosen stack (Technical_Decision.md, Final):** Python + FastAPI backend, Gemini 2.5 Flash for Study Note generation, yt-dlp for audio download, Faster Whisper for transcription, OpenCC (s2t) for Simplified→Traditional Chinese normalization, Markdown as the only output format, no DB, Windows localhost deployment for MVP.

**Actual current status (this is not a greenfield kickoff):** the MVP is already built and functionally tested. `git log` shows the build was completed and released (`Release MVP v0.1`, `feat: add transcript generation with faster-whisper`, `feat: add YouTube queue and metadata retrieval`), and `docs/MVP_Test_Report.md` records a PASS across the full workflow, download endpoints, and five error scenarios. Earlier today the Study Note section-naming question was resolved (decision recorded in `CHANGELOG.md` under "MVP v0.1 — Documentation Sync") and `app/TODO.md`, `Engineering_Backlog.md`, `Acceptance_Test.md`, and `Project_Dashboard.md` were updated to reflect that Milestone 02 (Build MVP) is functionally complete, pending your final Product Owner sign-off. I am treating this report as a checkpoint on top of that existing state, not as day-one discovery.

---

# 2. Repository Understanding

## 2.1 Layout

```text
app/                    FastAPI application (the only code in the repo)
  main.py               Routes: queue CRUD, transcript, study-note, downloads
  youtube.py            URL validation + yt-dlp metadata fetch
  queue_store.py        In-memory queue (add/list/remove/duplicate/100-item cap)
  transcript.py         yt-dlp audio download + faster-whisper transcription
  gemini_client.py       Gemini 2.5 Flash call + system instruction (Study Note prompt, inlined in Python, not loaded from docs/)
  study_note.py         Metadata block assembly + file save
  templates/, static/   Single-page HTML/CSS/JS frontend
outputs/                Generated transcripts/ and study_notes/ (persisted; queue itself is not)
docs/
  00_Project_Management/  Dev Ops constitution, Dashboard, CHANGELOG, Stage Gate
  01_Product_Requirements/Core   PRD, Product_Architecture, Runtime/Output/Workflow_Specification, Technical_Decision, Product_Index
  01_Product_Requirements/UI     UI_Component_Specification, Wireframe_Specification, Application Architecture Blueprint
  01_Product_Requirements/Integrations  Browser_Extension_PRD, Quick_Capture_Architecture (future scope)
  02_Prompt_Design/        Prompt_Specification, AI Role / System Instructions / Task Prompt / Output Schema chain for Study Note
  03_Workflows/            Workflow_Specification (detailed), Queue_System_Design, MVP_Single_Page_Workflow
  04_Templates/            StudyNote_Template_v3.0.md — declared Single Source of Truth for Study Note structure
  05_UI_UX/                Wireframes and design pack (images + doc)
  06_Google_AI_Studio/     Prototype build prompts (historical, prototype stage only)
  99_Milestone/            Milestone_00 (Project Freeze) → 01 (Prototype Freeze) → 02 (Build MVP), each with its own backlog/acceptance doc
```

## 2.2 Governance model (`Development_Operating_System.md`, referenced by the old `CLAUDE.md` and still the operative process even though `CLAUDE.md` itself was just simplified to v2.0)

- One Milestone at a time; a Milestone is "done" only after Spec → Code → Test → Review → Commit → Docs Updated.
- Single Source of Truth per topic — but see §4.1, this rule is currently violated in two places.
- Frozen decisions require a new version to change, not a silent edit.
- Reference documents instead of re-pasting them; review only diffs.

`CLAUDE.md` was rewritten today (external edit, not by me) into a leaner v2.0. It keeps the essential rules relevant here: no product decisions without confirmation, keep `README.md` / `TODO.md` / `Acceptance_Test.md` / `Engineering_Backlog.md` / `Project_Dashboard.md` in sync whenever implementation changes, summarize before committing, never push automatically, and when uncertain — explain options, recommend, wait.

## 2.3 What the code actually does today (verified by reading `app/`, not just docs)

- Queue is in-memory only (`queue_store.py`) — cleared on server restart. This matches Technical_Decision.md's "no Database" call, but is narrower than `Queue_System_Design.md`, which describes `queue.json` persistence and even multi-device cloud sync behind login — see §4.1.
- Transcript and Study Note generation are **manual, per-item button clicks** in the UI (`static/script.js`), not an automatic single-pipeline run after one "Generate" click — see §4.1 for the spec conflict this creates.
- Study Note output structure (`gemini_client.py` system instruction, verified against a real generated file in `outputs/study_notes/`) is: Metadata block (Title/Source/Author/Date/Language/Tags/Version) + `Executive Summary / Key Takeaways / Detailed Notes / Core Concepts / Workflow / Tools / Best Practices / Key Decisions / Future Research / References`. This was reconciled today with `StudyNote_Template_v3.0.md` and `StudyNote_Output_Schema_v1.0.md` — but not with three other "Final" documents that still describe the old 5-section Chinese structure. See §4.1.
- No OpenCC step anywhere in `app/` or `requirements.txt`, despite three Final specs requiring it. See §4.1.
- No logging module in the codebase (confirmed via grep) — `Engineering_Backlog.md` P1 "Logging" is correctly still unchecked.

---

# 3. Development Plan

Given the MVP is already built, tested, and functionally accepted (pending your sign-off), I'm not proposing a Sprint 1 "build from scratch" plan. Instead, two possible next steps depend entirely on decisions only you can make (§6):

**Path A — Close the spec/implementation gaps found in §4.1 first.** Before any new feature work, reconcile PRD.md / Workflow_Specification.md (Core) / Prompt_Specification.md against the actual Study Note structure and the OpenCC gap, since these are "Frozen/Final" governance documents and currently contradict both the code and the docs I updated this morning. This is pure documentation + a small, contained code decision (add OpenCC or formally drop it), no new features.

**Path B — Start Milestone 03 (per the just-corrected Project_Dashboard.md numbering: Improve UI/UX) once you sign off Milestone 02**, deferring the doc reconciliation in §4.1 to a tracked backlog item instead of blocking on it.

I recommend Path A first, narrowly scoped (just the specific contradictions listed below), because shipping new UI/UX work on top of governance docs that describe a different Study Note schema and a missing Chinese-conversion step will make the drift worse and harder to unwind later. But this is a recommendation, not something I've started — no docs beyond this report have been touched.

---

# 4. Risks

## 4.1 Specification contradictions (highest priority — these are all "Status: Final" documents disagreeing with each other and/or with the code)

| Topic | Says one thing | Says another thing | Actual code |
|---|---|---|---|
| Study Note structure | `PRD.md` (Core), `Workflow_Specification.md` (Core, 81 lines), `Prompt_Specification.md` (02_Prompt_Design root) — all specify 5 Chinese sections: 一句話摘要／重點摘要／重點解析／操作流程／延伸資訊 | `StudyNote_Template_v3.0.md` + `StudyNote_Output_Schema_v1.0.md` (updated this morning) — 9 English sections + Metadata block | Matches the *second* column exactly |
| Traditional Chinese conversion | `Technical_Decision.md` and `docs/03_Workflows/Workflow_Specification.md` (445-line version) both mandate an explicit OpenCC (s2t) step | — | Not implemented at all; not in `requirements.txt`, not imported anywhere. Spot-checked two real Chinese transcripts in `outputs/transcripts/` — both happen to already be Traditional Chinese (Faster Whisper's raw output), but there is no code-level guarantee of this for all inputs/models |
| Auto-pipeline vs manual steps | `Application Architecture Blueprint.md` (v2.0, Final) and `docs/03_Workflows/MVP_Single_Page_Workflow.md` (v1.0, Final) both specify "One Click Generate" / "Auto Pipeline" — one Generate click runs Audio→Transcript→Study Note automatically | — | UI requires a separate manual click per queue item for "產生 Transcript" and then again for "產生 Study Note" (already logged as a known, accepted MVP simplification in `MVP_Test_Report.md`'s backlog, so this one is a known deviation, not a fresh surprise) |
| Queue scope | `Queue_System_Design.md` (Final) describes `queue.json` persistence and cloud sync across devices behind login | `PRD.md` §9 explicitly excludes Login, Database, and Cloud Sync from MVP | In-memory queue only, no persistence, no login — matches PRD, contradicts Queue_System_Design.md |

None of these are things I should silently resolve — per both the old and new `CLAUDE.md`, product decisions need your confirmation, and the Dev Ops doc treats "Final" status as frozen (not to be reopened without a version bump). I flagged the Study Note naming question this morning and got a decision, but only updated the two prompt-layer docs (`Template`, `Output Schema`) — I did not touch the three higher-level "Final" docs that still describe the old schema, because that would have gone beyond what was asked at the time. That gap is now open again in a different form: which of `PRD.md` / `Workflow_Specification.md` / `Prompt_Specification.md` also need a version bump to match this morning's decision.

## 4.2 Documentation duplication (Single-Source-of-Truth violation, per the Dev Ops doc's own rule)

`docs/` has a flat root layer that duplicates several canonical sub-folder documents, with genuinely different content (not just copies) — e.g. `docs/PRD.md` (235 lines) vs `docs/01_Product_Requirements/Core/PRD.md` (332 lines); `docs/Workflow Specification.md` (270 lines, note the space in the filename) vs two other Workflow_Specification.md files (81 and 445 lines) in different folders; similarly for `Product_Architecture.md`, `Wireframe_Specification.md`, and `Prompt_Specification.md`. It's not obvious from the files themselves which is authoritative for a newcomer — I inferred it from `Product_Index.md`'s reading order, which points at the `01_Product_Requirements/Core` and `01_Product_Requirements/UI` copies. I have not touched or deleted any of these, per your instruction not to modify documentation unless told to.

## 4.3 Minor

- Root-level `CHANGELOG.md.md` looks like an unintended leftover from the AI Product Factory template scaffold, separate from the project's real `docs/00_Project_Management/CHANGELOG.md`.
- `Project_Dashboard.md`'s "Next Milestones" table used to number-collide with the `99_Milestone/` folder scheme (Milestone 00/01/02 already used on disk); this was corrected earlier today, flagging here only so the fix is visible to you.

---

# 5. Missing Information

- `Documentation_Standard.md`, `Product_Blueprint.md`, `AI_Pipeline_Architecture.md`, `Repository_Governance.md` — referenced by the kickoff prompt and, in the first case, also referenced from inside `Development_Operating_System.md`'s own front matter and `Product_Architecture.md`'s References section — but none exist in the repository. I cannot summarize documents that aren't there; I'd need to know whether they (a) were never written, (b) exist in the original AI Product Factory template repo and should be copied in, or (c) are already superseded by content that lives elsewhere under a different name.
- No stated deadline or urgency for Milestone 03 / next steps — the Dashboard's "Priorities" section is generic ("complete MVP core features") and doesn't indicate what happens after final sign-off.

---

# 6. Questions

1. **Study Note schema reconciliation (§4.1, row 1):** Should I version-bump `PRD.md`, the two `Workflow_Specification.md` files, and `Prompt_Specification.md` to match the 9-section English structure now recorded in `StudyNote_Template_v3.0.md`, or was this morning's decision meant to apply narrowly to the prompt/template layer only, leaving the product-level docs describing an aspirational/older schema on purpose?
2. **OpenCC (§4.1, row 2):** Is the missing Simplified→Traditional conversion step an acceptable, intentional MVP simplification (since Faster Whisper's raw output has been Traditional in the samples I checked), or should it be implemented to match `Technical_Decision.md` and the Workflow Specification, or should those two Final documents instead be amended to drop the OpenCC requirement?
3. **Doc duplication (§4.2):** Can I delete or archive the stale root-level `docs/*.md` duplicates (and the stray `CHANGELOG.md.md`) once you confirm the sub-folder versions are authoritative? I have not touched any of them yet since you said not to modify documentation unless instructed.
4. **Missing template docs (§5):** Do `Documentation_Standard.md` / `Product_Blueprint.md` / `AI_Pipeline_Architecture.md` / `Repository_Governance.md` need to be created, or should the kickoff reading list be treated as outdated for this repo?
5. **Next step:** Given Milestone 02 is functionally complete pending your sign-off, do you want me to wait for that sign-off before any further action, or proceed straight into scoping Milestone 03 (Improve UI/UX) in parallel with your review?

---

# Stop Condition

No production code was written. No files were modified. This report is the only new document created, as instructed. Waiting for your review before Sprint 1 / next Milestone work begins.
