---
Version: v1.0
Status: Active
Owner: YB
Document: Acceptance Test
Category: Quality Assurance
Purpose: Define the acceptance criteria and test checklist for Milestone 02.
Scope: YB Knowledge Factory MVP v0.1
Priority: High
Author: ChatGPT
Last Updated: 2026-07-30
Related Documents:
  - PRD.md
  - Workflow_Specification.md
  - Output_Specification.md
  - TODO.md
---

# Acceptance Test

> Milestone 02 – Build MVP v0.1

---

# Purpose

本文件定義 MVP 的正式驗收標準。

只有通過所有 Critical Test Case，Milestone 02 才能視為完成。

---

# Test Environment

| Item | Value |
|------|-------|
| Platform | Windows 11 |
| Browser | Chrome (Latest) |
| Development | Claude Code |
| AI Model | Gemini / OpenAI（依實際設定） |

---

# Acceptance Criteria

MVP 必須完成：

- 可輸入 YouTube URL
- 可成功取得影片資訊
- 可建立 Queue
- 可產生 Transcript
- 可產生 Study Note
- 可下載 Transcript.md
- 可下載 Study_Note.md

---

# Functional Test Cases

| ID | Test Item | Expected Result | Status |
|----|-----------|-----------------|--------|
| TC-001 | 輸入有效 YouTube URL | 成功接受網址 | ☑ PASS |
| TC-002 | 自動取得影片標題 | 顯示正確標題 | ☑ PASS |
| TC-003 | 新增至 Queue | Queue 顯示新項目 | ☑ PASS |
| TC-004 | 產生 Transcript | 成功建立 Transcript.md | ☑ PASS |
| TC-005 | 產生 Study Note | 成功建立 Study_Note.md | ☑ PASS |
| TC-006 | 下載 Transcript | 可下載 Markdown | ☑ PASS |
| TC-007 | 下載 Study Note | 可下載 Markdown | ☑ PASS |

詳細測試步驟與截圖等級證據見 `docs/MVP_Test_Report.md` §3.1。

---

# Workflow Verification

驗證完整流程：

```text
Paste URL
      │
      ▼
Get Video Title
      │
      ▼
Queue
      │
      ▼
Transcript
      │
      ▼
Study Note
      │
      ▼
Download Markdown
```

Checklist：

- [x] 流程可完整執行
- [x] 無中斷
- [x] 無錯誤訊息
- [x] 執行時間符合預期

---

# Output Verification

## Transcript

確認：

- [x] 檔案建立成功
- [x] UTF-8 編碼
- [x] Markdown 格式
- [x] 第一行包含影片名稱
- [x] 第二行包含 YouTube URL

---

## Study Note

確認：

- [x] 摘要完整
- [x] 重點整理正確
- [x] Workflow 存在
- [x] Markdown 格式正確

---

# User Experience Checklist

- [x] 首頁正常顯示
- [x] Queue 更新正常
- [x] Loading 顯示正常
- [x] Error Message 正確
- [x] Success Notification 正常

---

# Error Handling

測試：

- [x] 空白 URL
- [x] 非 YouTube 網址
- [x] 無效影片
- [x] Transcript 取得失敗（依賴 yt-dlp／faster-whisper 例外處理，已走過錯誤路徑，見 MVP_Test_Report.md）
- [x] LLM 回應失敗（Gemini Key 未設定／呼叫失敗，見 MVP_Test_Report.md §3.3）

系統應：

- 顯示明確錯誤訊息
- 不發生程式崩潰

---

# Performance Targets

| Item | Target |
|------|--------|
| 首頁載入 | < 3 秒 |
| Queue 更新 | < 1 秒 |
| Transcript 建立 | 可接受（依影片長度） |
| Study Note 建立 | 可接受（依模型速度） |

---

# Definition of Done

Milestone 02 視為完成，需符合：

- [x] 所有 Critical Test Case 通過
- [x] Workflow 完整
- [x] Markdown 可下載
- [x] 無重大 Bug
- [ ] Product Owner 驗收完成（待您正式確認；本次已確認 Study Note 章節命名維持現行實作，見 CHANGELOG.md「MVP v0.1 — Documentation Sync」）

---

# Test Result

| Tester | Date | Result |
|--------|------|--------|
| Claude Code | 2026-07-29 | ☑ PASS（詳見 `docs/MVP_Test_Report.md`，待 Product Owner 最終確認） |

---

# Notes

- 發現的新問題請記錄至 `Engineering_Backlog.md`。
- 若需修改產品需求，請同步更新 `CHANGELOG.md` 並依版本管理流程處理。

---

End of Document