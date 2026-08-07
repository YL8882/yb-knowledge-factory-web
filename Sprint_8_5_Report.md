# Sprint 8.5A 完成報告

【本次完成】
- Task 1 — Correlation ID 基礎建設 + Runtime Intelligence：`queue_store.add_item()` 產生 `request_id`（uuid4）並鏡射進 `history_store`，貫穿 Queue／Transcript／Gemini／Study Note／Download 全流程；新增 `app/observability/`（`logger.py`／`runtime_metrics.py`／`daily_report.py`），記錄四階段起訖時間與成功/失敗至 `outputs/logs/runtime.jsonl`，`daily_report.json` 即時增量更新
- Task 2 — Cost Intelligence：`gemini_client.py` 建立單一攔截點 `_generate_content()`，涵蓋全部 7 個 `generate_*()` 函式，讀取 `response.usage_metadata` 換算估算成本（USD），寫入 `outputs/logs/gemini_usage.jsonl`；追加所有 `estimated_cost` 補上 `currency` 欄位、新增只計入核心流程呼叫的 `study_package` 統計
- Task 3 — Cache Intelligence：既有 7 處 `find_cached_*` 快取檢查點記錄 Hit/Miss 與估算節省成本至 `outputs/logs/cache.jsonl`，估算優先採當天真實平均成本、無資料時退回 MVP 期間估算值
- Task 4 — Error Intelligence：Gemini 相關失敗集中在 `_generate_content()` 記錄（涵蓋全部 7 種 artifact_type，含先前完全未記錄的 quick_summary 靜默失敗），非 Gemini 失敗於既有 4 個 `last_error` 記錄點補上；`retry_count` 即時查詢 `errors.jsonl` 得出，不新增 `queue_store` 欄位
- 端對端驗證：以真實處理過的影片（`5o4OsLjINuQ`）追蹤同一組 `request_id`，確認 4 份 JSONL log 與 `daily_report.json` 完全一致

【目前可測試】
1. 完整跑一次 YouTube → Transcript → Study Note → Download，MVP 行為與 Sprint 8.5A 之前完全一致
2. `outputs/logs/runtime.jsonl`／`gemini_usage.jsonl`／`cache.jsonl` 皆以同一組 `request_id` 串起同一支影片的完整流程
3. `outputs/reports/daily_report.json` 即時反映 Runtime／Usage／Cache／Study Package／Errors 統計，無需等待每日批次
4. 將環境變數 `PRODUCT_INTELLIGENCE_ENABLED` 設為 `false` 後，MVP 功能正常但不產生任何 `outputs/logs/`、`outputs/reports/` 內容

【Known Issues】（本 Sprint 新增至 Product Backlog）
- `GeminiConfigError`（缺少 `GEMINI_API_KEY`）與 5 個獨立 Learning Model 端點的非 Gemini 失敗，目前不在 Error Intelligence 記錄範圍
- `POST /api/queue` 的無效網址／找不到影片拒絕點發生在 `request_id` 產生之前，完全不會留下任何紀錄——Human Test 期間使用者提出，屬 Product Analytics 範疇，非本次 Error Intelligence 必備功能
- Download 事件目前計入 Runtime Event，會因使用者重複下載產生大量紀錄——使用者確認暫不調整，待 Sprint 8.5A 全部完成後再一併檢討是否改列為 User Action
- Error Intelligence 的 Exception 路徑測試（例如移除 API Key）建議改由未來自動化／單元測試覆蓋，本次 Human Test 未涵蓋

【Regression Check】
- Sprint 1～8 既有功能（Chrome Extension、Transcript、Study Note、Knowledge Package Export、History、Rapid Learning／Learning Blueprint／Teach Back／Action List／Review）：PASS，每個 Task 皆以真實流程重新驗證一次
- Task 1～4 皆改動 `app/main.py`／`app/gemini_client.py` 的重疊區域，疊加後既有端點行為不受影響
- UI（`templates/`／`static/`）、所有 Prompt 內容、既有 API 回傳格式：全程未修改

【Environment】
- Backend：FastAPI + Uvicorn（`python run.py`），http://127.0.0.1:8000
- AI Provider：Gemini 2.5 Flash（`GEMINI_API_KEY`，沿用既有設定，未新增依賴）
- 新增環境變數：`PRODUCT_INTELLIGENCE_ENABLED`（預設開啟，選填）

【Test Artifacts】
- Human Test 逐項記錄：見 `Acceptance_Test.md` Sprint 8.5A 章節（Task 1／2／3／4／End-to-End Validation）
- 真實資料驗證：`outputs/logs/runtime.jsonl`（80 行）、`gemini_usage.jsonl`（7 行）、`cache.jsonl`（248 行）、`outputs/reports/daily_report.json`，皆由使用者實際操作產生，非模擬資料

【Sprint 封存】
- 驗收日期：2026-08-07
- 驗收結果：PASS
- 狀態：Sprint 8.5A 已完成全部 Task 與端對端驗證，Documentation Update 完成，尚待 Commit／Push（由使用者決定時機與方式）

【尚未完成】
無——Task 1～4 與端對端驗證皆已完成並驗收。已知限制（見上方 Known Issues）已全數記錄於 `TODO.md` Product Backlog。

【下一個 Sprint】
Engineering Kickoff Sprint 8.5 文件第 16 節已定義 Sprint 8.5B（Visualization Layer：Runtime Dashboard／Cost Dashboard／Product Dashboard），完成 Product Intelligence Foundation 第二階段；另有未排定編號的 Beta Polish Backlog（Queue Card 資訊層級、學習入口排序）。兩者皆待 Sprint 8.5A Push 後由使用者決定排入順序。
