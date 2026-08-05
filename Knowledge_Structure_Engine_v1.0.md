---
title: Knowledge Structure Engine Specification
version: v1.0
status: Design Freeze — Approved
owner: YB
last_updated: 2026-08-05
purpose: YB Learn v1.0 正式產品架構。Sprint 7 Task 3 起的所有工程實作，皆以本文件為唯一依據。未經確認不得變更 Product Position／Mission／Vision／Learning Model／Product Principles（見 Why.md）。
---

# Knowledge Structure Engine v1.0

**狀態：Design Freeze — Approved（2026-08-05 確認定稿）**

本文件是 Sprint 7 Task 3 起的產品架構規格，取代原本 Task 3（Learning Blueprint MVP）的單一線性文字樣板實作。與 `Why.md`（Mission／Vision／Product Principles）、`Learn_Package_Specification_v2.0.md`（Learn Package 六模組閱讀動線）、`TODO.md` Sprint 7「Design Freeze — Learning Model v1.0」共同構成產品最高原則，不因單一 Sprint 或功能改動。

---

## 1. Engine 定位

YB Learn 的核心不是 AI 摘要工具、Study Note 工具，也不是 Mind Map 工具，而是 **Knowledge Structure Engine（知識結構引擎）**。

- Study Note 回答「影片說了什麼？」
- Knowledge Structure Engine 回答「影片如何組織知識？」
- Learning Blueprint 回答「我應該如何理解？」
- Teach Back 回答「我是否真的學會了？」

Engine 的任務不是整理文字，而是：**根據內容，自動判斷最適合的知識結構，幫助使用者最快建立 Mental Model。**

Learning Blueprint 不是 Engine 本身，而是 Engine 的**第一個 Output**。未來 Teach Back、Quiz、Action List、Review、Skill Tree 都消費同一個 Engine 產出的 Knowledge JSON，不需要各自重新設計資料結構。

---

## 2. Knowledge Structure Taxonomy — Core Structures（v1.0，可擴充）

**Core Structures（本次實作範圍）：**

| 結構 | 資料形狀 | 適用影片類型 |
|---|---|---|
| Flow／流程 | 有序步驟 `[{step, action, purpose}]` | 教學、SOP、操作示範 |
| Cause & Effect／因果 | 因果鏈 `[{cause, effect, because}]` | 商業分析、時事評論 |
| Classification／分類 | 類別樹 `[{category, items[], trait}]` | 工具介紹、房地產類型比較 |
| Decision／決策 | 條件與選項 `[{condition, options[{choice, outcome}]}]` | 房地產購買建議、選擇型內容 |
| Comparison／比較 | 維度表 `[{dimension, optionA, optionB}]` | A vs B、產品比較 |
| Timeline／時間軸 | 時序事件 `[{time, event, significance}]` | 歷史、時事回顧、成長歷程 |
| Problem → Solution／問題→解法 | `[{problem, root_cause, solution, result}]` | 案例分析、問題解決型內容 |

無法分類時，Fallback 為 `generic`（沿用 `Learn_Package_Specification_v2.0.md` 既有的通用條列後備結構）。

**未來可擴充（不在本次範圍，僅預留架構彈性）：** Framework／Hierarchy／Layer／Cycle／Matrix／Pyramid／Network／其他。新增 Structure 不需要改 Renderer 的分派骨架；新增 Renderer 不需要改 Structure 的判斷邏輯。

每支影片判斷**單一主要結構**（沿用既有 Design Freeze 規則：內容混合多種特徵時，選最主導的單一結構）。

---

## 3. Structure 與 Renderer 正式分離

- **Structure** = 知識本身的語意形狀（資料層）
- **Renderer** = 畫面呈現方式（表現層）：Tree／Flow／Timeline／Card／Table／Diagram

新增 Renderer 不需要改 Structure；新增 Structure 不需要綁死特定 Renderer。兩者透過第 4 節的 Knowledge JSON 解耦。

---

## 4. Knowledge JSON Layer

```
Video
  ↓
Knowledge Extraction
  ↓
Knowledge Structure（判斷屬於哪個 Core Structure）
  ↓
Knowledge JSON（結構化資料，非自由格式文字）
  ↓
Renderer（依 Structure 類型分派排版）
  ↓
Learning Blueprint（呈現結果）
```

**關鍵原則：Renderer 只依賴 Knowledge JSON，不直接依賴 Prompt 輸出的自由文字。** Gemini 輸出必須是結構化 JSON（依 Structure 類型有對應欄位），不能是一段格式化過的 Markdown 長文。JSON 層也是未來 Web／Mobile／Desktop 共用資料的基礎。

---

## 5. Prompt Strategy

**Step 1 — Knowledge Structure Detection**：先判斷影片屬於哪一個 Core Structure（或 fallback `generic`）。

**Step 2 — Knowledge Extraction**：依判定出的 Structure，用該 Structure 專屬的 JSON 欄位抽取內容（例如 Flow 輸出 `steps` 陣列、Comparison 輸出 `dimension/optionA/optionB` 陣列），不是生成一段長文字。

**Renderer** 不屬於 Prompt／AI 的工作範圍，是前端依 Structure 類型把 Knowledge JSON 轉成畫面呈現的邏輯。

技術上用**一次 Gemini call**同時要求先回傳 `structure_type`、再依該類型輸出對應 JSON 欄位（避免兩次 API 呼叫的延遲與成本），邏輯上仍是「先判斷、再依結構抽取」兩個步驟。

---

## 6. Human Test／KPI

不只驗證「有沒有按鈕」「有沒有 Render」，而是驗證：

**30 秒內，使用者只看 Learning Blueprint，能否：**
1. 說出影片的主要知識架構（是流程／因果／分類...等）
2. 理解內容之間的關係（能說出「為什麼 A 導致 B」這類關係，不是逐字複誦）
3. 用自己的話重建約 70% 的內容重點

可操作的驗收項（Task 3／4 範圍內）：
- Structure 判斷是否合理（抽測不同類型影片：教學／商業／工具／房地產／課程）
- 同一影片重新生成，Structure Type 是否穩定一致
- 不同 Structure Type 的輸出，欄位／排版是否明顯不同（不是統一線性樣板）

「是否真的建立 Mental Model」的量化驗證（70% 複述完整度）屬於 Teach Back（Task 5）的主動驗證機制，不在 Task 3／4 範圍內。

---

## 與既有文件的關係

- **`Why.md`**：Mission／Vision／Product Principles 的來源，本文件的 Engine 定位（第 1 節）直接對應 Why.md「我們真正是什麼」的四層能力對照表。
- **`Learn_Package_Specification_v2.0.md`**：定義 Learn Package 六模組（One Sentence／Knowledge Outline／Learning Blueprint／Study Note／Teach Back／Action List）的閱讀動線；本文件是其中 Learning Blueprint 模組的架構深化，Knowledge Outline 由 Learning Blueprint 取代（沿用既有 Design Freeze 規則）。
- **`TODO.md`**：Sprint 7 Design Freeze 記錄與 Task 3～7 開發進度的唯一來源。

---

## Design Freeze 範圍

以下項目已定稿，不再修改，除非未來規劃 v2.0：

- Product Position／Mission／Vision／Product Principles（見 `Why.md`）
- Learning Model 三階段命名（值得學／看懂了／記住了，對應 Orientation／Comprehension／Retention）
- Knowledge Structure Engine 的 7 個 Core Structure 與 Structure／Renderer 分離原則

Sprint 7 Task 3～7 的所有工程實作，以本文件為唯一依據。
