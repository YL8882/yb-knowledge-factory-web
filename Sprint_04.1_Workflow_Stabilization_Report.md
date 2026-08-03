# Sprint 4.1 Workflow Stabilization 驗收報告

【範圍說明】
- 本次不屬於 TODO.md 定義的 Sprint 5（Markdown Export），為 Sprint 4 與 Sprint 5 之間的 Workflow Stabilization 修補
- Commit：`fbcae709ce11b922399f9a867c97387389b176a7` — `feat(workflow): stabilize transcript and study note pipeline`

【本次完成】
- Stage Guard：`_STAGE_RANK` / `_stage_rank()`，讓 `POST /transcript`、`POST /study-note` 具備 Forward Only 特性，已達成的階段不會被重複呼叫拉回
- Single Execution Path：手動觸發的 `/transcript`、`/study-note` 改走與自動流程相同的單一 `_pipeline_queue` / worker thread（`_await_job` / `_job_events` / `_job_outcomes`）
- Worker Recovery：`_pipeline_worker_loop` 最外層加上例外捕捉，單一 Job 的未預期例外不會讓 worker thread 整個死掉
- Study Note Pipeline 例外處理強化：`_generate_study_note_for_item` 包一層 wrapper，任何未預期例外都會被記錄到 `last_error`，不會被上層靜默吞掉
- 前端 Preview Fix：`isPipelineActive` 補上 `Transcript Ready` 判斷，避免輪詢在過渡狀態提早停止；`maybeDisplayStudyNote` 失敗時重設guard，允許下次輪詢重試
- Chrome Extension Single Workspace：重用既有 Workspace 分頁（`chrome.tabs.query` + `update`）取代每次都開新分頁；修正 `sendResponse` 造成的 message port 錯誤

【驗收結果】

1. 全新影片 → Transcript → Study Note → Preview → Download → Completed：✅ PASS
   （第一次驗收時發現卡住，RCA 後確認原因是驗收當下使用的是重啟前的舊版程式；重啟 server 套用本次 commit 後重測通過）
2. Single Queue：✅ PASS（連續加入 6 支影片，`queue.json` 的 `created_at` 依序處理，任一時刻僅一筆處於 active 狀態）
3. Single Worker：✅ PASS（同上，未觀察到兩筆同時處於 Downloading/Transcribing/Generating）
4. Stage Guard：✅ PASS（程式邏輯審查確認；驗收過程中重複觸發同一 Job 未出現狀態倒退）
5. Workflow Forward Only：✅ PASS（同上，未觀察到已完成階段被重新執行的情形）

【Intermittent Issue 調查】

問題描述：
- 驗收過程中觀察到 2 次 Study Note 卡住／失敗：
  - `LVCuE7DvffM`（23 分鐘）：`last_error_stage=download`，訊息「AI 處理服務目前無法使用或過於忙碌...（可能是 Gemini API 額度已用完）」，無 Transcript 產出
  - `I553Z1rf1OY`（未滿 15 分鐘）：相同錯誤特徵（同一 stage、同一訊息、同樣無 Transcript 產出）
- 兩次失敗皆發生在短時間內密集新增多支影片（單一測試區段內新增近 20 支影片）的期間

測試結果：
- 兩支失敗影片個別重新測試：皆 ✅ 成功完成 Study Note
- 針對 `I553Z1rf1OY` 執行獨立 yt-dlp 診斷（`--simulate -v`，繞開 app 本身）：成功取得格式資訊，無任何錯誤，僅有一則不影響結果的 JS runtime 警告
- Reproducibility Test（`wXcyq2Ay4uE`，每輪皆清除 Transcript/Study Note 快取檔案後重新執行完整 pipeline）：
  - Run 1（原始）：✅ PASS
  - Run 2：✅ PASS
  - Run 3：✅ PASS
  - Run 4、5：未執行（依驗收者決定，以 Run 1～3 + Run 6 證據視為足夠）
- Run 6（密集情境重現測試，短時間內連續加入多支不同影片，模擬原始失敗當下的情境）：✅ 全部 PASS，未重現問題

無法重現：
- 上述所有重測、獨立診斷、密集情境模擬，均未能重現原始失敗
- 未發現與影片長度、Transcript 字數、Gemini Token 用量相關的固定規律（`error_messages.classify_error()` 之友善訊息文字含「Gemini API 額度」字樣，但 `last_error_stage` 記錄為 `download`，代表實際失敗發生在 yt-dlp 下載階段，非 Gemini 呼叫階段；該訊息文字本身可能具誤導性，屬另一個獨立、非阻擋性的觀察，見下方備註）
- 沒有找到穩定、可預期的觸發條件

結案判定：
1. 目前無法在受控條件下穩定重現 ✅
2. 沒有發現固定觸發條件 ✅
3. Single Queue、Single Worker、Workflow Forward Only 均通過驗收 ✅
4. 本問題列為 **Known Intermittent Issue**，不列為本次 Workflow Stabilization 的阻擋項

**本問題不視為已永久解決。若未來再次出現，須以當次完整 Log（queue.json 該筆完整欄位、終端機 console 輸出、發生當下時間點與前後密集程度）重新開啟 RCA。**

後續觀察策略：
- 若再次出現，優先蒐集：發生當下的 `queue.json` 完整欄位快照、終端機 console 輸出、當時前後 5～10 分鐘內的請求密集程度
- 若可能，於失敗當下（尚未重試前）立即執行獨立 yt-dlp 診斷，比對「失敗當下」與「事後重測」的行為差異（本次診斷是在失敗過後才執行，錯開了真正的失敗時間點，是本次調查的已知限制）
- 現行架構下載階段失敗不會保留原始例外文字（`yt_dlp` 以 `quiet=True` 執行，診斷 log 於本次 Workflow Stabilization 中已移除），若要精確定位下次發生的根因，屆時需評估是否臨時開啟詳細記錄（不在本次範圍內實作，僅作為重新開啟 RCA 時的候選方案）
- `error_messages.classify_error()` 對 `429`/`quota` 等關鍵字的比對不分 stage，可能讓非 Gemini 相關的錯誤（如本次的下載階段錯誤）顯示誤導性訊息；是否修正列為未來待評估項目，非本次範圍

【Environment】
- Backend：FastAPI + Uvicorn，http://127.0.0.1:8000
- AI Provider：Gemini 2.5 Flash（`GEMINI_API_KEY`）
- 驗收期間新增影片數：本次驗收過程中累計新增超過 25 支不同影片進行測試

【Sprint 封存】
- 驗收日期：2026-08-03
- 驗收結果：PASS（Known Intermittent Issue 不視為阻擋項）
- 狀態：Sprint 4.1 Workflow Stabilization 已封存

【下一步】
- Why.md / README.md / CLAUDE.md / outputs/ 測試資料整理（本次驗收前已確認暫不處理）
- 待指示是否開始 Sprint 5（Markdown Export）
