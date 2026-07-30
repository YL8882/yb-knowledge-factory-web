---
Version: v1.0
Status: Final
Owner: YB
Document: Workflow Specification
Category: Workflow
Purpose: Define the end-to-end workflow for the MVP.
Priority: Critical
Last Updated: 2026-07-29
---

# Workflow Specification

# 1. Purpose

本文件定義 YB Knowledge Factory MVP 的標準工作流程。

目的：

- 定義資料流（Data Flow）
- 定義各階段責任
- 作為 Claude Code 的開發依據
- 避免功能重複與流程混亂

本文件不描述程式實作細節。

---

# 2. Workflow Overview

```text
使用者

↓

貼上 YouTube URL

↓

取得影片資訊

↓

取得 Transcript

↓

產生 Study Note

↓

產生 Markdown

↓

下載檔案

↓

完成
```

---

# 3. Workflow Steps

## Step 01：輸入影片網址

Input：

- YouTube URL

Output：

- Video URL

下一步：

取得影片資訊。

---

## Step 02：取得影片資訊

目的：

取得影片基本資訊。

內容：

- Video Title
- Video ID

Output：

Video Metadata

下一步：

取得逐字稿。

---

## Step 03：取得 Transcript

優先順序：

1. 官方字幕
2. AI Speech-to-Text

Output：

Transcript

儲存：

```
runtime/transcripts/
```

---

## Step 04：產生 Study Note

Input：

Transcript

依照：

Study Note Prompt

輸出：

Study Note

儲存：

```
runtime/study_notes/
```

---

## Step 05：輸出 Markdown

產生：

- Transcript.md
- Study_Note.md

提供：

下載。

Workflow 完成。

---

# 4. Runtime Flow

```text
URL

↓

Metadata

↓

Transcript

↓

Study Note

↓

Markdown
```

---

# 5. Folder Output

Transcript

```
runtime/transcripts/
```

Study Note

```
runtime/study_notes/
```

---

# 6. AI Responsibilities

Frontend

- URL Input
- Progress
- Download

Backend

- Workflow Control
- Runtime Management

AI Service

- Transcript
- Study Note

---

# 7. Error Handling

若：

URL 無效

↓

停止流程

若：

Transcript 取得失敗

↓

顯示錯誤

若：

Study Note 產生失敗

↓

保留 Transcript

---

# 8. Acceptance Criteria

Workflow 成功代表：

☐ 可以輸入 URL

☐ 可以取得影片資訊

☐ 可以完成 Transcript

☐ 可以完成 Study Note

☐ 可以下載 Markdown

☐ 全流程成功完成

---

# References

- Development_Operating_System.md
- PRD.md
- Prompt_Specification.md
- Product_Architecture.md