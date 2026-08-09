---
Version: v1.0
Status: Baseline
Owner: YB
Last Updated: 2026-08-07
Document Type: Product Strategy
Project: YB Learn
Document Name: YB_Learn_Cost_Analysis_v1.0
---

# YB Learn Cost Analysis v1.0 (Baseline)

> 本文件建立 YB Learn MVP 階段的第一份成本基準（Baseline），作為未來產品定價、Freemium 設計、成本優化與商業化決策的依據。

---

# 1. Purpose

本文件目的：

- 建立目前 MVP 的成本基準
- 分析主要成本來源
- 評估產品商業可行性
- 規劃成本優化方向
- 作為 Freemium 與 Pricing Strategy 的依據

---

# 2. Analysis Scope

分析期間：

2026/07/28 ～ 2026/08/05

產品版本：

YB Learn MVP v0.1

模型：

Gemini 2.5 Flash

---

# 3. Google Cloud Billing Summary

| 項目 | 數值 |
|------|------:|
| Billing Period | 2026/07/28 ～ 2026/08/05 |
| Currency | USD |
| Total Cost | US$55.58 |
| Main Service | Gemini API |
| Primary Cost | Generate Content Output Tokens |
| Secondary Cost | Generate Content Input Tokens |
| Logging Cost | 幾乎可忽略 |

---

# 4. Development Statistics

| 指標 | 數值 |
|------|------:|
| Transcript Generated | 185 |
| Study Notes Generated | 125 |
| Study Note Completion Rate | 67.6% |

說明：

本統計包含：

- MVP 功能測試
- Prompt Debug
- Retry
- Claude Code 開發
- 重複生成測試

因此：

> 不代表正式營運數據。

---

# 5. Cost Estimation (Baseline)

| 指標 | 估算 |
|------|------:|
| Average Cost / Transcript | 約 US$0.30 |
| Average Cost / Study Note | 約 US$0.44 |

> 此數值為 MVP 開發期間平均成本，包含大量重複測試，不可直接作為正式營運成本。

---

# 6. Cost Distribution

目前已知：

- 約 80% 成本來自 Output Tokens
- 約 20% 成本來自 Input Tokens
- Cloud Logging 幾乎沒有成本
- Cloud Storage 幾乎沒有成本

初步判斷：

目前成本主要來自：

- Gemini 回覆內容過長
- 開發期間重複生成
- Prompt Debug
- Retry

並非基礎架構造成。

---

# 7. Root Cause Analysis

目前造成成本較高的原因：

- 大量 MVP 測試
- 同一支影片重複生成
- Prompt 多次修改
- Output Tokens 過高
- 尚未建立 Usage Log
- 尚未完成完整成本優化

---

# 8. Cost Optimization Roadmap

| 項目 | 狀態 | 預期效果 |
|------|------|----------|
| Study Note Cache | ✅ 已完成 | 避免重複生成 |
| Prompt Optimization | Planned | 降低 Output Tokens |
| Output Length Control | Planned | 降低 API 成本 |
| Usage Log | Planned | 建立成本分析能力 |
| Token Dashboard | Planned | 即時成本監控 |

---

# 9. Known Limitations

目前尚未取得：

- 每次 Gemini Token 使用量
- 每支影片成本
- 每位使用者平均成本
- Cache 命中率
- API 成功率
- 每日成本趨勢

因此：

本文件定位為：

> Cost Baseline v1.0

---

# 10. Next Milestone

Sprint 8.5：

- 建立 Usage Log
- Token Cost Dashboard
- Prompt Cost Optimization
- Output Token Reduction

完成後：

建立

> YB Learn Cost Analysis v2.0

---

# 11. Conclusion

目前 Google Cloud 成本主要集中於 Gemini API Output Tokens。

依目前分析：

- 基礎架構成本極低。
- 成本主要來自 MVP 開發與大量測試。
- 待完成 Cache、Prompt Optimization、Usage Log 後，預期正式營運成本可明顯下降。

本文件作為：

> YB Learn 第一份成本基準（Baseline）。

未來所有 Pricing、Freemium、Business Model、ROI 分析皆以此文件為基礎持續更新。
