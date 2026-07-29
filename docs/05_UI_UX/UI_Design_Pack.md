我建議正式把它定位成**產品設計文件**，而不是只有幾張圖片。

它將成為 **Claude Code、Google AI Studio、Figma、前端工程師** 共用的 UI 設計規格。

---

# UI Design Pack v1.0

**Version:** v1.0  
**Status:** Final  
**Owner:** YB  
**Product:** YB Knowledge Factory MVP v0.1  
**Document Type:** UI Design Package  
**Language:** Traditional Chinese  
**Last Updated:** 2026-07-23

---

# Purpose

本文件提供 **YB Knowledge Factory MVP** 的完整 UI 設計圖。

用途：

- Claude Code UI 開發
    
- Google AI Studio Prototype
    
- Figma UI 依據
    
- 前端開發
    
- MVP 驗證
    

---

# Design Philosophy

整個 MVP 採用：

- Single Page Workflow
    
- Workflow First
    
- MVP First
    
- Desktop First
    
- One Click Generate
    
- Every Step Visible
    
- Every Result Downloadable
    

---

# UI Design Pack Structure

```text
UI_Design_Pack_v1.0/

├── README.md
│
├── 01_Page_Layout.png
│
├── 02_Workflow_Diagram.png
│
├── 03_Navigation_Diagram.png
│
├── 04_Component_Map.png
│
├── 05_State_Flow.png
│
└── 06_User_Journey.png
```

---

# 01 Page Layout（頁面配置圖）

**Purpose**

展示 MVP 唯一畫面的完整配置。

包含：

- Header
    
- URL Input
    
- Generate Button
    
- Workflow Progress
    
- Audio Module
    
- Transcript Module
    
- Study Note Module
    
- Footer Tips
    

**閱讀對象**

- UI Designer
    
- Claude Code
    
- Frontend Developer
    

---

# 02 Workflow Diagram（工作流程圖）

**Purpose**

說明產品完整 AI Workflow。

流程：

```text
YouTube URL
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

同時說明：

- Audio Workflow
    
- Transcript Workflow
    
- Study Note Workflow
    
- Output Files
    
- File Naming
    
- Status Flow
    

---

# 03 Navigation Diagram（導覽圖）

**Purpose**

展示整個產品 Navigation。

MVP：

```text
Single Page
```

沒有：

- Dashboard
    
- Login
    
- Sidebar
    

未來版本：

```text
History

↓

Settings

↓

Templates
```

---

# 04 Component Map（元件配置圖）

**Purpose**

定義畫面所有 Component。

包含：

Header

Input Area

Workflow Progress

Workflow Modules

Footer

以及：

- Primary Button
    
- Status Indicator
    
- Stepper
    
- Module Card
    
- Download Button
    

Claude Code 可以直接 Mapping。

---

# 05 State Flow（狀態流程圖）

**Purpose**

定義所有 Workflow Module 的狀態。

所有 Module 共用：

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

適用：

- Audio
    
- Transcript
    
- Study Note
    

---

# 06 User Journey（使用者旅程）

**Purpose**

描述使用者從開始到完成的完整體驗。

Journey：

```text
Open App

↓

Paste URL

↓

Generate

↓

AI Processing

↓

Completed

↓

Download Files

↓

Finish
```

同時描述：

- Screen Changes
    
- User Goals
    
- User Emotions
    
- Pain Points
    
- Solutions
    

---

# Reading Order

建議閱讀順序：

```text
01
Page Layout

↓

02
Workflow

↓

03
Navigation

↓

04
Components

↓

05
State Flow

↓

06
User Journey
```

---

# Relationship

```text
PRD
│
├──────────────┐
│              │
▼              ▼

Workflow     Prompt

│              │

└──────┬───────┘

       ▼

UI Design Pack

│

├── Page Layout

├── Workflow

├── Navigation

├── Components

├── State Flow

└── User Journey

       │

       ▼

Claude Code

       │

       ▼

Web App MVP
```

---

# Folder Structure

建議正式建立如下目錄：

```text
01_YB_Knowledge_Factory_MVP_v0.1/
│
├── 01_Product_Requirements/
│
├── 02_Prompt_Design/
│
├── 03_Workflows/
│
├── 04_Templates/
│
├── 05_UI_UX/
│   │
│   ├── README.md
│   │
│   ├── Wireframe_Specification_v2.0.md
│   │
│   └── UI_Design_Pack_v1.0/
│       │
│       ├── README.md
│       ├── 01_Page_Layout.png
│       ├── 02_Workflow_Diagram.png
│       ├── 03_Navigation_Diagram.png
│       ├── 04_Component_Map.png
│       ├── 05_State_Flow.png
│       └── 06_User_Journey.png
│
└── 06_Google_AI_Studio/
```

---

# Final Deliverables

|No.|File|Purpose|
|---|---|---|
|01|**01_Page_Layout.png**|單頁 UI 配置圖|
|02|**02_Workflow_Diagram.png**|AI Workflow 流程圖|
|03|**03_Navigation_Diagram.png**|MVP 導覽架構圖|
|04|**04_Component_Map.png**|UI 元件配置與對照|
|05|**05_State_Flow.png**|Workflow 狀態轉換圖|
|06|**06_User_Journey.png**|使用者完整操作旅程|

---

## Final（正式定位）

這份 **UI Design Pack v1.0** 建議作為 **YB Knowledge Factory MVP v0.1** 的正式 UI 設計套件。它與 `Wireframe_Specification_v2.0.md` 的分工如下：

- **Wireframe_Specification_v2.0.md**：文字規格、元件定義、事件、State、實作規範。
    
- **UI Design Pack v1.0**：六張可視化設計圖，讓產品經理、設計師、Claude Code 與前端工程師快速理解產品結構與操作流程。
    

這樣可以形成「**文字規格 + 視覺設計**」的完整產品設計文件組。