---
Version: v1.0
Status: Design Freeze
Owner: YB Learn
Last Updated: 2026-08-05
Document Type: Product Architecture
Priority: Core
---

# Knowledge Structure Engine v1.0

> **YB Learn 不只是幫使用者取得知識，而是幫助使用者快速建立知識結構，讓知識真正留在腦中。**

---

# 1. Mission

## Product Mission

YB Learn 並不是：

- AI 摘要工具
- Transcript 工具
- Study Note 工具
- 心智圖工具
- 筆記工具

YB Learn 是：

> **Knowledge Structure Engine（知識結構引擎）**

產品目的不是整理內容，而是協助使用者：

- 更快理解
- 更深理解
- 更久記住

建立真正的 **Mental Model（知識架構）**。

---

# 2. Product Philosophy

知識不是越多越好。

真正的學習，是建立：

- 結構（Structure）
- 關聯（Relationship）
- 因果（Cause）
- 流程（Flow）
- 決策（Decision）

讓知識在腦中形成可重建的模型，而不是一段又一段的文字。

---

# 3. Learning Model

Learning Model 採三階段設計。

## Phase 1 — Orientation

回答：

> 我要不要學？

目的：

快速建立方向感。

輸出：

- One Sentence
- 30 秒快速理解
- 五個重點

---

## Phase 2 — Comprehension

回答：

> 我真的看懂了嗎？

目的：

建立 Mental Model。

輸出：

Learning Blueprint

不是摘要。

而是：

知識架構。

---

## Phase 3 — Retention

回答：

> 我真的學會了嗎？

目的：

主動回憶。

輸出：

- Teach Back
- Quiz
- Action List
- Review

---

# 4. Knowledge Structure Engine

Knowledge Structure Engine 為產品核心。

它不是：

Renderer。

也不是：

Learning Blueprint。

它負責：

> 根據影片內容，自動判斷最適合的知識結構。

---

# 5. Architecture

```text
Video

↓

Knowledge Extraction

↓

Knowledge Structure Detection

↓

Knowledge JSON

↓

Renderer

↓

Learning Blueprint

↓

Teach Back

↓

Action List
```

---

# 6. Knowledge Structure Taxonomy

## Core Structures（v1.0）

目前支援：

| Structure | 適用內容 |
|------------|-----------|
| Flow | SOP、教學 |
| Cause & Effect | 商業分析 |
| Classification | 工具介紹 |
| Decision | 房地產、決策 |
| Comparison | A vs B |
| Timeline | 歷史、事件 |
| Problem → Solution | 案例分析 |

---

## Future Structures

保留未來擴充：

- Framework
- Hierarchy
- Layer
- Matrix
- Network
- Cycle
- Pyramid
- System Model
- Concept Graph

---

# 7. Knowledge Structure Detection

AI 第一件事不是摘要。

而是：

判斷：

> 這支影片最適合哪一種知識結構？

例如：

教學影片：

↓

Flow

商業評論：

↓

Cause & Effect

產品比較：

↓

Comparison

房地產：

↓

Decision

歷史：

↓

Timeline

---

# 8. Knowledge JSON

Knowledge JSON 為 Renderer 的唯一資料來源。

例如：

```json
{
  "type": "flow",
  "steps": [
    {
      "step": 1,
      "purpose": "...",
      "action": "..."
    }
  ]
}
```

Renderer 不直接依賴 Prompt。

Renderer 永遠依賴：

Knowledge JSON。

---

# 9. Renderer Strategy

Structure 與 Renderer 完全分離。

同一種 Structure 可以有不同 Renderer。

例如：

Flow：

- Step Card
- Timeline
- Tree

Decision：

- Decision Tree
- Decision Card

Comparison：

- Table
- Matrix

Timeline：

- Vertical Timeline
- Horizontal Timeline

Renderer 可以新增。

Structure 不需要修改。

---

# 10. Learning Blueprint

Learning Blueprint：

不是 Engine。

Learning Blueprint：

是 Engine 的第一個 Output。

目的：

建立：

Mental Model。

不是：

重新整理文字。

不是：

Markdown。

不是：

Mind Map。

而是：

最容易理解的知識架構。

---

# 11. Prompt Strategy

Prompt 分三步。

## Step 1

Knowledge Structure Detection

↓

判斷 Structure

---

## Step 2

Knowledge Extraction

↓

輸出 Knowledge JSON

---

## Step 3

Renderer

↓

依 Structure 呈現 Blueprint

避免：

直接生成大量文字。

---

# 12. Human Test

真正驗證：

不是：

按鈕是否出現。

不是：

Renderer 是否正常。

而是：

使用者是否建立 Mental Model。

Human Test：

30 秒內：

使用者是否可以：

- 說出影片主題
- 說出影片架構
- 解釋內容之間關係
- 重建約 70% 的內容

若可以：

Learning Blueprint 成功。

---

# 13. Product KPI

產品成功不是：

- Summary 比較漂亮
- Markdown 比較完整

而是：

使用者：

- 更快理解
- 更深理解
- 更久記住

---

# 14. Relationship

Knowledge Structure Engine

↓

Learning Blueprint

↓

Teach Back

↓

Quiz

↓

Action List

↓

Review

↓

Skill Tree

所有功能皆建立於同一套 Knowledge Structure Engine。

---

# 15. Design Principles

1. Structure First
2. Prompt Second
3. Renderer Last
4. Engine > Feature
5. Mental Model > Summary
6. Knowledge > Markdown
7. Learning > Note Taking

---

# 16. Vision

> **Learn Faster. Understand Deeper. Remember Longer.**

中文：

> **更快學會，更深理解，更久記住。**

YB Learn 的所有產品設計、Prompt、UI、AI Workflow 與 Human Test，皆應遵循本文件。