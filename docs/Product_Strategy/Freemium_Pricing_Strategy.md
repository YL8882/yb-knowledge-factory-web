---
Version: v1.0
Status: Draft
Owner: YB
Last Updated: 2026-08-07
Document Type: Product Strategy
Project: YB Learn
Document Name: Freemium_Pricing_Strategy
---

# Freemium Pricing Strategy v1.0

> 本文件定義 YB Learn 的免費版（Freemium）與付費方案（Pricing），作為產品商業化、成本控制與營收模式的策略文件。

---

# 1. Document Purpose

本文件目的：

- 建立 YB Learn 商業模式
- 定義免費版與付費版差異
- 控制 Gemini API 成本
- 建立可持續獲利模式
- 作為 Beta 與正式版定價依據

---

# 2. Product Positioning

## Product

YB Learn

## Product Vision

Capture First.
Process Later.

快速收藏 YouTube 影片，並利用 AI 快速整理成可學習、可複習、可累積的知識。

---

# 3. Business Objectives

## 短期（Beta）

- 驗證產品需求
- 建立第一批付費使用者
- 收集成本數據
- 驗證 Freemium 模式

---

## 中期

- 建立穩定訂閱收入
- 降低 API 成本
- 提高留存率

---

## 長期

- 成為 AI 學習助手平台
- 建立 Knowledge Cloud
- 建立 AI Personal Learning System

---

# 4. Pricing Principles

定價原則：

1. 免費版能真正產生價值。
2. AI 成本必須可控制。
3. 付費版必須明顯提升效率。
4. 優先採訂閱制。
5. 成本與價格保持健康利潤。

---

# 5. Freemium Strategy

## Free

適合：

- 新使用者
- 體驗產品
- SEO 導流

提供：

- YouTube Capture
- Transcript
- 基本摘要（Executive Summary）
- 最近歷史紀錄（有限）

限制：

- 每日 AI 次數限制
- 不提供完整 Study Note
- 不提供 Knowledge Package
- 不提供 Markdown 匯出

---

## Pro

適合：

- 長期學習者
- 專業工作者
- 創作者

提供：

- 無限制 Transcript
- 完整 Study Note
- Knowledge Package
- Teach Back
- Action List
- Review
- Markdown Download
- 歷史紀錄
- 未來 AI 功能優先使用

---

# 6. Pricing (Draft)

| Plan | Monthly | Status |
|------|---------:|--------|
| Free | NT$0 | MVP |
| Pro | 待決定 | Draft |

> 正式價格待 Cost Analysis v2.0 完成後決定。

---

# 7. Cost Control Strategy

成本控制原則：

## Cache First

相同影片：

- 不重複呼叫 Gemini
- 優先讀取已生成內容

---

## Output Optimization

控制：

- Executive Summary 長度
- Workflow 長度
- Study Note 長度

降低 Output Tokens。

---

## Usage Monitoring

建立：

- Usage Log
- Token Dashboard
- API Cost Dashboard

追蹤：

- 每份 Study Package 成本
- 每位使用者成本
- 每日 API 成本

---

# 8. Upgrade Triggers

建議使用者升級時機：

- AI 次數用完
- 想取得完整 Study Note
- 想下載 Markdown
- 想保存完整歷史紀錄
- 想使用進階學習工具

---

# 9. Success Metrics

Beta 階段追蹤：

- 免費使用者數
- 付費轉換率
- 每日活躍使用者（DAU）
- 每位使用者平均成本
- 每位使用者平均收入（ARPU）
- API 成本占收入比例

---

# 10. Dependencies

本文件依賴：

- YB_Learn_Cost_Analysis_v1.0
- Beta Feedback
- Usage Log
- API Cost Dashboard

---

# 11. Future Improvements

待完成：

- Usage Log
- Token Analysis
- Cost Dashboard
- Dynamic Pricing
- Team Plan
- Education Plan
- Enterprise Plan

---

# 12. Conclusion

Freemium 模式的目的不是提供所有功能，而是讓使用者快速體驗 YB Learn 的核心價值，並透過完整 AI 學習流程與進階功能，引導有持續需求的使用者升級至付費方案。

正式定價將依據 Cost Analysis、Beta 使用數據與 API 成本優化成果持續調整，以確保產品具備長期商業可行性。