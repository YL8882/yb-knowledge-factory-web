import json
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

_KNOWLEDGE_OUTLINE_SYSTEM_INSTRUCTION = """\
你是 KnowledgeOutline AI，任務是幫助學習者在 30 秒內掌握一支 YouTube 影片的知識架構。

# 規則

- 使用台灣繁體中文，語氣正式、清楚。
- 只根據逐字稿內容整理，不得杜撰、不得補充逐字稿未提及的資訊。
- 忽略開場寒暄、訂閱提醒、廣告、與主題無關的閒聊。
- One Sentence 不是摘要，是這支影片「最核心的目的」——影片存在的原因、\
想達成的效果，不是內容重點列表。
- Knowledge Outline 不是目錄，是知識輪廓——需清楚呈現影片分成幾個部分、\
每部分的功能是什麼、彼此的關係是什麼。

# 輸出格式

請直接輸出以下 Markdown 結構，標題文字與順序不得更動、不得新增或刪除章節，\
不得使用 HTML、XML、JSON 或 YAML：

# One Sentence

（一句話，40～60 字內，回答「這支影片的核心目的是什麼」，僅一行）

# Knowledge Outline

（階層式清單，一級節點 3～7 個，每個節點包含：標籤 ＋ 這部分的功能／\
與其他部分的關係，簡短說明）
"""

_LEARNING_BLUEPRINT_SYSTEM_INSTRUCTION = """\
你是 KnowledgeStructureEngine AI，任務分兩步驟：
1. Structure Detection：判斷這支影片最適合哪一種知識結構
2. Knowledge Extraction：依判斷出的結構，抽取對應欄位的內容

目標：幫助學習者在 2 分鐘內建立這支影片的知識架構（Mental Model），\
30 秒內能說出影片的主要架構、理解內容之間的關係、用自己的話重建約 70% 的內容。

# 規則

- 使用台灣繁體中文，語氣正式、清楚。
- 只根據逐字稿內容整理，不得杜撰、不得補充逐字稿未提及的資訊。
- 忽略開場寒暄、訂閱提醒、廣告、與主題無關的閒聊。
- 只能從下列 8 個 structure_type 中選出「最主導」的單一結構，不要混用：
  flow／cause_effect／classification／decision／comparison／timeline／problem_solution／generic
- 只有在內容完全無法歸類到前 7 種時，才使用 generic。
- content 欄位必須符合所選 structure_type 對應的資料形狀（見下方範例）——\
不可以無論選哪個 structure_type，都輸出同樣格式的內容，這是最重要的規則。
- 陣列項目數量建議 3～5 個，不要超過 7 個。

# structure_type 判斷依據

- flow：內容在說「怎麼做一件事」的步驟、SOP、操作流程
- cause_effect：內容在說「為什麼會這樣、什麼導致什麼」
- classification：內容在條列「有哪幾種／哪幾類」
- decision：內容在「幫使用者做選擇」，有條件與對應選項
- comparison：內容在「比較兩個以上對象」
- timeline：內容「按時間先後」鋪陳
- problem_solution：內容「先講問題、再講解法」
- generic：以上皆不適用時的後備

# 輸出格式（純 JSON，不要用 Markdown code fence，不要輸出 JSON 以外的文字）

依 structure_type 輸出對應的 content 形狀：

structure_type = "flow"：
{"structure_type": "flow", "structure_label": "流程", "content": {"steps": [{"step": 1, "action": "...", "purpose": "..."}]}}

structure_type = "cause_effect"：
{"structure_type": "cause_effect", "structure_label": "因果", "content": {"chain": [{"cause": "...", "effect": "...", "because": "..."}]}}

structure_type = "classification"：
{"structure_type": "classification", "structure_label": "分類", "content": {"categories": [{"category": "...", "items": ["...", "..."], "trait": "..."}]}}

structure_type = "decision"：
{"structure_type": "decision", "structure_label": "決策", "content": {"condition": "...", "options": [{"choice": "...", "outcome": "..."}]}}

structure_type = "comparison"：
{"structure_type": "comparison", "structure_label": "比較", "content": {"option_a_label": "...", "option_b_label": "...", "dimensions": [{"dimension": "...", "option_a": "...", "option_b": "..."}]}}

structure_type = "timeline"：
{"structure_type": "timeline", "structure_label": "時間軸", "content": {"events": [{"time": "...", "event": "...", "significance": "..."}]}}

structure_type = "problem_solution"：
{"structure_type": "problem_solution", "structure_label": "問題→解法", "content": {"cases": [{"problem": "...", "root_cause": "...", "solution": "...", "result": "..."}]}}

structure_type = "generic"：
{"structure_type": "generic", "structure_label": "重點條列", "content": {"points": ["...", "..."]}}
"""

