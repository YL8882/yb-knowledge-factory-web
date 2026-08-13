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

## Sprint 7 — Rapid Learning Engine

Learn Package Specification v2.0（見 `Learn_Package_Specification_v2.0.md`）第一階段實作：One Sentence + Knowledge Outline，以及讓使用者 30 秒內建立知識輪廓的呈現方式。

### Task 0 — Learning Blueprint Engine：Learn Package Specification v2.0 ✅ Completed

- [x] 定義 Learn Package 6 個模組（One Sentence／Knowledge Outline／Learning Blueprint／Study Note／Teach Back／Action List）的結構、驗收標準、閱讀動線
- [x] 純規格文件，未涉及程式、UI、Prompt

文件：`Learn_Package_Specification_v2.0.md`

### Task 1 — One Sentence + Knowledge Outline ✅ Completed

- [x] Queue Card 新增「🧠 開始快速學習」按鈕，Study Note 完成後才顯示（Queue 維持收件匣定位，Rapid Learning 是使用者主動開始學習的動作，不隨 Queue 自動產生）
- [x] 點擊後呼叫 Gemini 產生 One Sentence（影片核心目的，非摘要）＋ Knowledge Outline（知識輪廓），存成新檔案 `outputs/knowledge_outlines/KO_<title>_<video_id>.md`
- [x] 已產生過的項目重新整理頁面直接顯示，不重複呼叫 Gemini

新增 `app/knowledge_outline.py`（比照 `study_note.py`）、`app/gemini_client.py` 新增 Prompt 與 `generate_knowledge_outline()`、`app/main.py` 新增獨立的 `POST /api/queue/{video_id}/knowledge-outline`（未掛進 Single Worker／Stage Guard，只新增 `knowledge_outline_path` 附加欄位）。未修改 Transcript／Study Note 產生邏輯、Workflow、Stage Guard、Single Worker、`queue_store.py` 寫入結構、History、Export、Chrome Extension。

**過程記錄：** 初版 UI 把顯示區塊放在頁面上方共用的 `processing-panel`（跟 Study Note 預覽同一位置），Human Test 發現「畫面沒有變化」——RCA 確認不是程式錯誤，是 UI 版位問題：該面板只對應 `trackedVideoId`（最近一次追蹤的單一影片），不是每張 Queue Card 各自一份。改為在 `renderQueue()` 內、每張 Queue Card 直接渲染 Rapid Learning 區塊（新增 `knowledgeOutlineCache` 讓內容跨重新渲染存活），重新驗收通過。

### Task 2 — Quick Learn Layer（30 秒學習層）✅ Completed

- [x] Queue Card 上的 Rapid Learning 區塊重新設計：預設只顯示 One Sentence ＋ 精簡重點（①～⑤，從既有 Knowledge Outline 文字擷取，非重新產生），第一眼不超過一個螢幕
- [x] 完整 Knowledge Outline 預設收合，「▶ 展開完整內容」／「▲ 收合」純前端切換，不呼叫 Gemini、不重新整理資料
- [x] 展開狀態（`expandedKnowledgeOutlineCards`）跨重新渲染保留

僅修改 `app/static/script.js`（新增 `extractTopPoints()`，重寫 `buildRapidLearningSection()`）、`app/static/style.css`。未修改 Prompt、Gemini、`knowledge_outline.py`、`study_note.py`、Queue Store、History、Export、Chrome Extension。

### Design Freeze — Learning Model v1.0 ✅ Completed

Task 3（Learning Blueprint Engine）開發前的產品設計定稿，純討論，未修改任何程式、Prompt、UI、Repository。

- [x] 三個 Learning Phase 正式命名定案：雙層命名——使用者面「值得學／看懂了／記住了」，內部學術對應「Orientation／Comprehension／Retention」（取代原本容易被誤解為難度分級的 Level 1/2/3）
- [x] 確認 Knowledge Outline 正式退役，由 Learning Blueprint 取代；原通用清單邏輯保留為無法明確分類內容時的預設／後備結構
- [x] Learning Blueprint 正式定義：目的是幫助使用者建立心智模型，非整理知識；定義 7 種候選結構（流程／因果／分類／決策／比較／時間軸／問題→解法），每支影片判斷單一主要結構
- [x] 確認資料流程方向：各 Phase 各自生成、按需觸發、以上下文串接維持一致性（非單一資料多種呈現一次生成）
- [x] 定義三個 Phase 各自的目的／輸入／輸出／完成條件／Human Test
- [x] 提出產品 KPI（Teach Back 完成率為核心指標）與終局差異化定位

Sprint 7 Task 3 起依此 Learning Model v1.0 展開實作。

### Task 3（初版）— Learning Blueprint MVP：已由 Knowledge Structure Engine v1.0 取代

初版採單一線性文字樣板（`[錨點]→細節`），Human Test 過程中確認技術可正常運作，但內容本質上與 Knowledge Outline 難以區分，不符合 Learning Blueprint 的產品目標。未正式驗收，由下方 Design Freeze 重新定義範圍後取代；已產生的測試資料（`outputs/learning_blueprints/`）屬於除錯殘留，將於 Task 3 重做時一併清理。

**過程記錄：** Human Test 過程中經歷多輪「按鈕未顯示」的 RCA，最終定位兩個獨立原因：(1) 部分測試分頁的瀏覽器分頁未真正重新載入新版 `script.js`（確認方式：`document.querySelectorAll('.queue-item-rapid-learning').length` 應為 97，實際部分分頁僅 44，重新整理該分頁後恢復正常）；(2) Assistant 曾誤用 `typeof functionName` 在 Console 全域 scope 檢查函式是否載入，但 `script.js` 全部程式碼皆包在 `document.addEventListener('DOMContentLoaded', function() {...})` 的 closure 內，任何函式（含新舊版本）在全域 scope 查詢都會是 `undefined`，此診斷方式本身有誤，不能用來判斷版本是否載入，已於對話中修正並改用 DOM 實際渲染結果驗證。

### Design Freeze — Knowledge Structure Engine v1.0 ✅ Completed

Task 3 初版 Human Test 過程中，使用者判定產出內容本質上仍是 Knowledge Outline，未達成 Learning Blueprint 的產品目標，觸發重新設計。純討論與文件定稿，未修改程式、Prompt、UI。

- [x] 產品定位定案：YB Learn＝Knowledge Structure Engine，非摘要／Study Note／Mind Map 工具；Study Note／Knowledge Structure Engine／Learning Blueprint／Teach Back 四層能力各自回答不同問題
- [x] 7 種 Core Structure 重新定義為「可擴充清單」而非固定七選一，並為每種定義資料形狀（非僅結構名稱）
- [x] Structure 與 Renderer 正式分離：Structure＝知識語意形狀，Renderer＝畫面呈現，兩者透過 Knowledge JSON 解耦
- [x] 新增 Knowledge JSON Layer：Video → Knowledge Extraction → Knowledge Structure → Knowledge JSON → Renderer → Learning Blueprint
- [x] Prompt Strategy 改為兩步驟：Structure Detection → Knowledge Extraction，輸出結構化 JSON，取代原本單一線性文字樣板
- [x] Learning Blueprint 定位修正：Learning Blueprint 不是 Engine，是 Engine 的第一個 Output；Teach Back／Quiz／Action List／Review／Skill Tree 未來共用同一個 Engine
- [x] Human Test／KPI 重新定義：30 秒內能否說出架構、理解關係、複述 70% 內容
- [x] 同步更新 `Why.md`：新增 Vision（Learn Faster / Understand Deeper / Remember Longer）、擴充「我們真正是什麼」為四層能力對照表、Product Principles 正式定名為四句（Structure Knowledge／Make It Stick／Reduce Friction／Start Learning）、新增「Mission 的穩定性」與產品決策原則
- [x] 新增 `Knowledge_Structure_Engine_v1.0.md` 作為正式架構規格文件（status: Design Freeze — Approved）

