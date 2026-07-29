# StudyNote User Prompt

**Prompt ID:** Prompt-001  
**Prompt Name:** StudyNote_User_Prompt  
**Version:** v1.0 (Final)  
**Prompt Type:** User Prompt  
**Module:** 02_Prompt_Design / 02_User_Prompts  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final

---

# Purpose

本文件定義 **StudyNote User Prompt**。

User Prompt 負責描述本次任務需求。

AI 身分由：

```
StudyNote_AI_Role_Specification
```

定義。

輸出格式由：

```
StudyNote_Output_Schema
```

定義。

本 Prompt 不重複描述上述內容。

---

# Prompt

請根據提供的 **Transcript.md** 內容，完成一份符合 **StudyNote Output Schema** 的 Study Note。

在整理內容時，請遵循 **StudyNote AI Role Specification** 所定義的角色、知識分析原則、內容篩選規則、寫作風格與品質要求。

請注意以下事項：

1. 理解內容後再整理，不直接摘要逐字稿。
2. 依據主題重新組織內容，而非依照逐字稿順序排列。
3. 保留重要概念、流程、工具、方法與決策。
4. 忽略與主題無關的內容，例如開場白、訂閱提醒、廣告及重複敘述。
5. 不新增影片中未提及的資訊，不推測、不杜撰內容。
6. 嚴格依照 Output Schema 的章節與 Markdown 格式輸出。

---

# Input

輸入內容：

```
Transcript.md
```

內容包含：

- Video Title
- Video URL
- Transcript

---

# Output

輸出文件：

```
Study_Note.md
```

格式：

依照：

```
StudyNote_Output_Schema
```

---

# Dependencies

本 Prompt 依賴以下文件：

```
StudyNote_AI_Role_Specification_v1.0.md

StudyNote_Output_Schema_v1.0.md
```

---

# Expected Behaviour

AI 應：

- 理解內容
- 建立知識架構
- 重組資訊
- 提煉重點
- 產生高品質 Study Note

而不是：

- 翻譯逐字稿
- 縮短逐字稿
- 複製逐字稿

---

# Acceptance Criteria

完成後應符合：

- Markdown 格式正確
- 結構符合 Output Schema
- 重點完整
- 條理清楚
- 易閱讀
- 易搜尋
- 易複習
- 可直接保存於 Obsidian

---

# Related Documents

```
02_Prompt_Design/

00_AI_Roles/
└── StudyNote_AI_Role_Specification_v1.0.md

01_System_Prompts/
└── StudyNote_System_Prompt_v1.0.md

02_User_Prompts/
└── StudyNote_User_Prompt_v1.0.md

03_Output_Schemas/
└── StudyNote_Output_Schema_v1.0.md
```

---

# Version History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | Initial Release | First official version |

---

# Document Status

| Item     | Value                         |
| -------- | ----------------------------- |
| Document | StudyNote User Prompt         |
| Version  | v1.0 (Final)                  |
| Product  | YB Knowledge Factory MVP v0.1 |
| Status   | ✅ Final                       |