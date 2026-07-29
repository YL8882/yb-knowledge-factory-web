# Prompt Specification

**Document Version:** v1.0 (Final)  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# 1. Purpose

本文件定義 **YB Knowledge Factory MVP v0.1** 的 Prompt 設計規範。

Prompt 是 AI 產生 Study Note 的核心資產，因此需具備：

- 一致性（Consistency）
    
- 可維護性（Maintainability）
    
- 可重複使用（Reusability）
    
- 可版本管理（Version Control）
    

本文件規範 Prompt 的設計方式，而非記錄實際 Prompt 內容。

---

# 2. Design Principles

所有 Prompt 必須遵循以下原則：

1. 單一職責（Single Responsibility）
    
2. 固定輸入格式
    
3. 固定輸出格式
    
4. Markdown 輸出
    
5. 台灣繁體中文
    
6. 不依賴特定模型
    
7. 可獨立測試
    
8. 可版本化管理
    

---

# 3. Prompt Workflow

```text
Transcript.md
        │
        ▼
StudyNote_Prompt_v1.0
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
Study_Note.md
```

Prompt 僅負責：

> 將逐字稿轉換為高品質學習筆記。

---

# 4. Prompt Catalog

MVP v0.1 僅包含一個 Prompt。

|Prompt ID|名稱|狀態|
|---|---|---|
|Prompt-001|StudyNote_Prompt_v1.0|Active|

未來版本可新增：

- Prompt-002：Knowledge Card
    
- Prompt-003：SOP Generator
    
- Prompt-004：Prompt Library
    
- Prompt-005：Course Builder
    

---

# 5. Input Specification

Prompt 輸入來源：

```text
Transcript.md
```

內容包含：

- 影片名稱
    
- 影片網址
    
- 完整逐字稿
    

Prompt 不直接接收 YouTube 網址或音訊檔。

---

# 6. Output Specification

Prompt 必須輸出：

```text
Study_Note.md
```

固定結構如下：

```markdown
# 影片名稱

影片網址

---

## 一句話摘要

---

## 重點摘要

---

## 重點解析

---

## 操作流程

---

## 延伸資訊
```

不得新增、刪除或調整章節順序。

---

# 7. Output Quality Requirements

## 一句話摘要

- 一段文字
    
- 約 50～100 字
    
- 說明影片核心內容
    

---

## 重點摘要

- 5～8 點
    
- 每點聚焦一個重點
    
- 避免冗長描述
    

---

## 重點解析

要求：

- 依主題整理
    
- 保留重要觀念
    
- 補充必要說明
    
- 不直接複製逐字稿
    

建議篇幅：

約為逐字稿的 15%～25%。

---

## 操作流程

若影片包含流程：

使用：

```text
Step 1
↓

Step 2
↓

Step 3
```

若影片無操作流程：

請明確標示：

> 本影片無明確操作流程。

---

## 延伸資訊

包含：

### Keywords

- 5～10 個
    

### Tags

- 3～8 個
    

### Further Research

- 3～5 個延伸研究方向
    

---

# 8. Prompt Rules

Prompt 必須遵守：

- 使用 Markdown 格式
    
- 使用台灣繁體中文
    
- 不輸出 YAML
    
- 不輸出 JSON
    
- 不輸出 XML
    
- 不加入 AI 自我說明
    
- 不加入推理過程
    
- 不加入模型資訊
    
- 不輸出無關內容
    
- 不重複逐字稿
    

---

# 9. Quality Guidelines

Prompt 應優先：

- 保留重要知識
    
- 保留工具名稱
    
- 保留 Workflow
    
- 保留最佳實務
    
- 保留重要名詞
    

應忽略：

- 開場白
    
- 結尾致謝
    
- 訂閱提醒
    
- 贊助內容
    
- 重複內容
    
- 與主題無關的閒聊
    

---

# 10. Version Management

Prompt 採版本管理。

命名方式：

```text
StudyNote_Prompt_v1.0
StudyNote_Prompt_v1.1
StudyNote_Prompt_v2.0
```

原則：

- Major：輸出格式變更
    
- Minor：品質改善
    
- Patch：文字修正
    

---

# 11. Prompt Acceptance Criteria

Prompt 視為驗證成功需符合：

- 成功讀取 Transcript.md
    
- 成功產生 Study_Note.md
    
- 結構完全符合 Template
    
- 無 Markdown 格式錯誤
    
- 重點整理正確
    
- 無大量重複逐字稿
    
- 可直接保存於 Obsidian
    

---

# 12. Future Prompt Roadmap

MVP v0.1：

- StudyNote_Prompt_v1.0
    

v0.2：

- KnowledgeCard_Prompt_v1.0
    
- SOP_Prompt_v1.0
    

v0.3：

- PromptLibrary_Prompt_v1.0
    
- Skills_Prompt_v1.0
    

v1.0：

- AgentBuilder_Prompt
    
- CourseBuilder_Prompt
    
- AIProductBuilder_Prompt
    

---

# 13. Development Principles

所有 Prompt 開發遵循：

```text
Workflow
        ↓
Template
        ↓
Prompt
        ↓
Model
        ↓
Output
```

Prompt 必須遵守 Workflow 與 Template，不因模型不同而改變輸出格式。

---

## Document Status

| 項目       | 內容                            |
| -------- | ----------------------------- |
| Document | Prompt Specification          |
| Version  | v1.0 (Final)                  |
| Product  | YB Knowledge Factory MVP v0.1 |
| Status   | ✅ Final                       |