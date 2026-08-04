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
- [ ] Queue 頁面（`GET /api/queue/{video_id}/export`、`export-all`）的下載按鈕比照 History 頁面，改為驗證檔案是否仍在磁碟上，而不只是檢查 `queue_store` 的 path 欄位是否存在