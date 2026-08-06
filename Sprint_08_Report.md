# Sprint 8 完成報告

【本次完成】
- Task 1 — Gemini 呼叫失敗 Error Path：Learning Blueprint／Teach Back／Action List／Review 呼叫 Gemini 失敗時，錯誤訊息改為顯示在觸發的那個按鈕旁邊（inline），取代原本只寫入頁面頂部、可能捲動出畫面外的 `#status`；按鈕本身即為重試入口
- Task 3 — Loading／Processing 狀態一致化：5 個模組（Rapid Learning／Learning Blueprint／Teach Back／Action List／Review）處理中皆顯示統一 Loading 樣式，並修正輪詢重繪期間 Loading 狀態被意外重置的問題；Human Test 過程中另外發現並修正一個獨立 Bug——5 個端點內直接同步呼叫 Gemini SDK，卡住 uvicorn 事件迴圈，導致不同影片的獨立操作互相阻塞（非既有 Single Worker Queue 設計），已改用 `asyncio.to_thread` 修正
- Task 2 — Queue Card 模組展開／收合：5 個模組標題列皆可獨立點擊展開／收合（非 Accordion，無互斥、無自動收合），預設維持展開，Teach Back／Action List／Review 的下載按鈕收合狀態下仍可使用
- Task 4 — `classify_error()` 分類精確度改善：Quota／Rate Limit／Auth 相關錯誤訊息依 stage 分流，`download`／`transcript` 階段不再誤標成 Gemini 額度問題；以使用者實際遇到的 YouTube 字幕下載 429 真實案例作為正式驗收證據
- Task 5 — Structure Detection 一致性改善：**決定延後至 Product Backlog**，原因是目前沒有可穩定重現的 `structure_type` 判斷不一致案例，無法建立 Before／After 比較與客觀 PASS／FAIL 標準，依「可驗收的 Bug 優先」原則暫不處理

【目前可測試】
1. 任一支已產生 Study Note 的影片，依序觸發 Rapid Learning → Learning Blueprint → Teach Back → Action List → Review，全部正常產生，Loading／完成狀態正確
2. 對尚未建立 Learning Blueprint 的影片觸發 Teach Back／Action List／Review，錯誤訊息正確顯示在按鈕旁，可直接重新點擊重試
3. 一支影片仍在自動跑 Transcript／Study Note 期間，同時對另一支已完成的影片觸發任一 Learning Model 模組，可立即開始、不互相阻塞
4. 每個模組的展開／收合各自獨立操作，收合後下載按鈕仍可使用，收合再展開內容不消失、不重新呼叫 API
5. Queue／History／Export／Chrome Extension 既有功能不受影響

【Known Issues】（本 Sprint 新增至 Product Backlog）
- Queue Card 預設保持簡潔（只顯示一句話重點＋學習入口，詳細內容預設收合）——Task 2 Human Test 提出的 UX Improvement，非本次範圍
- 字幕下載 429 目前被 `main.py` 靜默吞掉，Whisper fallback 也失敗時會顯示「找不到可用的逐字稿內容」而非真正的 429 原因——Task 4 Human Test 發現的真實案例，修正需同時改 `app/main.py` 與 `app/error_messages.py`，超出 Task 4 Scope
- Structure Detection 一致性改善——Task 5 延後項目，等待真實不一致案例出現後再處理
- Sprint 8.5（Beta Polish，暫定）——Queue Card 資訊層級、學習入口排序等體驗優化，待 Sprint 8 完成後再確認是否成立

【Regression Check】
- Sprint 1～7 既有功能（Chrome Extension、Transcript、Study Note、Knowledge Package Export、History、Rapid Learning／Learning Blueprint／Teach Back／Action List／Review 的既有生成邏輯）：PASS，Integration Test 涵蓋一次完整迴歸
- Task 1／2／3 皆改動 `app/static/script.js` 的重疊區域（5 個模組的渲染／按鈕邏輯），三者疊加後功能不互相干擾，Human Test 逐一驗證通過
- Task 3／4 皆改動 `app/main.py`／後端錯誤處理路徑，疊加後既有端點行為不受影響

【Environment】
- Backend：FastAPI + Uvicorn（`python run.py`），http://127.0.0.1:8000（`reload=True`，本 Sprint 期間持續沿用同一個執行中的 process）
- AI Provider：Gemini 2.5 Flash（`GEMINI_API_KEY`，沿用既有設定，未新增依賴）
- Chrome Extension：Manifest V3（未於本 Sprint 修改）

【Test Artifacts】
- Commit：
  - Task 1：`67dfc78`
  - Task 3：`5fb3aac`
  - Task 2：`b89fc3b`
  - Task 4：`8a7a520`
  - Task 5 延後說明／Product Backlog 更新：`d2f7d89`
- Human Test 逐項記錄：見 `Acceptance_Test.md` Sprint 8 章節（Task 1／2／3／4，含 Task 4 的 YouTube 429 真實案例）
- Integration Test：6 項（End-to-End、Error Path × Loading、平行處理、展開／收合、錯誤分類、既有功能全面迴歸）全數 PASS

【Sprint 封存】
- 驗收日期：2026-08-06
- 驗收結果：PASS
- 狀態：Sprint 8 已完成 Integration Test，準備統一 Push

【尚未完成】
⬜ Task 5 — Structure Detection 一致性改善（延後至 Product Backlog，等待真實不一致案例出現後再依該案例修正與驗收）

【下一個 Sprint】
待確認：Sprint 8 Push 後，是否安排短 Sprint 8.5（Beta Polish：Queue Card 資訊層級、學習入口排序等 UX 細節）或直接進入 Sprint 9，由使用者決定。
