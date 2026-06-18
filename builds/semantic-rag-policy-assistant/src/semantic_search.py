"""Semantic search — Phase 5: query embedding and FAISS retrieval.

Embeds a user query using the same sentence-transformers model used for chunks,
then searches the FAISS vector index for the most similar chunks.
All processing is local — no external AI API calls.
"""

import numpy as np

from src.embedding_engine import get_default_embedding_model_name, load_embedding_model
from src.vector_store import search_vector_store

_LIMITATIONS = [
    "Semantic search retrieves likely relevant chunks, not guaranteed complete answers.",
    "Similarity scores are useful for ranking but should not be treated as confidence scores.",
    "Users should review the source chunks before making decisions.",
    "This prototype uses synthetic documents only.",
    (
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice."
    ),
]


def validate_semantic_search_inputs(query: str, vector_store) -> tuple:
    """Return (is_valid: bool, message: str).

    Checks:
    - query is a non-empty string after stripping
    - vector_store is a non-empty dict with a non-None index
    """
    if not query or not query.strip():
        return False, "Query is empty. Enter a question or search phrase to continue."
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
    return True, "Inputs are valid."


def embed_query(
    query: str,
    model=None,
    model_name: str = None,
    normalise: bool = True,
) -> dict:
    """Embed a single query string using a sentence-transformers model.

    Returns:
        {
            query: str,
            model_name: str,
            embedding: np.ndarray  shape (1, embedding_dimension),
            embedding_dimension: int,
            normalised: bool,
        }

    Raises ValueError for an empty or whitespace-only query.
    """
    if not query or not query.strip():
        raise ValueError("Query must not be empty.")

    resolved_name = model_name or get_default_embedding_model_name()

    if model is None:
        model = load_embedding_model(resolved_name)

    embedding = model.encode([query], normalize_embeddings=normalise)
    embedding = np.array(embedding, dtype=np.float32)

    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)

    dim = int(embedding.shape[1]) if embedding.ndim > 1 and embedding.shape[1] > 0 else 0

    return {
        "query": query,
        "model_name": resolved_name,
        "embedding": embedding,
        "embedding_dimension": dim,
        "normalised": normalise,
    }


def format_semantic_search_results(results: list) -> list:
    """Add source_label and preview_text to each result dict.

    Does not mutate the original result dicts.
    Returns a new list with the extra fields added.
    """
    formatted = []
    for r in results:
        item = dict(r)
        doc = item.get("document_name", "")
        idx = item.get("chunk_index", 0)
        item["source_label"] = f"From {doc} · chunk {idx}"
        text = item.get("text", "")
        item["preview_text"] = text[:200] + ("..." if len(text) > 200 else "")
        formatted.append(item)
    return formatted


def semantic_search(
    query: str,
    vector_store: dict,
    model=None,
    model_name: str = None,
    top_k: int = 5,
    normalise: bool = True,
) -> dict:
    """Embed a query and retrieve the top_k most similar chunks from the vector store.

    Returns:
        {
            query: str,
            model_name: str,
            top_k: int,
            results: list[dict],
            result_count: int,
            query_embedding_dimension: int,
            metric: str,
            limitations: list[str],
        }

    Raises ValueError if query is empty or vector_store is not ready.
    """
    valid, msg = validate_semantic_search_inputs(query, vector_store)
    if not valid:
        raise ValueError(msg)

    query_result = embed_query(query, model=model, model_name=model_name, normalise=normalise)
    resolved_name = query_result["model_name"]
    query_embedding = query_result["embedding"]
    dim = query_result["embedding_dimension"]

    raw_results = search_vector_store(vector_store, query_embedding, top_k=top_k)
    results = format_semantic_search_results(raw_results)

    return {
        "query": query,
        "model_name": resolved_name,
        "top_k": top_k,
        "results": results,
        "result_count": len(results),
        "query_embedding_dimension": dim,
        "metric": vector_store.get("metric", "cosine"),
        "limitations": _LIMITATIONS,
    }
