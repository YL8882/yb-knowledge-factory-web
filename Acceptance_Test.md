---
title: Acceptance Test
product: YB Knowledge Lite
version: v2.0
status: Active
purpose: MVP sprint acceptance checklist.
---

# Acceptance Test

## Sprint 1 — Chrome Extension

### Extension

- [x] Extension installed successfully
- [x] Loaded from local project
- [x] No installation errors

### YouTube Integration

- [x] YB Learn button displayed
- [x] Button position correct
- [x] Button clickable

### URL Capture

- [x] Current YouTube URL detected
- [x] Toast notification displayed
- [x] Console output correct
- [x] No JavaScript errors

### Sprint Result

- [x] Sprint 1 completed

---

## Sprint 2 — Backend API

### API Connection

- [x] Backend running
- [x] API reachable
- [x] Extension sends URL successfully
- [x] API returns success response

### Workspace Auto-Open

- [x] Clicking YB Learn opens the Workspace (http://127.0.0.1:8000/) automatically
- [x] Captured YouTube URL pre-filled into the Workspace input
- [x] Pre-fill only — Transcript generation still requires an explicit "加入暫存區" click

### Sprint Result

- [x] Sprint 2 completed

**Test Date:** 2026-08-02
**Test Result:** PASS

**Note:** Backend access log 未顯示於目前終端機，原因為背景已有另一個 Uvicorn Process，實際 API 已成功收到 OPTIONS + POST /api/capture 200 OK，功能正常。

---

## Sprint 3 — Transcript

- [x] Transcript generated
- [x] Transcript displayed
- [x] Error handling completed

### Sprint Result

- [x] Sprint 3 completed

**Test Date:** 2026-08-02
**Test Result:** PASS (verified on an isolated test port — see CHANGELOG for a note on a stray dev-server process on port 8000)

---

## Sprint 4 — Study Note

- [x] Study Note generated
- [x] Content quality verified
- [x] Chapter structure correct

### Sprint Result

- [x] Sprint 4 completed

**Test Date:** 2026-08-02
**Test Result:** PASS (verified on an isolated test port; see Sprint_04_Report.md)

---

## Sprint 4.1 — Workflow Stabilization

Not a Sprint 5 (Markdown Export) deliverable — stabilization patch between Sprint 4 and Sprint 5. See `Sprint_04.1_Workflow_Stabilization_Report.md` for full RCA and test log.

- [x] 全新影片 → Transcript → Study Note → Preview → Download → Completed
- [x] Single Queue
- [x] Single Worker
- [x] Stage Guard（Forward Only）
- [x] Workflow Forward Only

### Sprint Result

- [x] Sprint 4.1 completed

**Test Date:** 2026-08-03
**Test Result:** PASS

**Known Intermittent Issue:** Study Note 偶發卡住／下載階段失敗（`last_error_stage=download`）觀察到 2 次，個別重測、獨立 yt-dlp 診斷、密集情境重現測試（Run 1～3、Run 6）均無法重現，未發現與影片長度或 Transcript 大小相關的固定規律。列為 Known Intermittent Issue，移入 Product Backlog 觀察，不視為本次阻擋項，亦不視為已永久解決。

---

## Sprint 5 — Knowledge Package Export

重新定義範圍：不再是 Markdown Generate（Transcript.md / Study_Note.md 已存在），改為將既有 Markdown 檔案整理成單一知識包。

### Task 1 — Markdown Package Export

- [x] 每支影片完成後可匯出單一知識包（`.zip`）
- [x] 匯出結構：`<Video Title>/Transcript.md`、`<Video Title>/Study_Note.md`
- [x] 下載成功（瀏覽器點擊「📦 下載知識包」按鈕，下載並解壓縮驗證內容正確）

**Test Date:** 2026-08-03
**Test Result:** PASS

**過程記錄：** 首次人工驗收發現 `GET /api/queue/{video_id}/export` 回傳 404；RCA 定位為 port 8000 上同時有新舊兩個 server process 殘留（舊 process 未終止），實際回應請求的是不含新路由的舊 process，非程式碼問題。終止舊 process（PID 17364、13608）後，僅保留新 process（PID 2000、27776），重新測試 route 回應 200、zip 結構正確，人工驗收通過。

### Task 2 — Bulk Knowledge Package Export

- [x] Queue 列表「📦 匯出全部知識包」按鈕，一次匯出所有已完成影片
- [x] Zip 內部結構：每支影片各自獨立資料夾 `<Video Title>_<video_id>/`，`video_id` 後綴避免不同影片互相覆蓋
- [x] 完整性檢查：任一影片缺少 Transcript.md 或 Study_Note.md，整批匯出中止並回傳明確錯誤，不產生不完整 ZIP

**Test Date:** 2026-08-03
**Test Result:** PASS

**過程記錄：** 首次人工驗收下載成功但 Windows 內建解壓縮顯示「壓縮資料夾無效」。RCA 確認：`build_bulk_package()` 有正確在 `zf.close()` 後才回傳、`FileResponse` 回傳內容與建立內容一致、`zipfile.testzip()` 通過、WinRAR 可正常開啟 —— 確認 zip 本身完全正常，非建立流程或 FileResponse 問題。進一步比對 43 個資料夾名稱，唯一異常是其中一個含有 🔥（Emoji，BMP 之外字元），為 Windows 內建解壓縮工具已知的相容性限制。修正 `app/knowledge_package.py` 的 `_sanitize_filename()` 為白名單邏輯（保留中文/英文/數字/空白/`-`/`_`/`()`/`[]`，移除 Emoji 與控制字元）後，重新下載驗證：zip 大小改變（確認內容真的更新）、`testzip()` 通過、資料夾名稱不再含 BMP 之外字元，人工重新驗收通過（所有資料夾文件正常）。

### Task 3 — Knowledge Library UI

History 頁面重新定位為 Knowledge Library：每支影片一張卡片，展示 Knowledge Package 而不只是紀錄。

- [x] 每張卡片顯示 Transcript／Study Note／Knowledge Package 三項狀態
- [x] 「📦 下載知識包」為主要按鈕，與「開啟 Transcript」「開啟 Study Note」「回到 YouTube」次要按鈕視覺區隔
- [x] 「開啟 Transcript」「開啟 Study Note」在新分頁顯示內容，不強制下載
- [x] 缺檔情境：Study Note／Knowledge Package 正確顯示「⚠ 缺失」，下載按鈕與對應開啟按鈕正確隱藏，Transcript 開啟按鈕不受影響（獨立判斷）

**Test Date:** 2026-08-03
**Test Result:** PASS

**過程記錄：** 人工驗收過程中兩度懷疑程式邏輯有誤（正常情境畫面缺少狀態列與按鈕；缺檔情境下載按鈕未隱藏、Transcript 開啟按鈕誤消失）。逐一比對 server 實際回應與硬碟原始檔案（`diff` 結果完全一致）、直接呼叫 `GET /api/history` 確認資料正確，確認程式碼本身無誤；兩次現象皆為瀏覽器快取舊版 `history.js`／`history.html`／`style.css` 造成，強制重新整理（Ctrl+Shift+R）後正常情境與缺檔情境共 12 項檢查全數通過。測試用暫時移除的 `Study_Note.md` 已還原。過程中另發現一個獨立既有缺口：Queue 頁面的下載按鈕只檢查 `queue_store` 的 path 欄位、未驗證檔案是否還在磁碟上，已記錄於 Product Backlog，非本次範圍。

### Task 4 — History Bulk Export

History 頁面新增「📦 匯出全部知識包」按鈕，依磁碟實際檔案打包所有已完整的影片（Transcript + Study Note 皆存在），缺檔影片自動排除，不計入本次匯出。

- [x] 正常情境：History 頁面顯示按鈕，點擊後下載 zip，內容為所有完整影片各自資料夾（`<Video Title>_<video_id>/Transcript.md`、`Study_Note.md`）
- [x] 部分缺檔情境：缺 Study Note 的影片自動排除、不出現在 zip 中，其餘完整影片正常匯出，不顯示錯誤訊息
- [x] 全部缺檔情境（無任何完整項目）：不下載空 ZIP，畫面顯示明確錯誤訊息「目前沒有已完成的知識包可匯出」
- [x] 單張卡片狀態不受影響：Transcript／YouTube 連結維持顯示，Study Note 缺失時對應「開啟」按鈕與匯出資格正確反映

**Test Date:** 2026-08-04
**Test Result:** PASS

**過程記錄：** 人工驗收分三個情境進行。情境 1／2（頁面顯示、正常匯出）以既有真實資料直接測試。情境「部分缺檔」與「全部缺檔」的測試資料由 Assistant 建立與復原：分別將特定影片的 `Study_Note.md`（部分缺檔情境：2 個檔案）與全部 96 個 `Study_Note.md`（全部缺檔情境）暫時移至 Repository 外的暫存目錄，測試後依還原清單（manifest）移回原位，過程未修改 `outputs/history.json`／`outputs/queue.json`，也未由使用者手動搬移或編輯任何檔案。每次還原後皆重新計算磁碟上「Transcript + Study Note 皆存在」的項目數與 `git status` 異動筆數，確認與測試前基準一致（完整項目數 87、study_notes 檔案數 96、`git status` 未追蹤檔案數 127 不變），確認 Repository 未留下任何測試殘留。

### Sprint Result

- [ ] Sprint 5 completed（Task 1、Task 2、Task 3、Task 4 完成，待後續 Task 指示）

---

# MVP Acceptance

The Lite MVP is complete when:

- [ ] Chrome Extension works
- [ ] Backend API connected
- [ ] Transcript generated
- [ ] Study Note generated
- [ ] Markdown exported
- [ ] End-to-end workflow completed

```text
YouTube
    ↓
YB Learn
    ↓
Transcript
    ↓
Study Note
    ↓
Markdown
```

---

# Definition of Done

A Sprint is complete only if:

- [ ] Feature implemented
- [ ] Manual testing passed
- [ ] No console errors
- [ ] Git commit completed
- [ ] Acceptance Test updated