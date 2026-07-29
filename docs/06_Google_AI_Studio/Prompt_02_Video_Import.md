---
title: Prompt_02_Video_Import
version: v1.0
status: Final
owner: YB
document_type: Google AI Studio Prompt
product: YB Knowledge Factory MVP v0.1
module: Video Import
last_updated: 2026-07-27
---

# Prompt 02｜Video Import

## Purpose

實作 YouTube 影片匯入功能。

本 Prompt 僅負責：

- 驗證 YouTube 網址
- 自動取得影片資訊
- 更新影片名稱

不包含：

- 逐字稿
- 學習筆記
- Markdown 匯出

---

# Current Status

目前首頁 UI 已完成。

請保持目前所有 UI 完全不變。

不要修改：

- 品牌
- Logo
- 配色
- 字型
- 間距
- 元件大小
- Layout
- Responsive

---

# Objective

當使用者貼上：

YouTube 影片網址

系統應自動：

1. 驗證網址格式
2. 取得影片資訊
3. 更新影片名稱

不需要使用者按任何按鈕。

---

# Functional Requirements

## Step 1

使用者貼上：

YouTube 影片網址

例如：

https://www.youtube.com/watch?v=xxxxxxxxxxx

---

## Step 2

系統驗證：

是否為合法的 YouTube 網址。

若不是：

影片名稱區顯示：

> 請輸入有效的 YouTube 影片網址

停止後續流程。

---

## Step 3

若網址格式正確：

開始取得影片資訊。

目前只需要取得：

- Video Title

不要取得：

- Thumbnail
- Channel
- Description
- Views
- Publish Date
- Duration

---

## Step 4

取得成功：

更新：

影片名稱（自動顯示）

區塊。

---

# Loading

取得影片資訊時：

影片名稱區顯示：

> 正在取得影片資訊……

完成後：

顯示真正影片名稱。

---

# Error Handling

找不到影片：

> 找不到影片

網路錯誤：

> 無法取得影片資訊，請稍後再試

---

# UI Constraints

不要：

- 修改 UI
- 修改配色
- 修改版面
- 修改按鈕
- 新增元件
- 新增頁面

---

# Out of Scope

本 Prompt 不包含：

- Transcript
- Gemini
- Study Note
- Download Markdown
- History
- Login
- Database

---

# Acceptance Criteria

完成後：

- [ ] 能驗證 YouTube 網址
- [ ] 自動取得影片名稱
- [ ] 更新影片名稱區塊
- [ ] Loading 正常
- [ ] Error Message 正常
- [ ] UI 完全沒有改變

---

# Google AI Studio Prompt

## Task

請修改目前的 App。

不要建立新的 App。

目前首頁 UI 已完成。

請保持目前所有 UI 完全不變。

本次只完成：

YouTube Video Import。

功能需求：

當使用者貼上：

YouTube 影片網址

系統應：

1.

驗證網址格式。

2.

若合法：

自動取得影片名稱。

3.

更新：

影片名稱（自動顯示）

區塊。

若網址錯誤：

顯示：

> 請輸入有效的 YouTube 影片網址

若找不到影片：

顯示：

> 找不到影片

若網路失敗：

顯示：

> 無法取得影片資訊，請稍後再試

目前不要：

- 修改 UI
- 新增按鈕
- 建立 Transcript
- 呼叫 Gemini
- 建立 Study Note
- 下載 Markdown

完成後請直接更新目前 App。

---

# Output

完成後：

使用者流程：

貼上網址

↓

自動驗證

↓

自動取得影片名稱

↓

更新首頁

Status：

Ready for Prompt_03_Transcript