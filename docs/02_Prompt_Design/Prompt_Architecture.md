# Prompt Architecture

**Document Version:** v1.0 (Final)  
**Module:** 02_Prompt_Design  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# 1. Purpose

本文件定義 **YB Knowledge Factory** 的 Prompt System Architecture。

目的：

- 建立統一 Prompt 架構
- 建立 Prompt 分層設計（Layered Architecture）
- 降低 Prompt 維護成本
- 提高 Prompt 可重用性
- 支援未來所有 AI Product 共用

Prompt 並非單一提示詞，而是一套完整的 AI 工作流程（Prompt Pipeline）。

---

# 2. Design Philosophy

Prompt 設計遵循以下原則：

- Workflow First
- Template First
- Structured Output
- Separation of Concerns
- Modular Design
- Version Controlled

每個 Prompt 僅負責單一工作，不混合不同職責。

---

# 3. Prompt Architecture Overview

整體架構如下：

```text
                Workflow
                    │
                    ▼
            Output Template
                    │
                    ▼
            Output Schema
                    │
                    ▼
             System Prompt
                    │
                    ▼
              User Prompt
                    │
                    ▼
              AI Model (LLM)
                    │
                    ▼
             Markdown Output
```

每一層皆可獨立維護。

---

# 4. Prompt Layers

Prompt 系統共分六層。

---

## Layer 1 — Workflow

定義：

AI 要完成什麼工作。

例如：

```
Transcript

↓

Study Note
```

Workflow 不包含 Prompt。

只定義：

- Input
- Output
- Business Flow

---

## Layer 2 — Template

Template 定義文件結構。

例如：

```
# Title

一句話摘要

重點摘要

重點解析

操作流程

延伸資訊
```

Template 不包含 AI 指令。

---

## Layer 3 — Output Schema

Schema 定義：

AI 必須輸出的格式。

例如：

- Markdown
- Heading
- List
- Table

Schema 不定義內容。

只定義格式。

---

## Layer 4 — System Prompt

System Prompt 定義：

AI 身分。

例如：

- Role
- Goal
- Constraints
- Writing Style

System Prompt 通常長期固定。

---

## Layer 5 — User Prompt

User Prompt 定義：

本次工作的需求。

例如：

```
請閱讀下面逐字稿，
依照指定格式產生 Study Note。
```

這是最常調整的 Prompt。

---

## Layer 6 — AI Model

目前：

Gemini 2.5 Flash

未來可替換：

- GPT
- Claude
- Gemini Pro
- Local LLM

Prompt 不依賴模型。

---

# 5. Prompt Pipeline

MVP 採用以下 Pipeline：

```text
Transcript.md
        │
        ▼
StudyNote_Output_Schema
        │
        ▼
StudyNote_System_Prompt
        │
        ▼
StudyNote_User_Prompt
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
Study_Note.md
```

所有 Study Note 均遵循此流程。

---

# 6. Input Architecture

Prompt 不直接接收：

- YouTube URL
- Audio
- Video

Prompt 只接收：

```
Transcript.md
```

內容包括：

- Title
- URL
- Transcript

降低 Prompt 的複雜度。

---

# 7. Output Architecture

Prompt 必須輸出：

```
Study_Note.md
```

固定格式：

```
Title

Video URL

一句話摘要

重點摘要

重點解析

操作流程

延伸資訊
```

不得變更章節順序。

---

# 8. Prompt Components

每個 Prompt Package 包含：

```
StudyNote/

├── System Prompt
├── User Prompt
├── Output Schema
├── Examples
├── Test Cases
└── Version History
```

此架構適用所有 Prompt。

---

# 9. Prompt Lifecycle

所有 Prompt 均遵循：

```text
Requirement
      │
      ▼
Architecture
      │
      ▼
Template
      │
      ▼
Prompt Design
      │
      ▼
Testing
      │
      ▼
Release
      │
      ▼
Maintenance
```

禁止直接撰寫 Prompt 而略過前置設計。

---

# 10. MVP Prompt Architecture

MVP v0.1 僅包含一個 Prompt。

```
StudyNote_Prompt_v1.0
```

實際組成：

```
StudyNote_System_Prompt_v1.0

+

StudyNote_User_Prompt_v1.0

+

StudyNote_Output_Schema_v1.0

+

Examples

+

Test Cases
```

---

# 11. Future Architecture

未來所有 Prompt 將共用相同架構。

```
Knowledge Card

↓

SOP

↓

Prompt Library

↓

Skills

↓

Course

↓

Business Model

↓

AI Product
```

每個 Prompt 僅替換：

- Workflow
- Template
- Output Schema

Architecture 保持一致。

---

# 12. Architecture Principles

所有 Prompt 必須符合：

### Single Responsibility

一個 Prompt 僅完成一件事。

---

### Separation of Concerns

Workflow

Template

Schema

Prompt

彼此獨立。

---

### Structured Output

所有輸出皆固定格式。

---

### Model Independent

不得依賴：

- Gemini
- GPT
- Claude

可自由替換模型。

---

### Version Controlled

所有 Prompt 必須版本化管理。

例如：

```
StudyNote_System_Prompt_v1.0

StudyNote_System_Prompt_v1.1

StudyNote_System_Prompt_v2.0
```

---

# 13. Architecture Benefits

採用本架構可獲得：

- Prompt 容易維護
- Prompt 可重複利用
- Prompt 可測試
- Prompt 可版本管理
- Prompt 可快速替換模型
- Prompt 可快速擴充新產品
- Prompt 可交由 AI Agent 自動維護

---

# 14. Related Documents

```
01_Product_Requirements/
├── PRD.md
├── Technical_Decision.md
├── Workflow_Specification.md
└── Prompt_Specification.md

02_Prompt_Design/
├── README.md
├── Prompt_Architecture.md
├── Prompt_Development_Guide.md
└── Prompt_Test_Plan.md
```

---

# Document Status

| Item     | Value                         |
| -------- | ----------------------------- |
| Document | Prompt Architecture           |
| Version  | v1.0 (Final)                  |
| Product  | YB Knowledge Factory MVP v0.1 |
| Status   | ✅ Final                       |