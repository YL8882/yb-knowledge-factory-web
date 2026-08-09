import json
import os
import time

from google import genai
from google.genai import types

from observability import cost_metrics, error_metrics

MODEL_NAME = "gemini-2.5-flash"

_STUDY_NOTE_SYSTEM_INSTRUCTION = """\
你是 StudyNote AI，任務是把 YouTube 影片逐字稿整理成結構化的 Study Note，\
協助學習者快速吸收重點，而不是逐字摘要或翻譯逐字稿。

Study Note 是唯一的深度學習成果，必須在這一次輸出中，同時完成摘要、重點、\
脈絡、操作步驟、可執行建議與自我測驗——不會再有其他獨立模組個別產生這些內容。

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

# Flow / 關鍵脈絡

（用純文字箭頭表示這支影片內容的關鍵脈絡，例如「問題 → 原因 → 方法 → 執行 → 結果」，\
只用一行箭頭鏈呈現最主要的一條脈絡，不使用圖表、不使用巢狀結構；\
若影片內容沒有明確的因果或推進脈絡，請填寫「本影片無明確關鍵脈絡」）

# Workflow / 操作步驟

（若影片包含操作流程或步驟，依序列出 Step 1、Step 2、Step 3 ⋯，\
每步驟說明實際動作與目的，僅根據逐字稿中實際提及的內容說明；\
若無明確操作流程，請填寫「本影片無明確操作流程」，不得為了填滿這個章節而虛構步驟）

# Key Takeaways

（條列 3～5 條「今天可執行」的重點提醒，每條須是明確動詞開頭、範圍有限、\
不依賴額外資源即可執行的具體行動，不得是「應用所學」「多加練習」這類空泛建議；\
若逐字稿內容不足以產生具體行動，請填寫「無」）

# Quiz

（3～5 題學習測驗，用於確認使用者是否理解影片核心內容；\
每題格式為「Q：問題」與「A：參考答案」各一行，僅根據逐字稿內容出題，\
不得使用逐字稿未提及的資訊作為正確答案）

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

_KNOWLEDGE_OUTLINE_SYSTEM_INSTRUCTION = """\
你是 KnowledgeOutline AI，任務是幫助學習者在 30 秒內判斷「這支影片在講什麼、\
值不值得花時間深入」——不是產生摘要，也不是產生完整 Study Note。

# 規則

- 使用台灣繁體中文，語氣正式、清楚。
- 只根據逐字稿內容整理，不得杜撰、不得補充逐字稿未提及的資訊。
- 忽略開場寒暄、訂閱提醒、廣告、與主題無關的閒聊。
- 整體輸出必須維持精簡，讓讀者能在約 30 秒內讀完，不得寫成接近 Study Note 篇幅的內容。
- One Sentence 不是摘要，是這支影片「最核心的目的」——影片存在的原因、\
想達成的效果，不是內容重點列表。
- Key Points 是這支影片最重要的 3～5 個重點，簡短條列，不是階層式知識架構、\
不描述各部分之間的關係。
- Suitable For 不是替使用者下「值得看」或「不值得看」的絕對判斷，而是描述\
這支影片**適合什麼需求或學習目標的使用者**繼續深入（例如：適合想了解 XX 基礎概念的人、\
適合已有 XX 經驗、想進一步學習 YY 的人），讓讀者依自己的情境自行判斷。

# 輸出格式

請直接輸出以下 Markdown 結構，標題文字與順序不得更動、不得新增或刪除章節，\
不得使用 HTML、XML、JSON 或 YAML：

# One Sentence

（一句話，40～60 字內，回答「這支影片的核心目的是什麼」，僅一行）

# Key Points

（3～5 個最重要的重點，簡短條列）

# Suitable For

（1～2 句，描述適合什麼需求或學習目標的使用者繼續深入學習這支影片，\
不得使用「值得看」「不值得看」這類絕對判斷用語）
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


def _generate_content(
    *, client, model: str, contents, config, artifact_type: str,
    request_id: str | None, video_id: str | None,
):
    """Shared call point for every Gemini request (Sprint 8.5A Task 2, Cost
    Intelligence): times the call and logs token usage / estimated cost via
    cost_metrics — the single place that touches response.usage_metadata, so
    the 7 generate_*() functions below don't each duplicate the extraction.
    Logging is best-effort (cost_metrics.log_usage never raises); only the
    actual Gemini call itself can raise GeminiGenerationError here, same as
    before this change.
    """
    start = time.monotonic()
    try:
        response = client.models.generate_content(model=model, contents=contents, config=config)
    except Exception as exc:
        # Error Intelligence (Sprint 8.5A Task 4): single interception point
        # for every Gemini call failure, regardless of which of the 7
        # generate_*() functions or which caller triggered it.
        error_metrics.log_error(
            request_id=request_id, video_id=video_id, stage="gemini",
            artifact_type=artifact_type, exception=f"{type(exc).__name__}: {exc}",
        )
        raise GeminiGenerationError(str(exc)) from exc
    processing_time_seconds = round(time.monotonic() - start, 3)

    usage = getattr(response, "usage_metadata", None)
    input_tokens = getattr(usage, "prompt_token_count", None) if usage is not None else None
    output_tokens = None
    if usage is not None:
        # Gemini bills "thinking" tokens at the output rate, so they're
        # folded into output_tokens here rather than tracked separately.
        candidates_tokens = getattr(usage, "candidates_token_count", None) or 0
        thoughts_tokens = getattr(usage, "thoughts_token_count", None) or 0
        output_tokens = candidates_tokens + thoughts_tokens

    cost_metrics.log_usage(
        request_id=request_id,
        video_id=video_id,
        model=model,
        artifact_type=artifact_type,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        processing_time_seconds=processing_time_seconds,
    )

    return response


def generate_study_note(
    title: str, url: str, transcript_text: str,
    *, request_id: str | None = None, video_id: str | None = None,
) -> str:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript 產生 Study Note。"
    )

    response = _generate_content(
        client=client, model=MODEL_NAME, contents=prompt,
        config=types.GenerateContentConfig(system_instruction=_STUDY_NOTE_SYSTEM_INSTRUCTION),
        artifact_type="study_note", request_id=request_id, video_id=video_id,
    )

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return text.strip()


def generate_knowledge_outline(
    title: str, url: str, transcript_text: str,
    *, request_id: str | None = None, video_id: str | None = None,
) -> str:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript 產生 One Sentence 與 Knowledge Outline。"
    )

    response = _generate_content(
        client=client, model=MODEL_NAME, contents=prompt,
        config=types.GenerateContentConfig(system_instruction=_KNOWLEDGE_OUTLINE_SYSTEM_INSTRUCTION),
        artifact_type="knowledge_outline", request_id=request_id, video_id=video_id,
    )

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return text.strip()


def generate_quick_summary(
    title: str, url: str, transcript_text: str,
    *, request_id: str | None = None, video_id: str | None = None,
) -> str:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript，用一句話說明這部影片最重要的核心重點。"
    )

    response = _generate_content(
        client=client, model=MODEL_NAME, contents=prompt,
        config=types.GenerateContentConfig(system_instruction=_QUICK_SUMMARY_SYSTEM_INSTRUCTION),
        artifact_type="quick_summary", request_id=request_id, video_id=video_id,
    )

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return text.strip()
