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
- [ ] Learning Blueprint Error Path（`GeminiGenerationError` → HTTP 500）：重試策略、錯誤訊息與 UI 提示、是否自動重試。獨立 Bug Fix Task，不併入 Sprint 7 Task 3／4。發現於 Task 3／4 Human Test 期間（Assistant 短時間內連續呼叫約 15 次 Gemini API 做一致性驗證時觸發過一次，非常態重現）

  **需求：** 目前 Extension 僅支援 `https://www.youtube.com/watch?v=`，未支援 `https://www.youtube.com/shorts/`。Shorts 頁面需顯示 YB Learn 按鈕，點擊直接加入 Queue，不需手動貼網址，體驗與一般影片一致。