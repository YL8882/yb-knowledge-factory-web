# Study Note

Title: Suno AI 2026 作曲完整教學 | 入門到進階 | AI創作歌曲不僅好聽還可以商用

Source: https://www.youtube.com/watch?v=Xv_cpCtN4yE

Author: 未提供

Date: 2026-08-01

Language: 繁體中文

Tags: #SunoAI #AI音樂創作 #SunoV5 #CustomMode #Extend #Cover #Persona

Version: v1.0

---

## Executive Summary

Suno AI V5 是一款無需樂理知識也能生成高品質音樂的 AI 工具。本影片詳細介紹其最新功能，從簡易模式到客製化創作、進階的 Extend、Cover、人設（Persona）功能，以及音軌分離，協助使用者高效創作歌曲並了解商用潛力。

## Key Takeaways

*   Suno AI V5 提供簡易模式與客製化模式，能快速生成歌詞與音樂。
*   Custom Mode 透過 MetaTag 和 Style Tag 精確控制歌曲結構、唱腔與風格。
*   Extend 和 Cover 功能允許在保持調性或旋律下延伸或改編歌曲。
*   Audio Influence 參數能調整 AI 參考上傳音檔的程度。
*   Persona 功能可建立人設，讓 AI 參考特定風格或聲音生成歌曲。
*   最新版支援 Extract Stems（音軌分離），方便後製與二次創作。

## Detailed Notes

### Suno AI V5 介面與基本操作

*   **Create Workspace (工作區)**
    *   建議在開始製作歌曲前建立新的 Workspace。
    *   Workspace 類似資料夾，有助於管理和搜尋同一專案中的多首嘗試歌曲。
*   **Simple Mode (簡易模式)**
    *   可直接讓 AI 生成一首歌。
    *   勾選 `Instrumental`：生成純背景音樂。
    *   可生成 Lo-Fi Music。
    *   不勾選 `Instrumental`：生成帶歌詞的歌曲。
    *   每次生成會自動產生兩首歌曲。
*   **Custom Mode (客製化模式)**
    *   分為 Lyrics (歌詞) 與 Style (風格) 兩大部分。

### 歌詞 Lyrics

*   **AI 寫詞功能**
    *   點選魔法棒圖示，告訴 Suno 想要的歌曲類型，AI 會自動生成兩份歌詞供選擇。
    *   **MetaTag (中繼標籤)**
        *   功能：快速定義歌曲結構。
        *   常用結構型 MetaTag 範例：`[Intro]`, `[Verse 1]`, `[Verse 2]`。
        *   功能：指示 Suno AI 演唱方式或情緒。
        *   範例：`[Melodic Vocal]`, `[Vibrato Vocal]`, `[Spoken]`, `[High Energy]`, `[Emotional]`。
        *   注意事項：情緒類標籤（如 `[High Energy]`）依經驗可能不穩定，需多嘗試。
    *   **饒舌 Verse**
        *   將 `[Verse]` 改為 `[Rap Verse]` 即可。
    *   **Alem (即興短句)**
        *   將歌詞放在括號 `()` 內，增加極短句或感嘆詞。
        *   目的：增加歌曲的情緒與層次。
    *   **歌詞寫作建議**
        *   Suno AI 較擅長生成英文歌詞。
        *   若不想自行寫詞，可使用 ChatGPT 等工具輔助生成歌詞。

### 風格 Style

*   **Style Tags**
    *   用於告訴 Suno AI 歌曲的風格，例如 `R&B`, `Country Pop`。
    *   若不確定歌曲風格，可詢問 ChatGPT (例如：詢問 Taylor Swift 歌曲的風格)。
    *   點選右上角的魔法棒可讓 Suno AI 最佳化 Style Tags。
    *   **重要提醒：** 歌詞內容也會影響 AI 生成的風格走向。

### 進階選項 Advanced Options

*   **Exclude Styles (排除風格)**
    *   告知 Suno AI 不想要聽到的樂器或風格，例如 `No Guitar`, `No Piano`。
