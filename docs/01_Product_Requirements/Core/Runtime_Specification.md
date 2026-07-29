---
Version: v1.0
Status: Final
Owner: YB
Document: Runtime Specification
Category: Runtime
Context Weight: Medium
Load Trigger: Runtime Development / Backend Development
Last Updated: 2026-07-28
---

# Runtime Specification

## 1. Purpose

Define the runtime behavior of YB Knowledge Factory.

This document specifies:

- Runtime lifecycle
- Runtime folder structure
- File naming rules
- Temporary file policy

Implementation details are intentionally excluded.

---

# 2. Runtime Lifecycle

```text
YouTube URL
    │
    ▼
Input
    │
    ▼
Processing
    │
    ▼
Artifacts
    │
    ▼
Export
```

---

# 3. Runtime Structure

```text
03_Runtime/

├── Input/
├── Processing/
├── Artifacts/
├── Export/
└── Temp/
```

---

# 4. Folder Responsibility

| Folder | Responsibility |
|----------|----------------|
| Input | Source URLs and input metadata |
| Processing | Runtime processing files (Audio, Transcript) |
| Artifacts | AI-generated knowledge assets |
| Export | Final exported files |
| Temp | Temporary runtime files |

---

# 5. Runtime Outputs

| Stage | Output |
|--------|--------|
| Input | Source URL |
| Processing | Audio / Transcript |
| Artifacts | Study Note / Knowledge Card / SOP / Prompt |
| Export | Markdown / PDF (Future) |

---

# 6. File Naming

Standard Format

```text
{Title}_{VideoID}.md
```

Example

```text
Claude_Code_ABC123.md
```

Rules

- Preserve original title whenever possible.
- Preserve unique Video ID.
- Use UTF-8 filenames.
- Avoid duplicate filenames.

---

# 7. Runtime Rules

- Each runtime stage has a single responsibility.
- Temporary files must remain inside `Temp/`.
- Only completed assets are exported.
- Preserve source metadata throughout the pipeline.
- Never overwrite existing output files.

---

# 8. Temporary File Policy

Temporary files include:

- Download cache
- Audio cache
- Intermediate processing files

Rules

- Store only in `Temp/`.
- Remove automatically after successful completion.
- Keep only when debugging is enabled.

---

# 9. References

- PRD.md
- Product_Architecture.md
- Workflow_Specification.md
- Technical_Decision.md
- Output_Specification.md