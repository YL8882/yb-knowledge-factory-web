---
title: Prompt_06_Testing
version: v1.0
status: Final
owner: YB
document_type: Google AI Studio Prompt
product: YB Knowledge Factory MVP v0.1
module: Testing
last_updated: 2026-07-27
---

# Prompt 06｜Testing

## Purpose

完成 YB Knowledge Factory MVP v0.1 最終驗收。

本 Prompt 不新增任何功能。

僅驗證目前所有功能是否能正常運作。

---

# Current Status

目前已完成：

- Home UI
- Video Import
- Transcript
- Study Note
- Export

請不要新增任何功能。

請不要修改 UI。

請不要修改 Layout。

請不要修改 Color。

請不要修改 Typography。

---

# Testing Scope

驗證以下流程：

YouTube URL

↓

Video Import

↓

Transcript

↓

Study Note

↓

Export

全部可以正常運作。

---

# End-to-End Workflow

請依照以下流程測試：

Step 1

輸入：

合法 YouTube 網址。

確認：

- 成功驗證網址
- 自動取得影片名稱

---

Step 2

按下：

【取得逐字稿】

確認：

- Loading 正常
- 成功取得逐字稿
- 顯示於 Transcript 區

---

Step 3

按下：

【產生學習筆記】

確認：

- Loading 正常
- AI 成功產生 Study Note
- Markdown 格式正常
- 顯示於 Study Note 區

---

Step 4

按下：

【下載逐字稿】

確認：

成功下載：

Transcript.md

內容包含：

- 影片名稱
- YouTube URL
- Transcript

---

Step 5

按下：

【下載學習筆記】

確認：

成功下載：

Study_Note.md

內容包含：

- 影片名稱
- YouTube URL
- Study Note

---

# Error Testing

請驗證：

---

## Invalid URL

輸入：

非 YouTube 網址。

應顯示：

> 請輸入有效的 YouTube 影片網址。

---

## Video Not Found

不存在影片。

應顯示：

> 找不到影片。

---

## Transcript Error

逐字稿服務失敗。

應顯示：

> 無法取得逐字稿。

---

## Study Note Error

AI 回應失敗。

應顯示：

> 無法產生學習筆記。

---

## Download Error

沒有資料時下載。

應顯示：

> 尚未產生資料。

---

# UI Verification

確認：

- Logo 正確
- 品牌名稱正確
- 配色正確
- 字型一致
- Responsive 正常
- Layout 沒有改變
- 所有按鈕位置一致

---

# Performance Testing

確認：

- URL 驗證正常
- Loading 可正常顯示
- 長篇 Transcript 可 Scroll
- 長篇 Study Note 可 Scroll

---

# Acceptance Checklist

## Home UI

- [ ] 品牌名稱正確
- [ ] Logo 正確
- [ ] Layout 正常

---

## Video Import

- [ ] 驗證網址
- [ ] 成功取得影片名稱

---

## Transcript

- [ ] Loading 正常
- [ ] Transcript 正常

---

## Study Note

- [ ] Loading 正常
- [ ] Markdown 正常
- [ ] Study Note 正常

---

## Export

- [ ] Transcript.md 可下載
- [ ] Study_Note.md 可下載

---

## UI

- [ ] 沒有新增元件
- [ ] 沒有改變 UI
- [ ] Responsive 正常

---

# Definition of Done

MVP 視為完成需符合以下條件：

- 所有核心功能皆可正常執行。
- 使用者可依序完成完整操作流程。
- 所有錯誤訊息皆可正常顯示。
- UI 維持設計稿一致。
- 可成功下載 Transcript.md。
- 可成功下載 Study_Note.md。
- 無重大功能錯誤（Critical Error）。

---

# Google AI Studio Prompt

## Task

請測試目前 App。

不要新增任何功能。

不要修改任何 UI。

不要重新設計畫面。

請完整驗證：

1.

Video Import

2.

Transcript

3.

Study Note

4.

Markdown Download

請依照完整 Workflow 測試。

若有問題：

請直接修正 Bug。

不要新增功能。

不要改變畫面。

完成後請再次測試直到所有功能皆正常。

---

# Output

完成後請確認：

✅ Video Import

✅ Transcript

✅ Study Note

✅ Transcript.md Download

✅ Study_Note.md Download

全部正常。

---

# MVP Completion

當本文件所有 Acceptance Checklist 均通過後，

YB Knowledge Factory MVP v0.1 即可視為完成第一版（MVP Release）。

---

# Next Phase

完成 MVP 後，建議進入：

## Version 0.2

新增功能：

- History（歷史紀錄）
- Settings（設定）
- Prompt Templates（Prompt 模板）
- Runtime Folder（本機檔案管理）

完成驗證後，再規劃 Version 1.0：

- 多來源匯入（PDF、網頁、Podcast）
- Obsidian 自動同步
- Knowledge Card 自動生成
- SOP 自動生成
- Prompt Library 自動生成
- AI Agent Workflow