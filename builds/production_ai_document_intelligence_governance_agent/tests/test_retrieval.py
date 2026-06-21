"""Tests for logic/vector_index.py and logic/retrieval.py — Phase 3.

Uses FakeModel to avoid downloading sentence-transformers during testing.
All tests are deterministic and require no internet access.
"""

import numpy as np
import pytest

from logic.embeddings import embed_chunks, embed_query
from logic.retrieval import (
    WEAK_SCORE_THRESHOLD,
    _score_label,
    format_results_for_display,
    is_retrieval_weak,
    retrieve,
)
from logic.vector_index import build_index, index_summary, search_index

DIM = 16


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


SAMPLE_CHUNKS = [
    {
        "chunk_id": "policy_chunk_000",
        "document_id": "ai-policy",
        "source_name": "ai-policy.md",
        "chunk_index": 0,
        "text": "Staff must not enter learner names or reference numbers into AI tools.",
        "word_count": 12,
        "start_word": 0,
        "end_word": 11,
        "metadata": {},
    },
    {
        "chunk_id": "policy_chunk_001",
        "document_id": "ai-policy",
        "source_name": "ai-policy.md",
        "chunk_index": 1,
        "text": "Human review is required before any AI-generated content is shared.",
        "word_count": 11,
        "start_word": 160,
        "end_word": 170,
        "metadata": {},
    },
    {
        "chunk_id": "guidance_chunk_000",
        "document_id": "staff-guidance",
        "source_name": "staff-guidance.md",
        "chunk_index": 0,
        "text": "Safeguarding matters must never be processed using AI tools.",
        "word_count": 10,
        "start_word": 0,
        "end_word": 9,
        "metadata": {},
    },
]


@pytest.fixture
def model():
    return FakeModel()


@pytest.fixture
def embeddings(model):
    return embed_chunks(SAMPLE_CHUNKS, model)


@pytest.fixture
def index(embeddings):
    return build_index(embeddings)


# ---------------------------------------------------------------------------
# build_index
# ---------------------------------------------------------------------------


def test_build_index_returns_index_object(embeddings):
    idx = build_index(embeddings)
    assert idx is not None


def test_build_index_ntotal_matches_chunk_count(embeddings):
    idx = build_index(embeddings)
    assert idx.ntotal == len(SAMPLE_CHUNKS)


def test_build_index_accepts_float32(model):
    emb = embed_chunks(SAMPLE_CHUNKS, model)
    assert emb.dtype == np.float32
    idx = build_index(emb)
    assert idx.ntotal == len(SAMPLE_CHUNKS)


# ---------------------------------------------------------------------------
# search_index
# ---------------------------------------------------------------------------


