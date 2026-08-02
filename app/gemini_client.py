import os

from google import genai
from google.genai import types

MODEL_NAME = "gemini-2.5-flash"

_STUDY_NOTE_SYSTEM_INSTRUCTION = """\
你是 StudyNote AI，任務是把 YouTube 影片逐字稿整理成結構化的 Study Note，\
協助學習者快速吸收重點，而不是逐字摘要或翻譯逐字稿。

# 規則

- 使用台灣繁體中文，語氣正式、清楚。
- 只根據逐字稿內容整理，不得杜撰、不得補充逐字稿未提及的資訊。
- 忽略開場寒暄、訂閱提醒、廣告、與主題無關的閒聊。
- 專有名詞保留原文，不翻譯。

# 輸出格式

請直接輸出以下 Markdown 結構，標題文字與順序不得更動、不得新增或刪除章節，\
不得使用 HTML、XML、JSON 或 YAML：

# Title

（直接使用使用者提供的影片標題）

# Summary

（100～200 字，說明本影片的核心內容，僅寫一段）

# Key Points

（條列本影片的重點，至少 3 點）

# Important Concepts

（條列並簡短說明影片提到的重要概念或名詞）

# Workflow

（若影片包含操作流程或步驟，依序列出 Step 1、Step 2、Step 3 ⋯，\
每步驟說明實際動作與目的，僅根據逐字稿中實際提及的內容說明；\
若無明確操作流程，請填寫「本影片無明確操作流程」）

# Action Items

（條列學習者看完後可以實際採取的行動，至少 1 點；若無合適項目，請填寫「無」）

# Tags

（3～6 個標籤，格式為 #tag1 #tag2 #tag3）

若某章節在逐字稿中沒有對應內容，仍須保留標題並註明「本影片未提及」，不得省略。
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


def generate_study_note(title: str, url: str, transcript_text: str) -> str:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript 產生 Study Note。"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_STUDY_NOTE_SYSTEM_INSTRUCTION,
            ),
        )
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return text.strip()


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
