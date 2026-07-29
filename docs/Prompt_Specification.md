---
Version: v2.0
Status: Final
Owner: YB
Document: Prompt Specification
Category: Prompt Engineering Blueprint
Purpose: Define the standard prompt architecture, engineering principles, lifecycle, and evaluation framework for all AI Products.
Scope: All AI Products
Priority: Critical
Author: ChatGPT
Last Updated: 2026-07-29
Related Documents:
  - Development_Operating_System.md
  - Product_Architecture.md
  - Workflow_Specification.md
  - Runtime_Specification.md
  - Output_Specification.md
  - Documentation_Standard.md
---

# Prompt Specification

> Standard Prompt Engineering Blueprint for AI Product Factory

---

# 1. Purpose

本文件定義 AI Product 的 Prompt Engineering 標準。

目的：

- 建立一致的 Prompt 架構
- 提高 Prompt 可維護性
- 提高 Prompt 可重複使用性
- 降低 Token 成本
- 提高 AI Output 穩定性
- 建立 Prompt 全生命週期管理

本文件描述：

- Prompt 如何設計
- Prompt 如何組裝
- Prompt 如何管理
- Prompt 如何評估

不描述：

- 個別 Prompt 內容
- Workflow
- Runtime
- Business Logic

---

# 2. Prompt Engineering Principles

所有 Prompt 必須遵循：

| Principle | Description |
|------------|-------------|
| Single Responsibility | 一個 Prompt 只完成一件事 |
| Modular | 模組化 |
| Reusable | 可重複使用 |
| Composable | 可自由組裝 |
| Predictable | Output 穩定 |
| Context Efficient | 最小 Context |
| Maintainable | 易維護 |
| Testable | 可測試 |
| Versioned | 可版本管理 |
| Specification Driven | 依 Specification 建立 |

---

# 3. Prompt Layer Architecture

所有 Prompt 採四層架構：

```
System Prompt

↓

Developer Prompt

↓

Runtime Prompt

↓

User Prompt
```

---

## System Prompt

定義：

AI 長期規則。

例如：

- AI Identity
- Safety
- Global Rules

---

## Developer Prompt

定義：

產品邏輯。

例如：

Study Note Generator

Knowledge Card Builder

Translator

---

## Runtime Prompt

由程式：

動態組裝。

例如：

- Metadata
- Transcript
- Settings
- User Preferences

---

## User Prompt

使用者：

即時輸入。

例如：

問題

網址

需求

---

# 4. Prompt Architecture

每個 Prompt：

固定結構：

```
Role

↓

Goal

↓

Input

↓

Context

↓

Constraints

↓

Instructions

↓

Output Format

↓

Examples（Optional）
```

---

# 5. Prompt Assembly Workflow

大型任務：

由多個 Prompt 組成。

```
Transcript Prompt

↓

Study Note Prompt

↓

Knowledge Card Prompt

↓

Output Prompt
```

Application Layer：

負責：

Prompt Assembly。

AI：

只執行：

目前 Prompt。

---

# 6. Prompt Lifecycle

所有 Prompt：

遵循：

```
Draft

↓

Testing

↓

Review

↓

Accepted

↓

Frozen

↓

Deprecated
```

Accepted：

正式採用。

Frozen：

不可修改。

需要修改：

建立：

新版本。

---

# 7. Prompt Context Management

遵循：

Development Operating System。

## Small Context

只提供：

目前需要資訊。

---

## Progressive Context

Context：

依 Workflow

逐步增加。

---

## Reference First

引用：

Specification。

不要：

重貼內容。

---

## Single Source of Truth

PRD

Workflow

Architecture

不得重複。

---

# 8. Prompt Composition

Prompt：

可自由組合。

```
Input Prompt

+

Processing Prompt

+

Reasoning Prompt

+

Output Prompt
```

避免：

巨大 Prompt。

---

# 9. Prompt Folder Structure

```
prompts/

README.md

Prompt_01_Transcript.md

Prompt_02_Study_Note.md

Prompt_03_Knowledge_Card.md

Prompt_04_SOP.md

Prompt_05_Output.md

Prompt_Templates/

Prompt_Tests/
```

---

# 10. Prompt Versioning

命名：

```
Prompt_02_Study_Note_v1.0.md

↓

Prompt_02_Study_Note_v1.1.md

↓

Prompt_02_Study_Note_v2.0.md
```

版本：

不得覆蓋。

保留：

歷史版本。

---

# 11. Prompt Evaluation Standard

每個 Prompt：

評估：

| Metric | Description |
|----------|-------------|
| Accuracy | 正確性 |
| Consistency | 一致性 |
| Stability | 穩定性 |
| Token Cost | Token 成本 |
| Context Cost | Context 成本 |
| Reusability | 可重用 |
| Maintainability | 易維護 |
| Output Quality | 輸出品質 |

---

# 12. Prompt Quality Checklist

每個 Prompt：

□ Role

□ Goal

□ Input

□ Context

□ Constraints

□ Instructions

□ Output

□ Version

□ Test

□ Review

---

# 13. Success Criteria

Prompt Engineering 成功代表：

- Output 穩定
- Token 成本低
- Context 最小
- 可組裝
- 可維護
- 可測試
- 可重複使用
- 易於 AI 理解

---

# Design Principles

Prompt Specification 定義：

- Prompt Architecture
- Prompt Layers
- Prompt Lifecycle
- Prompt Composition
- Prompt Versioning
- Prompt Evaluation

Prompt 的實際內容應放置於：

```
prompts/
```

每個 Prompt：

保持：

單一責任。

模組化。

低 Token。

最小 Context。

---
End of Document