# Sprint 3 完成報告

【本次完成】
- Workspace 帶入網址後自動觸發 Transcript 下載（無需手動點擊）
- 重用既有 Transcript 模組（字幕優先 + yt-dlp/Whisper 備援、快取）
- Transcript 內容顯示於 Workspace 頁面
- 提供「下載 Transcript.md」按鈕
- 加入 Queue 不再自動串接 Study Note（改為 Sprint 4 獨立功能）

【目前可測試】
1. 從 YouTube 點擊「YB Learn」→ Workspace 自動開啟並自動開始下載 Transcript，完成後頁面顯示內容，可點按鈕下載 Transcript.md
2. 在 Workspace 手動貼上網址並按「加入暫存區」，同樣只產生 Transcript，不會自動產生 Study Note
3. Transcript 失敗時顯示明確錯誤訊息，並提供「重試」按鈕

【Known Issues】
- 開發過程中本機測試環境曾出現 port 8000 殘留舊版 process（`taskkill`／`Stop-Process` 皆無法關閉），導致一次測試誤判成「自動觸發了 Study Note」。已改用獨立測試 port 排除干擾，確認程式邏輯本身正確。建議實際驗收前先用工作管理員確認 8000 port 只有一個 `python.exe` 在跑。

【Regression Check】
- Sprint 1（Extension 按鈕／URL 擷取）：程式碼未觸及
- Sprint 2（`/api/capture`、CORS、自動開啟 Workspace、網址預帶入）：程式碼未觸及；同一顆 `addToQueue()` 在 Sprint 3 流程中被重用，間接驗證仍正常運作
- 既有「暫存區」多筆項目 UI、刪除、重試：未變動
- `POST /api/queue/{id}/study-note`（手動觸發）：已individually 驗證仍可正常運作，未被本次改動破壞

【Environment】
- Backend：FastAPI + Uvicorn（`python run.py` 或 `啟動YB知識工廠.bat`），http://127.0.0.1:8000
- 驗證時另於獨立測試 port 8001 執行（`python -m uvicorn main:app --port 8001`），避開本機殘留 process 干擾
- Chrome Extension：Manifest V3（content script + background service worker）

【Test Artifacts】
- 後端自動化驗證（curl，於乾淨測試 port 8001）：
  - `POST /api/queue`（測試影片 9bZkp7q19f0）→ 狀態依序 Queued → Transcribing → Transcript Ready，`study_note_path` 全程為 false
  - `GET /api/queue/{id}/transcript/download` → 200，內容含正確標題／網址／Transcript
  - `POST /api/queue/{id}/study-note`（手動觸發）→ 200，確認獨立端點未被破壞
- Commit：`b9d7c68 feat(transcript): Sprint 3 Transcript Download MVP`
- 測試過程新增的輸出檔案（供參考，可自行於暫存區刪除）：`outputs/transcripts` / `outputs/study_notes` 下 `dQw4w9WgXcQ`（Rick Astley，發現殘留 process 問題的測試）與 `9bZkp7q19f0`（PSY，乾淨驗證用）

【尚未完成】
⬜ Study Note
⬜ Markdown Export
⬜ AI Analysis

【下一個 Sprint】
Sprint 4：Study Note
