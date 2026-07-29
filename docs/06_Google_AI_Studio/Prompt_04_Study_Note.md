---
title: Prompt_04_Study_Note
version: v1.0
status: Final
owner: YB
document_type: Google AI Studio Prompt
product: YB Knowledge Factory MVP v0.1
module: Study Note
last_updated: 2026-07-27
---

# Prompt 04｜Study Note

## Purpose

實作 AI 學習筆記（Study Note）生成功能。

本 Prompt 僅負責：

- 將 Transcript 傳送至 AI
- 產生 Study Note
- 顯示 Study Note
- Loading 狀態
- Error Handling

不包含：

- Transcript
- Markdown Download
- History
- Login
- Database

---

# Current Status

目前已完成：

- Home UI
- Video Import
- Transcript

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

當使用者已成功取得 Transcript 後，

按下：

【產生學習筆記】

開始產生 AI Study Note。

---

# Functional Requirements

## Step 1

確認：

Transcript 已存在。

若沒有 Transcript：

顯示：

> 請先取得逐字稿。

停止流程。

---

## Step 2

將 Transcript 傳送至：

Gemini

（未來可切換其他 LLM）

目前請保持模型可替換。

不要綁定固定模型。

---

## Step 3

AI 應產生：

Study Note。

內容格式如下：

### 一句話摘要

簡要說明影片核心內容。

---

### 重點整理

使用條列方式整理重點。

---

### 詳細說明

依主題整理重要內容。

---

### 操作流程（Workflow）

整理影片中的操作步驟。

---

### 延伸學習

列出：

- 關鍵字
- 建議研究方向
- 延伸主題

---

## Step 4

完成後：

顯示於：

【學習筆記】

文字區。

保留：

- Markdown
- 換行
- 標題
- 清單格式

---

# Loading

開始產生 Study Note：

按鈕顯示：

> 正在產生學習筆記……

Study Note 區：

顯示 Loading。

完成後：

恢復正常。

---

# Error Handling

AI 失敗：

> 無法產生學習筆記。

API Timeout：

> AI 回應逾時，請稍後再試。

未知錯誤：

> 發生未知錯誤。

---

# UI Constraints

不要：

- 修改首頁
- 修改按鈕樣式
- 修改 Layout
- 修改 Color
- 修改 Typography
- 新增頁面

---

# Out of Scope

本 Prompt 不包含：

- Markdown Download
- History
- Login
- Database

---

# Acceptance Criteria

完成後：

- [ ] Transcript 存在才能執行
- [ ] Loading 正常
- [ ] AI 成功產生 Study Note
- [ ] Markdown 格式保留
- [ ] 支援長內容 Scroll
- [ ] Error Handling 正常
- [ ] UI 完全沒有改變

---

# Google AI Studio Prompt

## Task

請修改目前 App。

不要建立新的 App。

目前首頁 UI 已完成。

請保持目前所有 UI 完全不變。

本次只完成：

【產生學習筆記】

功能。

需求：

當使用者按下：

【產生學習筆記】

系統應：

1.

確認：

Transcript 已存在。

2.

將 Transcript 傳送至 AI。

3.

AI 產生：

Study Note。

4.

顯示：

Loading。

5.

完成後：

更新：

【學習筆記】

文字區。

Study Note 使用 Markdown 格式。

保留：

- 標題
- 條列
- 換行

若失敗：

顯示：

適當錯誤訊息。

請保持：

- UI
- Layout
- Color
- Button
- Typography

完全不變。

不要新增：

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

取得逐字稿

↓

點擊：

【產生學習筆記】

↓

Loading

↓

顯示 Study Note

---

# Next Prompt

Prompt_05_Export

目標：

下載：

- Transcript.md
- Study_Note.md

---

# Status

Ready for Prompt_05_Export