---
Version: v1.0
Status: Final
Owner: YB
Sprint: Sprint 8.5A
Document Type: Sprint Retrospective
Last Updated: 2026-08-07
---

# Sprint 8.5A Retrospective

---

# Sprint Summary

Sprint 8.5A 的目標為建立 Product Intelligence Foundation，讓 YB Learn 從「能運作的 MVP 工具」升級成「可觀測、可分析、可持續優化的 AI Product」，而非新增任何 AI 功能。

依 `Engineering_Kickoff_Sprint_8_5_Product_Intelligence.md` 與 Factory Standard `Product_Intelligence_Foundation_v1.0.md` 規劃，本 Sprint 專注於：

- Runtime Intelligence
- Cost Intelligence
- Cache Intelligence
- Error Intelligence
- Correlation ID

本 Sprint 額外驗證了一個新的開發流程階段：

```text
Repository Analysis
    ↓
Architecture Review
    ↓
Implementation Plan
    ↓
Coding
    ↓
Human Test
    ↓
Documentation Update
```

Architecture Review 由使用者於 Task 1 開發前主動提出，針對初版計畫做出 4 項架構調整（`app/observability/` package 化、JSONL 取代 CSV、Correlation ID 提前到 Task 1 一次建好、Daily Report 改為即時增量更新），核准後才進入 Implementation Plan，全 Sprint 未發生 Scope 擴張。

---

# Sprint Achievements

## Task 1 — Correlation ID 基礎建設 + Runtime Intelligence

完成：

- `request_id` 於 Queue 加入時產生，貫穿 Queue／Transcript／Gemini／Study Note／Download
- `app/observability/logger.py`／`runtime_metrics.py`／`daily_report.py` 骨架
- Human Test PASS

成果：

同一支影片的完整處理旅程，第一次可以用單一 ID 串起來看。

---

## Task 2 — Cost Intelligence

完成：

- `gemini_client.py` 單一攔截點記錄全部 7 種 Gemini 呼叫的 Token／估算成本
- `currency`／`study_package` 追加項目
- Human Test PASS

成果：

`Cost_Analysis.md` 記載「尚未建立 Usage Log」的限制正式解除，且往 Sprint 8.5 Kickoff 的下一里程碑（Cost Analysis v2.0）前進一步。

---

## Task 3 — Cache Intelligence

完成：

- 既有 7 處快取檢查點記錄 Hit/Miss
- Estimated Cost Saved 自動改用當天真實平均成本
- Human Test PASS

成果：

Cache 節省的成本第一次有數字可以看，且會隨真實使用資料自動變準，不需要每次手動校正估算值。

---

## Task 4 — Error Intelligence

完成：

- Gemini／非 Gemini 失敗分別記錄，`retry_count` 即時查詢得出
- Human Test PASS（範圍由使用者主動收斂：不做 Developer 層級的故障注入測試）

成果：

先前完全靜默、零記錄的 quick_summary 失敗，第一次有紀錄可查。

---

# What Went Well

## Architecture Review 提前攔下設計問題

使用者在 Coding 開始前就指出 Correlation ID 的正確語意（整個處理旅程共用一組 ID，而非每次呼叫各自一組），若等到 Task 4 才發現，等於要重工前 3 個 Task 已經寫好的邏輯。提前一個階段做 Review，遠比事後修正便宜。

---

## 增量式 Daily Report 撐過了真實高強度使用

Human Test 期間使用者反覆點擊、重新整理，`daily_report.json` 最終單日累積超過 300 筆事件（含 248 筆 Cache 事件），increment-in-place 的設計全程沒有損壞或遺失資料，鎖（Lock）機制在真實併發下也沒有出過問題。

---

## Observability 真的沒有中斷過主流程

Engineering Rule #4（Observability 絕不可中斷正常流程）全程遵守，Human Test 期間即使遇到真實錯誤（YouTube 429、快取邊界案例），MVP 功能本身從未因為 Product Intelligence 的程式碼而失敗。

---

# Problems Found

## 中途修改程式造成單日統計出現歷史缺口

`study_package` 是 Task 2 過程中追加的功能，在它被加入之前就已經完成的幾次 Study Note 生成，自然不會被算進 `study_package.count`，導致同一天內 `study_notes_generated`（6）與 `study_package.count`（2）出現落差。這不是邏輯錯誤，而是「增量更新」架構的必然結果：只會反映程式碼存在之後發生的事件。正式上線後程式不會在同一天內變動，這個現象不會重現，但值得記錄下來，避免未來誤判成 Bug。

---

## 使用者輸入驗證失敗完全沒有留下痕跡

`POST /api/queue` 的無效網址／找不到影片，兩個拒絕點都發生在 `request_id` 誕生之前，目前對 Product Intelligence 完全不可見。使用者主動發現這點，並正確判斷這屬於 Product Analytics（有多少人輸入格式錯誤），跟 Runtime Error（系統執行失敗）是不同性質的問題，不應該混在一起統計，已記錄於 Product Backlog。

---

## Download 是 Runtime Event 還是 User Action，界線未定

