"""Vector store — Phase 4: FAISS-based vector index for embedded document chunks.

Builds an in-memory FAISS index from Phase 3 embedding matrices.
All processing is local — no external AI API calls, no cloud services.
"""

import numpy as np


# ── FAISS import helper ────────────────────────────────────────────────────────

def _import_faiss():
    """Lazy-import FAISS with a readable error message if not installed."""
    try:
        import faiss
        return faiss
    except ImportError:
        raise ImportError(
            "FAISS is not installed. Install dependencies with: pip install -r requirements.txt"
        )


# ── Validation ─────────────────────────────────────────────────────────────────

def validate_embedding_matrix(embedding_matrix, embedded_chunks: list) -> tuple:
    """Check that an embedding matrix and chunk list are ready for indexing.

    Returns (is_valid: bool, message: str).

    Rules checked:
    - embedding_matrix is not None
    - embedded_chunks is not empty
    - embedding_matrix is a 2D numpy array
    - embedding dimension is greater than 0
    - number of matrix rows equals number of chunks
    - values are numeric
    """
    if embedding_matrix is None:
        return False, "Embedding matrix is None. Generate embeddings first."

    if not embedded_chunks:
        return False, "No embedded chunks provided. Generate embeddings first."

    if not hasattr(embedding_matrix, "shape"):
        return False, "Embedding matrix must be a numpy array."

    if embedding_matrix.ndim != 2:
        return (
            False,
            f"Embedding matrix must have 2 dimensions, got {embedding_matrix.ndim}.",
        )

    n_rows, dim = embedding_matrix.shape

    if dim == 0:
        return False, "Embedding dimension is 0. Embeddings may not have been generated correctly."

    if n_rows != len(embedded_chunks):
        return (
            False,
            f"Mismatch: embedding matrix has {n_rows} rows "
            f"but {len(embedded_chunks)} chunks provided. "
            "Re-generate embeddings to fix this.",
        )

    if not np.issubdtype(embedding_matrix.dtype, np.number):
        return (
            False,
            f"Embedding matrix contains non-numeric values (dtype: {embedding_matrix.dtype}).",
        )

    return True, f"{n_rows} embeddings with dimension {dim} are ready for indexing."


# ── Index building ─────────────────────────────────────────────────────────────

def build_faiss_index(embedding_matrix, metric: str = "cosine"):
    """Build and return a FAISS index from a 2D embedding matrix.

    metric="cosine": uses IndexFlatIP (inner product).
        Assumes embeddings are already unit-normalised (Phase 3 normalises by default).
        Higher score means more similar.

    metric="l2": uses IndexFlatL2 (Euclidean distance).
        Lower distance means more similar.
    """
    faiss = _import_faiss()
    matrix = np.array(embedding_matrix, dtype=np.float32)

    if matrix.ndim != 2:
        raise ValueError(f"embedding_matrix must be 2D, got {matrix.ndim}D")

    _, dim = matrix.shape

    if metric == "l2":
        index = faiss.IndexFlatL2(dim)
    else:
        index = faiss.IndexFlatIP(dim)

    index.add(matrix)
    return index


def create_vector_store(
    embedded_chunks: list,
    embedding_matrix,
    metric: str = "cosine",
) -> dict:
    """Build a FAISS vector index and return a vector store dictionary.

    Validates inputs, builds the index, and packages everything the search
    function needs.

    Returns:
        {
            index, embedded_chunks, embedding_matrix, metric,
            dimension, chunk_count, document_count, index_type
        }
    """
    valid, msg = validate_embedding_matrix(embedding_matrix, embedded_chunks)
    if not valid:
        raise ValueError(msg)

    index = build_faiss_index(embedding_matrix, metric=metric)

    matrix = np.array(embedding_matrix, dtype=np.float32)
    _, dim = matrix.shape
    doc_names = {c.get("document_name", "") for c in embedded_chunks}
    index_type = "IndexFlatL2" if metric == "l2" else "IndexFlatIP"

    return {
        "index": index,
        "embedded_chunks": embedded_chunks,
        "embedding_matrix": embedding_matrix,
        "metric": metric,
        "dimension": int(dim),
        "chunk_count": len(embedded_chunks),
        "document_count": len(doc_names),
        "index_type": index_type,
    }


# ── Search ─────────────────────────────────────────────────────────────────────

def search_vector_store(
    vector_store: dict,
    query_embedding,
    top_k: int = 5,
) -> list:
    """Search the vector store for the top_k chunks most similar to a query embedding.

    Returns a list of result dicts ordered by similarity score.
    Does not mutate the original embedded_chunks.

    Each result includes:
        rank, score, chunk_id, document_name, chunk_index,
        text, word_count, character_count, embedding_index
    """
    index = vector_store.get("index")
    embedded_chunks = vector_store.get("embedded_chunks", [])

    if index is None or not embedded_chunks:
        return []

    chunk_count = len(embedded_chunks)
    k = min(top_k, chunk_count)
    if k == 0:
        return []

    q = np.array(query_embedding, dtype=np.float32)
    if q.ndim == 1:
        q = q.reshape(1, -1)

    scores, indices = index.search(q, k)
    scores = scores[0]
    indices = indices[0]

    results = []
    for rank, (idx, score) in enumerate(zip(indices, scores), start=1):
        idx = int(idx)
        if idx < 0 or idx >= chunk_count:
            continue
        chunk = embedded_chunks[idx]
        results.append({
            "rank": rank,
            "score": float(score),
            "chunk_id": chunk.get("chunk_id", ""),
            "document_name": chunk.get("document_name", ""),
            "chunk_index": chunk.get("chunk_index", 0),
            "text": chunk.get("text", ""),
            "word_count": chunk.get("word_count", 0),
            "character_count": chunk.get("character_count", 0),
            "embedding_index": chunk.get("embedding_index", idx),
        })

    return results


# ── Summary ────────────────────────────────────────────────────────────────────

def get_vector_store_summary(vector_store: dict) -> dict:
    """Return aggregate statistics for a vector store dictionary.

    Returns:
        {
            index_type, metric, chunk_count, document_count, dimension,
            is_trained, total_vectors, documents_indexed
        }

    Returns safe defaults for empty or missing vector stores.
    """
    if not vector_store:
        return {
            "index_type": "N/A",
            "metric": "N/A",
            "chunk_count": 0,
            "document_count": 0,
            "dimension": 0,
            "is_trained": False,
            "total_vectors": 0,
            "documents_indexed": [],
        }

    index = vector_store.get("index")
    embedded_chunks = vector_store.get("embedded_chunks", [])
    doc_names = sorted({c.get("document_name", "") for c in embedded_chunks})

    return {
        "index_type": vector_store.get("index_type", "N/A"),
        "metric": vector_store.get("metric", "N/A"),
        "chunk_count": vector_store.get("chunk_count", 0),
        "document_count": vector_store.get("document_count", 0),
        "dimension": vector_store.get("dimension", 0),
        "is_trained": bool(index is not None and getattr(index, "is_trained", True)),
        "total_vectors": int(index.ntotal) if index is not None else 0,
        "documents_indexed": doc_names,
    }


# ── Save / load ────────────────────────────────────────────────────────────────

def save_faiss_index(index, path: str) -> None:
    """Write a FAISS index to disk at the given path."""
    faiss = _import_faiss()
    faiss.write_index(index, path)


def load_faiss_index(path: str):
    """Load a FAISS index from disk and return it."""
    faiss = _import_faiss()
    return faiss.read_index(path)
