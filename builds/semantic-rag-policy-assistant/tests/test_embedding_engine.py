"""Tests for src/embedding_engine.py — Phase 3.

Uses FakeEmbeddingModel throughout — no sentence-transformers model is downloaded.
All tests run offline.
"""

import numpy as np
import pytest
from src.embedding_engine import (
    get_default_embedding_model_name,
    validate_chunks_for_embedding,
    embed_texts,
    embed_chunks,
    get_embedding_summary,
)


# ── Fake model ────────────────────────────────────────────────────────────────

class FakeEmbeddingModel:
    """Predictable fake embedding model for testing — returns fixed 4-d vectors."""

    def encode(self, texts, normalize_embeddings=True):
        n = len(texts)
        return np.tile([0.25, 0.50, 0.75, 1.00], (n, 1)).astype(np.float32)


FAKE_MODEL = FakeEmbeddingModel()

SAMPLE_CHUNKS = [
    {
        "chunk_id": "doc-a__chunk_000",
        "document_name": "doc-a.md",
        "chunk_index": 0,
        "text": "Staff must not enter personal data into AI tools.",
        "word_count": 9,
        "character_count": 49,
        "start_word": 0,
        "end_word": 8,
        "chunk_size": 20,
        "overlap": 5,
        "strategy": "word",
    },
    {
        "chunk_id": "doc-a__chunk_001",
        "document_name": "doc-a.md",
        "chunk_index": 1,
        "text": "Human review is required before acting on any output.",
        "word_count": 9,
        "character_count": 53,
        "start_word": 5,
        "end_word": 13,
        "chunk_size": 20,
        "overlap": 5,
        "strategy": "word",
    },
    {
        "chunk_id": "doc-b__chunk_000",
        "document_name": "doc-b.md",
        "chunk_index": 0,
        "text": "Safeguarding information must not be entered into AI tools.",
        "word_count": 10,
        "character_count": 59,
        "start_word": 0,
        "end_word": 9,
        "chunk_size": 20,
        "overlap": 5,
        "strategy": "word",
    },
]


# ── get_default_embedding_model_name ──────────────────────────────────────────

def test_default_model_name_returns_string():
    assert isinstance(get_default_embedding_model_name(), str)


def test_default_model_name_is_minilm():
    assert get_default_embedding_model_name() == "sentence-transformers/all-MiniLM-L6-v2"


# ── validate_chunks_for_embedding ─────────────────────────────────────────────

def test_validate_empty_chunks_is_invalid():
    ok, _ = validate_chunks_for_embedding([])
    assert ok is False


def test_validate_empty_chunks_message_non_empty():
    _, msg = validate_chunks_for_embedding([])
    assert isinstance(msg, str) and len(msg) > 0


def test_validate_chunk_with_empty_text_is_invalid():
    bad = dict(SAMPLE_CHUNKS[0])
    bad["text"] = ""
    ok, _ = validate_chunks_for_embedding([bad])
    assert ok is False


def test_validate_chunk_with_whitespace_text_is_invalid():
    bad = dict(SAMPLE_CHUNKS[0])
    bad["text"] = "   "
    ok, _ = validate_chunks_for_embedding([bad])
    assert ok is False


def test_validate_valid_chunks_returns_true():
    ok, _ = validate_chunks_for_embedding(SAMPLE_CHUNKS)
    assert ok is True


def test_validate_valid_chunks_message_contains_count():
    _, msg = validate_chunks_for_embedding(SAMPLE_CHUNKS)
    assert str(len(SAMPLE_CHUNKS)) in msg


# ── embed_texts ───────────────────────────────────────────────────────────────

def test_embed_texts_returns_dict():
    result = embed_texts(["hello", "world"], model=FAKE_MODEL)
    assert isinstance(result, dict)


def test_embed_texts_has_required_keys():
    result = embed_texts(["hello"], model=FAKE_MODEL)
    for key in ("model_name", "embedding_dimension", "embeddings", "text_count", "normalised"):
        assert key in result, f"Missing key: {key}"


def test_embed_texts_text_count_single():
    result = embed_texts(["hello"], model=FAKE_MODEL)
    assert result["text_count"] == 1


def test_embed_texts_text_count_multiple():
    result = embed_texts(["a", "b", "c"], model=FAKE_MODEL)
    assert result["text_count"] == 3


def test_embed_texts_embedding_dimension():
    result = embed_texts(["hello"], model=FAKE_MODEL)
    assert result["embedding_dimension"] == 4


def test_embed_texts_embeddings_is_ndarray():
    result = embed_texts(["hello", "world"], model=FAKE_MODEL)
    assert isinstance(result["embeddings"], np.ndarray)


def test_embed_texts_embeddings_shape():
    result = embed_texts(["a", "b"], model=FAKE_MODEL)
    assert result["embeddings"].shape == (2, 4)


def test_embed_texts_normalised_true():
    result = embed_texts(["hello"], model=FAKE_MODEL, normalise=True)
    assert result["normalised"] is True


def test_embed_texts_normalised_false():
    result = embed_texts(["hello"], model=FAKE_MODEL, normalise=False)
    assert result["normalised"] is False


def test_embed_texts_model_name_stored_when_provided():
    result = embed_texts(["hello"], model=FAKE_MODEL, model_name="my-test-model")
    assert result["model_name"] == "my-test-model"


def test_embed_texts_empty_list_returns_zero_count():
    result = embed_texts([], model=FAKE_MODEL)
    assert result["text_count"] == 0


def test_embed_texts_empty_list_zero_dimension():
    result = embed_texts([], model=FAKE_MODEL)
    assert result["embedding_dimension"] == 0


