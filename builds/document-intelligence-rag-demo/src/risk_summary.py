"""
risk_summary.py — deterministic risk and safeguard summary generation.

Phase 5: maps each supported topic to a structured risk record, then
combines that record with extracted evidence to produce a summary.

Functions:
    get_risk_mapping()                                       → full mapping dict
    get_risk_summary_for_topic(topic)                        → risk record dict for one topic
    summarise_evidence_for_topic(topic, evidence_results,    → top-N evidence items for a topic
                                 max_items=3)
    generate_risk_safeguard_summary(topics, evidence_results)→ list of summary item dicts
    get_overall_summary(summary_items)                       → overall counts + note dict
    generate_risk_summary_markdown(summary_items,            → Markdown string
                                   overall_summary)

Each summary item dict contains:
    topic                 — topic string
    risk_title            — short risk title
    risk_description      — one- or two-sentence risk description
    why_it_matters        — why this risk matters
    recommended_safeguards— list of safeguard strings
    suggested_owner       — suggested responsible owner
    evidence_items        — list of top evidence dicts (up to max_items)
    evidence_count        — total evidence snippets found for this topic
    coverage_note         — short note based on evidence_count
"""

# ── Risk mapping ──────────────────────────────────────────────────────────────

_RISK_MAPPING = {
    "learner data": {
        "risk_title": "Learner data entered into AI tools",
        "risk_description": (
            "Staff may accidentally enter identifiable learner information into AI tools, "
            "creating privacy, confidentiality, and data protection risks."
        ),
        "recommended_safeguards": [
            "Do not enter identifiable learner data into AI tools.",
            "Use synthetic or anonymised examples.",
            "Apply data minimisation.",
            "Use approved tools only.",
            "Require human review before use.",
        ],
        "why_it_matters": (
            "Learner information may be personal or sensitive and must be handled "
            "under appropriate organisational controls."
        ),
        "suggested_owner": "Data protection lead / senior manager",
    },
    "safeguarding": {
        "risk_title": "Safeguarding information mishandled through AI tools",
        "risk_description": (
            "Staff may enter safeguarding case details into AI tools or rely on "
            "AI outputs for safeguarding judgement."
        ),
        "recommended_safeguards": [
            "Do not enter safeguarding case details into AI tools.",
            "Escalate concerns to the safeguarding lead.",
            "Keep safeguarding decisions human-led.",
            "Use AI only for generic training or awareness material.",
            "Document escalation routes clearly.",
        ],
        "why_it_matters": (
            "Safeguarding decisions require trained human judgement and formal "
            "organisational procedures."
        ),
        "suggested_owner": "Safeguarding lead",
    },
    "human review": {
        "risk_title": "AI outputs used without human review",
        "risk_description": (
            "Staff may treat AI-generated content as final and use it without checking "
            "accuracy, suitability, fairness, or context."
        ),
        "recommended_safeguards": [
            "Require human review before external use.",
            "Assign a named reviewer.",
            "Check outputs against source material.",
            "Document assumptions and limitations.",
            "Escalate uncertain outputs.",
        ],
        "why_it_matters": (
            "AI outputs can be inaccurate, incomplete, biased, or inappropriate for context."
        ),
        "suggested_owner": "Workflow owner / line manager",
    },
    "approved tools": {
        "risk_title": "Unapproved or personal AI tools used for work",
        "risk_description": (
            "Staff may use personal accounts or unapproved tools, creating privacy, "
            "security, accountability, and retention concerns."
        ),
        "recommended_safeguards": [
            "Define an approved AI tools list.",
            "Avoid personal accounts for work use.",
            "Confirm data settings and retention rules.",
            "Train staff on approved use.",
            "Review tool use periodically.",
        ],
        "why_it_matters": (
            "Tool choice affects privacy, control, data retention, and organisational accountability."
        ),
        "suggested_owner": "Senior manager / IT or data protection lead",
    },
    "accountability": {
        "risk_title": "Unclear accountability for AI-assisted work",
        "risk_description": (
            "Staff may be unsure who is responsible for AI-assisted outputs and decisions."
        ),
        "recommended_safeguards": [
            "Assign a responsible owner.",
            "Document who reviews and approves outputs.",
            "Keep humans accountable for final decisions.",
            "Define escalation routes.",
            "Record limitations and assumptions.",
        ],
        "why_it_matters": (
            "AI does not remove organisational responsibility for decisions, content, or actions."
        ),
        "suggested_owner": "Senior manager / workflow owner",
    },
    "bias": {
        "risk_title": "Biased or unfair AI output",
        "risk_description": (
            "AI outputs may include unfair assumptions, discriminatory wording, or "
            "accessibility issues."
        ),
        "recommended_safeguards": [
            "Review outputs for fairness and accessibility.",
            "Avoid relying on AI for decisions about individuals.",
            "Test outputs with diverse examples.",
            "Escalate sensitive or uncertain use cases.",
            "Keep human accountability.",
        ],
        "why_it_matters": (
            "Unfair outputs can harm learners, staff, clients, or service quality."
        ),
        "suggested_owner": "Equality/compliance lead / manager",
    },
    "hallucination": {
        "risk_title": "Inaccurate or invented AI output",
        "risk_description": (
            "AI tools may generate confident but false, invented, or unsuitable information."
        ),
        "recommended_safeguards": [
            "Verify outputs against source material.",
            "Require human review.",
            "Avoid using AI as a sole source of truth.",
            "Keep records of checks for important outputs.",
            "Do not use AI for final decisions.",
        ],
        "why_it_matters": (
            "Incorrect outputs can cause poor decisions, misinformation, or reputational harm."
        ),
        "suggested_owner": "Workflow owner / quality lead",
    },
    "copyright": {
        "risk_title": "Copyright or intellectual property misuse",
        "risk_description": (
            "Staff may upload copyrighted material without permission or reuse "
            "AI-generated content without checking rights."
        ),
        "recommended_safeguards": [
            "Avoid uploading proprietary or copyrighted material without permission.",
            "Check reuse rights.",
            "Use approved source material.",
            "Attribute sources where needed.",
            "Review generated content before publication.",
        ],
        "why_it_matters": (
            "Copyright and IP issues can create legal, reputational, and commercial risk."
        ),
        "suggested_owner": "Manager / content owner",
    },
    "escalation": {
        "risk_title": "Unclear escalation route for AI-related concerns",
        "risk_description": (
            "Staff may not know what to do when AI outputs are wrong, risky, biased, "
            "or involve sensitive information."
        ),
        "recommended_safeguards": [
            "Define escalation routes.",
            "Train staff on when to ask a manager.",
            "Escalate safeguarding issues to safeguarding lead.",
            "Escalate data concerns to data protection lead.",
            "Record and review incidents.",
        ],
        "why_it_matters": (
            "Clear escalation prevents small mistakes becoming serious governance failures."
        ),
        "suggested_owner": "Senior manager / safeguarding or data lead",
    },
    "data minimisation": {
        "risk_title": "Too much information entered into AI tools",
        "risk_description": (
            "Staff may include unnecessary personal, confidential, or sensitive context in prompts."
        ),
        "recommended_safeguards": [
            "Include only the minimum necessary information.",
            "Remove names and identifiers.",
            "Use generic scenarios.",
            "Avoid confidential details.",
            "Review prompts before submission.",
        ],
        "why_it_matters": (
            "Reducing data input reduces privacy, confidentiality, and misuse risk."
        ),
        "suggested_owner": "Data protection lead / workflow owner",
    },
    "anonymisation": {
        "risk_title": "Information not properly anonymised before AI use",
        "risk_description": (
            "Staff may believe data is anonymous when individuals can still be "
            "identified from context."
        ),
        "recommended_safeguards": [
            "Remove names, identifiers, and unique details.",
            "Use synthetic examples where possible.",
            "Check whether re-identification is possible.",
            "Avoid sensitive context.",
            "Ask the data lead when unsure.",
        ],
        "why_it_matters": (
            "Poor anonymisation can still expose personal or sensitive information."
        ),
        "suggested_owner": "Data protection lead",
    },
    "retention": {
        "risk_title": "AI inputs or outputs retained without control",
        "risk_description": (
            "Prompts, uploaded content, or outputs may be stored longer than expected "
            "by tools or internal systems."
        ),
        "recommended_safeguards": [
            "Check tool retention settings.",
            "Use approved tools.",
            "Avoid entering sensitive information.",
            "Define storage and deletion rules.",
            "Keep only necessary records.",
        ],
        "why_it_matters": (
            "Retention affects privacy, confidentiality, auditability, and organisational control."
        ),
        "suggested_owner": "IT / data protection lead",
    },
    "incident reporting": {
        "risk_title": "AI-related incidents not reported",
        "risk_description": (
            "Staff may fail to report accidental disclosure, unsafe outputs, or policy "
            "breaches involving AI tools."
        ),
        "recommended_safeguards": [
            "Define incident reporting routes.",
            "Report suspected data breaches promptly.",
            "Record AI-related issues.",
            "Review incidents for learning.",
            "Escalate serious concerns immediately.",
        ],
        "why_it_matters": (
            "Timely reporting helps limit harm and improve governance controls."
        ),
        "suggested_owner": "Data protection lead / senior manager",
    },
}

