---
Version: v1.0
Status: Final
Owner: YB
Sprint: Sprint 08
Document Type: Sprint Retrospective
Last Updated: 2026-08-06
---

# Sprint 08 Retrospective

---

# Sprint Summary

Sprint 08 的目標為提升 YB Learn Beta MVP 的穩定性與使用體驗，而非新增大型功能。

本 Sprint 專注於：

- Error Handling
- Queue Card UI
- Loading / Processing
- Error Classification
- Human Test
- Product Polish

整體遵循 AI Product Factory Standard：

```text
Proposal
    ↓
Human Review
    ↓
Implementation
    ↓
Human Test
    ↓
Documentation Update
    ↓
Commit (No Push)
```

所有 Task 皆採相同流程完成，Sprint 8 Integration Test（6 項情境）已全數 PASS，未發生 Scope 擴張。

---

# Sprint Achievements

## Task 1 — Error Handling

完成：

- Inline Error Message
- Retry Button
- Error 顯示於對應 Queue Card
- Human Test PASS

成果：

使用者不再需要查看 Console 即可知道錯誤原因。

---

## Task 2 — Queue Card UI

完成：

- Learning Module 可獨立展開 / 收合
- 共用 Toggle Header
- Queue Card 更容易閱讀
- Human Test PASS

新增 Product Backlog：

未來 Queue Card 預設應保持簡潔，只顯示一句話重點與學習入口，詳細內容按需展開。

---

## Task 3 — Loading / Processing

完成：

- 五個模組 Loading 狀態一致
- 防止重複點擊
- 修正 Gemini Blocking 問題
- 支援 Parallel Processing
- Human Test PASS

成果：

不同影片可同時執行 Gemini 工作，不再互相阻塞。

---

## Task 4 — Error Classification

完成：

- classify_error() 錯誤分類改善
- stage-aware Error Mapping
- Human Test 通過

真實驗證案例：

YouTube Subtitle Download

↓

HTTP 429

↓

Retry

↓

PASS

確認：

此案例並非 Gemini API 額度問題，而是 YouTube 字幕下載遭到 Rate Limit。

---

## Task 5 — Structure Detection 一致性改善（Deferred）

Proposal 已規劃修法（`_LEARNING_BLUEPRINT_SYSTEM_INSTRUCTION` 新增判斷優先順序規則），使用者審閱後決定**不執行，延後至 Product Backlog**。

決策原因：

- 目前沒有可穩定重現的 `structure_type` 判斷不一致案例
- 無法建立 Before／After 比較
- 無法定義明確 PASS／FAIL
- Human Test 沒有客觀驗收方式

依「可驗收的 Bug 優先」原則，等之後再次遇到真實不一致案例，再依該案例修正與驗收。

---

# What Went Well

本 Sprint 最大成果：

## Proposal 品質提升

所有功能皆先 Proposal。

Human Review 後才開始實作。

大幅降低返工。

---

## Human Test 發揮價值

多個重要問題並非程式閱讀發現，而是 Human Test 發現：

- Parallel Blocking
- Queue Card UX
- HTTP 429 Root Cause

證明 Human Test 為必要流程。

---

## Scope Control

所有 Task 均控制於最小修正範圍：

- Bug Fix
- UI Improvement
- Error Handling

避免 Scope 擴張。

---

## Git Discipline

持續遵守：

- One Task = One Commit
- Sprint 統一 Push
- No Push Before Integration Test

Git History 保持乾淨。

---

# Problems Found

## Queue Card Information Hierarchy

目前 Queue Card 展開後資訊量仍偏大。

雖然已支援收合，

但預設畫面仍不夠簡潔。

已列入 Product Backlog。

---

## Error Source Identification

相同 HTTP Status 可能來自不同來源：

例如：

HTTP 429

可能代表：

- Gemini API
- YouTube
- 其他第三方服務

不能僅依 Status Code 判斷錯誤來源。

---

## Retry Scenario

部分 Error（429 / 503）不容易人工重現。

未來應持續累積真實案例。

---

# Root Cause Analysis

本 Sprint 最重要 Root Cause：

