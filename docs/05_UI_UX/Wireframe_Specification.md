
---
Title: Wireframe Specification
Version: v3.0
Status: Final
Owner: YB
Product: YB Knowledge Factory MVP v0.1
Document Type: UI Structure Specification
Language: Traditional Chinese
Last Updated: 2026-07-24
---

# Wireframe Specification

## 1. Purpose

本文件定義 **YB Knowledge Factory MVP v0.1** 的 UI 畫面結構（Wireframe），作為 Prototype、Google AI Studio 與前端開發的共同依據。

本文件包含：

- Information Architecture
- Screen Layout
- Wireframe
- UI Components
- Navigation
- Workflow Overview
- Responsive Design

本文件不包含：

- UI 行為（Behavior）
- Validation Rules
- State Management
- Error Handling
- API Design
- Prompt Design
- Backend Workflow

上述內容由 **UI_Behavior_Specification.md** 與其他相關文件負責。

---

# 2. Design Principles

本產品 UI 設計遵循以下原則：

- MVP First
- Simple UI
- Desktop First
- Wizard Flow
- Single Responsibility
- Context Efficiency
- One Screen One Task

---

# 3. Information Architecture

```text
                Home
                  │
                  ▼
            Processing
                  │
                  ▼
               Result

        ┌──────────────┐
        │ Future (V1.1)│
        ├──────────────┤
        │ History      │
        │ Settings     │
        └──────────────┘
```

目前 MVP 僅包含：

- Home
- Processing
- Result

History 與 Settings 保留至 V1.1。

---

# 4. Screen Specifications

## 4.1 Home

### Purpose

建立新的知識整理任務。

### Layout

```text
+------------------------------------------------+

            YB Knowledge Factory

--------------------------------------------------

 YouTube URL

 [________________________________________]

 Output Folder

 [________________________________________]

             [ Generate ]

 Status : Ready

+------------------------------------------------+
```

### Components

- Product Title
- YouTube URL Input
- Output Folder
- Generate Button
- Status

### User Interaction

```text
輸入 YouTube URL
        │
        ▼
點擊 Generate
        │
        ▼
切換至 Processing
```

---

## 4.2 Processing

### Purpose

執行完整知識整理 Workflow。

### Layout

```text
+------------------------------------------------+

 Processing...

--------------------------------------------------

 Progress

 ███████□□□□□□

 Current Step

 Download Transcript

 Workflow

✓ Transcript

⏳ Study Note

□ Save

+------------------------------------------------+
```

### Components

- Progress Bar
- Current Step
- Workflow Status
- Status Message

### User Interaction

```text
開始 Workflow
      │
      ▼
執行所有步驟
      │
      ▼
切換至 Result
```

---

## 4.3 Result

### Purpose

查看並下載產出結果。

### Layout

```text
+------------------------------------------------+

 Result

--------------------------------------------------

 Transcript Preview

----------------------------

 Study Note Preview

----------------------------

[ Download Transcript ]

[ Download Study Note ]

[ Open Folder ]

+------------------------------------------------+
```

### Components

- Transcript Preview
- Study Note Preview
- Download Transcript
- Download Study Note
- Open Folder

### User Interaction

```text
預覽結果
     │
     ▼
下載檔案
     │
     ▼
完成
```

---

## 4.4 Future Screens（V1.1）

預留未來功能：

- History
- Settings

不屬於 MVP 範圍。

---

# 5. Components

| Component | Purpose | Screen |
|------------|----------|--------|
| Product Title | 顯示產品名稱 | Home |
| YouTube URL Input | 輸入影片網址 | Home |
| Output Folder | 選擇輸出位置 | Home |
| Generate Button | 啟動 Workflow | Home |
| Status | 顯示目前狀態 | Home |
| Progress Bar | 顯示執行進度 | Processing |
| Current Step | 顯示目前步驟 | Processing |
| Workflow Status | 顯示 Workflow 執行情況 | Processing |
| Status Message | 顯示提示訊息 | Processing |
| Transcript Preview | 預覽逐字稿 | Result |
| Study Note Preview | 預覽 Study Note | Result |
| Download Transcript | 下載逐字稿 | Result |
| Download Study Note | 下載 Study Note | Result |
| Open Folder | 開啟輸出資料夾 | Result |

---

# 6. Navigation

```text
Home
   │
   ▼
Processing
   │
   ▼
Result
```

MVP 採單向流程，不提供跨頁跳轉。

---

# 7. Workflow Overview

畫面對應的 Workflow 如下：

```text
Paste YouTube URL
        │
        ▼
Generate
        │
        ▼
Download Audio
        │
        ▼
Transcript
        │
        ▼
Study Note
        │
        ▼
Save Files
        │
        ▼
Result
        │
        ▼
Download
```

完整 Workflow 請參考：

**Workflow_Specification.md**

---

# 8. Responsive Design

| Device | Support |
|---------|----------|
| Desktop | ✅ Primary |
| Tablet | ✅ Basic Support |
| Mobile | ⏳ Planned (V1.1) |

MVP 採 **Desktop First** 設計。

---

# 9. Design Notes

設計原則：

- 單欄式 Layout
- 不使用 Sidebar
- 不使用 Dashboard
- 一個畫面只完成一項主要任務
- 操作流程保持線性
- UI 簡潔、降低學習成本
- 優先支援 Prototype 驗證

---

# 10. Related Documents

本文件與下列文件共同構成 UI 規格：

- PRD.md
- Technical_Decision.md
- Workflow_Specification.md
- Prompt_Specification.md
- UI_Behavior_Specification.md
- Google_AI_Studio_Application_Architecture_Blueprint.md
- Prototype_Test_Checklist.md

---

# Appendix A

## Complete User Journey

```text
Home

↓

Paste YouTube URL

↓

Generate

↓

Processing

↓

Transcript

↓

Study Note

↓

Save Output

↓

Result

↓

Download

↓

Finish
```

---