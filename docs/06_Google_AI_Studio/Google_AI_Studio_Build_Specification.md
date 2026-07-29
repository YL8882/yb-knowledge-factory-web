# Google_AI_Studio_Build_Specification_v2.0.md

---
Title: Google AI Studio Build Specification
Version: v2.0
Status: Final
Owner: YB
Product: YB Knowledge Factory MVP v0.1
Document Type: Build Specification
Language: Traditional Chinese
Last Updated: 2026-07-23
---

# 1. Purpose

本文件定義如何使用 Google AI Studio 建立 **YB Knowledge Factory MVP v0.1** 的第一版 Prototype。

Google AI Studio 的任務不是開發正式產品，而是快速建立可驗證的 MVP，確認：

- Workflow 是否正確
- Prompt 是否有效
- UI 是否符合需求
- 使用流程是否順暢
- MVP 是否具備開發價值

Prototype 驗證完成後，再交由 Claude Code 完成正式開發。

---

# 2. Build Objectives

本 Prototype 必須完成以下核心流程：

YouTube URL

↓

Download Audio

↓

Generate Transcript

↓

Generate Study Note

↓

Download Results

整個流程必須由使用者一次操作完成。

---

# 3. MVP Scope

## Included

- Single Page Web Application
- YouTube URL Input
- Generate Button
- Workflow Progress
- Audio Module
- Transcript Module
- Study Note Module
- Download Files

## Excluded

- Login
- User Management
- Dashboard
- History
- Settings
- Database
- Subscription
- Cloud Storage
- Multi-user

---

# 4. Build Principles

Google AI Studio 開發 Prototype 必須遵循以下原則。

## Workflow First

先完成 Workflow，再優化畫面。

---

## Prototype First

目標是建立可驗證 Prototype，而不是 Production。

---

## Single Page

MVP 僅保留一個操作頁面。

---

## Reuse Existing Specifications

所有設計均引用既有文件：

- PRD
- Workflow Specification
- Application Architecture Blueprint
- Wireframe Specification
- UI Design Pack
- Prompt Design

不得重新定義產品需求。

---

## No Scope Expansion

不得自行增加需求。

例如：

- Dark Mode
- Search
- History
- Dashboard
- Analytics

均不屬於 MVP。

---

# 5. Required Input Documents

建置 Prototype 前，需先閱讀以下文件：

| 文件 | 用途 |
|------|------|
| PRD.md | 定義產品需求 |
| Technical_Decision.md | 技術選型 |
| Workflow_Specification.md | Workflow 規格 |
| Application_Architecture_Blueprint_v2.0.md | 系統架構 |
| Wireframe_Specification_v2.0.md | UI 規格 |
| UI_Design_Pack_v1.0 | 視覺設計 |
| StudyNote Prompt | AI Prompt |

---

# 6. Application Structure

Prototype 採 Single Page Layout。

```
Header

↓

YouTube URL Input

↓

Generate Button

↓

Workflow Progress

↓

Audio Module

↓

Transcript Module

↓

Study Note Module

↓

Footer
```

不得增加其他頁面。

---

# 7. Workflow Implementation

Generate Button 為唯一入口。

Workflow：

```
Paste URL

↓

Download Audio

↓

Generate Transcript

↓

Generate Study Note

↓

Download Files
```

每個步驟完成後，自動進入下一步。

---

# 8. Module Responsibilities

## Audio Module

Input：

- YouTube URL

Output：

- Audio File

功能：

- Download
- Rename
- Save
- Download Button

---

## Transcript Module

Input：

- Audio File

Output：

- Transcript.md

功能：

- Speech-to-Text
- Format
- Save
- Download

---

## Study Note Module

Input：

- Transcript.md

Output：

- StudyNote.md

功能：

- Prompt
- LLM
- Template
- Save
- Download

---

# 9. Runtime Rules

Module 間以檔案傳遞資料。

```
Audio

↓

Transcript

↓

Study Note
```

禁止跨 Module 直接存取。

每個 Module 僅負責：

Read

↓

Process

↓

Write

---

# 10. State Management

所有 Module 共用 State。

```
Waiting

↓

Processing

↓

Completed

↓

Downloaded
```

失敗：

```
Processing

↓

Error

↓

Retry

↓

Waiting
```

UI 必須同步更新。

---

# 11. File Naming Convention

Audio

```
{VideoTitle}_{YouTubeID}.mp3
```

Transcript

```
{VideoTitle}_{YouTubeID}_Transcript.md
```

Study Note

```
{VideoTitle}_{YouTubeID}_StudyNote.md
```

所有檔名皆自動產生。

---

# 12. Build Sequence

建議依照以下順序完成：

1. 建立 Single Page Layout
2. 建立 URL Input
3. 建立 Generate Button
4. 建立 Workflow Progress
5. 建立 Audio Module
6. 建立 Transcript Module
7. 建立 Study Note Module
8. 建立 Download 功能
9. Runtime 測試
10. Prototype 驗證

---

# 13. Validation Checklist

Prototype 完成後，至少驗證：

- 可以貼上 YouTube URL
- 可以開始 Workflow
- Audio 成功產生
- Transcript 成功產生
- Study Note 成功產生
- 三個檔案皆可下載
- Workflow 狀態正確更新
- UI 顯示正常

全部通過後，Prototype 視為完成。

---

# 14. Handoff to Claude Code

Prototype 驗證完成後，由 Claude Code 接手正式開發。

Google AI Studio：

- Workflow 驗證
- Prompt 驗證
- Prototype UI

Claude Code：

- 程式碼重構
- API 串接
- Runtime 優化
- Error Handling
- Production Ready

---

# 15. Success Criteria

Prototype 完成代表：

- 使用者只需貼上一個 YouTube URL。
- 系統可自動完成 Audio、Transcript、Study Note 三個 Workflow。
- 三個成果檔案可正常下載。
- 全流程無需人工介入。

達成以上條件，即完成 MVP Prototype。

---

# 16. Related Documents

- PRD.md
- Technical_Decision.md
- Workflow_Specification.md
- Application_Architecture_Blueprint_v2.0.md
- Wireframe_Specification_v2.0.md
- UI_Design_Pack_v1.0
- Prompt_Specification.md
- Prototype_Test_Checklist.md

---

# Appendix A — Build Pipeline

```
Read Product Documents
        │
        ▼
Build Single Page UI
        │
        ▼
Implement Workflow
        │
        ▼
Implement Runtime
        │
        ▼
Prototype Testing
        │
        ▼
Prototype Validation
        │
        ▼
Handoff to Claude Code
```

---

# Document Summary

本文件作為 **Google AI Studio Prototype 建置指南**，負責定義 MVP Prototype 的建置流程、驗證方式與交接標準。

它不重新定義產品需求，而是依據既有的 **PRD、Architecture Blueprint、Wireframe Specification、UI Design Pack** 等文件，快速完成可驗證的 Prototype，並作為後續 Claude Code 正式開發的基礎。