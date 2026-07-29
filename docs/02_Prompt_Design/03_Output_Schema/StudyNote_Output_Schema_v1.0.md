# StudyNote Output Schema

**Document Version:** v1.0 (Final)  
**Document Type:** Output Schema Specification  
**Module:** 02_Prompt_Design / 03_Output_Schemas  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# 1. Purpose

本文件定義 **Study Note** 的官方輸出結構（Output Schema）。

Output Schema 是 Study Note 的標準資料契約（Data Contract），規範所有 AI 模型必須遵循的輸出格式，以確保：

- 結構一致
- 品質一致
- 易於閱讀
- 易於搜尋
- 易於版本管理
- 易於後續 AI 自動化處理

本文件不定義 AI 行為，也不描述任務內容。

---

# 2. Scope

本 Schema 適用於：

- Google AI Studio
- Gemini API
- FastAPI
- Claude Code
- n8n Workflow
- 未來所有支援的 LLM

所有 Study Note 均必須符合本 Schema。

---

# 3. Output Principles

Study Note 必須符合以下原則：

- Markdown 格式
- 結構固定
- 易閱讀
- 易搜尋
- 易維護
- 易於 AI 再利用
- 可直接存入 Obsidian

---

# 4. Document Structure

Study Note 應依照以下固定章節輸出：

```text
Metadata
│
├── Executive Summary
│
├── Key Takeaways
│
├── Detailed Notes
│
├── Core Concepts
│
├── Workflow
│
├── Tools
│
├── Best Practices
│
├── Key Decisions
│
├── Future Research
│
└── References
```

不得新增、刪除或重新排列章節。

---

# 5. Metadata Schema

文件開頭必須包含 Metadata：

```markdown
# Study Note

Title:

Source:

Author:

Date:

Language:

Tags:

Version:
```

Metadata 主要供：

- Obsidian
- Search
- Workflow
- AI Retrieval

使用。

---

# 6. Executive Summary

目的：

一句話說明影片核心內容。

建議：

1～3 段。

避免細節。

---

# 7. Key Takeaways

列出最重要重點。

建議：

5～15 點。

每點一句。

---

# 8. Detailed Notes

Study Note 主體。

依照主題重新組織。

不得依照逐字稿順序。

可使用：

```markdown
## 主題

### 子主題

- 重點
```

---

# 9. Core Concepts

整理：

- 定義
- 名詞
- 架構
- Framework

例如：

| Concept | Description |
|----------|-------------|
| Agent | ... |

---

# 10. Workflow

若影片包含流程：

使用：

```text
Input

↓

Process

↓

Output
```

若無流程：

可省略內容，但保留章節。

---

# 11. Tools

整理：

- Tool
- Model
- Framework
- Library

建議格式：

| Tool | Purpose |
|------|----------|

---

# 12. Best Practices

整理：

作者提出：

- 建議
- 經驗
- 注意事項

使用條列。

---

# 13. Key Decisions

整理：

作者的重要判斷。

例如：

- 為什麼不用某工具
- 為什麼採某 Workflow

---

# 14. Future Research

列出：

值得延伸研究：

- 技術
- Prompt
- Tool
- Framework
- Business

---

# 15. References

至少包含：

- Video Title
- Video URL

若有：

- 官方網站
- GitHub
- Paper

亦可整理。

---

# 16. Markdown Rules

允許：

- #
- ##
- ###
- Bullet List
- Number List
- Table
- Code Block
- Block Quote

禁止：

- HTML
- XML
- JSON
- YAML 作為主要輸出

---

# 17. Naming Rules

章節名稱固定。

例如：

```text
Executive Summary

Key Takeaways

Detailed Notes

Core Concepts

Workflow

Tools

Best Practices

Key Decisions

Future Research

References
```

不得自行改名。

---

# 18. Quality Requirements

Study Note 應符合：

✓ 結構一致

✓ Markdown 正確

✓ 重點完整

✓ 易閱讀

✓ 易搜尋

✓ 可直接存入 Obsidian

✓ AI 可再次解析

---

# 19. Validation Checklist

輸出完成後應確認：

- Metadata 完整
- 所有章節存在
- Markdown 正確
- 無空章節（若無內容可註明「本影片未提及」）
- 無杜撰內容
- 無重複內容

---

# 20. Dependencies

本 Schema 由以下文件共同組成：

```text
StudyNote_AI_Role_Specification_v1.0.md

↓

StudyNote_System_Instructions_v1.0.md

↓

StudyNote_Task_Prompt_v1.0.md

↓

StudyNote_Output_Schema_v1.0.md

↓

Study_Note.md
```

---

# 21. Future Compatibility

本 Schema 應支援：

- Knowledge Card Generator
- SOP Generator
- Prompt Library Builder
- Agent Builder
- Course Builder
- AI Product Builder

所有後續 AI Workflow 均應以本 Schema 作為輸入來源。

---

# 22. Version Policy

版本管理：

- Major：Schema 結構重大變更
- Minor：新增章節或欄位
- Patch：文字修正與說明優化

---

# Related Documents

```text
02_Prompt_Design/
│
├── 00_AI_Roles/
│   └── StudyNote_AI_Role_Specification_v1.0.md
│
├── 01_System_Prompts/
│   └── StudyNote_System_Instructions_v1.0.md
│
├── 02_Task_Prompts/
│   └── StudyNote_Task_Prompt_v1.0.md
│
└── 03_Output_Schemas/
    └── StudyNote_Output_Schema_v1.0.md
```

---

# Document Status

| Item | Value |
|------|-------|
| Document | StudyNote Output Schema |
| Version | v1.0 (Final) |
| Product | YB Knowledge Factory MVP v0.1 |
| Status | ✅ Final |