# MVP_Single_Page_Workflow.md

---
Title: MVP Single Page Workflow
Version: v1.0
Status: Final
Owner: YB
Product: YB Knowledge Factory MVP v0.1
Document Type: Product Workflow Specification
Language: Traditional Chinese
Last Updated: 2026-07-23
---

# 1. Purpose

本文件定義 **YB Knowledge Factory MVP v0.1** 的核心產品 Workflow。

目的：

- 定義使用者完整操作流程
- 定義系統執行流程
- 作為 UI、Workflow、Build 的共同依據
- 提供 Google AI Studio 與 Claude Code 實作參考

本文件描述的是 **產品流程（Product Workflow）**，不包含技術實作細節。

---

# 2. Design Principles

MVP Workflow 採用以下設計原則：

- Single Page
- One Workflow
- One Click Generate
- Auto Pipeline
- File Driven
- Desktop First
- MVP First

---

# 3. Workflow Overview

整個 MVP 僅提供一個核心工作流程：

```text
Paste YouTube URL
        │
        ▼
Click Generate
        │
        ▼
Download Audio
        │
        ▼
Generate Transcript
        │
        ▼
Generate Study Note
        │
        ▼
Download Results
```

所有流程皆由系統自動完成。

---

# 4. User Workflow

使用者操作流程如下：

```text
Open Application
        │
        ▼
Paste YouTube URL
        │
        ▼
Click Generate
        │
        ▼
Observe Processing Status
        │
        ▼
Download Output Files
        │
        ▼
Finish
```

使用者僅需完成兩個操作：

1. 貼上 YouTube URL
2. 點擊 Generate

其餘皆由系統自動處理。

---

# 5. System Workflow

Generate 後，系統依序執行：

```text
Generate
        │
        ▼
Audio Workflow
        │
        ▼
Transcript Workflow
        │
        ▼
Study Note Workflow
        │
        ▼
Output Files
```

Workflow 不允許跳步或並行執行。

---

# 6. Workflow Modules

MVP 包含三個核心模組。

## Module 1 — Audio

Input：

- YouTube URL

Output：

- Audio (.mp3)

主要功能：

- Download
- Rename
- Save

---

## Module 2 — Transcript

Input：

- Audio

Output：

- Transcript.md

主要功能：

- Speech-to-Text
- Format
- Save

---

## Module 3 — Study Note

Input：

- Transcript

Output：

- StudyNote.md

主要功能：

- Prompt
- LLM
- Template
- Save

---

# 7. Runtime Flow

Module 間透過檔案串接：

```text
YouTube URL
        │
        ▼
Audio
        │
        ▼
Transcript
        │
        ▼
Study Note
```

每個 Module 皆遵循：

Read

↓

Process

↓

Write

---

# 8. State Flow

所有 Module 共用相同狀態：

```text
Waiting
        │
        ▼
Processing
        │
        ▼
Completed
        │
        ▼
Downloaded
```

若失敗：

```text
Processing
        │
        ▼
Error
        │
        ▼
Retry
```

---

# 9. Output Flow

Prototype 最終輸出：

```text
Output
│
├── Audio.mp3
│
├── Transcript.md
│
└── StudyNote.md
```

所有輸出皆可下載。

---

# 10. File Naming

Audio：

```
{VideoTitle}_{YouTubeID}.mp3
```

Transcript：

```
{VideoTitle}_{YouTubeID}_Transcript.md
```

Study Note：

```
{VideoTitle}_{YouTubeID}_StudyNote.md
```

全部由系統自動命名。

---

# 11. Future Workflow

未來 Workflow 將持續延伸：

```text
Study Note
        │
        ▼
Knowledge Card
        │
        ▼
SOP
        │
        ▼
Prompt Library
        │
        ▼
Skills
        │
        ▼
Agent
        │
        ▼
AI Product
        │
        ▼
Course
        │
        ▼
Business Model
```

Application Architecture 不需修改。

僅增加 Workflow Module。

---

# 12. Related Documents

- PRD.md
- Technical_Decision.md
- Workflow_Specification.md
- Application_Architecture_Blueprint_v2.0.md
- Wireframe_Specification_v2.0.md
- UI_Design_Pack_v1.0
- Google_AI_Studio_Build_Specification_v2.0.md

---

# Appendix A — Complete MVP Workflow

```text
                     User
                       │
                       ▼
             Paste YouTube URL
                       │
                       ▼
                Click Generate
                       │
                       ▼
               Audio Workflow
                       │
                       ▼
            Transcript Workflow
                       │
                       ▼
           Study Note Workflow
                       │
                       ▼
              Output Files (.md)
                       │
                       ▼
                  Download
                       │
                       ▼
                     Finish
```

---

# Document Summary

MVP_Single_Page_Workflow.md 定義 **YB Knowledge Factory MVP v0.1** 的核心產品流程。

本文件以「產品操作流程」為核心，描述使用者如何完成一次完整任務，以及系統如何依序執行 Audio、Transcript 與 Study Note 三個 Workflow。

它作為 **Application Architecture、Wireframe、Google AI Studio Build** 與 **Claude Code 實作** 之間的共同橋樑，確保所有開發階段遵循一致的產品流程。