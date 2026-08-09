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

### Task 5 — Queue Export Disk-Verification Parity

Queue 頁面的匯出行為改為磁碟驗證，比照 History（Task 4）：`GET /api/queue` 新增 `transcript_exists`／`study_note_exists` 衍生欄位，「📦 下載知識包」按鈕依此顯示；`GET /api/queue/export-all` 候選判斷改用磁碟實際檔案，缺檔項目自動排除、不再整批中止。

- [x] 正常情境：Queue 全部完整 → 各項目按鈕正常顯示 → 「匯出全部知識包」下載成功，ZIP 內容正確
- [x] 部分缺檔情境：缺 Study Note 的項目「下載知識包」按鈕消失，不計入本次匯出；其餘完整項目正常匯出，不整批失敗；Queue 其他功能與 History 頁面不受影響
- [x] 全部缺檔情境：不下載空 ZIP，畫面顯示明確錯誤訊息「目前沒有已完成的知識包可匯出」
- [x] 單支下載（`GET /api/queue/{video_id}/export`）行為不受影響：缺檔時正確回傳 404「Study Note 檔案不存在」

**Test Date:** 2026-08-04
**Test Result:** PASS

**過程記錄：** 人工驗收共 3 個情境，過程中出現兩次需要 RCA 才能釐清的誤判：(1) 全部缺檔情境首次回報 FAIL——直接對執行中的伺服器重現同一請求，確認 Backend 判斷完全正確（回傳預期的 404），根本原因是瀏覽器 Downloads 資料夾殘留 10 個先前測試留下的同名 `YB_Knowledge_Packages*.zip`，使用者誤認為是這次點擊產生的新下載；清空 Downloads 並強制重新整理（Ctrl+Shift+R）後，重新驗證「Network 面板確實送出 `GET /api/queue/export-all`、無新檔案寫入 Downloads、畫面正確顯示無可匯出訊息」，非程式問題。(2) 重建全部缺檔測試資料的過程中，一度誤判「Queue 仍有完整影片」，經比對確認該影片實際只存在於 `history.json`（101 筆中不屬於 Queue 44 筆的其中一筆），與本次 Queue 範圍的測試資料無關。測試用暫時移出的 44 個 `Study_Note.md` 已全部還原，`git status` 未追蹤與已修改檔案數與測試前基準一致（未追蹤 127、新增修改僅 `app/main.py`／`app/static/script.js` 兩個檔案），確認 Repository 未留下任何測試殘留。

### Sprint Result

- [x] Sprint 5 completed（Task 1、Task 2、Task 3、Task 4、Task 5 全部完成並驗收通過）

---

## Sprint 6 — Bug Fixes & Extension Enhancements

### Task 1 — Bug Fix: Windows ZIP Path Too Long

修正 Knowledge Package ZIP（單支與批次匯出）標題過長時，Windows Explorer 內建解壓縮因路徑超過 MAX_PATH（260 字元）而失敗的問題。`knowledge_package._sanitize_filename()` 新增 50 字長度截斷，`video_id` 一律在截斷後才接上以確保唯一性。

- [x] 最長標題影片（`video_id=U5YuWsheuIc`）：ZIP 成功下載、Windows Explorer 正常解壓縮、資料夾名稱已縮短但保留部分標題與 `video_id`、`Transcript.md`／`Study_Note.md` 正常
- [x] 批次匯出：ZIP 正常下載、所有影片資料夾正常、解壓縮正常
- [x] 一般短標題影片：命名正常、不會過度裁切
- [x] Queue／History：畫面正常、單支下載正常、批次下載正常、Export API 正常

**Test Date:** 2026-08-04
**Test Result:** PASS

**過程記錄：** 此 Bug 於 Sprint 5 Task 5 Human Test 過程中發現並完成 RCA，記錄於 TODO.md Product Backlog。Sprint 6 Task 1 依 RCA 建議方向（僅調整 ZIP 內部資料夾命名策略）修正，只修改 `app/knowledge_package.py` 一個檔案，未觸碰 Queue、History、Workflow、Export API、UI、下載流程。Assistant 用正式程式碼與資料庫內最長標題影片自行驗證：Explorer 解壓完整路徑從 235／244 降到 153／162（Downloads／OneDrive 同步 Downloads），並以 `Expand-Archive` 實際解壓縮成功、內容非空後，才交付人工驗收，一次通過。

### Task 2 — Chrome Extension 支援 YouTube Shorts

新增 YouTube Shorts（`/shorts/*`）支援：Shorts 頁面顯示 YB Learn 按鈕，點擊行為與一般影片一致（自動加入 Queue，不需手動貼網址）。

- [x] 直接開啟 `https://www.youtube.com/shorts/...`，首次載入即出現 YB Learn 按鈕
- [x] 點擊後：Workspace 分頁開啟／聚焦、網址正確帶入、自動加入 Queue、自動跑完 Transcript→Study Note，與一般影片相同
- [x] Shorts 摘要流上下滑動切換，按鈕持續正確顯示
- [x] 連續切換首頁 → Watch → Shorts → 搜尋 → Shorts，按鈕不重複注入，任何頁面僅一個按鈕
- [x] 一般 `/watch` 影片頁迴歸測試：按鈕顯示、點擊、加入 Queue、Transcript→Study Note 全流程正常
- [x] Console 無 JavaScript 錯誤

**Test Date:** 2026-08-04
**Test Result:** PASS

**過程記錄：** 檢查 `app/youtube.py` 的 `extract_video_id()` 後發現正規表示式早已包含 `shorts/` 路徑分支，後端本來就能正確解析 Shorts 網址；問題完全出在 `extension/content.js` 的按鈕顯示邏輯只認 `/watch`。修正只新增 `isShortsPage()`／`isSupportedVideoPage()` 判斷，`manifest.json`（`content_scripts.matches` 本來就是 `*://www.youtube.com/*`，已涵蓋 `/shorts/*`）與 `extension/background.js` 皆未修改，`app/` 底下所有檔案也未觸碰，人工驗收一次通過。

### Sprint Result

- [x] Sprint 6 completed（Task 1、Task 2 全部完成並驗收通過）

---

## Sprint 7 — Rapid Learning Engine

### Task 0 — Learning Blueprint Engine：Learn Package Specification v2.0

規格文件，定義 Learn Package 6 個模組（One Sentence／Knowledge Outline／Learning Blueprint／Study Note／Teach Back／Action List）的結構、驗收標準與閱讀動線。未涉及程式、UI、Prompt。

