"""RAG engine — Phase 6: deterministic grounded Q&A.

Generates grounded answers from retrieved FAISS chunks using template-based logic.
No external LLM API calls. All evidence is sourced from retrieved chunks only.
"""

from src.semantic_search import semantic_search

# ── Intent detection maps ──────────────────────────────────────────────────────

_TOPIC_KEYWORDS = {
    "learner data": [
        "learner", "student", "personal data", "learner data",
        "learner name", "identifiable", "pupil", "names into",
    ],
    "safeguarding": [
        "safeguarding", "welfare", "vulnerable", "disclosure",
        "safeguarding concern", "safeguarding information",
    ],
    "human review": [
        "check", "review", "verify", "human", "oversight",
        "before use", "validate",
    ],
    "approved tools": [
        "tool", "chatgpt", "ai tool", "allowed", "approved",
        "authorised", "authorized", "permitted", "which tools",
    ],
    "accountability": [
        "responsible", "accountability", "accountable",
        "responsibility", "who is", "who holds",
    ],
    "bias": ["bias", "biased", "discrimination", "unfair", "prejudice"],
    "hallucination": [
        "false", "inaccurate", "hallucination", "fabricate",
        "made up", "incorrect", "invented", "error",
    ],
    "copyright": ["copyright", "plagiarism", "intellectual property"],
    "escalation": ["escalate", "escalation", "manager", "senior", "report to"],
    "data minimisation": [
        "data minimisation", "minimise", "minimize",
        "only necessary", "minimum data",
    ],
    "anonymisation": ["anonymise", "anonymize", "anonymised", "anonymized", "anonymous"],
    "retention": ["retention", "retain", "how long", "delete data", "keep data"],
    "incident reporting": ["incident", "breach", "data breach", "report incident", "data incident"],
}

# Checked in priority order — first match wins
_QUESTION_TYPE_RULES = [
    ("safeguarding",       ["safeguarding"]),
    ("data_protection",    ["learner data", "data minimisation", "anonymisation", "retention", "incident reporting"]),
    ("output_quality",     ["hallucination", "bias", "human review"]),
    ("approved_use",       ["approved tools"]),
    ("accountability",     ["accountability"]),
    ("incident_response",  ["incident reporting"]),
    ("general_policy",     ["copyright", "escalation"]),
]

_CAUTION_TOPICS = {
    "learner data":       "This question involves learner or personal data.",
    "safeguarding":       "This question involves safeguarding boundaries.",
    "incident reporting": "This question involves a data incident or breach.",
}

_ANSWER_TEMPLATES = {
    "data_protection": (
        "Based on the retrieved synthetic policy evidence, staff should not enter identifiable "
        "learner data or learner names into AI tools. The retrieved chunks point towards using "
        "synthetic or anonymised examples, applying data minimisation, using approved tools, and "
        "requiring human review before outputs are used. Review the cited source chunks before "
        "making any organisational decision."
    ),
    "safeguarding": (
        "Based on the retrieved synthetic policy evidence, safeguarding case details should not "
        "be entered into AI tools. Safeguarding concerns should be escalated to the safeguarding "
        "lead and handled through human-led procedures. AI should not be used to make safeguarding "
        "decisions. Review the cited source chunks and follow the organisation's safeguarding process."
    ),
    "output_quality": (
        "Based on the retrieved synthetic policy evidence, AI-generated outputs should be checked "
        "before use because outputs may be inaccurate, invented, biased, or unsuitable. Staff "
        "should verify outputs against source material, apply human review, and escalate uncertain "
        "or unsafe outputs."
    ),
    "approved_use": (
        "Based on the retrieved synthetic policy evidence, staff should only use tools that have "
        "been explicitly approved by their organisation. Unapproved tools may not meet data "
        "protection or acceptable use requirements. Check the approved tools list and escalate "
        "to a manager if unsure."
    ),
    "accountability": (
        "Based on the retrieved synthetic policy evidence, the member of staff who uses or "
        "submits AI-assisted outputs is accountable for their accuracy and appropriateness. "
        "AI does not remove individual responsibility to review and verify content before use. "
        "Human judgement and sign-off remain required."
    ),
    "incident_response": (
        "Based on the retrieved synthetic policy evidence, data incidents or AI misuse incidents "
        "should be reported promptly to the responsible person or data protection lead. Do not "
        "attempt to resolve a data breach without guidance. Follow the organisation's incident "
        "reporting procedure and document the steps taken."
    ),
    "general_policy": (
        "Based on the retrieved synthetic policy evidence, the retrieved chunks contain relevant "
        "guidance for your query. Review the evidence below carefully and check the full source "
        "documents before acting. Apply human review and escalate uncertain cases to a responsible "
        "owner."
    ),
    "unknown": (
        "Based on the retrieved synthetic policy evidence, the retrieved chunks may contain "
        "relevant context for your query. Review the evidence below and consult the source "
        "documents for more complete guidance. Human review and expert judgement remain required."
    ),
}

