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

## 2026-08-04

### Added
- `GET /api/history/export-all`：History 頁面「匯出全部知識包」，依磁碟實際檔案（`find_cached_transcript`／`find_cached_study_note`，不依賴 `queue_store`）打包所有 Transcript + Study Note 皆存在的影片；缺檔影片自動排除，不計入本次匯出
- History 頁面新增「📦 匯出全部知識包」按鈕
- `GET /api/queue` 回應新增 `transcript_exists`／`study_note_exists` 衍生欄位（比照 `GET /api/history`）
- Chrome Extension 新增 YouTube Shorts（`/shorts/*`）支援：YB Learn 按鈕在 Shorts 頁面正確顯示，點擊行為與一般影片一致（自動加入 Queue，不需手動貼網址）
- `POST /api/queue/{video_id}/knowledge-outline`：Rapid Learning Engine，手動觸發產生 One Sentence（影片核心目的）＋ Knowledge Outline（知識輪廓），存成 `outputs/knowledge_outlines/KO_<title>_<video_id>.md`
- Queue Card 新增「🧠 開始快速學習」按鈕（Study Note 完成後才顯示），點擊後在同一張卡片展開 Quick Learn Layer：One Sentence ＋ 精簡重點永遠可見，完整 Knowledge Outline 預設收合、可展開／收合（純前端切換，不重新呼叫 Gemini）
- 新增 `Learn_Package_Specification_v2.0.md`：Sprint 7 Learn Package 6 模組（One Sentence／Knowledge Outline／Learning Blueprint／Study Note／Teach Back／Action List）規格文件

### Changed
- Queue 頁面「📦 下載知識包」按鈕改依磁碟實際檔案顯示，不再只信任 `queue_store` 的 path 欄位
- `GET /api/queue/export-all` 候選判斷改用磁碟實際檔案，缺檔項目自動排除、不再讓整批匯出中止（語意比照 `/api/history/export-all`）
- Learning Model v1.0 Design Freeze 完成：Learning Phase 正式命名定案（值得學／看懂了／記住了，內部對應 Orientation／Comprehension／Retention）、確認 Knowledge Outline 未來由 Learning Blueprint 取代、定義 Learning Blueprint 7 種候選結構與各 Phase 的目的／輸入／輸出／完成條件；純產品設計，未涉及程式異動

### Fixed
- Knowledge Package ZIP（單支與批次匯出）標題過長時，Windows Explorer 內建解壓縮可能因路徑超過 MAX_PATH（260 字元）而失敗；`knowledge_package._sanitize_filename()` 新增 50 字長度截斷（`video_id` 一律截斷後才接上，確保唯一性不受影響）

## 2026-08-05

### Added
- 新增 `Knowledge_Structure_Engine_v1.0.md`：Knowledge Structure Engine 正式架構規格文件（Design Freeze — Approved），定義 Engine 定位、7 種 Core Structure Taxonomy、Structure／Renderer 分離、Knowledge JSON Layer、兩步驟 Prompt Strategy、Human Test／KPI
- `Why.md` 新增 Vision（Learn Faster / Understand Deeper / Remember Longer）、Product Principles 正式定名為四句（Structure Knowledge／Make It Stick／Reduce Friction／Start Learning）、「Mission 的穩定性」段落與產品決策原則

### Changed
- `POST /api/queue/{video_id}/learning-blueprint`：Gemini 呼叫改為兩步驟（Structure Detection → Knowledge Extraction），輸出結構化 Knowledge JSON（`structure_type` + 對應 `content` 欄位，`response_mime_type="application/json"`、`temperature=0`），取代初版單一線性文字樣板；存檔格式改為 `.json`
- Queue Card Learning Blueprint 顯示區塊改為 pretty-printed JSON（最小可視化，證明不同 `structure_type` 產生不同 `content` 形狀）；依結構分派的正式 Renderer 留待 Sprint 7 Task 4
- `Why.md`「我們真正是什麼」擴充為四層能力對照表（Study Note／Knowledge Structure Engine／Learning Blueprint／Teach Back）

- Queue Card Learning Blueprint 顯示改為依 `structure_type` 分派的排版（Flow 步驟卡片／Comparison 表格／Timeline 時間軸／Decision 決策樹／Classification 分類清單／Cause & Effect 因果箭頭／Problem→Solution 四段卡片／generic 條列），取代 Task 3 的 `JSON.stringify` 顯示

### Known Limitations
- Structure Detection 一致性未達完全穩定：同一支內容特徵模糊的影片，重複生成可能得到不同 `structure_type`（已加 `temperature=0` 改善，未完全消除）
- Gemini 呼叫失敗時的 Error Response 處理未強化，待後續獨立 Bug Fix Task
