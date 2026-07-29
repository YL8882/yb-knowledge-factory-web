# Expected Study Note Output

**Document Version:** v1.0 (Final)  
**Document Type:** Golden Output Reference  
**Module:** 02_Prompt_Design / 04_Examples / Example_01_StudyNote  
**Product:** YB Knowledge Factory MVP v0.1  
**Status:** Final  
**Owner:** YB Knowledge Factory

---

# 1. Purpose

本文件定義 **Example_01_StudyNote** 的官方預期輸出（Expected Output）。

此文件作為 Study Note Prompt Pipeline 的 **Golden Output**，用於驗證大型語言模型（LLM）是否產生符合規範的結果。

本文件不代表唯一答案，而是定義輸出品質、內容結構與格式標準。

---

# 2. Objectives

Expected Output 的目的：

- 作為 Prompt 開發基準
- 驗證 Study Note 品質
- 建立 Regression Testing Baseline
- 驗證 Output Schema 是否正確
- 驗證 Prompt Pipeline 是否穩定
- 作為未來版本比較依據

---

# 3. Expected Output Structure

Study Note 應符合正式 Output Schema。

標準章節如下：

```text
Metadata

Executive Summary

Key Takeaways

Detailed Notes

Core Concepts

Workflow

Tools

Best Practices

Key Decisions

Future Research

References
```

不得遺漏主要章節。

---

# 4. Expected Content Quality

Study Note 應符合以下品質要求：

### Completeness

完整涵蓋影片主要內容。

不得遺漏重要概念。

---

### Accuracy

不得產生與影片內容不符的資訊。

不得新增未提及內容。

---

### Readability

內容應易於閱讀。

使用清楚標題與層級。

---

### Logical Organization

內容依主題整理。

避免逐字稿式輸出。

應以知識重組方式呈現。

---

### Practical Value

Study Note 應具有實際學習價值。

應能協助讀者：

- 快速理解影片
- 掌握核心概念
- 延伸後續研究

---

# 5. Expected Markdown Format

Study Note 應採用 Markdown。

例如：

```markdown
# Study Note

## Executive Summary

...

## Key Takeaways

...

## Detailed Notes

...

## Core Concepts

...

## Workflow

...

## Tools

...

## Best Practices

...

## Future Research

...
```

保持一致的標題層級。

---

# 6. Expected Metadata

Study Note 應包含完整 Metadata。

例如：

```yaml
Title:
Source:
Video URL:
Video ID:
Channel:
Language:
Generated Date:
Prompt Version:
Output Schema Version:
```

Metadata 必須完整。

---

# 7. Output Validation

完成後應確認：

- Metadata 完整
- 所有章節存在
- Markdown 格式正確
- 無遺漏重要內容
- 無重複內容
- 無幻覺（Hallucination）
- 無格式錯誤

---

# 8. Comparison Rules

每次 Prompt 執行完成後，應與本文件比較。

比較項目包括：

| Validation Item | Expected |
|-----------------|----------|
| Structure | 一致 |
| Section Order | 一致 |
| Markdown | 正確 |
| Metadata | 完整 |
| Key Concepts | 完整 |
| Workflow | 存在 |
| Tools | 存在（若影片有提及） |
| Future Research | 存在 |

比較重點為內容品質，而非逐字相同。

---

# 9. Acceptance Criteria

Study Note 應符合以下條件：

- 符合 Output Schema
- 符合 AI Role 定義
- 符合 System Instructions
- 符合 Task Prompt
- 保持知識完整性
- 保持結構一致性
- 可直接作為學習筆記使用

---

# 10. Example Output (Abbreviated)

以下為簡化示例：

````markdown
# Study Note

## Metadata

- Title:
- Video URL:
- Video ID:
- Language:
- Generated Date:

---

## Executive Summary

本影片介紹……

---

## Key Takeaways

- 重點一
- 重點二
- 重點三

---

## Detailed Notes

### Topic 1

...

### Topic 2

...

---

## Core Concepts

- Prompt Engineering
- Study Note
- Workflow

---

## Workflow

1.
2.
3.

---

## Tools

- Google AI Studio
- Gemini

---

## Best Practices

- ...

---

## Key Decisions

- ...

---

## Future Research

- ...

---

## References

- YouTube