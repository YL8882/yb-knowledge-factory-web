---
title: CHANGELOG
product: YB Knowledge Lite
version: v1.0
status: Active
purpose: Track added, changed, fixed, and removed functionality per release.
---

# CHANGELOG

## 2026-08-02

### Added
- Chrome Extension：YouTube 影片頁面注入「YB Learn」按鈕
- Backend `POST /api/capture`：接收並驗證 YouTube 網址，回傳成功狀態
- 點擊 YB Learn 後自動開啟 Workspace 並帶入已擷取的網址
- 帶著網址開啟 Workspace 時自動開始下載 Transcript，完成後於頁面內顯示內容並提供下載按鈕
- Transcript 完成後自動產生 Study Note（Title/Summary/Key Points/Important Concepts/Workflow/Action Items/Tags），於頁面顯示並提供下載按鈕

### Changed
- Study Note 產生改用新的精簡結構化格式，取代舊版 Executive Summary/Key Takeaways 等 10 章節格式
- 加入 Queue 重新自動串接 Study Note 產生（Sprint 3 曾暫時移除，Sprint 4 起 Transcript → Study Note 全自動）

### Fixed
- Extension 重新載入後，已開啟分頁的 content script 連線失效（`Extension context invalidated`）導致訊息無法送出
- Workspace 因瀏覽器快取舊版 `script.js`，導致網址未帶入輸入框
- `sendMessage` 失敗時錯誤訊息誤標為「後端連線失敗」，改為獨立標示為「無法自動開啟 Workspace」

## 2026-08-03

### Added
- `GET /api/queue/{video_id}/export`：將已產生的 `Transcript.md` + `Study_Note.md` 打包成單一知識包（`.zip`），結構為 `<Video Title>/Transcript.md`、`<Video Title>/Study_Note.md`
- Queue 列表新增「📦 下載知識包」按鈕（項目完成後顯示）
- `GET /api/queue/export-all`：一次把所有已完成影片打包成單一知識包 zip，結構為 `<Video Title>_<video_id>/Transcript.md`、`Study_Note.md`
- Queue 列表新增「📦 匯出全部知識包」按鈕
- `GET /api/history/{video_id}/export`：History 頁面單支知識包下載（依磁碟實際檔案，不依賴 Queue 資料）
- `GET /api/history/{video_id}/transcript`、`GET /api/history/{video_id}/study-note`：在新分頁開啟內容，不強制下載
- `GET /api/history` 回應新增 `transcript_exists`／`study_note_exists` 衍生欄位

### Changed
- `POST /transcript`、`POST /study-note` 改走與自動流程相同的單一 worker thread（Single Execution Path），不再各自繞過單一 worker 保證
- Workspace 頁面移除 Transcript 內嵌預覽區塊，僅預覽 Study Note（Transcript 仍會自動下載）
- Chrome Extension 改為重用既有 Workspace 分頁（Single Workspace），不再每次都開新分頁
- History 頁面重新定位為 Knowledge Library：清單改為卡片，每張卡片顯示 Transcript／Study Note／Knowledge Package 狀態，並提供下載知識包（主要按鈕）、開啟 Transcript／Study Note、回到 YouTube（次要按鈕）

### Fixed
- `POST /transcript`、`POST /study-note` 重複呼叫已完成的階段時，會被拉回重跑（新增 Stage Guard，Forward Only）
- Worker thread 遇到未預期例外會整個中斷，導致佇列中後續項目永久卡住（新增 Worker Recovery，例外只影響單一 Job）
- Study Note 產生過程中的未預期例外會被靜默吞掉，Job 卡在「Transcript Ready」且無任何錯誤紀錄
- 前端輪詢在「Transcript Ready」過渡狀態會提早停止，導致畫面停留在「Generating Study Note」不再更新
- Study Note 預覽讀取失敗後不會重試，永久無法顯示
- Chrome Extension 開啟 Workspace 時偶發「message port closed before a response was received」
- 批次匯出知識包（`export-all`）時，資料夾名稱若含 Emoji（BMP 之外字元）會導致 Windows 內建解壓縮工具判定整個 zip 無效；`knowledge_package._sanitize_filename()` 改為白名單邏輯，僅保留中文/英文/數字/空白/`-`/`_`/`()`/`[]`