- [x] 文件內容涵蓋 6 個模組定義、閱讀動線、與現有系統的關係、待確認開放問題
- [x] 使用者審閱結構後確認，作為 Task 1 起的設計依據

**Test Date:** 2026-08-04
**Test Result:** PASS（文件審閱確認，非程式驗收）

### Task 1 — One Sentence + Knowledge Outline

Queue Card 新增「🧠 開始快速學習」按鈕，Study Note 完成後才顯示；點擊後產生 One Sentence（影片核心目的）＋ Knowledge Outline（知識輪廓）。

- [x] 一支影片跑完 Study Note 後，Queue Card 顯示「🧠 開始快速學習」按鈕，Queue 完成不會自動觸發
- [x] 點擊後在同一張 Queue Card 展開 One Sentence + Knowledge Outline
- [x] 內容檢查：One Sentence 讀起來像「目的」而非摘要；Knowledge Outline 有段落與功能／關係說明
- [x] 重新整理頁面，已產生的項目直接顯示，不重複呼叫 Gemini
- [x] 多張卡片各自獨立，互不影響
- [x] 迴歸：Transcript、Study Note、Queue、History、Export 不受影響

**Test Date:** 2026-08-04
**Test Result:** PASS

**過程記錄：** 初版 Human Test 回報「Server 200 OK 但畫面沒有變化」，經過兩輪 RCA（先排除 API／JS Exception／DOM 選取錯誤，再加入除錯 Log 定位）確認：不是程式錯誤，是 UI 版位問題——內容原本更新到頁面上方共用的 `processing-panel`，只對應 `trackedVideoId`（最近一次追蹤的單一影片），不是每張 Queue Card 各自一份。改為在 `renderQueue()` 內每張 Queue Card 直接渲染，並移除 RCA 過程加入的所有除錯 Log，重新驗收通過。

### Task 2 — Quick Learn Layer（30 秒學習層）

Rapid Learning 區塊重新設計：預設只顯示 One Sentence ＋ 精簡重點（①～⑤），完整 Knowledge Outline 預設收合，可展開／收合。

- [x] 第一眼看到「30 秒快速理解」區塊（One Sentence + 核心重點），完整 Knowledge Outline 預設收合
- [x] 點擊「▶ 展開完整內容」，完整 Knowledge Outline 正確顯示，按鈕變成「▲ 收合」
- [x] 再次點擊可收合，按鈕變回「▶ 展開完整內容」
- [x] Network 面板確認展開／收合過程沒有任何新的 API 請求
- [x] One Sentence 與核心重點全程保持可見，只有完整 Knowledge Outline 可展開／收合
- [x] 多張卡片各自獨立測試，互不影響
- [x] 迴歸：Transcript、Study Note、Queue、History、Export 不受影響

**Test Date:** 2026-08-04
**Test Result:** PASS

**過程記錄：** 人工驗收一次通過。精簡重點是純前端從既有 Knowledge Outline 文字擷取一級清單項目（`extractTopPoints()`），非重新呼叫 Gemini；展開／收合為純 CSS class 切換，不觸發任何 API 請求。

### Design Freeze — Knowledge Structure Engine v1.0

Task 3 初版（Learning Blueprint MVP，單一線性文字樣板）Human Test 過程中，使用者判定產出內容本質上仍是 Knowledge Outline，未達成 Learning Blueprint 的產品目標，觸發重新設計。純文件定稿，未修改程式。

- [x] 產品定位、Taxonomy、Structure／Renderer 分離、Knowledge JSON Layer、Prompt Strategy、Human Test／KPI 定案（見 `Knowledge_Structure_Engine_v1.0.md`）
- [x] `Why.md` 同步更新（Vision、四層能力對照表、Product Principles 四句、Mission 穩定性聲明）

**Test Date:** 2026-08-05
**Test Result:** PASS（文件審閱確認，非程式驗收）

### Task 3 — Knowledge Structure Engine

依 Knowledge Structure Engine v1.0 重做：Gemini 呼叫改為兩步驟（Structure Detection → Knowledge Extraction），輸出結構化 Knowledge JSON（`structure_type` + 對應 `content` 欄位），取代初版單一線性文字樣板。本次僅完成 Engine（判斷＋抽取＋回傳 JSON＋最小可視化 JSON 顯示），依結構分派的 Renderer 留給 Task 4。

- [x] 對多支不同類型影片觸發「🗺️ 建立知識架構」，`structure_type` 判斷合理（實測涵蓋 flow／problem_solution／classification 等）
- [x] `content` 欄位符合對應 structure_type 的資料形狀，不是統一格式（例如 problem_solution 產生 `cases`，flow 產生 `steps`）
- [x] 未退化成一般條列摘要
- [x] 重新整理頁面，已產生項目直接顯示，不重複呼叫 Gemini
- [x] 迴歸：Transcript、Study Note、既有「🧠 開始快速學習」、Queue、History、Export 皆不受影響

**Test Date:** 2026-08-05
**Test Result:** PASS

**過程記錄：** Human Test 過程中經歷數輪排查：(1) 一支影片點擊按鈕後「沒有任何反應」，經 Network 確認 Request 停在 Pending，最終定位為 Assistant 先前為驗證 Structure Detection 一致性、短時間內連續呼叫約 15 次 Gemini API 做壓力測試，佔用了單一 Worker 的處理時間，並非程式邏輯錯誤；(2) 同一輪中回報過一次 500 Internal Server Error，後續重測未再重現，確認為同一批壓力測試期間的暫時性錯誤，非常態問題。

**已知限制（不阻擋本次驗收，經使用者確認延後處理）：**
- Structure Detection 一致性未達完全穩定：同一支內容特徵模糊的影片，重複生成可能得到不同 `structure_type`（已加入 `temperature=0` 改善，但未完全消除）。是否需要進一步處理（例如加強 Prompt 判斷規則），待後續獨立 Task 決定。
- Gemini 呼叫失敗時的 Error Response 處理未強化，依使用者指示不併入本次 Task，若 Human Test 發現不足，將另立獨立 Bug Fix Task。

僅修改 `app/gemini_client.py`（Learning Blueprint 系統指令與 `generate_learning_blueprint()` 改為兩步驟＋JSON 輸出＋`temperature=0`）、`app/learning_blueprint.py`（存檔格式改為 `.json`）、`app/main.py`（`learning-blueprint` 端點回傳結構化物件）、`app/static/script.js`（`buildLearningBlueprintSection()` 改為 JSON 最小顯示）。未修改 Workflow、Stage Guard、Single Worker、Transcript／Study Note 生成邏輯、`queue_store.py` 寫入結構、History、Export、Chrome Extension。

