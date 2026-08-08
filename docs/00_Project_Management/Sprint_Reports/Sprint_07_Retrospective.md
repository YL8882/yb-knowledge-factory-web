---
Version: 1.0
Status: Final
Owner: YB Learn
Last Updated: 2026-08-05
Document Type: Sprint Retrospective
Sprint: Sprint 7
---

# Sprint 7 Retrospective

## Sprint Overview

Sprint 7 的目標是完成 **Learning Package** 的核心學習模組，讓使用者不只是取得影片摘要，而是建立完整的學習閉環（Learning Loop）。

本 Sprint 共完成四個主要功能：

- Learning Blueprint
- Teach Back
- Action List
- Review（Active Recall）

並完成多次 Human Test、Acceptance Test、Git Commit 與正式 Push。

---

# Sprint Goal

建立完整的 Learning Package MVP，使使用者可以從影片內容快速完成：

```text
理解
↓

輸出

↓

實作

↓

回憶
```

形成真正的學習流程，而不是只有 AI 摘要。

---

# Completed Features

## Task 4 — Learning Blueprint

### 完成內容

- Learning Blueprint Generator
- Learning Blueprint Preview
- Markdown Download
- Learning Blueprint API
- Queue 整合

### 成果

將影片內容整理成具有學習架構的 Blueprint，作為後續所有功能的共同基礎。

---

## Task 5 — Teach Back

### 完成內容

- Teach Back Generator
- Explain in Your Own Words
- Dynamic Checklist
- Practice Questions
- Reflection
- Markdown Download

### 成果

導入 Teach Back Method，協助使用者確認是否真正理解，而非僅閱讀內容。

---

## Task 6 — Action List

### 完成內容

- AI Action List Generator
- Today Action List
- Markdown Download
- Preview

### 成果

將影片內容轉換為可立即執行的行動，提高知識轉化為實作的效率。

---

## Task 7 — Review

### 完成內容

- Active Recall Review Generator
- One Sentence Recall
- Recall Questions
- Workflow Recall
- Reflection
- Show / Hide Reference Answer
- Markdown Download

### 成果

建立主動回憶（Active Recall）流程，幫助使用者檢查長期記憶，而不是重新閱讀內容。

---

# Final Learning Workflow

Sprint 7 完成後，Learning Package 已形成完整流程：

```text
YouTube URL

↓

Transcript

↓

Learning Blueprint

↓

Study Note

↓

Teach Back

↓

Action List

↓

Review

↓

Markdown Download
```

---

# Human Testing Summary

## 已完成驗證

- Transcript
- Learning Blueprint
- Study Note
- Teach Back
- Action List
- Review
- Markdown Download
- Preview UI
- Queue Flow

皆已完成 Human Test。

---

# Git Summary

Sprint 7 採用固定開發流程：

```text
Proposal

↓

Implementation

↓

Human Test

↓

Commit（No Push）

↓

Integration Test

↓

Push
```

所有 Task 均遵循相同流程。

---

# What Went Well

## 1. Feature First

本 Sprint 未提前進行大型 Refactor。

新功能完成後再考慮共用化，大幅降低 Regression Risk。

---

## 2. 模組高度獨立

每個功能皆具有：

- 獨立 API
- 獨立 Markdown
- 獨立 Generator
- 獨立 Download

降低模組間耦合。

---

## 3. Commit Discipline

所有 Task 均：

- Human Test
- Commit
- 不立即 Push

最後再完成 Integration Test 後 Push。

Git History 清楚且容易回溯。

---

## 4. MVP 控制良好

未加入：

- Database
- User Account
- Memory
- Gamification
- Dashboard
- Review History

保持 MVP 精簡。

---

# Challenges

Sprint 7 過程中主要挑戰：

- Gemini Error Path 尚未完整強化
- Structure Detection 一致性仍可提升
- Browser Console 必須人工驗證
- Claude CLI 無法驗證瀏覽器互動

---

# Decisions Made

本 Sprint 確立以下重要開發原則：

## Feature First, Refactor Later

功能完成優先。

架構整理留待未來 Refactor Sprint。

---

## Independent Module

所有 Learning Module：

- Learning Blueprint
- Teach Back
- Action List
- Review

皆採獨立設計。

---

## Markdown First

所有輸出皆採 Markdown。

方便：

- Preview
- Download
- Obsidian
- Git Versioning

---

## Human Verification Before Push

正式 Push 前必須：

- Human Test
- Integration Test

避免未驗證程式進入 Main。

---

# Known Issues

目前已知問題：

- Gemini Error Path 可再強化
- Structure Detection 穩定性可提升

上述問題皆已列入 Backlog，不影響 MVP 使用。

---

# Technical Debt

目前暫緩事項：

- 共用 Generator 整理
- extract_blueprint_items() 共用化
- Prompt 共用 Builder
- Markdown Renderer 共用
- Download Helper 共用

依照 Feature First 原則，未於 Sprint 7 提前重構。

---

# Lessons Learned

本 Sprint 最大收穫：

- Proposal → Human Review → Implementation 可大幅降低返工。
- 小步驟 Commit 能降低風險並提高可回溯性。
- Feature 與 Refactor 分離，可有效避免 Regression。
- 以 Learning Blueprint 為核心建立其他模組，可保持架構一致。

---

# Product Outcome

Sprint 7 完成後，YB Learn 已具備四項核心學習能力：

- 理解（Study Note）
- 輸出（Teach Back）
- 行動（Action List）
- 回憶（Review）

形成完整的學習閉環，成為產品的重要差異化能力。

---

# Sprint 8 Priorities

建議 Sprint 8 聚焦於：

1. UI / UX 優化
2. Learning Package 整合體驗
3. Error Handling 強化
4. Performance Optimization
5. 使用者操作流程優化
6. Beta User Feedback 收集

避免立即新增大量功能。

---

# Overall Evaluation

## Sprint Status

✅ Completed Successfully

## MVP Stability

⭐⭐⭐⭐⭐

## Architecture Quality

⭐⭐⭐⭐⭐

## Human Test

PASS

## Integration Test

PASS

## Production Readiness

Ready for Continued Development

---

# Closing Summary

Sprint 7 成功建立 YB Learn 的第一個完整 Learning Package MVP。

產品已不再只是 AI 摘要工具，而是具備：

- 理解（Understand）
- 教學（Teach）
- 行動（Act）
- 回憶（Recall）

四個核心能力的 AI 學習系統。

這將作為後續 Sprint 8 及未來功能擴充的重要基礎。