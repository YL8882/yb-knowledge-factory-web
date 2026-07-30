---
Version: v1.0
Status: Active
Owner: YB
Document: TODO
Category: Development
Purpose: Track the current implementation tasks for Claude Code.
Scope: YB Knowledge Factory MVP v0.1
Priority: High
Author: ChatGPT
Last Updated: 2026-07-30
Related Documents:
  - Project_Dashboard.md
  - Product_Index.md
  - PRD.md
  - Engineering_Backlog.md
---

# TODO

> Current Development Tasks

---

# Current Sprint

**Milestone 02 – Build MVP v0.1**

Status

✅ Complete（見 `docs/MVP_Test_Report.md`，待 Product Owner 最終驗收確認）

Goal

完成第一個可正常運作的 MVP。

---

# Priority 1 - Core Features

## Home Page

- [x] 建立首頁版面
- [x] 套用 YB 品牌配色
- [x] 響應式版面（Desktop First）

---

## YouTube Import

- [x] 貼上 YouTube URL
- [x] 驗證網址格式
- [x] 自動取得影片標題
- [x] 新增至 Queue

---

## Queue

- [x] 建立 Queue 清單
- [x] 顯示影片名稱
- [x] 顯示處理狀態
- [x] 支援移除項目

---

## Transcript

- [x] 建立 Transcript API
- [x] 取得逐字稿
- [x] 儲存 Transcript.md

---

## Study Note

- [x] 呼叫 LLM 生成 Study Note
- [x] 套用 Study Note Template
- [x] 儲存 Study_Note.md

---

## Export

- [x] 下載 Transcript.md
- [x] 下載 Study_Note.md

---

# Priority 2 - User Experience

- [x] Loading 動畫（按鈕 disable／文字提示）
- [x] 錯誤訊息提示
- [x] 成功通知
- [x] Queue 完成狀態

---

# Priority 3 - Testing

- [x] YouTube URL 測試
- [x] Transcript 測試
- [x] Study Note 測試
- [x] Markdown 匯出測試

---

# Completed

- Home Page、YouTube Import、Queue、Transcript、Study Note、Export、基本 UX 與測試（見上方 Priority 1–3）
- 詳細驗收紀錄：`docs/MVP_Test_Report.md`

---

# Blocked

> 記錄目前無法完成或等待決策的項目。

---

# Notes

- MVP 階段不新增 Scope。
- 所有新需求先記錄至 Engineering_Backlog.md。
- 優先完成可運作版本，再進行優化。
- 非阻塞性 Known Issues（anyio 版本警告、ffmpeg 未安裝、Queue 無持久化、Gemini 無自動重試等）見
  `docs/MVP_Test_Report.md` 第 5 節，未列入本次 Definition of Done。

---

# Definition of Done

完成以下條件即視為 MVP 完成：

- [x] 可輸入 YouTube URL
- [x] 可取得影片標題
- [x] 可產生 Transcript
- [x] 可產生 Study Note
- [x] 可下載 Transcript.md
- [x] 可下載 Study_Note.md
- [x] 完成基本操作流程測試

---

End of Document