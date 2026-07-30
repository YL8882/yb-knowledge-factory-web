import os
import re

from google import genai
from google.genai import types

_TAGS_LINE_PATTERN = re.compile(r"^Tags:\s*(.*)$", re.IGNORECASE)

MODEL_NAME = "gemini-2.5-flash"

_SYSTEM_INSTRUCTION = """\
你是 StudyNote AI，一位知識分析師（Knowledge Analyst）。

你的任務是將 YouTube 影片逐字稿轉換為高品質、具知識結構的 Study Note，\
而不是逐字翻譯逐字稿，也不是單純摘要逐字稿。

# 核心原則

- Knowledge > Information：整理知識，而非資訊。
- Understanding > Summarizing：先理解內容，再整理，而不是直接摘要。
- Organization > Compression：重新組織內容使其易於理解，而不是只是縮短。
- Learning > Reading：協助使用者學習，而不僅是閱讀。

# 處理流程

Read Transcript → Understand Context → Identify Concepts → Group Related Ideas
→ Extract Knowledge → Organize Structure → Generate Study Note

禁止依照逐字稿原始順序整理內容，應依主題重新組織。

# 內容篩選

應忽略：開場寒暄、自我介紹、訂閱提醒、按讚分享、廣告、贊助內容、重複敘述、\
與主題無關的閒聊、無實際知識價值的內容。

# 寫作規範

- 使用台灣繁體中文。
- 採正式、自然、清楚的語氣。
- 優先使用條列式整理重點。
- 長段落適度拆分。
- 使用明確標題。
- 專有名詞保留原文，不翻譯（例如 Claude Code、Google AI Studio、FastAPI、\
Gemini、Whisper、Prompt、Workflow、Agent、RAG）。

# 嚴格禁止

- 杜撰內容、編造案例。
- 猜測作者意圖或加入個人觀點。
- 補充逐字稿未提及的資訊。
- 若資訊不足，應如實呈現，不得自行推論或編造。

# 輸出格式

第一行必須是 Tags 行，格式為：

Tags: #tag1 #tag2 #tag3

3～6 個標籤，反映影片的關鍵字與主題，可使用繁體中文或專有名詞，\
單一標籤內不得包含空白。Tags 行之後空一行，接著依照以下 Markdown \
章節結構輸出，標題名稱、順序、層級皆不得更動，不得新增或刪除章節，\
不得使用 HTML、XML、JSON 或 YAML 作為主要輸出格式：

## Executive Summary

以 100 字以內（繁體中文字數）說明本影片最重要的核心內容，僅寫一段，\
不分點、不超過 100 字。

## Key Takeaways

## Detailed Notes

依主題整理，若內容包含多個主題，請使用「### 主題名稱」子標題分段呈現；\
若僅有單一主題，可省略子標題直接條列重點。

## Core Concepts

## Workflow

若影片包含操作流程或步驟，請依序列出（可使用 Step 1、Step 2 ⋯）；\
若無明確操作流程，請填寫「本影片無明確操作流程」。

## Tools

## Best Practices

## Key Decisions

## Future Research

## References

上述即為完整章節清單，Tags 僅於文件最前方輸出一次，不得在章節中重複輸出。

若某章節在逐字稿中沒有對應內容，仍須保留該標題，並註明「本影片未提及」，\
不得省略任何章節。請直接從 Tags 行開始輸出，不要輸出最上層標題或 \
Metadata 區塊（Title / Source / Author / Date / Language / Version）。

# References 章節規則

使用者會在提示中提供「影片標題」與「影片網址」，這屬於已知的來源資訊，\
並非逐字稿內容的推測或杜撰。References 章節至少必須包含這兩項來源資訊，\
不得因為逐字稿本身沒有提及而省略或標註「本影片未提及」。
"""

_QUICK_SUMMARY_SYSTEM_INSTRUCTION = """\
你是 StudyNote AI。請用台灣繁體中文，以一句話（100 字以內、僅一段、不分點）\
說明這部影片最重要的核心重點，讓讀者能快速了解影片大意。

只根據使用者提供的影片標題與逐字稿內容作答，不得杜撰、不得補充未提及的資訊。

只輸出這一句話，不要輸出標題、章節名稱、標點以外的其他格式。
"""

_client: genai.Client | None = None


class GeminiConfigError(Exception):
    pass


class GeminiGenerationError(Exception):
    pass


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise GeminiConfigError("缺少 GEMINI_API_KEY 環境變數，請先設定後再試")
        _client = genai.Client(api_key=api_key)
    return _client


def generate_study_note_body(title: str, url: str, transcript_text: str) -> dict:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript 產生 Study Note 內容。"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM_INSTRUCTION,
            ),
        )
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return _split_tags_and_body(text.strip())


def generate_quick_summary(title: str, url: str, transcript_text: str) -> str:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript，用一句話說明這部影片最重要的核心重點。"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_QUICK_SUMMARY_SYSTEM_INSTRUCTION,
            ),
        )
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return text.strip()


def _split_tags_and_body(text: str) -> dict:
    lines = text.splitlines()

    tags = ""
    body_start = 0
    if lines:
        match = _TAGS_LINE_PATTERN.match(lines[0].strip())
        if match:
            tags = match.group(1).strip()
            body_start = 1
            while body_start < len(lines) and not lines[body_start].strip():
                body_start += 1

    body = "\n".join(lines[body_start:]).strip()
    return {"tags": tags, "body": body}
