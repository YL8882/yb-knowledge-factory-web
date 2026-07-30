---
Version: v1.0
Status: Final
Owner: YB
Document: Product Requirements Document (PRD)
Category: Product Requirements
Purpose: Define the MVP scope, requirements, and acceptance criteria.
Priority: Critical
Last Updated: 2026-07-29
---

# Product Requirements Document (PRD)

# 1. Product Overview

## Product Name

YB Knowledge Factory MVP

## Product Vision

建立一套以 AI 為核心的知識學習工具。

使用者只需貼上 YouTube 網址，即可快速取得逐字稿（Transcript）與 AI 學習筆記（Study Note），並輸出為 Markdown，方便整理至個人知識庫。

本產品採用：

- Web First
- MVP First
- Workflow First
- AI First

策略，優先驗證產品價值，再逐步擴充功能。

---

# 2. MVP Goal

完成第一個可實際使用的 Web MVP。

成功流程如下：

YouTube URL

↓

Transcript

↓

Study Note

↓

Markdown Download

使用者可於數分鐘內完成整個流程。

---

# 3. Target Users

主要使用者：

- AI 學習者
- YouTube 重度學習者
- 知識工作者
- 研究人員
- 課程整理者

---

# 4. Core Features

MVP 僅包含以下功能。

## Feature 01

輸入 YouTube 網址。

---

## Feature 02

取得影片逐字稿。

若沒有官方字幕，可使用 AI Speech-to-Text。

---

## Feature 03

產生 Study Note。

依照 Study Note Prompt 與 Template 輸出。

---

## Feature 04

下載：

- Transcript.md
- Study_Note.md

---

# 5. Out of Scope

以下功能不屬於 MVP。

- 登入
- 會員
- 訂閱
- 資料庫
- 雲端同步
- 多人協作
- Mobile App
- iOS
- Android
- 多語系 UI
- RAG
- Agent
- Marketplace

未來版本再規劃。

---

# 6. Product Workflow

標準流程：

YouTube URL

↓

Transcript

↓

Study Note

↓

Markdown Output

Workflow 詳細內容請參考：

Workflow_Specification.md

---

# 7. User Interface

首頁包含：

- YouTube URL
- Generate 按鈕
- Processing 狀態
- Download Transcript
- Download Study Note

詳細 UI 請參考：

Wireframe_Specification.md

---

# 8. Technical Scope

Frontend

- Web Application

Backend

- API

Runtime

- Audio
- Transcript
- Study Note

詳細架構請參考：

Product_Architecture.md

---

# 9. Acceptance Criteria

MVP 完成時應符合：

□ 可以貼上 YouTube 網址

□ 可以取得逐字稿

□ 可以產生 Study Note

□ 可以下載 Transcript.md

□ 可以下載 Study_Note.md

□ 完整流程可成功執行

---

# 10. Future Roadmap

V1

完成 Web MVP。

V2

加入多語系。

V3

推出 iOS / Android。

V4

登入、同步、訂閱。

---

# References

- Development_Operating_System.md
- Workflow_Specification.md
- Prompt_Specification.md
- Product_Architecture.md
- Wireframe_Specification.md