"""
evidence_extractor.py — topic-based evidence extraction from policy documents.

Phase 4: 13 topics, helper functions, extract_evidence_from_documents.

Functions:
    get_supported_topics()                                           → list of topic strings
    get_topic_keywords(topic)                                        → list of keyword strings
    get_topic_description(topic)                                     → short explanation string
    extract_sentences_with_keywords(text, keywords)                  → list of matching sentences
    extract_policy_evidence(text, topic, document_name="")           → list of evidence dicts
    extract_evidence_from_documents(documents, topic)                → list of evidence dicts across docs

Each evidence dict contains:
    topic            — the topic string
    document_name    — source document name (empty string if not provided)
    line_number      — 1-based line number
    evidence_text    — the matched line (stripped)
    matched_keywords — list of keywords that matched
    relevance_count  — total keyword occurrences in the line (higher = more relevant)
"""

import re

# Keyword lists for each supported topic.
# All keywords are lowercase substrings matched case-insensitively against document lines.
TOPIC_KEYWORDS = {
    "learner data": [
        "learner data",
        "learner records",
        "learner information",
        "identifiable learner",
        "personal data",
        "student data",
        "learner contact",
        "attendance record",
        "assessment grade",
    ],
    "safeguarding": [
        "safeguarding",
        "safeguarding case",
        "safeguarding concern",
        "safeguarding lead",
        "child protection",
        "vulnerable learner",
        "safeguard",
        "vulnerable",
        "disclosure",
        "welfare",
        "designated safeguarding",
        "dsl",
    ],
    "human review": [
        "human review",
        "human oversight",
        "reviewed by staff",
        "reviewed by a tutor",
        "manager review",
        "human-led",
        "final decision",
        "reviewed by",
        "staff review",
        "checked by",
        "not rely solely",
        "before use",
        "before sharing",
        "accountable for",
    ],
    "approved tools": [
        "approved tools",
        "approved ai tools",
        "authorised tools",
        "personal accounts",
        "organisation-approved",
        "approved tool",
        "approved ai",
        "approved platform",
        "approved account",
        "permitted tool",
        "list of approved",
    ],
    "accountability": [
        "accountability",
        "accountable",
        "responsible owner",
        "decision owner",
        "staff remain responsible",
        "human accountability",
        "responsible",
        "responsibility",
        "policy owner",
        "compliance",
    ],
    "bias": [
        "bias",
        "biased",
        "fairness",
        "fair",
        "discriminatory",
        "unfair assumptions",
        "accessibility",
        "discriminat",
        "stereotyp",
        "representation",
    ],
    "hallucination": [
        "hallucination",
        "hallucinate",
        "inaccurate output",
        "invented",
        "false information",
        "verify outputs",
        "inaccurate",
        "incorrect output",
        "fabricat",
        "made up",
        "not exist",
        "unverified",
    ],
    "copyright": [
        "copyright",
        "intellectual property",
        "licensed material",
        "ownership",
        "reuse rights",
        "intellectual-property",
        "ip rights",
        "plagiarism",
        "reproduce",
        "protected work",
    ],
    "escalation": [
        "escalation",
        "escalate",
        "safeguarding lead",
        "data protection lead",
        "report to",
        "raise with",
        "inform your manager",
        "designated lead",
        "concern",
        "incident report",
        "notify",
        "escalat",
        "manager",
    ],
    "data minimisation": [
        "data minimisation",
        "minimum necessary",
        "minimise data",
        "only include necessary",
        "minimum data",
        "only necessary",
    ],
    "anonymisation": [
        "anonymised",
        "anonymisation",
        "remove names",
        "remove identifiers",
        "synthetic",
        "anonymise",
        "de-identified",
    ],
    "retention": [
        "retention",
        "data retention",
        "storage period",
        "keep records",
        "stored",
        "delete",
        "purge",
        "how long",
    ],
    "incident reporting": [
        "incident reporting",
        "incident report",
        "data breach",
        "reporting procedure",
        "incident",
        "breach",
        "report",
        "notify",
    ],
}

