---
Version: v2.0
Status: Final
Owner: YB
Document: Wireframe Specification
Category: UI/UX Specification
Purpose: Define the standard wireframe architecture, layout principles, navigation structure, and design guidelines for all AI Products.
Scope: All AI Products
Priority: Critical
Author: ChatGPT
Last Updated: 2026-07-29
Related Documents:
  - Development_Operating_System.md
  - Product_Architecture.md
  - UI_Component_Specification.md
  - Workflow_Specification.md
  - PRD.md
---

# Wireframe Specification

> Standard Wireframe Design Blueprint for AI Product Factory

---

# 1. Purpose

本文件定義 AI Product 的 Wireframe（線框圖）設計標準。

目的：

- 建立一致的 UI Layout
- 定義頁面架構
- 定義畫面層級
- 定義導航方式
- 提高 UI 一致性
- 降低重新設計成本

本文件描述：

- 頁面配置（Layout）
- 資訊架構（Information Architecture）
- 導覽（Navigation）
- 畫面流程（Screen Flow）

本文件不描述：

- UI Style
- Color
- Icon
- Animation
- Component Design

---

# 2. Design Principles

所有 Wireframe 必須遵循：

| Principle | Description |
|------------|-------------|
| User First | 使用者操作優先 |
| Simplicity First | 保持簡潔 |
| One Goal Per Screen | 每個畫面一個主要目標 |
| Progressive Disclosure | 漸進式資訊揭露 |
| Consistency | 一致性 |
| Responsive | 響應式設計 |
| Accessibility | 易於操作 |
| Scalable | 可擴充 |

---

# 3. Information Architecture

```
Application

├── Home

├── Dashboard

├── Detail

├── Settings

└── Help
```

所有產品：

至少應建立：

- 首頁
- 主要功能
- 詳細頁
- 設定

---

# 4. Screen Hierarchy

```
Home

↓

Feature

↓

Detail

↓

Result

↓

Export
```

避免：

```
Home

↓

大量跳轉

↓

返回

↓

跳轉

↓

返回
```

保持：

單一路徑。

---

# 5. Standard Screen Layout

```
+--------------------------------------+

Header

----------------------------------------

Navigation（Optional）

----------------------------------------

Content

----------------------------------------

Primary Action

----------------------------------------

Footer（Optional）

+--------------------------------------+
```

---

# 6. Navigation Architecture

建議：

```
Home

├── Dashboard

├── History

├── Settings

└── Help
```

Navigation：

保持：

最多兩層。

避免：

三層以上。

---

# 7. User Flow

標準流程：

```
Open

↓

Input

↓

Processing

↓

Result

↓

Export

↓

Done
```

避免：

```
Input

↓

Settings

↓

Back

↓

Retry

↓

Again
```

---

# 8. Screen Categories

建議畫面：

| Screen | Purpose |
|---------|---------|
| Home | 首頁 |
| Dashboard | 功能入口 |
| Input | 輸入 |
| Processing | 執行中 |
| Result | 結果 |
| Detail | 詳細內容 |
| Export | 匯出 |
| Settings | 設定 |
| About | 關於 |

---

# 9. Layout Grid

Desktop：

```
12 Columns
```

Tablet：

```
8 Columns
```

Mobile：

```
4 Columns
```

保持：

一致 Grid。

---

# 10. Responsive Rules

Desktop：

優先。

Tablet：

自適應。

Mobile：

保留核心功能。

不要：

重新設計整個介面。

---

# 11. Wireframe Levels

每個產品：

遵循：

```
Low Fidelity

↓

Mid Fidelity

↓

High Fidelity

↓

Prototype
```

Low：

功能配置。

Mid：

資訊排列。

High：

接近正式 UI。

Prototype：

可互動。

---

# 12. Wireframe Naming Standard

建議：

```
WF_01_Home

WF_02_Input

WF_03_Processing

WF_04_Result

WF_05_Settings
```

避免：

```
首頁2

新版首頁

Final

Final2
```

---

# 13. Wireframe Folder Structure

```
wireframes/

README.md

WF_01_Home.md

WF_02_Input.md

WF_03_Result.md

WF_04_Settings.md

Prototype/

Images/
```

---

# 14. Wireframe Review Checklist

每個 Wireframe：

□ 一個畫面一個目標

□ Layout 清楚

□ Navigation 清楚

□ User Flow 合理

□ Action Button 明確

□ Responsive 完整

□ Information Hierarchy 清楚

□ 與 Workflow 一致

---

# 15. Success Criteria

Wireframe 成功代表：

- 使用者快速理解
- 操作流程順暢
- Layout 一致
- Navigation 清楚
- 易於 Prototype
- 易於實作
- 易於測試
- 易於擴充

---

# Design Principles

Wireframe Specification 僅定義：

- Layout
- Screen
- Navigation
- User Flow
- Information Architecture

UI 樣式、Component、Color、Typography 等內容，應由 UI_Component_Specification.md 負責。

Workflow、Prompt、Runtime、Output 等內容，應由各自 Specification 文件負責。

---
End of Document