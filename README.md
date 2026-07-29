---
Version: v1.1
Status: Active
Owner: YB
Document: README
Category: Project Entry
Purpose: Project Overview
Priority: Critical
Last Updated: 2026-07-29
---

# YB Knowledge Factory MVP

## 專案簡介

YB Knowledge Factory MVP 是一個 AI 學習工具。

使用者貼上 YouTube 網址後，系統自動完成：

YouTube URL
→ Queue
→ Transcript
→ Study Note
→ Markdown Output（可下載）

本專案以 **Web First、MVP First、Workflow First** 為核心開發原則。

---

## 目前功能（MVP v0.1）

- 首頁 UI：YouTube URL 輸入框、Generate 按鈕
- YouTube URL 驗證與影片資訊擷取（支援一般網址與 `/shorts/`）
- Learning Queue：加入、列表、移除、重複網址偵測
- Transcript：下載音訊並以 Faster Whisper 轉錄，存成 `outputs/transcripts/{影片名}_{VideoID}.md`
- Study Note：以 Gemini 2.5 Flash 依官方 Template 產生，存成 `outputs/study_notes/{影片名}_{VideoID}.md`
- 下載 Transcript.md 與 Study_Note.md

詳細驗收結果請見：`docs/MVP_Test_Report.md`

---

## 安裝與執行

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 2. 設定 Gemini API Key

複製 `.env.example` 為 `.env`，並填入你的 Gemini API Key：

```bash
cp .env.example .env
```

```text
GEMINI_API_KEY=你的實際金鑰
```

`.env` 已加入 `.gitignore`，不會被提交至版本控制。

### 3. 啟動伺服器

```bash
python run.py
```

### 4. 開啟瀏覽器

```text
http://localhost:8000
```

首次產生 Transcript 時，會自動從 Hugging Face 下載 Faster Whisper 模型（需網路連線），
之後會快取於本機，不需重複下載。

---

## 專案結構

```text
app/
    main.py            FastAPI 進入點與 API 路由
    youtube.py          YouTube URL 驗證與影片中繼資料
    queue_store.py       Learning Queue（記憶體內）
    transcript.py        音訊下載與 Whisper 轉錄
    study_note.py         Study Note 組裝與存檔
    gemini_client.py      Gemini API 呼叫與 Prompt
    templates/           首頁 HTML
    static/              CSS / JavaScript

docs/
    Product Specifications、Milestone、Test Report

outputs/
    transcripts/         產生的 Transcript.md（不納入版控）
    study_notes/          產生的 Study_Note.md（不納入版控）

CLAUDE.md
    Claude Code Entry Point
```

---

## 開發流程

本專案遵循：

1. CLAUDE.md
2. Development_Operating_System.md
3. PRD
4. Workflow
5. Milestone

依序閱讀後開始開發。

---

## 開發原則

- Specification First
- One Milestone at a Time
- MVP First
- Small Commits
- Token Economy