### Task 4 — Learning Blueprint Renderer

純前端 Renderer：`buildLearningBlueprintSection()` 改為依 Task 3 已產出的 `structure_type` 分派到對應排版（步驟卡片／因果箭頭／分類清單／決策樹／比較表格／時間軸／問題解法卡片／條列 fallback），取代原本的 `JSON.stringify` 顯示。不修改 API、Prompt、JSON Schema。

- [x] `structure_type` 對應正確排版顯示（不再是原始 JSON）
- [x] `generic`（fallback）正確顯示為條列清單
- [x] Session 內：建立 Learning Blueprint 後直接看到對應排版
- [x] F5 重新整理：已產生項目直接使用既有 Learning Blueprint 顯示對應排版，不重新呼叫 Gemini
- [x] 迴歸：Transcript、Study Note、既有「🧠 開始快速學習」、Queue、History、Export 皆不受影響

**Test Date:** 2026-08-05
**Test Result:** PASS

**驗收方式備註：** 本項目最初於實作完成當下標記為 Not Tested（見版本歷史），因當時尚未經使用者於瀏覽器實際操作確認。使用者於 Sprint 7 整合驗收（End-to-End Test，測試影片 `C6FkQuO4Fdw`，含 `generic` fallback 路徑）過程中親自於瀏覽器完成本項目的實際驗證後回報 PASS，本次依實際結果更新，非回溯補寫。

僅修改 `app/static/script.js`（`buildLearningBlueprintSection()` 改為依 `structure_type` 分派、新增 8 個 Renderer 函式）、`app/static/style.css`（新增對應排版樣式）。未修改 `app/gemini_client.py`、`app/learning_blueprint.py`、`app/main.py`、Knowledge JSON Schema、Workflow、Queue、History、Export、Chrome Extension。

Gemini 呼叫失敗的 Error Path（`GeminiGenerationError` → HTTP 500）與 Structure Detection 一致性，不屬於本次驗收範圍，已移至 `TODO.md` Product Backlog。

### Task 5 — Teach Back

根據已存在的 Learning Blueprint（不重讀 Transcript），依每一個 Blueprint 學習重點各自產生一組 Teach Back：Explain in Your Own Words（教學提示）、Self Check Checklist（動態產生，內容特定）、Practice Questions（Concept／Scenario／Application 三種）、Reflection（固定 4 題，導向 Next Action）。Preview 為真實 HTML（非 `<pre>`），下載輸出 Markdown。

- [x] 出現「📝 開始 Teach Back」按鈕（僅 Learning Blueprint 已存在時顯示）
- [x] 點擊後每個 Blueprint 各自顯示四區塊，為排版後的 HTML，非純文字
- [x] 「⬇ 下載 Teach Back」正常下載 `.md`
- [x] F5 重新整理直接顯示，不重新呼叫 Gemini
- [x] 迴歸：Transcript、Study Note、Learning Blueprint、Queue、History、Export 皆不受影響

**Test Date:** 2026-08-05
**Test Result:** PASS

僅新增 `app/teach_back.py`；修改 `app/gemini_client.py`（新增 Prompt／`generate_teach_back()`）、`app/main.py`（新增 `POST /api/queue/{video_id}/teach-back`、`GET .../teach-back/download`）、`app/static/script.js`、`app/static/style.css`。未修改 Knowledge Structure Engine 既有邏輯（`app/learning_blueprint.py`）、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

Gemini 呼叫失敗的 Error Path，不屬於本次驗收範圍，已在 `TODO.md` Product Backlog。

### Task 6 — Action List

根據已存在的 Learning Blueprint（不重讀 Transcript），彙總全部學習重點，產生一份 3～5 條「今天可執行」的行動清單（明確動詞開頭、範圍有限、不依賴額外資源），與 Study Note 既有的 Action Items 區隔。Preview 為真實 HTML checkbox 清單，下載輸出 Markdown。

- [x] 出現「✅ 開始 Action List」按鈕（與「📝 開始 Teach Back」平行顯示，Learning Blueprint 已存在時顯示）
- [x] 點擊後顯示 3～5 條行動，真實 checkbox 清單，非純文字
- [x] 「⬇ 下載 Action List」正常下載 `.md`
- [x] F5 重新整理直接顯示，不重新呼叫 Gemini
- [x] 迴歸：Transcript、Study Note、Learning Blueprint、Teach Back、Queue、History、Export 皆不受影響

**Test Date:** 2026-08-05
**Test Result:** PASS

僅新增 `app/action_list.py`；修改 `app/gemini_client.py`（新增 Prompt／`generate_action_list()`）、`app/main.py`（新增 `POST /api/queue/{video_id}/action-list`、`GET .../action-list/download`）、`app/static/script.js`。未修改 `app/static/style.css`（重用 Task 5 既有樣式）、`app/teach_back.py`（`extract_blueprint_items()` 依使用者決定 Feature First / Refactor Later，維持原位，由 `main.py` 直接呼叫，未搬移）、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

Gemini 呼叫失敗的 Error Path，不屬於本次驗收範圍，已在 `TODO.md` Product Backlog。

### Task 7 — Review（Active Recall）

根據已存在的 Learning Blueprint（不重讀 Transcript），產生 One Sentence Recall／Recall Questions／Workflow Recall／Blank Filling（Gemini 自行判斷是否適合，不強制）／Reflection＋Self Score。設計核心：先引導使用者自行回答，答案預設隱藏，需點擊「Show Reference Answer」才展開，不是直接顯示內容。

- [x] 出現「🔄 開始 Review」按鈕（與「📝 開始 Teach Back」「✅ 開始 Action List」平行顯示，Learning Blueprint 已存在時顯示）
- [x] 每題預設只顯示問題，答案隱藏；點擊「▶ Show Reference Answer」才展開參考答案
- [x] Blank Filling 區塊：內容不適合時整段不顯示，不強制出現
- [x] Reflection 區塊包含 Self Score（百分比選項）
- [x] 「⬇ 下載 Review」正常下載 `.md`
- [x] F5 重新整理直接顯示，不重新呼叫 Gemini
- [x] 迴歸：Transcript、Study Note、Learning Blueprint、Teach Back、Action List、Queue、History、Export 皆不受影響

**Test Date:** 2026-08-05
**Test Result:** PASS

