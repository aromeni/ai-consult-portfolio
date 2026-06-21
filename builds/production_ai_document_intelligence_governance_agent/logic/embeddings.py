"""
Sentence-transformer embedding engine for Build 11.

Loads the all-MiniLM-L6-v2 model locally and generates
384-dimensional unit-normalised embeddings for chunks and queries.
No external API calls.
"""

from __future__ import annotations

import numpy as np

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_model(model_name: str = DEFAULT_MODEL_NAME):
    """Load and return the sentence-transformers model."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str], model) -> np.ndarray:
    """
    Embed a list of strings. Returns a 2D numpy array of shape (len(texts), dim).
    Unit-normalises embeddings for cosine similarity via inner product.
    """
    if not texts:
        dim = embedding_dimension(model)
        return np.zeros((0, dim), dtype=np.float32)
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return np.asarray(embeddings, dtype=np.float32)


def embed_chunks(chunks: list[dict], model) -> np.ndarray:
    """Extract text from chunk dicts and embed. Returns array of shape (len(chunks), dim)."""
    texts = [c["text"] for c in chunks]
    return embed_texts(texts, model)


def embed_query(query: str, model) -> np.ndarray:
    """Embed a single query string. Returns 1D array of shape (dim,)."""
    return embed_texts([query], model)[0]


def embedding_dimension(model) -> int:
    """Return the output embedding dimension for the model."""
    return model.get_sentence_embedding_dimension()
