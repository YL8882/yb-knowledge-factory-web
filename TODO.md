---
title: TODO
product: YB Knowledge Lite
version: v2.0
status: Active
purpose: Development task list and product backlog.
---

# TODO

> Sprint breakdown kept in sync with `Acceptance_Test.md`.

## Sprint 1 — Chrome Extension ✅ Completed

- [x] Create Chrome Extension project
- [x] Inject "YB Learn" button into YouTube
- [x] Detect current YouTube URL
- [x] Send URL to Backend API
- [x] Show processing status

---

## Sprint 2 — Backend API ✅ Completed

- [x] Receive YouTube URL
- [x] Return success response
- [x] Extension ↔ Backend connected
- [x] Auto-open Workspace with captured URL pre-filled

---

## Sprint 3 — Transcript ✅ Completed

- [x] Generate Transcript
- [x] Transcript Download
- [x] Error handling completed

---

## Sprint 4 — Study Note ✅ Completed

- [x] Generate Study Note
- [x] Content quality verified
- [x] Chapter structure correct

---

## Sprint 4.1 — Workflow Stabilization ✅ Completed

- [x] Stage Guard（Forward Only，已達成階段不重跑）
- [x] Single Execution Path（手動 API 併入單一 worker）
- [x] Worker Recovery（單一 Job 例外不中斷 worker thread）
- [x] Single Queue / Single Worker 驗證
- [x] Single Workspace（Chrome Extension 分頁重用）

不屬於 MVP 功能擴充，為 Sprint 4 與 Sprint 5 之間的穩定性修補，詳見 `Sprint_04.1_Workflow_Stabilization_Report.md`。

Known Intermittent Issue（Study Note 偶發卡住／下載階段失敗）已調查但無法穩定重現，列入 Product Backlog 觀察，非本次阻擋項。

---

## Sprint 5 — Knowledge Package Export

重新定義範圍：Transcript.md / Study_Note.md 皆已產生，不再需要 Markdown Generate；改為將既有 Markdown 檔案整理成單一知識包。

### Task 1 — Markdown Package Export ✅ Completed

- [x] 每支影片完成後可匯出單一知識包（.zip）：`<Video Title>/Transcript.md`、`<Video Title>/Study_Note.md`
- [x] 手動下載（Queue 列表「📦 下載知識包」按鈕）
- [x] 內容驗證（zip 完整性、內部結構正確）

僅新增 Export Layer（`app/knowledge_package.py`、`GET /api/queue/{video_id}/export`），未修改 Workflow 或 AI Pipeline。

未來可擴充（不在本次範圍）：`Metadata.md`、`Images/`、`Prompt.md`

### Task 2 — Bulk Knowledge Package Export ✅ Completed

- [x] Queue 列表新增「📦 匯出全部知識包」按鈕，一次打包所有已完成影片
- [x] Zip 結構：`Knowledge.zip` → `<Video Title>_<video_id>/Transcript.md` + `Study_Note.md`，`video_id` 後綴避免不同影片互相覆蓋
- [x] 完整性檢查：任一影片缺少 Transcript.md 或 Study_Note.md，整批匯出直接中止並回傳明確錯誤，不產生不完整 ZIP

僅新增 Export Layer（`app/knowledge_package.py` 的 `build_bulk_package()`、`GET /api/queue/export-all`），未修改 Workflow 或 AI Pipeline。

**修正記錄：** 首次人工驗收下載後 Windows 內建解壓縮顯示「壓縮資料夾無效」。RCA 確認 zip 本身完全正常（`zipfile.testzip()` 通過、WinRAR 可正常開啟），根本原因是資料夾名稱含 Emoji（BMP 之外字元），Windows 內建解壓縮工具對此不相容。修正 `app/knowledge_package.py` 的 `_sanitize_filename()`，改為白名單邏輯（僅保留中文、英文、數字、空白、`-`、`_`、`()`、`[]`，移除 Emoji 與控制字元），修正後重新驗收通過。

### Task 3 — Knowledge Library UI ✅ Completed

History 頁面重新定位為 **Knowledge Library**：不再只是瀏覽紀錄，而是每支影片的知識包卡片。