僅新增 `app/review.py`；修改 `app/gemini_client.py`（新增 Prompt／`generate_review()`）、`app/main.py`（新增 `POST /api/queue/{video_id}/review`、`GET .../review/download`）、`app/static/script.js`、`app/static/style.css`（新增 Show/Hide Answer 與 Self Score 樣式）。未修改 `app/teach_back.py`（`extract_blueprint_items()` 依 Feature First / Refactor Later 原則，維持原位，由 `main.py` 直接呼叫）、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

Gemini 呼叫失敗的 Error Path，不屬於本次驗收範圍，已在 `TODO.md` Product Backlog。

### Sprint Result

- [x] Sprint 7 completed（Task 0～7 全部完成並驗收通過）

---

## Sprint 8 — Reliability & Product Polish

### Task 1 — Gemini 呼叫失敗 Error Path

Learning Blueprint／Teach Back／Action List／Review 四個模組呼叫 Gemini 失敗時，錯誤訊息改為顯示在觸發的那個按鈕旁邊（inline），取代原本只寫入頁面頂部、可能捲動出畫面外的 `#status`。按鈕本身即為重試入口（失敗後自動重新啟用），未新增獨立的重試按鈕。

- [x] 正常情境：4 個模組正常成功產生內容，畫面與原本一致
- [x] 失敗情境：對尚未建立 Learning Blueprint 的影片觸發 Teach Back／Action List／Review，錯誤文字正確出現在該按鈕旁邊，即使卡片在頁面下方也不用捲回頂部
- [x] 按鈕失敗後仍可點擊，非永久停用
- [x] 迴歸：加入暫存區／刪除／匯出等既有功能的頂部 `#status` 行為不受影響
- [x] Retry：可再次點擊、正常重新呼叫 API、Loading 狀態正常恢復、成功後錯誤訊息隨卡片重繪自動清除，不需重新整理頁面

**Test Date:** 2026-08-06
**Test Result:** PASS

**過程記錄：** Proposal 階段研究確認後端錯誤回應與前端「失敗後按鈕重新啟用」的重試機制本來就存在，真正落差是頂部 `#status` 在長列表下容易被忽略；本次僅針對此 root cause 修正。Assistant 以 `node --check` 驗證語法，並對真實影片（`video_id=V6KgW35co8E`）呼叫 `POST /api/queue/{video_id}/teach-back` 確認 400 錯誤格式不受影響、無磁碟副作用；本次環境無瀏覽器自動化工具，實際視覺／點擊確認由使用者於瀏覽器完成 Human Test（含 Retry 情境），回報 PASS。

僅修改 `app/static/script.js`（新增 `showInlineError()`／`clearInlineError()`，套用到既有 4 個 `startX()` 函式）、`app/static/style.css`（新增 `.queue-item-inline-error` 樣式）。未修改 `app/main.py`、`app/error_messages.py`、Workflow、Stage Guard、Single Worker、Queue Store、History、Export、Chrome Extension。

### Task 3 — Loading／Processing 狀態一致化

Rapid Learning／Learning Blueprint／Teach Back／Action List／Review 五個模組處理中改為統一顯示 disabled＋「⏳ 處理中…」，並修正 `renderQueue()` 輪詢重繪期間會把處理中按鈕換成全新可點擊節點的問題（改用既有 `*FetchInFlight` Set 判斷）。Human Test 過程中另外發現並修正一個獨立 Bug：不同影片的手動觸發彼此會互相阻塞，RCA 確認非既有 Single Worker Queue 設計、而是 5 個端點內直接同步呼叫 Gemini SDK 卡住事件迴圈，經使用者確認後併入本次以最小範圍修正（`asyncio.to_thread`）。

- [x] 正常情境：5 個模組正常成功產生內容，處理中顯示 Loading 文字，完成後畫面正常
- [x] 快速連點同一顆按鈕：只送出一次 API，不會重複呼叫
- [x] Loading 結束後完全復原：成功後按鈕連同 Loading 樣式一併被正式內容取代；失敗後按鈕恢復可點擊、無殘留 Loading 文字或永久 disabled
- [x] 不同影片平行處理：影片 A 仍在處理中時，點擊影片 B 的 Teach Back／Action List／Review 可立即開始，不需等待影片 A 完成（第一輪 Human Test FAIL，修正 `asyncio.to_thread` 後重測 PASS）
- [x] Retry：發生錯誤後可再次點擊、正常重新呼叫 API，行為與 Task 1 一致，未被本次改動破壞
- [x] 迴歸：Transcript、Study Note、Queue、History、Download 等既有功能不受影響

**Test Date:** 2026-08-06
**Test Result:** PASS

**過程記錄：** 第一輪 Human Test：正常情境／快速連點／既有功能迴歸 PASS，Retry 因本輪未發生錯誤而 Not Tested（維持 Task 1 已驗證的邏輯不變，同意暫不重測）；「不同影片平行處理」FAIL。使用者要求先確認是否為既有 Single Worker Queue（Sprint 4.1，僅序列化自動 Transcript／Study Note 流程）的預期設計再決定如何處理。Assistant 以程式碼（`_pipeline_queue`／`_pipeline_worker_loop` 的既有註解，明確記載 5 個 Learning Model 端點刻意不經過該 Queue）確認這是 Bug、不是架構問題：5 個端點雖宣告為 `async def`，內部卻直接呼叫同步 Gemini SDK，卡住 uvicorn 唯一的事件迴圈，使所有請求（含不同影片的獨立呼叫、Queue 輪詢）互相阻塞。使用者確認後指示併入 Task 3、限定最小修正範圍（不重構、不整理其他程式、不動 Queue 設計）；修正後重新 Human Test（平行處理、Loading 狀態、Regression）三項皆 PASS。

僅修改 `app/static/script.js`（新增共用 `buildTriggerButton()`，5 個模組共用既有 `*FetchInFlight` Set）、`app/main.py`（新增 `import asyncio`，5 個端點的 Gemini 呼叫改為 `await asyncio.to_thread(...)`）。未修改 `app/gemini_client.py`、`app/static/style.css`、Queue 設計、Stage Guard、Queue Store 寫入結構、History、Export、Chrome Extension。

### Task 2 — Queue Card 模組展開／收合

5 個模組（Rapid Learning／Learning Blueprint／Teach Back／Action List／Review）的標題列改為可點擊，獨立切換展開／收合；不是 Accordion（沒有互斥、沒有自動收合前一個），各模組互不影響，預設維持展開（與既有行為一致）。

