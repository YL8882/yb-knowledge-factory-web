---
Version: v1.0
Status: Draft
Owner: YB
Document: MVP Test Report
Category: Quality Assurance
Purpose: Record MVP v0.1 acceptance test execution and results.
Scope: YB Knowledge Factory MVP v0.1
Priority: High
Last Updated: 2026-07-29
Related Documents:
  - docs/99_Milestone/Milestone_02_Build_MVP/Acceptance_Test.md
  - docs/01_Product_Requirements/Core/PRD.md
  - docs/02_Prompt_Design/03_Output_Schema/StudyNote_Output_Schema_v1.0.md
  - app/TODO.md
---

# MVP Test Report

> YB Knowledge Factory MVP v0.1 — Acceptance Test Execution

---

# 1. Test Environment

| Item | Value |
|------|-------|
| Platform | Windows 11 |
| Python | 3.14.6 |
| Backend | FastAPI 0.104.1 + Uvicorn 0.24.0 |
| Video Metadata / Audio | yt-dlp 2026.7.4 |
| Speech-to-Text | faster-whisper 1.2.1 (model: `base`, device: cpu, compute_type: int8) |
| AI Model | Gemini 2.5 Flash (via `google-genai` 2.14.0) |
| Test Date | 2026-07-29 |

---

# 2. 已完成功能（Completed Features）

- 首頁 UI：YouTube URL 輸入框、Generate 按鈕
- YouTube URL 驗證（regex）與影片中繼資料擷取（yt-dlp，支援一般網址與 `/shorts/`）
- Queue（記憶體內）：新增、列表、移除、重複網址偵測、100 筆上限
- Transcript：yt-dlp 下載音訊（暫存）→ faster-whisper 轉錄 → 存成 `outputs/transcripts/{Title}_{VideoID}.md`
- Study Note：讀取 Transcript → Gemini 2.5 Flash 依 `StudyNote_Output_Schema_v1.0` 產生 → 存成 `outputs/study_notes/{Title}_{VideoID}.md`
- Download：`/api/queue/{video_id}/transcript/download`、`/api/queue/{video_id}/study-note/download`
- Gemini API Key 透過 `.env`／環境變數讀取，不寫入程式碼、不印出於任何 log

---

# 3. 驗收結果

## 3.1 完整流程測試

測試影片：`https://www.youtube.com/watch?v=jNQXAC9IVRw`（"Me at the zoo"）

| Step | 項目 | 結果 |
|------|------|------|
| 1 | YouTube URL → 加入 Queue | ✅ PASS |
| 2 | Queue → Transcript | ✅ PASS |
| 3 | Transcript → Study Note | ✅ PASS |
| 4 | Download Transcript.md | ✅ PASS（`Content-Disposition: attachment`） |
| 5 | Download Study_Note.md | ✅ PASS（`Content-Disposition: attachment`） |

補充：先前 Sprint 已另外驗證過 Shorts 網址（`/shorts/...`）與一支約 10 分鐘中文長影片的 Transcript 全流程，皆為 PASS（詳見對話紀錄，未重複列於本報告的即時測試中）。

---

## 3.2 Study Note 格式驗收

比對項目為使用者於本次驗收指定的 6 項欄位。目前實作採用的是 `docs/02_Prompt_Design/03_Output_Schema/StudyNote_Output_Schema_v1.0.md`（AI Role + System Instructions + Task Prompt + Output Schema 四份文件組成的正式 `StudyNote_Prompt_v1.0`），而非 `docs/04_Templates/StudyNote_Template_v3.0.md` 的舊版章節命名。兩者章節名稱不同，但內容涵蓋範圍一致，對應如下：

| 驗收項目 | 對應章節 | 結果 |
|----------|----------|------|
| 影片名稱 | Metadata → `Title` | ✅ PASS |
| 影片網址 | Metadata → `Source`，另於 `References` 重複列出 | ✅ PASS |
| 100 字摘要 | `Executive Summary`（已於本次驗收調整 Prompt，明確限制 100 字內、單段） | ✅ PASS |
| 分段重點 | `Detailed Notes`（依主題以 `###` 子標題分段） | ✅ PASS |
| Workflow／操作步驟 | `Workflow`（無流程時填「本影片無明確操作流程」） | ✅ PASS |
| 延伸資訊－關鍵字 | `Core Concepts` | ✅ PASS（以同義章節呈現） |
| 延伸資訊－標籤 | Metadata → `Tags`（本次驗收發現並修正的 Bug，見 4.1） | ✅ PASS（修正後) |
| 延伸資訊－延伸主題 | `Future Research` | ✅ PASS（以同義章節呈現） |

⚠️ **待您確認**：`Core Concepts` / `Future Research` 是否可視為「關鍵字」「延伸主題」的正式對應章節，或您希望改回 `04_Templates/StudyNote_Template_v3.0.md` 的原始章節命名。目前實作尚未變更章節結構，僅修正 Tags 欄位空白的問題。

---

## 3.3 錯誤情境測試

| 情境 | 測試方式 | 結果 |
|------|----------|------|
| 空白網址 | `POST /api/queue {"url": ""}` | ✅ PASS — HTTP 400「無效的 YouTube 網址」 |
| 無效網址 | `POST /api/queue {"url": "https://example.com/foo"}` | ✅ PASS — HTTP 400「無效的 YouTube 網址」 |
| 不存在影片 | `POST /api/queue` 傳入格式正確但不存在的 Video ID | ✅ PASS — HTTP 400「無法取得影片資訊」，未當機 |
| Gemini API Key 未設定 | 於獨立 process 移除 `GEMINI_API_KEY` 後呼叫 `generate_study_note_body` | ✅ PASS — 拋出 `GeminiConfigError`（「缺少 GEMINI_API_KEY 環境變數，請先設定後再試」），API 端會回傳 HTTP 500 並還原 Queue 狀態為 `Transcript Ready` |
| Gemini API 呼叫失敗 | 使用無效 API Key 呼叫 Gemini | ✅ PASS — 拋出 `GeminiGenerationError`（「API key not valid...」），API 端回傳 HTTP 500 並還原 Queue 狀態；正式環境亦曾實際遇到 Gemini 503（暫時過載）並成功走此錯誤路徑 |

