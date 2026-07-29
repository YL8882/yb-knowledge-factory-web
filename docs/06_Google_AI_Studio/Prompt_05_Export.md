---
title: Prompt_05_Export
version: v1.0
status: Final
owner: YB
document_type: Google AI Studio Prompt
product: YB Knowledge Factory MVP v0.1
module: Export
last_updated: 2026-07-27
---

# Prompt 05｜Export

## Purpose

實作 Markdown 匯出（Export）功能。

本 Prompt 僅負責：

- 匯出 Transcript
- 匯出 Study Note
- Markdown 檔案下載
- 檔案命名

不包含：

- Transcript 產生
- Study Note 產生
- History
- Login
- Database

---

# Current Status

目前已完成：

- Home UI
- Video Import
- Transcript
- Study Note

首頁 UI 已凍結（UI Freeze）。

請保持目前所有 UI 完全不變。

不要修改：

- 品牌
- Logo
- 色彩
- 字型
- Layout
- 元件大小
- 按鈕樣式
- Responsive

---

# Objective

當使用者完成：

- Transcript
- Study Note

後，

可以下載：

1.

Transcript.md

2.

Study_Note.md

---

# Functional Requirements

## Download Transcript

當使用者按下：

【下載逐字稿】

系統應：

下載：

Transcript.md

內容：

- 影片標題
- YouTube URL
- Transcript

Markdown 格式。

---

## Download Study Note

當使用者按下：

【下載學習筆記】

系統應：

下載：

Study_Note.md

內容：

- 影片標題
- YouTube URL
- AI Study Note

Markdown 格式。

---

# File Naming

Transcript：

```
Transcript.md
```

Study Note：

```
Study_Note.md
```

未來版本：

可支援：

```
{Video_Title}.md

{Video_Title}_Transcript.md

{Video_Title}_Study_Note.md
```

目前 MVP：

保持：

Transcript.md

Study_Note.md

---

# Markdown Format

## Transcript

```markdown
# 影片標題

影片網址：

https://......

---

# Transcript

......
```

---

## Study Note

```markdown
# 影片標題

影片網址：

https://......

---

# Summary

......

---

# Key Points

......

---

# Workflow

......

---

# Further Learning

......
```

---

# Error Handling

若沒有 Transcript：

顯示：

> 尚未產生逐字稿。

若沒有 Study Note：

顯示：

> 尚未產生學習筆記。

若下載失敗：

顯示：

> 檔案下載失敗，請稍後再試。

---

# UI Constraints

不要：

- 修改首頁
- 修改按鈕樣式
- 修改版面
- 修改 Layout
- 修改 Color
- 修改 Typography

---

# Out of Scope

本 Prompt 不包含：

- Login
- History
- Database
- Cloud Storage
- Google Drive
- Obsidian Sync

---

# Acceptance Criteria

完成後：

- [ ] 可下載 Transcript.md
- [ ] 可下載 Study_Note.md
- [ ] Markdown 格式正確
- [ ] 保留標題
- [ ] 保留 URL
- [ ] 保留換行
- [ ] UI 完全沒有改變

---

# Google AI Studio Prompt

## Task

請修改目前 App。

不要建立新的 App。

目前首頁 UI 已完成。

請保持目前所有 UI 完全不變。

本次只完成：

【Markdown Download】

功能。

需求：

當使用者按下：

【下載逐字稿】

下載：

Transcript.md

內容：

- 影片標題
- YouTube URL
- Transcript

Markdown 格式。

--------------------------------

當使用者按下：

【下載學習筆記】

下載：

Study_Note.md

內容：

- 影片標題
- YouTube URL
- Study Note

Markdown 格式。

--------------------------------

若尚未產生：

Transcript

顯示：

> 尚未產生逐字稿。

若尚未產生：

Study Note

顯示：

> 尚未產生學習筆記。

請保持：

- UI
- Layout
- Color
- Typography

完全不變。

完成後請直接更新目前 App。

---

# Output

使用者流程：

貼上網址

↓

取得影片資訊

↓

取得逐字稿

↓

產生學習筆記

↓

下載：

Transcript.md

↓

下載：

Study_Note.md

---

# Next Prompt

Prompt_06_Testing

目標：

完成 MVP 驗收測試。

---

# Status

Ready for Prompt_06_Testing