- [x] 每個模組可獨立展開／收合，箭頭方向正確切換
- [x] 收合 A 模組不影響 B／C／D／E 的展開狀態
- [x] 收合狀態下 Teach Back／Action List／Review 仍可正常下載
- [x] Rapid Learning 既有「展開完整內容」子層 toggle 行為不變
- [x] 迴歸：Transcript、Study Note、Queue、History、Download 不受影響
- [x] 收合後再次展開：內容正常顯示、未重新呼叫 API、未重新生成內容、未出現空白內容

**Test Date:** 2026-08-06
**Test Result:** PASS

**過程記錄：** Proposal 最初依 UX Issue 規劃成 Accordion（一次只展開一個、自動收合前一個），過程中釐清使用者所指「Study Note」實際是 Rapid Learning（Queue Card 裡 Study Note 本身沒有行內展開區塊）；提出 Accordion Proposal 後，使用者主動簡化為單純獨立展開／收合，理由是維持 MVP、避免過度設計。Human Test 6 項全數 PASS。使用者另外提出一項未來 UX 建議（Queue Card 預設收合，只顯示 One Sentence＋學習入口按鈕），已記錄於 `TODO.md` Product Backlog，非本次範圍。

僅修改 `app/static/script.js`（5 個 `buildXSection()` 改為標題＋可收合主體，新增共用 `buildModuleToggleHeader()` 與 5 個獨立的收合狀態 Set）、`app/static/style.css`（新增 Accordion Header／箭頭樣式）。未修改任何後端、Task 1 inline 錯誤機制、Task 3 Loading／`buildTriggerButton()`、Queue／History／Export、Chrome Extension。

### Task 4 — `classify_error()` 分類精確度改善

Quota／Rate Limit／Auth 關鍵字命中時，依 stage 分流訊息：`studynote`（Gemini 呼叫）維持提及 Gemini 額度；`download`／`transcript`（yt-dlp／本機 Whisper，不呼叫 Gemini）改為不指名來源的通用訊息，不再誤標成 Gemini 問題。

- [x] 純函式驗證：`download`／`transcript` + 429／403 等關鍵字 → 通用訊息，不再出現「Gemini API 額度」字樣
- [x] 迴歸：`studynote` + quota 關鍵字 → 訊息不變（仍提及 Gemini）
- [x] 迴歸：`empty transcript`／安全過濾／私人影片／YouTube 限制／網路問題等其他分類文字與邏輯皆不變

**Test Date:** 2026-08-06
**Test Result:** PASS

#### 正式驗收案例：YouTube 字幕下載 429 → Retry 成功（真實案例，非模擬）

Human Test 過程中使用者實際遇到的真實錯誤，直接作為本次驗收證據：

```text
Unable to download video subtitles for 'zh-Hant'

HTTP Error 429: Too Many Requests
```

**Case:** YouTube Subtitle Download HTTP 429

**Observed:** yt-dlp subtitle download returned HTTP 429（上方原始錯誤文字）

**Expected UI（Product Backlog 目標，非本次 Task 4 實際產出——見下方說明）:** 「YouTube 暫時限制字幕下載，請稍後再試。」

**Retry:** PASS（不需重新整理頁面）

**Final Result:**
- Transcript：成功
- Study Note：成功
- Download：成功

- [x] 第一次執行：字幕下載遭 YouTube 429 Rate Limit
- [x] 點擊 Retry：不需重新整理頁面
- [x] Retry 後 Transcript 成功產生
- [x] Retry 後 Study Note 成功產生
- [x] 確認並非 Gemini API 額度問題，是 YouTube 字幕下載端的暫時性限流

**關於「Expected UI」的重要澄清：** 上方「YouTube 暫時限制字幕下載，請稍後再試。」是這個案例**最終應該達到的目標訊息**，但**不是本次 Task 4 實際會顯示的文字**。真實案例發生當下，字幕 429 被 `main.py` 既有邏輯靜默吞掉，UI 沒有顯示任何錯誤訊息（直接無聲 fallback 嘗試 Whisper）。要讓 UI 真的顯示這句話，需要同時修改 `app/main.py`（保留字幕錯誤文字，不再丟棄），已列入 Product Backlog、不屬於本次 Task 4 Scope（見下方過程記錄）。本次 Task 4 驗證的是 Retry Flow 本身正常、且確認問題根源並非 Gemini 額度。

**過程記錄：** 使用者在 Proposal 審閱階段提出這個真實案例，帶出一個比原訂 Scope 更深的既有落差：`main.py` 目前會靜默吞掉字幕下載失敗的錯誤文字，直接 fallback 到音訊下載＋本機 Whisper；若 fallback 也失敗（`TranscriptionError("empty transcript")`），使用者看到的是「找不到可用的逐字稿內容」，而非真正的 429 原因。修正這點需要同時改 `app/main.py`（保留字幕錯誤文字）與 `app/error_messages.py`（新增字幕＋429 的專屬分類），超出本次「僅改 `error_messages.py`」的 Scope，經使用者確認後列入 `TODO.md` Product Backlog，不併入 Task 4。本次 Task 4 完成的是 Root Cause 的另一半：`classify_error()` 本身在收到 429／Quota 等關鍵字時，不再無條件假設是 Gemini 問題。Retry Flow（不需重新整理頁面即可重試並成功）本身不受本次修改影響，維持既有行為，使用者確認符合預期。

僅修改 `app/error_messages.py`（新增 `_SERVICE_UNAVAILABLE_SOURCE` 常數＋一行 stage 分流判斷）。未修改 `app/main.py`、Workflow、Stage Guard、Single Worker、UI、其他模組。

### Sprint Result

- [x] Task 1 completed and accepted
- [x] Task 3 completed and accepted
- [x] Task 2 completed and accepted
- [x] Task 4 completed and accepted

---

## Sprint 8.5A — Product Intelligence Foundation

依 Engineering Kickoff Sprint 8.5（Product Intelligence Foundation）與 Factory Standard 規劃，純 Backend 可觀測性，不修改 UI／Prompt／既有 API 回傳格式。

### Task 1 — Correlation ID 基礎建設 + Runtime Intelligence

`queue_store.add_item()` 產生 `request_id`（uuid4）並鏡射進 `history_store`；新增 `app/observability/logger.py`／`runtime_metrics.py`／`daily_report.py`，記錄 Queue／Transcript／Study Note／Download 四階段起訖與成功/失敗至 `outputs/logs/runtime.jsonl`，即時增量更新 `outputs/reports/daily_report.json`。

