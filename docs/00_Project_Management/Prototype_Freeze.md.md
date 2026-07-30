---
版本：v1.0
狀態：Final
負責人：YB
文件名稱：Prototype_Freeze
文件分類：Project Management
用途：凍結 Google AI Studio Prototype，作為 Claude Code 唯一實作依據
優先級：Critical
最後更新：2026-07-30
---

# Prototype Freeze

> 本文件用於凍結（Freeze）Google AI Studio Prototype，作為 AI Coding Agent（如 Claude Code）實作產品的唯一 UI 與 Workflow 規格來源。

---

# 一、文件目的

Prototype Freeze 的目的在於：

- 確認 Prototype 已完成驗證
- 宣告 Prototype 為正式版本
- 防止 AI Coding Agent 自行重新設計 UI
- 建立 Prototype 與實作階段之間的正式交接點（Implementation Handover）

本文件不負責：

- UI 設計
- Workflow 設計
- Product Requirement

僅負責宣告哪些 Prototype 已正式凍結。

---

# 二、Prototype 狀態

**狀態：Approved（已核准）**

Google AI Studio Prototype 已完成驗證，可作為正式實作依據。

---

# 三、Prototype Authority（最高優先權）

下列 Prototype 為本產品唯一官方版本：

## Homepage

- Homepage_High_Fidelity_v2.png

## Navigation

- 03_Navigation_Diagram

## Workflow

- 02_Workflow_Diagram

## Component

- 04_Component_Map

## User Journey

- 06_User_Journey

以上檔案具有最高優先權。

若與其他文件內容衝突，以 Prototype 為準。

---

# 四、Implementation Rules

Claude Code 或其他 AI Coding Agent 必須遵循以下規則：

## 必須（Must）

- 忠實實作 Prototype
- 保留版面配置（Layout）
- 保留導覽流程（Navigation）
- 保留 UI 層級（Visual Hierarchy）
- 保留主要操作流程（Workflow）
- 保留色彩系統（Color System）
- 保留 Typography
- 保留元件配置（Component Layout）

---

## 禁止（Must Not）

不得：

- 自行重新設計首頁
- 自行更改操作流程
- 自行修改色彩風格
- 自行加入新的 UI 元件
- 自行刪除既有功能
- 使用預設 Bootstrap 版型取代 Prototype

除非 Repository Owner 明確核准。

---

# 五、Language Policy

本產品統一採用：

## UI

台灣繁體中文（zh-TW）

## Transcript

台灣繁體中文（zh-TW）

## Study Note

台灣繁體中文（zh-TW）

## Markdown

UTF-8

所有輸出不得使用簡體中文。

---

# 六、Workflow Freeze

官方 Workflow：

```text
貼上 YouTube 網址
        │
        ▼
自動取得影片名稱
        │
        ▼
取得逐字稿
        │
        ▼
產生學習筆記
        │
        ▼
下載 Markdown
```

AI Coding Agent 不得自行改變流程。

---

# 七、Design Changes

若需修改 Prototype：

必須：

1. 更新 Google AI Studio Prototype
2. 完成 Prototype Review
3. 更新 Prototype_Freeze.md
4. 再交由 Claude Code 實作

不得直接修改程式取代 Prototype。

---

# 八、Implementation Handover

Prototype Freeze 完成後：

正式交由 Claude Code 進入實作階段。

Claude Code 應以本文件及 Prototype 為最高優先權。

---

# 九、關聯文件

- PRD.md
- Product_Architecture.md
- Workflow_Specification.md
- Product_Index.md
- Milestone_00_Project_Freeze.md

---

# 十、結論

Google AI Studio Prototype 已完成驗證，並正式凍結為本產品唯一官方 UI 與 Workflow 規格。

所有 AI Coding Agent 均應依據 Prototype 實作，不得自行重新設計介面、流程或互動方式。

Prototype Freeze 是 AI Product Factory 中，Prototype 與正式開發之間的唯一交接點，也是未來所有產品的標準流程。