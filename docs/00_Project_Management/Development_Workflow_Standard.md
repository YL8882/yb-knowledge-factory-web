---
Title: Development Workflow Standard
Version: v1.0
Status: Active
Owner: YB AI Product Factory
Last Updated: 2026-08-05
Document Type: Development Standard
Scope: All AI Products
---

# Development Workflow Standard

> Defines the standard development workflow for all AI Product Factory projects.

---

# 1. Purpose

建立一套可重複、可驗證、可持續改善的 AI 產品開發流程。

本標準適用於：

- YB Learn
- YB Knowledge Factory
- AI Market Research
- AI Real Estate
- 未來所有 AI Product Factory 專案

本文件規範：

- Task 開發流程
- Human Test 流程
- Acceptance 流程
- Commit 流程
- Bug 管理流程

---

# 2. Development Principles

所有開發皆遵循以下七項原則：

1. Proposal First
2. Scope Freeze
3. Code First
4. Test First
5. Record Second
6. Commit After Approval
7. Push After Approval

任何功能不得跳過上述流程。

---

# 3. Standard Development Workflow

```text
Task Proposal
      │
      ▼
Scope Freeze
      │
      ▼
Implementation
      │
      ▼
Self Test
      │
      ▼
Human Test
      │
      ▼
Acceptance Test Update
      │
      ▼
TODO / Backlog Update
      │
      ▼
CHANGELOG Update
      │
      ▼
Commit Scope Review
      │
      ▼
Git Commit
      │
      ▼
Git Push
      │
      ▼
Milestone Update（必要時）
```

---

# 4. Phase Definition

## Phase 1 — Proposal

開始任何開發之前，必須先提出 Proposal。

Proposal 至少包含：

- Task Goal
- Scope
- Out of Scope
- Human Test
- Commit Scope

未經確認不得開始實作。

---

## Phase 2 — Scope Freeze

Proposal 確認後即進入 Scope Freeze。

Scope Freeze 後：

- 不新增功能
- 不新增 Prompt
- 不新增 UI
- 不新增需求

若需新增功能，必須重新提出 Proposal。

---

## Phase 3 — Implementation

開始實作。

此階段：

可以：

- 修改程式
- Refactor（Scope 內）

不可：

- Commit
- 修改 Acceptance Test
- 修改 TODO（除非發現新問題）

---

## Phase 4 — Self Test

完成程式後，先由 AI 自行驗證。

包含：

- Unit Test
- API Test
- Mock Test
- Node Test（依產品）

確認：

- Happy Path 正常
- Regression 無異常

---

## Phase 5 — Human Test

AI 必須提供：

- Human Test Steps
- 預期結果
- PASS / FAIL 判定方式

Human Test 必須由使用者實際操作。

---

## Phase 6 — Acceptance Test

Acceptance Test 必須依據：

Human Test 的實際結果更新。

不得：

- 預先填寫 PASS
- 依推測填寫結果
- 使用模擬結果代替 Human Test

正式原則：

> Test First → Record Second

---

## Phase 7 — TODO / Backlog

若開發過程中發現：

- Bug
- Enhancement
- Technical Debt
- Future Idea

全部加入：

TODO.md

不得：

為單一 Bug 建立獨立文件。

---

## Phase 8 — CHANGELOG

Task 完成後：

更新 CHANGELOG。

內容包含：

- 新功能
- 修改內容
- 修正內容

不記錄開發中的暫時變更。

---

## Phase 9 — Commit Scope Review

Commit 前，

AI 必須列出：

- Modified Files
- New Files
- Excluded Files

等待使用者確認。

未經確認不得 Commit。

---

## Phase 10 — Git Commit

Commit 後，

必須回報：

- Commit Hash
- Commit Message
- git status
- 是否領先 origin/main

---

## Phase 11 — Git Push

只有在使用者確認後，

才允許 Push。

---

# 5. Human Test Standard

Human Test 必須包含：

- 測試目的
- 測試步驟
- 預期結果
- PASS / FAIL
- Observation

不得僅提供：

- Node 測試
- Mock 測試
- 理論推論

---

# 6. Happy Path vs Error Path

每個 Sprint 必須區分：

## Happy Path

本 Sprint 必須完成。

例如：

- 正常建立 Study Note
- 正常建立 Learning Blueprint
- 正常 Renderer

---

## Error Path

例如：

- API Timeout
- Rate Limit
- Gemini Error
- Retry Strategy

若不影響主流程：

加入 TODO，

後續 Sprint 處理。

不得擴大目前 Sprint Scope。

---

# 7. Bug Management

Bug 發現流程：

```text
Development

↓

Found Bug

↓

TODO.md

↓

Engineering Backlog

↓

Future Sprint
```

Bug 不應直接中斷目前 Sprint。

---

# 8. Commit Standard

每次 Commit：

只能包含：

本 Task 的修改。

不得順便：

- Refactor 其它模組
- 修改 UI（Scope 外）
- 修改 Prompt（Scope 外）
- 修改文件（Scope 外）

---

# 9. Required Outputs

每完成一個 Task，

至少更新：

- TODO.md（若有新增）
- Acceptance_Test.md
- CHANGELOG.md

必要時：

- Milestone
- Design Proposal

---

# 10. Definition of Done

Task 完成必須符合：

- Proposal 已確認
- Scope 未擴張
- Implementation 完成
- Self Test 通過
- Human Test 完成
- Acceptance Test 更新
- TODO 更新
- CHANGELOG 更新
- Commit Scope 已確認
- Git Commit 完成

以上全部完成，

Task 才視為 Done。

---

# 11. Future Improvements

未來可加入：

- CI/CD Workflow
- Automated Testing
- Pull Request Review Standard
- Release Workflow
- Versioning Standard

本文件持續維護，但所有修改需經 Scope Review。