- [x] 正常情境：完整跑一次 YouTube → Transcript → Study Note → Download，MVP 行為與之前完全一致
- [x] `outputs/queue.json` 該筆項目出現 `request_id` 欄位
- [x] `outputs/logs/runtime.jsonl` 出現該影片多筆紀錄（`queue`／`transcript`／`study_note`／`download`），`request_id` 全部一致
- [x] 不同影片各自產生不同的 `request_id`
- [x] `outputs/reports/daily_report.json` 的 `transcript_generated`／`study_notes_generated`／`runtime` 數字正確累加

**Test Date:** 2026-08-07　**Test Result:** PASS

**過程記錄：** 使用者於 Human Test 中觀察到 Download 動作目前會產生大量 Runtime 事件（同一支影片多次下載即多筆紀錄），確認這不是 Bug、暫時維持現行行為，留待 Sprint 8.5A 全部完成後再一併檢討 Download 應歸類為 Runtime Event 或 User Action，不在開發中途調整架構。

僅修改 `app/queue_store.py`（`add_item()` 產生 `request_id`）、`app/history_store.py`（`add_entry()` 鏡射 `request_id`）、`app/main.py`（4 處插入計時），新增 `app/observability/`。未修改 UI、Prompt、`app/gemini_client.py`。

### Task 2 — Cost Intelligence

`app/gemini_client.py` 新增共用攔截點 `_generate_content()`，涵蓋全部 7 個 `generate_*()` 函式，讀取 `response.usage_metadata` 換算估算成本，寫入 `outputs/logs/gemini_usage.jsonl`，`daily_report.json` 新增 `usage` 區塊。

- [x] 正常情境：MVP 行為與之前完全一致
- [x] `outputs/logs/gemini_usage.jsonl` 出現對應紀錄，`request_id` 與 `runtime.jsonl` 一致
- [x] `input_tokens`／`output_tokens`／`estimated_cost` 數值合理
- [x] `outputs/reports/daily_report.json` 新增 `usage` 區塊，`api_calls`／`estimated_cost` 正確累加
- [x] 追加：`estimated_cost` 出現處皆帶 `"currency": "USD"`
- [x] 追加：`daily_report.json` 新增 `study_package`（`count`／`total_cost`／`average_cost`），只計入 `quick_summary` + `study_note`

**Test Date:** 2026-08-07　**Test Result:** PASS

**過程記錄：** 使用者觀察到 Knowledge Outline 的快取估算成本已自動改用真實數值，確認這是 `average_cost_for_artifact_type()` 的通用邏輯（任何 artifact_type 只要當天有一筆真實用量即自動套用），非針對 Knowledge Outline 額外處理，Learning Blueprint／Teach Back／Action List／Review 也會在各自第一次真實呼叫後自動生效，不需要額外修改程式。

僅修改 `app/gemini_client.py`（新增 `_generate_content()`，7 個函式加 `request_id`／`video_id`）、`app/main.py`（9 處呼叫點）、`app/observability/daily_report.py`／`logger.py`，新增 `app/observability/cost_metrics.py`。

### Task 3 — Cache Intelligence

新增 `app/observability/cache_metrics.py`，於既有 7 處 `find_cached_*` 快取檢查點記錄 hit/miss 至 `outputs/logs/cache.jsonl`，`daily_report.json` 新增 `cache` 區塊。

- [x] 對已產生過 Study Note 的影片重複觸發：MVP 行為與之前完全一致
- [x] 第一次執行（無快取）：`result` 為 `miss`
- [x] 重複執行（有快取）：`result` 為 `hit`
- [x] `outputs/logs/cache.jsonl` 的 `request_id` 與同一支影片的 `runtime.jsonl`／`gemini_usage.jsonl` 一致
- [x] `outputs/reports/daily_report.json` 的 `cache.hit_rate`（0～1 之間）、`estimated_cost_saved` 正確

**Test Date:** 2026-08-07　**Test Result:** PASS

僅修改 `app/main.py`（7 處快取檢查點）、`app/observability/daily_report.py`／`logger.py`，新增 `app/observability/cache_metrics.py`。

### Task 4 — Error Intelligence

新增 `app/observability/error_metrics.py`；Gemini 相關失敗集中在 `_generate_content()` 記錄，非 Gemini 失敗（Download／Transcription／Worker／Study Note 未預期例外）於既有 4 個 `last_error` 記錄點補上，`daily_report.json` 新增 `errors` 區塊。

- [x] 正常情境：MVP 行為與之前完全一致
- [x] `outputs/reports/daily_report.json` 的 `errors.count`／`by_stage` 正確累加

**Test Date:** 2026-08-07　**Test Result:** PASS

**過程記錄：** 使用者確認不進行移除 `GEMINI_API_KEY` 等 Developer 層級的人工故障注入測試，Exception 路徑的完整覆蓋建議改由未來的自動化／單元測試負責，本次 Human Test 聚焦於「正常流程不受影響」與「Daily Report 統計正確」兩項。過程中使用者另外指出 `POST /api/queue` 的無效網址／找不到影片這兩個拒絕點發生在 `request_id` 產生之前，完全不會留下任何紀錄——確認為真實現象、非本次範圍，已記錄於 `TODO.md` Product Backlog（Product Analytics 範疇，非 Error Intelligence 必備）。

僅修改 `app/gemini_client.py`（`_generate_content()` 記錄失敗）、`app/main.py`（4 處既有 `last_error` 記錄點）、`app/observability/daily_report.py`／`logger.py`，新增 `app/observability/error_metrics.py`。

### End-to-End Validation

挑選真實處理過的影片（`video_id=5o4OsLjINuQ`），追蹤同一組 `request_id` 是否完整串起 4 份 log 與 `daily_report.json`。

- [x] `runtime.jsonl`：`queue`／`transcript`／`download`／`study_note`／`download`……各階段皆帶同一 `request_id`
- [x] `gemini_usage.jsonl`：`quick_summary`／`study_note`／`knowledge_outline` 三筆皆帶同一 `request_id`
- [x] `cache.jsonl`：`knowledge_outline` 由 `miss` 到之後多次 `hit`，皆帶同一 `request_id`
- [x] `daily_report.json` 的 `runtime`／`usage`／`cache`／`study_package` 數字與上述原始紀錄一致

**Test Date:** 2026-08-07　**Test Result:** PASS

### Sprint Result

- [x] Task 1 completed and accepted
- [x] Task 2 completed and accepted
- [x] Task 3 completed and accepted
- [x] Task 4 completed and accepted
- [x] End-to-End Validation completed and accepted

---

## Feature 001 — Transcript / Learning Blueprint Error Handling Completion（Spec Kit / SDD Lite，User Story 1 + User Story 2）

