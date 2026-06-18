"""Retrieval comparison — Phase 7: keyword vs semantic side-by-side.

Runs both keyword and semantic retrieval for the same query and returns
a structured comparison including overlap, summaries, and a deterministic insight.
All processing is local — no external AI API calls.
"""

from src.keyword_search import keyword_search_chunks
from src.semantic_search import semantic_search

_LIMITATIONS = [
    "Keyword and semantic retrieval are evidence-finding methods, not final answers.",
    "Semantic similarity scores are ranking signals, not confidence scores.",
    "Keyword results may miss relevant content using different wording.",
    "Semantic results may retrieve conceptually related but imperfect chunks.",
    "Users should review source chunks before acting.",
    "This prototype uses synthetic documents only.",
    (
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice."
    ),
]


def summarise_keyword_results(keyword_results: list) -> dict:
    """Return aggregate statistics for a keyword retrieval result list."""
    if not keyword_results:
        return {
            "result_count": 0,
            "documents_found": [],
            "unique_documents": 0,
            "top_score": 0,
            "matched_terms": [],
            "method_note": (
                "Keyword retrieval depends on exact or near-exact word matches. "
                "It may miss relevant content if the document uses different wording."
            ),
        }
    docs = sorted({r.get("document_name", "") for r in keyword_results})
    all_terms: list = []
    for r in keyword_results:
        all_terms.extend(r.get("matched_terms", []))
    top_score = max(r.get("score", 0) for r in keyword_results)
    return {
        "result_count": len(keyword_results),
        "documents_found": docs,
        "unique_documents": len(docs),
        "top_score": top_score,
        "matched_terms": sorted(set(all_terms)),
        "method_note": (
            "Keyword retrieval depends on exact or near-exact word matches. "
            "It may miss relevant content if the document uses different wording."
        ),
    }


def summarise_semantic_results(semantic_results: list) -> dict:
    """Return aggregate statistics for a semantic retrieval result list."""
    if not semantic_results:
        return {
            "result_count": 0,
            "documents_found": [],
            "unique_documents": 0,
            "top_score": 0.0,
            "method_note": (
                "Semantic retrieval uses vector similarity to find related meaning. "
                "It can retrieve relevant chunks even when exact words differ, "
                "but results still need human review."
            ),
        }
    docs = sorted({r.get("document_name", "") for r in semantic_results})
    top_score = max(float(r.get("score", 0.0)) for r in semantic_results)
    return {
        "result_count": len(semantic_results),
        "documents_found": docs,
        "unique_documents": len(docs),
        "top_score": round(top_score, 4),
        "method_note": (
            "Semantic retrieval uses vector similarity to find related meaning. "
            "It can retrieve relevant chunks even when exact words differ, "
            "but results still need human review."
        ),
    }


def find_overlap_between_results(
    keyword_results: list,
    semantic_results: list,
) -> list:
    """Return chunks appearing in both results, matched by chunk_id.

    Each overlap item includes chunk_id, document_name, keyword_rank, semantic_rank.
    """
    keyword_map = {
        r["chunk_id"]: i + 1
        for i, r in enumerate(keyword_results)
        if r.get("chunk_id")
    }
    overlap = []
    for i, r in enumerate(semantic_results):
        cid = r.get("chunk_id")
        if cid and cid in keyword_map:
            overlap.append(
                {
                    "chunk_id": cid,
                    "document_name": r.get("document_name", ""),
                    "keyword_rank": keyword_map[cid],
                    "semantic_rank": i + 1,
                }
            )
    return overlap


def generate_retrieval_comparison_insight(
    query: str,
    keyword_summary: dict,
    semantic_summary: dict,
    overlap: list,
) -> str:
    """Return a deterministic one-paragraph explanation of the retrieval comparison."""
    kw_count = keyword_summary.get("result_count", 0)
    sem_count = semantic_summary.get("result_count", 0)
    overlap_count = len(overlap)

    if sem_count > 0 and kw_count == 0:
        return (
            "Semantic retrieval found evidence where keyword retrieval did not. "
            "This suggests the query may use different wording from the policy documents, "
            "and semantic search is helpful for meaning-based retrieval."
        )
    if kw_count > 0 and sem_count > 0 and overlap_count > 0:
        return (
            "Both retrieval methods found some of the same chunks. "
            "This suggests the query terms align reasonably well with the policy wording, "
            "while semantic search may still provide additional context."
        )
    if kw_count > 0 and sem_count > 0 and overlap_count == 0:
        return (
            "Keyword search found exact term matches, while semantic search found chunks "
            "that may be conceptually related. "
            "Review both sets before deciding which evidence is most relevant."
        )
    if kw_count == 0 and sem_count == 0:
        return (
            "Neither method found useful evidence. "
            "Try rephrasing the query, broadening the document set, "
            "or reviewing the documents manually."
        )
    return (
        "Keyword retrieval found exact term matches, but semantic retrieval did not return "
        "results. This may indicate that the vector index is not built yet, or that the "
        "embedding space does not closely represent these policy terms. "
        "Review the keyword results and consider rebuilding the index."
    )