文件：`Knowledge_Structure_Engine_v1.0.md`、`Why.md`

**Product Position／Mission／Vision／Learning Model／Product Principles 自本次起凍結，除非規劃 v2.0，不再修改。**

Sprint 7 後續開發順序重新確認：Task 3 Knowledge Structure Engine → Task 4 Learning Blueprint Renderer → Task 5 Teach Back → Task 6 Action List → Task 7 Review。

### Task 3 — Knowledge Structure Engine ✅ Completed

- [x] Gemini 呼叫改為兩步驟（Structure Detection → Knowledge Extraction），輸出結構化 Knowledge JSON（`structure_type` + 對應 `content` 欄位），取代初版單一線性文字樣板
- [x] 存檔格式改為 `.json`（`outputs/learning_blueprints/LB_<title>_<video_id>.json`）
- [x] `temperature=0`：改善（非完全消除）Structure Detection 一致性
- [x] Queue Card 最小可視化：pretty-printed JSON，證明不同 `structure_type` 產生不同 `content` 形狀；依結構分派的正式 Renderer 留給 Task 4

僅修改 `app/gemini_client.py`、`app/learning_blueprint.py`、`app/main.py`、`app/static/script.js`。未修改 Workflow、Stage Guard、Single Worker、Transcript／Study Note 生成邏輯、`queue_store.py` 寫入結構、History、Export、Chrome Extension。

**過程記錄：** 詳見 `Acceptance_Test.md` Sprint 7 Task 3。Human Test 期間排查出的「Pending／500」現象最終定位為 Assistant 自行做一致性驗證時短時間內連續呼叫約 15 次 Gemini API 造成，非程式錯誤。

**已知限制（延後處理，經使用者確認不阻擋本次驗收）：** Structure Detection 一致性未達完全穩定；Gemini 呼叫失敗的 Error Response 處理未強化——兩者皆待後續獨立 Task 決定是否處理，不併入 Task 3。

### Task 4 — Learning Blueprint Renderer ✅ Completed

- [x] `buildLearningBlueprintSection()` 改為依 `structure_type` 分派到對應排版（8 個新增 Render 函式），取代 Task 3 的 `JSON.stringify` 顯示
- [x] `generic` fallback 顯示為條列清單
- [x] F5 重新整理沿用 Task 3 已建立的快取機制，Task 4 未變更 fetch／cache 邏輯

僅修改 `app/static/script.js`、`app/static/style.css`。未修改 `app/gemini_client.py`、`app/learning_blueprint.py`、`app/main.py`、Knowledge JSON Schema、Workflow、Queue、History、Export、Chrome Extension。

**過程記錄：** 實作完成當下先以 Node 模擬 DOM 環境自行驗證（合成資料＋磁碟上真實 Gemini 樣本比對欄位名稱，確認無例外），但當時未取得使用者實際 Human Test，`Acceptance_Test.md` 如實記錄為 Not Tested。使用者於 Sprint 7 整合驗收（End-to-End Test，測試影片 `C6FkQuO4Fdw`，含 `generic` fallback 路徑）過程中親自於瀏覽器完成本項目驗證後回報 PASS，`Acceptance_Test.md` 已依實際結果更新。

Gemini 呼叫失敗的 Error Path、Structure Detection 一致性：不屬於 Task 4 範圍，已移至上方 Product Backlog。

### Task 5 — Teach Back ✅ Completed

- [x] 依已存在的 Learning Blueprint（不重讀 Transcript）逐一產生 Teach Back：`extract_blueprint_items()` 依 7 種 structure_type 各自的資料形狀，統一轉成 `{title, detail}` 學習重點清單餵給 Gemini
- [x] 每個學習重點各自產生 Explain in Your Own Words（教學提示）、Self Check Checklist（動態、內容特定）、Practice Questions（Concept／Scenario／Application）——皆由 Gemini 依內容客製生成，非固定模板
- [x] Reflection 為固定 4 題模板（非 Gemini 生成，見 `teach_back.py` `_REFLECTION_QUESTIONS`），導向 Next Action
- [x] Preview 為真實 HTML（`<h4>`／checkbox `<input>`／`<dl>`），非 `<pre>` 純文字
- [x] 下載輸出 Markdown（`.md`，與 `.json` 一併持久化，`.md` 直接透過 `FileResponse` 下載，比照 Transcript／Study Note 既有模式）
- [x] F5 直接讀取既有 Teach Back，不重新呼叫 Gemini（沿用 Task 3 建立的 cache-first 模式）

新增 `app/teach_back.py`；修改 `app/gemini_client.py`、`app/main.py`（`POST /api/queue/{video_id}/teach-back`、`GET .../teach-back/download`）、`app/static/script.js`、`app/static/style.css`。未修改 `app/learning_blueprint.py`、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

**過程記錄：** Assistant 以真實 API 呼叫端到端驗證（非模擬）：確認依 Learning Blueprint 的學習重點數量產生對應數量的 Teach Back（例：4 個 `cases` → 4 組 Teach Back）、每組內容具體對應該學習重點而非通用模板、`.md` 下載檔案結構與編碼正確、Learning Blueprint 不存在時正確回傳 400。使用者於瀏覽器完成 Human Test 後回報 PASS，詳見 `Acceptance_Test.md` Sprint 7 Task 5。

### Task 6 — Action List ✅ Completed

- [x] 根據已存在的 Learning Blueprint（不重讀 Transcript），彙總全部學習重點，產生 3～5 條「今天可執行」的行動（明確動詞開頭、範圍有限、不依賴額外資源）——與 Teach Back 不同，是單一彙總清單，不是逐一拆解每個學習重點
- [x] 與 Study Note 既有「Action Items」區隔：Action Items＝所有建議行動，Action List＝篩選後、今天就能做的
- [x] Preview 為真實 HTML checkbox 清單，非 `<pre>` 純文字
- [x] 下載輸出 Markdown（`.md`，比照 Teach Back 的持久化模式）
- [x] F5 直接讀取既有 Action List，不重新呼叫 Gemini

**Feature First, Refactor Later（使用者決定，2026-08-05）：** `extract_blueprint_items()` 維持在 `app/teach_back.py`，未搬移至 `app/learning_blueprint.py`；`app/main.py` 的 `generate_action_list()` 端點直接呼叫 `teach_back.extract_blueprint_items()`。若後續有第三個以上模組共用，再另外安排 Refactor Sprint 統一整理。

新增 `app/action_list.py`；修改 `app/gemini_client.py`、`app/main.py`（`POST /api/queue/{video_id}/action-list`、`GET .../action-list/download`）、`app/static/script.js`。未修改 `app/static/style.css`（重用 Task 5 既有樣式）、`app/teach_back.py`、`app/learning_blueprint.py`、Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