透過 Spec Kit（`.specify/`）建立的第一個功能，對應 `specs/001-error-handling-completion/`（spec.md／plan.md／research.md／quickstart.md／tasks.md）。涵蓋 User Story 1（P1，Transcript，2026-08-08 完成驗收）與 User Story 2（P2，Learning Blueprint，2026-08-09 完成驗收）。

### User Story 1 — Transcript 429 正確歸因（T001-T007、T014）

實作：`app/main.py` `_do_generate_transcript_for_item()`，保留字幕下載失敗（`SubtitleFetchError`）的原始錯誤文字；若 Whisper fallback 也失敗，僅在「字幕分類結果為限流／暫時性服務問題」且「Whisper 分類結果為既有的『找不到可用的逐字稿內容』通用訊息」兩者同時成立時，改用字幕的分類結果顯示給使用者，其餘情境維持既有行為不變。未修改 `app/error_messages.py`、`app/static/script.js`。

- [ ] T003（quickstart.md Scenario 1：字幕 429 + Whisper fallback 也失敗）— **NOT REPRODUCED**
- [x] T004（quickstart.md Scenario 2：字幕失敗、Whisper 成功，迴歸）— **PASS**
- [ ] T005（quickstart.md Scenario 3：字幕非 429 原因失敗 + Whisper 也失敗，迴歸）— **NOT REPRODUCED**
- [ ] T006（quickstart.md Scenario 4：失敗後 Retry 機制正常，迴歸）— **NOT REPRODUCED**
- [x] T007（quickstart.md Scenario 5：既有成功路徑迴歸抽測，有字幕影片）— **PASS**
- [x] T014（Final Phase，SC-005：Gemini/API 呼叫次數未增加）— **PASS**

**Test Date:** 2026-08-08　**Test Result:** User Story 1 部分驗證通過（PASS：T004／T007／T014；NOT REPRODUCED：T003／T005／T006，皆非 PASS 亦非 FAIL）

**T004 — PASS：** 測試影片 `https://www.youtube.com/shorts/FbIp25kvq7o`（無字幕）。Whisper fallback 成功，Transcript／Study Note 皆成功，Queue 正常走完，無任何錯誤訊息，行為與修改前一致。

**T007 — PASS：** 測試影片 `https://www.youtube.com/watch?v=HjMO5oBvcRA`（有字幕）。Queue 處理成功、Transcript／Study Note 皆成功、下載 200 OK。因 UI 中間狀態轉換過快，人工無法單靠觀察確認是否為字幕優先路徑，改以 `outputs/logs/runtime.jsonl` 查證：該影片 `transcript` 階段僅耗時 7.129 秒（`request_id=e81457b6-9f6b-42ff-ae3e-63f4fab875f0`），遠低於音訊下載＋本機 Whisper 轉錄所需時間量級，確認實際走的是字幕優先路徑（`main.py` 既有的 317-336 行，本次修改完全未觸碰的程式碼），而非 Whisper fallback。

**T014 / SC-005 — PASS：** 比對 `outputs/logs/gemini_usage.jsonl` 修改前（2026-08-07，`qrFE4Zne-1I`／`AUrx6yMn1c0` 等）與修改後（2026-08-08，`FbIp25kvq7o`／`HjMO5oBvcRA` 及本輪其餘 10 支測試影片）的真實紀錄，成功路徑的 Gemini 呼叫模式完全一致：每支影片固定 `quick_summary` + `study_note` 共 2 次呼叫，無任何一筆記錄出現額外或重複呼叫。

**T003／T005／T006 — NOT REPRODUCED（環境相依，未強制觸發，未修改程式碼或加入測試專用 hook）：**
- **T003**（字幕 429 + Whisper 也失敗）：連續送出 5 支不同影片（`43knP15HEok`／`n8OTYXkHwWk`／`dUDi-F6eAvk`／`VUj6zDFs-2Q`／`-451m1UVYCo`）嘗試誘發 YouTube 字幕端限流，5/5 皆成功完成，未觀察到任何 429。此情境依賴 YouTube 端是否恰好觸發限流，屬環境相依。
- **T005**（字幕非 429 原因失敗 + Whisper 也失敗）：兩度嘗試以純音樂／無人聲 Shorts 誘發 Whisper 產生空逐字稿（`MFZZrkSZrcw`、`VQC3Uq9MF-Q`），兩次 Whisper 皆未失敗，而是產生了看似合理但與影片實際內容無關的 hallucinated 文字，Transcript／Study Note 皆判定為成功，無法重現「Whisper 也失敗」這個前提條件。
- **T006**（失敗後 Retry 正常運作）：嘗試將自有頻道影片設為 Private 以製造失敗狀態，但失敗發生於 Queue item 建立之前（`POST /api/queue` 回傳 400「無法取得影片資訊」），不會產生可供測試 Retry 的 Queue Card，因此無法重現「Queue item 已存在 → 處理失敗 → 可按 Retry」的測試前提。

三項 NOT REPRODUCED 皆非程式邏輯缺陷造成，是測試前提條件本身依賴難以主動控制的外部環境（YouTube 限流時機、Whisper 對無語音內容的實際行為、失敗發生的時間點），依使用者指示不視為 PASS 亦不視為 FAIL。

**Human Test 過程中另外發現一個獨立問題（不屬於本次 Feature 001 範圍，未修改程式碼處理）：** Whisper 對純音樂／無實際語音內容的影片，可能產生看似合理但與影片內容無關的 hallucinated 逐字稿，而非回傳空結果或失敗；系統目前會將這類 hallucinated 內容視為有效 Transcript 並繼續產生 Study Note。重現案例：`https://www.youtube.com/shorts/MFZZrkSZrcw`、`https://www.youtube.com/shorts/VQC3Uq9MF-Q`。列為 Future Backlog Candidate，詳見 `specs/001-error-handling-completion/research.md`。

僅修改 `app/main.py`（`_do_generate_transcript_for_item()` 內兩處：保留字幕失敗文字、`TranscriptionError` 例外處理新增優先順序判斷）。未修改 `app/error_messages.py`、`app/static/script.js`、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

### User Story 2 — Learning Blueprint 正確歸因（T008-T013）

