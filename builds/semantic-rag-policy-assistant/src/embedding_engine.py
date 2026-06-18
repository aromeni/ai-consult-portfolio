"""Local embedding engine for the Semantic RAG Policy Assistant.

Phase 3: generates vector embeddings for document chunks using sentence-transformers.
All processing is local — no external AI API calls.
"""

import numpy as np

_DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ── Model name ────────────────────────────────────────────────────────────────

def get_default_embedding_model_name() -> str:
    """Return the default sentence-transformers model name."""
    return _DEFAULT_MODEL


# ── Model loading ─────────────────────────────────────────────────────────────

def load_embedding_model(model_name: str = None):
    """Load and return a SentenceTransformer model.

    Uses the default model if model_name is not supplied.
    The import is lazy so the module can be imported without sentence-transformers installed.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "sentence-transformers is required for embedding generation. "
            "Run: pip install sentence-transformers"
        )
    return SentenceTransformer(model_name or _DEFAULT_MODEL)


# ── Validation ────────────────────────────────────────────────────────────────

def validate_chunks_for_embedding(chunks: list) -> tuple:
    """Return (is_valid: bool, message: str) for a list of chunk dicts.

    Rules:
    - chunks must not be empty
    - each chunk must have non-empty text
    """
    if not chunks:
        return (
            False,
            "No chunks to embed. Go to the Chunking Explorer and generate chunks first.",
        )
    for i, chunk in enumerate(chunks):
        if not chunk.get("text", "").strip():
            return (
                False,
                f"Chunk at index {i} (id: {chunk.get('chunk_id', '?')}) has empty text. "
                "All chunks must have non-empty text before embedding.",
            )
    return True, f"{len(chunks)} chunks are ready for embedding."


# ── Text embedding ────────────────────────────────────────────────────────────

def embed_texts(
    texts: list,
    model=None,
    model_name: str = None,
    normalise: bool = True,
) -> dict:
    """Embed a list of text strings.

    If model is not supplied, loads the model by model_name (or the default model).

    Returns:
        {
            model_name: str,
            embedding_dimension: int,
            embeddings: np.ndarray,  shape (n_texts, dim)
            text_count: int,
            normalised: bool,
        }
    """
    resolved_name = model_name or _DEFAULT_MODEL

    if not texts:
        return {
            "model_name": resolved_name,
            "embedding_dimension": 0,
            "embeddings": np.array([]).reshape(0, 0),
            "text_count": 0,
            "normalised": normalise,
        }

    if model is None:
        model = load_embedding_model(resolved_name)

    embeddings = model.encode(texts, normalize_embeddings=normalise)
    embeddings = np.array(embeddings)
    dim = int(embeddings.shape[1]) if embeddings.ndim > 1 else 0

    return {
        "model_name": resolved_name,
        "embedding_dimension": dim,
        "embeddings": embeddings,
        "text_count": len(texts),
        "normalised": normalise,
    }


# ── Chunk embedding ───────────────────────────────────────────────────────────

def embed_chunks(
    chunks: list,
    model=None,
    model_name: str = None,
    normalise: bool = True,
) -> dict:
    """Embed a list of chunk dicts produced by the chunker.

    Validates chunks before embedding. Raises ValueError if validation fails.

    Each embedded chunk preserves all original metadata and adds:
        embedding_index (int): position in the embedding matrix
        embedding_vector (list[float]): serialisable list form of the embedding

    Returns:
        {
            model_name: str,
            embedding_dimension: int,
            embedded_chunks: list[dict],
            embedding_matrix: np.ndarray,  shape (n_chunks, dim)
            chunk_count: int,
            normalised: bool,
        }
    """
    valid, msg = validate_chunks_for_embedding(chunks)
    if not valid:
        raise ValueError(msg)

    texts = [c["text"] for c in chunks]
    text_result = embed_texts(texts, model=model, model_name=model_name, normalise=normalise)

    embeddings = text_result["embeddings"]
    resolved_name = text_result["model_name"]
    dim = text_result["embedding_dimension"]

    embedded = []
    for i, chunk in enumerate(chunks):
        ec = dict(chunk)
        ec["embedding_index"] = i
        ec["embedding_vector"] = embeddings[i].tolist()
        embedded.append(ec)

    return {
        "model_name": resolved_name,
        "embedding_dimension": dim,
        "embedded_chunks": embedded,
        "embedding_matrix": embeddings,
        "chunk_count": len(embedded),
        "normalised": normalise,
    }


# ── Embedding summary ─────────────────────────────────────────────────────────

def get_embedding_summary(
    embedded_chunks: list,
    model_name: str,
    embedding_dimension: int = None,
    normalised: bool = True,
) -> dict:
    """Return aggregate statistics for a list of embedded chunk dicts.

    Returns:
        {
            model_name, chunk_count, embedding_dimension, normalised,
            documents_embedded, average_chunk_words, min_chunk_words, max_chunk_words
        }
    """
    if not embedded_chunks:
        return {
            "model_name": model_name,
            "chunk_count": 0,
            "embedding_dimension": embedding_dimension or 0,
            "normalised": normalised,
            "documents_embedded": 0,
            "average_chunk_words": 0,
            "min_chunk_words": 0,
            "max_chunk_words": 0,
        }

    word_counts = [c.get("word_count", 0) for c in embedded_chunks]
    doc_names = {c.get("document_name", "") for c in embedded_chunks}

    dim = embedding_dimension
    if dim is None and "embedding_vector" in embedded_chunks[0]:
        dim = len(embedded_chunks[0]["embedding_vector"])

    return {
        "model_name": model_name,
        "chunk_count": len(embedded_chunks),
        "embedding_dimension": dim or 0,
        "normalised": normalised,
        "documents_embedded": len(doc_names),
        "average_chunk_words": round(sum(word_counts) / len(word_counts), 1),
        "min_chunk_words": min(word_counts),
        "max_chunk_words": max(word_counts),
    }