**過程記錄：** Assistant 以真實 API 呼叫端到端驗證：`POST /api/queue/K6npgLhA7r8/action-list` 產生 4 條內容具體、明確動詞開頭的行動；下載檔案與 Content-Disposition 正確；Learning Blueprint 不存在時正確回傳 400。驗證過程中發現 port 8000 上有非 Assistant 啟動的既有 server process（研判為使用者自行開啟），確認其為 Task 5 之前的舊程式碼（`/action-list` 回 404）後已重啟為新版，未影響任何磁碟資料。使用者於瀏覽器完成 Human Test 後回報 PASS，詳見 `Acceptance_Test.md` Sprint 7 Task 6。

### Task 7 — Review（Active Recall）✅ Completed

- [x] 根據已存在的 Learning Blueprint，產生 One Sentence Recall／Recall Questions（每個學習重點各一題，比照 Teach Back 的 per-item 模式）／Workflow Recall／Blank Filling（Gemini 自行判斷是否適合，不強制生成）
- [x] Reflection 為固定 4 題模板（非 Gemini 生成，見 `review.py` `_REFLECTION_QUESTIONS`，聚焦「回想表現」，與 Teach Back 的 Reflection 刻意不同）＋ Self Score（固定百分比選項，純 UI 自我評估，不儲存）
- [x] Preview 預設隱藏每題參考答案，需點擊「▶ Show Reference Answer」才展開（先回想、後比對，不直接顯示答案）
- [x] 下載輸出 Markdown（`.md`，答案不隱藏，完整記錄供日後查閱）
- [x] F5 直接讀取既有 Review，不重新呼叫 Gemini

新增 `app/review.py`；修改 `app/gemini_client.py`、`app/main.py`（`POST /api/queue/{video_id}/review`、`GET .../review/download`）、`app/static/script.js`、`app/static/style.css`。依 Feature First, Refactor Later 原則，`extract_blueprint_items()` 維持在 `app/teach_back.py`，未搬移，`main.py` 直接呼叫。未修改 Workflow、Stage Guard、Single Worker、Queue Store 寫入結構、History、Export、Chrome Extension。

**過程記錄：** Assistant 以真實 API 呼叫端到端驗證：對內容清楚的影片（`M7Tjx0aXrQ8`）產生高品質、內容具體的 Review（4 題 Recall Questions、5 題 Blank Filling，皆客製化非模板）；對內容本身單薄的既有測試影片，Review 正確反映其 Learning Blueprint 內容有限的既有狀況（非新增問題）。驗證過程中一度誤判內容為亂碼，經改用檔案直接核對（避開 bash/curl 終端機顯示的既有編碼顯示問題）後確認資料完全正確，純屬顯示層級的誤判，非真實資料損毀。使用者於瀏覽器完成 Human Test 後回報 PASS，詳見 `Acceptance_Test.md` Sprint 7 Task 7。

**Sprint 7（Rapid Learning Engine → Knowledge Structure Engine）全部完成：Task 0～7。**

---

## Sprint 8 — Reliability & Product Polish

Sprint 7 完成後的穩定化與打磨；不新增 Learning Model 功能模組，聚焦 Error Handling、Loading／Processing 體驗、Queue Card UI 整理與既有 Product Backlog 缺口修正。

Priority／Development Order（Sprint 8 Proposal 確認）：P0（Task 1 Error Path、Task 3 Loading/Processing）→ P1（Task 2 Queue Card UI、Task 4 classify_error）→ P2（Task 5 Structure Detection 一致性）。開發順序：Task 1 → Task 3 → Task 2 → Task 4 → Task 5。

**Task 5 決定延後至 Product Backlog（未執行）：** 使用者審閱 Proposal 後認為目前沒有可穩定重現的 `structure_type` 判斷不一致案例，無法建立 Before／After 比較、無法定義明確 PASS／FAIL，Human Test 沒有客觀驗收方式；依「可驗收的 Bug 優先」原則，改為等之後再次遇到真實不一致案例時，依該案例修正與驗收，詳見下方 Product Backlog。

### Task 1 — Gemini 呼叫失敗 Error Path ✅ Completed

- [x] Learning Blueprint／Teach Back／Action List／Review 四個模組呼叫 Gemini 失敗時，錯誤訊息顯示在觸發的那張 Queue Card／按鈕旁邊（inline），不再只寫入頁面頂部、可能捲動出畫面外的 `#status`
- [x] 按鈕本身即為重試入口（失敗後自動重新啟用），未新增獨立的重試按鈕
- [x] Retry：可再次點擊、正常重新呼叫 API、Loading 狀態正常恢復、成功後錯誤訊息隨卡片重繪自動清除，不需重新整理頁面

新增共用 helper `showInlineError()`／`clearInlineError()`，套用到既有 4 個 `startX()` 函式。僅修改 `app/static/script.js`、`app/static/style.css`。未修改 `app/main.py`、`app/error_messages.py`、其他既有呼叫點（加入暫存區／刪除／匯出）。

**過程記錄：** Proposal 階段研究發現，4 個模組後端已回傳分類過的錯誤訊息、前端失敗後按鈕也早已重新啟用（重試機制其實已存在），真正的落差（root cause）是 `showStatus()` 只寫入頁面唯一、非 sticky 的頂部 `#status`，Queue／History 列表較長時容易被使用者忽略。本次只修正這個 root cause，未重做已經正確的部分。Assistant 以 `node --check` 驗證語法，並對真實影片（`video_id=V6KgW35co8E`）呼叫 `POST /api/queue/{video_id}/teach-back` 確認 400 錯誤格式不受影響、無磁碟副作用；受限於本次環境沒有瀏覽器自動化工具，實際視覺／點擊確認（含使用者新增的 Retry 情境）由使用者於瀏覽器完成 Human Test，回報 PASS。

### Task 3 — Loading／Processing 狀態一致化 ✅ Completed

- [x] Rapid Learning／Learning Blueprint／Teach Back／Action List／Review 五個模組處理中皆顯示統一的 Loading 樣式（disabled＋「⏳ 處理中…」），取代原本只有半透明 disabled、按鈕文字不變的狀態
- [x] 修正正確性落差：`renderQueue()` 每 1.5 秒輪詢重繪一次，先前手動點擊只把 `disabled` 設在被點擊的那個 DOM 節點上，若輪詢在請求進行中觸發重繪，該節點會被換成全新、未 disabled 的按鈕，使用者可能誤以為已恢復而再次點擊，造成同一影片同一模組被併發呼叫兩次 Gemini；改為讓每個模組共用既有的 `*FetchInFlight` Set（`knowledgeOutlineFetchInFlight`／`learningBlueprintFetchInFlight`／`teachBackFetchInFlight`／`actionListFetchInFlight`／`reviewFetchInFlight`），`renderQueue()` 重繪時依 Set 判斷是否仍在處理中，每次重繪都正確渲染 Loading 狀態
- [x] 5 個 `startX()` 函式開頭加上與 Set 對應的早期 return，快速連點同一顆按鈕不會送出第二次請求
- [x] Human Test 過程中發現一個獨立於本次範圍的 Bug：不同影片的手動觸發（例如影片 A 還在處理、點擊影片 B 的 Teach Back）不會立即開始，必須等影片 A 完成——RCA 確認這**不是** Sprint 4.1 既有的 Single Worker Queue 設計（那個機制只序列化 Transcript／Study Note 的自動生成，程式碼註解已明確記載這 5 個模組刻意不經過 `_pipeline_queue`／single worker thread）；真正原因是這 5 個端點宣告成 `async def`，但內部直接呼叫同步（blocking）的 Gemini SDK，卡住 uvicorn 唯一的事件迴圈，連帶讓所有其他請求（包含不同影片的獨立呼叫、`GET /api/queue` 輪詢）一起被卡住。使用者確認此為 Bug（違反既有設計意圖，非架構決策），指示併入 Task 3 以最小範圍修正：5 個端點的 Gemini 呼叫皆改為 `await asyncio.to_thread(gemini_client.generate_X, ...)`，不重構、不動 Queue 設計、不修改 `gemini_client.py`
- [x] 修正後重新 Human Test：不同影片可同時處理不互相阻塞、Loading 狀態正常、無 Regression