*   **Gender (性別)**
    *   選擇 `Male` (男生) 或 `Female` (女生)。
*   **Warmth**
    *   描述歌曲的「正常」程度，是否符合大眾歌曲走向。
    *   `0` (中規中矩)，`100` (較不尋常)。
    *   建議設定在 `50-80` 之間，讓歌曲保有變化性又不至於太奇怪。
*   **Style**
    *   設定 Suno AI 參考 Style Tags 的比重。
    *   `0`：Suno AI 主要依歌詞意思推算歌曲風格。
    *   `100`：Suno AI 完全依照使用者提供的 Style Tags 生成。

### Upload Audio (上傳音檔)

*   **功能**
    *   可錄製一段聲音或上傳一段旋律，Suno AI 會以此為基礎生成歌曲。
    *   上傳音檔後，點選 `Remix Edit` 進行後續操作。
*   **Extend (延續)**
    *   用途：用原本的調性與風格延續歌曲。
    *   特點：生成的旋律會與上傳音檔不同。
    *   可選擇從音檔的特定位置開始延續。
*   **Cover (翻唱)**
    *   用途：保持原本的旋律，但更換風格或伴奏。
    *   注意事項：撰寫歌詞時，字數需與原本旋律的字數對應。
*   **Audio Influence (音檔影響力)**
    *   設定 Suno AI 參考上傳音檔的程度。
    *   `0`：Suno AI 不太參考音檔。
    *   `100`：Suno AI 完全參考音檔。

### Instrumental (純音樂) 與 Vocal (人聲)

*   **Add Instrumental (新增伴奏)**
    *   上傳人聲，Suno AI 會為其配樂。
    *   建議將 `Audio Influence` 調高至 `70` 以上，以使生成音樂與原音檔相似。
*   **Add Vocal (新增人聲)**
    *   上傳伴奏，Suno AI 會為其填詞並生成人聲。
    *   建議將 `Audio Influence` 調高，以確保生成人聲與伴奏吻合。

### Persona (人設)

*   **功能**
    *   建立一個人設，讓 Suno AI 在生成歌曲時參考特定歌曲或聲音的風格。
    *   可選擇已生成的歌曲或已上傳的音檔來建立 Persona。
*   **應用**
    *   建立完成後，在生成歌曲時可選擇已建立的 Persona。
    *   若要生成歌曲與 Persona 的風格非常相似，建議將 `Audio Influence` 調高至 `80` 以上。

### Extract Stems (音軌分離)

*   **功能**
    *   將已生成的歌曲分離成不同的音軌（如人聲、鼓、樂器等）。
    *   需消耗 `50 Credit`。
*   **操作**
    *   可播放歌曲，並選擇將特定音軌靜音 (Mute, M) 或獨奏 (Solo, S)。
*   **用途**
    *   分離後的音軌品質良好，可單獨下載人聲或伴奏。
    *   適用於自行演唱、二次創作或進行採樣。

## Core Concepts

