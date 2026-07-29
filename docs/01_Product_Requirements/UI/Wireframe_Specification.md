---
Version: v1.0
Status: Final
Owner: YB
Document: Wireframe Specification
Category: UI
Context Weight: Medium
Load Trigger: Frontend Development / UI Design
Last Updated: 2026-07-28
---

# Wireframe Specification

## 1. Purpose

Define the page layout and user interaction flow of YB Knowledge Factory.

This document specifies:

- Page structure
- UI components
- User flow
- Navigation

Visual design and implementation are intentionally excluded.

---

# 2. User Flow

```text
Home
 │
 ▼
Processing
 │
 ▼
Result
 │
 ├──────────► Download
 │
 └──────────► New Task
```

---

# 3. Page Structure

| Page | Purpose |
|------|---------|
| Home | Create a new task |
| Processing | Display processing status |
| Result | Display generated outputs |

---

# 4. Home

```text
+--------------------------------------------------+
| YB Knowledge Factory                             |
+--------------------------------------------------+

 YouTube URL

 [________________________________________]

              [ Generate Study Note ]

----------------------------------------------------

 Recent Tasks

 • Video A
 • Video B
 • Video C
```

### Components

| Component | Purpose |
|-----------|---------|
| URL Input | Enter YouTube URL |
| Generate Button | Start workflow |
| Recent Tasks | Quick access to history |

---

# 5. Processing

```text
+--------------------------------------------------+

Processing...

██████████░░░░░░░

Downloading

↓

Transcribing

↓

Generating Study Note

↓

Completed
```

### Components

| Component | Purpose |
|-----------|---------|
| Progress Bar | Processing status |
| Current Stage | Current workflow step |

---

# 6. Result

```text
+--------------------------------------------------+

Video Title

Summary

-----------------------------

✓ Transcript

✓ Study Note

✓ Knowledge Card

-----------------------------

[ Download Transcript ]

[ Download Study Note ]

[ New Task ]
```

### Components

| Component | Purpose |
|-----------|---------|
| Summary | AI summary |
| Asset List | Generated outputs |
| Download Buttons | Export files |
| New Task | Return to Home |

---

# 7. Navigation

```text
Home
 │
 ▼
Processing
 │
 ▼
Result
 │
 ├── Download
 └── New Task
```

---

# 8. UI Rules

- One primary action per page.
- Keep layout simple and focused.
- Display processing progress clearly.
- Group generated assets together.
- Minimize unnecessary navigation.

---

# 9. References

- PRD.md
- Product_Architecture.md
- Workflow_Specification.md
- Application_Architecture_Blueprint.md