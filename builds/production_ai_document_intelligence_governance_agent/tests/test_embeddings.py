"""Tests for logic/embeddings.py — Phase 3.

Uses FakeModel to avoid downloading sentence-transformers (~90MB) during testing.
All tests are deterministic and require no internet access.
"""

import numpy as np
import pytest

from logic.embeddings import (
    embed_chunks,
    embed_query,
    embed_texts,
    embedding_dimension,
)

DIM = 16  # Fake model dimension


class FakeModel:
    """Minimal sentence-transformer interface for testing — no download required."""

    DIM = DIM

    def encode(self, texts, convert_to_numpy=True, normalize_embeddings=True, **kwargs):
        results = []
        for i, text in enumerate(texts):
            rng = np.random.RandomState(i + len(text))
            vec = rng.rand(self.DIM).astype(np.float32)
            if normalize_embeddings:
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
            results.append(vec)
        if not results:
            return np.zeros((0, self.DIM), dtype=np.float32)
        return np.array(results, dtype=np.float32)

    def get_sentence_embedding_dimension(self):
        return self.DIM


@pytest.fixture
def model():
    return FakeModel()


# ---------------------------------------------------------------------------
# embed_texts
# ---------------------------------------------------------------------------


def test_embed_texts_returns_ndarray(model):
    result = embed_texts(["hello world"], model)
    assert isinstance(result, np.ndarray)


def test_embed_texts_correct_shape(model):
    texts = ["first sentence", "second sentence", "third sentence"]
    result = embed_texts(texts, model)
    assert result.shape == (3, DIM)


def test_embed_texts_single_text_shape(model):
    result = embed_texts(["one text"], model)
    assert result.shape == (1, DIM)


def test_embed_texts_empty_list_returns_empty(model):
    result = embed_texts([], model)
    assert result.shape[0] == 0
    assert result.shape[1] == DIM


def test_embed_texts_dtype_is_float32(model):
    result = embed_texts(["hello"], model)
    assert result.dtype == np.float32


def test_embed_texts_unit_normalised(model):
    result = embed_texts(["hello world", "test text"], model)
    norms = np.linalg.norm(result, axis=1)
    np.testing.assert_allclose(norms, 1.0, atol=1e-5)


def test_embed_texts_different_inputs_produce_different_vectors(model):
    result = embed_texts(["apples", "zebras"], model)
    assert not np.allclose(result[0], result[1])


# ---------------------------------------------------------------------------
# embed_chunks
# ---------------------------------------------------------------------------


SAMPLE_CHUNKS = [
    {
        "chunk_id": "doc1_chunk_000",
        "document_id": "doc1",
        "source_name": "doc1.md",
        "chunk_index": 0,
        "text": "Staff must not enter learner names into AI tools.",
        "word_count": 9,
        "start_word": 0,
        "end_word": 8,
        "metadata": {},
    },
    {
        "chunk_id": "doc1_chunk_001",
        "document_id": "doc1",
        "source_name": "doc1.md",
        "chunk_index": 1,
        "text": "Human review is required before any AI output is used.",
        "word_count": 10,
        "start_word": 160,
        "end_word": 169,
        "metadata": {},
    },
]


def test_embed_chunks_returns_ndarray(model):
    result = embed_chunks(SAMPLE_CHUNKS, model)
    assert isinstance(result, np.ndarray)


def test_embed_chunks_correct_shape(model):
    result = embed_chunks(SAMPLE_CHUNKS, model)
    assert result.shape == (len(SAMPLE_CHUNKS), DIM)


def test_embed_chunks_empty_list_returns_empty(model):
    result = embed_chunks([], model)
    assert result.shape[0] == 0


def test_embed_chunks_dtype_float32(model):
    result = embed_chunks(SAMPLE_CHUNKS, model)
    assert result.dtype == np.float32


def test_embed_chunks_uses_text_field(model):
    chunks_with_text = [{**SAMPLE_CHUNKS[0], "text": "unique text for chunk"}]
    result = embed_chunks(chunks_with_text, model)
    assert result.shape == (1, DIM)


# ---------------------------------------------------------------------------
# embed_query
# ---------------------------------------------------------------------------


def test_embed_query_returns_1d_array(model):
    result = embed_query("What is the safeguarding policy?", model)
    assert result.ndim == 1


def test_embed_query_correct_shape(model):
    result = embed_query("test query", model)
    assert result.shape == (DIM,)


def test_embed_query_dtype_float32(model):
    result = embed_query("test query", model)
    assert result.dtype == np.float32


def test_embed_query_unit_normalised(model):
    result = embed_query("Can staff enter learner data into ChatGPT?", model)
    norm = np.linalg.norm(result)
    assert abs(norm - 1.0) < 1e-5


# ---------------------------------------------------------------------------
# embedding_dimension
# ---------------------------------------------------------------------------


def test_embedding_dimension_returns_int(model):
    assert isinstance(embedding_dimension(model), int)


def test_embedding_dimension_matches_embed_output(model):
    dim = embedding_dimension(model)
    result = embed_texts(["test"], model)
    assert result.shape[1] == dim


def test_embedding_dimension_correct_value(model):
    assert embedding_dimension(model) == DIM
