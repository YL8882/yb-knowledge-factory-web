# Prompt Engineering Standard

**Document Version:** v1.0 (Final)  
**Document Type:** Engineering Standard  
**Module:** 02_Prompt_Design  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final  
**Owner:** YB Knowledge Factory

---

# 1. Purpose

本文件定義 **YB Knowledge Factory** 的 Prompt Engineering 開發標準。

目的為建立一致的 Prompt 設計、開發、測試、版本管理與維護流程，使所有 AI Product 能共享相同的工程規範。

本文件適用於所有 Prompt 模組，不限於 Study Note。

---

# 2. Objectives

Prompt Engineering Standard 的目標：

- 建立一致的 Prompt 架構
- 提高 Prompt 可維護性
- 降低 Prompt 重複設計
- 建立模組化 Prompt
- 支援多模型（Gemini、GPT、Claude 等）
- 支援版本管理
- 支援 AI Workflow 自動化
- 提升 Prompt 品質與可測試性

---

# 3. Design Principles

所有 Prompt 應遵循以下原則：

## Single Responsibility

每個 Prompt 僅負責一項職責。

不得同時定義：

- AI Role
- 任務
- Output Format

---

## Separation of Concerns

Prompt 必須依職責分層。

不同層級不得互相混用。

---

## Reusability

Prompt 應可於不同 Workflow、不同產品及不同模型間重複使用。

---

## Maintainability

Prompt 修改應集中於單一文件，不影響其他模組。

---

## Model Agnostic

Prompt 不應依賴特定 LLM。

應可套用於：

- Gemini
- ChatGPT
- Claude
- DeepSeek
- 未來其他模型

---

## Consistency

相同輸入應產生一致的輸出品質與結構。

---

# 4. Prompt Architecture

所有 AI Product 必須遵循四層架構：

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
```

各層職責如下：

| Layer | Responsibility |
|--------|----------------|
| AI Role Specification | 定義 AI 身分、能力與知識分析原則 |
| System Instructions | 定義固定執行規則與限制 |
| Task Prompt | 定義本次任務 |
| Output Schema | 定義輸出格式與資料結構 |

---

# 5. Prompt Development Workflow

所有 Prompt 應依照以下流程開發：

```text
Product Requirement
        │
        ▼
Define Output
        │
        ▼
Design AI Role
        │
        ▼
Create System Instructions
        │
        ▼
Create Task Prompt
        │
        ▼
Define Output Schema
        │
        ▼
Prepare Examples
        │
        ▼
Prompt Testing
        │
        ▼
Review
        │
        ▼
Release
```

不得跳過 Output Schema 或測試流程。

---

# 6. Folder Standard

Prompt 模組統一採用以下結構：

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

# 7. Naming Convention

所有 Prompt 文件應遵循：

```text
<Product>_<Component>_v<Version>.md
```

例如：

```text
StudyNote_AI_Role_Specification_v1.0.md

StudyNote_System_Instructions_v1.0.md

StudyNote_Task_Prompt_v1.0.md

StudyNote_Output_Schema_v1.0.md
```

不得使用模糊命名，例如：

- Prompt.md
- Prompt_Final.md
- New Prompt.md

---

# 8. Version Control

版本規則：

| Version | Description |
|----------|-------------|
| Major | 架構重大變更 |
| Minor | 新增功能或規則 |
| Patch | 文字修正、描述優化 |

例如：

```text
v1.0

v1.1

v1.2

v2.0
```

---

# 9. Testing Standard

每個 Prompt 必須經過測試。

至少包含：

- 正常案例（Happy Path）
- 邊界案例（Edge Case）
- 錯誤案例（Error Case）

測試內容包含：

- Markdown 是否正確
- Schema 是否符合
- Output 是否完整
- 是否有幻想內容（Hallucination）
- 是否符合 AI Role

---

# 10. Review Process

Prompt 發布前應完成：

- 自我檢查
- 人工審查
- AI 測試
- Workflow 驗證
- Release Review

未通過 Review 不得正式使用。

---

# 11. Best Practices

建議：

- Prompt 保持簡潔
- 單一文件負責單一職責
- 重複規則集中管理
- Output Schema 保持穩定
- 專有名詞保持一致
- 優先引用既有文件，不重複撰寫內容

避免：

- 將 AI Role 寫入 Task Prompt
- 將 Output Format 寫入 AI Role
- 將任務需求寫入 System Instructions

---

# 12. Prompt Lifecycle

Prompt 生命週期如下：

```text
Requirement
        │
        ▼
Design
        │
        ▼
Development
        │
        ▼
Testing
        │
        ▼
Review
        │
        ▼
Release
        │
        ▼
Maintenance
```

每次版本更新皆應重新測試。

---

# 13. Future Compatibility

本標準適用於所有 AI Product：

- Study Note
- Knowledge Card
- SOP
- Prompt Library
- Skills
- Agent
- Course
- Business Model
- AI Product

未來新增產品時，應沿用相同 Prompt Engineering 架構。

---

# 14. Related Documents

```text
02_Prompt_Design/
│
├── README.md
├── Prompt_Architecture.md
├── Prompt_Engineering_Standard_v1.0.md
├── Prompt_Test_Plan.md
│
├── 00_AI_Roles/
│   └── <Product>_AI_Role_Specification.md
│
├── 01_System_Prompts/
│   └── <Product>_System_Instructions.md
│
├── 02_Task_Prompts/
│   └── <Product>_Task_Prompt.md
│
├── 03_Output_Schemas/
│   └── <Product>_Output_Schema.md
│
├── 04_Examples/
└── 05_Testing/
```

---

# 15. Success Criteria

Prompt Engineering Standard 應達成：

- 所有 Prompt 採用一致架構
- 各模組職責清楚
- Prompt 易於維護
- Prompt 易於測試
- Prompt 可跨模型使用
- Prompt 可跨產品重複使用
- Prompt 支援版本管理
- Prompt 支援 AI Workflow 自動化

---

# Document Status

| Item | Value |
|------|-------|
| Document | Prompt Engineering Standard |
| Version | v1.0 (Final) |
| Product | YB Knowledge Factory MVP v0.1 |
| Status | ✅ Final |