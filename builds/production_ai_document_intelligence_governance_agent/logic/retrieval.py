"""
Retrieval interface for Build 11.

Connects query embedding to FAISS search and returns ranked results.
Handles empty and weak-retrieval cases explicitly.
"""

from __future__ import annotations

import numpy as np

from logic.embeddings import embed_query
from logic.vector_index import search_index

WEAK_SCORE_THRESHOLD = 0.25


def retrieve(
    query: str,
    model,
    index,
    chunks: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """
    Embed query and search the index.

    Returns a ranked list of result dicts.
    Each result includes: chunk_id, source_name, text, score, rank, is_weak (bool).
    """
    if not chunks:
        return []
    query_emb = embed_query(query, model)
    results = search_index(index, query_emb, chunks, top_k)
    for r in results:
        r["is_weak"] = r["score"] < WEAK_SCORE_THRESHOLD
    return results


def is_retrieval_weak(results: list[dict], threshold: float = WEAK_SCORE_THRESHOLD) -> bool:
    """Return True if the top result score is below the threshold or results is empty."""
    if not results:
        return True
    return results[0]["score"] < threshold


def format_results_for_display(results: list[dict]) -> list[dict]:
    """Return results formatted for Streamlit display (score as percentage string, etc.)."""
    return [
        {
            **r,
            "score_pct": f"{r['score'] * 100:.1f}%",
            "score_label": _score_label(r["score"]),
        }
        for r in results
    ]


def _score_label(score: float) -> str:
    if score >= 0.7:
        return "Strong"
    if score >= 0.5:
        return "Good"
    if score >= 0.25:
        return "Moderate"
    return "Weak"