_NO_CHUNKS_ANSWER = (
    "No relevant evidence was retrieved from the selected synthetic documents. "
    "Broaden the query, rebuild the index with a different chunk size, or review "
    "the documents manually."
)

_LIMITATIONS = [
    "This answer is generated using deterministic template logic over retrieved synthetic policy chunks.",
    "Retrieved chunks may not include all relevant policy context.",
    "Similarity scores are ranking signals, not confidence scores.",
    "Users should review the full source documents before acting.",
    "Human judgement and responsible owners remain required.",
    (
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice."
    ),
    (
        "Do not use this prototype with real learner data, safeguarding case details, "
        "confidential records, staff HR data, personal data, or regulated information."
    ),
]


# ── Validation ─────────────────────────────────────────────────────────────────

def validate_rag_inputs(question: str, vector_store) -> tuple:
    """Return (is_valid: bool, message: str).

    Checks:
    - question is non-empty
    - vector_store exists, has an index, and has embedded chunks
    """
    if not question or not question.strip():
        return False, "Question is empty. Enter a policy question to continue."
    if not vector_store:
        return (
            False,
            "No vector store found. Build a FAISS index on the Embedding Index Builder page first.",
        )
    if not isinstance(vector_store, dict) or vector_store.get("index") is None:
        return (
            False,
            "Vector store is not ready. Build the FAISS index on the Embedding Index Builder page.",
        )
    if not vector_store.get("embedded_chunks"):
        return False, "Vector store has no embedded chunks. Rebuild the index with embeddings."
    return True, "Inputs are valid."


# ── Intent detection ───────────────────────────────────────────────────────────

def detect_question_intent(question: str) -> dict:
    """Detect policy topics and question type from a question string.

    Uses deterministic keyword matching — no model calls.

    Returns:
        {
            detected_topics: list[str],
            question_type: str,
            needs_caution: bool,
            caution_reason: str,
        }
    """
    q_lower = question.lower()

    detected_topics = []
    for topic, keywords in _TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in q_lower:
                detected_topics.append(topic)
                break

    question_type = "unknown"
    for qt, required_topics in _QUESTION_TYPE_RULES:
        if any(t in detected_topics for t in required_topics):
            question_type = qt
            break

    needs_caution = False
    caution_reason = ""
    for caution_topic, reason in _CAUTION_TOPICS.items():
        if caution_topic in detected_topics:
            needs_caution = True
            caution_reason = reason
            break

    return {
        "detected_topics": detected_topics,
        "question_type": question_type,
        "needs_caution": needs_caution,
        "caution_reason": caution_reason,
    }


# ── Answer generation ──────────────────────────────────────────────────────────

def generate_grounded_answer(
    question: str,
    retrieved_chunks: list,
    intent: dict = None,
) -> str:
    """Return a deterministic grounded answer based on question intent and retrieved chunks.

    Uses a template keyed on question_type. Does not invent evidence.
    Returns a cautious no-results message when no chunks are retrieved.
    """
    if not retrieved_chunks:
        return _NO_CHUNKS_ANSWER

    if intent is None:
        intent = detect_question_intent(question)

    question_type = intent.get("question_type", "unknown")
    return _ANSWER_TEMPLATES.get(question_type, _ANSWER_TEMPLATES["unknown"])


def generate_evidence_summary(retrieved_chunks: list, max_items: int = 5) -> list:
    """Return a list of evidence dicts from the top retrieved chunks.

    Each dict includes: rank, score, document_name, chunk_id,
    chunk_index, evidence_text, source_label.
    """
    summary = []
    for r in retrieved_chunks[:max_items]:
        doc = r.get("document_name", "")
        idx = r.get("chunk_index", 0)
        summary.append({
            "rank": r.get("rank", 0),
            "score": r.get("score", 0.0),
            "document_name": doc,
            "chunk_id": r.get("chunk_id", ""),
            "chunk_index": idx,
            "evidence_text": r.get("text", ""),
            "source_label": r.get("source_label", f"From {doc} · chunk {idx}"),
        })
    return summary


