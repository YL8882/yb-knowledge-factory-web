# Technical Decision

**Document Version:** v1.0 (Final)  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# 1. Purpose

本文件記錄 **YB Knowledge Factory MVP v0.1** 的技術選型與設計決策。

所有技術皆以 **MVP 快速驗證** 為核心原則，優先考量：

- 開發速度
    
- 穩定性
    
- Token 成本
    
- 維護成本
    
- 後續擴充性
    

避免過度設計（Over Engineering）。

---

# 2. Development Principles

本產品遵循以下開發原則：

```text
Workflow First
        ↓
Prompt First
        ↓
MVP First
        ↓
Code Last
```

先驗證 Workflow，再驗證 Prompt，最後才投入程式開發。

---

# 3. Technical Decision Summary

|項目|決策|
|---|---|
|Product Type|Web Application|
|Development Platform|Google AI Studio|
|Programming Language|Python|
|Backend Framework|FastAPI|
|AI Model|Gemini 2.5 Flash|
|Video Download|yt-dlp|
|Speech-to-Text|Faster Whisper|
|Chinese Conversion|OpenCC（s2t）|
|Output Format|Markdown|
|Database|不使用（MVP）|
|Storage|Local Files|
|Authentication|不使用|
|Deployment|Windows Localhost|

---

# 4. Technology Stack

## Frontend

**Google AI Studio**

用途：

- 建立 MVP Prototype
    
- 驗證 Prompt
    
- 驗證 Workflow
    
- 快速測試 UI
    

未來版本：

- Next.js
    

---

## Backend

**Python + FastAPI**

用途：

- API Server
    
- Workflow 控制
    
- 呼叫 AI Model
    
- Markdown 產生
    

選擇原因：

- AI 生態成熟
    
- 套件完整
    
- 易於維護
    

---

## AI Model

**Gemini 2.5 Flash**

用途：

- Study Note 生成
    
- 重點整理
    
- Workflow 分析
    

選擇原因：

- 成本低
    
- 速度快
    
- 長 Context
    
- 適合大量影片分析
    

---

## Video Download

**yt-dlp**

用途：

- 下載 YouTube 音訊
    

選擇原因：

- 穩定
    
- 開源
    
- 社群維護完善
    

---

## Speech-to-Text

**Faster Whisper**

用途：

- 音訊轉逐字稿
    

選擇原因：

- 本地執行
    
- 品質穩定
    
- 成本低
    
- 支援長影片
    

---

## Traditional Chinese Conversion

**OpenCC（s2t）**

用途：

- 將逐字稿統一轉為台灣繁體中文
    

---

## Output

Markdown (.md)

輸出：

- Transcript.md
    
- Study_Note.md
    

選擇原因：

- AI 容易處理
    
- Git 友善
    
- Obsidian 相容
    
- 可長期保存
    

---

# 5. Database Decision

MVP v0.1

**不使用 Database。**

原因：

- 僅需輸出 Markdown
    
- 無會員需求
    
- 無搜尋需求
    
- 降低複雜度
    

未來版本再導入 PostgreSQL + pgvector。

---

# 6. Deployment Decision

MVP：

Windows Localhost

原因：

- 開發最快
    
- 容易 Debug
    
- 不需雲端成本
    

未來部署：

- Zeabur
    
- Railway
    
- Render
    

---

# 7. Architecture Overview

```text
Browser
        │
        ▼
Google AI Studio
        │
        ▼
Python + FastAPI
        │
 ├── yt-dlp
 ├── Faster Whisper
 ├── OpenCC
 ├── Gemini 2.5 Flash
 └── Markdown Export
        │
        ▼
Output
 ├── Transcript.md
 └── Study_Note.md
```

---

# 8. MVP Constraints

第一版不包含：

- Login
    
- Database
    
- Cloud Storage
    
- RAG
    
- AI Chat
    
- Knowledge Card
    
- SOP
    
- Prompt Library
    
- Agent
    
- Docker
    
- n8n
    

優先完成可使用的 MVP。

---

# 9. Future Technical Roadmap

## v0.2

- Knowledge Card Generator
    
- SOP Generator
    
- Prompt Library
    

## v0.3

- PostgreSQL
    
- pgvector
    
- 全文搜尋
    

## v1.0

- RAG
    
- AI Chat
    
- 多來源知識整合
    
- SaaS 架構
    

---

# 10. Final Decision

本產品正式採用以下技術：

- Google AI Studio（Prototype）
    
- Python
    
- FastAPI
    
- Gemini 2.5 Flash
    
- yt-dlp
    
- Faster Whisper
    
- OpenCC
    
- Markdown
    

並遵循：

> **Workflow First → Prompt First → MVP First → Code Last**

作為 YB Knowledge Factory MVP v0.1 的唯一開發原則。

---

## Document Status

| 項目       | 內容                            |
| -------- | ----------------------------- |
| Document | Technical Decision            |
| Version  | v1.0 (Final)                  |
| Product  | YB Knowledge Factory MVP v0.1 |
| Status   | ✅ Final                       |