_RESPONSIBLE_USE_TEXT = (
    "This summary is generated by a prototype using deterministic topic and keyword matching. "
    "It is intended to support discussion and review, not to replace legal, safeguarding, HR, "
    "compliance, medical, financial, academic-integrity, or professional advice. "
    "Users should review the full source documents and involve appropriate responsible owners "
    "before acting."
)


# ── Public functions ──────────────────────────────────────────────────────────

def get_risk_mapping() -> dict:
    """Return the full topic → risk record mapping dict."""
    return dict(_RISK_MAPPING)


def get_risk_summary_for_topic(topic: str) -> dict:
    """
    Return the risk record for a topic, or an empty dict if the topic is not supported.

    The returned dict contains: risk_title, risk_description, why_it_matters,
    recommended_safeguards, suggested_owner.
    """
    return dict(_RISK_MAPPING.get(topic.lower(), {}))


def summarise_evidence_for_topic(
    topic: str, evidence_results: list, max_items: int = 3
) -> list:
    """
    Return up to max_items evidence results for a topic, sorted by relevance_count descending.

    evidence_results — list of evidence dicts produced by extract_policy_evidence or
                       extract_evidence_from_documents (must contain a 'topic' key).
    """
    matched = [r for r in evidence_results if r.get("topic") == topic]
    matched_sorted = sorted(matched, key=lambda r: r.get("relevance_count", 0), reverse=True)
    return matched_sorted[:max_items]


