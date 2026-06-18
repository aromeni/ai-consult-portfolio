"""
brief_generator.py — generates a Markdown evidence brief from policy evidence and risk data.

Phase 6: complete rewrite with short answer generation, next actions, filename helper.

Functions:
    generate_short_answer(question, topics, evidence_results)  → str
    deduplicate_list(items)                                     → list
    generate_next_actions(topics, evidence_results)             → list[str]
    generate_markdown_brief(brief_data)                         → str
    create_brief_filename(title)                                → str

brief_data keys:
    title               — str
    question            — str
    topics              — list[str]
    documents_reviewed  — list[str]
    generated_date      — str (defaults to today)
    short_answer        — str (generated from topics if absent)
    evidence_results    — list[dict] from extract_policy_evidence / summarise_evidence_for_topic
    risk_summary_items  — list[dict] from generate_risk_safeguard_summary
    next_actions        — list[str]
    reviewer_notes      — list[str]
"""

import re
from collections import defaultdict
from datetime import date as _date

# ── Short answer templates ────────────────────────────────────────────────────

_SHORT_ANSWER_TEMPLATES = {
    "learner data": (
        "Based on the synthetic policy documents, staff should not enter identifiable "
        "learner data into AI tools. Only synthetic, anonymised, or approved non-sensitive "
        "examples should be used, with human review and appropriate data controls."
    ),
    "safeguarding": (
        "Based on the synthetic policy documents, safeguarding case details should not be "
        "entered into AI tools. Safeguarding concerns should be escalated to the safeguarding "
        "lead and remain human-led."
    ),
    "human review": (
        "Based on the synthetic policy documents, AI-generated outputs should be reviewed by "
        "a responsible human before use, especially where outputs affect learners, staff, "
        "clients, decisions, or external communication."
    ),
    "approved tools": (
        "Based on the synthetic policy documents, staff should only use organisation-approved "
        "AI tools for work purposes. Personal accounts or unapproved tools should not be used "
        "for work-related tasks."
    ),
    "accountability": (
        "Based on the synthetic policy documents, staff remain accountable for any "
        "AI-assisted work. A named responsible owner should be assigned for AI use decisions "
        "and outputs."
    ),
    "bias": (
        "Based on the synthetic policy documents, AI outputs should be reviewed for fairness "
        "and accessibility before use. Outputs should not be relied on for decisions about "
        "individuals without human oversight."
    ),
    "hallucination": (
        "Based on the synthetic policy documents, staff should verify AI outputs against "
        "source material before use, as AI tools may generate inaccurate, invented, or "
        "unsuitable information."
    ),
    "copyright": (
        "Based on the synthetic policy documents, staff should check copyright and intellectual "
        "property rights before uploading or reusing content with AI tools."
    ),
    "escalation": (
        "Based on the synthetic policy documents, staff should escalate concerns about AI "
        "outputs, safeguarding information, or data issues to the appropriate responsible lead."
    ),
    "data minimisation": (
        "Based on the synthetic policy documents, only the minimum necessary information "
        "should be included when working with AI tools. Names and identifiers should be "
        "removed where possible."
    ),
    "anonymisation": (
        "Based on the synthetic policy documents, information should be anonymised or "
        "de-identified before being used with AI tools."
    ),
    "retention": (
        "Based on the synthetic policy documents, staff should check tool retention settings "
        "and ensure sensitive information is not stored longer than necessary."
    ),
    "incident reporting": (
        "Based on the synthetic policy documents, suspected data breaches, accidental "
        "disclosures, or unsafe AI outputs should be reported promptly through the "
        "organisation's incident reporting process."
    ),
}

_NO_EVIDENCE_ANSWER = (
    "The selected documents did not provide enough direct evidence for a confident summary. "
    "Review the full documents manually and involve the appropriate responsible owner."
)

# ── Next action templates ─────────────────────────────────────────────────────

_NEXT_ACTIONS_UNIVERSAL = [
    "Review the relevant source policy sections.",
    "Confirm the responsible owner for this issue.",
    "Train staff on the relevant policy boundary.",
    "Use only synthetic or anonymised examples where appropriate.",
    "Require human review before use.",
    "Escalate safeguarding or data protection concerns to the appropriate lead.",
    "Update the AI acceptable-use policy if the evidence reveals a gap.",
]

