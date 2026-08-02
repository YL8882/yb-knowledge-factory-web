---
title: CHANGELOG
product: YB Knowledge Lite
version: v1.0
status: Active
purpose: Development log — issues, root causes, and resolutions.
---

# CHANGELOG

## 2026-08-02 — Workspace 未自動開啟且未帶入網址

### 問題

點擊 YB Learn 後，Workspace 未自動開啟；開啟後也未帶入 YouTube 網址。

### 原因

兩個獨立問題，皆屬測試環境（瀏覽器／Extension 狀態）問題，非程式邏輯錯誤：

1. 開發過程中重新載入 Extension 後，已開啟的 YouTube 分頁裡的 content script 仍握著舊的連線，呼叫 `chrome.runtime.sendMessage()` 時拋出 `Extension context invalidated`，訊息送不到 background service worker。
2. Workspace 分頁的 `app/static/script.js` 被瀏覽器快取成尚未加入網址帶入邏輯的舊版本——即使網址列已經正確帶有 `?url=` 參數，頁面仍執行舊版程式碼而未帶入輸入框。

### 解決方式

- 確認 `extension/background.js`、`extension/content.js`、`app/static/script.js` 的訊息傳遞與帶入邏輯本身正確（實作於 commit `4b071bd`）
- 排除方式：重新載入 Extension 後，需**同時**重新整理已開啟的 YouTube 分頁（清除過期的 content script 連線），並對 Workspace 分頁強制重新整理（略過快取）
- 未額外修改程式碼——排除環境問題後，功能即與原本實作一致

### 驗收結果

使用者按下 YB Learn 後，不需任何手動操作，即可完成：

YouTube → Backend → Workspace 的完整流程（自動開啟分頁 + 自動帶入網址）。
