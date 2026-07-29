---
Version: v1.0
Status: Final
Owner: YB
Document: Product Architecture
Category: Product Design
Context Weight: High
Primary Consumer: All AI Agents
Load Trigger: Architecture Design / Feature Planning
Last Updated: 2026-07-28
---

# Product Architecture

## 1. Purpose

Define the overall architecture of YB Knowledge Factory.

This document describes **how the product is organized**, not why it exists, how it is implemented, or detailed workflows.

---

# 2. System Overview

```
                    User
                      │
                Web Interface
                      │
                Backend Service
                      │
             AI Processing Engine
                      │
                Runtime Storage
                      │
                 Output Files
```

---

# 3. Product Layers

| Layer | Responsibility |
|--------|----------------|
| User Interface | User interaction |
| Backend | Workflow orchestration & API |
| AI Engine | Transcript, Study Note, Knowledge Generation |
| Runtime | Temporary files & processing |
| Output | Markdown / Export files |

---

# 4. Platform Architecture

| Platform | Status | Shared Logic |
|----------|--------|--------------|
| Web | MVP | Yes |
| Android | Planned | Yes |
| iOS | Planned | Yes |
| Desktop | Future | Yes |

Platform differences are limited to the User Interface.

Business Logic, AI Workflow and Runtime remain shared.

---

# 5. Core Modules

| Module | Responsibility |
|---------|----------------|
| Transcript | Speech-to-Text |
| Study Note | AI Summary |
| Knowledge Card | Knowledge Extraction |
| Export | Markdown Generation |
| Runtime | File Management |

---

# 6. Data Flow

```
YouTube URL
      │
      ▼
Transcript
      │
      ▼
Study Note
      │
      ▼
Knowledge Card
      │
      ▼
Export
```

Detailed workflow is defined in:

> Workflow_Specification.md

---

# 7. Module Dependency

```
User Interface
        │
        ▼
Backend Service
        │
        ▼
AI Engine
        │
        ▼
Runtime
        │
        ▼
Output
```

---

# 8. Runtime Architecture

```
Input
 │
 ▼
Temporary Files
 │
 ▼
Transcript
 │
 ▼
Study Note
 │
 ▼
Knowledge Card
 │
 ▼
Output
```

Runtime manages:

- Temporary Files
- Transcript
- Study Notes
- Knowledge Cards
- Export Files

---

# 9. Architecture Constraints

| Rule | Description |
|------|-------------|
| Shared Workflow | All platforms use the same workflow |
| Shared Backend | Single backend implementation |
| Shared AI | Same Prompt & AI Pipeline |
| Shared Runtime | Same file structure |
| Platform UI Only | UI may differ by platform |

---

# 10. Capability Roadmap

| Capability | MVP | Future |
|------------|-----|--------|
| YouTube | ✓ | |
| Study Note | ✓ | |
| Knowledge Card | ✓ | |
| SOP Builder | | ✓ |
| Prompt Builder | | ✓ |
| Multi-language | | ✓ |
| Android | | ✓ |
| iOS | | ✓ |

---

# 11. References

This document intentionally avoids implementation details.

See:

- PRD.md
- Workflow_Specification.md
- Technical_Decision.md
- Wireframe_Specification.md
- Implementation_Guide.md
- Documentation_Standard.md