新增共用 `buildTriggerButton()` 取代 5 個模組各自重複的按鈕建立程式碼。僅修改 `app/static/script.js`（Loading 狀態）、`app/main.py`（新增 `import asyncio`，5 個端點的 Gemini 呼叫改為 `asyncio.to_thread`）。未修改 `app/gemini_client.py`、`app/static/style.css`（沿用既有 `:disabled` 樣式）、Queue 設計（`_pipeline_queue`／single worker thread 不變）、Stage Guard、Queue Store 寫入結構、History、Export、Chrome Extension。

**過程記錄：** 第一輪 Human Test（正常情境／快速連點／既有功能迴歸）PASS，但「不同影片平行處理」FAIL——使用者主動要求先確認這是否為既有 Single Worker Queue 的預期設計，再決定修程式或改 Proposal。Assistant 讀 `main.py` 確認 `_pipeline_queue`／`_pipeline_worker_loop`（Sprint 4.1）只處理自動 Transcript／Study Note 流程，5 個 Learning Model 端點的既有程式碼註解本就明確寫著不經過這個 Queue，判定為 Bug 而非架構問題。使用者確認後指示併入 Task 3、限定最小修正範圍（不重構、不整理其他程式、不動 Queue 設計）。修正後重新 Human Test 三項（平行處理、Loading 狀態、Regression）皆 PASS。

### Task 2 — Queue Card 模組展開／收合 ✅ Completed

範圍在 Proposal 階段兩度簡化：原始構想是 Accordion（一次只展開一個、自動收合前一個），使用者確認後改為單純獨立展開／收合，不做 Accordion、不做互斥、不做自動收合。

- [x] 5 個模組（Rapid Learning／Learning Blueprint／Teach Back／Action List／Review）的標題列皆可點擊切換展開／收合，箭頭方向正確切換（▶ 收合／▲ 展開）
- [x] 5 個模組各自獨立收合狀態，互不連動（收合 A 不影響 B／C／D／E），沒有 Accordion 互斥邏輯
- [x] 預設維持展開（與 Task 2 之前的既有行為一致），只新增「可以收合」的能力
- [x] Teach Back／Action List／Review 的下載按鈕移到收合區塊外面，收合狀態下仍可正常下載
- [x] Rapid Learning 既有的「▶ 展開完整內容」內層 toggle（Sprint 7 Task 2）完全不變，這次只在外面多包一層模組層級的收合
- [x] 收合後再次展開：內容正常顯示、不重新呼叫 API、不重新生成內容、不出現空白內容

新增共用 `buildModuleToggleHeader()`，5 個模組各自一個獨立的「收合中」Set（`collapsedRapidLearningCards`／`collapsedLearningBlueprintCards`／`collapsedTeachBackCards`／`collapsedActionListCards`／`collapsedReviewCards`），比照既有 `expandedKnowledgeOutlineCards` 的跨輪詢重繪存活模式。僅修改 `app/static/script.js`（5 個 `buildXSection()` 改為標題＋可收合主體）、`app/static/style.css`（新增 `.rapid-learning-module-header`／`.rapid-learning-module-arrow`／`.rapid-learning-module-body.is-hidden`）。未修改任何後端、Task 1 inline 錯誤機制、Task 3 Loading／`buildTriggerButton()`、Queue／History／Export、Chrome Extension。

**過程記錄：** Proposal 最初依你回饋的 UX Issue 規劃成 Accordion（一次一個、自動收合前一個），過程中額外釐清「Study Note」在 Queue Card 裡其實沒有行內展開區塊（只會自動下載，History 頁面的「開啟 Study Note」是另開新分頁），確認使用者所指其實是 Rapid Learning。提出 Accordion Proposal 後，使用者主動簡化需求，改為單純獨立展開／收合，理由是維持 MVP、避免過度設計；重新規劃並確認 Scope 後實作，Human Test 6 項（展開/收合、獨立 Toggle、收合後功能、Rapid Learning 迴歸、整體 Regression、再次展開）全數 PASS。

### Task 4 — `classify_error()` 分類精確度改善 ✅ Completed

- [x] Quota／Rate Limit／Auth 關鍵字（`quota`／`429`／`503`／`overloaded`／`rate limit`／`api key`／`unauthorized`／`401`／`403`）命中時，依 `stage` 分流訊息文字：`stage == "studynote"`（Gemini 呼叫）才顯示「可能是 Gemini API 額度已用完」；`download`／`transcript`（yt-dlp／本機 Whisper，皆不呼叫 Gemini）改顯示新增的通用訊息「服務目前無法使用或過於忙碌，請稍後再試。」，不再誤標成 Gemini 問題
- [x] `_NO_TRANSCRIPT`／`_CONTENT_FILTERED`／`_PRIVATE_OR_UNAVAILABLE`／`_YOUTUBE_RESTRICTED`／`_NETWORK_ISSUE`／`_UNKNOWN` 邏輯與文字皆不變（迴歸）

僅修改 `app/error_messages.py`（新增 `_SERVICE_UNAVAILABLE_SOURCE` 常數＋一行 stage 分流判斷）。未修改 `main.py` 任何呼叫點的 `stage` 參數、Workflow、Stage Guard、Single Worker、UI、其他模組。

**過程記錄：** Proposal 階段確認 Root Cause：Quota 關鍵字判斷未依 stage 區分來源，`download`／`transcript` 階段若剛好命中 `429`／`403` 等數字（yt-dlp／YouTube 本身的錯誤碼），會被誤判成 Gemini 額度問題。Proposal 審閱過程中使用者以真實 Human Test 案例（見 `Acceptance_Test.md`）帶出一個更深的既有落差：`main.py` 的字幕下載失敗會被靜默吞掉，若後續 Whisper fallback 也失敗，最終看到的是「找不到可用的逐字稿內容」而非真正的 429 原因——這需要同時修改 `app/main.py` 才能解決，超出本次「只改 `error_messages.py`」的 Scope，經使用者確認後列入 Product Backlog，不併入 Task 4。本次 Scope 內的修正以純函式呼叫窮舉所有分支驗證（含使用者提供的真實 429 錯誤文字），確認修正生效且無既有分支被影響；Human Test 以使用者已回報的真實案例（YouTube 字幕 429 → Retry → Transcript／Study Note 皆成功）作為正式驗收證據，PASS。

---

## Sprint 8.5A — Product Intelligence Foundation

