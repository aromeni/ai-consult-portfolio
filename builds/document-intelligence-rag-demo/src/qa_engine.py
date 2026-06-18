"""
qa_engine.py — deterministic policy Q&A using topic detection and evidence retrieval.

Phase 7: evidence-based Q&A without AI APIs, embeddings, or vector databases.

Functions:
    detect_topics_from_question(question)                              → list[str]
    generate_policy_answer(question, detected_topics,                  → str
                           evidence_results, risk_summary_items)
    get_question_limitations(detected_topics, evidence_results)        → list[str]
    answer_policy_question(question, documents, selected_document=None)→ dict
    generate_qa_markdown(qa_result)                                    → str

qa_result dict keys:
    question            — str
    detected_topics     — list[str]
    answer              — str
    evidence_results    — list[dict]
    safeguards          — list[str] (deduplicated across topics)
    owners              — list[str] (deduplicated across topics)
    limitations         — list[str]
    coverage_note       — str
    risk_summary_items  — list[dict]
"""

from collections import defaultdict

from src.evidence_extractor import extract_policy_evidence, extract_evidence_from_documents
from src.risk_summary import generate_risk_safeguard_summary
from src.brief_generator import deduplicate_list

# ── Question → topic keyword mapping ─────────────────────────────────────────
# Each list contains substrings matched case-insensitively against the question.

_QUESTION_TOPIC_KEYWORDS = {
    "learner data": [
        "learner data", "learner records", "personal data", "student data",
        "learner information", "identifiable learner",
    ],
    "safeguarding": [
        "safeguarding", "safeguard", "welfare", "child protection", "disclosure",
    ],
    "human review": [
        "human review", "review required", "check before", "review before",
        "reviewed by", "ai output", "ai outputs",
    ],
    "approved tools": [
        "approved tools", "approved ai", "permitted tool", "unapproved",
        "personal account", "which ai", "what tools", "which tools",
        "ai tool", "ai tools", "allowed", "prohibited",
    ],
    "accountability": [
        "responsible", "accountability", "accountable", "responsibility",
        "who owns",
    ],
    "bias": [
        "bias", "biased", "unfair", "fairness", "discriminatory",
    ],
    "hallucination": [
        "inaccurate", "incorrect", "invented", "false information",
        "unsafe output", "inaccuracy", "unsafe", "unreliable",
        "seems wrong", "ai-generated", "generated output",
    ],
    "copyright": [
        "copyright", "intellectual property", "ip rights", "reuse rights",
    ],
    "escalation": [
        "escalate", "escalation", "what should", "what do staff",
        "who to inform", "who to tell", "raise a concern",
    ],
    "data minimisation": [
        "data minimisation", "minimum necessary", "minimum data",
        "only necessary", "minimise data",
    ],
    "anonymisation": [
        "anonymise", "anonymisation", "anonymous", "de-identify",
        "remove names", "remove identifiers",
    ],
    "retention": [
        "retention", "how long stored", "how long data",
        "delete data", "data deletion",
    ],
    "incident reporting": [
        "incident report", "data breach", "accidentally enter",
        "accidentally", "sensitive information", "accidental disclosure",
        "breach",
    ],
}

# When a topic is detected directly, automatically add these related topics.
_CO_DETECTION_MAP = {
    "learner data": ["data minimisation", "anonymisation", "approved tools", "human review"],
    "safeguarding": ["escalation", "human review", "accountability"],
    "human review": ["accountability"],
    "hallucination": ["bias", "human review", "escalation", "accountability"],
    "incident reporting": ["learner data", "data minimisation", "escalation"],
    "accountability": ["human review", "escalation"],
}

# ── Deterministic answer templates per topic ──────────────────────────────────