def test_embed_texts_empty_list_returns_dict():
    result = embed_texts([], model=FAKE_MODEL)
    assert isinstance(result, dict)


def test_embed_texts_embeddings_values_match_fake():
    result = embed_texts(["test"], model=FAKE_MODEL)
    expected = np.array([[0.25, 0.50, 0.75, 1.00]], dtype=np.float32)
    np.testing.assert_array_almost_equal(result["embeddings"], expected)


# ── embed_chunks ──────────────────────────────────────────────────────────────

def test_embed_chunks_returns_dict():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    assert isinstance(result, dict)


def test_embed_chunks_has_required_keys():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for key in ("model_name", "embedding_dimension", "embedded_chunks",
                "embedding_matrix", "chunk_count", "normalised"):
        assert key in result, f"Missing key: {key}"


def test_embed_chunks_chunk_count():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    assert result["chunk_count"] == len(SAMPLE_CHUNKS)


def test_embed_chunks_embedded_chunks_length():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    assert len(result["embedded_chunks"]) == len(SAMPLE_CHUNKS)


def test_embed_chunks_preserves_chunk_id():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec, orig in zip(result["embedded_chunks"], SAMPLE_CHUNKS):
        assert ec["chunk_id"] == orig["chunk_id"]


def test_embed_chunks_preserves_document_name():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec, orig in zip(result["embedded_chunks"], SAMPLE_CHUNKS):
        assert ec["document_name"] == orig["document_name"]


def test_embed_chunks_preserves_text():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec, orig in zip(result["embedded_chunks"], SAMPLE_CHUNKS):
        assert ec["text"] == orig["text"]


def test_embed_chunks_preserves_word_count():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec, orig in zip(result["embedded_chunks"], SAMPLE_CHUNKS):
        assert ec["word_count"] == orig["word_count"]


def test_embed_chunks_embedding_index_sequential():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for i, ec in enumerate(result["embedded_chunks"]):
        assert ec["embedding_index"] == i


def test_embed_chunks_has_embedding_vector():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec in result["embedded_chunks"]:
        assert "embedding_vector" in ec


def test_embed_chunks_embedding_vector_is_list():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec in result["embedded_chunks"]:
        assert isinstance(ec["embedding_vector"], list)


def test_embed_chunks_embedding_vector_length():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    for ec in result["embedded_chunks"]:
        assert len(ec["embedding_vector"]) == 4


def test_embed_chunks_embedding_matrix_is_ndarray():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    assert isinstance(result["embedding_matrix"], np.ndarray)


def test_embed_chunks_embedding_matrix_shape():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    assert result["embedding_matrix"].shape == (len(SAMPLE_CHUNKS), 4)


def test_embed_chunks_embedding_dimension_correct():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)
    assert result["embedding_dimension"] == 4


def test_embed_chunks_normalised_stored():
    result = embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL, normalise=True)
    assert result["normalised"] is True


def test_embed_chunks_empty_raises_value_error():
    with pytest.raises(ValueError):
        embed_chunks([], model=FAKE_MODEL)


def test_embed_chunks_empty_text_raises_value_error():
    bad = [dict(SAMPLE_CHUNKS[0])]
    bad[0]["text"] = ""
    with pytest.raises(ValueError):
        embed_chunks(bad, model=FAKE_MODEL)


# ── get_embedding_summary ─────────────────────────────────────────────────────

def _make_embedded():
    return embed_chunks(SAMPLE_CHUNKS, model=FAKE_MODEL)


def test_summary_returns_dict():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"], r["embedding_dimension"])
    assert isinstance(summary, dict)


def test_summary_has_required_keys():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"], r["embedding_dimension"])
    for key in ("model_name", "chunk_count", "embedding_dimension", "normalised",
                "documents_embedded", "average_chunk_words", "min_chunk_words", "max_chunk_words"):
        assert key in summary, f"Missing key: {key}"


def test_summary_chunk_count_correct():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"])
    assert summary["chunk_count"] == len(SAMPLE_CHUNKS)


def test_summary_documents_embedded_correct():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"])
    # SAMPLE_CHUNKS has 2 chunks from doc-a.md and 1 from doc-b.md
    assert summary["documents_embedded"] == 2


def test_summary_embedding_dimension_inferred_from_vector():
    r = _make_embedded()
    # Don't pass embedding_dimension — let it infer from embedding_vector
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"])
    assert summary["embedding_dimension"] == 4


def test_summary_embedding_dimension_explicit():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"], embedding_dimension=384)
    assert summary["embedding_dimension"] == 384


def test_summary_word_stats_non_zero():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"])
    assert summary["average_chunk_words"] > 0
    assert summary["min_chunk_words"] > 0
    assert summary["max_chunk_words"] > 0


def test_summary_min_le_avg_le_max():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], r["model_name"])
    assert summary["min_chunk_words"] <= summary["average_chunk_words"]
    assert summary["average_chunk_words"] <= summary["max_chunk_words"]


def test_summary_empty_chunks_safe():
    summary = get_embedding_summary([], "test-model")
    assert summary["chunk_count"] == 0
    assert summary["documents_embedded"] == 0
    assert summary["average_chunk_words"] == 0


def test_summary_empty_chunks_returns_dict():
    summary = get_embedding_summary([], "test-model")
    assert isinstance(summary, dict)


def test_summary_model_name_stored():
    r = _make_embedded()
    summary = get_embedding_summary(r["embedded_chunks"], "my-named-model")
    assert summary["model_name"] == "my-named-model"
