"""Keyword search over document chunks for the Semantic RAG Policy Assistant.

Phase 1 provides deterministic keyword matching as a retrieval baseline.
Later phases will add semantic search for comparison.
"""

import re

_STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "its", "this", "that", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "do", "does",
    "did", "not", "no", "as", "if", "so", "up", "out", "about", "into",
    "than", "then", "when", "where", "which", "who", "what", "how", "all",
    "any", "can", "may", "will", "would", "should", "could", "must", "shall",
}


def tokenise_query(query: str) -> list:
    """Return lowercase non-stop-word tokens from a query string."""
    if not query or not query.strip():
        return []
    tokens = re.findall(r"[a-z0-9]+", query.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 1]


def keyword_search_chunks(chunks: list, query: str, top_k: int = 5) -> list:
    """Search chunks for query terms; return top_k results scored by matched term count.

    Each result dict adds:
      score (int: number of matched terms),
      matched_terms (list of str).
    """
    terms = tokenise_query(query)
    if not terms or not chunks:
        return []

    scored = []
    for chunk in chunks:
        text_lower = chunk["text"].lower()
        matched = [t for t in terms if t in text_lower]
        if matched:
            result = dict(chunk)
            result["score"] = len(matched)
            result["matched_terms"] = matched
            scored.append(result)

    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:top_k]
