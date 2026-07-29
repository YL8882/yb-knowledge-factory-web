我重新檢視了我們這一個月建立的所有文件，我認為 **Application Architecture Blueprint** 應該提升到**產品最高層級的設計文件**。

它不應該再描述畫面，而是描述：

> **整個產品如何運作。**

因此，我建議定稿如下。

---

# Application_Architecture_Blueprint_v2.0.md (Final)

```yaml
Title: Application Architecture Blueprint
Version: v2.0
Status: Final
Owner: YB
Product: YB Knowledge Factory MVP v0.1
Document Type: Product Architecture Specification
Language: Traditional Chinese
Last Updated: 2026-07-23
```

---

# 1. Purpose

本文件定義 **YB Knowledge Factory MVP v0.1** 的整體產品架構（Application Architecture）。

用途：

- 作為 Claude Code 開發依據
    
- 作為 Google AI Studio Prototype 建立依據
    
- 作為產品架構設計文件
    
- 作為 MVP 驗證依據
    

本文件描述：

- System Architecture
    
- Information Architecture
    
- Workflow Architecture
    
- Runtime Architecture
    
- Data Flow
    
- Module Architecture
    
- User Journey
    

本文件不描述：

- UI 視覺設計
    
- Prompt 細節
    
- Workflow 細部實作
    

---

# 2. Architecture Principles

整個 MVP 採用以下設計原則。

---

## Workflow First

產品只負責完成一件事情：

```text
YouTube URL

↓

Study Note
```

所有設計圍繞 Workflow。

---

## Single Page

整個 MVP 只有：

```text
One Page

One Workflow

One Result
```

避免複雜導覽。

---

## One Job

一次只處理：

```text
一個 YouTube URL
```

不支援 Batch。

---

## Desktop First

優先 Desktop。

Mobile 不列入 MVP。

---

## Auto Pipeline

Generate 後：

全部流程自動完成。

使用者不需要介入。

---

## File Driven

所有 Workflow 都以檔案為核心。

```text
Audio

↓

Transcript

↓

Study Note
```

---

# 3. System Architecture

## Overall Architecture

```text
                     User
                       │
                       ▼
          ┌────────────────────────┐
          │ Single Page Web App    │
          └────────────┬───────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │ Workflow Controller    │
          └────────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 ┌────────────┐ ┌────────────┐ ┌────────────┐
 │ Audio      │ │ Transcript │ │ Study Note │
 │ Workflow   │ │ Workflow   │ │ Workflow   │
 └────────────┘ └────────────┘ └────────────┘
        │              │              │
        └──────────────┼──────────────┘
                       ▼
             Output Files (.mp3/.md)
```

---

# 4. Information Architecture

MVP 採用 Single Page Architecture。

```text
Application

│

├── Header

├── Input Area

├── Workflow Progress

├── Audio Module

├── Transcript Module

├── Study Note Module

└── Footer
```

沒有：

- Dashboard
    
- Sidebar
    
- Login
    
- Multi Page
    

---

# 5. Application Layout

整個 Application 採固定排列。

```text
Header

↓

YouTube URL

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

Footer Tips
```

畫面配置依據：

> UI Design Pack v1.0

---

# 6. Workflow Architecture

Workflow 為 MVP 核心。

```text
Paste URL

↓

Generate

↓

Download Audio

↓

Generate Transcript

↓

Generate Study Note

↓

Download Results

↓

Finish
```

每一步完成後自動執行下一步。

---

# 7. Module Architecture

## Audio Module

負責：

```text
YouTube

↓

Download Audio

↓

Rename

↓

Save

↓

Download
```

輸出：

```text
影片名稱_YouTubeID.mp3
```

---

## Transcript Module

負責：

```text
Audio

↓

Speech To Text

↓

Transcript Template

↓

Save

↓

Download
```

輸出：

```text
影片名稱_YouTubeID_Transcript.md
```

---

## Study Note Module

負責：

```text
Transcript

↓

Study Note Prompt

↓

LLM

↓

Study Note Template

↓

Save

↓

Download
```

輸出：

```text
影片名稱_YouTubeID_StudyNote.md
```

---

# 8. Runtime Architecture

Runtime 採 Pipeline。

```text
YouTube URL

↓

Video Metadata

↓

Audio

↓

Transcript

↓

Study Note

↓

Output Folder
```

所有 Runtime 都採：

```text
Read

↓

Process

↓

Write
```

每個 Module 只負責自己的 Input / Output。

---

# 9. Data Flow

Data 永遠單向流動。

```text
YouTube URL

↓

Video Metadata

↓

Audio File

↓

Transcript File

↓

Study Note File

↓

Download
```

禁止逆向修改。

避免流程耦合。

---

# 10. State Flow

所有 Module 共用 State Machine。

```text
Waiting

↓

Processing

↓

Completed

↓

Downloaded
```

若失敗：

```text
Processing

↓

Error

↓

Retry

↓

Waiting
```

所有 Module 使用一致狀態。

---

# 11. User Journey

```text
Open App

↓

Paste YouTube URL

↓

Generate

↓

Processing

↓

Completed

↓

Download Files

↓

Finish
```

使用者只做：

- 貼網址
    
- 點 Generate
    
- 下載結果
    

其餘全部自動完成。

---

# 12. Output Architecture

最終產生：

```text
Output

│

├── Audio

│      └── *.mp3

│

├── Transcript

│      └── *.md

│

└── Study Note

       └── *.md
```

所有檔案皆：

- 自動命名
    
- 可下載
    
- 可保存
    

---

# 13. Future Architecture

後續只增加 Module。

```text
Study Note

↓

Knowledge Card

↓

SOP

↓

Prompt Library

↓

Skills

↓

Agent

↓

AI Product

↓

Course

↓

Business Model
```

Application 不需重新設計。

---

# 14. Related Documents

- PRD.md
    
- Technical_Decision.md
    
- Workflow_Specification.md
    
- Prompt_Specification.md
    
- Wireframe_Specification_v2.0.md
    
- UI_Design_Pack_v1.0
    
- Google_AI_Studio_Build_Specification.md
    
- Prototype_Test_Checklist.md
    

---

# Appendix A — Complete Architecture Overview

```text
                    User
                      │
                      ▼
             Single Page Web App
                      │
                      ▼
             Workflow Controller
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     Audio       Transcript    Study Note
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                Output Files
                      │
                      ▼
                  Download
```

---

# Architecture Summary

本架構以 **Workflow** 為核心，而非以頁面為核心。

產品定位為：

> **Single Page + One Job + Auto Pipeline + File Driven**

整個 MVP 只有一個工作流程：

> **貼上 YouTube 網址 → 自動完成 Audio → Transcript → Study Note → 下載成果。**

未來若增加 Knowledge Card、SOP、Prompt Library、Skills、Agent 等功能，只需在 Pipeline 後方新增 Workflow Module，而不需要重新設計 Application Architecture，讓 MVP 能自然演進為完整的 **YB Knowledge Factory**。