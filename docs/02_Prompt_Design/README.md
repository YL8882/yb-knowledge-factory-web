# Prompt Design

**Module:** 02_Prompt_Design  
**Version:** v1.0 (Final)  
**Product:** YB Knowledge Factory MVP v0.1

---

# Overview

本模組負責管理 **YB Knowledge Factory** 所有 AI Prompt 的設計、開發、測試與版本管理。

Prompt 是整個產品的核心資產（Core Asset），直接決定 AI 輸出的品質、一致性與可維護性。

因此，本專案將 Prompt 視為產品的一部分，而非單純的提示詞。

---

# Objectives

本模組的目標：

- 建立可重複使用的 Prompt
- 建立一致的 Prompt 開發流程
- 建立 Prompt 版本管理
- 提高 AI 輸出品質
- 降低 Prompt 維護成本
- 支援未來多產品共用 Prompt 架構

---

# Development Principles

所有 Prompt 必須遵循：

```text
Workflow
        ↓
Template
        ↓
Output Schema
        ↓
System Prompt
        ↓
User Prompt
        ↓
Testing
        ↓
Release
```

Prompt 不應直接開始撰寫，而是依照上述流程逐步完成。

---

# Folder Structure

```text
02_Prompt_Design/
│
├── README.md
├── Prompt_Architecture.md
├── Prompt_Development_Guide.md
├── Prompt_Test_Plan.md
│
├── 01_System_Prompts/
├── 02_User_Prompts/
├── 03_Output_Schema/
├── 04_Examples/
└── 05_Prompt_Versions/
```

---

# Module Description

## Prompt_Architecture

定義 Prompt 整體架構。

包含：

- Prompt Flow
- Prompt Layer
- Input / Output 關係

---

## Prompt_Development_Guide

Prompt 撰寫規範。

包含：

- 撰寫原則
- 命名規範
- Markdown 規範
- Version 管理

---

## Prompt_Test_Plan

Prompt 驗證流程。

包含：

- 測試案例
- 驗收標準
- 品質檢查

---

## 01_System_Prompts

存放所有 System Prompt。

例如：

- StudyNote_System_Prompt_v1.0

---

## 02_User_Prompts

存放所有 User Prompt。

例如：

- StudyNote_User_Prompt_v1.0

---

## 03_Output_Schema

定義 AI 必須輸出的固定格式。

例如：

- StudyNote_Output_Schema.md

---

## 04_Examples

存放 Prompt 範例。

包含：

- Input Example
- Output Example
- Good Example
- Bad Example

---

## 05_Prompt_Versions

管理 Prompt 歷史版本。

包含：

- CHANGELOG
- Version History

---

# Prompt Lifecycle

所有 Prompt 均遵循以下生命週期：

```text
Requirement
      ↓
Design
      ↓
Development
      ↓
Testing
      ↓
Release
      ↓
Maintenance
```

---

# Current MVP

目前 MVP v0.1 僅開發一個 Prompt：

| Prompt ID | Name | Status |
|-----------|------|--------|
| Prompt-001 | StudyNote_Prompt_v1.0 | Active |

負責將：

```
Transcript.md
```

轉換為：

```
Study_Note.md
```

---

# Naming Convention

Prompt 建議採用以下命名：

```
<Function>_<PromptType>_v<Version>.md
```

例如：

```
StudyNote_System_Prompt_v1.0.md

StudyNote_User_Prompt_v1.0.md

StudyNote_Output_Schema_v1.0.md
```

---

# Design Principles

所有 Prompt 必須符合以下原則：

- Single Responsibility（單一職責）
- Structured Output（固定輸出格式）
- Markdown First
- Model Independent（不依賴特定模型）
- Easy to Maintain（易於維護）
- Version Controlled（版本管理）

---

# Future Expansion

未來將新增：

- Knowledge Card Prompt
- SOP Prompt
- Prompt Library Prompt
- Skills Prompt
- AI Product Prompt
- Course Prompt
- Business Model Prompt

所有 Prompt 將沿用相同的開發流程與設計規範。

---

# Related Documents

```
01_Product_Requirements/
├── PRD.md
├── Technical_Decision.md
├── Workflow_Specification.md
└── Prompt_Specification.md
```

---

# Document Status

| Item    | Value                         |
| ------- | ----------------------------- |
| Module  | Prompt Design                 |
| Version | v1.0 (Final)                  |
| Product | YB Knowledge Factory MVP v0.1 |
| Status  | ✅ Final                       |