*   **Suno AI:** 一款基於人工智慧的音樂生成工具，可將文字提示轉換為歌曲。
*   **Workspace:** 在 Suno AI 平台中用於組織和管理多個歌曲專案的虛擬空間。
*   **Simple Mode:** Suno AI 的簡易歌曲生成模式，使用者僅需輸入基本提示即可快速生成歌曲。
*   **Custom Mode:** Suno AI 的進階客製化模式，允許使用者對歌詞、風格及其他音樂參數進行精確控制。
*   **MetaTag:** 用於定義歌曲結構（如 `[Verse]`, `[Chorus]`）和唱腔（如 `[Melodic Vocal]`）的特殊標籤，置於歌詞中。
*   **Alem:** 在歌詞中以括號 `()` 表示的短句、感嘆詞或語氣詞，用以增加歌曲的情緒和層次。
*   **Style Tags:** 描述歌曲音樂風格的關鍵字或短語，如 `R&B`, `Pop`, `Jazz`，用於引導 AI 生成特定風格的音樂。
*   **Advanced Options:** 在 Custom Mode 下提供更細緻的生成控制參數，包括排除風格、性別、歌曲的「常規性」和風格參考比重。
*   **Extend:** Suno AI 的一項功能，用於在保持原始調性與風格的前提下，從歌曲的某一點開始生成新的、旋律不同的後續部分。
*   **Cover:** Suno AI 的一項功能，用於在保持原始旋律不變的情況下，改變歌曲的風格、伴奏或人聲。
*   **Audio Influence:** 一個參數，用來控制 Suno AI 在生成音樂時對上傳音檔的參考程度，數值越高表示參考程度越強。
*   **Persona:** 在 Suno AI 中建立的「人設」，可選擇已有的歌曲或音檔作為參考，讓 AI 在生成新歌曲時模仿其風格或聲線特徵。
*   **Extract Stems:** Suno AI 的一項音軌分離功能，可將生成歌曲中的不同音軌（如人聲、鼓、旋律）分開，方便後製、混音或採樣。

## Workflow

1.  **Step 1: 建立工作區**
    *   **動作:** 在 Suno AI 介面中，點選左側「Create」後，建議先建立一個新的 Workspace。
    *   **目的/注意事項:** Workspaces 類似資料夾，方便管理和搜尋多首嘗試生成的歌曲。
2.  **Step 2: 選擇生成模式**
    *   **動作:** 選擇「Simple Mode」或「Custom Mode」。
    *   **目的/注意事項:**
        *   Simple Mode 適用於快速生成歌曲，可勾選 `Instrumental` 生成純背景音樂，或直接生成帶歌詞歌曲。
        *   Custom Mode 適用於需要精確控制歌詞、風格和結構的進階創作。
3.  **Step 3: 編寫或生成歌詞 (Custom Mode)**
    *   **動作:**
        *   可手動在 Lyrics 區塊寫詞。
        *   點擊魔法棒讓 Suno AI 根據需求生成歌詞。
        *   使用 ChatGPT 等工具輔助生成歌詞（Suno 對英文歌詞生成效果較好）。
        *   在歌詞中使用 `[MetaTag]`（如 `[Intro]`, `[Verse 1]`）定義歌曲結構和唱腔（如 `[Melodic Vocal]`）。
        *   使用括號 `(Alem)` 增加情緒短句。
    *   **目的/注意事項:** MetaTags 有助於 AI 理解歌曲結構和表現方式。Alem 增加歌曲層次。
4.  **Step 4: 設定音樂風格 (Custom Mode)**
    *   **動作:** 在 Style 區塊輸入 Style Tags（如 `R&B`, `Hip Hop`）。
    *   **目的/注意事項:**
        *   可詢問 ChatGPT 某首歌或歌手的風格來獲取靈感。
        *   點擊魔法棒讓 Suno AI 最佳化 Style Tags。
        *   歌詞的內容也會影響 AI 生成的風格走向。
5.  **Step 5: 調整進階選項 (Custom Mode)**
    *   **動作:** 點擊 Advanced Options 展開進階設定。
    *   **目的/注意事項:**
        *   `Exclude Styles`: 排除不想要的樂器或風格。
        *   `Gender`: 設定人聲性別。
        *   `Warmth`: 調整歌曲的「常規」程度，建議設為 50-80 以保持變化性又不失協調。
        *   `Style`: 設定 AI 參考 Style Tags 的比重，0 為依歌詞推算風格，100 為完全參考 Style Tags。
6.  **Step 6: 上傳音檔進行延伸或翻唱 (Upload Audio)**
    *   **動作:** 點選 `Upload Audio` 上傳自己的聲音或旋律檔，然後選擇 `Remix Edit`。
    *   **目的/注意事項:**
        *   `Extend`：用於在不改變調性與風格下，從指定句數後延續歌曲，旋律會不同。
        *   `Cover`：用於保持原有旋律，但更改風格或伴奏。需確保歌詞字數與原旋律對應。
        *   `Audio Influence`：調整 AI 參考上傳音檔的程度，0 為參考較少，100 為完全參考。
