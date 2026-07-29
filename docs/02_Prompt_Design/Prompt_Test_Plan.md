# Prompt Test Plan

**Document Version:** v1.0 (Final)  
**Document Type:** Test Plan  
**Module:** 02_Prompt_Design  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final  
**Owner:** YB Knowledge Factory

---

# 1. Purpose

本文件定義 **YB Knowledge Factory** 的 Prompt 測試規範。

目的在於建立一致的 Prompt 驗證流程，確保所有 Prompt 在正式發布前皆符合品質、穩定性與可維護性的要求。

本文件適用於所有 Prompt 模組，不限於 Study Note。

---

# 2. Objectives

Prompt 測試目標：

- 驗證 Prompt 是否符合設計需求
- 驗證 Output Schema 是否正確
- 驗證不同模型輸出的一致性
- 驗證 Prompt 是否容易維護
- 驗證 Workflow 是否正常運作
- 降低 Hallucination（模型幻覺）
- 建立 Prompt 品質基準

---

# 3. Test Scope

所有 Prompt 均須完成以下測試：

- AI Role Specification
- System Instructions
- Task Prompt
- Output Schema
- Prompt 組合流程
- 完整 Workflow

---

# 4. Test Environment

建議測試環境：

| 項目 | 建議 |
|------|------|
| Primary | Google AI Studio |
| Secondary | Gemini API |
| Optional | ChatGPT |
| Optional | Claude |
| Workflow | n8n |
| Backend | FastAPI |

---

# 5. Test Workflow

所有 Prompt 應依照以下流程測試：

```text
Prepare Input
        │
        ▼
Load AI Role
        │
        ▼
Load System Instructions
        │
        ▼
Load Task Prompt
        │
        ▼
Load Output Schema
        │
        ▼
Execute Prompt
        │
        ▼
Validate Output
        │
        ▼
Review
        │
        ▼
Approve
```

---

# 6. Test Categories

## 6.1 Functional Test

確認 Prompt 是否完成指定任務。

驗證：

- 是否完成任務
- 是否符合需求
- 是否缺少內容

---

## 6.2 Output Validation

確認輸出符合 Schema。

檢查：

- Markdown
- 標題
- 表格
- Code Block
- 章節順序

---

## 6.3 Quality Test

確認：

- 是否容易閱讀
- 是否容易理解
- 是否容易搜尋
- 是否可作為知識資產

---

## 6.4 Consistency Test

使用相同輸入重複測試。

確認：

- 結構一致
- 名詞一致
- 品質一致

---

## 6.5 Robustness Test

使用特殊輸入：

- 很短 Transcript
- 很長 Transcript
- 缺少 Metadata
- 中英文混合
- 雜訊內容

確認 Prompt 是否仍正常工作。

---

# 7. Test Cases

至少建立以下案例：

| Test ID | Type | Description |
|---------|------|-------------|
| TC-001 | Happy Path | 正常影片逐字稿 |
| TC-002 | Short Transcript | 極短逐字稿 |
| TC-003 | Long Transcript | 超長逐字稿 |
| TC-004 | Missing Metadata | 缺少影片資訊 |
| TC-005 | Mixed Language | 中英混合內容 |
| TC-006 | Noisy Transcript | 含大量口語與贅詞 |

---

# 8. Validation Checklist

每次測試均須確認：

## Structure

- Metadata 完整
- 章節完整
- Markdown 正確

---

## Content

- 無遺漏重要知識
- 無重複內容
- 無幻想內容
- 無杜撰資訊

---

## Quality

- 易閱讀
- 易理解
- 易搜尋
- 易複習

---

## Workflow

- 能供後續 AI 使用
- 能供 Knowledge Card 使用
- 能供 SOP 使用

---

# 9. Acceptance Criteria

Prompt 通過測試需符合：

| 項目 | 標準 |
|------|------|
| Markdown | 100% 正確 |
| Schema | 完全符合 |
| Hallucination | 不得出現 |
| Missing Content | 不得遺漏核心內容 |
| Structure | 完整一致 |
| Readability | 良好 |
| Reusability | 可重複使用 |

---

# 10. Defect Classification

測試發現問題時，依嚴重程度分類：

| Level | Description |
|--------|-------------|
| Critical | 無法完成任務 |
| High | Output Schema 錯誤 |
| Medium | 內容遺漏或格式不一致 |
| Low | 文字、排版或描述問題 |

---

# 11. Test Report

每次測試完成後應記錄：

- Prompt Version
- Model Version
- Test Date
- Tester
- Input Source
- Output Result
- Issues
- Conclusion

---

# 12. Release Criteria

Prompt 發布前須符合：

- 全部測試完成
- 無 Critical Issue
- 無 High Issue
- Output Schema 完全符合
- Workflow 驗證完成
- 人工 Review 通過

---

# 13. Continuous Improvement

Prompt 發布後仍應持續：

- 收集測試案例
- 優化 Prompt
- 更新測試資料
- 建立 Regression Test
- 建立 Benchmark Dataset

---

# 14. Related Documents

```text
02_Prompt_Design/
│
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

# 15. Success Criteria

Prompt Test Plan 應達成：

- 所有 Prompt 均完成測試
- 所有 Prompt 品質一致
- Output Schema 完整符合
- Workflow 可穩定執行
- 支援多模型驗證
- 降低後續維護成本
- 建立可持續改善的 Prompt QA 流程

---

# Document Status

| Item | Value |
|------|-------|
| Document | Prompt Test Plan |
| Version | v1.0 (Final) |
| Product | YB Knowledge Factory MVP v0.1 |
| Status | ✅ Final |