依 `docs/00_Project_Management/Engineering_Kickoff/Engineering_Kickoff_Sprint_8_5_Product_Intelligence.md` 與 Factory Standard `Product_Intelligence_Foundation_v1.0.md` 規劃。本 Sprint 不新增任何 AI 功能、不修改 UI／Prompt，純建立 Backend 可觀測性（Observability）。開發流程新增 Architecture Review 階段（Repository Analysis → Architecture Review → Implementation Plan → Coding），核准後才開始 Task 1。

Engineering Rules（Task 1 核准時一併確認，全 Task 適用）：Backward Compatible（既有 MVP 流程不受影響）、Zero UI Changes、Feature Flag Friendly（`PRODUCT_INTELLIGENCE_ENABLED` 環境變數可整體關閉）、Observability 絕不可中斷正常流程（所有寫入皆 best-effort，失敗吞掉不拋出）。

### Task 1 — Correlation ID 基礎建設 + Runtime Intelligence ✅ Completed

- [x] `queue_store.add_item()` 產生 `request_id`（uuid4），鏡射進 `history_store.add_entry()`，供項目被移出 Queue 後仍可追溯
- [x] 新增 `app/observability/`（`logger.py`／`runtime_metrics.py`／`daily_report.py`），JSONL 記錄 Queue／Transcript／Study Note／Download 四個階段的起訖時間與成功/失敗，寫入 `outputs/logs/runtime.jsonl`
- [x] `daily_report.json` 每筆事件即時增量更新（非每日批次重算）

**Test Date:** 2026-08-07　**Test Result:** PASS——同一支影片全流程共用同一組 `request_id`，不同影片各自產生不同 `request_id`，MVP 既有流程不受影響。

### Task 2 — Cost Intelligence ✅ Completed

- [x] `app/gemini_client.py` 建立單一攔截點 `_generate_content()`，涵蓋全部 7 個 `generate_*()` 函式，讀取 `response.usage_metadata`（含 `thoughts_token_count`）換算估算成本，寫入 `outputs/logs/gemini_usage.jsonl`
- [x] `daily_report.json` 新增 `usage`（`api_calls`／`estimated_cost`／`by_model`／`by_artifact_type`）
- [x] 追加：所有 `estimated_cost` 欄位皆補上 `"currency": "USD"`；新增 `study_package` 統計（只計入 `quick_summary` + `study_note` 兩個核心流程自動觸發的 Gemini 呼叫，於 Study Note 階段成功時結算，5 個選用 Learning Model 產出不計入）

**Test Date:** 2026-08-07　**Test Result:** PASS——Token／估算成本記錄正確，Daily Report 正確彙總。

### Task 3 — Cache Intelligence ✅ Completed

- [x] 新增 `app/observability/cache_metrics.py`，於既有 7 處 `find_cached_*` 快取檢查點記錄 hit/miss，寫入 `outputs/logs/cache.jsonl`
- [x] Estimated Cost Saved 優先採當天真實平均成本（`daily_report.average_cost_for_artifact_type()`），無資料時退回 `Cost_Analysis.md` 記載的 MVP 期間估算值當 fallback（會隨真實資料累積自動被取代，包含 Knowledge Outline 以外的其餘 4 個 Learning Model 產出，不需額外修改程式）
- [x] `daily_report.json` 新增 `cache`（`hits`／`misses`／`hit_rate`／`estimated_cost_saved`／`by_artifact_type`）

**Test Date:** 2026-08-07　**Test Result:** PASS——第一次執行為 MISS，重複執行變 HIT，Daily Report 快取統計正確。

### Task 4 — Error Intelligence ✅ Completed

- [x] 新增 `app/observability/error_metrics.py`；Gemini 相關失敗集中在 `gemini_client.py` 的 `_generate_content()` 記錄（涵蓋全部 7 種 artifact_type、含先前完全未記錄的 quick_summary 靜默失敗與 5 個獨立端點），非 Gemini 失敗（Download／Transcription／Worker 未預期例外／Study Note 非 Gemini 未預期例外）於既有 4 個 `last_error` 記錄點補上，避免與 Gemini 錯誤重複計數
- [x] `retry_count` 於寫入當下即時查詢 `errors.jsonl`（同一 (video_id, stage) 今天已發生幾次），不新增 `queue_store` 欄位
- [x] `daily_report.json` 新增 `errors`（`count`／`by_stage`）

**Test Date:** 2026-08-07　**Test Result:** PASS。使用者確認不另外進行 API Key 移除等 Developer 層級測試，建議未來以自動化測試覆蓋 Exception 路徑（見下方 Product Backlog）。

**端對端驗證：** 挑選真實處理過的影片（`5o4OsLjINuQ`），確認同一組 `request_id` 完整串接 Runtime（Queue→Transcript→Study Note→Download）、Gemini Usage（quick_summary／study_note／knowledge_outline）、Cache（miss→hit）三份 log 與 `daily_report.json`，全部一致。

**Sprint 8.5A（Product Intelligence Foundation）全部完成：Task 1～4。**

僅修改 `app/gemini_client.py`／`app/queue_store.py`／`app/history_store.py`／`app/main.py`，新增 `app/observability/`（`logger.py`／`runtime_metrics.py`／`cost_metrics.py`／`cache_metrics.py`／`error_metrics.py`／`daily_report.py`）。未修改任何 UI（`templates/`／`static/`）、任何 Prompt 內容、既有 API 回傳格式。

---

## External Beta Deployment — Task T1 — Beta Token Authentication Foundation ✅ Completed

依 T1 Proposal 規劃（Closed Beta，5–10 位受邀測試者，無登入／帳號／資料庫）。本 Task 只解決「這次請求是誰」（`tester_id`）的辨識問題，不涉及 `queue_store`／`history_store`／`usage_quota` 等既有儲存路徑，也尚未接入任何既有 Route（接入為 T3 待辦）。

- [x] 新增 `app/beta_auth.py`：`_parse_beta_tokens()`（解析 `BETA_TOKENS` 環境變數，逗號分隔，每項為 `token` 或 `token:nickname`）、`is_beta_mode_enabled()`、`get_tester_id()`（FastAPI dependency，解析順序：本機模式 bypass → 合法 Cookie → 合法 `?beta=` query param（並建立／更新 Cookie）→ 403）
- [x] `app/main.py` 新增獨立診斷端點 `GET /api/beta/whoami`（`Depends(beta_auth.get_tester_id)`），尚未接入任何既有功能路由

**Root Cause Diagnosis（2026-08-12，Read-Only）：** 前一日 Human Test Scenario 2 Step 2 一度 FAIL（設定 `BETA_TOKENS` 後仍回傳 `local`）。經比對程式碼（`_parse_beta_tokens()` 為 request-time 讀取 `os.environ`，非 import-time 快取）與 Uvicorn `reload=True` 於 Windows 上的子行程機制（`multiprocessing` spawn 對應 Windows `CreateProcess` 預設完整繼承父行程環境變數）確認兩者皆非程式碼缺陷；判定為前一日 PowerShell 操作／環境變數設定問題，非 production code defect。經全新 PowerShell 視窗重新設定並驗證後，該 Step 已 PASS。

**Self Test：** PASS

**Human Test Scenario 1 — Local Backward Compatibility：** PASS（未設定 `BETA_TOKENS` 時，`get_tester_id()` 一律回傳 `local`，不檢查 Cookie／Query Param，不可能觸發 403）

**Human Test Scenario 2（設定 `BETA_TOKENS = "demoTokenA:Tester1,demoTokenB:Tester2"`）：**

