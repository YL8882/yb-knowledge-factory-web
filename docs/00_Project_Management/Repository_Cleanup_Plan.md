---
Version: v1.0
Status: Draft — Awaiting Approval
Owner: Claude Code
Document: Repository Cleanup Plan
Category: Project Management
Purpose: Propose official-version recommendations, archive plan, removal candidates, and Product_Index/cross-reference updates for the final pre-Sprint-1 repository cleanup. Nothing in this plan has been executed.
Scope: YB Knowledge Factory MVP v0.1
Priority: Critical
Last Updated: 2026-07-30
Related Documents:
  - Repository_Discovery_Report.md
  - Engineering_Understanding_Report.md
---

# Repository Cleanup Plan

> No files have been moved, archived, edited, or deleted while producing this plan. All recommendations below require your approval before Task 2–5 execution begins.

---

# Task 1 — Official Version Recommendations

I read the full content of every duplicated pair/set below before recommending (not just file sizes). Two distinct situations turned up, which changes the reasoning:

- **Generic template artifacts** — some root-level `docs/*.md` files turned out not to be alternate drafts of this project's documents at all. Their own front matter says `Scope: All AI Products`, `Author: ChatGPT`, and their content describes a generic AI-Product-Factory template product (Next.js/Tailwind stack recommendations, `Dashboard`/`History`/`Settings`/`About` screens that don't exist in this MVP, a generic `prompts/` folder layout that doesn't match `docs/02_Prompt_Design/`). These read the same way as the stray `CHANGELOG.md.md` — leftovers from scaffolding this repo off a template, not project content.
- **Genuine project-specific duplicates** — other root-level files are clearly about YB Knowledge Factory (mention YouTube, Transcript, Study Note, `Development_Operating_System.md`) but are shorter/earlier drafts of the same document that exists in more detail elsewhere.

## Recommendation Table

