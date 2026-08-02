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

### Changed
- 加入 Queue 不再自動串接 Study Note 產生，Transcript 完成即為終點（Study Note 改為 Sprint 4 獨立功能）

### Fixed
- Extension 重新載入後，已開啟分頁的 content script 連線失效（`Extension context invalidated`）導致訊息無法送出
- Workspace 因瀏覽器快取舊版 `script.js`，導致網址未帶入輸入框
