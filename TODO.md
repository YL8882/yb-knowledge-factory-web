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

### Task 3 — 待指示

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