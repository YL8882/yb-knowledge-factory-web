---
title: Quick_Capture_Architecture
version: v1.0
status: Final
owner: YB
document_type: Architecture
product: YB Knowledge Factory MVP v0.1
module: Quick Capture
last_updated: 2026-07-27
---

# Quick Capture Architecture

## Purpose

Quick Capture 是 YB Knowledge Factory 的核心能力。

其目標不是立即完成 AI 分析，而是讓使用者能以最短時間收藏值得學習的 YouTube 影片，之後再由系統於背景完成轉錄、摘要與知識整理。

產品理念：

> Capture First. Process Later.

先收藏，再整理。

---

# Product Vision

使用者最大的痛點並不是無法取得逐字稿，而是：

- 看到值得學習的影片時沒有時間整理。
- 通勤、開會、工作中無法立即閱讀。
- 容易忘記影片。
- 收藏影片後很少再回去觀看。

Quick Capture 的目標，就是讓整個收藏流程縮短至 1~3 秒。

---

# Core Concept

Quick Capture 將整個學習流程拆成五個階段：

```
Capture

↓

Queue

↓

Transcript

↓

Study Note

↓

Archive
```

Capture 與 Process 完全分離。

使用者只需要完成 Capture。

其餘工作可於任何時間完成。

---

# Overall Architecture

```
                YouTube

                    │

                    ▼

        Browser Extension

                    │

                    ▼

          Quick Capture API

                    │

                    ▼

             Queue Database

                    │

      ┌─────────────┴─────────────┐

      ▼                           ▼

Transcript Worker         Study Note Worker

      │                           │

      ▼                           ▼

 Transcript.md            SN_影片名稱.md

      └─────────────┬─────────────┘

                    ▼

             User File Folder
```

---

# System Components

## 1. Browser Extension

負責：

- 取得目前影片網址
- 取得影片標題
- 傳送至 Cloud API

Extension 不執行：

- AI
- Whisper
- Gemini
- Download

只負責快速收藏。

---

## 2. Quick Capture API

接收：

```
Video Title

Video URL

Created Time

User ID
```

建立：

Queue Item。

---

## 3. Queue

Queue 是整個產品核心。

用途：

暫存尚未處理的影片。

建議限制：

100 筆。

每筆 Queue 包含：

```
影片名稱

影片網址

加入時間

Transcript Status

Study Note Status
```

---

## 4. Transcript Worker

負責：

下載影片音訊。

流程：

```
YouTube

↓

Audio

↓

Speech to Text

↓

Markdown
```

輸出：

```
影片名稱.md
```

---

## 5. Study Note Worker

讀取：

Transcript。

流程：

```
Transcript

↓

LLM

↓

Study Note
```

輸出：

```
SN_影片名稱.md
```

---

# User Workflow

## Step 1

使用者瀏覽 YouTube。

看到值得學習的影片。

---

## Step 2

點擊：

Browser Extension。

或：

右鍵：

```
Send to YB Learning Inbox
```

---

## Step 3

Extension 自動取得：

```
Title

URL
```

傳送至：

Quick Capture API。

---

## Step 4

Queue 新增：

一筆待處理影片。

狀態：

```
○ 已加入
```

---

## Step 5

使用者有空時：

開啟：

YB Knowledge Factory。

開始：

Transcript。

---

## Step 6

完成 Transcript。

狀態：

```
✔ 已轉錄
```

---

## Step 7

開始：

Study Note。

完成：

```
✔ 已摘要
```

---

## Step 8

完成全部流程。

可刪除 Queue。

Markdown 保留。

---

# Queue Status

每筆影片包含：

```
○ 已加入

↓

○ 轉錄中

↓

✔ 已轉錄

↓

○ 摘要中

↓

✔ 已摘要

↓

✔ 已完成
```

狀態以圖示呈現。

避免使用者閱讀大量文字。

---

# Folder Structure

```
YB_Knowledge_Factory/

    Queue/

        queue.json

    Transcript/

        影片名稱.md

    Study_Notes/

        SN_影片名稱.md
```

Queue 僅保存待處理項目。

正式知識資產儲存於：

Transcript

Study Notes

---

# File Naming

Transcript：

```
影片名稱.md
```

Study Note：

```
SN_影片名稱.md
```

保持所有知識檔案命名一致。

---

# Design Principles

Quick Capture 必須符合：

## Fast

收藏時間：

小於三秒。

---

## Lightweight

不需要等待 AI。

不需要等待下載。

---

## Asynchronous

所有 AI 工作皆背景執行。

避免阻塞使用者。

---

## Cross Device

登入後：

任何裝置皆可看到：

Queue。

---

## Knowledge First

產品目的不是影片收藏。

而是建立：

可持續累積的個人知識庫。

---

# MVP Scope

MVP v0.1

包含：

- Browser Extension
- Queue
- Video Title
- URL
- Queue List

不包含：

- AI
- Transcript
- Study Note

---

MVP v0.2

新增：

Transcript。

---

MVP v0.3

新增：

Study Note。

---

MVP v1.0

新增：

- Folder Export
- History
- Retry
- Batch Processing
- Queue Management

---

# Future Extensions

未來 Quick Capture 可支援：

- YouTube
- Podcast
- PDF
- 網頁文章
- Threads
- X（Twitter）
- Facebook
- Instagram
- TikTok

所有內容皆可透過相同 Queue 流程處理。

---

# Success Metrics

Quick Capture 成功的指標：

- 收藏時間 < 3 秒
- Queue 操作簡單直覺
- 使用者不需複製貼上網址
- 不需等待 AI 完成
- 任意裝置皆可繼續處理
- Markdown 檔案成功建立
- Queue 與知識檔案保持同步

---

# Architecture Summary

Quick Capture 並非轉錄工具。

它是整個 YB Knowledge Factory 的入口。

其核心價值為：

> 讓使用者在任何時間、任何裝置，以最短時間收藏值得學習的內容，再交由 AI 於背景完成知識整理，逐步建立可長期累積的個人知識庫。