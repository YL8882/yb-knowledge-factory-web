# Prompt Assembly

**Document Version:** v1.0 (Final)  
**Document Type:** Example Execution Guide  
**Module:** 02_Prompt_Design / 04_Examples / Example_01_StudyNote  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final  
**Owner:** YB Knowledge Factory

---

# 1. Purpose

本文件說明 **Example_01_StudyNote** 如何組裝完整 Prompt，並送交大型語言模型（LLM）執行。

本文件屬於範例執行文件（Example Execution Guide），示範正式的 Prompt Pipeline。

所有 Prompt 元件均引用正式規格文件，不在此重複定義。

---

# 2. Prompt Pipeline

本範例採用 YB Knowledge Factory 標準 Prompt Pipeline：

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
        │
        ▼
LLM
        │
        ▼
Study_Note.md
```

---

# 3. Prompt Components

本範例使用以下 Prompt 元件：

| Order | Component | Purpose |
|------:|-----------|---------|
| 1 | StudyNote_AI_Role_Specification_v1.0.md | 定義 AI 身分、能力與知識分析原則 |
| 2 | StudyNote_System_Instructions_v1.0.md | 定義固定執行規則 |
| 3 | StudyNote_Task_Prompt_v1.0.md | 定義本次任務 |
| 4 | StudyNote_Output_Schema_v1.0.md | 定義輸出格式 |
| 5 | Transcript_Input.md | 提供待分析逐字稿 |

---

# 4. Assembly Sequence

Prompt 必須依照固定順序組裝。

```text
Load AI Role Specification

↓

Load System Instructions

↓

Load Task Prompt

↓

Load Output Schema

↓

Append Transcript Input

↓

Execute Prompt
```

不得調整組裝順序。

---

# 5. Runtime Example

執行時，模型收到的 Prompt 概念如下：

```text
========================================
StudyNote AI Role Specification
========================================

(角色定義)

========================================
StudyNote System Instructions
========================================

(固定執行規則)

========================================
StudyNote Task Prompt
========================================

(本次任務)

========================================
StudyNote Output Schema
========================================

(輸出格式)

========================================
Transcript Input
========================================

(影片逐字稿)
```

所有元件共同構成最終 Prompt。

---

# 6. Prompt Responsibilities

各元件負責不同職責，不得重複。

| Component | Responsibility |
|-----------|----------------|
| AI Role | 定義 AI 身分、分析能力與知識原則 |
| System Instructions | 定義固定執行規則 |
| Task Prompt | 定義本次工作內容 |
| Output Schema | 定義輸出格式與章節 |
| Transcript Input | 提供原始資料 |

遵循單一職責原則（Single Responsibility Principle）。

---

# 7. Execution Rules

執行 Prompt 時應遵守：

- 不修改 AI Role。
- 不修改 System Instructions。
- 不修改 Output Schema。
- 保留 Transcript 原始內容。
- 僅依任務需要更新 Task Prompt 與 Transcript Input。

---

# 8. Expected Output

完成後應產生：

```text
Study_Note.md
```

內容應完全符合：

- StudyNote_Output_Schema_v1.0.md
- StudyNote_AI_Role_Specification_v1.0.md
- StudyNote_System_Instructions_v1.0.md

---

# 9. Validation

執行完成後應確認：

- Prompt 組裝順序正確。
- 所有元件均已載入。
- Study Note 結構符合 Output Schema。
- 無遺漏重要內容。
- 無新增未提供資訊。
- Markdown 格式正確。

---

# 10. Related Documents

```text
02_Prompt_Design/

00_AI_Roles/
└── StudyNote_AI_Role_Specification_v1.0.md

01_System_Prompts/
└── StudyNote_System_Instructions_v1.0.md

02_Task_Prompts/
└── StudyNote_Task_Prompt_v1.0.md

03_Output_Schemas/
└── StudyNote_Output_Schema_v1.0.md

04_Examples/
└── Example_01_StudyNote/
    ├── Transcript_Input.md
    ├── Prompt_Assembly.md
    ├── Expected_StudyNote_Output.md
    └── Notes.md
```

---

# 11. Success Criteria

本 Example 應達成：

- 成功組裝完整 Prompt。
- 成功執行 Prompt Pipeline。
- 成功產生符合 Output Schema 的 Study Note。
- 可於 Google AI Studio、Gemini API、Claude Code 等環境重複執行。
- 可作為未來 Prompt Regression Test 的標準案例。

---

# Document Status

| Item | Value |
|------|-------|
| Document | Prompt Assembly |
| Version | v1.0 (Final) |
| Product | YB Knowledge Factory MVP v0.1 |
| Status | ✅ Final |