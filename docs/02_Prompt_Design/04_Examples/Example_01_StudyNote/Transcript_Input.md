# Transcript Input

**Document Version:** v1.0 (Final)  
**Document Type:** Example Input  
**Module:** 02_Prompt_Design / 04_Examples / Example_01_StudyNote  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final  
**Owner:** YB Knowledge Factory

---

# 1. Purpose

本文件提供 **Study Note Prompt Pipeline** 的標準輸入範例（Standard Input Example）。

此文件用於：

- Google AI Studio Prompt 測試
- Gemini API 測試
- Claude Code 測試
- FastAPI Workflow
- n8n Workflow
- Regression Testing

本文件同時作為所有 Study Note Workflow 的標準輸入格式。

---

# 2. Input Structure

所有 Transcript Input 必須符合以下結構：

```text
Video Title

Video URL

Video ID

Channel

Duration

Language

Published Date

Transcript
```

所有欄位均應保持固定順序。

---

# 3. Metadata

## Video Title

```text
<Video Title>
```

例如：

```text
Claude Code 完整教學
```

---

## Video URL

```text
https://www.youtube.com/watch?v=xxxxxxxxxxx
```

---

## Video ID

```text
xxxxxxxxxxx
```

---

## Channel

```text
Channel Name
```

---

## Duration

格式：

```text
HH:MM:SS
```

例如：

```text
00:42:18
```

---

## Language

例如：

```text
Traditional Chinese

English

Japanese
```

---

## Published Date

格式：

```text
YYYY-MM-DD
```

例如：

```text
2026-07-18
```

---

# 4. Transcript

Transcript 為 Prompt 的主要輸入。

格式：

```text
00:00

逐字稿內容

00:35

逐字稿內容

01:02

逐字稿內容
```

可保留時間戳。

若無時間戳亦可。

不得修改逐字稿內容。

---

# 5. Example

```markdown
# Transcript

## Video Title

Claude Code 完整教學

---

## Video URL

https://www.youtube.com/watch?v=xxxxxxxxxxx

---

## Video ID

xxxxxxxxxxx

---

## Channel

YB AI

---

## Duration

00:38:15

---

## Language

Traditional Chinese

---

## Published Date

2026-07-18

---

## Transcript

00:00

今天我們介紹 Claude Code...

00:35

Claude Code 最大的特色...

01:18

我們接著介紹...
```

---

# 6. Input Requirements

Transcript 應符合：

- UTF-8 編碼
- Markdown 格式
- 保留原始內容
- 不得摘要
- 不得翻譯
- 不得自行修正內容

若逐字稿有錯字：

保持原樣。

由 AI 後續理解。

---

# 7. Source Rules

Transcript 可來自：

- YouTube
- Podcast
- Web Page
- PDF OCR
- Speech-to-Text

所有來源均應轉換為本標準格式。

---

# 8. Validation Checklist

建立 Transcript Input 前應確認：

- Video Title 存在
- Video URL 正確
- Transcript 不為空
- UTF-8 編碼
- Markdown 格式正確
- Metadata 完整

---

# 9. Dependencies

本文件作為以下模組的輸入：

```text
Transcript_Input.md
        │
        ▼
StudyNote_AI_Role_Specification
        │
        ▼
StudyNote_System_Instructions
        │
        ▼
StudyNote_Task_Prompt
        │
        ▼
StudyNote_Output_Schema
        │
        ▼
Study_Note.md
```

---

# 10. Related Documents

```text
04_Examples/
│
├── README.md
│
└── Example_01_StudyNote/
    ├── Transcript_Input.md
    ├── Prompt_Assembly.md
    ├── Expected_StudyNote_Output.md
    └── Notes.md
```

---

# 11. Success Criteria

Transcript Input 應符合：

- Metadata 完整
- Transcript 完整
- Markdown 正確
- 可直接作為 Prompt Input
- 可供 Workflow 重複使用
- 可供 Regression Test 使用

---

# Document Status

| Item | Value |
|------|-------|
| Document | Transcript Input |
| Version | v1.0 (Final) |
| Product | YB Knowledge Factory MVP v0.1 |
| Status | ✅ Final |