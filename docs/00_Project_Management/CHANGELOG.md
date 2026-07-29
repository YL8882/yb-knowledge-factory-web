---
Version: v1.0
Status: Final
Owner: YB
Document: CHANGELOG
Category: Project Management
Purpose: Record all major changes to the project, documentation, architecture, specifications, and milestones.
Scope: All AI Products
Priority: High
Author: ChatGPT
Last Updated: 2026-07-29
Related Documents:
  - Project_Dashboard.md
  - Development_Operating_System.md
  - Documentation_Standard.md
---

# CHANGELOG

> Official change history for the AI Product.

---

# Purpose

本文件記錄專案的重要變更。

目的：

- 記錄版本演進
- 記錄重大設計決策
- 記錄文件更新
- 記錄 Milestone 完成
- 提供專案歷史追蹤

本文件**不記錄**：

- 每日開發過程
- 小幅文字修正
- 臨時測試

僅記錄重要版本。

---

# Version History

---

## v0.1

Date

2026-07-20

Status

Project Started

### Added

- 建立 MVP 專案
- 建立基礎資料夾
- 建立 README
- 建立 CLAUDE

---

## v0.2

Date

2026-07-24

Status

Prototype

### Added

- Google AI Studio Prototype
- UI Wireframe
- Queue Design
- Quick Capture Design

---

## v1.0

Date

2026-07-29

Status

Architecture Complete

### Added

Project Foundation：

- Development_Operating_System.md
- Documentation_Standard.md

Product Specification：

- Product_Architecture.md
- PRD.md
- Workflow_Specification.md
- Prompt_Specification.md
- Runtime_Specification.md
- Output_Specification.md
- Wireframe_Specification.md
- UI_Component_Specification.md

Project Management：

- Project_Dashboard.md
- Stage_Review_Checklist.md

---

## MVP v0.1

Date

2026-07-29

Status

Build Complete — Acceptance Test Passed

### Added

FastAPI Web Application（`app/`）：

- 首頁 UI（YouTube URL 輸入框、Generate 按鈕）
- YouTube URL 驗證與影片中繼資料擷取（yt-dlp，支援一般網址與 `/shorts/`）
- Learning Queue（記憶體內，含新增／列表／移除／重複偵測）
- Transcript 產生（yt-dlp + Faster Whisper），存成 `outputs/transcripts/`
- Study Note 產生（Gemini 2.5 Flash），存成 `outputs/study_notes/`
- Transcript.md／Study_Note.md 下載端點
- `.env` 讀取 GEMINI_API_KEY（不寫入程式碼、不印出於 log）

### Changed

- `StudyNote_Output_Schema_v1.0.md` 更新為 v2.0，結構完全同步 `StudyNote_Template_v3.0.md`，
  確立 Template 為 Study Note 輸出格式的唯一官方來源（Single Source of Truth）
- README.md 更新為反映實際功能與安裝步驟

### Fixed

- Study Note Metadata 的 Tags 欄位一直空白，已修正為由 Gemini 產生標籤
- Executive Summary（一句話摘要）未限制字數，已修正為 100 字內
- References／延伸資訊未正確帶入影片標題與網址，已修正 Prompt 指示

### Testing

- 完成 MVP v0.1 驗收測試，詳見 `docs/MVP_Test_Report.md`
- 完整流程（YouTube URL → Queue → Transcript → Study Note → 下載）：PASS
- 錯誤情境（空白網址／無效網址／不存在影片／Gemini Key 未設定／Gemini 呼叫失敗）：PASS

### Known Issues

- anyio 版本相依性警告（`google-genai` 與 `fastapi==0.104.1` 的 anyio 版本要求衝突，
  實測運作正常）
- ffmpeg 未安裝警告（目前不影響功能）
- Queue 僅存於記憶體，伺服器重啟後清空（Transcript／Study Note 檔案本身持久保存）

---

# Change Categories

重大更新分類：

| Category | Description |
|----------|-------------|
| Added | 新增功能或文件 |
| Changed | 重大修改 |
| Improved | 改善 |
| Deprecated | 停止使用 |
| Removed | 移除 |
| Fixed | 修正重大問題 |

---

# Recording Rules

以下情況必須更新 CHANGELOG：

- 新增正式文件
- 新增 Milestone
- 完成 Stage Gate
- 架構重大修改
- Workflow 重大修改
- Prompt 規格重大修改
- 發布新版本

以下情況不用更新：

- 錯字修正
- 排版調整
- 小幅內容補充
- 臨時測試

---

# Version Naming

建議版本：

```
v0.1

↓

v0.2

↓

v0.5

↓

v1.0

↓

v1.1

↓

v2.0
```

---

# References

- Project_Dashboard.md
- Development_Operating_System.md
- Documentation_Standard.md

---

End of Document