# Workflow Specification

**Document Version:** v1.0 (Final)  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# 1. Purpose

本文件定義 **YB Knowledge Factory MVP v0.1** 的完整工作流程（Workflow）。

Workflow 是整個產品的核心，所有 Prompt、程式開發與 AI Agent 均必須依照本文件執行。

本版本遵循：

> **Workflow First → Prompt First → MVP First → Code Last**

---

# 2. Workflow Overview

使用者只需貼上一個 YouTube 影片網址，即可自動完成影片分析，並輸出兩份 Markdown 文件。

```text
YouTube URL
      │
      ▼
取得影片資訊
      │
      ▼
下載影片音訊
      │
      ▼
語音辨識
      │
      ▼
台灣繁體中文轉換
      │
      ▼
產生 Transcript.md
      │
      ▼
AI 分析逐字稿
      │
      ▼
產生 Study_Note.md
      │
      ▼
下載兩份 Markdown
```

---

# 3. Workflow Steps

## Step 1：輸入 YouTube 網址

### Input

使用者貼上一個 YouTube 網址。

例如：

```
https://www.youtube.com/watch?v=XXXXXXXX
```

### Output

取得影片網址。

---

## Step 2：取得影片資訊

系統自動取得：

- 影片名稱
    
- 頻道名稱
    
- Video ID
    
- 影片長度
    

主要用途：

- 作為 Transcript 標題
    
- 檔案命名
    
- 顯示於介面
    

---

## Step 3：下載影片音訊

使用：

- yt-dlp
    

目的：

下載影片音訊供 Whisper 使用。

Output：

```
audio.mp3
```

---

## Step 4：語音辨識

使用：

- Faster Whisper
    

功能：

將音訊轉換為逐字稿。

Output：

```
transcript.txt
```

---

## Step 5：繁體中文轉換

使用：

- OpenCC（s2t）
    

目的：

統一轉換為台灣繁體中文。

Output：

```
Traditional Chinese Transcript
```

---

## Step 6：建立 Transcript.md

依照 Transcript Template 建立：

```
Transcript.md
```

內容：

- 影片名稱
    
- 影片網址
    
- 完整逐字稿
    

完成第一份輸出文件。

---

## Step 7：AI 分析逐字稿

輸入：

```
Transcript.md
```

使用：

- Gemini 2.5 Flash
    

搭配：

```
StudyNote_Prompt_v1.0
```

AI 負責：

- 理解影片內容
    
- 萃取重點
    
- 建立學習筆記
    

---

## Step 8：建立 Study_Note.md

依照 Study Note Template 產生：

```
Study_Note.md
```

內容包括：

- 一句話摘要
    
- 重點摘要
    
- 重點解析
    
- 操作流程
    
- 延伸資訊
    

完成第二份輸出文件。

---

## Step 9：下載 Markdown

提供下載：

- Transcript.md
    
- Study_Note.md
    

Workflow 完成。

---

# 4. Input

使用者輸入：

|項目|說明|
|---|---|
|YouTube URL|一個影片網址|

---

# 5. Output

系統輸出：

## Transcript.md

包含：

- 影片名稱
    
- 影片網址
    
- 完整台灣繁體中文逐字稿
    

---

## Study_Note.md

包含：

- 一句話摘要
    
- 重點摘要
    
- 重點解析
    
- 操作流程
    
- 延伸資訊
    

---

# 6. File Flow

```
YouTube URL
      │
      ▼
audio.mp3
      │
      ▼
transcript.txt
      │
      ▼
Transcript.md
      │
      ▼
Study_Note.md
```

---

# 7. Exception Handling

若流程發生錯誤：

## 無法取得影片

顯示：

> 無法讀取 YouTube 影片資訊。

---

## 無法下載影片

顯示：

> 無法下載影片音訊。

---

## Whisper 失敗

顯示：

> 無法完成逐字稿轉換。

---

## AI 分析失敗

顯示：

> 無法產生 Study Note。

---

# 8. MVP Scope

本 Workflow 僅包含：

- YouTube
    
- Transcript
    
- Study Note
    

不包含：

- Knowledge Card
    
- SOP
    
- Prompt Library
    
- AI Agent
    
- Database
    
- RAG
    
- AI Chat
    

---

# 9. Future Workflow

未來版本：

```
YouTube URL
      │
      ▼
Transcript
      │
      ▼
Study Note
      │
      ├── Knowledge Card
      ├── SOP
      ├── Prompt Library
      ├── Skills
      ├── AI Agent
      ├── AI Product
      └── Course
```

MVP 不實作上述流程。

---

# 10. Workflow Principles

所有開發必須遵守：

1. Workflow 優先。
    
2. Prompt 優先於程式。
    
3. 每一步皆可獨立測試。
    
4. 每一步皆有明確 Input 與 Output。
    
5. 保持流程簡單、可維護、可擴充。
    

---

# 11. Acceptance Criteria

Workflow 視為完成需符合：

- 成功取得 YouTube 影片資訊。
    
- 成功下載影片音訊。
    
- 成功產生台灣繁體中文逐字稿。
    
- 成功建立 Transcript.md。
    
- 成功建立 Study_Note.md。
    
- 使用者可下載兩份 Markdown 文件。
    
- 全流程一次完成，無需人工介入。
    

---

## Document Status

| 項目       | 內容                            |
| -------- | ----------------------------- |
| Document | Workflow Specification        |
| Version  | v1.0 (Final)                  |
| Product  | YB Knowledge Factory MVP v0.1 |
| Status   | ✅ Final                       |