私人影片（真正的私人網址）與長影片測試，依您先前指示列為 Release Candidate 驗證項目，本次未納入 Blocking 驗收範圍。

---

# 4. Bug 修正記錄

## 4.1 Study Note Metadata 的 Tags 欄位一直空白

**問題**：`build_metadata_block()` 中 `Tags:` 欄位從未被賦值，永遠輸出空白。

**修正**：
- 調整 Gemini System Instruction，要求回應第一行輸出 `Tags: #tag1 #tag2 #tag3`
- `gemini_client.generate_study_note_body()` 改為解析並拆分 Tags 與主體內容，回傳 `{"tags": ..., "body": ...}`
- `study_note.save_study_note()` 新增 `tags` 參數並寫入 Metadata

**驗證**：重測後 Metadata 正確輸出，例如 `Tags: #動物 #大象 #生物特徵 #動物園`。

## 4.2 Executive Summary 字數未限制

**問題**：先前 Prompt 未限制 Executive Summary 字數，可能超出使用者要求的「100 字摘要」。

**修正**：System Instruction 明確要求「100 字以內、僅一段、不分點」。

## 4.3 References 章節曾誤判為「本影片未提及」

**問題**（上一個 Sprint 發現並已修正，本次重新確認未回歸）：Gemini 誤將使用者提供的影片標題／網址視為「逐字稿未提及」而省略。已於 System Instruction 明確說明此為已知來源資訊，非杜撰內容，重測後 PASS。

---

# 5. 已知問題（Known Issues，非 Blocking）

| 項目 | 說明 |
|------|------|
| anyio 版本衝突 | `fastapi==0.104.1` 宣告需要 `anyio<4.0.0`，但 `google-genai` 安裝時將 `anyio` 升級至 4.14.2，pip 顯示相依性衝突警告。實測伺服器啟動與所有端點皆正常運作，暫無實際影響，但建議未來升級 FastAPI 版本時一併處理。 |
| ffmpeg 未安裝 | `yt-dlp` 執行時顯示 `ffmpeg not found` 警告。目前透過下載原生音訊格式＋faster-whisper 內建 PyAV 解碼可正常運作，但若遇到需要合併／轉檔的影片格式可能失敗。建議正式環境安裝 ffmpeg。 |
| Queue 僅存於記憶體 | 伺服器重啟後 Queue 內容會清空（符合 MVP 不使用 Database 的技術決策），Transcript／Study Note 檔案本身則持久保存於 `outputs/`。 |
| Whisper `base` 模型偶有轉錯字 | 例如將 "trunks" 誤判為 "punks"，Gemini 有時會自行判讀修正、有時原樣保留。屬 CPU 輕量模型的準確度取捨，可於未來評估升級模型大小。 |
| 首次執行需下載 Whisper 模型 | 需要網路連線從 Hugging Face 下載，之後會快取於本機，不影響離線後續使用。 |
| Gemini API 偶發 503 過載 | 目前無自動重試機制，失敗會直接回傳錯誤並還原 Queue 狀態，需使用者手動重新觸發。 |
| 長影片／私人影片未完整驗收 | 已於先前 Sprint 個別測試長影片（~10 分鐘）Transcript 成功；私人影片僅以「不存在的 Video ID」模擬錯誤處理路徑，未使用真正的私人網址測試。依指示列為 Release Candidate 項目。 |
| Study Note 章節命名 | 採用 `StudyNote_Output_Schema_v1.0.md` 的章節命名（Core Concepts / Future Research 等），與 `04_Templates/StudyNote_Template_v3.0.md` 的舊版命名（關鍵字 / 延伸研究等）不同。內容涵蓋一致，但命名需您確認是否符合預期。 |

---

# 6. 後續待辦（Backlog，非本次範圍）

以下項目明確排除於本次 Sprint 與驗收範圍之外，尚未開始：

- Knowledge Card Generator
- SOP Generator
- Prompt Library Builder
- Obsidian 整合／同步
- Queue 持久化儲存（例如 `queue.json` 或資料庫）
- Gemini API 失敗自動重試機制
- ffmpeg 自動安裝／封裝
- 前端自動輪詢處理狀態（目前需手動點擊各階段按鈕）
- 長影片／私人影片正式驗收（Release Candidate 階段執行）
- 多語系 UI、Mobile App、雲端同步、多人協作、登入／訂閱（PRD 明列 Out of Scope）

---

# 7. Definition of Done 對照

依 `Acceptance_Test.md` 與 `TODO.md` 的 Definition of Done：

- [x] 可輸入 YouTube URL
- [x] 可取得影片標題
- [x] 可產生 Transcript
- [x] 可產生 Study Note
- [x] 可下載 Transcript.md
- [x] 可下載 Study_Note.md
- [x] 完成基本操作流程測試

---

# 8. Test Result

| Tester | Date | Result |
|--------|------|--------|
| Claude Code | 2026-07-29 | 本報告所列項目：PASS（詳見 3.1–3.3），待您最終驗收確認 |

---

End of Document
