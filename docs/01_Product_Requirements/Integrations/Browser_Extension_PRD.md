---
title: Browser_Extension_PRD
version: v1.0
status: Final
owner: YB
document_type: Product Requirements Document
product: YB Knowledge Factory MVP v0.1
module: Browser Extension
last_updated: 2026-07-27
---

# Browser Extension PRD

## Purpose

Browser Extension 是 YB Knowledge Factory 的第一個入口（Entry Point）。

它的目的不是下載影片，也不是執行 AI，而是讓使用者能在看到值得學習的 YouTube 影片時，以最快速度完成收藏。

產品理念：

> One Click Capture. Learn Later.

---

# Product Goal

讓使用者在 3 秒內完成一支 YouTube 影片的收藏。

收藏完成後：

- 自動加入 Queue
- 保留影片標題
- 保留影片網址
- 等待後續 Transcript 與 Study Note 處理

---

# Target Users

主要使用者：

- 通勤族
- AI 學習者
- YouTube 重度使用者
- 知識工作者
- 研究人員
- 課程製作者

---

# Supported Browsers

MVP：

- Google Chrome

Version 1.0：

- Microsoft Edge

Future：

- Firefox
- Safari

---

# User Story

## User Story 1

當我在 YouTube 看到值得學習的影片時，

我希望：

只按一下，

就能加入我的學習清單。

---

## User Story 2

當我回到家時，

我希望：

所有影片都已經存在 Queue，

等待我開始整理。

---

## User Story 3

我不希望：

每次都複製網址。

也不希望：

開啟 Web App 後再貼網址。

---

# Functional Requirements

## Feature 1

Quick Capture

點擊 Extension Icon：

```
Save to YB Learning Inbox
```

系統應：

自動取得：

- Video Title
- Video URL

並送至：

Quick Capture API。

---

## Feature 2

Right Click Menu

在 YouTube 頁面：

右鍵：

```
Send to YB Learning Inbox
```

功能與 Extension Icon 相同。

---

## Feature 3

Duplicate Detection

若影片已存在 Queue：

顯示：

> 此影片已存在。

不重複加入。

---

## Feature 4

Success Notification

成功加入：

Toast：

```
已加入 YB Learning Inbox
```

約 2 秒後自動消失。

---

## Feature 5

Offline Mode

若沒有網路：

先暫存於 Local Storage。

恢復網路後：

自動同步至 Cloud Queue。

---

# Data Capture

Extension 自動取得：

```
Video Title

Video URL

Capture Time

Browser

Source = YouTube
```

MVP 不取得：

- 字幕
- Thumbnail
- Channel
- Views
- Description

---

# API Specification

POST

```
/api/queue
```

Request：

```json
{
  "title": "Architecture of Production LLM Apps",
  "url": "https://youtube.com/...",
  "source": "youtube",
  "captured_at": "2026-07-27T08:30:00Z"
}
```

Response：

```json
{
  "success": true,
  "queue_id": "123456"
}
```

---

# UI Specification

Extension Popup：

```
YB Learning Inbox

────────────

Video

Architecture of Production LLM Apps

────────────

Save

────────────

Open Queue
```

保持極簡。

不要加入設定頁。

---

# Permissions

Manifest V3

需要：

- activeTab
- contextMenus
- storage

如需與網站通訊：

- host_permissions

僅允許：

```
https://www.youtube.com/*
```

以及：

```
https://your-domain.com/*
```

---

# Error Handling

影片不存在：

```
找不到影片資訊
```

API 失敗：

```
無法加入 Queue
```

重複影片：

```
影片已存在
```

離線：

```
已暫存，恢復連線後將自動同步
```

---

# Security Requirements

不得：

- 收集 Cookie
- 收集 Google 帳號資訊
- 收集瀏覽紀錄
- 收集觀看紀錄

僅取得：

- Video Title
- URL

---

# Performance Requirements

收藏速度：

< 3 秒

Extension Size：

< 2 MB

使用者操作：

最多一次點擊。

---

# Acceptance Criteria

完成後：

- [ ] Chrome 可正常安裝
- [ ] Extension Icon 可使用
- [ ] Right Click Menu 可使用
- [ ] 成功取得影片名稱
- [ ] 成功取得影片網址
- [ ] 成功加入 Queue
- [ ] 成功提示通知
- [ ] 重複影片不重複加入
- [ ] 離線可暫存
- [ ] 恢復連線可同步

---

# MVP Scope

包含：

- Chrome Extension
- Quick Capture
- Queue API
- 成功通知
- Duplicate Check

不包含：

- Transcript
- Study Note
- Download
- AI
- History

---

# Future Roadmap

Version 1.1

- Edge Extension
- Queue Counter
- 快速搜尋

Version 1.2

- Android Share
- iOS Share Sheet

Version 2.0

- PDF Capture
- Web Article Capture
- Podcast Capture
- Threads Capture
- X (Twitter) Capture
- TikTok Capture

---

# Success Metrics

Quick Capture 成功代表：

- 收藏一支影片 < 3 秒
- 不需要複製貼上網址
- 不需要先開啟網站
- 不需要等待 AI
- 收藏成功率 > 99%
- Queue 能正確同步至使用者帳號

---

# Product Summary

Browser Extension 是整個 YB Knowledge Factory 的入口。

它的唯一目標是：

> 讓使用者以最快速度收藏值得學習的內容。

AI、Transcript、Study Note 都屬於後續流程。

透過 Browser Extension，使用者可以在任何電腦安裝擴充功能、登入帳號後，即時建立自己的 Learning Inbox，讓知識收集與整理分離，大幅降低學習過程的摩擦成本。