- [x] 每張卡片顯示 Transcript／Study Note／Knowledge Package 三項狀態（Knowledge Package 為衍生欄位，不額外儲存）
- [x] 「📦 下載知識包」為主要按鈕，與「開啟 Transcript」「開啟 Study Note」「回到 YouTube」的次要按鈕區分開，避免視覺焦點分散
- [x] 「開啟 Transcript」「開啟 Study Note」在新分頁顯示內容，不強制下載
- [x] 缺檔（Knowledge Package = Incomplete）時，下載按鈕與對應的「開啟」按鈕自動隱藏

僅新增 Export／History Layer（`GET /api/history` 新增衍生欄位、`GET /api/history/{video_id}/export`、`GET /api/history/{video_id}/transcript`、`GET /api/history/{video_id}/study-note`），未修改 `history_store.py`、Workflow、Stage Guard、Single Worker、Queue Pipeline。

**過程記錄：** 人工驗收過程中兩度因瀏覽器快取舊版 `history.js`/`history.html`/`style.css` 造成誤判（畫面缺少狀態列與按鈕），經比對 server 端實際回應與硬碟原始檔案確認程式碼本身正確；強制重新整理（Ctrl+Shift+R）後功能全部正常。另發現一個獨立、非本次範圍的既有缺口：Queue 頁面（Task 1/2）的「下載知識包」按鈕僅檢查 `queue_store` 的 `study_note_path` 欄位是否存在，未驗證檔案是否仍在磁碟上，已記錄於 Product Backlog。

### Task 4 — History Bulk Export ✅ Completed

- [x] History（知識庫）頁面新增「📦 匯出全部知識包」按鈕，一次匯出所有已完整（Transcript + Study Note 皆存在於磁碟）的影片
- [x] 資料來源改用磁碟實際檔案驗證（`history_store` + `find_cached_transcript`／`find_cached_study_note`），而非 `queue_store` 的 path 欄位
- [x] 缺檔影片（Study Note 或 Transcript 缺失）自動排除，不計入本次匯出，其餘完整項目正常匯出
- [x] 完全沒有可匯出項目時，回傳明確錯誤訊息，不下載空 ZIP

僅新增 Export／History Layer（`GET /api/history/export-all`，重用 `knowledge_package.build_bulk_package()`），未修改 Workflow、Queue、Stage Guard、Single Worker、Pipeline、`knowledge_package.py`、`queue_store.py`、`history_store.py`。

與 Task 2（`GET /api/queue/export-all`）的差異：Task 2 採「整批中止」（任一項目缺檔則全部取消），Task 4 採「自動排除」（缺檔影片不計入，其餘正常匯出）——因為 History 頁面本來就允許單一影片缺檔（Task 3 卡片邏輯），沿用 Task 2 的中止語意並不合理。

### Task 5 — Queue Export Disk-Verification Parity ✅ Completed

- [x] `GET /api/queue` 回應新增 `transcript_exists`／`study_note_exists` 衍生欄位（比照 `GET /api/history`）
- [x] Queue 列表「📦 下載知識包」按鈕改依磁碟實際檔案顯示，不再只信任 `queue_store` 的 path 欄位
- [x] `GET /api/queue/export-all` 候選判斷改用磁碟實際檔案，缺檔項目自動排除、不再讓整批匯出中止（語意比照 Task 4 `/api/history/export-all`）

僅修改 `app/main.py`、`app/static/script.js`；沿用既有 `knowledge_package.build_package()`／`build_bulk_package()`，未新增第二套 zip 建立邏輯；未修改 Workflow、Queue Pipeline、Stage Guard、Single Worker、Transcript／Study Note 產生流程、History UI、`queue_store.py`（僅讀取，未新增寫入）。卡片上「Transcript／Study Note ✓ 已產生」的 checklist 文字維持原本邏輯（依 `item.status` 判斷流程進度，非磁碟驗證）——刻意不動，因為那是 Workflow 顯示邏輯，不在本次 Export Layer 範圍內。

呼應並收斂 Product Backlog 中「Queue 頁面下載按鈕未驗證磁碟」的已知缺口（Task 3、Task 4 過程記錄中皆有提及）。

