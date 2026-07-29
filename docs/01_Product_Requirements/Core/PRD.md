# Product Requirements Document (PRD)

**Document Version:** PRD v1.0 (Final)  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# 1. Product Information

|項目|內容|
|---|---|
|Product Name|YB Knowledge Factory|
|Product Version|MVP v0.1|
|Document Version|PRD v1.0 (Final)|
|Product Type|AI Learning Assistant|
|Platform|Web Application|
|Target User|YB AI 重度學習者|
|Development Method|Google AI Studio → Claude Code|
|Development Principle|**Workflow First → Prompt First → MVP First → Code Last**|

---

# 2. Product Vision

YB Knowledge Factory 是一個專為 **YB AI 教學影片**打造的 AI 學習助手。

使用者只需貼上一個 YouTube 影片網址，即可自動完成：

- 下載影片音訊
    
- 轉換為台灣繁體中文逐字稿
    
- 產生高品質 Study Note
    
- 匯出 Markdown 文件
    

讓影片內容快速轉換為可閱讀、可搜尋、可永久保存的知識。

**MVP 的目標不是建立完整知識庫，而是打造一個每天都能使用的 AI 學習工具。**

---

# 3. Problem Statement

目前觀看 YB 教學影片時，存在以下痛點：

- 每部影片通常長達 20～60 分鐘。
    
- 需要反覆觀看才能整理完整筆記。
    
- 手動製作逐字稿耗費大量時間。
    
- 容易遺漏重要操作流程與實作細節。
    
- 學習成果難以累積與重複利用。
    

因此，需要一個能夠自動完成整理與摘要的 AI 工具。

---

# 4. Target User

本產品主要使用者包括：

- YB AI 教學影片重度學習者
    
- AI 工具研究者
    
- Vibe Coding 學習者
    
- 個人知識管理使用者
    

---

# 5. Product Goal

透過一次操作完成整個學習流程：

```text
YouTube URL
        ↓
下載影片音訊
        ↓
台灣繁體中文逐字稿
        ↓
Study Note
        ↓
Markdown 匯出
```

讓影片快速轉換為可閱讀、可保存、可複習的知識。

---

# 6. MVP Scope

## Input

使用者輸入：

- 一個 YouTube 影片網址
    

例如：

```
https://youtu.be/xxxxxxxx
```

---

## Output

系統產生兩份 Markdown 文件。

### 1. Transcript.md

內容包含：

- 影片名稱
    
- 影片網址
    
- 完整台灣繁體中文逐字稿
    

### 2. Study_Note.md

內容包含：

- 一句話摘要
    
- 重點摘要
    
- 重點解析
    
- 操作流程
    
- 延伸資訊
    

---

# 7. Functional Requirements

|編號|功能需求|
|---|---|
|FR-001|使用者貼上一個 YouTube 網址。|
|FR-002|系統自動下載影片音訊。|
|FR-003|系統自動轉換為台灣繁體中文逐字稿。|
|FR-004|系統依據逐字稿自動產生 Study Note。|
|FR-005|系統提供 Transcript.md 與 Study_Note.md 下載。|

---

# 8. Non-functional Requirements

系統需符合以下要求：

- 操作流程簡單
    
- 不需登入
    
- 不需資料庫
    
- 不需會員系統
    
- 不需安裝
    
- 固定 Markdown 格式輸出
    
- 支援長影片處理
    
- 低 Token 成本
    
- 穩定且一致的 AI 輸出
    

---

# 9. Out of Scope（MVP 不包含）

第一版不包含以下功能：

- Login
    
- Database
    
- 收藏功能
    
- Tag 管理
    
- Knowledge Card
    
- SOP 自動生成
    
- Prompt Library
    
- AI Agent
    
- RAG
    
- AI Chat
    
- Cloud Sync
    
- 多人協作
    

以上功能將於後續版本逐步加入。

---

# 10. Success Criteria

當使用者完成一次操作後：

成功取得：

- ✅ Transcript.md
    
- ✅ Study_Note.md
    

並且：

- 可直接閱讀
    
- 不需再次手動整理
    
- 可永久保存
    
- 可作為後續知識資產來源
    

即視為 MVP 成功。

---

# 11. Future Roadmap

## v0.2

新增：

- Knowledge Card
    
- SOP
    
- Prompt Library
    

## v0.3

支援更多內容來源：

- Podcast
    
- PDF
    
- 網頁文章
    

## v1.0

完整個人知識庫：

- RAG
    
- 全文搜尋
    
- AI Chat
    
- 知識管理
    
- 多來源整合
    

---

# 12. MVP Development Strategy

本產品採用以下開發策略：

```text
Workflow First
        ↓
Prompt First
        ↓
Google AI Studio Prototype
        ↓
MVP Validation
        ↓
Claude Code Implementation
        ↓
Web Application
```

先驗證核心 Workflow 與 Prompt 品質，再投入程式開發與產品化，降低開發成本與風險。

---

# 13. MVP Success Definition

YB Knowledge Factory MVP v0.1 完成的標準：

使用者只需貼上一個 YB YouTube 影片網址，即可在一次操作中，自動完成：

1. 下載影片音訊
    
2. 產生台灣繁體中文逐字稿（Transcript.md）
    
3. 產生高品質學習筆記（Study_Note.md）
    
4. 匯出兩份 Markdown 文件
    

整個流程無需手動整理內容，即可將影片轉換為可保存、可閱讀、可複習的知識資產。

---

## Document Status

|項目|內容|
|---|---|
|Document|Product Requirements Document|
|Version|PRD v1.0 (Final)|
|Product|YB Knowledge Factory MVP v0.1|
|Status|✅ Final|