def _coverage_note(evidence_count: int) -> str:
    if evidence_count == 0:
        return (
            "No direct evidence found in the selected documents. "
            "Review the full policy set manually."
        )
    elif evidence_count == 1:
        return (
            "Limited evidence found. "
            "Review surrounding document context before acting."
        )
    return (
        "Multiple evidence snippets found. "
        "Review source sections before making decisions."
    )


def generate_risk_safeguard_summary(topics: list, evidence_results: list) -> list:
    """
    Build a structured summary for each topic in topics.

    evidence_results — flat list of evidence dicts; each must contain a 'topic' key.
    Unsupported topics (not in the risk mapping) are silently skipped.

    Returns a list of summary item dicts, one per supported topic.
    """
    items = []
    for topic in topics:
        risk_data = get_risk_summary_for_topic(topic)
        if not risk_data:
            continue
        all_topic_evidence = [r for r in evidence_results if r.get("topic") == topic]
        evidence_count = len(all_topic_evidence)
        evidence_items = summarise_evidence_for_topic(topic, evidence_results)
        items.append({
            "topic": topic,
            "risk_title": risk_data["risk_title"],
            "risk_description": risk_data["risk_description"],
            "why_it_matters": risk_data["why_it_matters"],
            "recommended_safeguards": risk_data["recommended_safeguards"],
            "suggested_owner": risk_data["suggested_owner"],
            "evidence_items": evidence_items,
            "evidence_count": evidence_count,
            "coverage_note": _coverage_note(evidence_count),
        })
    return items


