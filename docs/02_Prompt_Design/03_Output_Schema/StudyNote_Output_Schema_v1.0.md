# StudyNote Output Schema

**Document Version:** v2.0 (Final)
**Document Type:** Output Schema Specification
**Module:** 02_Prompt_Design / 03_Output_Schema
**Product:** YB Knowledge Factory MVP v0.1
**Status:** Final

---

# 1. Purpose

本文件定義 **Study Note** 的官方輸出結構（Output Schema）。

自 v2.0 起，本文件之輸出結構**完全同步**於：

```text
docs/04_Templates/StudyNote_Template_v3.0.md
```

`StudyNote_Template_v3.0.md` 為 Study Note 輸出格式的**唯一官方格式（Single Source of
Truth）**。本文件僅將該 Template 轉譯為適用於 AI 模型（Gemini、Claude Code 等）的
Output Schema 描述，不得與 Template 產生結構差異。若兩者未來出現不一致，應以
Template 為準並回頭修正本文件。

Output Schema 規範所有 AI 模型必須遵循的輸出格式，以確保：

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
- 結構固定，與 `StudyNote_Template_v3.0.md` 完全一致
- 易閱讀
- 易搜尋
- 易維護
- 易於 AI 再利用
- 可直接存入 Obsidian

---

# 4. Document Structure

Study Note 應依照以下固定章節輸出：

```text
{{影片名}}（標題）
│
├── 影片網址
│
├── 一句話摘要
│
├── 重點摘要
│
├── 重點解析
│   └── 主題一、主題二、主題三……
│
├── 操作流程
│   └── Step 1、Step 2、Step 3……
│
└── 延伸資訊
    ├── 關鍵字（Keywords）
    ├── Tags
    └── 延伸研究
```

不得新增、刪除或重新排列章節。

---

# 5. 標題與影片網址

文件開頭直接以影片名稱作為標題，並列出影片網址，格式如下：

```markdown
# {{影片名}}

**影片網址：**
{{影片網址}}
```

本 Schema 不使用獨立的 Metadata 區塊（不包含 Author / Date / Language / Tags /
Version 等欄位）；影片名稱與網址即為文件唯一必要的來源資訊。

---

# 6. 一句話摘要

目的：

100 字內說明本影片最重要的核心內容，讓讀者快速了解影片大意。

規則：

- 僅寫一段。
- 不分點。
- 不超過 100 字（繁體中文字數）。
- 避免細節，聚焦核心重點。

---

# 7. 重點摘要

列出最重要重點。

規則：

- 使用條列式（Bullet List）。
- 建議 5 點左右。
- 每點一句，避免展開說明。

---

# 8. 重點解析

Study Note 主體，依主題重新組織內容，不得依照逐字稿原始順序排列。

格式：

```markdown
## 主題一（或 00:00－xx:xx）

- 重點
- 重點

---

## 主題二（或 xx:xx－xx:xx）

- 重點
- 重點
```

主題數量依影片內容彈性增減，每個主題之間以 `---` 分隔。

---

# 9. 操作流程

若影片包含明確操作流程或步驟，依序使用：

```markdown
### Step 1

...

### Step 2

...
```

若影片沒有明確操作流程，整段內容填寫：

```text
本影片無明確操作流程。
```

不得省略本章節標題。

---

# 10. 延伸資訊

包含三個固定子章節，缺一不可：

## 關鍵字（Keywords）

列出影片重要關鍵字或名詞，使用條列式。

## Tags

列出 Hashtag 形式標籤，例如：

```markdown
- #AI
- #VibeCoding
- #ClaudeCode
```

## 延伸研究

列出值得延伸研究的主題、技術、工具或商業觀點，使用條列式。

若某子章節無對應內容，仍須保留標題並註明「本影片未提及」。

---

# 11. Markdown Rules

允許：

- `#`
- `##`
- `###`
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

# 12. Naming Rules

章節名稱固定，須與下列名稱完全一致：

```text
{{影片名}}

影片網址

一句話摘要

重點摘要

重點解析

操作流程

延伸資訊
├── 關鍵字（Keywords）
├── Tags
└── 延伸研究
```

不得自行改名、翻譯或調整順序。

---

# 13. Quality Requirements

Study Note 應符合：

✓ 結構與 `StudyNote_Template_v3.0.md` 完全一致

✓ Markdown 正確

✓ 重點完整

✓ 易閱讀

✓ 易搜尋

✓ 可直接存入 Obsidian

✓ AI 可再次解析

---

# 14. Validation Checklist

輸出完成後應確認：

- 標題為影片名稱
- 影片網址存在
- 一句話摘要不超過 100 字
- 重點摘要存在
- 重點解析依主題分段
- 操作流程存在（無流程時已填寫替代文字）
- 延伸資訊包含關鍵字、Tags、延伸研究三個子章節
- Markdown 正確
- 無空章節（若無內容須註明「本影片未提及」）
- 無杜撰內容
- 無重複內容

---

# 15. Dependencies

本 Schema 由以下文件共同組成：

```text
StudyNote_AI_Role_Specification_v1.0.md

↓

StudyNote_System_Instructions_v1.0.md

↓

StudyNote_Task_Prompt_v1.0.md

↓

StudyNote_Output_Schema_v1.0.md（本文件，結構同步自 04_Templates/StudyNote_Template_v3.0.md）

↓

Study_Note.md
```

---

# 16. Future Compatibility

本 Schema 應支援：

- Knowledge Card Generator
- SOP Generator
- Prompt Library Builder
- Agent Builder
- Course Builder
- AI Product Builder

所有後續 AI Workflow 均應以本 Schema（即 `StudyNote_Template_v3.0.md`）作為輸入來源。

---

# 17. Version Policy

版本管理：

- Major：Schema 結構重大變更，或與 Template 同步時的結構調整
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
└── 03_Output_Schema/
    └── StudyNote_Output_Schema_v1.0.md（本文件）

04_Templates/
└── StudyNote_Template_v3.0.md（唯一官方格式 / Single Source of Truth）
```

---

# Document Status

| Item | Value |
|------|-------|
| Document | StudyNote Output Schema |
| Version | v2.0 (Final) |
| Product | YB Knowledge Factory MVP v0.1 |
| Status | ✅ Final — Synced with StudyNote_Template_v3.0.md |
