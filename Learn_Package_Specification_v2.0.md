---
title: Learn Package Specification
version: v2.0
status: Draft — awaiting confirmation
purpose: Sprint 7 Task 0 (Learning Blueprint Engine) deliverable. Defines the structure of the next-generation Learn Package. Specification only — no Prompt design, no UI design, no Workflow change.
---

# Learn Package Specification v2.0

**Sprint 7 — Task 0：Learning Blueprint Engine**

本次目標不是新增功能，是重新設計 Learn Package 的結構。本文件只定義結構，是規格文件，不是實作文件。

## 產品定位

YB Learn 的目標不是產生 Study Note。

目標是：讓使用者花 **3 分鐘**建立知識輪廓，並能**說出影片約 70% 的內容**。

Learn Package 是達成這個目標的產出格式，共 6 個模組：定錨（1 句話）、建圖（輪廓）、記憶（藍圖）、查閱（完整筆記）、驗證（複述練習）、行動（今天能做的事）。

本文件只定義**結構**，不涉及：
- 由哪個／哪些 Prompt 產生內容（Prompt 設計留待規格確認後、拆分 Sprint 7 各 Task 時再進行）
- UI 呈現方式（本次不設計 UI）
- 是否／如何修改既有 Workflow、Pipeline（本次不修改，沿用現有 Transcript 作為輸入來源）

---

## 閱讀動線

```
One Sentence → Knowledge Outline → Learning Blueprint → Study Note → Teach Back → Action List
```

先用「一句話」定錨，再用「輪廓」建立地圖，再用「Learning Blueprint」讓使用者能夠複述吸收——這三步是 3 分鐘理解＋70% 複述目標的核心。Study Note 是「需要時查閱」的完整內容。Teach Back 是主動驗證：檢查前面建立的記憶是否真的內化。Action List 收尾，把知識轉成行動。

---

## 1. One Sentence

**目的：** 讓使用者在幾秒內知道這支影片在講什麼，作為進入 Knowledge Outline 前的錨點。

**內容規則：**
- 單一句子，建議 40～60 字內
- 必須包含「核心主題」＋「核心價值／結論」，不是「這支影片介紹了...」這種空泛開頭
- 讀完這句話，使用者不需要看任何其他內容，就能回答「這支影片在講什麼」

**格式：** 純文字，單行。

**驗收標準：** 只讀這一句話，就能對別人複述「這支影片在講什麼」。

---

## 2. Knowledge Outline（知識輪廓）

**目的：** 建立影片的邏輯骨架——不是逐字重述內容，而是抽出「影片涵蓋哪些範疇、彼此如何關聯」。

**內容規則：**
- 階層式結構，建議 2～3 層
- 一級節點建議 3～7 個（避免資訊過載）
- 每個節點是精簡標籤／短句，不是完整段落
- 順序依照影片實際敘事順序或邏輯優先順序（依內容類型判斷）

**格式：** 巢狀清單。

**驗收標準：** 只看 Outline，使用者能畫出「這支影片大概分幾塊、順序是什麼」。

---

## 3. Learning Blueprint（原 Memory Blueprint）— 本次設計重點

**目的：** 不是給你「查閱用」的資料結構，是給你「記憶用、複述用」的結構。設計目標：使用者看過一次後，闔上畫面，能不看原文自己說出約 70% 的內容。

**明確排除：** 傳統放射狀心智圖（一個中心節點向四面八方發散、缺乏順序性、閱讀者需要自己決定閱讀路徑、不利於「複述」）。

**設計原則（符合人腦理解與回憶順序的結構）：**

1. **線性／半線性敘事流**：資訊排成一條可以直接「複述」的路徑，不是需要自行拼湊的網狀圖
2. **因果／邏輯鏈**：用 Problem → Solution、Before → After、因為...所以... 這類關係連接重點，不是單純分類清單
3. **分層 Chunking**：3～5 個「記憶錨點」（一級重點）→ 每個錨點底下 1～3 個支撐細節（符合工作記憶的組塊限制）
4. **可複述的短句／關鍵詞**：每個錨點用短句或關鍵詞呈現，不是完整段落——目的是讓使用者「用自己的話展開」，不是背誦原文
5. **明示邏輯關係**：錨點之間用連接詞或箭頭（→、因為／所以、接著）標示關係，強化回憶路徑

