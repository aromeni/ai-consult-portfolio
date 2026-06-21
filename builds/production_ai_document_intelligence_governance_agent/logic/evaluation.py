"""
Retrieval evaluation helpers for Build 11.

Provides basic evaluation metrics: retrieval coverage, groundedness checklist,
risk flag summary, and manual evaluation form data handling.
"""

from __future__ import annotations

from datetime import datetime

_RISK_LEVEL_ORDER = {"High": 3, "Medium": 2, "Low": 1}


def retrieval_coverage(results: list[dict], top_k: int = 5) -> dict:
    """
    Return retrieval coverage metrics.

    Includes: result_count (int), top_score (float), avg_score (float),
    unique_sources (int), coverage_grade (str).
    """
    if not results:
        return {
            "result_count": 0,
            "top_score": 0.0,
            "avg_score": 0.0,
            "unique_sources": 0,
            "coverage_grade": "Poor",
        }
    scores = [r["score"] for r in results]
    top_score = scores[0]
    avg_score = sum(scores) / len(scores)
    unique_sources = len({r.get("source_name", "") for r in results})
    return {
        "result_count": len(results),
        "top_score": top_score,
        "avg_score": round(avg_score, 4),
        "unique_sources": unique_sources,
        "coverage_grade": _coverage_grade(top_score, len(results), top_k),
    }


def groundedness_checklist(answer_dict: dict, results: list[dict]) -> list[dict]:
    """
    Return a checklist of groundedness criteria.

    Each item: criterion (str), passed (bool), note (str).
    """
    has_evidence = answer_dict.get("has_evidence", False)
    citations = answer_dict.get("citations", [])
    confidence = answer_dict.get("confidence", "insufficient")
    unique_cited_sources = len({c.get("source_name") for c in citations})

    return [
        {
            "criterion": "Evidence retrieved above threshold",
            "passed": has_evidence,
            "note": (
                "At least one chunk was retrieved above the minimum confidence threshold."
                if has_evidence
                else "No evidence retrieved above threshold."
            ),
        },
        {
            "criterion": "Answer grounded in retrieved text",
            "passed": has_evidence and len(citations) > 0,
            "note": (
                "Answer is drawn directly from retrieved document chunks."
                if (has_evidence and citations)
                else "No grounded citations available."
            ),
        },
        {
            "criterion": "Citations provided",
            "passed": len(citations) > 0,
            "note": (
                f"{len(citations)} citation(s) included."
                if citations
                else "No citations included."
            ),
        },
        {
            "criterion": "Confidence above weak threshold",
            "passed": confidence in ("strong", "moderate"),
            "note": f"Confidence level: {confidence}.",
        },
        {
            "criterion": "Multiple sources consulted",
            "passed": unique_cited_sources > 1,
            "note": f"{unique_cited_sources} unique source(s) cited.",
        },
    ]


def risk_summary(risk_flags: list[dict]) -> dict:
    """Return a risk summary dict from a list of governance flags."""
    if not risk_flags:
        return {
            "total_flags": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "highest_risk_level": "None",
            "categories": [],
        }
    highest = max(
        risk_flags, key=lambda f: _RISK_LEVEL_ORDER.get(f.get("risk_level", ""), 0)
    )["risk_level"]
    return {
        "total_flags": len(risk_flags),
        "high_count": sum(1 for f in risk_flags if f.get("risk_level") == "High"),
        "medium_count": sum(1 for f in risk_flags if f.get("risk_level") == "Medium"),
        "low_count": sum(1 for f in risk_flags if f.get("risk_level") == "Low"),
        "highest_risk_level": highest,
        "categories": [f.get("category", "") for f in risk_flags],
    }


def record_manual_evaluation(
    query: str,
    relevance_rating: int,
    answer_grounded: bool,
    citations_useful: bool,
    missing_content: str,
) -> dict:
    """
    Record and return a manual evaluation entry dict.

    Stores: query, relevance_rating (1-5), answer_grounded (bool),
    citations_useful (bool), missing_content (str), timestamp (str).
    """
    return {
        "query": query,
        "relevance_rating": relevance_rating,
        "answer_grounded": answer_grounded,
        "citations_useful": citations_useful,
        "missing_content": missing_content,
        "timestamp": datetime.now().isoformat(),
    }


def evaluation_summary(
    documents: list[dict],
    chunks: list[dict],
    index_dim: int,
    risk_flags: list[dict],
) -> dict:
    """
    Return a summary dict for the Evaluation Dashboard page.

    Includes: doc_count, chunk_count, embedding_dim, risk_flag_count, risk_levels.
    """
    risk_levels = sorted(
        {f.get("risk_level", "") for f in risk_flags},
        key=lambda lvl: _RISK_LEVEL_ORDER.get(lvl, 0),
        reverse=True,
    )
    return {
        "doc_count": len(documents),
        "chunk_count": len(chunks),
        "embedding_dim": index_dim,
        "risk_flag_count": len(risk_flags),
        "risk_levels": risk_levels,
    }


def _coverage_grade(top_score: float, result_count: int, top_k: int) -> str:
    if top_score >= 0.7 and result_count >= min(3, top_k):
        return "Good"
    if top_score >= 0.5:
        return "Moderate"
    if top_score >= 0.25:
        return "Weak"
    return "Poor"
