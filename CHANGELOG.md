---
title: CHANGELOG
product: YB Knowledge Lite
version: v1.0
status: Active
purpose: Track added, changed, fixed, and removed functionality per release.
---

# CHANGELOG

## 2026-08-02

### Added
- Chrome Extension：YouTube 影片頁面注入「YB Learn」按鈕
- Backend `POST /api/capture`：接收並驗證 YouTube 網址，回傳成功狀態
- 點擊 YB Learn 後自動開啟 Workspace 並帶入已擷取的網址
- 帶著網址開啟 Workspace 時自動開始下載 Transcript，完成後於頁面內顯示內容並提供下載按鈕
- Transcript 完成後自動產生 Study Note（Title/Summary/Key Points/Important Concepts/Workflow/Action Items/Tags），於頁面顯示並提供下載按鈕

### Changed
- Study Note 產生改用新的精簡結構化格式，取代舊版 Executive Summary/Key Takeaways 等 10 章節格式
- 加入 Queue 重新自動串接 Study Note 產生（Sprint 3 曾暫時移除，Sprint 4 起 Transcript → Study Note 全自動）

### Fixed
- Extension 重新載入後，已開啟分頁的 content script 連線失效（`Extension context invalidated`）導致訊息無法送出
- Workspace 因瀏覽器快取舊版 `script.js`，導致網址未帶入輸入框
- `sendMessage` 失敗時錯誤訊息誤標為「後端連線失敗」，改為獨立標示為「無法自動開啟 Workspace」
