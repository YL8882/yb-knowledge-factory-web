---
Version: v2.0
Status: Final
Owner: YB
Document: Development Operating System
Category: Project Management
Purpose: Define the standard operating system for developing AI Products.
Scope: All AI Products
Priority: Critical
Author: ChatGPT
Last Updated: 2026-07-29
Related Documents:
  - README.md
  - CLAUDE.md
  - Documentation_Standard.md
  - Product_Architecture.md
  - PRD.md
  - Workflow_Specification.md
  - Prompt_Specification.md
---

# Development Operating System

> **The Development Constitution of AI Product Factory**

---

# 1. Purpose

本文件定義 AI Product Factory 的標準開發制度。

所有 AI Product 必須遵循本文件。

本文件不描述產品功能，而是定義：

- 如何開發產品
- 如何管理 AI Context
- 如何管理文件
- 如何管理 Milestone
- 如何降低開發成本
- 如何建立一致性的 AI Product

---

# 2. Principle Zero

## Build Before Discuss

當功能可以透過 MVP 驗證時：

優先建立

↓

驗證

↓

改善

避免過度設計。

原則：

```
Build

↓

Validate

↓

Improve
```

而不是：

```
Discuss

↓

Discuss

↓

Discuss

↓

Coding
```

---

# 3. Core Principles

所有 AI Product 必須遵循以下原則。

| Principle | Description |
|------------|-------------|
| Product First | 產品價值優先 |
| MVP First | 優先完成 MVP |
| Workflow First | 先驗證 Workflow |
| Specification First | 規格先於程式 |
| Build Before Discuss | 能做就先驗證 |
| Small Milestones | 小步快速迭代 |
| Continuous Improvement | 持續改善 |
| Reusable Design | 可重複使用 |
| AI Collaboration | AI 分工合作 |
| Simplicity First | 保持簡潔 |

---

# 4. AI Responsibilities

## Standard AI Roles

| AI | Responsibility |
|----|----------------|
| Product Owner | Product Vision、Decision、Approval |
| ChatGPT | Architecture、PRD、Workflow、Prompt、Review |
| Claude Code | Coding、Refactor、Debug、Testing |
| Google AI Studio | Prototype、UI、Prompt Validation |
| Gemini | Analysis、Research、Large Context |
| Future AI Agents | Follow Specification |

原則：

AI 不應超出自身職責。

---

# 5. Standard Development Workflow

所有產品皆遵循固定流程。

```
Idea

↓

Product Architecture

↓

PRD

↓

Workflow

↓

Prompt

↓

Prototype

↓

Milestone

↓

Implementation

↓

Testing

↓

Review

↓

Git Commit

↓

Next Milestone
```

禁止：

直接 Coding。

---

# 6. AI Resource Economy

AI Product 的核心不是節省 Token。

而是有效管理 AI 資源。

AI Resource Economy 包含：

```
AI Resources

├── Token Economy

├── Context Economy

├── Conversation Economy

└── Documentation Economy
```

---

# 6.1 Token Economy

目標：

降低 Token 消耗。

Principles：

- 使用精簡 Prompt
- 避免重複內容
- 引用文件
- 不重新生成已定稿內容
- 保持最小輸入

---

# 6.2 Context Economy

Context 是 AI 最重要的資源。

Principles：

## Small Context

只提供完成目前工作需要的 Context。

不要：

一次提供全部文件。

---

## Progressive Context

Context 應隨 Milestone 增加。

```
README

↓

CLAUDE

↓

Development OS

↓

PRD

↓

Workflow

↓

Prompt

↓

Current Milestone
```

---

## Single Source of Truth

每個主題：

只有一份正式文件。

例如：

| Topic | Document |
|--------|----------|
| Product | PRD |
| Workflow | Workflow Specification |
| Prompt | Prompt Specification |
| Architecture | Product Architecture |

禁止：

重複描述。

---

## Reference First

優先引用文件。

不要：

重新貼上文件。

例如：

✔

請依照：

Workflow_Specification.md

而不是：

重新貼 Workflow。

---

## Review Only Changes

Code Review：

只 Review：

Git Diff。

不要重新閱讀整個專案。

---

## Frozen Context

已接受：

↓

已定稿：

↓

不重新建立 Context。

需要修改：

建立新版本。

---

# 6.3 Conversation Economy

Conversation 也是資源。

標準：

```
One Conversation

↓

One Goal

↓

One Milestone

↓

One Commit
```

避免：

```
One Conversation

↓

Entire Product
```

---

# 6.4 Documentation Economy

每份文件：

只負責一個責任。

| Document | Responsibility |
|-----------|---------------|
| README | Project Overview |
| CLAUDE | AI Entry Guide |
| Development Operating System | Development Rules |
| PRD | Product Requirements |
| Workflow | Process |
| Prompt | AI Prompt |
| Runtime | Runtime Rules |
| Output | Output Format |

禁止：

內容重複。

---

# 7. Decision Governance

所有重大決策皆遵循：

```
Draft

↓

Proposed

↓

Accepted

↓

Frozen

↓

Deprecated
```

說明：

Draft

尚未完成。

↓

Proposed

等待決策。

↓

Accepted

正式採用。

↓

Frozen

不得重新討論。

↓

Deprecated

新版取代。

---

# 8. Milestone Management

每次開發：

只完成：

一個 Milestone。

流程：

```
Planning

↓

Implementation

↓

Testing

↓

Review

↓

Git Commit

↓

Next Milestone
```

禁止：

一次完成全部產品。

---

# 9. Definition of Done

Milestone 完成代表：

☑ Specification 完成

☑ Coding 完成

☑ Testing 完成

☑ Review 完成

☑ Git Commit

☑ Documentation Updated

才能進入：

下一個 Milestone。

---

# 10. AI Startup Checklist

所有 AI 開始工作前：

依序閱讀：

```
README

↓

CLAUDE

↓

Development Operating System

↓

PRD

↓

Workflow

↓

Prompt

↓

Current Milestone
```

確認：

□ Scope

□ Requirements

□ Workflow

□ Prompt

□ Output

□ Milestone

確認完成：

開始 Coding。

---

# 11. File Hierarchy

```
README.md

↓

CLAUDE.md

↓

Development_Operating_System.md

↓

Product_Architecture.md

↓

PRD.md

↓

Workflow_Specification.md

↓

Prompt_Specification.md

↓

Current Milestone

↓

Implementation
```

---

# 12. Success Criteria

本文件成功的標準：

- 所有 AI 使用相同開發流程
- 所有產品使用相同文件架構
- 文件職責明確
- Context 保持最小
- Token 消耗最小
- Milestone 可快速迭代
- AI 能快速理解專案
- 新產品可直接複製開發流程

---

# Design Principles

Development Operating System 是：

- AI Product Factory 的最高開發規範
- 所有 AI Product 的共同制度
- 所有 AI Coding Agent 的共同入口
- 長期維護且版本穩定的核心文件

本文件僅定義「如何開發」。

產品需求、Workflow、Prompt、Runtime 與 Output Specification 應由各自文件負責，不應在本文件中重複描述。

---
End of Document