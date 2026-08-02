---
title: Acceptance Test
product: YB Knowledge Lite
version: v1.0
status: Active
purpose: MVP acceptance checklist.
---

# Acceptance Test

## MVP Workflow

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

The MVP is complete only when the entire workflow succeeds.

---

# Chrome Extension

- [x] YB Learn button appears on YouTube
- [x] Current YouTube URL detected
- [ ] URL sent to Backend
- [ ] Processing status displayed

---

# Backend

- [ ] Receive YouTube URL
- [ ] Generate Transcript
- [ ] Generate Study Note
- [ ] Return result successfully

---

# Workspace

- [ ] Transcript displayed
- [ ] Study Note displayed
- [ ] Markdown exported
- [ ] History updated

---

# Final Acceptance

- [ ] End-to-end workflow completed
- [ ] No manual URL copy required
- [ ] Study Note quality acceptable
- [ ] Developer willing to use every day

---

# Definition of Done

A feature is complete only if:

- [ ] Feature works
- [ ] Manual test passed
- [ ] Existing features unaffected
- [ ] Acceptance checklist updated