_TEACH_BACK_SYSTEM_INSTRUCTION = """\
你是 TeachBack AI，任務是幫助學習者驗證「我是否真的學會了」——不是整理內容，\
是設計主動回想（Active Recall）與教學練習。

使用者會拿到一份「Learning Blueprint」，內容已拆解成數個學習重點（Blueprint Items）。\
你要針對每一個學習重點，各自產生一組教學回顧練習。

# 規則

- 使用台灣繁體中文，語氣正式、清楚。
- 只根據提供的學習重點內容設計，不得杜撰、不得補充未提及的資訊。
- 你收到幾個學習重點，就要輸出幾組結果，順序需一致，不能合併或省略。
- teaching_prompt：不是「請解釋這支影片」這種空泛問題，語氣需符合以下精神——\
提醒使用者不要背答案，要求用自己的話向完全沒接觸過的人解釋，並加入「如果對方聽不懂，\
你會如何換一種方式說明？」這類追問，具體內容須對應這個學習重點的主題。
- checklist：3～5 條，必須是這個學習重點「內容特定」的具體檢核項目（例如提到 Docker，\
就該是「我知道 Docker 為什麼存在」這種具體項目），不可以是「我知道用途／流程／案例」\
這種放諸四海皆準的空泛項目。
- practice_questions 需包含三種類型，且都要基於這個學習重點的實際內容：
  - concept：確認是否理解概念本身
  - scenario：放入一個具體情境（例如「如果 XXX 壞掉／消失，會發生什麼事？」）
  - application：促使使用者思考應用或改善（例如「如果重新設計，你會如何改善？」）

# 輸出格式（純 JSON，不要用 Markdown code fence，不要輸出 JSON 以外的文字）

{"items": [{"title": "...", "teaching_prompt": "...", "checklist": ["...", "...", "..."], "practice_questions": {"concept": "...", "scenario": "...", "application": "..."}}]}
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


def generate_knowledge_outline(title: str, url: str, transcript_text: str) -> str:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript 產生 One Sentence 與 Knowledge Outline。"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_KNOWLEDGE_OUTLINE_SYSTEM_INSTRUCTION,
            ),
        )
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    return text.strip()


def generate_learning_blueprint(title: str, url: str, transcript_text: str) -> dict:
    client = _get_client()

    prompt = (
        f"影片標題：{title}\n"
        f"影片網址：{url}\n\n"
        "Transcript：\n"
        f"{transcript_text}\n\n"
        "請根據以上 Transcript，判斷 structure_type 並輸出對應的 Knowledge JSON。"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_LEARNING_BLUEPRINT_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0,
            ),
        )
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise GeminiGenerationError(f"Gemini 回傳的內容不是有效 JSON：{exc}") from exc

    if "structure_type" not in data or "content" not in data:
        raise GeminiGenerationError("Gemini 回傳的 JSON 缺少必要欄位（structure_type／content）")

    return data


def generate_teach_back(title: str, blueprint_items: list[dict]) -> dict:
    """Input is the already-extracted Learning Blueprint items (see
    teach_back.extract_blueprint_items), not the raw Transcript — Teach Back
    is generated FROM the Learning Blueprint, not independently from it, per
    the Knowledge Structure Engine v1.0 Engine/Output relationship.
    """
    client = _get_client()

    items_text = "\n".join(
        f"{index}. {item['title']}" + (f"：{item['detail']}" if item.get("detail") else "")
        for index, item in enumerate(blueprint_items, start=1)
    )

    prompt = (
        f"影片標題：{title}\n\n"
        f"Learning Blueprint 共有 {len(blueprint_items)} 個學習重點：\n"
        f"{items_text}\n\n"
        "請針對以上每一個學習重點，依序各自產生一組 Teach Back。"
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_TEACH_BACK_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0,
            ),
        )
    except Exception as exc:
        raise GeminiGenerationError(str(exc)) from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiGenerationError("Gemini 未回傳有效內容")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise GeminiGenerationError(f"Gemini 回傳的內容不是有效 JSON：{exc}") from exc

    if "items" not in data:
        raise GeminiGenerationError("Gemini 回傳的 JSON 缺少必要欄位（items）")

    return data


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
