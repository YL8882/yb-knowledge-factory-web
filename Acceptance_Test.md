---
title: Acceptance Test
product: YB Knowledge Lite
version: v2.0
status: Active
purpose: MVP sprint acceptance checklist.
---

# Acceptance Test

## Sprint 1 — Chrome Extension

### Extension

- [x] Extension installed successfully
- [x] Loaded from local project
- [x] No installation errors

### YouTube Integration

- [x] YB Learn button displayed
- [x] Button position correct
- [x] Button clickable

### URL Capture

- [x] Current YouTube URL detected
- [x] Toast notification displayed
- [x] Console output correct
- [x] No JavaScript errors

### Sprint Result

- [x] Sprint 1 completed

---

## Sprint 2 — Backend API

### API Connection

- [x] Backend running
- [x] API reachable
- [x] Extension sends URL successfully
- [x] API returns success response

### Workspace Auto-Open

- [x] Clicking YB Learn opens the Workspace (http://127.0.0.1:8000/) automatically
- [x] Captured YouTube URL pre-filled into the Workspace input
- [x] Pre-fill only — Transcript generation still requires an explicit "加入暫存區" click

### Sprint Result

- [x] Sprint 2 completed

**Test Date:** 2026-08-02
**Test Result:** PASS

**Note:** Backend access log 未顯示於目前終端機，原因為背景已有另一個 Uvicorn Process，實際 API 已成功收到 OPTIONS + POST /api/capture 200 OK，功能正常。

---

## Sprint 3 — Transcript

- [x] Transcript generated
- [x] Transcript displayed
- [x] Error handling completed

### Sprint Result

- [x] Sprint 3 completed

**Test Date:** 2026-08-02
**Test Result:** PASS (verified on an isolated test port — see CHANGELOG for a note on a stray dev-server process on port 8000)

---

## Sprint 4 — Study Note

- [ ] Study Note generated
- [ ] Content quality verified
- [ ] Chapter structure correct

### Sprint Result

- [ ] Sprint 4 completed

---

## Sprint 5 — Markdown Export

- [ ] Markdown generated
- [ ] Download successful
- [ ] Markdown format verified

### Sprint Result

- [ ] Sprint 5 completed

---

# MVP Acceptance

The Lite MVP is complete when:

- [ ] Chrome Extension works
- [ ] Backend API connected
- [ ] Transcript generated
- [ ] Study Note generated
- [ ] Markdown exported
- [ ] End-to-end workflow completed

```text
YouTube
    ↓
YB Learn
    ↓
Transcript
    ↓
Study Note
    ↓
Markdown
```

---

# Definition of Done

A Sprint is complete only if:

- [ ] Feature implemented
- [ ] Manual testing passed
- [ ] No console errors
- [ ] Git commit completed
- [ ] Acceptance Test updated