# Short explanations shown in the Evidence Extraction UI when a topic is selected.
_TOPIC_DESCRIPTIONS = {
    "learner data": (
        "Finding policy rules about learner records, personal data handling, "
        "and what information must not be entered into AI tools."
    ),
    "safeguarding": (
        "Finding policy rules about safeguarding case information, escalation routes, "
        "and boundaries around AI use in safeguarding contexts."
    ),
    "human review": (
        "Finding requirements for staff to review AI outputs before acting on them, "
        "and where human judgement must not be replaced by AI."
    ),
    "approved tools": (
        "Finding rules about which AI tools are permitted for work use "
        "and what staff must not use without approval."
    ),
    "accountability": (
        "Finding who is responsible for AI use decisions and where accountability rests "
        "when AI is involved in a process."
    ),
    "bias": (
        "Finding policy statements about fairness, avoiding bias in AI outputs, "
        "and accessibility considerations."
    ),
    "hallucination": (
        "Finding rules about verifying AI outputs, and acknowledging that AI can produce "
        "inaccurate or invented information."
    ),
    "copyright": (
        "Finding policy on intellectual property, copyright, "
        "and the reuse of AI-generated or AI-assisted content."
    ),
    "escalation": (
        "Finding defined routes for raising concerns about AI use, data breaches, "
        "and safeguarding matters."
    ),
    "data minimisation": (
        "Finding rules about using only the minimum necessary data when working with AI tools."
    ),
    "anonymisation": (
        "Finding requirements to anonymise or de-identify information before it is used with AI tools."
    ),
    "retention": (
        "Finding policy on how long data should be stored, when it should be deleted, "
        "and storage period limits."
    ),
    "incident reporting": (
        "Finding the process for reporting data breaches, policy breaches, "
        "or AI-related incidents to the appropriate lead."
    ),
}


def get_supported_topics() -> list:
    """Return the list of all supported topic names in the order they appear in TOPIC_KEYWORDS."""
    return list(TOPIC_KEYWORDS.keys())


def get_topic_keywords(topic: str) -> list:
    """Return the keyword list for a topic, or an empty list if the topic is not supported."""
    return TOPIC_KEYWORDS.get(topic.lower(), [])


def get_topic_description(topic: str) -> str:
    """Return a short explanation of what the topic is useful for finding."""
    return _TOPIC_DESCRIPTIONS.get(topic.lower(), "")


def extract_sentences_with_keywords(text: str, keywords: list) -> list:
    """
    Return sentences from text that contain any of the given keywords.

    Sentences are split on sentence-ending punctuation followed by whitespace.
    Matching is case-insensitive. Returns an empty list if keywords is empty or text is empty.
    """
    if not keywords:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", text or "")
    kw_lower = [k.lower() for k in keywords]
    results = []
    for sentence in sentences:
        if any(kw in sentence.lower() for kw in kw_lower):
            cleaned = sentence.strip()
            if cleaned:
                results.append(cleaned)
    return results


def extract_policy_evidence(text: str, topic: str, document_name: str = "") -> list:
    """
    Extract lines from text that are relevant to the given topic.

    Uses TOPIC_KEYWORDS for matching (case-insensitive).
    Unsupported or unknown topics return an empty list.
    Results are deduplicated and sorted by relevance_count descending.

    Each result dict contains:
        topic            — the topic string
        document_name    — the document_name argument (empty string if not provided)
        line_number      — 1-based line number
        evidence_text    — the matched line (stripped)
        matched_keywords — list of keywords that matched
        relevance_count  — total keyword occurrences in the line (higher = more relevant)
    """
    keywords = TOPIC_KEYWORDS.get(topic.lower(), [])
    if not keywords:
        return []

    seen = set()
    results = []

    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped in seen:
            continue
        line_lower = stripped.lower()
        matched = [kw for kw in keywords if kw in line_lower]
        if matched:
            seen.add(stripped)
            relevance_count = sum(line_lower.count(kw) for kw in matched)
            results.append({
                "topic": topic,
                "document_name": document_name,
                "line_number": i,
                "evidence_text": stripped,
                "matched_keywords": matched,
                "relevance_count": relevance_count,
            })

    return sorted(results, key=lambda r: r["relevance_count"], reverse=True)


def extract_evidence_from_documents(documents: dict, topic: str) -> list:
    """
    Extract evidence for a topic across multiple documents.

    documents — dict mapping document name (str) to text content (str)

    Returns a flat list of result dicts (same structure as extract_policy_evidence),
    sorted by relevance_count descending so the most relevant snippets appear first.
    """
    results = []
    for doc_name, text in documents.items():
        results.extend(extract_policy_evidence(text, topic, document_name=doc_name))
    return sorted(results, key=lambda r: r["relevance_count"], reverse=True)