_ANSWER_TEMPLATES = {
    "learner data": (
        "Staff should not enter identifiable learner data into AI tools. "
        "Policies point to using synthetic or anonymised examples, applying data minimisation, "
        "using only approved tools, and requiring human review before any AI-assisted output is used."
    ),
    "safeguarding": (
        "Safeguarding case details should not be entered into AI tools. "
        "Safeguarding concerns should be escalated to the safeguarding lead "
        "and handled through human-led procedures rather than AI-generated judgement."
    ),
    "human review": (
        "AI-generated outputs should be reviewed by a responsible human before use, "
        "especially where outputs affect learners, staff, clients, decisions, "
        "or external communication. Staff remain accountable for any AI-assisted work."
    ),
    "approved tools": (
        "Staff should use only organisation-approved AI tools for work purposes. "
        "Personal accounts or unapproved tools should not be used for work-related tasks. "
        "The approved tools list should be confirmed and kept up to date."
    ),
    "accountability": (
        "Staff remain accountable for any AI-assisted work. "
        "A named responsible owner should be assigned for AI use decisions and outputs. "
        "AI does not remove organisational responsibility for decisions, content, or actions."
    ),
    "bias": (
        "AI outputs should be reviewed for fairness and accessibility before use. "
        "Outputs should not be relied upon for decisions about individuals without human oversight."
    ),
    "hallucination": (
        "Staff should verify AI outputs against source material before use, "
        "as AI tools may generate inaccurate, invented, or unsuitable information. "
        "Outputs should not be used as a sole source of truth."
    ),
    "copyright": (
        "Staff should check copyright and intellectual property rights before uploading "
        "or reusing content with AI tools."
    ),
    "escalation": (
        "Staff should escalate concerns about AI outputs, safeguarding information, "
        "or data issues to the appropriate responsible lead. "
        "Clear escalation routes should be defined and known to all staff."
    ),
    "data minimisation": (
        "Only the minimum necessary information should be included when working with AI tools. "
        "Names and identifiers should be removed where possible."
    ),
    "anonymisation": (
        "Information should be anonymised or de-identified before being used with AI tools. "
        "Check that all identifiers have been removed before submitting prompts."
    ),
    "retention": (
        "Staff should check tool retention settings and ensure sensitive information "
        "is not stored longer than necessary."
    ),
    "incident reporting": (
        "Suspected data breaches, accidental disclosures, or unsafe AI outputs should be "
        "reported promptly through the organisation's incident reporting process."
    ),
}

_NO_TOPICS_ANSWER = (
    "I could not confidently identify the relevant policy topic from the question. "
    "Try asking about learner data, safeguarding, approved tools, human review, "
    "accountability, hallucination, bias, copyright, escalation, retention, "
    "or incident reporting."
)

_NO_EVIDENCE_ANSWER = (
    "I detected relevant policy topics, but the selected document scope did not return "
    "enough direct evidence. Review the full source documents manually or broaden "
    "the document scope."
)


# ── Public functions ──────────────────────────────────────────────────────────

def detect_topics_from_question(question: str) -> list:
    """
    Detect relevant policy topics from a question using keyword matching and co-detection.

    First pass: check each topic's keyword list against the lowercased question.
    Second pass: for each detected topic, add related topics from _CO_DETECTION_MAP.

    Returns a deduplicated list: primary topics first, co-detected topics appended.
    """
    if not question or not question.strip():
        return []

    q_lower = question.lower()
    detected = []

    for topic, keywords in _QUESTION_TOPIC_KEYWORDS.items():
        if any(kw in q_lower for kw in keywords):
            if topic not in detected:
                detected.append(topic)

    extra = []
    for topic in list(detected):
        for related in _CO_DETECTION_MAP.get(topic, []):
            if related not in detected and related not in extra:
                extra.append(related)

    return detected + extra


def generate_policy_answer(
    question: str,
    detected_topics: list,
    evidence_results: list,
    risk_summary_items: list,
) -> str:
    """
    Generate a deterministic policy answer from detected topics and evidence.

    Returns a cautious fallback if no topics were detected.
    Returns a no-evidence fallback if topics were detected but no evidence was found.
    Otherwise builds an answer from topic templates.
    """
    if not detected_topics:
        return _NO_TOPICS_ANSWER

    if not evidence_results:
        return _NO_EVIDENCE_ANSWER

    parts = [
        _ANSWER_TEMPLATES[t]
        for t in detected_topics
        if t in _ANSWER_TEMPLATES
    ]

    if not parts:
        return _NO_TOPICS_ANSWER

    return (
        "Based on the synthetic policy documents:\n\n"
        + " ".join(parts)
        + "\n\nReview the full source sections before acting on this summary."
    )


def get_question_limitations(detected_topics: list, evidence_results: list) -> list:
    """Return a standard list of limitation notes for a Q&A answer."""
    limitations = [
        "This answer is generated by deterministic keyword/topic matching, "
        "not by a legal or safeguarding expert.",
        "Evidence snippets may miss relevant content if the policy uses different wording.",
        "Review the full source sections before acting.",
        "Human judgement and responsible owners remain required.",
        "This prototype does not provide legal, safeguarding, HR, compliance, "
        "medical, financial, academic-integrity, or professional advice.",
    ]
    if not evidence_results:
        limitations.append(
            "No direct evidence was found for the detected topics. "
            "Broaden the document scope or review the full policy set manually."
        )
    return limitations


