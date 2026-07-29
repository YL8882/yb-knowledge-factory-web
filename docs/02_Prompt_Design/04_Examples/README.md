# Examples

**Document Version:** v1.0 (Final)  
**Document Type:** Module README  
**Module:** 02_Prompt_Design / 04_Examples  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final  
**Owner:** YB Knowledge Factory

---

# 1. Purpose

本資料夾存放 **YB Knowledge Factory** 的官方 Prompt 範例（Reference Examples）。

每個 Example 均代表一個完整、可重複執行的 Prompt Pipeline，提供開發、測試、驗證與版本比較使用。

Examples 並非教學文件，而是 Prompt Engineering 的官方參考實作（Reference Implementation）。

---

# 2. Objectives

Examples 的主要目的：

- 驗證 Prompt 設計是否符合規格
- 驗證 Output Schema 是否正確
- 建立標準輸入與輸出
- 提供 Prompt 測試案例
- 建立 Regression Test Dataset
- 作為未來 AI Product 開發的參考範本

---

# 3. Example Structure

每個 Example 應包含完整的 Prompt Pipeline。

建議結構如下：

```text
Example_xx/

├── Transcript_Input.md
├── Prompt_Assembly.md
├── Expected_StudyNote_Output.md
└── Notes.md
```

---

# 4. File Description

## Transcript_Input.md

提供 AI 的標準輸入資料。

內容通常包含：

- Video Title
- Video URL
- Transcript

此文件作為 Prompt Pipeline 的輸入來源。

---

## Prompt_Assembly.md

記錄實際送入 AI 的 Prompt 組合方式。

由以下模組組成：

```text
AI Role Specification
        │
        ▼
System Instructions
        │
        ▼
Task Prompt
        │
        ▼
Output Schema
        │
        ▼
Transcript Input
```

此文件用於確認 Prompt Pipeline 是否符合設計規範。

---

## Expected_StudyNote_Output.md

定義官方預期輸出（Expected Output）。

此文件作為：

- Prompt 測試標準
- Output 比對基準
- Regression Test Benchmark

所有測試結果皆應與此文件進行比較。

---

## Notes.md

記錄每次測試資訊，包括：

- 測試日期
- Prompt 版本
- Model
- Temperature（若適用）
- Token 使用量（若可取得）
- 測試結果
- 已知問題
- 修正紀錄

此文件有助於後續 Prompt 優化與版本追蹤。

---

# 5. Naming Convention

Example 命名建議：

```text
Example_01_StudyNote

Example_02_LongTranscript

Example_03_MixedLanguage

Example_04_PoorTranscript

Example_05_Podcast
```

採用流水號加主題，方便擴充與管理。

---

# 6. Development Workflow

建立新 Example 時，應依照以下流程：

```text
Prepare Transcript
        │
        ▼
Assemble Prompt
        │
        ▼
Execute Prompt
        │
        ▼
Compare Expected Output
        │
        ▼
Record Notes
        │
        ▼
Review & Improve
```

---

# 7. Testing Principles

所有 Example 應符合以下原則：

- 使用固定輸入資料
- 使用固定 Prompt 架構
- 使用固定 Output Schema
- 保留完整測試紀錄
- 可跨模型重複驗證
- 可作為 Regression Test

---

# 8. Future Expansion

Examples 將逐步擴充至不同情境，例如：

- 長篇逐字稿
- 多語言逐字稿
- Podcast
- 訪談內容
- AI 教學影片
- 技術文件
- 品質較差的逐字稿

每新增一種情境，均應建立對應 Example。

---

# 9. Related Documents

```text
02_Prompt_Design/
│
├── README.md
├── Prompt_Architecture.md
├── Prompt_Engineering_Standard_v1.0.md
├── Prompt_Test_Plan.md
│
├── 00_AI_Roles/
├── 01_System_Prompts/
├── 02_Task_Prompts/
├── 03_Output_Schemas/
├── 04_Examples/
└── 05_Testing/
```

---

# 10. Success Criteria

Examples 應達成以下目標：

- 提供完整 Prompt Pipeline 範例
- 提供固定測試資料
- 提供標準預期輸出
- 支援 Prompt 品質驗證
- 支援 Regression Testing
- 支援未來 AI Product 擴充

---

# Folder Structure

```text
04_Examples/
│
├── README.md
│
├── Example_01_StudyNote/
│   ├── Transcript_Input.md
│   ├── Prompt_Assembly.md
│   ├── Expected_StudyNote_Output.md
│   └── Notes.md
│
├── Example_02_LongTranscript/
├── Example_03_MixedLanguage/
├── Example_04_PoorTranscript/
└── Example_05_Podcast/
```

---

# Document Status

| Item     | Value                         |
| -------- | ----------------------------- |
| Document | Examples README               |
| Version  | v1.0 (Final)                  |
| Product  | YB Knowledge Factory MVP v0.1 |
| Status   | ✅ Final                       |