| Step | 對應 AC | 驗證內容 | 結果 |
|---|---|---|---|
| Step 1 | — | 設定 `BETA_TOKENS` 並重新啟動 Server | PASS |
| Step 2 | AC4 前置 | 不帶 Token 訪問 `/api/beta/whoami` → `403 Invalid or missing beta token` | PASS |
| Step 3 | AC3 | 合法 `?beta=demoTokenA` → `200`，回傳正確 `tester_id`，並設定 Cookie（HttpOnly／Secure／SameSite=Lax） | PASS |
| Step 4 | AC4 | 不合法 `?beta=wrongToken` → `403`，且不設定 Cookie（以全新無痕視窗測試，避開既有合法 Cookie） | PASS |
| Step 5 | AC5 | 已有合法 Cookie 時，不帶 `?beta=` 仍回傳相同 `tester_id` | PASS |
| Step 6 | AC6（前半） | 將 `demoTokenA` 自 `BETA_TOKENS` 移除並重啟 Server 後，原持有 `demoTokenA` Cookie 的請求 → `403` | PASS |
| Step 7 | AC6（後半） | 同一瀏覽器改帶合法 `?beta=demoTokenB` → `200`，回傳正確 `tester_id`，Cookie 更新 | PASS |

**T1（Beta Token Authentication Foundation）Scenario 1、Scenario 2（Step 1–7，AC3–AC6）全數 PASS。** 僅新增 `app/beta_auth.py`、`app/main.py` 新增一個獨立診斷端點，未修改／未接入任何既有 Route（Queue／History／Usage Quota 等）、未修改 UI。T3（既有 Route 接入）尚未開始，不在本次範圍內。

### T2 — Beta Session Foundation

**Status：CANCELLED / NOT REQUIRED**

**Decision：** T1 `get_tester_id()` 已經是完整、可重用的 FastAPI dependency，T3 可以直接透過 `Depends(beta_auth.get_tester_id)` 取得 `tester_id`。建立額外 Session／Context abstraction 沒有增加目前所需能力，因此依 Keep It Simple／Avoid Over-engineering 原則取消 T2。編號保留（不重新編號 T3），以保留既有文件與程式碼歷史語意。

### T3 — Existing Route Authentication Integration ✅ Completed

**Goal：** 只做 Authentication Gating——將 T1 的 `Depends(beta_auth.get_tester_id)` 接入需要保護的既有 Route，不涉及資料隔離（資料隔離為獨立的 T4）。

**Scope（實作後核實）：** `app/main.py` 中既有的 **19** 個 API Route（Queue／History／Usage／Transcript／Study Note／Knowledge Outline／Download／Export）＋ `GET /`（作為 `?beta=` Cookie bootstrap 入口）＋ `GET /history`，共 **21** 個既有 Route 加上 `Depends(beta_auth.get_tester_id)`；加上 T1 既有的 `GET /api/beta/whoami`，**合併後總共 22 個受保護 Route**（先前 Spec 階段誤寫「20 個 API Route」，經 `inspect.signature` 逐一程式內省核實更正為 19）。

**Out of Scope：** `queue_store.py`／`history_store.py`／`app/observability/usage_quota.py` 的資料模型或函式簽名（皆未修改，`git diff` 為空）、per-tester 資料隔離（見下方 T4）。

**Acceptance Criteria — 全數 PASS：**

| AC | 內容 | 結果 |
|---|---|---|
| AC1 | 未設定 `BETA_TOKENS` 時，本機既有流程保持完全相容 | ✅ PASS |
| AC2 | Beta Mode 開啟後，沒有合法 token 的受保護 Route 回傳 403 | ✅ PASS |
| AC3 | 合法 Beta Tester token 可以正常使用受保護 Route | ✅ PASS |
| AC4 | 原有 Queue → Transcript → Study Note → Knowledge Outline → Download／Export → History 流程沒有 Regression | ✅ PASS |
| AC5 | T3 不宣稱已完成 per-tester data isolation | ✅ PASS（`queue_store.py`／`history_store.py`／`usage_quota.py` 皆無變更；不同合法 token 目前仍共用同一份 Queue／History／Usage 資料，留給 T4 處理） |

**Automated Verification：** `httpx.AsyncClient` + `ASGITransport` in-process 測試，22 個受保護 Route × 4 情境（Local Mode／No Token／Invalid Token／Valid Token）＝ 88 項斷言全數 PASS，且測試後確認未留下任何測試殘留資料。

**Human Verification（Beta Mode，`demoTokenA`／`demoTokenB`）：** Scenario 2 Step 1-7（對應 AC2、AC3）逐步以真實瀏覽器驗證，全數 PASS——設定 `BETA_TOKENS` 並重啟、無 Token 訪問 403、合法 `?beta=` 建立 Cookie、非法 `?beta=` 403 且不設 Cookie、Cookie 複用、Token 移除後舊 Cookie 403、重新提供合法 Token 可恢復。

**Human Verification（Local Mode，`BETA_TOKENS` 完全未設定）：** 停止舊 Server、確認 Port 8000 釋放、以純 Local Mode 重新啟動並確認無 stale process 後，完整跑一次真實流程並全數 PASS：首頁載入無 403 → 新影片（含 Playlist 長網址）加入 Queue → Transcript 自動完成並自動下載一次 → 手動產生 Study Note 並自動下載一次 → 30秒快速學習正常顯示且未觸發重複下載 → 📦 下載知識包 ZIP 正確且未觸發額外自動下載 → History 頁面／開啟 Transcript／開啟 Study Note 皆正常且未觸發自動下載。

**過程記錄：** T3 Human Test 期間發現一個與 T3 Authentication 無關的既有 Bug——`app/static/script.js` 的自動下載邏輯在 fresh session 載入大量既有 Completed Queue 項目時會觸發大量重複下載（BUG-01），經 RCA 確認與 T3 無因果關係後，以獨立 Task 修正並驗收，已獨立 commit（`5449f14`），不算入 T3 Scope。

### T4 — Per-Tester Data Isolation

**Status：Backlog，尚未設計、尚未實作**

- **Goal：** 讓不同 Beta Tester 的 Queue／History／Usage Quota／Transcript／Study Note／Export 等資料存取依 `tester_id` 隔離，使 Tester A 無法看見或下載 Tester B 的資料，Usage 額度也不互相共用。
- **依賴：** 需先完成 T3（Authentication Gating），隔離邏輯才有可信任的 `tester_id` 來源。
- **已知影響範圍（T3 Implementation Readiness Review，2026-08-12 確認，非新增判斷）：** `queue_store.py`、`history_store.py`、`app/observability/usage_quota.py` 三個模組目前皆為單一全域共享狀態（無 `tester_id` 欄位），需要重新設計資料結構與讀寫函式簽名才能支援 per-tester 分流。
- **本次不展開：** Scope／Files Expected to Change／Acceptance Criteria／Verification Plan，待正式進入 T4 規劃階段再定義。

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
- [ ] Learning Blueprint Error Path（`GeminiGenerationError` → HTTP 500）：重試策略、錯誤訊息與 UI 提示、是否自動重試。獨立 Bug Fix Task，不併入 Sprint 7 Task 3／4。發現於 Task 3／4 Human Test 期間（Assistant 短時間內連續呼叫約 15 次 Gemini API 做一致性驗證時觸發過一次，非常態重現）

  **需求：** 目前 Extension 僅支援 `https://www.youtube.com/watch?v=`，未支援 `https://www.youtube.com/shorts/`。Shorts 頁面需顯示 YB Learn 按鈕，點擊直接加入 Queue，不需手動貼網址，體驗與一般影片一致。