def generate_retrieval_comparison_markdown(comparison_result: dict) -> str:
    """Return a Markdown report string from a compare_retrieval_methods result dict."""
    lines = ["# Retrieval Comparison Report", ""]
    lines += ["## Query", "", comparison_result.get("query", ""), ""]

    ks = comparison_result.get("keyword_summary", {})
    lines += ["## Keyword Retrieval Summary", ""]
    lines += [f"- Results found: {ks.get('result_count', 0)}"]
    lines += [f"- Unique documents: {ks.get('unique_documents', 0)}"]
    docs = ks.get("documents_found", [])
    if docs:
        lines += [f"- Documents: {', '.join(docs)}"]
    lines += [f"- Top score: {ks.get('top_score', 0)}"]
    terms = ks.get("matched_terms", [])
    if terms:
        lines += [f"- Matched terms: {', '.join(terms)}"]
    lines += [f"- Note: {ks.get('method_note', '')}", ""]

    ss = comparison_result.get("semantic_summary", {})
    lines += ["## Semantic Retrieval Summary", ""]
    lines += [f"- Results found: {ss.get('result_count', 0)}"]
    lines += [f"- Unique documents: {ss.get('unique_documents', 0)}"]
    docs2 = ss.get("documents_found", [])
    if docs2:
        lines += [f"- Documents: {', '.join(docs2)}"]
    lines += [f"- Top score: {ss.get('top_score', 0.0)}"]
    lines += [f"- Note: {ss.get('method_note', '')}", ""]

    overlap = comparison_result.get("overlap", [])
    lines += ["## Overlapping Results", ""]
    if overlap:
        lines += ["| Chunk ID | Document | Keyword Rank | Semantic Rank |"]
        lines += ["|---|---|---|---|"]
        for item in overlap:
            lines += [
                f"| {item['chunk_id']} | {item['document_name']} "
                f"| {item['keyword_rank']} | {item['semantic_rank']} |"
            ]
    else:
        lines += ["No overlapping chunks found."]
    lines += [""]

    lines += ["## Comparison Insight", "", comparison_result.get("comparison_insight", ""), ""]

    kw_results = comparison_result.get("keyword_results", [])
    lines += ["## Keyword Results", ""]
    if kw_results:
        for rank, r in enumerate(kw_results, 1):
            lines += [
                f"**Rank {rank}** · {r.get('document_name', '')} · {r.get('chunk_id', '')}",
                f"Score: {r.get('score', '')} · Terms: {', '.join(r.get('matched_terms', []))}",
                f"> {r.get('text', '')[:300]}",
                "",
            ]
    else:
        lines += ["No keyword results.", ""]

    sem_results = comparison_result.get("semantic_results", [])
    lines += ["## Semantic Results", ""]
    if sem_results:
        for r in sem_results:
            lines += [
                f"**Rank {r.get('rank', '')}** · {r.get('document_name', '')} · {r.get('chunk_id', '')}",
                f"Score: {r.get('score', '')}",
                f"> {r.get('text', '')[:300]}",
                "",
            ]
    else:
        lines += ["No semantic results.", ""]

    lines += ["## Limitations and Responsible Use", ""]
    for lim in comparison_result.get("limitations", _LIMITATIONS):
        lines += [f"- {lim}"]

    return "\n".join(lines)


def compare_retrieval_methods(
    query: str,
    chunks: list,
    vector_store: dict,
    model=None,
    model_name: str = None,
    top_k: int = 5,
) -> dict:
    """Run keyword and semantic retrieval for the same query; return structured comparison.

    Returns:
        {
            query, top_k,
            keyword_results, semantic_results,
            keyword_summary, semantic_summary,
            overlap, comparison_insight, limitations
        }
    """
    keyword_results = keyword_search_chunks(chunks, query, top_k=top_k)

    try:
        sem_output = semantic_search(
            query,
            vector_store,
            model=model,
            model_name=model_name,
            top_k=top_k,
        )
        semantic_results = sem_output.get("results", [])
    except Exception:
        semantic_results = []

    keyword_summary = summarise_keyword_results(keyword_results)
    semantic_summary = summarise_semantic_results(semantic_results)
    overlap = find_overlap_between_results(keyword_results, semantic_results)
    insight = generate_retrieval_comparison_insight(
        query, keyword_summary, semantic_summary, overlap
    )

    return {
        "query": query,
        "top_k": top_k,
        "keyword_results": keyword_results,
        "semantic_results": semantic_results,
        "keyword_summary": keyword_summary,
        "semantic_summary": semantic_summary,
        "overlap": overlap,
        "comparison_insight": insight,
        "limitations": _LIMITATIONS,
    }
