---
Version: v1.0
Status: Draft
Owner: Claude Code
Document: Repository Discovery Report
Category: Project Management
Purpose: Full repository inventory (structure, duplicates, obsolete candidates, broken references) prior to any documentation reading or planning.
Scope: YB Knowledge Factory MVP v0.1 (entire repository)
Priority: High
Last Updated: 2026-07-30
---

# Repository Discovery Report

> Produced from a full scan of the actual repository on disk. No files were modified or deleted while producing this report. Where a document's existence is asserted below, it was verified with `find`/`Glob`, not assumed from another document's references.

---

# 1. Folder Structure

```text
.
├── .claude/                          settings.local.json
├── app/                               FastAPI application (only code in repo)
│   ├── static/                        script.js, style.css
│   └── templates/                     index.html
├── docs/
│   ├── 00_Project_Management/         Dev Ops constitution, Dashboard, CHANGELOG, Stage Gate Checklist
│   ├── 01_Product_Requirements/
│   │   ├── Core/                      PRD, Product_Architecture, Runtime/Output/Workflow_Specification, Technical_Decision, Product_Index
│   │   ├── Diagrams/                  5 PNGs
│   │   ├── Integrations/              Browser_Extension_PRD, Quick_Capture_Architecture (future scope, not MVP)
│   │   ├── UI/                        UI_Component_Specification, Wireframe_Specification (v1.0), Application Architecture Blueprint
│   │   ├── Principle Zero.md          (loose file, not in a subfolder)
│   │   ├── Product_Principles_v4.0.md (loose file, not in a subfolder)
│   │   └── desktop.ini
│   ├── 02_Prompt_Design/
│   │   ├── 00_AI_Roles/ 01_System_Prompts/ 02_Task_Prompts/ 03_Output_Schema/   StudyNote prompt chain
│   │   ├── 04_Examples/
│   │   │   ├── Example_01_StudyNote/  4 files (populated)
│   │   │   ├── Example_02_LongTranscript/    EMPTY
│   │   │   ├── Example_03_MixedLanguage/     EMPTY
│   │   │   ├── Example_04_PoorTranscript/    EMPTY
│   │   │   ├── Example_05_Podcast/           EMPTY
│   │   │   └── README.md
│   │   ├── 05_Prompt_Testing/          EMPTY
│   │   ├── Prompt_Architecture.md, Prompt_Engineering_Standard_v1.0.md, Prompt_Specification.md, Prompt_Test_Plan.md, README.md
│   ├── 03_Workflows/                  Workflow_Specification (445 lines), Queue_System_Design, MVP_Single_Page_Workflow
│   ├── 04_Templates/                  StudyNote_Template_v3.0.md, Transcript_Template_v2.0.md
│   ├── 05_UI_UX/                      UI_Design_Pack.md, Wireframe_Specification.md (v3.0!), diagrams + screenshots (PNG)
│   ├── 06_Google_AI_Studio/           9 prototype build/prompt docs + 2 PNGs (prototype-stage, pre-dates Claude Code build)
│   ├── 99_Milestone/
│   │   ├── Milestone_00_Project_Freeze.md
│   │   ├── Milestone_01_Prototype_Freeze/    00_README, Engineering_Backlog, Engineering_Kickoff, Prototype_Handover, 2 screenshots
│   │   └── Milestone_02_Build_MVP/           Acceptance_Test.md
│   ├── MVP_Test_Report.md             (loose file, docs/ root)
│   ├── PRD.md                         (loose file, docs/ root — duplicate, see §3)
│   ├── Product_Architecture.md        (loose file, docs/ root — duplicate, see §3)
│   ├── Prompt_Specification.md        (loose file, docs/ root — duplicate, see §3)
│   ├── Wireframe_Specification.md     (loose file, docs/ root — duplicate, see §3)
│   └── Workflow Specification.md      (loose file, docs/ root, note the space in the filename — duplicate, see §3)
├── outputs/
│   ├── study_notes/                   1 generated file
│   └── transcripts/                   3 generated files
├── CHANGELOG.md.md                    stray root file, see §4
├── CLAUDE.md                          rewritten to v2.0 today (external edit)
├── README.md
├── requirements.txt
└── run.py
```