**格式範例：**

```
[錨點1：標籤] → 細節a → 細節b
   ↓（因為／所以／接著）
[錨點2：標籤] → 細節a → 細節b
   ↓
[錨點3：標籤] → 細節a
```

**驗收標準：** 使用者只看 Learning Blueprint（不看 Study Note 全文），闔上畫面後口頭複述，應能涵蓋原內容約 70% 的重點。（如何客觀驗證這個 70%，見下方 Teach Back 模組。）

---

## 4. Study Note（完整學習內容）

**目的：** 保留目前已存在、完整、結構化的學習筆記，作為「深入查閱」用途。Learning Blueprint 是精簡入口，Study Note 是完整內容備查。

**內容規則：** 延用現有 Study Note 結構與 Prompt（Title／Summary／Key Points／Important Concepts／Workflow／Action Items／Tags）——**本次不修改**其內容邏輯，Learn Package 只是把它納入成為第 4 個模組。

**格式：** 延用現有 Markdown 格式，不變動。

---

## 5. Teach Back（教學回顧）— 新增模組

**目的：** 主動驗證機制。Learning Blueprint 提供「容易複述的結構」，但結構好不代表使用者真的內化了——Teach Back 是讓使用者實際「輸出」一次，用「假裝教別人」的方式驗證並強化記憶，直接對應「說出約 70% 內容」這個產品目標的驗收動作，而不只是被動提供一份好記的筆記。

**內容規則：**
- 提供一組「教學提示」：例如「請用自己的話，向一個完全沒看過這支影片的人解釋：這支影片在講什麼？」
- 搭配 3～5 個對應 Learning Blueprint 各記憶錨點的子提示（每個錨點一個引導問題）
- 附一份「自我檢核清單」：列出使用者複述時應該有提到的關鍵字／重點，讓使用者對照自己的複述內容，自行判斷有沒有涵蓋到 70%

**格式：** 條列式教學提示 ＋ 自我檢核清單。

**與 Learning Blueprint 的關係：** Learning Blueprint 是「記憶的骨架」，Teach Back 是「驗證記憶是否真的建立」的主動練習——兩者搭配才能真正達成「看過一次→能複述 70%」，不只是提供一個好記的結構。

**驗收標準：** 使用者依照教學提示口頭或書面複述後，對照自我檢核清單，能自行判斷複述涵蓋率是否達到約 70%。

---

## 6. Action List（行動清單）

**目的：** 把知識轉成「今天就能執行」的具體行動——強調可執行性與時效性，不是抽象的「應用所學」。

**內容規則：**
- 條列式，建議 3～5 條
- 每條需符合「今天可執行」：明確動詞開頭、範圍有限、不依賴額外資源取得
- 與現有 Study Note 的「Action Items」欄位可能重疊（見下方待確認問題）

**格式：** 條列清單。

---

## 待你確認的開放問題

1. **Action List 與現有 Study Note 內的「Action Items」是同一件事，還是刻意分開、意義不同？**（例如 Action Items 是「所有建議行動」，Action List 是「篩選後、今天就能做的」）
2. **Learn Package 是否完全取代目前單一的 `Study_Note.md` 輸出？** 還是在其之外「新增」五個模組（One Sentence／Knowledge Outline／Learning Blueprint／Teach Back／Action List），Study Note 維持現狀不變？
3. **Learning Blueprint 的具體呈現方式**，你比較偏好上面草擬的「線性條列＋箭頭」，還是你腦中已經有其他具體形式（例如故事線 Storyline、時間軸 Timeline、問題-解答鏈 Q&A Chain）？
4. **Teach Back 的形式**，你偏好「提示問題＋自我檢核清單」（如上）這種輕量文字形式，還是希望之後（不在本次範圍）發展成互動式問答？

---

等你確認以上結構（含四個開放問題）後，才會把 Sprint 7 拆成各個開發 Task（Task 1 起）。本文件（Task 0）目前不涉及程式、UI、Prompt 修改。
