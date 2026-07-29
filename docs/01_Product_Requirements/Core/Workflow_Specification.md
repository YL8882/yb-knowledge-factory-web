---
Version: v1.0
Status: Final
Owner: YB
Document: Workflow Specification
Category: Workflow
Context Weight: High
Load Trigger: Product Development / Backend Development
Last Updated: 2026-07-28
---

# Workflow Specification

## Purpose

Define the end-to-end workflow of YB Knowledge Factory.

This document describes **what happens**, not **how it is implemented**.

---

# Workflow Overview

```text
YouTube URL
    │
    ▼
Download
    │
    ▼
Transcription
    │
    ▼
Study Note
    │
    ▼
Knowledge Assets
    │
    ▼
Export
```

---

# Workflow Stages

| Stage | Input | Output |
|--------|-------|--------|
| Download | YouTube URL | Audio |
| Transcription | Audio | Transcript |
| Study Note | Transcript | Study Note |
| Knowledge Assets | Study Note | Knowledge Cards / SOP / Prompt / Skills |
| Export | Knowledge Assets | Markdown Files |

---

# Workflow Rules

- Each stage has one clear responsibility.
- Output from one stage becomes the input of the next stage.
- Stages should remain independent and replaceable.
- Failed stages must not affect completed outputs.

---

# Workflow Outputs

| Stage | Generated Asset |
|--------|-----------------|
| Transcription | Transcript.md |
| Study Note | Study_Note.md |
| Knowledge Assets | Knowledge Cards, SOPs, Prompt Library, Skills |
| Export | Final Markdown Files |

---

# References

- PRD.md
- Product_Architecture.md
- Runtime_Specification.md
- Technical_Decision.md