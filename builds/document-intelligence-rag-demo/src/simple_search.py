"""
simple_search.py — keyword-based document search.

Functions:
    normalise_text(text)                             → lowercase stripped string
    tokenise_query(query)                            → list of meaningful lowercase tokens
    search_document(text, query, document_name="")  → list of result dicts
    search_documents(documents, query)               → list of result dicts across docs

Each result dict contains:
    document_name   — name of the source document (empty string if not provided)
    line_number     — 1-based line number of the match
    snippet         — the matched line, stripped of whitespace
    relevance_count — total occurrences of all matched terms in the line
    matched_terms   — list of query tokens that appeared in the line
"""

# Common words filtered out of queries — they add noise in policy document search.
# Deliberately short: "not" and "must" are kept because they are meaningful in policy text.
_STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "of", "in", "is", "it", "to",
    "be", "are", "was", "for", "on", "at", "by", "with",
    "what", "does", "do", "say", "about", "how", "who", "which", "when",
})


def normalise_text(text: str) -> str:
    """Return text lowercased and stripped of leading/trailing whitespace."""
    return text.lower().strip()


def tokenise_query(query: str) -> list:
    """
    Split a query string into lowercase tokens, filtering stop words.

    Returns a list of meaningful search terms.
    Empty or whitespace-only queries return an empty list.

    Examples:
        tokenise_query("Learner Data")            → ["learner", "data"]
        tokenise_query("what is safeguarding")    → ["safeguarding"]
        tokenise_query("")                        → []
    """
    return [t for t in query.lower().split() if t and t not in _STOP_WORDS]


def search_document(text: str, query: str, document_name: str = "") -> list:
    """
    Search a single document for a query string.

    - Case-insensitive multi-term search: each word in the query is matched
      independently, so "learner data" finds lines containing either term.
    - Identical snippets are deduplicated.
    - Empty or stop-word-only queries return an empty list.

    Returns a list of dicts, each with:
        document_name   — the document_name argument (empty string if not provided)
        line_number     — 1-based line number of the match
        snippet         — the matched line (stripped)
        relevance_count — total term occurrences in the line (higher = more relevant)
        matched_terms   — list of query tokens that matched
    """
    tokens = tokenise_query(query)
    if not tokens:
        return []

    seen_snippets = set()
    results = []

    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped in seen_snippets:
            continue
        line_lower = stripped.lower()
        matched = [t for t in tokens if t in line_lower]
        if matched:
            seen_snippets.add(stripped)
            relevance_count = sum(line_lower.count(t) for t in matched)
            results.append({
                "document_name": document_name,
                "line_number": i,
                "snippet": stripped,
                "relevance_count": relevance_count,
                "matched_terms": matched,
            })

    return results


def search_documents(documents: dict, query: str) -> list:
    """
    Search across multiple documents.

    documents — dict mapping document name (str) to text content (str)

    Returns a flat list of result dicts (same structure as search_document),
    sorted by relevance_count descending so the most relevant snippets appear first.
    """
    results = []
    for doc_name, text in documents.items():
        results.extend(search_document(text, query, document_name=doc_name))
    return sorted(results, key=lambda r: r["relevance_count"], reverse=True)
