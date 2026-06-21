"""
Evidence-based answer generation for Build 11.

Produces grounded, cited answers from retrieved chunks only.
Does not invent information not present in retrieved evidence.
If evidence is weak, returns an explicit "insufficient evidence" response.
No external LLM API calls in the default mode.
"""

from __future__ import annotations

INSUFFICIENT_EVIDENCE_THRESHOLD = 0.25
MIN_CHUNKS_FOR_ANSWER = 1

_CONFIDENCE_LABELS = {
    "strong": "Strong",
    "moderate": "Moderate",
    "weak": "Weak",
    "insufficient": "Insufficient",
}


def generate_answer(query: str, results: list[dict]) -> dict:
    """
    Generate a grounded answer from retrieved results.

    Returns a dict with keys:
        answer (str), citations (list[dict]), evidence_used (list[str]),
        confidence (str: "strong"|"moderate"|"weak"|"insufficient"),
        limitations (str), has_evidence (bool).
    """
    if not results:
        return insufficient_evidence_response(query)

    top_score = results[0]["score"]
    if top_score < INSUFFICIENT_EVIDENCE_THRESHOLD:
        return insufficient_evidence_response(query)

    citations = [build_citation(r) for r in results]
    evidence_used = [r["text"] for r in results]

    answer = " ".join(r["text"].strip() for r in results)

    confidence = _derive_confidence(top_score)

    limitations = (
        "This answer is drawn directly from the documents in the library. "
        "It has not been verified by a subject-matter expert. "
        "Always apply professional judgement before acting on any guidance."
    )

    return {
        "answer": answer,
        "citations": citations,
        "evidence_used": evidence_used,
        "confidence": confidence,
        "limitations": limitations,
        "has_evidence": True,
    }


def build_citation(result: dict) -> dict:
    """Build a citation dict from a retrieval result. Includes source, chunk_id, score."""
    return {
        "source_name": result.get("source_name", "Unknown"),
        "chunk_id": result.get("chunk_id", ""),
        "document_id": result.get("document_id", ""),
        "score": result.get("score", 0.0),
        "rank": result.get("rank", 0),
        "excerpt": result.get("text", "")[:200],
    }


def format_answer_for_display(answer_dict: dict) -> str:
    """Format the answer dict as a readable Markdown string for Streamlit."""
    if not answer_dict.get("has_evidence"):
        return (
            f"**Insufficient evidence**\n\n"
            f"{answer_dict.get('answer', '')}\n\n"
            f"*{answer_dict.get('limitations', '')}*"
        )

    confidence_label = _CONFIDENCE_LABELS.get(
        answer_dict.get("confidence", ""), "Unknown"
    )

    lines = [
        f"**Confidence:** {confidence_label}",
        "",
        answer_dict.get("answer", ""),
        "",
        "**Sources**",
    ]

    for i, cit in enumerate(answer_dict.get("citations", []), start=1):
        source = cit.get("source_name", "Unknown")
        chunk = cit.get("chunk_id", "")
        score = cit.get("score", 0.0)
        lines.append(f"{i}. {source} — chunk `{chunk}` (score: {score:.3f})")

    lines += ["", f"*{answer_dict.get('limitations', '')}*"]
    return "\n".join(lines)


def insufficient_evidence_response(query: str) -> dict:
    """Return a standardised insufficient-evidence answer dict."""
    return {
        "answer": (
            "The documents in the library do not contain sufficiently relevant "
            "information to answer this query confidently. "
            "Consider rephrasing your question or uploading additional documents."
        ),
        "citations": [],
        "evidence_used": [],
        "confidence": "insufficient",
        "limitations": (
            "No document in the library scored above the minimum retrieval threshold "
            f"for the query: \"{query}\". No answer has been generated."
        ),
        "has_evidence": False,
    }


def _derive_confidence(top_score: float) -> str:
    if top_score >= 0.7:
        return "strong"
    if top_score >= 0.5:
        return "moderate"
    return "weak"
