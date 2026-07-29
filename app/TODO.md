---
Version: v1.0
Status: Active
Owner: YB
Document: TODO
Category: Development
Purpose: Track the current implementation tasks for Claude Code.
Scope: YB Knowledge Factory MVP v0.1
Priority: High
Author: ChatGPT
Last Updated: 2026-07-29
Related Documents:
  - Project_Dashboard.md
  - Product_Index.md
  - PRD.md
  - Engineering_Backlog.md
---

# TODO

> Current Development Tasks

---

# Current Sprint

**Milestone 02 – Build MVP v0.1**

Status

🟡 In Progress

Goal

完成第一個可正常運作的 MVP。

---

# Priority 1 - Core Features

## Home Page

- [ ] 建立首頁版面
- [ ] 套用 YB 品牌配色
- [ ] 響應式版面（Desktop First）

---

## YouTube Import

- [ ] 貼上 YouTube URL
- [ ] 驗證網址格式
- [ ] 自動取得影片標題
- [ ] 新增至 Queue

---

## Queue

- [ ] 建立 Queue 清單
- [ ] 顯示影片名稱
- [ ] 顯示處理狀態
- [ ] 支援移除項目

---

## Transcript

- [ ] 建立 Transcript API
- [ ] 取得逐字稿
- [ ] 儲存 Transcript.md

---

## Study Note

- [ ] 呼叫 LLM 生成 Study Note
- [ ] 套用 Study Note Template
- [ ] 儲存 Study_Note.md

---

## Export

- [ ] 下載 Transcript.md
- [ ] 下載 Study_Note.md

---

# Priority 2 - User Experience

- [ ] Loading 動畫
- [ ] 錯誤訊息提示
- [ ] 成功通知
- [ ] Queue 完成狀態

---

# Priority 3 - Testing

- [ ] YouTube URL 測試
- [ ] Transcript 測試
- [ ] Study Note 測試
- [ ] Markdown 匯出測試

---

# Completed

> 完成後將工作移至此區塊。

---

# Blocked

> 記錄目前無法完成或等待決策的項目。

---

# Notes

- MVP 階段不新增 Scope。
- 所有新需求先記錄至 Engineering_Backlog.md。
- 優先完成可運作版本，再進行優化。

---

# Definition of Done

完成以下條件即視為 MVP 完成：

- [ ] 可輸入 YouTube URL
- [ ] 可取得影片標題
- [ ] 可產生 Transcript
- [ ] 可產生 Study Note
- [ ] 可下載 Transcript.md
- [ ] 可下載 Study_Note.md
- [ ] 完成基本操作流程測試

---

End of Document