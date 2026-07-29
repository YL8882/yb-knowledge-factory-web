# Prototype_Test_Checklist.md

---
Title: Prototype Test Checklist
Version: v2.0
Status: Final
Owner: YB
Product: YB Knowledge Factory MVP v0.1
Document Type: Prototype Validation Specification
Language: Traditional Chinese
Last Updated: 2026-07-23
---

# 1. Purpose

本文件定義 Google AI Studio Prototype 的驗證標準（Acceptance Criteria）。

目的：

- 驗證 MVP 是否符合產品需求
- 驗證 Workflow 是否完整
- 驗證 Prompt 是否正確
- 驗證 UI 是否符合設計
- 作為 Prototype 是否可交付 Claude Code 的依據

Prototype 必須全部通過本文件所有測試項目，方可進入正式開發階段。

---

# 2. Validation Scope

Prototype 僅驗證 MVP 範圍。

包含：

- Single Page
- Workflow
- Prompt
- Runtime
- Output
- UI

不驗證：

- 效能（Performance）
- 安全性（Security）
- 權限管理
- 多人使用
- 商業功能

---

# 3. Environment Check

確認 Prototype 環境：

| 項目 | 驗證 |
|------|------|
| Google AI Studio 可正常執行 | □ |
| Prototype 可開啟 | □ |
| Prompt 已載入 | □ |
| Runtime 可執行 | □ |

---

# 4. UI Validation

確認畫面符合 Wireframe。

| 項目 | 驗證 |
|------|------|
| Header 顯示正常 | □ |
| URL Input 正常 | □ |
| Generate Button 正常 | □ |
| Workflow Progress 顯示 | □ |
| Audio Module 顯示 | □ |
| Transcript Module 顯示 | □ |
| Study Note Module 顯示 | □ |
| Footer 顯示 | □ |

---

# 5. Workflow Validation

驗證完整 Workflow。

## Step 1

貼上 YouTube URL。

□ 成功

---

## Step 2

按下 Generate。

□ 成功

---

## Step 3

開始 Audio Workflow。

□ 成功

---

## Step 4

開始 Transcript Workflow。

□ 成功

---

## Step 5

開始 Study Note Workflow。

□ 成功

---

## Step 6

Workflow 全部完成。

□ 成功

---

# 6. Module Validation

## Audio Module

| 項目 | 驗證 |
|------|------|
| Status 更新 | □ |
| Audio 建立 | □ |
| File Name 正確 | □ |
| Download Button 可用 | □ |

---

## Transcript Module

| 項目 | 驗證 |
|------|------|
| Status 更新 | □ |
| Transcript 建立 | □ |
| Markdown 格式正確 | □ |
| Download Button 可用 | □ |

---

## Study Note Module

| 項目 | 驗證 |
|------|------|
| Status 更新 | □ |
| Study Note 建立 | □ |
| Template 正確 | □ |
| Download Button 可用 | □ |

---

# 7. Output Validation

確認輸出。

| 檔案 | 驗證 |
|------|------|
| Audio.mp3 | □ |
| Transcript.md | □ |
| StudyNote.md | □ |

---

# 8. File Naming Validation

確認命名規則。

Audio：

□ `{VideoTitle}_{YouTubeID}.mp3`

Transcript：

□ `{VideoTitle}_{YouTubeID}_Transcript.md`

Study Note：

□ `{VideoTitle}_{YouTubeID}_StudyNote.md`

---

# 9. Prompt Validation

確認 Prompt。

| 項目 | 驗證 |
|------|------|
| System Instructions 生效 | □ |
| Task Prompt 生效 | □ |
| Output Schema 正確 | □ |
| Study Note 品質符合需求 | □ |

---

# 10. State Validation

所有 Module：

Waiting

↓

Processing

↓

Completed

↓

Downloaded

驗證：

□ Waiting

□ Processing

□ Completed

□ Downloaded

Error：

□ Error 顯示正常

□ Retry 正常

---

# 11. Runtime Validation

確認 Runtime。

| 項目 | 驗證 |
|------|------|
| Audio → Transcript | □ |
| Transcript → Study Note | □ |
| Runtime 無中斷 | □ |
| Module 順序正確 | □ |

---

# 12. User Experience Validation

確認操作流程。

| 項目 | 驗證 |
|------|------|
| 操作簡單 | □ |
| 畫面清楚 | □ |
| Workflow 易理解 | □ |
| 狀態明確 | □ |
| 下載容易 | □ |

---

# 13. Acceptance Criteria

Prototype 必須符合：

✓ Single Page

✓ Workflow 完整

✓ Prompt 正確

✓ Runtime 正常

✓ UI 正常

✓ 三個 Module 全部成功

✓ 三個 Output 全部成功

✓ Download 正常

全部完成後：

Prototype 驗收通過。

---

# 14. Handoff Criteria

符合以下條件即可交付 Claude Code：

- 所有 Acceptance Criteria 通過
- 無阻塞性問題
- Workflow 可完整執行
- Prompt 品質符合需求

---

# 15. Final Result

Validation Result：

□ PASS

□ FAIL

Reviewer：

__________________

Review Date：

__________________

Comments：

________________________________________

---

# Document Summary

Prototype_Test_Checklist.md 為 Google AI Studio Prototype 的正式驗收文件。

其目的不是進行程式測試，而是確認 Prototype 是否已符合 MVP 規格，並作為是否交付 Claude Code 進行正式開發的唯一驗收依據。