_NEXT_ACTIONS_BY_TOPIC = {
    "learner data": "Do not enter identifiable learner records or personal data into AI tools.",
    "safeguarding": "Ensure all safeguarding concerns are escalated to the safeguarding lead — not AI tools.",
    "human review": "Assign a named reviewer for AI-generated outputs in this area.",
    "approved tools": "Confirm the approved AI tools list is up to date and communicated to staff.",
    "accountability": "Assign a named responsible owner for AI use in this area.",
    "bias": "Review AI outputs for fairness and accessibility before use.",
    "hallucination": "Verify AI outputs against source material before acting on them.",
    "copyright": "Check copyright and reuse rights before uploading or publishing AI-generated content.",
    "escalation": "Define and document escalation routes for AI-related concerns.",
    "data minimisation": "Review prompts to ensure only minimum necessary information is included.",
    "anonymisation": "Check that all identifiers have been removed before using AI tools.",
    "retention": "Confirm AI tool data retention settings and define a storage and deletion policy.",
    "incident reporting": "Confirm the incident reporting pathway is known to all relevant staff.",
}

# ── Default reviewer notes ────────────────────────────────────────────────────

_REVIEWER_NOTES = [
    "Check whether the evidence snippets are sufficient for the question asked.",
    "Read the surrounding document sections before drawing conclusions.",
    "Confirm whether organisational policy needs updating based on this review.",
    "Confirm whether staff training or escalation routes are required.",
]

# ── Limitations text ──────────────────────────────────────────────────────────

_LIMITATIONS_TEXT = (
    "This brief is generated by a prototype using deterministic keyword, topic, and template "
    "logic. It is intended to support discussion and review, not to replace legal, safeguarding, "
    "HR, compliance, medical, financial, academic-integrity, or professional advice.\n\n"
    "Users should review the full source documents and involve appropriate responsible owners "
    "before acting.\n\n"
    "The tool should not be used with real learner data, safeguarding case details, confidential "
    "client records, staff HR data, personal data, or regulated information unless appropriate "
    "governance, approvals, and controls are in place."
)


# ── Public functions ──────────────────────────────────────────────────────────

def generate_short_answer(question: str, topics: list, evidence_results: list) -> str:
    """
    Return a deterministic short answer based on selected topics.

    Combines short-answer templates for each topic that has a known template.
    If no topics have templates or no evidence was found, returns a cautious fallback.
    """
    if not topics:
        return _NO_EVIDENCE_ANSWER

    parts = [
        _SHORT_ANSWER_TEMPLATES[t]
        for t in topics
        if t in _SHORT_ANSWER_TEMPLATES
    ]

    if not parts:
        return _NO_EVIDENCE_ANSWER

    return " ".join(parts)