71 Markdown files total; 18,812 lines total across them.

---

# 2. Existing Markdown Documents

Full inventory with line counts (grouped by area):

**Project Management (5):** `Development_Operating_System.md` (651), `Project_Dashboard.md` (220), `Stage_Gate_Checklist.md` (260), `CHANGELOG.md` (276), plus this report and `Engineering_Understanding_Report.md` (both created today).

**Product Requirements — Core (7):** `PRD.md` (332), `Product_Architecture.md` (192), `Product_Index.md` (279), `Runtime_Specification.md` (140), `Output_Specification.md` (125), `Workflow_Specification.md` (81), `Technical_Decision.md` (392).

**Product Requirements — loose / UI / Integrations (6):** `Principle Zero.md`, `Product_Principles_v4.0.md`, `UI_Component_Specification.md` (170), `Wireframe_Specification.md` (190), `Application Architecture Blueprint.md`, `Browser_Extension_PRD.md` (447, future scope), `Quick_Capture_Architecture.md` (569, future scope).

**Prompt Design (14 + 4 empty example folders):** `README.md`, `Prompt_Architecture.md` (497), `Prompt_Engineering_Standard_v1.0.md` (384), `Prompt_Specification.md` (403), `Prompt_Test_Plan.md` (324), the AI Role/System Instructions/Task Prompt/Output Schema chain (4 files), and `04_Examples/Example_01_StudyNote/` (4 files) + its `README.md`.

**Workflows (3):** `MVP_Single_Page_Workflow.md` (376), `Queue_System_Design.md` (624), `Workflow_Specification.md` (445).

**Templates (2):** `StudyNote_Template_v3.0.md` (updated today), `Transcript_Template_v2.0.md` (11 — very short).

**UI/UX (2 + images):** `UI_Design_Pack.md` (475), `Wireframe_Specification.md` (415, versioned v3.0 — a *third*, more detailed, more recent copy).

**Google AI Studio prototype docs (9):** build spec, playbook, 6 numbered prompt docs, design reviewer, prototype test checklist — all dated to the prototype phase.

**Milestones (5):** `Milestone_00_Project_Freeze.md`, `Milestone_01_Prototype_Freeze/` (4 docs), `Milestone_02_Build_MVP/Acceptance_Test.md`.

**Loose docs/ root (6):** `MVP_Test_Report.md`, plus 5 duplicates covered in §3.

**Root-level (3):** `CLAUDE.md`, `README.md`, `CHANGELOG.md.md` (stray, see §4).

**App (1):** `app/TODO.md`.

---

# 3. Duplicate Documents

These are not simple copies — each pair/set has **different line counts and genuinely different content**, meaning they diverged over time rather than being accidental exact copies:

| Logical Document | Copies Found | Notes |
|---|---|---|
| PRD | `docs/PRD.md` (235 lines) **vs** `docs/01_Product_Requirements/Core/PRD.md` (332 lines) | `Product_Index.md`'s reading order points at the `Core/` copy — treat it as canonical |
| Product Architecture | `docs/Product_Architecture.md` (484 lines) **vs** `docs/01_Product_Requirements/Core/Product_Architecture.md` (192 lines) | Same — `Core/` copy is what `Product_Index.md` and `Development_Operating_System.md` point to |
| Prompt Specification | `docs/Prompt_Specification.md` (495 lines) **vs** `docs/02_Prompt_Design/Prompt_Specification.md` (403 lines) | `Core/`-equivalent (`02_Prompt_Design/`) copy referenced by Product_Index |
| Wireframe Specification | **three** copies: `docs/Wireframe_Specification.md` (465 lines) / `docs/01_Product_Requirements/UI/Wireframe_Specification.md` (190 lines, v1.0) / `docs/05_UI_UX/Wireframe_Specification.md` (415 lines, **v3.0, Final**, includes actual ASCII wireframes + references the PNG screenshots in the same folder) | Genuinely three different maturity levels. The `05_UI_UX/` v3.0 copy looks like the most current/detailed one, but `Product_Index.md` points at the `01_Product_Requirements/UI/` (v1.0) copy — this is a real ambiguity, not just noise |
| Workflow Specification | **three** copies: `docs/Workflow Specification.md` (270 lines, note the space in the filename) / `docs/01_Product_Requirements/Core/Workflow_Specification.md` (81 lines, high-level) / `docs/03_Workflows/Workflow_Specification.md` (445 lines, step-by-step detail) | The `03_Workflows/` copy is the detailed one actually matching the real pipeline (Steps 1–9, exception handling, acceptance criteria); the `Core/` copy is a short abstract; the root copy is a third variant |
| CHANGELOG | `CHANGELOG.md.md` (root, 128 lines, front matter says `Owner: AI Product Factory` / `Category: Product Template`) **vs** `docs/00_Project_Management/CHANGELOG.md` (276 lines, this project's real changelog) | The root one reads as generic template boilerplate, not project-specific content — see §4 |

**None of these were modified, merged, or deleted** — flagging only, per your "do not modify any files" instruction.

---

# 4. Possible Obsolete Documents

- **`CHANGELOG.md.md`** (root) — front matter identifies it as the *AI Product Factory template's own* changelog ("Version history for AI Product Factory Template"), not this project's. Almost certainly a leftover from scaffolding this repo off a template, never cleaned up. The typo'd double extension (`.md.md`) supports this — it reads like an artifact of a copy operation rather than an intentional filename.
- **`docs/01_Product_Requirements/Principle Zero.md`** — a short, early draft ("Knowledge is the Product...") whose content is reproduced (and extended) as the opening section of `docs/01_Product_Requirements/Product_Principles_v4.0.md` ("v4.0, Final", explicitly framed as "The Constitution of YB Knowledge Factory"). The standalone file looks superseded by the v4.0 constitution doc.
- **`docs/06_Google_AI_Studio/` (9 docs)** — all scoped to the Google AI Studio *prototype* stage (build spec, numbered UI prompts 01–06, design reviewer, prototype test checklist). `Milestone_01_Prototype_Freeze/Prototype_Handover.md` confirms the prototype phase is "✅ Completed" and engineering has since moved past it (MVP is built and tested per `MVP_Test_Report.md`). These aren't wrong, but they document a stage that's now behind the project — candidates for archiving rather than active reference, not for deletion (historical record).
- **Five empty directories:** `docs/02_Prompt_Design/04_Examples/Example_02_LongTranscript/`, `Example_03_MixedLanguage/`, `Example_04_PoorTranscript/`, `Example_05_Podcast/`, and `docs/02_Prompt_Design/05_Prompt_Testing/` — all exist as folders with zero files inside. These look like planned-but-never-filled scaffolding (only `Example_01_StudyNote/` was ever populated).
- **`docs/04_Templates/Transcript_Template_v2.0.md`** (11 lines) — minor drift, not obsolete: template shows a top-level `# Transcript` heading, but the actual code (`app/transcript.py`) writes `## Transcript` (one level deeper, under the title/URL/`---` block). Small enough that I'm flagging it rather than calling it obsolete.

---

# 5. Missing Documents Referenced by Other Files

Confirmed via targeted search — these filenames are referenced (in "Related Documents" / "References" sections) but **do not exist anywhere in the repository**:

| Referenced As | Referenced From | Exists? |
|---|---|---|
| `Documentation_Standard.md` | `Development_Operating_System.md` front matter; `Product_Architecture.md` §11; `Product_Index.md`; kickoff prompt reading list | ❌ Not found |
| `Product_Blueprint.md` | Kickoff prompt reading list only | ❌ Not found |
| `AI_Pipeline_Architecture.md` | Kickoff prompt reading list only | ❌ Not found |
| `Repository_Governance.md` | Kickoff prompt reading list only | ❌ Not found |
| `Implementation_Guide.md` | `Product_Architecture.md` §11 References | ❌ Not found |
| `Application_Architecture_Blueprint_v2.0.md` (exact versioned name) | `MVP_Single_Page_Workflow.md` §12 | ⚠️ Close match exists: `Application Architecture Blueprint.md` (no version suffix, spaces instead of underscores) |
| `Wireframe_Specification_v2.0.md` (exact versioned name) | `MVP_Single_Page_Workflow.md` §12; `Application Architecture Blueprint.md` §14 | ⚠️ Close match exists (see §3 — three unversioned copies, none named exactly this) |
| `UI_Design_Pack_v1.0` | Same two files as above | ⚠️ Close match exists: `docs/05_UI_UX/UI_Design_Pack.md` (no version suffix) |
| `Google_AI_Studio_Build_Specification_v2.0.md` | `MVP_Single_Page_Workflow.md` §12 | ⚠️ Close match exists: `Google_AI_Studio_Build_Specification.md` (no version suffix) |

The pattern across the last four rows: several "Final" docs reference a specific **versioned** filename (`_v2.0.md`, `_v1.0`) that doesn't exist — only an unversioned file with similar content does. This suggests either the version suffix was dropped at some point during a rename, or the reference was written aspirationally before the file was finalized. Either way, a reader following these references literally will hit a 404.

---

# 6. Comparison With Expected Architecture

`Product_Index.md` (the repo's own declared navigation document) states the expected document set and reading order:

```text
PRD → Product Architecture → Workflow Specification → Prompt Specification
→ Runtime Specification → Output Specification → UI Component Specification
→ Wireframe Specification → Current Milestone → Coding
```

Checked against what's actually on disk:

- Every document in that list **exists** (in `01_Product_Requirements/Core/`, `02_Prompt_Design/`, or `01_Product_Requirements/UI/`) — the expected architecture is not missing pieces, structurally.
- However, for three of those eight documents (Workflow Specification, Prompt Specification, Wireframe Specification), the file `Product_Index.md` implicitly points to is **not the most detailed or most recently updated version** — richer copies exist elsewhere (`03_Workflows/`, `docs/` root, `05_UI_UX/`) that Product_Index doesn't mention at all. A reader following only `Product_Index.md`'s stated order would miss `03_Workflows/Workflow_Specification.md` (445 lines, the one with actual step-by-step pipeline detail and exception handling) entirely, since Product_Index only names `Workflow_Specification.md` without a folder path.
- `Product_Index.md` also lists `Development_Operating_System.md` and `Documentation_Standard.md` under "Project Management" related documents — the latter does not exist (§5).
- The kickoff prompt's own expected reading order (`Documentation_Standard → CLAUDE → README → Product_Blueprint → PRD → ...`) does not match `Product_Index.md`'s expected order at all (different document names, different sequence) — these two "expected architecture" definitions disagree with each other, in addition to the kickoff order naming four files that don't exist.

**Net assessment:** the repository is not missing its core product/spec/prompt/UI documentation — it's present and substantially matches what `Product_Index.md` expects. The actual problems are (a) governance/meta docs referenced from multiple places (`Documentation_Standard.md`, `Implementation_Guide.md`, `Repository_Governance.md`, `Product_Blueprint.md`, `AI_Pipeline_Architecture.md`) that were never created, and (b) unresolved duplication where the "expected" canonical copy is not the most complete one.

---

# 7. What This Report Does Not Cover

This is a structural/inventory pass only — it does not evaluate whether document *content* is internally consistent (e.g., whether the Study Note section names in `PRD.md` match the actual generated output). Several such content-level conflicts were found while reading documents for `Engineering_Understanding_Report.md` and are recorded there instead, to keep this report scoped to "what exists on disk and how it's organized."

---

# Stop Condition

No files were modified, merged, renamed, or deleted while producing this report. Waiting for direction on which of the items in §3–§5 (if any) should be cleaned up, and whether to proceed to `Engineering_Understanding_Report.md`'s open questions next.