7.  **Step 7: 建立與應用人設 (Persona)**
    *   **動作:** 點選 `Persona`，然後點擊 `Create New Persona`。可選擇已生成的歌曲或上傳的音檔作為人設參考。
    *   **目的/注意事項:** 讓 AI 在生成歌曲時參考特定風格或聲線。若要高度相似，`Audio Influence` 建議調高至 80 以上。
8.  **Step 8: 生成並試聽歌曲**
    *   **動作:** 設定完成後，點擊生成按鈕。
    *   **目的/注意事項:** Suno AI 通常會生成兩首歌曲。試聽後可根據結果進行調整。
9.  **Step 9: 分離音軌 (Extract Stems)**
    *   **動作:** 在生成歌曲後，可使用 Extract Stems 功能。
    *   **目的/注意事項:** 需消耗 50 Credit。可將歌曲分解為不同音軌（如人聲、伴奏），方便消音、獨奏或下載進行二次創作。

## Tools

*   Suno AI V5
*   ChatGPT (用於生成歌詞、查詢歌曲風格)

## Best Practices

*   建議建立 Workspace 來整理和管理歌曲專案。
*   歌詞對歌曲的 Flow 和走向影響極大，建議自行撰寫歌詞或仔細編輯 AI 生成的歌詞。
*   精確使用 MetaTag（如 `[Verse]`, `[Chorus]`, `[Melodic Vocal]`）以控制歌曲結構和唱腔。
*   透過在歌詞中使用括號 `(Alem)` 增加情緒短句或感嘆詞，提升歌曲的層次感。
*   當不確定歌曲風格時，可利用 ChatGPT 查詢以獲取靈感。
*   Warmth 參數建議設定在 50-80 之間，可在保持歌曲多樣性的同時避免過於怪異。
*   使用 Cover 功能時，務必確保歌詞字數與原旋律的字數對應。
*   利用 Audio Influence 參數精細調整 AI 參考上傳音檔的程度，以達到期望的效果。
*   若希望歌曲與 Persona 高度相似，將 Audio Influence 調高至 80 以上會更有效。
*   活用 Extract Stems 功能進行音軌分離，便於後製、自行演唱或進行聲音採樣。

## Key Decisions

*   **是否使用簡易模式 (Simple Mode) 或客製化模式 (Custom Mode):** 取決於創作需求，Simple Mode 適合快速生成，Custom Mode 適合精確控制。
*   **是否讓 AI 生成歌詞:** 可利用 Suno AI 或其他工具 (如 ChatGPT) 生成，但建議自行修改以確保品質和風格。
*   **如何應用 MetaTag 和 Style Tags:** MetaTag 用於結構與唱腔，Style Tags 用於風格，精確使用可顯著影響生成結果。
*   **調整 Warmth 和 Style 參數的比重:** Warmth 影響歌曲的常規性，Style 影響 AI 遵循風格標籤的程度，需根據實驗來決定最佳設定。
*   **Extend 或 Cover 的選擇:** Extend 用於在保持調性與風格下延續創意，Cover 用於改編已知旋律，兩者有不同應用場景。
*   **Audio Influence 的設定:** 根據希望 AI 參考上傳音檔的程度來調整。
*   **是否建立 Persona:** 當希望多首歌曲具有一致風格或參考特定聲音時，建立 Persona 會很有幫助。
*   **是否使用 Extract Stems:** 需消耗 Credit，但對於需要分離音軌進行後製或採樣的創作者來說是重要功能。

## Future Research

本影片未提及

## References

*   影片標題：Suno AI 2026 作曲完整教學 | 入門到進階 | AI創作歌曲不僅好聽還可以商用
*   影片網址：https://www.youtube.com/watch?v=Xv_cpCtN4yE