def test_search_index_returns_list(index, model):
    query_emb = embed_query("learner data policy", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    assert isinstance(results, list)


def test_search_index_returns_at_most_top_k(index, model):
    query_emb = embed_query("learner data policy", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=2)
    assert len(results) <= 2


def test_search_index_returns_all_when_top_k_exceeds_chunks(index, model):
    query_emb = embed_query("policy", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=100)
    assert len(results) == len(SAMPLE_CHUNKS)


def test_search_index_results_have_score(index, model):
    query_emb = embed_query("learner data", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    assert all("score" in r for r in results)


def test_search_index_results_have_rank(index, model):
    query_emb = embed_query("safeguarding", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    assert all("rank" in r for r in results)


def test_search_index_rank_starts_at_one(index, model):
    query_emb = embed_query("human review", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    assert results[0]["rank"] == 1


def test_search_index_ranks_are_sequential(index, model):
    query_emb = embed_query("ai tools", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    ranks = [r["rank"] for r in results]
    assert ranks == list(range(1, len(results) + 1))


def test_search_index_sorted_by_score_descending(index, model):
    query_emb = embed_query("learner names", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_search_index_results_have_chunk_id(index, model):
    query_emb = embed_query("policy", model)
    results = search_index(index, query_emb, SAMPLE_CHUNKS, top_k=3)
    assert all("chunk_id" in r for r in results)


def test_search_index_empty_chunks_returns_empty(index, model):
    query_emb = embed_query("query", model)
    results = search_index(index, query_emb, [], top_k=3)
    assert results == []


# ---------------------------------------------------------------------------
# index_summary
# ---------------------------------------------------------------------------


def test_index_summary_returns_dict(index, embeddings):
    summary = index_summary(index, embeddings)
    assert isinstance(summary, dict)


def test_index_summary_total_vectors(index, embeddings):
    summary = index_summary(index, embeddings)
    assert summary["total_vectors"] == len(SAMPLE_CHUNKS)


def test_index_summary_embedding_dimension(index, embeddings):
    summary = index_summary(index, embeddings)
    assert summary["embedding_dimension"] == DIM


def test_index_summary_index_type(index, embeddings):
    summary = index_summary(index, embeddings)
    assert summary["index_type"] == "IndexFlatIP"


# ---------------------------------------------------------------------------
# retrieve
# ---------------------------------------------------------------------------


def test_retrieve_returns_list(model, index):
    results = retrieve("learner data", model, index, SAMPLE_CHUNKS)
    assert isinstance(results, list)


def test_retrieve_empty_chunks_returns_empty(model, index):
    results = retrieve("any query", model, index, [])
    assert results == []


def test_retrieve_results_include_is_weak(model, index):
    results = retrieve("learner names", model, index, SAMPLE_CHUNKS)
    assert all("is_weak" in r for r in results)


def test_retrieve_is_weak_flag_type(model, index):
    results = retrieve("safeguarding", model, index, SAMPLE_CHUNKS)
    assert all(isinstance(r["is_weak"], bool) for r in results)


def test_retrieve_respects_top_k(model, index):
    results = retrieve("policy", model, index, SAMPLE_CHUNKS, top_k=2)
    assert len(results) <= 2


# ---------------------------------------------------------------------------
# is_retrieval_weak
# ---------------------------------------------------------------------------


def test_is_retrieval_weak_empty_returns_true():
    assert is_retrieval_weak([]) is True


def test_is_retrieval_weak_low_score_returns_true():
    results = [{"score": 0.1, "rank": 1}]
    assert is_retrieval_weak(results, threshold=0.25) is True


def test_is_retrieval_weak_high_score_returns_false():
    results = [{"score": 0.8, "rank": 1}]
    assert is_retrieval_weak(results, threshold=0.25) is False


def test_is_retrieval_weak_boundary_score():
    results = [{"score": 0.25, "rank": 1}]
    assert is_retrieval_weak(results, threshold=0.25) is False


# ---------------------------------------------------------------------------
# format_results_for_display
# ---------------------------------------------------------------------------


def test_format_results_includes_score_pct():
    results = [{"chunk_id": "c1", "text": "hello", "score": 0.75, "rank": 1, "is_weak": False}]
    formatted = format_results_for_display(results)
    assert "score_pct" in formatted[0]


def test_format_results_score_pct_format():
    results = [{"chunk_id": "c1", "text": "hello", "score": 0.756, "rank": 1, "is_weak": False}]
    formatted = format_results_for_display(results)
    assert formatted[0]["score_pct"] == "75.6%"


def test_format_results_includes_score_label():
    results = [{"chunk_id": "c1", "text": "hello", "score": 0.6, "rank": 1, "is_weak": False}]
    formatted = format_results_for_display(results)
    assert "score_label" in formatted[0]


def test_format_results_empty_input():
    assert format_results_for_display([]) == []


# ---------------------------------------------------------------------------
# _score_label
# ---------------------------------------------------------------------------


def test_score_label_strong():
    assert _score_label(0.75) == "Strong"


def test_score_label_good():
    assert _score_label(0.55) == "Good"


def test_score_label_moderate():
    assert _score_label(0.30) == "Moderate"


def test_score_label_weak():
    assert _score_label(0.10) == "Weak"