def answer_policy_question(
    question: str,
    documents: dict,
    selected_document: str | None = None,
) -> dict:
    """
    Generate a full evidence-based policy Q&A result for a question.

    documents         — dict mapping document_name (str) to text content (str)
    selected_document — if set, restrict evidence extraction to this document only

    Returns a dict with:
        question, detected_topics, answer, evidence_results,
        safeguards, owners, limitations, coverage_note, risk_summary_items
    """
    detected_topics = detect_topics_from_question(question)

    evidence_results = []
    if selected_document:
        doc_text = documents.get(selected_document, "")
        for topic in detected_topics:
            evidence_results.extend(
                extract_policy_evidence(doc_text, topic, document_name=selected_document)
            )
    else:
        for topic in detected_topics:
            evidence_results.extend(extract_evidence_from_documents(documents, topic))

    evidence_results = sorted(
        evidence_results, key=lambda r: r.get("relevance_count", 0), reverse=True
    )

    risk_summary_items = generate_risk_safeguard_summary(detected_topics, evidence_results)

    answer = generate_policy_answer(
        question, detected_topics, evidence_results, risk_summary_items
    )

    all_safeguards = []
    all_owners = []
    for item in risk_summary_items:
        all_safeguards.extend(item.get("recommended_safeguards", []))
        owner = item.get("suggested_owner", "")
        if owner:
            all_owners.append(owner)

    safeguards = deduplicate_list(all_safeguards)
    owners = deduplicate_list(all_owners)

    doc_names_with_evidence = {
        e.get("document_name", "")
        for e in evidence_results
        if e.get("document_name")
    }
    if len(doc_names_with_evidence) == 0:
        coverage_note = (
            "No direct evidence found; broaden the search scope or review documents manually."
        )
    elif len(doc_names_with_evidence) == 1:
        coverage_note = (
            "Evidence found in one document only; review related policy documents manually."
        )
    else:
        coverage_note = "Evidence found across multiple documents."

    limitations = get_question_limitations(detected_topics, evidence_results)

    return {
        "question": question,
        "detected_topics": detected_topics,
        "answer": answer,
        "evidence_results": evidence_results,
        "safeguards": safeguards,
        "owners": owners,
        "limitations": limitations,
        "coverage_note": coverage_note,
        "risk_summary_items": risk_summary_items,
    }


def generate_qa_markdown(qa_result: dict) -> str:
    """
    Generate a Markdown document from a Q&A result dict.

    Sections:
        1. Question
        2. Short Answer
        3. Detected Topics
        4. Evidence Found  (capped at 8 items)
        5. Recommended Safeguards
        6. Suggested Responsible Owners
        7. Limitations
    """
    question = qa_result.get("question") or "—"
    answer = qa_result.get("answer") or "—"
    detected_topics = qa_result.get("detected_topics") or []
    evidence_results = qa_result.get("evidence_results") or []
    safeguards = qa_result.get("safeguards") or []
    owners = qa_result.get("owners") or []
    limitations = qa_result.get("limitations") or []

    lines = [
        "# Evidence-Based Policy Q&A",
        "",
        "---",
        "",
        "## Question",
        "",
        question,
        "",
        "---",
        "",
        "## Short Answer",
        "",
        answer,
        "",
        "---",
        "",
        "## Detected Topics",
        "",
    ]

    if detected_topics:
        lines += [f"- {t}" for t in detected_topics]
    else:
        lines.append("*No topics detected.*")

    lines += ["", "---", "", "## Evidence Found", ""]

    if evidence_results:
        for e in evidence_results[:8]:
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
        lines.append("*No evidence found in the selected documents.*")
        lines.append("")

    lines += ["---", "", "## Recommended Safeguards", ""]
    if safeguards:
        lines += [f"- {s}" for s in safeguards]
    else:
        lines.append("*No safeguards identified.*")

    lines += ["", "---", "", "## Suggested Responsible Owners", ""]
    if owners:
        lines += [f"- {o}" for o in owners]
    else:
        lines.append("*No responsible owners identified.*")

    lines += ["", "---", "", "## Limitations", ""]
    if limitations:
        lines += [f"- {lim}" for lim in limitations]
    else:
        lines.append("*No limitations specified.*")

    lines += [
        "",
        "---",
        "",
        "*Generated by BrightPath Document Intelligence Demo (prototype). "
        "All documents are synthetic. This Q&A provides indicative evidence only.*",
    ]

    return "\n".join(lines)