目前 Download 被當成 Runtime 的一個 stage 記錄，但一支影片被重複下載幾次，就會產生幾筆 Runtime 事件，稀釋了「今天處理了幾支影片」這類指標的意義。使用者判斷這是架構層級的問題，主動要求先不調整，等 Sprint 8.5A 全部完成後再一次檢討，避免開發中途反覆調整架構。

---

# Root Cause Analysis

本 Sprint 沒有出現需要 RCA 的 Bug——4 個 Task 的 Human Test 全數一次 PASS，沒有 FAIL 後修正重測的情況（與 Sprint 8 明顯不同）。真正需要深入討論的是兩個「這是不是 Bug」的判斷：

```text
Download 產生大量 Runtime 事件
    ↓
不是 Bug，是 Runtime／User Action 的分類界線尚未定義
    ↓
使用者決定：不在開發中途調整架構
```

```text
輸入驗證失敗零記錄
    ↓
不是 Bug，是 Error Intelligence（系統面）與 Product Analytics（使用者行為面）的範疇差異
    ↓
使用者決定：記錄至 Backlog，非本次必備
```

兩者共同的教訓：Product Intelligence 的「正確性」不只是「有沒有記錄到」，更是「記錄的東西分類是否正確」——這比單純補齊記錄點更需要人為判斷。

---

# Key Lessons Learned

- Architecture Review 值得成為正式的流程階段，尤其是牽涉跨 Task 共用基礎設施（如 Correlation ID）的 Sprint。
- 「這是不是 Bug」的判斷，比「有沒有記錄到」更需要 Human Review——本 Sprint 兩個真正有價值的討論（Download 分類、輸入驗證缺口）都是使用者主動判斷「這不是 Bug」，而不是要求立刻修正。
- 增量式（Incremental）架構的副作用（中途改程式造成的歷史缺口）需要在文件中明確記錄，否則未來排查會誤判成資料損毀。
- Observability 模組全程對主流程「零侵入」是可以在真實高強度使用下驗證的，不只是設計時的理論保證。

---

# Process Improvements

本 Sprint 驗證成功的新流程：

```text
Repository Analysis
    ↓
Architecture Review
    ↓
Implementation Plan
    ↓
Human Review
    ↓
Coding
    ↓
Human Test
    ↓
Documentation Update
    ↓
Commit（No Push）
```

建議正式納入 AI_Product_Factory_Standard，作為 Repository Architecture 或跨 Task 共用基礎設施類型 Sprint 的標準前置階段。

---

# Product Backlog

已新增：

## Product Analytics — 使用者輸入驗證失敗追蹤

新增獨立的 `validation` 統計（例如 `invalid_url`／`unsupported_video`），不併入 Runtime Error 統計。

---

## Runtime／User Action 分類界線

Download 目前計入 Runtime Event，待 Sprint 8.5A 全部完成後與使用者一起檢討是否應改列為獨立的 User Action 統計。

---

## Error Intelligence 覆蓋範圍擴充

`GeminiConfigError`、5 個獨立 Learning Model 端點的非 Gemini 失敗，目前不在記錄範圍，優先度較低。

---

## Sprint 8.5B — Visualization Layer

Runtime Dashboard／Cost Dashboard／Product Dashboard，完成 Product Intelligence Foundation 第二階段（Engineering Kickoff Sprint 8.5 文件第 16 節已定義）。

---

# Action Items

Sprint 8.5A（已完成）：

- Task 1／Task 2／Task 3／Task 4 完成並驗收
- 端對端驗證（Correlation ID 跨 4 份 log 一致性）PASS
- Documentation Update 完成，待 Commit／Push

Sprint 8.5B（待評估，Push 後由使用者決定是否成立）：

- Runtime／Cost／Product Dashboard

Product Backlog（等待評估或觸發條件，非排定 Sprint）：

- 使用者輸入驗證失敗追蹤（Product Analytics）
- Download Runtime／User Action 分類界線檢討
- Error Intelligence 覆蓋範圍擴充（`GeminiConfigError`、5 個獨立端點）

---

# Key Metrics

Completed Tasks:

- Task 1
- Task 2
- Task 3
- Task 4
- End-to-End Validation

Human Test Result:

全部一次 PASS，無 FAIL 後修正重測的情況。

Commits:

待使用者確認 Commit 方式（依 Task 個別回溯補 Commit，或本次 Documentation Update 一併整理成單一 Commit）。

Push Strategy:

One Sprint = One Push（待使用者確認 Integration Test 範圍與時機）。

---

# Final Reflection

Sprint 8.5A 沒有新增任何使用者看得到的功能，卻是 YB Learn 第一次真正「知道自己在做什麼」——今天處理了幾支影片、花了多少 Gemini 成本、Cache 省下多少錢、哪裡失敗過幾次，全部第一次有數字可以回答。

比起功能本身，本 Sprint 更重要的成果是驗證了 Architecture Review 這個新流程階段的價值：兩次關鍵的架構調整（Correlation ID 語意、Daily Report 增量更新）都發生在寫程式之前，而不是事後修正。這與 Sprint 8「Human Test 發現真正問題」的教訓互補——Sprint 8 證明了執行後驗證的價值，Sprint 8.5A 證明了執行前審查同樣重要。

Task 1～4 與端對端驗證皆已完成並一次驗收通過，Documentation Update 已完成，準備依使用者指示進行 Commit。