- [ ] Queue Card 預設保持簡潔，只顯示一句話重點與學習入口，詳細內容預設收合、按需展開（Sprint 8 Task 2 Human Test 提出的 UX Improvement，非本次範圍）：5 個模組（Rapid Learning／Learning Blueprint／Teach Back／Action List／Review）預設收合，點擊後才展開。Task 2 已完成的是「可以收合」，這項是「預設就收合」，屬於後續獨立的 UX 決策，不併入 Task 2。
- [x] **（過時描述已於 2026-08-11 修正）字幕下載 429 被靜默吞掉，Whisper fallback 也失敗時顯示誤導訊息**（原記錄於 Sprint 8 Task 4 Human Test，Feature 004 驗收彙整曾誤引用為「未修復」）：核心 429 attribution 機制（保留字幕下載失敗的原始錯誤文字、Whisper fallback 也失敗時優先使用該原因，而非顯示誤導性的「找不到可用的逐字稿內容」）**已由 Feature 001 User Story 1（commit `59572c0`，2026-08-08）修復**，本條目此前的敘述未反映此事實，屬記錄疏漏，非重複 Bug。Feature 001 驗收當時該情境的真實重現（`Acceptance_Test.md` T003：字幕 429 ＋ Whisper 也失敗）因依賴 YouTube 端限流時機，屬 NOT REPRODUCED（非 FAIL）。2026-08-11 額外完成的收斂修復（見 `Acceptance_Test.md` 對應章節）：`app/error_messages.py` 新增字幕專屬訊息「YouTube 字幕目前暫時無法取得，請稍後再試。」，`app/main.py` 既有的窄範圍收斂分支（字幕分類為 `_SERVICE_UNAVAILABLE_SOURCE` 且 Whisper 分類為 `_NO_TRANSCRIPT`）改顯示此專屬訊息，取代原本沿用的通用「服務目前無法使用或過於忙碌」文字；未修改 `classify_error()` 分類邏輯、keyword、stage 判斷本身。
- [ ] Structure Detection 一致性改善（Sprint 8 Task 5，決定延後）：同一支內容特徵模糊的影片，重複生成 Learning Blueprint 可能得到不同 `structure_type`（`temperature=0` 已改善但未完全消除）。Proposal 已規劃修法（`_LEARNING_BLUEPRINT_SYSTEM_INSTRUCTION` 新增判斷優先順序規則），但審閱後判定：目前沒有可穩定重現的不一致案例，無法建立 Before／After 比較、無法定義明確 PASS／FAIL，不符合「可驗收的 Bug 優先」原則。**觸發條件：** 等之後再次遇到真實的 `structure_type` 判斷不一致案例（記錄下該案例的影片與兩次不同的判斷結果），再依該案例修正與驗收，不要在沒有真實案例時純靠猜測調整 Prompt。
- [ ] Beta Polish（原暫稱「Sprint 8.5」，因與 Product Intelligence Foundation 的 Sprint 8.5A 撞號，改為未排定 Sprint 編號的 Backlog 項目）：Queue Card 資訊層級預設簡潔化（見上方「Queue Card 預設保持簡潔」項）、學習入口依學習時間排序、其他 Beta 實際使用過程中發現的 UX 細節。屬於產品體驗優化，待評估排入哪個 Sprint。
- [ ] Sprint 8.5B — Visualization Layer（Engineering Kickoff Sprint 8.5 文件第 16 節已定義）：Runtime Dashboard／Cost Dashboard／Product Dashboard，完成 Product Intelligence Foundation 第二階段。待 Sprint 8.5A 統一 Push 後由使用者決定是否排入。
- [ ] 使用者輸入驗證失敗未被記錄（Sprint 8.5A Task 4 Human Test 期間使用者提出，Product Analytics 範疇，非 Error Intelligence 必備）：`POST /api/queue` 的 `InvalidYouTubeURLError`／`VideoMetadataError` 兩個拒絕點都在 `queue_store.add_item()`（產生 `request_id`）之前就以 `HTTPException` 擋掉，目前完全不會產生任何 Runtime／Error 紀錄，因此無法得知有多少使用者因輸入格式錯誤而失敗。若要補上，建議新增獨立的 `validation` 統計（例如 `invalid_url`／`unsupported_video`），不要併入 Runtime Error 統計以免混淆「系統執行失敗」與「使用者輸入錯誤」兩種不同性質的事件。
- [ ] `GeminiConfigError`（缺少 `GEMINI_API_KEY`）未被 Error Intelligence 記錄（Sprint 8.5A Task 4 Known Limitation）：發生在 `gemini_client._generate_content()` 攔截點「之前」，屬一次性環境設定問題而非執行期錯誤，Task 4 判斷優先度較低，先不處理。
- [ ] 5 個獨立 Learning Model 端點（Knowledge Outline／Learning Blueprint／Teach Back／Action List／Review）若因非 Gemini 原因失敗，目前沒有既有的 `last_error` 記錄點可掛 Error Intelligence（Sprint 8.5A Task 4 Known Limitation），維持原狀。
- [ ] **Product Flow / Monetization Requirement（下一階段，非 Feature 003 範圍，目前未實作 Freemium／Paywall）：** 修正先前記錄的認知落差——「30秒快速學習」（Knowledge Outline）**不是永久免費功能**。既定商業邏輯（Human 於 2026-08-10 確認）：
  1. Transcript：永久免費、自動產生、自動下載、不使用 Gemini。
  2. 30秒快速學習：使用者主動觸發，每次約 1 次 Gemini 呼叫；新使用者前 10 次免費，免費額度用完後採低額收費，定位為低成本快速學習產品。
  3. 完整 Study Note：使用者主動觸發，每次約 1 次 Gemini 呼叫，定位為較高價值的付費學習內容。
  4. 完整知識包：使用既有 Study Note／Transcript 等 artifacts 打包匯出，不額外呼叫 Gemini，隨完整 Study Note／付費方案提供。

  目前程式（Feature 003 Revised Scope）尚未實作任何用量計數、免費額度扣減或收費邏輯——Transcript／Study Note／30秒快速學習皆為使用者可無限次主動觸發，不受本項目影響。本項純粹記錄下一階段 Freemium／Paywall 設計依據，待獨立 Proposal 提出並確認 Scope 後才實作，不併入 Feature 003 或任何現行 Sprint/Task。
