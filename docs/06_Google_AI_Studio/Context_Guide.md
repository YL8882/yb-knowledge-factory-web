# Context_Guide.md

---
Title: Context Guide
Version: v2.0
Status: Final
Owner: YB
Product: YB Knowledge Factory MVP v0.1
Document Type: AI Context Guide
Language: Traditional Chinese
Last Updated: 2026-07-23
---

# 1. Purpose

本文件為 Google AI Studio 的 Context Entry Point。

目的：

- 建立完整專案 Context
- 指引 AI 閱讀正確文件
- 避免重複定義需求
- 確保所有 Prototype 依照同一套規格建立

本文件不定義產品需求，而是告知 AI：

> **開始 Build 前應閱讀哪些文件，以及閱讀順序。**

---

# 2. Project Goal

建立一個可驗證的 MVP。

Workflow：

YouTube URL

↓

Download Audio

↓

Generate Transcript

↓

Generate Study Note

↓

Download Results

使用者只需：

- 貼上 YouTube URL
- 點擊 Generate

其餘流程全部自動完成。

---

# 3. AI Working Principles

Google AI Studio 建立 Prototype 時，必須遵循：

- Workflow First
- MVP First
- Single Page
- Desktop First
- Reuse Existing Specifications
- No Scope Expansion

不得自行新增需求。

---

# 4. Document Reading Order

開始 Build 前，請依照以下順序閱讀。

## Step 1

PRD.md

目的：

了解產品需求。

---

## Step 2

Technical_Decision.md

目的：

了解技術限制。

---

## Step 3

Workflow_Specification.md

目的：

了解完整 Workflow。

---

## Step 4

Application_Architecture_Blueprint_v2.0.md

目的：

了解整體產品架構。

---

## Step 5

Wireframe_Specification_v2.0.md

目的：

了解 UI 配置。

---

## Step 6

UI_Design_Pack_v1.0

目的：

了解畫面設計。

---

## Step 7

Study Note Prompt

目的：

了解 AI 如何產生 Study Note。

---

## Step 8

Google_AI_Studio_Build_Specification_v2.0.md

目的：

開始 Build Prototype。

---

# 5. Source of Truth

所有需求均以以下文件為準。

| 文件 | 職責 |
|------|------|
| PRD | 產品需求 |
| Technical Decision | 技術選型 |
| Workflow Specification | Workflow |
| Application Blueprint | 系統架構 |
| Wireframe Specification | UI 規格 |
| UI Design Pack | UI 設計 |
| Prompt Design | AI Prompt |

若不同文件內容衝突：

以較高層級文件為準。

優先順序：

PRD

↓

Architecture

↓

Workflow

↓

Wireframe

↓

UI Design

↓

Prompt

---

# 6. Scope Boundary

本次 Prototype 僅包含：

- Single Page
- YouTube URL
- Audio
- Transcript
- Study Note
- Download

不包含：

- Login
- Dashboard
- Database
- Search
- History
- Settings
- Subscription
- Analytics

---

# 7. Expected Output

Google AI Studio 最終輸出：

- Single Page Prototype
- Audio Module
- Transcript Module
- Study Note Module
- Download Buttons

Prototype 必須符合：

Workflow 可操作

Prompt 可驗證

UI 可展示

---

# 8. Validation

Prototype 完成後：

請依照：

Prototype_Test_Checklist.md

完成驗證。

全部通過後：

Prototype 即完成。

---

# 9. Handoff

Prototype 驗證完成後：

交由 Claude Code。

Claude Code 負責：

- Production Code
- API Integration
- Runtime Optimization
- Error Handling
- Refactoring

Google AI Studio 任務結束。

---

# 10. Workspace Structure

Google AI Studio Workspace：

```

06_Google_AI_Studio/
│
├── README.md
├── Context_Guide.md
├── Google_AI_Studio_Build_Specification_v2.0.md
└── Prototype_Test_Checklist.md

```

Context_Guide 為所有工作的入口文件。

---

# Document Summary

Context_Guide.md 是 Google AI Studio Workspace 的入口文件。

它不定義產品需求，而是建立 AI 的工作 Context，指引 AI 依照既有規格建立 Prototype，確保所有建置流程遵循相同的產品需求、架構與設計規範。