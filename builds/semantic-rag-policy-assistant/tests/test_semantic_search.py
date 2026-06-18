"""Tests for src/semantic_search.py — Phase 5.

All tests use FakeModel (no sentence-transformers downloads) and fake numpy arrays.
Requires faiss-cpu to be installed — skipped otherwise.
"""

import numpy as np
import pytest

faiss = pytest.importorskip("faiss")

from src.semantic_search import (
    validate_semantic_search_inputs,
    embed_query,
    format_semantic_search_results,
    semantic_search,
)
from src.vector_store import create_vector_store


# ── Fake helpers ───────────────────────────────────────────────────────────────

class FakeModel:
    """Sentence-transformers lookalike — no internet or model downloads required."""

    def encode(self, texts, normalize_embeddings=True):
        n = len(texts)
        m = np.tile([0.25, 0.50, 0.75, 1.00], (n, 1)).astype(np.float32)
        if normalize_embeddings:
            norms = np.linalg.norm(m, axis=1, keepdims=True)
            m = m / norms
        return m


def _fake_matrix(n=5, dim=4):
    rng = np.random.default_rng(42)
    m = rng.random((n, dim)).astype(np.float32)
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / norms


def _fake_chunks(n=5):
    return [
        {
            "chunk_id": f"doc-{i % 2}__chunk_{i:03d}",
            "document_name": f"doc-{i % 2}.md",
            "chunk_index": i,
            "text": f"Synthetic policy chunk number {i} for testing purposes only.",
            "word_count": 10,
            "character_count": 55,
            "embedding_index": i,
            "embedding_vector": [0.1, 0.2, 0.3, 0.4],
        }
        for i in range(n)
    ]


def _fake_vector_store(n=5, dim=4):
    matrix = _fake_matrix(n, dim)
    chunks = _fake_chunks(n)
    return create_vector_store(chunks, matrix, metric="cosine")


# ── TestValidateSemanticSearchInputs ──────────────────────────────────────────

class TestValidateSemanticSearchInputs:

    def test_rejects_empty_string_query(self):
        vs = _fake_vector_store()
        valid, msg = validate_semantic_search_inputs("", vs)
        assert not valid

    def test_empty_query_message_mentions_empty(self):
        vs = _fake_vector_store()
        _, msg = validate_semantic_search_inputs("", vs)
        assert "empty" in msg.lower()

    def test_rejects_whitespace_only_query(self):
        vs = _fake_vector_store()
        valid, _ = validate_semantic_search_inputs("   ", vs)
        assert not valid

    def test_rejects_none_vector_store(self):
        valid, msg = validate_semantic_search_inputs("valid query", None)
        assert not valid

    def test_missing_vector_store_message_is_readable(self):
        _, msg = validate_semantic_search_inputs("valid query", None)
        assert "vector store" in msg.lower()

    def test_rejects_empty_dict_vector_store(self):
        valid, _ = validate_semantic_search_inputs("valid query", {})
        assert not valid

    def test_rejects_vector_store_with_none_index(self):
        valid, _ = validate_semantic_search_inputs("valid query", {"index": None})
        assert not valid

    def test_accepts_valid_query_and_vector_store(self):
        vs = _fake_vector_store()
        valid, msg = validate_semantic_search_inputs("What is the safeguarding policy?", vs)
        assert valid

    def test_valid_message_is_readable(self):
        vs = _fake_vector_store()
        _, msg = validate_semantic_search_inputs("test", vs)
        assert isinstance(msg, str) and len(msg) > 0

    def test_returns_tuple_of_two_elements(self):
        vs = _fake_vector_store()
        result = validate_semantic_search_inputs("test", vs)
        assert len(result) == 2


# ── TestEmbedQuery ─────────────────────────────────────────────────────────────

class TestEmbedQuery:

    def test_returns_dict(self):
        result = embed_query("test query", model=FakeModel())
        assert isinstance(result, dict)

    def test_returns_all_expected_keys(self):
        result = embed_query("test query", model=FakeModel())
        expected = {"query", "model_name", "embedding", "embedding_dimension", "normalised"}
        assert expected.issubset(result.keys())

    def test_embedding_is_numpy_array(self):
        result = embed_query("test query", model=FakeModel())
        assert isinstance(result["embedding"], np.ndarray)

    def test_embedding_is_2d(self):
        result = embed_query("test query", model=FakeModel())
        assert result["embedding"].ndim == 2

    def test_embedding_first_dimension_is_1(self):
        result = embed_query("test query", model=FakeModel())
        assert result["embedding"].shape[0] == 1

    def test_embedding_dimension_matches_shape(self):
        result = embed_query("test query", model=FakeModel())
        assert result["embedding_dimension"] == result["embedding"].shape[1]

    def test_embedding_dimension_is_positive(self):
        result = embed_query("test query", model=FakeModel())
        assert result["embedding_dimension"] > 0

    def test_stores_original_query(self):
        q = "Can staff share learner data?"
        result = embed_query(q, model=FakeModel())
        assert result["query"] == q

    def test_normalised_flag_stored_true(self):
        result = embed_query("test", model=FakeModel(), normalise=True)
        assert result["normalised"] is True

    def test_normalised_flag_stored_false(self):
        result = embed_query("test", model=FakeModel(), normalise=False)
        assert result["normalised"] is False

    def test_custom_model_name_stored(self):
        result = embed_query("test", model=FakeModel(), model_name="custom/model-v1")
        assert result["model_name"] == "custom/model-v1"

    def test_embedding_dtype_is_float32(self):
        result = embed_query("test", model=FakeModel())
        assert result["embedding"].dtype == np.float32

    def test_raises_value_error_on_empty_query(self):
        with pytest.raises(ValueError):
            embed_query("", model=FakeModel())

    def test_raises_value_error_on_whitespace_query(self):
        with pytest.raises(ValueError):
            embed_query("   ", model=FakeModel())

    def test_default_model_name_used_when_none_provided(self):
        from src.embedding_engine import get_default_embedding_model_name
        result = embed_query("test", model=FakeModel())
        assert result["model_name"] == get_default_embedding_model_name()


