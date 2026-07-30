---
Version: v1.0
Status: Final
Owner: YB
Document: Product Index
Category: Product Requirements
Purpose: Provide a single entry point for understanding the product structure, specifications, and document reading order.
Scope: Current Product
Priority: Critical
Author: ChatGPT
Last Updated: 2026-07-30
Related Documents:
  - 01_Product_Requirements/Core/PRD.md
  - 01_Product_Requirements/Core/Product_Architecture.md
  - 01_Product_Requirements/Core/Workflow_Specification.md (repository-level; see 03_Workflows/Workflow_Specification.md for detailed implementation)
  - 02_Prompt_Design/Prompt_Specification.md
  - 01_Product_Requirements/Core/Runtime_Specification.md
  - 01_Product_Requirements/Core/Output_Specification.md
  - 01_Product_Requirements/UI/UI_Component_Specification.md
  - 01_Product_Requirements/UI/Wireframe_Specification.md (product-level; see 05_UI_UX/Wireframe_Specification.md for engineering implementation)
---

# Product Index

> Product Navigation Center

---

# Purpose

Product Index 是本產品所有設計文件的入口。

目的：

- 提供產品總覽
- 建立文件閱讀順序
- 說明各文件責任
- 幫助 AI 快速建立 Product Context
- 避免重複閱讀不必要文件

本文件不描述：

- Product Requirement
- Workflow
- Prompt
- Runtime
- UI Design

僅作為導航文件。

---

# Product Overview

Product Name

YB Knowledge Factory MVP

Current Version

v0.1

Current Stage

MVP Development

Product Goal

將 YouTube 影片快速轉換為：

- Transcript
- Study Note
- Knowledge Assets

---

# Document Reading Order

所有 AI Coding Agent 建議依照以下順序閱讀：

```
PRD

↓

Product Architecture

↓

Workflow Specification

↓

Prompt Specification

↓

Runtime Specification

↓

Output Specification

↓

UI Component Specification

↓

Wireframe Specification

↓

Current Milestone

↓

Coding
```

---

# Product Specifications

| Document | Purpose |
|----------|---------|
| 01_Product_Requirements/Core/PRD.md | 定義產品需求與 MVP 範圍 |
| 01_Product_Requirements/Core/Product_Architecture.md | 定義產品架構、模組與能力 |
| 01_Product_Requirements/Core/Workflow_Specification.md | 定義資料流程與工作流程（Repository-level，抽象概觀） |
| 03_Workflows/Workflow_Specification.md | 詳細工作流程實作（Step-by-step，含 Exception Handling） |
| 02_Prompt_Design/Prompt_Specification.md | 定義 Prompt Engineering 標準 |
| 01_Product_Requirements/Core/Runtime_Specification.md | 定義系統執行方式 |
| 01_Product_Requirements/Core/Output_Specification.md | 定義輸出格式與品質 |
| 01_Product_Requirements/UI/UI_Component_Specification.md | 定義 UI 元件 |
| 01_Product_Requirements/UI/Wireframe_Specification.md | 定義畫面配置與資訊架構（Product-level，抽象概觀） |
| 05_UI_UX/Wireframe_Specification.md | 詳細 UI Wireframe 實作（含實際畫面配置與設計稿） |

---

# Product Structure

```
Product

├── Requirements

├── Architecture

├── Workflow

├── Prompt

├── Runtime

├── Output

└── UI
```

---

# Development Flow

```
Product Idea

↓

PRD

↓

Architecture

↓

Workflow

↓

Prompt

↓

Prototype

↓

Implementation

↓

Testing

↓

Release
```

---

# Current Product Scope

Current MVP

✓ YouTube URL

✓ Transcript

✓ Study Note

✓ Markdown Export

Future Version

- Knowledge Card
- Prompt Library
- SOP Generator
- Browser Extension
- Multi-source Import

---

# Related Documents

## Project Management

- Development_Operating_System.md
- Project_Dashboard.md

---

## Product Requirements

- 01_Product_Requirements/Core/PRD.md
- 01_Product_Requirements/Core/Product_Architecture.md
- 01_Product_Requirements/Core/Workflow_Specification.md (repository-level; see 03_Workflows/Workflow_Specification.md for detailed implementation)
- 02_Prompt_Design/Prompt_Specification.md
- 01_Product_Requirements/Core/Runtime_Specification.md
- 01_Product_Requirements/Core/Output_Specification.md
- 01_Product_Requirements/UI/UI_Component_Specification.md
- 01_Product_Requirements/UI/Wireframe_Specification.md (product-level; see 05_UI_UX/Wireframe_Specification.md for engineering implementation)

---

## Development

- Current Milestone
- Testing
- Release Notes

---

# AI Startup Guide

建議所有 AI Coding Agent：

1. 閱讀 Product Index
2. 閱讀 PRD
3. 閱讀 Product Architecture
4. 閱讀 Workflow Specification
5. 閱讀 Prompt Specification
6. 閱讀目前 Milestone
7. 開始開發

---

# Design Principles

Product Index 的目的：

- 提供產品導航
- 建立閱讀順序
- 快速建立 Context
- 避免重複閱讀
- 提高 AI 開發效率

本文件僅負責導航，不重複任何 Specification 的內容。

---
End of Document