| File Name | Existing Versions | Differences | Most Complete Version | Reason | Confidence |
|---|---|---|---|---|---|
| **PRD** | `docs/PRD.md` (235 lines) vs `docs/01_Product_Requirements/Core/PRD.md` (332 lines) | Both are YB-specific. Root version has 10 short sections, no FR-numbering. Core version adds numbered Functional Requirements (FR-001–005), explicit Non-functional Requirements, a detailed Out-of-Scope list, Success Criteria, MVP Development Strategy, and a versioned Future Roadmap (v0.2/v0.3/v1.0). | `docs/01_Product_Requirements/Core/PRD.md` | Strictly more complete; it's also the copy `Product_Index.md` already points to and the copy every other Core-tier "Final" doc (Technical_Decision, Runtime/Output Spec) cross-references. | **High** |
| **Product_Architecture** | `docs/Product_Architecture.md` (484 lines, v3.0, `Scope: All AI Products`) vs `docs/01_Product_Requirements/Core/Product_Architecture.md` (192 lines, v1.0) | Root version is generic template content (Capability Map, generic Tech Stack table recommending Next.js/Tailwind/PostgreSQL, no mention of YouTube/Transcript/Study Note anywhere). Core version describes YB's actual modules (Transcript, Study Note, Knowledge Card) and actual data flow. | `docs/01_Product_Requirements/Core/Product_Architecture.md` | Root copy is not a draft of *this* product's architecture — it's the template's generic architecture doc. Not a "which is more complete" question; the root one isn't about this product. | **High** |
| **Prompt_Specification** | `docs/Prompt_Specification.md` (495 lines, v2.0, `Scope: All AI Products`) vs `docs/02_Prompt_Design/Prompt_Specification.md` (403 lines, v1.0) | Root version is generic (4-layer Prompt Architecture, generic `prompts/` folder standard, no reference to StudyNote anything). `02_Prompt_Design` version has a concrete Prompt Catalog naming the actual `StudyNote_Prompt_v1.0` and describes this product's real input/output. | `docs/02_Prompt_Design/Prompt_Specification.md` | Same situation as Product_Architecture — root is template content, not a draft of this project's prompt spec. | **High** |
| **Workflow Specification** | `docs/Workflow Specification.md` (270 lines, root, note the space in the filename) vs `docs/01_Product_Requirements/Core/Workflow_Specification.md` (81 lines) vs `docs/03_Workflows/Workflow_Specification.md` (445 lines) | Root version is YB-specific but shorter, and references a `runtime/transcripts/` / `runtime/study_notes/` folder convention that doesn't match the actual code (`app/transcript.py`, `app/study_note.py` write to `outputs/transcripts/` and `outputs/study_notes/`). Core version is a deliberately abstract 7-stage overview ("This document describes what happens, not how it is implemented" — stated explicitly). `03_Workflows` version is a detailed 9-step walkthrough with exact inputs/outputs per step, exception handling, and acceptance criteria — this is the one that actually matches the real pipeline. | `docs/03_Workflows/Workflow_Specification.md` for engineering detail. | Root copy is the weakest (wrong folder convention, least detail) — clear archive candidate. Core vs `03_Workflows` looks like an **intentional two-tier split** (abstract product contract vs detailed engineering spec), consistent with how `Product_Architecture.md`, `Runtime_Specification.md`, and `Output_Specification.md` all explicitly say "implementation details intentionally excluded." I don't recommend archiving the Core version — only clarifying, in Product_Index, that `03_Workflows/Workflow_Specification.md` is the one to read for actual step-by-step behavior. | **High** (root is obsolete) / **Medium** (Core vs `03_Workflows` being intentionally layered rather than duplicated) |
| **Wireframe Specification** | `docs/Wireframe_Specification.md` (465 lines, root, v2.0, `Scope: All AI Products`) vs `docs/01_Product_Requirements/UI/Wireframe_Specification.md` (190 lines, v1.0) vs `docs/05_UI_UX/Wireframe_Specification.md` (415 lines, v3.0, Final) | Root version is generic template content (`Dashboard`/`History`/`Settings`/`About` screens, generic `WF_01_Home.md`-style naming standard — none of this matches the actual single-page app). `01_Product_Requirements/UI` version is YB-specific but abstract (Home/Processing/Result, no visual layout, explicitly excludes "visual design"). `05_UI_UX` version is YB-specific **and** detailed — actual ASCII wireframe layouts for Home/Processing/Result matching the real single-page app, and sits alongside the real PNG screenshots/diagrams in the same folder. | `docs/05_UI_UX/Wireframe_Specification.md` for actual UI reference. | Root copy is template noise, same reasoning as Product_Architecture/Prompt_Specification above. `01_Product_Requirements/UI` vs `05_UI_UX` again looks like the same intentional abstract-vs-detailed split as Workflow Specification — recommend keeping both, but pointing Product_Index at `05_UI_UX` as the practical reference since it's the one with real layout content and design assets. | **High** (root) / **Medium** (UI/ vs 05_UI_UX/ being intentionally layered) |
| **Principle Zero** *(other duplicated documentation)* | `docs/01_Product_Requirements/Principle Zero.md` (short standalone) vs the "Principle Zero" section inside `docs/01_Product_Requirements/Product_Principles_v4.0.md` (Final, framed as "The Constitution of YB Knowledge Factory") | Standalone file's opening lines ("Knowledge is the Product... Knowledge is the product... Everything else exists to create, preserve, and reuse knowledge.") are reproduced near-verbatim as the opening section of the v4.0 constitution document, which then goes on to build a full principle set around it. | `docs/01_Product_Requirements/Product_Principles_v4.0.md` | The v4.0 doc supersedes the standalone note; it's explicitly versioned as the authoritative constitution and contains everything the standalone file has plus more. | **High** |

## Explicitly Not Recommending Silent Merges