HTTP 429 並非一定代表 Gemini API 額度不足。

真正案例：

```text
YouTube Subtitle Download

↓

yt-dlp

↓

HTTP 429

↓

Retry

↓

Success
```

因此：

Error Classification 必須依照：

- Stage
- Source
- Raw Message

共同判斷。

---

# Key Lessons Learned

- Human Test 比 Code Review 更容易發現真實問題。
- Error Classification 必須依照 Stage + Source 判斷，不能只依 HTTP Status。
- Product Backlog 有助於控制 Scope，避免為了完成 Sprint 而加入沒有驗收標準的功能。
- Proposal → Human Review → Human Test → Commit（No Push）流程已驗證有效，可持續作為 AI Product Factory 的標準開發流程。

---

# Process Improvements

本 Sprint 驗證成功的新流程：

```text
Proposal

↓

Human Review

↓

Implementation

↓

Human Test

↓

Acceptance Test

↓

Commit (No Push)
```

建議正式納入：

AI_Product_Factory_Standard v3.1

---

# Product Backlog

已新增：

## Queue Card UX

預設保持簡潔：

- One Sentence Summary
- 學習入口
- 詳細內容預設收合

---

## Error Classification

字幕下載 429 目前被 `main.py` 靜默吞掉，若後續 Whisper fallback 也失敗，使用者看到的是 generic 的「找不到可用的逐字稿內容」，蓋掉了真正的 429 原因。

修正需要同時改 `app/main.py`（保留字幕錯誤文字）與 `app/error_messages.py`（新增字幕＋429 專屬分類），超出 Task 4 只改 `error_messages.py` 的範圍，未納入本 Sprint Scope。

---

## Structure Detection

改善一致性（Task 5，Deferred）。

觸發條件：等之後再次遇到真實的 `structure_type` 判斷不一致案例（記錄該案例的影片與兩次不同的判斷結果），再依該案例修正與驗收。

---

## Sprint 8.5（Beta Polish，待評估）

Queue Card 資訊層級預設簡潔化、學習入口依學習時間排序、其他 Beta 實際使用過程中發現的 UX 細節。屬於產品體驗優化，Sprint 8 Push 後再確認是否成立。

---

# Action Items

Sprint 08（已完成）：

- Task 1／Task 3／Task 2／Task 4 完成並驗收
- Task 5 決定 Deferred（Product Backlog）
- Integration Test（6 項）全數 PASS
- 統一 Push

Sprint 08.5（待評估，Push 後由使用者決定是否成立）：

- Queue Card 資訊層級預設簡潔化
- 學習入口依學習時間排序
- 其他 Beta 使用過程中發現的 UX 細節

Product Backlog（等待觸發條件，非排定 Sprint）：

- Structure Detection 一致性改善（等真實不一致案例）
- 字幕下載 429 被靜默吞掉的 Error Path 修正

---

# Key Metrics

Completed Tasks:

- Task 1
- Task 2
- Task 3
- Task 4

Deferred to Product Backlog:

- Task 5（無可重現案例，等待真實案例後再處理）

Commits:

One Task = One Commit（Task 1: `67dfc78`／Task 3: `5fb3aac`／Task 2: `b89fc3b`／Task 4: `8a7a520`／Task 5 Deferred + Backlog 更新: `d2f7d89`）

Push Strategy:

One Sprint = One Push（Integration Test PASS 後執行）

---

# Final Reflection

Sprint 08 並沒有新增大量功能。

真正的成果是：

產品品質。

透過 Proposal、Human Review、Human Test 與 Product Backlog 的流程，

YB Learn 已逐步建立一套可重複、可維護且適合 AI 協作的開發模式。

本 Sprint 不只是改善產品，

也驗證並強化了 AI Product Factory 的開發標準。

Task 5 最終選擇不做，而不是硬做一個無法客觀驗收的修正，本身就是這套標準（可驗收的 Bug 優先）發揮作用的證明。

Sprint 8 Integration Test 已全數 PASS，準備統一 Push，並由使用者決定是否接著進行 Sprint 8.5（Beta Polish）。