**過程記錄：** 人工驗收共進行 3 個情境，過程中出現兩次誤判需要 RCA 才能釐清：(1) Scenario 3（全部缺檔）首次測試顯示「FAIL」——實際重現與程式碼分析後確認，Backend 邏輯完全正確（直接呼叫 API 得到正確的 404），根本原因是瀏覽器 Downloads 資料夾殘留 10 個先前測試留下的同名 zip 檔案，使用者誤認為是這次點擊產生的新下載；清空 Downloads 後配合強制重新整理重測即正確重現「不下載、顯示無可匯出訊息」。(2) 重建 Scenario 3 過程中一度誤判「仍有完整影片」，經確認該影片實際只存在於 `history.json`（101 筆中不在 Queue 44 筆內的其中一筆），與本次 Queue 測試範圍無關，非測試資料建立錯誤。兩次誤判皆與程式碼本身無關，最終在乾淨的瀏覽器狀態下重新驗收，情境 1／2／3 全數 PASS。

---

## Sprint 6 — Bug Fixes & Extension Enhancements

### Task 1 — Bug Fix: Windows ZIP Path Too Long ✅ Completed

- [x] `knowledge_package._sanitize_filename()` 新增 `_MAX_TITLE_LENGTH = 50` 長度截斷，套用於單支與批次匯出共用的命名邏輯（`build_package()`／`build_bulk_package()` 皆呼叫同一函式，不需分別修改）
- [x] `video_id` 一律在截斷後才接上，確保資料夾／檔名仍然唯一
- [x] 最長標題影片（`video_id=U5YuWsheuIc`，清理後 91 字）驗證：Explorer 解壓完整路徑從 235／244 降到 153／162（Downloads／OneDrive 同步 Downloads），距離 MAX_PATH=260 有約 100 字餘裕
- [x] 短標題不受影響，命名邏輯與修正前一致

僅修改 `app/knowledge_package.py`，未修改 Queue、History、Workflow、Export API、UI、下載流程。

**過程記錄：** Sprint 5 Task 5 Human Test 過程中發現的獨立 Bug，RCA 記錄曾留在 Product Backlog；Sprint 6 Task 1 依 RCA 建議方向（調整 ZIP 內部資料夾命名策略）修正並驗收通過，Backlog 項目移除。

### Task 2 — Chrome Extension 支援 YouTube Shorts ✅ Completed

- [x] Shorts 頁面（`/shorts/*`）正確顯示 YB Learn 按鈕，直接開啟 Shorts 網址也能首次載入就出現
- [x] 點擊後行為與一般影片完全一致：送出至 `/api/capture`、開啟／聚焦 Workspace、自動加入 Queue、自動跑完 Transcript→Study Note
- [x] 首頁 → Watch → Shorts → 搜尋 → Shorts 連續切換，按鈕不重複注入，任何頁面僅一個按鈕
- [x] 一般 `/watch` 影片頁行為不受影響

僅修改 `extension/content.js`（新增 `isShortsPage()`／`isSupportedVideoPage()`，`syncButtonVisibility()` 改用合併後的判斷）。`manifest.json` 的 `content_scripts.matches`（`*://www.youtube.com/*`）本來就涵蓋 `/shorts/*`，不需修改；`extension/background.js`（Single Workspace 邏輯）與所有 `app/` 底下的檔案完全未觸碰。

**關鍵發現：** `app/youtube.py` 的 `extract_video_id()` 正規表示式早就包含 `shorts/` 路徑分支，代表後端本來就能正確解析 Shorts 網址——問題完全出在 Extension 端的按鈕顯示邏輯只認 `/watch`，因此本次修正不需要動到 Web App／Queue／History／FastAPI／Export 任何一行程式碼。

---

## Acceptance

- [ ] Complete end-to-end workflow

YouTube

↓

YB Learn

↓

Transcript

↓

Study Note

↓

Markdown

---

## Product Backlog

Future versions only.

- [ ] Knowledge Cards
- [ ] Quiz + Explanation
- [ ] Mind Map
- [ ] AI Chat
- [ ] Citation
- [ ] Learning Progress
- [ ] Skill Tree
- [ ] AI Mentor
- [ ] Multi-language
- [ ] iOS App
- [ ] Known Intermittent Issue 觀察追蹤（Study Note 偶發卡住／下載階段失敗，目前無法穩定重現；若再次出現需以完整 Log 重新開啟 RCA）
- [ ] `error_messages.classify_error()` stage 判斷精確度改善（避免下載階段錯誤誤標為 Gemini 額度問題）

  **需求：** 目前 Extension 僅支援 `https://www.youtube.com/watch?v=`，未支援 `https://www.youtube.com/shorts/`。Shorts 頁面需顯示 YB Learn 按鈕，點擊直接加入 Queue，不需手動貼網址，體驗與一般影片一致。