Per your instruction, I have not decided anything — the table above is a recommendation for you to approve or override, especially the two "Medium" confidence rows, where "duplicate" may really mean "intentionally layered abstract + detailed spec" rather than "one is wrong."

---

# Archive Plan (pending approval)

If the recommendations above are approved, these files would move to `Archive/` (original filenames preserved, per your instruction — nothing renamed):

| File | Reason | Confidence |
|---|---|---|
| `docs/PRD.md` | Superseded by `docs/01_Product_Requirements/Core/PRD.md` | High |
| `docs/Product_Architecture.md` | Generic template artifact, not project content | High |
| `docs/Prompt_Specification.md` | Generic template artifact, not project content | High |
| `docs/Workflow Specification.md` | Superseded by `docs/03_Workflows/Workflow_Specification.md`; references a stale `runtime/` folder convention | High |
| `docs/Wireframe_Specification.md` | Generic template artifact, not project content | High |
| `docs/01_Product_Requirements/Principle Zero.md` | Superseded by `docs/01_Product_Requirements/Product_Principles_v4.0.md` | High |

**Flagged but not recommended for action without your explicit confirmation** (out of the "duplicated documentation" scope you named, so I'm surfacing rather than deciding):

- `docs/06_Google_AI_Studio/` (9 documents) — all scoped to the Prototype stage, which `Milestone_01_Prototype_Freeze/Prototype_Handover.md` already declares "✅ Completed." These aren't duplicates of anything; they're a closed project phase's working documents. Archiving them would be consistent with Task 4's stated purpose ("move superseded documents into Archive/"), but since you didn't name this set explicitly, I'm asking rather than including it in the plan by default.
- Five empty directories (`docs/02_Prompt_Design/04_Examples/Example_02_LongTranscript/` through `Example_05_Podcast/`, and `docs/02_Prompt_Design/05_Prompt_Testing/`) — nothing to archive (no files inside), and removing empty directories isn't really "removing an obsolete file." Recommend leaving as-is; noting only for completeness.

---

# Removal Candidates (Task 5 — pending approval)

Only one file clearly satisfies all four of your criteria (unrelated to this project, template leftover, confirmed obsolete, not referenced anywhere as *this project's* changelog):

| File | Why it qualifies |
|---|---|
| `CHANGELOG.md.md` (repo root) | Front matter: `Owner: AI Product Factory`, `Category: Product Template`, "Version history for AI Product Factory Template." Not this project's changelog (that's `docs/00_Project_Management/CHANGELOG.md`, which is what `Project_Dashboard.md` and `Milestone_00_Project_Freeze.md` actually reference). The double `.md.md` extension is itself evidence of an unintentional copy artifact. |

No other file met all four criteria with enough certainty — everything else in the Archive Plan above is superseded-but-historically-relevant, not "unrelated to the project," so it goes to `Archive/` rather than removal, per your Task 4/5 distinction.

---

# Task 2 (Draft) — Proposed Product_Index.md Updates

Pending approval, these are the specific changes I'd make to `docs/01_Product_Requirements/Core/Product_Index.md`'s "Product Specifications" and "Related Documents" tables — today they list bare filenames with no folder path, which is exactly what makes them ambiguous against the duplicates above:

| Current entry | Proposed entry | Reason |
|---|---|---|
| `PRD.md` | `01_Product_Requirements/Core/PRD.md` | Disambiguate from the (to-be-archived) root copy |
| `Product_Architecture.md` | `01_Product_Requirements/Core/Product_Architecture.md` | Same |
| `Workflow_Specification.md` | `03_Workflows/Workflow_Specification.md` (detailed) — with a note that `01_Product_Requirements/Core/Workflow_Specification.md` is the abstract product-level version | Surfaces the detailed version that Product_Index currently doesn't mention at all |
| `Prompt_Specification.md` | `02_Prompt_Design/Prompt_Specification.md` | Disambiguate from root copy |
| `Wireframe_Specification.md` | `05_UI_UX/Wireframe_Specification.md` (detailed, with real layouts) — with a note that `01_Product_Requirements/UI/Wireframe_Specification.md` is the abstract version | Same reasoning as Workflow Specification |
| `Documentation_Standard.md` (listed under Project Management related docs) | **Remove this row** | File does not exist anywhere in the repository (confirmed in Repository_Discovery_Report.md §5); listing it as a related document is a broken reference |

I would **not** add any new rows, sections, or a new "how to read this index" methodology — only correct existing rows to point at real, unambiguous files, per your "do not introduce new documentation standards" instruction.

---

# Task 3 (Draft) — Proposed Cross-Reference Fixes

These "Related Documents" / "References" mentions point at filenames that don't exist verbatim on disk (confirmed in Repository_Discovery_Report.md §5). Proposed fix is a straight rename-to-match-actual-filename in the referencing text, nothing else:

| Referencing Document | Broken Reference | Proposed Fix |
|---|---|---|
| `docs/01_Product_Requirements/UI/Application Architecture Blueprint.md` §14 | `Wireframe_Specification_v2.0.md` | `Wireframe_Specification.md` (and clarify which folder, per Task 2 table above) |
| `docs/01_Product_Requirements/UI/Application Architecture Blueprint.md` §14 | `UI_Design_Pack_v1.0` | `UI_Design_Pack.md` |
| `docs/03_Workflows/MVP_Single_Page_Workflow.md` §12 | `Application_Architecture_Blueprint_v2.0.md` | `Application Architecture Blueprint.md` |
| `docs/03_Workflows/MVP_Single_Page_Workflow.md` §12 | `Wireframe_Specification_v2.0.md` | `Wireframe_Specification.md` (folder per Task 2) |
| `docs/03_Workflows/MVP_Single_Page_Workflow.md` §12 | `UI_Design_Pack_v1.0` | `UI_Design_Pack.md` |
| `docs/03_Workflows/MVP_Single_Page_Workflow.md` §12 | `Google_AI_Studio_Build_Specification_v2.0.md` | `Google_AI_Studio_Build_Specification.md` |
| `docs/01_Product_Requirements/Core/Product_Architecture.md` §11 | `Documentation_Standard.md`, `Implementation_Guide.md` | Neither exists anywhere — proposed fix is to **remove these two lines** rather than invent replacement files (no new documents, per Out of Scope) |
| `docs/01_Product_Requirements/Core/Product_Index.md` (Related Documents, Project Management section) | `Documentation_Standard.md` | Remove the line (same reasoning) |

I have not changed any of these yet. This table is the complete list of every broken reference found during discovery — no others were found beyond what's listed here and in Repository_Discovery_Report.md §5.

---

# Success Criteria Check (once approved and executed)

- One Topic = One Official Document → achieved for PRD/Product_Architecture/Prompt_Specification (root copies were template noise, not real alternatives); Workflow/Wireframe keep two intentionally-layered documents each (abstract + detailed), both retained and both correctly pointed to.
- No duplicated *active* documentation → root template artifacts and superseded drafts move to `Archive/`.
- No broken Markdown references → all 8 broken references above get fixed or removed.
- Product_Index fully accurate → 6 row corrections proposed above.
- Historical documents preserved in `Archive/` → nothing deleted except the one confirmed-template file.
- Repository ready for Sprint 1 → contingent on your approval of the above; no code touched at any point in this cleanup.

---

# Stop Condition

This is a plan only. Nothing has been moved, archived, edited, or deleted. Waiting for your approval — in particular on:

1. The two Medium-confidence rows (Workflow Specification, Wireframe Specification) — do you want both tiers kept as I recommend, or a different resolution?
2. Whether to include `docs/06_Google_AI_Studio/` in the archive batch.
3. Sign-off to proceed with Tasks 2–5 as drafted above.
