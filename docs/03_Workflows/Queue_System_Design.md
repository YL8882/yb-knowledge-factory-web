---
title: Queue_System_Design
version: v1.0
status: Final
owner: YB
document_type: System Design
product: YB Knowledge Factory MVP v0.1
module: Learning Queue
last_updated: 2026-07-27
---

# Queue System Design

## Purpose

Learning Queue 是 YB Knowledge Factory 的核心。

所有影片在正式成為知識資產之前，都必須先進入 Queue。

Queue 的目的不是永久儲存影片，而是管理整個知識建立流程。

產品理念：

> Capture Once.
>
> Process When Ready.

---

# Design Goals

Queue 必須：

- 快速加入影片
- 容易查看待處理項目
- 清楚顯示目前處理狀態
- 不需要立即等待 AI
- 完成後可快速清空 Queue

---

# System Overview

```
Browser Extension

        │

        ▼

Learning Queue

        │

───────────────

Transcript

        │

───────────────

Study Note

        │

───────────────

Knowledge Assets

        │

───────────────

Queue Complete
```

Queue 是整個系統唯一入口。

---

# Queue Data Model

每筆 Queue Item 包含：

```
Queue ID

Video Title

Video URL

Source

Created Time

Transcript Status

Study Note Status

Overall Status
```

---

# Queue Status

每筆影片具有以下生命週期：

```
Queued

↓

Transcript Pending

↓

Transcribing

↓

Transcript Ready

↓

Study Note Pending

↓

Generating

↓

Study Note Ready

↓

Completed

↓

Archived（Optional）
```

---

# Status Definition

## Queued

剛加入 Queue。

尚未開始任何工作。

圖示：

○

---

## Transcribing

背景開始下載音訊。

正在 Speech To Text。

圖示：

⏳

---

## Transcript Ready

逐字稿完成。

檔案：

```
影片名稱.md
```

已建立。

圖示：

✔

---

## Generating

AI 正在整理 Study Note。

圖示：

⏳

---

## Study Note Ready

Study Note 完成。

檔案：

```
SN_影片名稱.md
```

已建立。

圖示：

✔

---

## Completed

整個流程完成。

可選擇：

保留

或

刪除 Queue。

---

# Queue UI

首頁主要畫面：

```
Learning Queue

────────────────────

Architecture of Production LLM Apps

加入：

今天

Transcript

○ 未完成

Study Note

○ 未完成

Delete

────────────────────

Agent Skill

……

────────────────────
```

---

# Queue Card

每張 Card 包含：

```
影片名稱

影片網址

加入時間

────────────

Transcript

Status

Button

────────────

Study Note

Status

Button

────────────

Delete
```

---

# Queue Capacity

MVP：

最多：

100 筆。

若超過：

提示：

```
Queue 已滿。

請先完成或刪除部分項目。
```

---

# Queue Sorting

預設：

Newest First。

可切換：

- 最新加入
- 最舊加入
- 尚未轉錄
- 尚未摘要
- 已完成

---

# Duplicate Detection

若：

Video URL 相同。

不得重複建立 Queue。

提示：

```
此影片已存在 Queue。
```

---

# Processing Flow

```
Capture

↓

Queue

↓

Transcript

↓

Study Note

↓

Completed
```

所有 AI 工作皆背景執行。

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

Queue 不保存正式知識。

正式知識保存於：

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

保持一致。

---

# Queue Synchronization

所有 Queue 儲存於 Cloud。

登入帳號後：

任何裝置皆可看到：

相同 Queue。

不需要手動同步。

---

# Delete Policy

刪除 Queue：

只刪除：

Queue Item。

不刪除：

- Transcript
- Study Note

避免知識遺失。

---

# Retry Policy

若：

Transcript 失敗。

可：

Retry。

若：

Study Note 失敗。

亦可 Retry。

不需要重新加入 Queue。

---

# Batch Processing

Future Version：

可一次：

```
全部轉錄
```

或：

```
全部摘要
```

---

# Search

Future：

支援：

- Keyword
- Video Title
- URL

---

# Filter

Future：

支援：

```
Queued

Transcript Ready

Study Note Ready

Completed
```

---

# Dashboard Summary

首頁頂端：

```
Today

Queued

12

────────────

Transcript Ready

8

────────────

Study Note Ready

5

────────────

Completed

21
```

快速了解今日進度。

---

# System Rules

Rule 1

一個 URL

只能存在一筆 Queue。

---

Rule 2

Study Note 必須依賴 Transcript。

不可跳過。

---

Rule 3

Queue 完成後：

可刪除。

Markdown 保留。

---

Rule 4

任何 AI 工作皆不可阻塞 Queue。

---

Rule 5

Queue 永遠是暫存區。

不是知識庫。

---

# Success Metrics

Queue 成功代表：

- 收藏速度 < 3 秒
- Queue 可保存 100 筆
- 狀態更新正確
- Transcript 可成功建立
- Study Note 可成功建立
- Queue 可安全刪除
- Markdown 永久保留

---

# Architecture Summary

Learning Queue 是整個 YB Knowledge Factory 的工作中心。

它負責管理每一支影片從收藏、轉錄、摘要到完成的生命週期。

Queue 並不是知識庫，而是知識工廠的生產排程。

所有正式知識（Transcript、Study Note）完成後，都會獨立保存為 Markdown 檔案，而 Queue 則可清空，讓使用者持續維持乾淨、易管理的學習工作清單。