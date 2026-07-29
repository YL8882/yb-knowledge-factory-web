---
Version: v1.0
Status: Final
Owner: YB
Document: UI Component Specification
Category: UI
Context Weight: Medium
Load Trigger: Frontend Development / UI Implementation
Last Updated: 2026-07-28
---

# UI Component Specification

## 1. Purpose

Define reusable UI components for YB Knowledge Factory.

This document specifies:

- UI components
- Component responsibilities
- Component interactions

Visual design and implementation are intentionally excluded.

---

# 2. Component Overview

```text
Page
 │
 ├── Input
 ├── Button
 ├── Progress
 ├── Card
 ├── List
 └── Download
```

---

# 3. Component List

| Component | Purpose |
|-----------|---------|
| URL Input | Enter YouTube URL |
| Action Button | Start processing |
| Progress Bar | Display processing status |
| Status Label | Show current stage |
| Result Card | Display generated content |
| Asset List | List generated files |
| Download Button | Download output files |
| Navigation Button | Start a new task |

---

# 4. URL Input

### Responsibility

Accept a YouTube URL.

### States

| State | Description |
|--------|-------------|
| Empty | No URL entered |
| Valid | Valid YouTube URL |
| Invalid | Invalid URL format |

---

# 5. Action Button

### Responsibility

Start the workflow.

### States

| State | Description |
|--------|-------------|
| Enabled | Ready to start |
| Disabled | Waiting for input |
| Loading | Workflow running |

---

# 6. Progress Bar

### Responsibility

Display workflow progress.

Stages

- Download
- Transcription
- Study Note
- Complete

---

# 7. Result Card

### Responsibility

Display generated assets.

Content

- Video Title
- Summary
- Generated Files

---

# 8. Asset List

Display available outputs.

- Transcript
- Study Note
- Knowledge Card
- SOP
- Prompt

---

# 9. Download Button

### Responsibility

Export generated files.

Supported Formats

- Markdown

Future

- PDF
- DOCX

---

# 10. Navigation Button

Available Actions

- New Task
- Back Home

---

# 11. Component Rules

- One responsibility per component.
- Components should be reusable.
- Keep interactions simple.
- Use consistent naming.
- Avoid duplicated functionality.

---

# 12. References

- Wireframe_Specification.md
- Product_Architecture.md
- Workflow_Specification.md