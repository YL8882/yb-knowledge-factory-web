import json
import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "teach_backs"

_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def _sanitize_filename(name: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", name).strip()


def find_cached_teach_back(video_id: str) -> Path | None:
    """Processing cache lookup: find an existing Teach Back Knowledge JSON
    already on disk for this video_id, so callers can reuse it instead of
    calling Gemini again (Persistence — Knowledge_Structure_Engine_v1.0.md §7).
    """
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def load_teach_back(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_cached_teach_back_markdown(video_id: str) -> Path | None:
    matches = sorted(
        OUTPUT_DIR.glob(f"*_{video_id}.md"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    return matches[0] if matches else None


def save_teach_back(video_id: str, title: str, data: dict) -> Path:
    """Persists both the structured Knowledge JSON (source of truth, used to
    re-render the HTML Preview) and the formatted .md (generated once here,
    served directly via FileResponse for download — same pattern as
    Transcript/Study Note, avoids building Content-Disposition by hand for a
    dynamically-generated string).
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_title = _sanitize_filename(title)
    json_path = OUTPUT_DIR / f"TB_{safe_title}_{video_id}.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = OUTPUT_DIR / f"TB_{safe_title}_{video_id}.md"
    md_path.write_text(format_teach_back_markdown(title, data), encoding="utf-8")

    return json_path


# Each Learning Blueprint structure_type stores its "teachable points" under a
# different array field with different per-item keys. This maps each
# structure_type's content into a uniform list of {title, detail} — the input
# Gemini needs to generate one Teach Back block per point. flow/cause_effect/
# classification/timeline/problem_solution naturally have several parallel
# points (one per array item); decision/comparison are treated as a single
# teachable point each (breaking a decision's options, or a comparison's
# dimensions, into separate Teach Back blocks would fragment a single idea).
def extract_blueprint_items(structure_type: str, content: dict) -> list[dict]:
    if structure_type == "flow":
        return [
            {"title": step.get("action", ""), "detail": step.get("purpose", "")}
            for step in content.get("steps", [])
        ]
    if structure_type == "cause_effect":
        return [
            {
                "title": link.get("effect", ""),
                "detail": f"{link.get('cause', '')} → {link.get('effect', '')}（{link.get('because', '')}）",
            }
            for link in content.get("chain", [])
        ]
    if structure_type == "classification":
        return [
            {"title": cat.get("category", ""), "detail": "、".join(cat.get("items", []))}
            for cat in content.get("categories", [])
        ]
    if structure_type == "decision":
        options_text = "；".join(
            f"{opt.get('choice', '')} → {opt.get('outcome', '')}" for opt in content.get("options", [])
        )
        return [{"title": content.get("condition", "決策"), "detail": options_text}]
    if structure_type == "comparison":
        dims_text = "；".join(
            f"{dim.get('dimension', '')}：{dim.get('option_a', '')} vs {dim.get('option_b', '')}"
            for dim in content.get("dimensions", [])
        )
        label = f"{content.get('option_a_label', 'A')} vs {content.get('option_b_label', 'B')}"
        return [{"title": label, "detail": dims_text}]
    if structure_type == "timeline":
        return [
            {"title": event.get("event", ""), "detail": f"{event.get('time', '')}：{event.get('significance', '')}"}
            for event in content.get("events", [])
        ]
    if structure_type == "problem_solution":
        return [
            {
                "title": case.get("problem", ""),
                "detail": f"原因：{case.get('root_cause', '')}；解法：{case.get('solution', '')}；結果：{case.get('result', '')}",
            }
            for case in content.get("cases", [])
        ]
    # generic fallback
    return [{"title": point, "detail": ""} for point in content.get("points", [])]


_REFLECTION_QUESTIONS = [
    "今天最大的收穫？",
    "哪裡還不理解？",
    "下一步準備做什麼？",
    "什麼時候會再次使用？",
]


def format_teach_back_markdown(title: str, data: dict) -> str:
    """Formats the persisted Teach Back JSON into the downloadable .md file.
    Reflection is a fixed template (not Gemini-generated — see
    _REFLECTION_QUESTIONS), appended identically to every Blueprint block.
    """
    lines = [f"# Teach Back — {title}", ""]
    items = data.get("items", [])
    for index, item in enumerate(items, start=1):
        lines.append("---")
        lines.append("")
        lines.append(f"## Blueprint {index}: {item.get('title', '')}")
        lines.append("")
        lines.append("### Explain in Your Own Words")
        lines.append("")
        lines.append(item.get("teaching_prompt", ""))
        lines.append("")
        lines.append("### Self Check Checklist")
        lines.append("")
        for check in item.get("checklist", []):
            lines.append(f"- [ ] {check}")
        lines.append("")
        lines.append("### Practice Questions")
        lines.append("")
        questions = item.get("practice_questions", {})
        lines.append(f"**Concept：** {questions.get('concept', '')}")
        lines.append("")
        lines.append(f"**Scenario：** {questions.get('scenario', '')}")
        lines.append("")
        lines.append(f"**Application：** {questions.get('application', '')}")
        lines.append("")
        lines.append("### Reflection")
        lines.append("")
        for question in _REFLECTION_QUESTIONS:
            lines.append(f"- {question}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
