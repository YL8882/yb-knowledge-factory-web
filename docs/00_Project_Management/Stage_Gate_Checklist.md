---
title: Stage Review Checklist
version: v1.0
status: Final
owner: YB
last_updated: 2026-07-24
document_type: Review Checklist
purpose: Standard review checklist for each development stage to ensure quality before moving to the next phase.
---

# Stage Review Checklist

> 本文件定義 YB Knowledge Factory MVP 各開發階段的標準審查項目（Stage Gate）。
>
> 每完成一個階段，必須完成 Review 並確認符合 Checklist，才能進入下一階段。

---

# Review Workflow

```
Current Stage

↓

Self Review

↓

Checklist Review

↓

Approved

↓

Next Stage
```

---

# Stage 1 — Product Planning Review

## Objective

確認產品需求完整且一致。

### Checklist

- [ ] MVP 範圍已明確定義
- [ ] 使用者流程（User Journey）完整
- [ ] 輸入與輸出已定義
- [ ] Success Criteria 已定義
- [ ] 無超出 MVP 範圍的功能

**Output**

- PRD Final

---

# Stage 2 — Workflow Review

## Objective

確認 Workflow 可執行且完整。

### Checklist

- [ ] 每一步輸入（Input）已定義
- [ ] 每一步輸出（Output）已定義
- [ ] 使用工具已確認
- [ ] Runtime 流程完整
- [ ] 無遺漏流程

**Output**

- Workflow Final

---

# Stage 3 — Prompt Review

## Objective

確認 Prompt 品質符合要求。

### Checklist

- [ ] AI Role 已完成
- [ ] System Instructions 已完成
- [ ] Task Prompt 已完成
- [ ] Output Schema 已完成
- [ ] Prompt 組裝完成
- [ ] Prompt 無衝突
- [ ] Token 使用合理

**Output**

- Prompt Final

---

# Stage 4 — Google AI Studio Review

## Objective

驗證 Prompt 與 Workflow。

### Checklist

- [ ] Prompt 可正常執行
- [ ] Study Note 品質符合需求
- [ ] Output Format 正確
- [ ] Token 消耗可接受
- [ ] 無明顯 Hallucination
- [ ] 輸出一致性良好

**Output**

- Prototype Approved

---

# Stage 5 — UI / Wireframe Review

## Objective

確認介面設計後再開始 Coding。

### Checklist

- [ ] Wireframe 已完成
- [ ] 操作流程合理
- [ ] 畫面資訊完整
- [ ] 使用者操作簡單
- [ ] 已完成 UI Review

**Output**

- UI Approved

---

# Stage 6 — Claude Code Implementation Review

## Objective

確認功能依規格完成。

### Checklist

- [ ] 功能符合 PRD
- [ ] Workflow 正常
- [ ] Prompt 正常整合
- [ ] Runtime 正常
- [ ] 檔案輸出正常
- [ ] 無重大 Error

**Output**

- Implementation Complete

---

# Stage 7 — Internal Testing Review

## Objective

確認 MVP 可正常展示與使用。

### Checklist

- [ ] YouTube URL 可輸入
- [ ] Audio Download 正常
- [ ] Transcript 正常
- [ ] Study Note 正常
- [ ] Markdown 可輸出
- [ ] Workflow 全流程完成

**Output**

- MVP Ready

---

# Stage 8 — Release Review

## Objective

確認可正式發布。

### Checklist

- [ ] 所有 Review 已完成
- [ ] Bug 已修正
- [ ] Demo 可展示
- [ ] Documentation 已更新
- [ ] Version 已更新

**Output**

- MVP Released

---

# Review Principles

所有階段皆遵循以下原則：

## Workflow First

確認流程，再開始開發。

---

## Human in the Loop

重要決策必須人工確認。

---

## Incremental Development

一次完成一個階段。

---

## Continuous Validation

完成立即驗證，不累積問題。

---

## Definition of Done

未完成 Checklist，不得進入下一階段。

---

# Approval Record

| Stage | Reviewer | Date | Status |
|--------|----------|------|--------|
| Product Planning | | | |
| Workflow | | | |
| Prompt | | | |
| Google AI Studio | | | |
| UI / Wireframe | | | |
| Claude Code | | | |
| Internal Testing | | | |
| Release | | | |

---

# Change Log

| Version | Date       | Description           |
| ------- | ---------- | --------------------- |
| v1.0    | 2026-07-24 | Initial Final Version |