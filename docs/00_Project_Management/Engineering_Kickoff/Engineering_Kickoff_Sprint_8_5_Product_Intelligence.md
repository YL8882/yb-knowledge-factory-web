---
Version: v1.0
Status: Approved
Owner: YB
Last Updated: 2026-08-07
Document Type: Engineering Kickoff
Project: YB Learn
Sprint: Sprint 8.5
Epic: Product Intelligence Foundation
Document Name: Engineering_Kickoff_Sprint_8_5_Product_Intelligence
---

# Engineering Kickoff — Sprint 8.5
# Product Intelligence Foundation

> 本文件作為 Sprint 8.5 的正式工程開發文件，提供 Claude Code 實作 Product Intelligence Foundation 的完整需求、開發範圍與驗收標準。

---

# 1. Sprint Goal

本 Sprint 不新增任何 AI 功能。

目標為建立：

> **Product Intelligence Foundation**

讓 YB Learn 從 MVP 工具，升級成可監控、可分析、可持續優化的 AI Product。

完成後系統應能回答：

- 今天產生多少 Study Note？
- 今天 Gemini 花多少成本？
- 平均生成時間？
- Cache 是否生效？
- 哪個流程最慢？
- 今天是否有 Error？

---

# 2. Background

目前 MVP 已完成：

- YouTube Capture
- Transcript
- Study Note
- Download
- Queue
- History

目前缺乏：

- Runtime Metrics
- API Usage Metrics
- Cost Metrics
- Error Metrics
- Cache Metrics

導致：

- 無法分析成本
- 無法分析效能
- 無法分析產品使用情況

因此開始建立：

Product Intelligence Foundation。

---

# 3. References

開發前請閱讀：

- Product_Intelligence_Foundation_v1.0.md
- AI_Product_Factory_Standard.md
- Runtime_Specification.md
- Workflow_Specification.md

所有實作皆應符合上述標準。

---

# 4. Scope

本 Sprint 僅建立：

Backend Product Intelligence。

不修改：

- UI
- Prompt
- Product Features

---

# 5. Phase 1 — Runtime Intelligence

建立 Runtime Metrics。

記錄：

- Request ID
- Timestamp
- Video ID
- Processing Stage
- Start Time
- End Time
- Duration
- Status

Stages：

- Queue
- Transcript
- Study Note
- Download

---

# 6. Phase 2 — Cost Intelligence

建立 Gemini Usage Log。

記錄：

- Model
- Input Tokens
- Output Tokens
- Estimated Cost
- Processing Time

輸出：

```text
outputs/logs/gemini_usage.jsonl
```

---

# 7. Phase 3 — Cache Intelligence

建立 Cache Metrics。

記錄：

- Cache Hit
- Cache Miss
- Estimated Cost Saved

輸出：

```text
outputs/logs/cache.jsonl
```

---

# 8. Phase 4 — Error Intelligence

建立 Error Log。

輸出：

```text
outputs/logs/errors.jsonl
```

記錄：

- Timestamp
- Request ID
- Processing Stage
- Exception
- Retry Count

---

# 9. Phase 5 — Runtime Report

建立每日統計。

輸出：

```text
outputs/reports/daily_report.json
```

內容：

- Transcript Generated
- Study Notes Generated
- API Calls
- Estimated Cost
- Average Runtime
- Cache Hit Rate
- Error Count

---

# 10. Directory Structure

```text
outputs/

├── logs/
│
├── gemini_usage.jsonl
├── runtime.jsonl
├── cache.jsonl
├── errors.jsonl
│
└── reports/

    └── daily_report.json
```

---

# 11. Engineering Requirements

Logging：

- 不可影響正常流程。
- Logging Failure 不可中斷產品。
- Logging 應盡量採非同步。

所有 Log：

UTF-8

JSONL

JSON

格式固定。

---

# 12. Out of Scope

本 Sprint 不做：

- Dashboard UI
- Charts
- Analytics Page
- Business Intelligence
- AI Chat
- Mobile
- Team Plan

---

# 13. Acceptance Criteria

完成後系統應能回答：

## Runtime

- 今天處理多少影片？
- 平均處理時間？

---

## Cost

- 今天 Gemini 花多少？
- 平均每份 Study Note 成本？

---

## Cache

- Cache Hit Rate？
- 節省多少 API 成本？

---

## Error

- 今天有多少 Error？
- Retry 幾次？

---

若上述問題皆可回答。

代表：

Product Intelligence Foundation

第一階段完成。

---

# 14. Deliverables

Claude Code 應提供：

## Architecture Summary

說明：

本次新增架構。

---

## Files Changed

列出：

所有修改檔案。

---

## Directory Structure

列出：

新增資料夾。

---

## Migration Notes

若有：

相容性變更。

---

## Acceptance Test

提供：

測試方式。

---

## Known Limitations

列出：

目前限制。

---

# 15. Definition of Done

完成後：

✓ Runtime Metrics

✓ Gemini Usage Log

✓ Cache Log

✓ Error Log

✓ Daily Report

全部正常產生。

且：

不影響目前 MVP 功能。

---

# 16. Next Sprint

Sprint 8.5B

Visualization Layer

內容：

- Runtime Dashboard
- Cost Dashboard
- Product Dashboard

完成 Product Intelligence Foundation 第二階段。

---

# 17. Engineering Notes

本 Sprint 的目標不是增加功能，而是建立平台能力（Platform Capability）。

完成後，YB Learn 將具備：

- 可觀測（Observable）
- 可量測（Measurable）
- 可分析（Analyzable）
- 可優化（Optimizable）

未來所有 AI Product 皆應遵循相同的 Product Intelligence Foundation 標準。