# ── Limitations ────────────────────────────────────────────────────────────────

def get_rag_limitations() -> list:
    """Return the standard list of responsible-use limitations for RAG responses."""
    return list(_LIMITATIONS)


# ── Full response ──────────────────────────────────────────────────────────────

def generate_rag_response(
    question: str,
    vector_store: dict,
    model=None,
    model_name: str = None,
    top_k: int = 5,
) -> dict:
    """Run the full RAG pipeline: validate → detect intent → retrieve → answer.

    Returns:
        {
            question, answer, detected_topics, question_type,
            needs_caution, caution_reason, retrieved_chunks,
            evidence_summary, top_k, model_name, metric, limitations
        }

    Raises ValueError if question is empty or vector_store is not ready.
    """
    valid, msg = validate_rag_inputs(question, vector_store)
    if not valid:
        raise ValueError(msg)

    intent = detect_question_intent(question)

    search_result = semantic_search(
        question,
        vector_store,
        model=model,
        model_name=model_name,
        top_k=top_k,
    )

    retrieved_chunks = search_result.get("results", [])
    answer = generate_grounded_answer(question, retrieved_chunks, intent=intent)
    evidence_summary = generate_evidence_summary(retrieved_chunks, max_items=top_k)

    return {
        "question": question,
        "answer": answer,
        "detected_topics": intent["detected_topics"],
        "question_type": intent["question_type"],
        "needs_caution": intent["needs_caution"],
        "caution_reason": intent["caution_reason"],
        "retrieved_chunks": retrieved_chunks,
        "evidence_summary": evidence_summary,
        "top_k": top_k,
        "model_name": search_result.get("model_name", model_name or ""),
        "metric": vector_store.get("metric", "cosine"),
        "limitations": get_rag_limitations(),
    }


# ── Markdown export ────────────────────────────────────────────────────────────

def generate_rag_markdown(rag_response: dict) -> str:
    """Generate a Markdown string from a RAG response dictionary.

    Sections: Question, Short Answer, Detected Topics, Question Type,
    Retrieved Evidence, Caution Notes (if needed), Limitations and Responsible Use.
    """
    lines = []
    lines.append("# RAG Q&A Response")
    lines.append("")

    lines.append("## Question")
    lines.append(f"> {rag_response.get('question', '')}")
    lines.append("")

    lines.append("## Short Answer")
    lines.append(rag_response.get("answer", ""))
    lines.append("")

    lines.append("## Detected Topics")
    topics = rag_response.get("detected_topics", [])
    if topics:
        for t in topics:
            lines.append(f"- {t}")
    else:
        lines.append("- No specific topics detected.")
    lines.append("")

    lines.append("## Question Type")
    lines.append(f"`{rag_response.get('question_type', 'unknown')}`")
    lines.append("")

    lines.append("## Retrieved Evidence")
    evidence_summary = rag_response.get("evidence_summary", [])
    if evidence_summary:
        for item in evidence_summary:
            lines.append(f"### Rank {item['rank']} · Score: {item['score']:.4f}")
            lines.append(f"**Document:** {item['document_name']}  ")
            lines.append(f"**Chunk ID:** `{item['chunk_id']}`  ")
            lines.append(f"**Chunk Index:** {item['chunk_index']}")
            lines.append("")
            lines.append(item.get("evidence_text", ""))
            lines.append("")
            lines.append(f"*{item.get('source_label', '')}*")
            lines.append("")
    else:
        lines.append("No evidence retrieved.")
        lines.append("")

    if rag_response.get("needs_caution"):
        lines.append("## Caution Notes")
        lines.append(f"> {rag_response.get('caution_reason', '')}")
        lines.append("")

    lines.append("## Limitations and Responsible Use")
    for lim in rag_response.get("limitations", []):
        lines.append(f"- {lim}")
    lines.append("")

    lines.append("---")
    lines.append("*Generated by Semantic RAG Policy Assistant · Prototype · Synthetic documents only.*")

    return "\n".join(lines)