def get_overall_summary(summary_items: list) -> dict:
    """
    Compute overall metrics and a summary note from a list of summary items.

    Returns a dict with: topics_reviewed, topics_with_evidence,
    topics_without_evidence, total_evidence_snippets, overall_note.
    """
    topics_reviewed = len(summary_items)
    topics_with_evidence = sum(1 for item in summary_items if item["evidence_count"] > 0)
    topics_without_evidence = topics_reviewed - topics_with_evidence
    total_evidence_snippets = sum(item["evidence_count"] for item in summary_items)

    if topics_reviewed == 0 or topics_with_evidence == 0:
        overall_note = (
            "No matching evidence was found. "
            "Try broader topics or review the full documents manually."
        )
    elif topics_with_evidence < topics_reviewed:
        overall_note = (
            "Evidence was found for some topics, but gaps remain. "
            "Review topics with no evidence manually."
        )
    else:
        overall_note = (
            "Evidence was found for all selected topics. "
            "Use the snippets as starting points and review full source sections."
        )

    return {
        "topics_reviewed": topics_reviewed,
        "topics_with_evidence": topics_with_evidence,
        "topics_without_evidence": topics_without_evidence,
        "total_evidence_snippets": total_evidence_snippets,
        "overall_note": overall_note,
    }


def generate_risk_summary_markdown(summary_items: list, overall_summary: dict) -> str:
    """
    Generate a Markdown risk and safeguard summary document.

    Includes overall metrics, per-topic sections, and a responsible use disclaimer.
    """
    lines = []
    lines.append("# Risk and Safeguard Summary")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overall Summary")
    lines.append("")
    lines.append(f"- **Topics reviewed:** {overall_summary['topics_reviewed']}")
    lines.append(f"- **Topics with evidence:** {overall_summary['topics_with_evidence']}")
    lines.append(f"- **Topics without evidence:** {overall_summary['topics_without_evidence']}")
    lines.append(f"- **Total evidence snippets:** {overall_summary['total_evidence_snippets']}")
    lines.append("")
    lines.append(overall_summary["overall_note"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Topic Summaries")

    for item in summary_items:
        lines.append("")
        lines.append(f"### {item['risk_title']}")
        lines.append("")
        lines.append(f"**Topic:** {item['topic']}")
        lines.append("")
        lines.append(f"**Risk:** {item['risk_description']}")
        lines.append("")
        lines.append(f"**Why it matters:** {item['why_it_matters']}")
        lines.append("")
        lines.append(f"**Suggested responsible owner:** {item['suggested_owner']}")
        lines.append("")
        lines.append("**Recommended safeguards:**")
        lines.append("")
        for sg in item["recommended_safeguards"]:
            lines.append(f"- {sg}")
        lines.append("")
        snippet_count = len(item["evidence_items"])
        total_count = item["evidence_count"]
        lines.append(
            f"**Evidence found** (showing {snippet_count} of {total_count} snippet(s)):"
        )
        lines.append("")
        if item["evidence_items"]:
            for e in item["evidence_items"]:
                doc = e.get("document_name", "—")
                line_no = e.get("line_number", "—")
                text = e.get("evidence_text", "")
                lines.append(f"- *{doc}*, line {line_no}:")
                lines.append(f"  > {text}")
                lines.append("")
        else:
            lines.append("No direct evidence found in the selected documents.")
            lines.append("")
        lines.append(f"**Coverage note:** {item['coverage_note']}")
        lines.append("")
        lines.append("---")

    lines.append("")
    lines.append("## Responsible Use and Limitations")
    lines.append("")
    lines.append(_RESPONSIBLE_USE_TEXT)
    lines.append("")

    return "\n".join(lines)
