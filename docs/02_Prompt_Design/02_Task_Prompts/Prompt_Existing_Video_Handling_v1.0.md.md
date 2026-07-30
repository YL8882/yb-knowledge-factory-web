---
title: Prompt_Existing_Video_Handling_v1.0
version: v1.0
status: Final
owner: YB
document_type: Development Task Prompt
feature: Existing Video Handling
priority: High
target: Claude Code
last_updated: 2026-07-30
---

# Feature: Existing Video Handling

## Objective

Detect when a YouTube video has already been processed.

Prevent duplicate processing by reusing existing outputs whenever possible while allowing users to choose the next action.

---

## Requirements

Before starting a new processing task, determine whether outputs already exist for the selected YouTube video.

If previous outputs exist:

- Do not start processing automatically.
- Inform the user that the video has already been processed.
- Display only the actions supported by the existing outputs.
- Allow the user to decide the next action.

If some outputs are missing:

- Reuse all existing outputs.
- Generate only the missing outputs.

---

## Regeneration

When the user requests regeneration:

- Reuse all reusable outputs.
- Regenerate only the assets explicitly requested by the user.

---

## Future Compatibility

Design this feature to support future knowledge assets without requiring redesign.

Future outputs may include, but are not limited to:

- Transcript
- Study Note
- Knowledge Card
- SOP
- Prompt Library

The system should always identify:

- Existing outputs
- Missing outputs

Only generate missing outputs.

---

## User Experience

Always preserve existing knowledge assets.

Users should be able to continue building knowledge from previously generated outputs without repeating completed work.

---

## Constraints

Do NOT:

- Automatically overwrite existing outputs.
- Generate duplicate outputs.
- Start processing without user confirmation.
- Redesign the existing UI.
- Modify unrelated code.

Modify only the files required for this feature.

---

## Deliverable

Implement the Existing Video Handling feature while preserving the current architecture, workflow, and user experience.

Start implementing immediately.