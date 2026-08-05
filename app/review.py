import json
import re
from pathlib import Path

# extract_blueprint_items() stays in teach_back.py per user decision (Feature
# First, Refactor Later) — main.py already imports teach_back and calls
# teach_back.extract_blueprint_items() directly, no re-export needed here.

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "reviews"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def find_cached_review(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Review Knowledge JSON already
    on disk for this video_id, so callers can reuse it instead of calling
    Gemini again (Persistence — Knowledge_Structure_Engine_v1.0.md §7).
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def load_review(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_cached_review_markdown(video_id: str) -> Path | None:
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.md"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def save_review(video_id: str, title: str, data: dict) -> Path:
    """Persists both the structured Knowledge JSON (source of truth, used to
    re-render the HTML Preview) and the formatted .md (generated once here,
    served directly via FileResponse for download) — same pattern as
    teach_back.save_teach_back() / action_list.save_action_list().
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    json_path = OUTPUT_DIR / f"RV_{safe_title}_{video_id}.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = OUTPUT_DIR / f"RV_{safe_title}_{video_id}.md"
    md_path.write_text(format_review_markdown(title, data), encoding="utf-8")

    return json_path


# Fixed template, mirrors teach_back.py's _REFLECTION_QUESTIONS pattern —
# not Gemini-generated. Deliberately different questions from Teach Back's
# Reflection: this one is backward-looking (assessing recall performance),
# Teach Back's is forward-looking (Next Action). Self Score is a pure UI
# affordance (star/percentage), not persisted — appended as text options in
# the downloadable Markdown since there's no interactivity in a static file.
_REFLECTION_QUESTIONS = [
    "這次測驗中，哪些地方答得出來？",
    "哪些地方完全想不起來？",
    "需要回頭重看哪一段？",
    "這次複習後，記憶有變得更清楚嗎？",
]

_SELF_SCORE_OPTIONS = ["0%", "25%", "50%", "75%", "100%"]


def format_review_markdown(title: str, data: dict) -> str:
    lines = [f"# Review — {title}", ""]

    one_sentence = data.get("one_sentence_recall", {})
    if one_sentence:
        lines.append("## One Sentence Recall")
        lines.append("")
        lines.append(f"**Q：** {one_sentence.get('prompt', '')}")
        lines.append(f"**參考答案：** {one_sentence.get('reference_answer', '')}")
        lines.append("")

    recall_questions = data.get("recall_questions", [])
    if recall_questions:
        lines.append("## Recall Questions")
        lines.append("")
        for index, item in enumerate(recall_questions, start=1):
            lines.append(f"**Q{index}：** {item.get('prompt', '')}")
            lines.append(f"**參考答案：** {item.get('reference_answer', '')}")
            lines.append("")

    workflow_recall = data.get("workflow_recall", {})
    if workflow_recall:
        lines.append("## Workflow Recall")
        lines.append("")
        lines.append(f"**Q：** {workflow_recall.get('prompt', '')}")
        lines.append(f"**參考答案：** {workflow_recall.get('reference_answer', '')}")
        lines.append("")

    blank_filling = data.get("blank_filling", [])
    if blank_filling:
        lines.append("## Blank Filling")
        lines.append("")
        for index, item in enumerate(blank_filling, start=1):
            lines.append(f"{index}. {item.get('prompt', '')}")
            lines.append(f"   **答案：** {item.get('answer', '')}")
        lines.append("")

    lines.append("## Reflection")
    lines.append("")
    for question in _REFLECTION_QUESTIONS:
        lines.append(f"- {question}")
    lines.append("")
    lines.append("**Self Score：** " + " / ".join(_SELF_SCORE_OPTIONS))
    lines.append("")

    return "\n".join(lines).strip() + "\n"
