"""
FAISS vector index for Build 11.

Builds an in-memory FAISS IndexFlatIP index over chunk embeddings.
Supports search and returns ranked results with metadata.
"""

from __future__ import annotations

import numpy as np


def build_index(embeddings: np.ndarray):
    """
    Build a FAISS IndexFlatIP index from a 2D numpy array of unit-normalised embeddings.
    Returns the FAISS index object.
    """
    import faiss
    emb = embeddings.astype(np.float32)
    dim = emb.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(emb)
    return index


def search_index(
    index,
    query_embedding: np.ndarray,
    chunks: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """
    Search the index with a query embedding.

    Returns a list of result dicts (up to top_k), each containing:
        chunk_id, document_id, source_name, chunk_index, text,
        word_count, score (float), rank (int).
    Sorted by score descending.
    """
    if not chunks:
        return []
    query = query_embedding.astype(np.float32).reshape(1, -1)
    k = min(top_k, len(chunks))
    scores, indices = index.search(query, k)
    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < 0:
            continue
        results.append({**chunks[int(idx)], "score": float(score), "rank": rank + 1})
    return results


def index_summary(index, embeddings: np.ndarray) -> dict:
    """Return summary statistics for the built index."""
    dim = int(embeddings.shape[1]) if embeddings.ndim == 2 and len(embeddings) > 0 else 0
    return {
        "total_vectors": index.ntotal,
        "embedding_dimension": dim,
        "index_type": "IndexFlatIP",
    }