# ── TestFormatSemanticSearchResults ───────────────────────────────────────────

class TestFormatSemanticSearchResults:

    def _sample_result(self):
        return {
            "rank": 1,
            "score": 0.95,
            "chunk_id": "doc-0__chunk_000",
            "document_name": "policy-doc.md",
            "chunk_index": 3,
            "text": "This is a test chunk about safeguarding policy content.",
            "word_count": 9,
            "character_count": 55,
            "embedding_index": 0,
        }

    def test_returns_list(self):
        assert isinstance(format_semantic_search_results([]), list)

    def test_empty_input_returns_empty_list(self):
        assert format_semantic_search_results([]) == []

    def test_adds_source_label(self):
        results = format_semantic_search_results([self._sample_result()])
        assert "source_label" in results[0]

    def test_source_label_contains_document_name(self):
        results = format_semantic_search_results([self._sample_result()])
        assert "policy-doc.md" in results[0]["source_label"]

    def test_source_label_contains_chunk_index(self):
        results = format_semantic_search_results([self._sample_result()])
        assert "3" in results[0]["source_label"]

    def test_adds_preview_text(self):
        results = format_semantic_search_results([self._sample_result()])
        assert "preview_text" in results[0]

    def test_preview_text_truncates_long_text(self):
        long_result = self._sample_result()
        long_result["text"] = "word " * 100
        results = format_semantic_search_results([long_result])
        assert results[0]["preview_text"].endswith("...")
        assert len(results[0]["preview_text"]) <= 203

    def test_short_text_not_truncated(self):
        results = format_semantic_search_results([self._sample_result()])
        assert not results[0]["preview_text"].endswith("...")

    def test_does_not_mutate_original_dicts(self):
        original = self._sample_result()
        original_keys = set(original.keys())
        format_semantic_search_results([original])
        assert set(original.keys()) == original_keys

    def test_preserves_rank_and_score(self):
        results = format_semantic_search_results([self._sample_result()])
        assert results[0]["rank"] == 1
        assert results[0]["score"] == 0.95

    def test_preserves_chunk_id_and_text(self):
        results = format_semantic_search_results([self._sample_result()])
        assert results[0]["chunk_id"] == "doc-0__chunk_000"
        assert "test chunk" in results[0]["text"]


# ── TestSemanticSearch ─────────────────────────────────────────────────────────

class TestSemanticSearch:

    def test_returns_dict(self):
        vs = _fake_vector_store()
        result = semantic_search("policy question", vs, model=FakeModel())
        assert isinstance(result, dict)

    def test_returns_all_expected_keys(self):
        vs = _fake_vector_store()
        result = semantic_search("policy question", vs, model=FakeModel())
        expected = {
            "query", "model_name", "top_k", "results",
            "result_count", "query_embedding_dimension", "metric", "limitations",
        }
        assert expected.issubset(result.keys())

    def test_stores_original_query(self):
        vs = _fake_vector_store()
        q = "What is the safeguarding policy?"
        result = semantic_search(q, vs, model=FakeModel())
        assert result["query"] == q

    def test_result_count_matches_results_length(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert result["result_count"] == len(result["results"])

    def test_top_k_stored_in_output(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        assert result["top_k"] == 3

    def test_results_capped_at_chunk_count(self):
        vs = _fake_vector_store(n=3)
        result = semantic_search("test", vs, model=FakeModel(), top_k=10)
        assert result["result_count"] <= 3

    def test_each_result_has_rank(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        for r in result["results"]:
            assert "rank" in r

    def test_each_result_has_score(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        for r in result["results"]:
            assert "score" in r

    def test_each_result_has_chunk_id(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        for r in result["results"]:
            assert "chunk_id" in r

    def test_each_result_has_document_name(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        for r in result["results"]:
            assert "document_name" in r

    def test_each_result_has_text(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        for r in result["results"]:
            assert "text" in r

    def test_each_result_has_source_label(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        for r in result["results"]:
            assert "source_label" in r

    def test_limitations_is_non_empty_list(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert isinstance(result["limitations"], list)
        assert len(result["limitations"]) > 0

    def test_limitations_contains_synthetic_docs_notice(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert any("synthetic" in lim.lower() for lim in result["limitations"])

    def test_limitations_contains_review_notice(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert any("review" in lim.lower() for lim in result["limitations"])

    def test_raises_on_empty_query(self):
        vs = _fake_vector_store()
        with pytest.raises(ValueError):
            semantic_search("", vs, model=FakeModel())

    def test_raises_on_none_vector_store(self):
        with pytest.raises(ValueError):
            semantic_search("test", None, model=FakeModel())

    def test_metric_matches_vector_store(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert result["metric"] == vs["metric"]

    def test_query_embedding_dimension_is_positive(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert result["query_embedding_dimension"] > 0

    def test_first_result_rank_is_1(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel(), top_k=3)
        if result["results"]:
            assert result["results"][0]["rank"] == 1

    def test_results_is_list(self):
        vs = _fake_vector_store()
        result = semantic_search("test", vs, model=FakeModel())
        assert isinstance(result["results"], list)