實作：`app/error_messages.py` 新增 `_SERVICE_UNAVAILABLE_LEARNING_BLUEPRINT` 常數，`classify_error()` 的 quota/429 判斷分支由二選一（`studynote` / 其他）改為三選一，新增 `learning_blueprint` → 新常數；Gemini-aware 路由條件由 `stage == "studynote"` 擴大為 `stage in ("studynote", "learning_blueprint")`，使 Learning Blueprint 的非 quota 失敗（安全過濾／未知錯誤）也能正確路由，不再落入 YouTube 導向的分類。`app/main.py`：`generate_learning_blueprint()` 的 `GeminiGenerationError` 例外處理改用 `stage="learning_blueprint"`（原為 `stage="studynote"`）。`GeminiConfigError` 處理、Teach Back／Action List／Review 三個模組皆未修改。

- [x] T008（`app/error_messages.py` 新增常數＋分流邏輯）— 已實作
- [x] T009（`app/main.py` 改用新 stage）— 已實作
- [x] T010（quickstart.md Scenario 6：Learning Blueprint Gemini 失敗歸因）— **PASS**
- [x] T011（quickstart.md Scenario 7：失敗後 Retry，條件解除即成功）— **PASS**
- [x] T012（quickstart.md Scenario 8：Teach Back／Action List／Review 迴歸，不受影響）— **PASS**
- [x] T013（quickstart.md Scenario 9：`GeminiConfigError`／金鑰缺失路徑不受影響）— **PASS**

**Test Date:** 2026-08-09　**Test Result:** User Story 2 全部驗證通過（PASS：T010／T011／T012／T013）

**T010 — PASS：** 測試影片 `A50IsjwUAjs`（This Changes English Learning，Transcript 已完成、無 Learning Blueprint 快取）。於獨立測試環境（`127.0.0.1:8001`，暫時性、僅限單一 process 的無效 `GEMINI_API_KEY`，未寫入 `.env`）點擊「建立知識架構」，畫面顯示「Learning Blueprint 服務目前無法使用或過於忙碌，請稍後再試（可能是 Gemini API 額度已用完）。」，明確包含「Learning Blueprint」字樣、無 Study Note 用語。交叉比對 `outputs/logs/errors.jsonl` 新增一筆 `artifact_type: learning_blueprint`、`API_KEY_INVALID` 錯誤特徵（`logged_at: 2026-08-09T03:07:31Z`），`gemini_usage.jsonl` 與 `outputs/learning_blueprints/` 皆無該影片紀錄（純失敗、無快取污染），確認訊息確實來自本次修改的分類邏輯。

**T011 — PASS：** 延續 T010 失敗狀態，將 8001 測試 process 換成正常讀取 `.env` 真實金鑰（未修改 `.env` 本身）後，於同一張 Queue Card 再次點擊同一顆「建立知識架構」按鈕，紅色錯誤訊息消失、Learning Blueprint 正常顯示。交叉比對 `outputs/logs/gemini_usage.jsonl` 新增一筆 `A50IsjwUAjs` 的 `learning_blueprint` 真實成功紀錄（真實 token 用量與費用，`logged_at: 2026-08-09T03:16:22Z`，非快取命中），確認為真正重新呼叫 Gemini 成功，而非讀取舊快取；`errors.jsonl` 於此之後無新增失敗紀錄。

**T012 — PASS：** 於已有 Learning Blueprint 快取的 `A50IsjwUAjs` 上，沿用 T010 的無效金鑰測試環境，依序對 Teach Back／Action List／Review 三個模組觸發同類型失敗。三者畫面皆維持原本 Study Note 用語的錯誤訊息，未出現「Learning Blueprint」字樣，Retry 提示皆正常。交叉比對 `errors.jsonl` 新增三筆獨立紀錄（`artifact_type` 分別為 `teach_back`／`action_list`／`review`，皆為 `API_KEY_INVALID` 特徵，`logged_at` 03:28:14／03:28:42／03:28:45），確認三個模組各自獨立呼叫、各自失敗，且程式碼（`app/main.py` 對應三處例外處理）確認皆仍為 `stage="studynote"`，本次未修改。

**T013 — PASS：** 測試影片 `LJqnEPXWr4A`（Transcript 已完成、無 Learning Blueprint 快取）。將 8001 測試 process 改為金鑰缺失狀態（於 Python 行程內直接以 `os.environ['GEMINI_API_KEY']=''` 設定，避免 Windows 環境變數「空字串等同刪除」的限制導致 `load_dotenv()` 誤載入真實金鑰；未修改 `.env`）後點擊「建立知識架構」，畫面顯示原始例外文字「缺少 GEMINI_API_KEY 環境變數，請先設定後再試」，與 `app/gemini_client.py` 的 `GeminiConfigError` 訊息逐字相符，未經過 `classify_error()` 分類。交叉比對 8001 test server 自身 request log（該請求回應 `500 Internal Server Error`）確認請求確實送達；`errors.jsonl` 無新增紀錄（`GeminiConfigError` 發生於 Gemini 呼叫之前，本就不經過該記錄點，這也是驗證項之一）；`gemini_usage.jsonl` 與快取目錄皆無該影片紀錄，確認未實際呼叫 Gemini。`app/main.py` 1001-1002 行的 `GeminiConfigError` 處理本次未修改。

**Human Test 過程中的測試方法記錄（皆未修改 production code、`.env`，或新增測試專用 hook）：**
- 測試方式：以獨立測試伺服器（`127.0.0.1:8001`，與正式 `127.0.0.1:8000` 完全分離的 process）搭配暫時性、僅限單一 process 的 `GEMINI_API_KEY` 覆寫，模擬 Gemini 呼叫失敗／金鑰缺失，測試後即終止該 process，不影響正式伺服器與 `.env`。
- 過程中發現並修正兩個測試方法本身的誤區（非程式邏輯缺陷）：(1) `generate_learning_blueprint()` 呼叫 Gemini 前會先檢查磁碟快取（`app/main.py` 981-986 行，既有邏輯），若選到已有快取的影片，不論金鑰是否有效都不會真正呼叫 Gemini，需改選尚無快取的影片才能真正測到失敗路徑；(2) Windows 環境變數無法儲存「存在但空字串」的狀態（`$env:VAR=""` 等同刪除該變數），導致 `load_dotenv()`（`override=False`）誤判變數不存在而從 `.env` 補上真實金鑰，改用 Python 行程內直接設定 `os.environ` 的方式（不經過 Windows 建立子行程時的環境區塊）才能穩定重現金鑰缺失狀態。

僅修改 `app/error_messages.py`（T008：新增 1 個常數、擴大 2 處判斷）、`app/main.py`（T009：`generate_learning_blueprint()` 例外處理 1 行，`stage="studynote"` → `stage="learning_blueprint"`）。未修改 `app/static/script.js`、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension、Teach Back／Action List／Review 模組本身。

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