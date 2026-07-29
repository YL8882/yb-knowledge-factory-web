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
Last Updated: 2026-07-29
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
| TC-001 | 輸入有效 YouTube URL | 成功接受網址 | ☐ |
| TC-002 | 自動取得影片標題 | 顯示正確標題 | ☐ |
| TC-003 | 新增至 Queue | Queue 顯示新項目 | ☐ |
| TC-004 | 產生 Transcript | 成功建立 Transcript.md | ☐ |
| TC-005 | 產生 Study Note | 成功建立 Study_Note.md | ☐ |
| TC-006 | 下載 Transcript | 可下載 Markdown | ☐ |
| TC-007 | 下載 Study Note | 可下載 Markdown | ☐ |

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

- [ ] 流程可完整執行
- [ ] 無中斷
- [ ] 無錯誤訊息
- [ ] 執行時間符合預期

---

# Output Verification

## Transcript

確認：

- [ ] 檔案建立成功
- [ ] UTF-8 編碼
- [ ] Markdown 格式
- [ ] 第一行包含影片名稱
- [ ] 第二行包含 YouTube URL

---

## Study Note

確認：

- [ ] 摘要完整
- [ ] 重點整理正確
- [ ] Workflow 存在
- [ ] Markdown 格式正確

---

# User Experience Checklist

- [ ] 首頁正常顯示
- [ ] Queue 更新正常
- [ ] Loading 顯示正常
- [ ] Error Message 正確
- [ ] Success Notification 正常

---

# Error Handling

測試：

- [ ] 空白 URL
- [ ] 非 YouTube 網址
- [ ] 無效影片
- [ ] Transcript 取得失敗
- [ ] LLM 回應失敗

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

- [ ] 所有 Critical Test Case 通過
- [ ] Workflow 完整
- [ ] Markdown 可下載
- [ ] 無重大 Bug
- [ ] Product Owner 驗收完成

---

# Test Result

| Tester | Date | Result |
|--------|------|--------|
| | | ☐ PASS / ☐ FAIL |

---

# Notes

- 發現的新問題請記錄至 `Engineering_Backlog.md`。
- 若需修改產品需求，請同步更新 `CHANGELOG.md` 並依版本管理流程處理。

---

End of Document