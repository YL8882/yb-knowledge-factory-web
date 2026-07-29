---
title: Prompt_03_Transcript
version: v1.0
status: Final
owner: YB
document_type: Google AI Studio Prompt
product: YB Knowledge Factory MVP v0.1
module: Transcript
last_updated: 2026-07-27
---

# Prompt 03｜Transcript

## Purpose

實作 YouTube 影片逐字稿（Transcript）功能。

本 Prompt 僅負責：

- 呼叫逐字稿服務
- 顯示逐字稿
- 錯誤處理
- Loading 狀態

不包含：

- Study Note
- Markdown Download
- History
- Login
- Database

---

# Current Status

目前已完成：

- Home UI
- Video Import（影片匯入）

首頁 UI 已凍結（UI Freeze）。

請保持目前所有 UI 完全不變。

不要修改：

- 品牌
- Logo
- 色彩
- 字型
- 間距
- 元件大小
- Layout
- Responsive

---

# Objective

當使用者已成功取得影片資訊後，

按下：

【取得逐字稿】

開始產生影片逐字稿。

---

# Functional Requirements

## Step 1

確認：

影片名稱已存在。

若沒有影片資訊：

顯示：

> 請先輸入有效的 YouTube 影片網址。

停止流程。

---

## Step 2

使用：

YouTube URL

開始取得逐字稿。

逐字稿來源可使用：

- 自建 Transcript API
- Whisper
- Gemini
- 其他 Transcript Service

目前請保留可替換的架構。

不要綁定特定服務。

---

## Step 3

取得成功後：

將逐字稿內容顯示於：

【逐字稿】

文字區。

支援：

- 長篇內容
- Scroll
- 保留段落
- 保留換行

---

# Loading

開始取得逐字稿時：

按鈕顯示：

> 正在產生逐字稿……

逐字稿區：

顯示 Loading。

完成後：

恢復正常。

---

# Error Handling

若取得失敗：

顯示：

> 無法取得逐字稿。

若影片沒有字幕：

顯示：

> 此影片沒有可用字幕。

若網路錯誤：

顯示：

> 網路連線失敗，請稍後再試。

---

# UI Constraints

不要：

- 修改首頁
- 修改按鈕樣式
- 修改顏色
- 修改 Layout
- 修改字型
- 新增頁面
- 新增 Dashboard

---

# Out of Scope

本 Prompt 不包含：

- Study Note
- Gemini
- Markdown Download
- History
- Login
- Database

---

# Acceptance Criteria

完成後：

- [ ] 點擊「取得逐字稿」可開始執行
- [ ] 顯示 Loading 狀態
- [ ] 成功顯示逐字稿
- [ ] 保留換行與段落
- [ ] 支援長篇內容捲動
- [ ] 錯誤訊息正常
- [ ] UI 完全沒有改變

---

# Google AI Studio Prompt

## Task

請修改目前 App。

不要建立新的 App。

目前首頁 UI 已完成。

請保持目前所有 UI 完全不變。

本次只完成：

【取得逐字稿】

功能。

需求：

當使用者按下：

【取得逐字稿】

系統應：

1.

確認影片資訊已存在。

2.

開始取得逐字稿。

3.

顯示：

Loading。

4.

完成後：

將逐字稿顯示於：

【逐字稿】

文字區。

5.

若失敗：

顯示適當錯誤訊息。

請保持：

- UI
- Layout
- Color
- Button
- Typography

完全不變。

不要新增：

- Study Note
- Download
- Dashboard
- History
- Login

完成後請直接更新目前 App。

---

# Output

使用者流程：

貼上 YouTube 網址

↓

取得影片資訊

↓

點擊：

【取得逐字稿】

↓

Loading

↓

顯示逐字稿

---

# Next Prompt

Prompt_04_Study_Note

目標：

使用 Transcript

產生：

Study Note。

---

# Status

Ready for Prompt_04_Study_Note