- [ ] **Bug — Queue Card UI Stale Processing State after Manual Study Note Generation**（原「Queue Card UI 狀態與實際 Study Note 完成狀態不同步」，Feature 004 Human Test Step 5 期間發現，2026-08-10；2026-08-11 完成 Read-Only Code RCA，**尚未實機穩定重現、本輪未修復**，非 Feature 004 Regression）：

  - **Symptom：** Study Note 實際已在後端完成，但 Queue 卡片持續停留在「Generating Study Note」、進度條持續運行；手動重新整理瀏覽器（F5）後卡片立即恢復正常 Completed 狀態。
  - **Confirmed Root Cause（依程式碼分析確認，非猜測；Backend state 正確，問題在 Frontend polling coverage）：** Feature 003 把 Study Note 改為使用者主動觸發（`startStudyNote()`），但前端唯一的即時輪詢機制 `pollPipelineProgress()`（`app/static/script.js:270`）只在 `handleCapture()`／`retryProcessing()` 兩處啟動；頁面載入時的 `loadQueue()`（`script.js:173`）只抓一次，不會為既有停在 `Transcript Ready` 的項目恢復輪詢。`POST /api/queue/{video_id}/study-note`（`app/main.py:856`）是同步阻塞端點（透過 `_await_job()`，逾時 600 秒），`startStudyNote()`（`script.js:827`）只在該 fetch 完全結束後呼叫一次 `loadQueue()`，中途無任何輪詢。因此只要使用者在「Transcript Ready → 點擊產生 Study Note」之間重新整理／關閉重開分頁（原本綁定該影片的 interval 隨頁面消失），Study Note 產生期間就完全沒有機制重新抓取 `/api/queue`，畫面凍結在點擊當下最後一次渲染的 `Generating` 狀態。進度條「持續運行」是純 CSS 動畫錯覺（`style.css:454`，`.progress-bar-fill` 在非 `is-determinate` 狀態套用 `animation: progress-slide 1.2s infinite`），與資料是否更新無關。Backend 狀態機本身正確（`main.py:570` 寫入 `Generating`，`main.py:602` 完成後寫入 `Study Note Ready`）。
  - **Severity：Medium**——不影響資料正確性、單次可用 F5 完全復原，但體感像系統卡住；觸發條件（重新整理頁面後再觸發）在真實使用情境下常見，非邊緣案例。
  - **Reproduction Conditions（依程式碼推導，尚未實機驗證）：** (1) 加入影片並等待 Transcript 完成（狀態變成 `Transcript Ready`）；(2) 重新整理頁面或關閉重開分頁，讓該影片原本的 `pollPipelineProgress` interval 消失；(3) 點擊「📓 產生 Study Note」；(4) Gemini 呼叫進行期間不觸發任何其他會呼叫 `loadQueue()` 的動作；(5) 預期卡片凍結在 Generating，直到該次 fetch 回應或使用者手動整理頁面。
  - **Workaround：** 重新整理頁面（Refresh）。
  - **Suggested Fix Direction（未實作，待排入修復時再確認最小修正範圍）：** 讓 `startStudyNote()` 觸發後也啟動與 `pollPipelineProgress(videoId)` 相同的輪詢；或頁面載入時對所有非終端狀態（`Transcript Ready`／`Generating` 等）項目一併恢復輪詢。
  - **Status：尚未實機穩定重現、尚未修復。** 觸發條件：等下次真實重現、或決定排入 Sprint 修復時，再依上方 Suggested Fix Direction 展開 Proposal 與 Human Test 驗收，不在沒有真實重現前直接修改程式。
- [ ] **BUG-02 / Investigation — Railway Production：YouTube Metadata / `POST /api/queue` 400**（2026-08-12 記錄，2026-08-13 完成 Read-Only RCA 與診斷 log 部署，狀態改為 Intermittent / Monitoring，與 T3 Beta Auth、BUG-01 Duplicate Download 為各自獨立問題）：

  - **已知證據 1（Local Mode 已實測 PASS）：** 使用含 `&list=...&index=...` 的 YouTube Playlist 長網址（`https://www.youtube.com/watch?v=fB4uipaYYeU&list=PLKrHjFg4YYFmcrZ_7vjkaN31Ax3U_42Rg&index=23`）在本機 Local Mode 完整走過一次：加入 Queue PASS、Transcript PASS、Transcript 自動下載一次 PASS、Study Note PASS、Study Note 自動下載一次 PASS。**因此目前沒有證據顯示 `&list=`／`&index=` 或 Playlist 長網址本身是問題**，不要把這個 Bug 歸類成「Long URL Bug」。
  - **已知證據 2（Railway Production 曾出現失敗）：** Railway Production 曾用同一支影片的 Playlist 長網址（`https://www.youtube.com/watch?v=JXDQglxJczE&list=PLKrHjFg4YYFmcrZ_7vjkaN31Ax3U_42Rg&index=10`）與乾淨網址（`https://www.youtube.com/watch?v=JXDQglxJczE`）皆出現 `POST /api/queue → 400 Bad Request`，UI 顯示「無法取得影片資訊」。
  - **已知證據 3（Railway Production 之後改為 PASS）：** 同一支影片 `JXDQglxJczE` 之後在 Railway Production 重測，metadata 標題正確載入（「I Made 100 Youtube Shorts with Claude Code in 5 minutes」）、加入 Queue 成功、Transcript 完成、Transcript.md 自動下載成功。**目前無法再重現先前的 400 失敗**，且期間未對 metadata 抓取邏輯、yt-dlp 或 requirements.txt 做任何修改，僅新增了診斷 log（見下）。原始 Railway 失敗當下的真實 exception 訊息目前仍未取得。
  - **Status：Intermittent / Monitoring。** `app/main.py` 的 `add_to_queue()` 已於 commit `1d0c2b3` 加入 `[BUG-02]` 診斷 print（`except youtube.VideoMetadataError as exc:` 分支），會在下次失敗重現時記錄原始例外訊息至 Railway Deploy Logs，目前保持啟用中以利未來重現時採證。
  - **Decision：** 在失敗重現且診斷 log 取得真正 Root Cause 之前，不進行任何程式修復（不修改 `fetch_video_metadata()`、不改 yt-dlp、不改 requirements.txt）。
- [ ] **Product Inspiration — YouTube In-Page Learning Panel**（2026-08-11 記錄，純產品洞察，未評估、未規劃、未開發）：

  - **Reference Product：** YT Transcript Generator——可直接在 YouTube 影片頁面右側顯示 Extension Panel，使用者不需離開 YouTube 即可操作 Transcript 功能。
  - **OwnLearn 未來構想：** 將目前的 Quick Capture Chrome Extension，未來升級為 YouTube In-Page Learning Panel。使用者觀看 YouTube 時，Extension 自動取得目前 Video URL／Video ID，直接在 YouTube 頁面側邊提供：Transcript／30秒快速學習／Study Note／Workflow 操作步驟／下載學習包。
  - **Product Value：** 核心不是模仿 Transcript Extension，而是把 OwnLearn 的完整學習流程帶進 YouTube——YouTube → Capture → Transcript → 30秒快速理解 → Study Note → Workflow → Learning Package，讓使用者盡量不需要離開 YouTube 即可完成快速學習。
  - **Priority：Future / Post External Beta。現階段不開發。** 目前優先順序仍是：Local MVP → External Beta Deployment → Beta Validation → 再評估 YouTube In-Page Learning Panel。
  - **Architecture Note：** 未來 External Beta Backend 部署完成後，Chrome Extension 不再呼叫 localhost API，改為呼叫 OwnLearn Cloud API，屆時再評估是否將結果直接渲染於 YouTube 頁面（與 Deployment Readiness Audit，2026-08-11 記錄的 Extension `127.0.0.1:8000` 硬編碼問題屬同一條演進路徑，但本項是更後面的獨立階段，不併入 Deployment Sprint）。
  - **Guardrail：** 不納入目前 Deployment Sprint、不修改 Extension、不修改 Backend、不建立 Proposal、不加入目前 Acceptance Criteria。