def deduplicate_list(items: list) -> list:
    """Return items with duplicates removed, preserving original order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def generate_next_actions(topics: list, evidence_results: list) -> list:
    """
    Return a list of practical next actions based on the selected topics.

    Starts with universal actions, appends topic-specific actions, then deduplicates.
    """
    actions = list(_NEXT_ACTIONS_UNIVERSAL)
    for topic in topics:
        if topic in _NEXT_ACTIONS_BY_TOPIC:
            actions.append(_NEXT_ACTIONS_BY_TOPIC[topic])
    return deduplicate_list(actions)


def generate_markdown_brief(brief_data: dict) -> str:
    """
    Generate a 9-section Markdown evidence brief from brief_data.

    Sections:
        1. Question / Topic
        2. Documents Reviewed
        3. Short Answer
        4. Evidence Found
        5. Key Risks
        6. Recommended Safeguards
        7. Suggested Next Actions
        8. Limitations and Responsible Use
        9. Notes for Reviewer
    """
    today = brief_data.get("generated_date") or _date.today().strftime("%d %B %Y")
    title = brief_data.get("title") or "Policy Evidence Brief"
    question = brief_data.get("question") or "—"
    topics = brief_data.get("topics") or []
    docs_reviewed = brief_data.get("documents_reviewed") or []
    short_answer = brief_data.get("short_answer") or generate_short_answer(
        question, topics, brief_data.get("evidence_results") or []
    )
    evidence_results = brief_data.get("evidence_results") or []
    risk_items = brief_data.get("risk_summary_items") or []
    next_actions = brief_data.get("next_actions") or []
    reviewer_notes = brief_data.get("reviewer_notes") or _REVIEWER_NOTES

    lines = [
        f"# {title}",
        "",
        f"**Generated:** {today}",
        "",
        "---",
        "",
    ]

    # Section 1
    lines += ["## 1. Question / Topic", "", question, "", "---", ""]

    # Section 2
    lines += ["## 2. Documents Reviewed", ""]
    lines += [f"- {d}" for d in docs_reviewed] if docs_reviewed else ["*No documents specified.*"]
    lines += ["", "---", ""]

    # Section 3
    lines += ["## 3. Short Answer", "", short_answer, "", "---", ""]

    # Section 4: Evidence Found (grouped by topic)
    lines += ["## 4. Evidence Found", ""]
    if evidence_results:
        ev_by_topic = defaultdict(list)
        for e in evidence_results:
            ev_by_topic[e.get("topic", "unknown")].append(e)

        for t in topics:
            items = ev_by_topic.get(t, [])
            lines.append(f"### {t.title()} ({len(items)} snippet(s))")
            lines.append("")
            if items:
                for e in items:
                    doc = e.get("document_name", "—")
                    line_no = e.get("line_number", "—")
                    text = e.get("evidence_text", "")
                    kw = e.get("matched_keywords", [])
                    lines.append(f"**{doc}**, line {line_no}:")
                    lines.append(f"> {text}")
                    if kw:
                        lines.append(f"*Matched keywords: {', '.join(kw)}*")
                    lines.append("")
            else:
                lines.append("*No evidence found for this topic in the selected documents.*")
                lines.append("")
    else:
        lines.append("*No evidence was extracted. Review the full documents manually.*")
        lines.append("")
    lines += ["---", ""]

    # Section 5: Key Risks
    lines += ["## 5. Key Risks", ""]
    if risk_items:
        for item in risk_items:
            lines.append(f"### {item.get('risk_title', '—')}")
            lines.append("")
            lines.append(f"**Risk:** {item.get('risk_description', '—')}")
            lines.append("")
            lines.append(f"**Why it matters:** {item.get('why_it_matters', '—')}")
            lines.append("")
            lines.append(f"**Suggested responsible owner:** {item.get('suggested_owner', '—')}")
            lines.append("")
    else:
        lines.append("*No risk data available for the selected topics.*")
        lines.append("")
    lines += ["---", ""]

    # Section 6: Recommended Safeguards (deduplicated across all topics)
    lines += ["## 6. Recommended Safeguards", ""]
    all_safeguards = []
    for item in risk_items:
        all_safeguards.extend(item.get("recommended_safeguards", []))
    deduped = deduplicate_list(all_safeguards)
    if deduped:
        lines += [f"- {s}" for s in deduped]
    else:
        lines.append("*No safeguards specified.*")
    lines += ["", "---", ""]

    # Section 7: Suggested Next Actions
    lines += ["## 7. Suggested Next Actions", ""]
    if next_actions:
        lines += [f"- {a}" for a in next_actions]
    else:
        lines.append("*No next actions specified.*")
    lines += ["", "---", ""]

    # Section 8: Limitations and Responsible Use
    lines += ["## 8. Limitations and Responsible Use", "", _LIMITATIONS_TEXT, "", "---", ""]

    # Section 9: Notes for Reviewer
    lines += ["## 9. Notes for Reviewer", ""]
    lines += [f"- {n}" for n in reviewer_notes]
    lines += [
        "",
        "---",
        "",
        "*Generated by BrightPath Document Intelligence Demo (prototype).  "
        "All documents are synthetic. This brief provides indicative evidence only.*",
    ]

    return "\n".join(lines)


def create_brief_filename(title: str) -> str:
    """
    Create a safe, lowercase Markdown filename from a brief title.

    Non-alphanumeric characters are replaced with hyphens.
    Returns 'document-intelligence-mini-brief.md' if title is empty.
    """
    if not title or not title.strip():
        return "document-intelligence-mini-brief.md"
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{slug}.md" if slug else "document-intelligence-mini-brief.md"
