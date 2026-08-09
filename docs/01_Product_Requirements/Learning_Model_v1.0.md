---
Version: v1.0
Status: Design Freeze
Owner: YB Learn
Last Updated: 2026-08-05
Document Type: Product Learning Model
Priority: Core
---

# Learning Model v1.0

> **Learning Model 定義 YB Learn 如何幫助使用者從「取得知識」走向「真正學會知識」。**

---

# 1. Purpose

Learning Model 是 YB Learn 的核心學習架構。

它不是：

- UI 流程
- Prompt 流程
- AI Workflow

而是定義：

> **使用者如何從第一次接觸內容，到真正將知識留存在腦中。**

所有產品功能，都必須建立於此 Learning Model。

---

# 2. Learning Philosophy

YB Learn 不相信：

閱讀 = 學會。

整理 = 理解。

摘要 = 記住。

真正的學習必須完成三件事：

1. 建立方向感（Orientation）
2. 建立知識結構（Comprehension）
3. 建立長期記憶（Retention）

這三個階段缺一不可。

---

# 3. Learning Journey

```text
Video / PDF / Book / Course

↓

Phase 1
Orientation

↓

Phase 2
Comprehension

↓

Phase 3
Retention

↓

Knowledge becomes Ability
```

---

# 4. Three Learning Phases

| Phase | 名稱 | 目的 | 回答的問題 |
|------|------|------|------------|
| Phase 1 | Orientation | 建立方向感 | 我要不要學？ |
| Phase 2 | Comprehension | 建立知識架構 | 我真的看懂了嗎？ |
| Phase 3 | Retention | 建立長期記憶 | 我真的學會了嗎？ |

---

# 5. Phase 1 — Orientation

## Objective

快速建立影片輪廓。

協助使用者判斷：

這支影片值不值得投入時間。

---

## Goal

30 秒內知道：

- 主題
- 核心價值
- 是否值得繼續

---

## Outputs

- One Sentence
- 30 秒快速理解
- 五個重點（Quick Learn Layer）

---

## Success Criteria

使用者可以回答：

> 「這支影片主要在講什麼？」

而不是：

> 「我看了很多文字。」

---

# 6. Phase 2 — Comprehension

## Objective

建立 Mental Model。

不是閱讀內容。

而是理解：

內容彼此之間的關係。

---

## Goal

建立：

Knowledge Structure。

讓知識形成可重建的架構。

---

## Core Engine

Knowledge Structure Engine

---

## Primary Output

Learning Blueprint

Learning Blueprint 不是摘要。

而是：

根據影片內容，自動選擇最適合的知識結構。

例如：

- Flow
- Cause & Effect
- Timeline
- Decision
- Classification
- Comparison
- Problem → Solution

---

## Success Criteria

使用者可以：

用自己的話，

說出影片的知識架構。

而不是背誦內容。

---

# 7. Phase 3 — Retention

## Objective

將理解轉換成長期記憶。

真正的學習，

發生於主動回憶。

而不是再次閱讀。

---

## Goal

讓知識真正留在腦中。

---

## Outputs

- Teach Back
- Quiz
- Action List
- Review

---

## Success Criteria

使用者可以：

不用查看原始內容，

重建約 70% 的知識。

並能立即應用。

---

# 8. Product Mapping

| Phase | Product Feature |
|------|-----------------|
| Phase 1 | One Sentence、30 秒快速理解、五個重點 |
| Phase 2 | Knowledge Structure Engine、Learning Blueprint |
| Phase 3 | Teach Back、Quiz、Action List、Review |

---

# 9. Knowledge Progression

```text
Information

↓

Understanding

↓

Knowledge Structure

↓

Memory

↓

Ability
```

學習不是停留在：

Information。

而是：

最終形成：

Ability。

---

# 10. Learning Principles

所有功能，

都必須符合：

## Learn Faster

降低開始學習的成本。

---

## Understand Deeper

建立知識結構。

---

## Remember Longer

建立長期記憶。

---

## Use Immediately

知識必須能立即應用。

---

# 11. Human Test

Learning Model 的驗收，

不是驗證 AI。

而是驗證使用者。

每個 Phase 都應有獨立驗收。

---

## Phase 1

30 秒內：

使用者是否知道：

影片值不值得看？

---

## Phase 2

使用者是否能：

說出：

影片的知識架構。

而不是：

影片逐字內容。

---

## Phase 3

使用者是否能：

在沒有任何提示下，

用自己的語言，

重建約 70% 的內容。

---

# 12. Product KPI

Learning Model 成功，

不是：

- Summary 很完整
- Markdown 很漂亮
- Prompt 很長

而是：

使用者：

- 更快理解
- 更深理解
- 更久記住

---

# 13. Relationship with Other Documents

Brand_Strategy_v1.0

↓

Why.md

↓

Learning_Model_v1.0

↓

Knowledge_Structure_Engine_v1.0

↓

Prompt Design

↓

UI Design

↓

Implementation

Learning Model 定義：

**使用者如何學習。**

Knowledge Structure Engine 定義：

**AI 如何建立知識結構。**

兩者相互依存，

但職責不同。

---

# 14. Future Evolution

Learning Model v1.0

未來可擴充：

- Adaptive Learning
- Personalized Review
- Spaced Repetition
- AI Mentor
- Skill Tree
- Learning Analytics

但所有新增能力，

都不得破壞三階段 Learning Model。

---

# 15. Design Freeze

Learning Model v1.0 為 YB Learn 核心產品模型。

未來：

所有 Prompt、UI、Workflow、AI Engine 與 Human Test，

皆應遵循本 Learning Model。

除非進入 v2.0，

否則不修改 Learning Model 的核心三階段架構。