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