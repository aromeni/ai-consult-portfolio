"""Tests for src/vector_store.py — Phase 4: FAISS vector index.

All tests use fake numpy arrays and fake chunk dicts.
No model downloads, no internet access, no sentence-transformers required.
"""

import pytest
import numpy as np

# Skip the entire module if faiss-cpu is not installed.
faiss = pytest.importorskip("faiss", reason="faiss-cpu not installed — run: pip install -r requirements.txt")

from src.vector_store import (
    validate_embedding_matrix,
    build_faiss_index,
    create_vector_store,
    search_vector_store,
    get_vector_store_summary,
    save_faiss_index,
    load_faiss_index,
)


# ── Test helpers ───────────────────────────────────────────────────────────────

def _fake_matrix(n: int = 5, dim: int = 4) -> np.ndarray:
    """Return a normalised float32 matrix with n rows and dim columns."""
    rng = np.random.default_rng(42)
    m = rng.random((n, dim)).astype(np.float32)
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / norms


def _fake_chunks(n: int = 5) -> list:
    """Return n fake chunk dicts with minimal required fields."""
    return [
        {
            "chunk_id": f"doc-{i % 2}__chunk_{i:03d}",
            "document_name": f"doc-{i % 2}.md",
            "chunk_index": i,
            "text": f"Synthetic policy chunk number {i} for testing purposes.",
            "word_count": 10,
            "character_count": 50,
            "embedding_index": i,
            "embedding_vector": [0.1, 0.2, 0.3, 0.4],
        }
        for i in range(n)
    ]


# ── validate_embedding_matrix ──────────────────────────────────────────────────

class TestValidateEmbeddingMatrix:

    def test_rejects_none_matrix(self):
        ok, msg = validate_embedding_matrix(None, _fake_chunks(3))
        assert not ok
        assert "None" in msg

    def test_rejects_empty_chunks(self):
        ok, msg = validate_embedding_matrix(_fake_matrix(3), [])
        assert not ok
        assert "chunk" in msg.lower()

    def test_rejects_mismatched_row_count(self):
        ok, msg = validate_embedding_matrix(_fake_matrix(3), _fake_chunks(5))
        assert not ok
        assert "3" in msg and "5" in msg

    def test_rejects_1d_matrix(self):
        m1d = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
        ok, msg = validate_embedding_matrix(m1d, _fake_chunks(1))
        assert not ok
        assert "dimension" in msg.lower()

    def test_rejects_zero_embedding_dimension(self):
        m = np.zeros((3, 0), dtype=np.float32)
        ok, msg = validate_embedding_matrix(m, _fake_chunks(3))
        assert not ok

    def test_accepts_valid_matrix_and_chunks(self):
        ok, msg = validate_embedding_matrix(_fake_matrix(5), _fake_chunks(5))
        assert ok

    def test_valid_message_contains_count_and_dimension(self):
        ok, msg = validate_embedding_matrix(_fake_matrix(5, 4), _fake_chunks(5))
        assert ok
        assert "5" in msg
        assert "4" in msg

    def test_returns_tuple(self):
        result = validate_embedding_matrix(_fake_matrix(3), _fake_chunks(3))
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_bool(self):
        ok, _ = validate_embedding_matrix(_fake_matrix(3), _fake_chunks(3))
        assert isinstance(ok, bool)

    def test_rejects_non_array_matrix(self):
        ok, msg = validate_embedding_matrix([[0.1, 0.2], [0.3, 0.4]], _fake_chunks(2))
        # Lists have no .shape attribute — should fail
        assert not ok


# ── build_faiss_index ──────────────────────────────────────────────────────────

class TestBuildFaissIndex:

    def test_builds_cosine_index(self):
        index = build_faiss_index(_fake_matrix(5, 4), metric="cosine")
        assert index is not None

    def test_cosine_index_has_correct_vector_count(self):
        index = build_faiss_index(_fake_matrix(5, 4), metric="cosine")
        assert index.ntotal == 5

    def test_builds_l2_index(self):
        index = build_faiss_index(_fake_matrix(5, 4), metric="l2")
        assert index is not None

    def test_l2_index_has_correct_vector_count(self):
        index = build_faiss_index(_fake_matrix(5, 4), metric="l2")
        assert index.ntotal == 5

    def test_default_metric_is_cosine(self):
        index = build_faiss_index(_fake_matrix(5, 4))
        assert index.ntotal == 5

    def test_index_dimension_matches_input(self):
        index = build_faiss_index(_fake_matrix(5, 8), metric="cosine")
        assert index.d == 8

    def test_single_vector_index(self):
        index = build_faiss_index(_fake_matrix(1, 4))
        assert index.ntotal == 1

    def test_raises_on_non_2d_matrix(self):
        with pytest.raises(ValueError):
            build_faiss_index(np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32))


# ── create_vector_store ────────────────────────────────────────────────────────

class TestCreateVectorStore:

    def test_returns_dict(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        assert isinstance(vs, dict)

    def test_returns_all_expected_keys(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        expected = {"index", "embedded_chunks", "embedding_matrix", "metric",
                    "dimension", "chunk_count", "document_count", "index_type"}
        assert expected.issubset(vs.keys())

    def test_chunk_count_matches_input(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        assert vs["chunk_count"] == 5

    def test_default_metric_is_cosine(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        assert vs["metric"] == "cosine"

    def test_cosine_uses_indexflatip(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4), metric="cosine")
        assert vs["index_type"] == "IndexFlatIP"

    def test_l2_uses_indexflatl2(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4), metric="l2")
        assert vs["metric"] == "l2"
        assert vs["index_type"] == "IndexFlatL2"

    def test_dimension_matches_matrix(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 8))
        assert vs["dimension"] == 8

    def test_document_count_is_unique_documents(self):
        # _fake_chunks(5) alternates doc-0.md and doc-1.md → 2 unique docs
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        assert vs["document_count"] == 2

    def test_raises_on_mismatched_count(self):
        with pytest.raises(ValueError):
            create_vector_store(_fake_chunks(3), _fake_matrix(5, 4))

    def test_raises_on_none_matrix(self):
        with pytest.raises(ValueError):
            create_vector_store(_fake_chunks(3), None)

    def test_index_is_populated(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        assert vs["index"].ntotal == 5


# ── get_vector_store_summary ───────────────────────────────────────────────────

class TestGetVectorStoreSummary:

    def test_returns_expected_keys(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        summary = get_vector_store_summary(vs)
        expected = {"index_type", "metric", "chunk_count", "document_count",
                    "dimension", "is_trained", "total_vectors", "documents_indexed"}
        assert expected.issubset(summary.keys())

    def test_empty_dict_returns_safe_defaults(self):
        summary = get_vector_store_summary({})
        assert summary["chunk_count"] == 0
        assert summary["total_vectors"] == 0
        assert summary["is_trained"] is False
        assert summary["documents_indexed"] == []

    def test_total_vectors_matches_chunk_count(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        summary = get_vector_store_summary(vs)
        assert summary["total_vectors"] == 5
        assert summary["chunk_count"] == 5

    def test_is_trained_true_for_flat_index(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        summary = get_vector_store_summary(vs)
        assert summary["is_trained"] is True

    def test_documents_indexed_is_sorted_list(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 4))
        summary = get_vector_store_summary(vs)
        assert isinstance(summary["documents_indexed"], list)
        assert summary["documents_indexed"] == sorted(summary["documents_indexed"])

    def test_dimension_reported_correctly(self):
        vs = create_vector_store(_fake_chunks(5), _fake_matrix(5, 8))
        summary = get_vector_store_summary(vs)
        assert summary["dimension"] == 8


# ── search_vector_store ────────────────────────────────────────────────────────

class TestSearchVectorStore:

    def setup_method(self):
        self.chunks = _fake_chunks(5)
        self.matrix = _fake_matrix(5, 4)
        self.vs = create_vector_store(self.chunks, self.matrix)
        # Query using the first chunk's own vector — it should rank first.
        self.query = self.matrix[0]

    def test_returns_list(self):
        results = search_vector_store(self.vs, self.query, top_k=3)
        assert isinstance(results, list)

    def test_returns_correct_number_of_results(self):
        results = search_vector_store(self.vs, self.query, top_k=3)
        assert len(results) == 3

    def test_result_contains_required_fields(self):
        results = search_vector_store(self.vs, self.query, top_k=1)
        r = results[0]
        for field in ("rank", "score", "chunk_id", "document_name", "text",
                      "word_count", "character_count", "embedding_index"):
            assert field in r, f"Missing required field: {field}"

    def test_rank_starts_at_1(self):
        results = search_vector_store(self.vs, self.query, top_k=3)
        assert results[0]["rank"] == 1
        assert results[1]["rank"] == 2
        assert results[2]["rank"] == 3

    def test_top_k_larger_than_chunk_count_returns_all(self):
        results = search_vector_store(self.vs, self.query, top_k=100)
        assert len(results) == 5

    def test_top_1_returns_self_for_cosine(self):
        results = search_vector_store(self.vs, self.query, top_k=1)
        assert results[0]["chunk_id"] == self.chunks[0]["chunk_id"]

    def test_score_is_float(self):
        results = search_vector_store(self.vs, self.query, top_k=1)
        assert isinstance(results[0]["score"], float)

    def test_empty_vector_store_returns_empty_list(self):
        results = search_vector_store({}, self.query, top_k=5)
        assert results == []

    def test_chunk_ids_are_strings(self):
        results = search_vector_store(self.vs, self.query, top_k=5)
        for r in results:
            assert isinstance(r["chunk_id"], str)

    def test_document_name_is_string(self):
        results = search_vector_store(self.vs, self.query, top_k=5)
        for r in results:
            assert isinstance(r["document_name"], str)

    def test_text_field_is_non_empty_string(self):
        results = search_vector_store(self.vs, self.query, top_k=1)
        assert isinstance(results[0]["text"], str)
        assert len(results[0]["text"]) > 0

    def test_results_do_not_mutate_original_chunks(self):
        original_chunk_count = len(self.chunks)
        search_vector_store(self.vs, self.query, top_k=5)
        assert len(self.chunks) == original_chunk_count
        assert "rank" not in self.chunks[0]

    def test_1d_query_works(self):
        q_1d = self.matrix[0]
        assert q_1d.ndim == 1
        results = search_vector_store(self.vs, q_1d, top_k=3)
        assert len(results) == 3

    def test_top_k_zero_handled(self):
        results = search_vector_store(self.vs, self.query, top_k=0)
        # min(0, chunk_count) = 0, so result should be empty
        assert results == []


# ── save / load ────────────────────────────────────────────────────────────────

class TestSaveLoadFaissIndex:

    def test_save_and_load_roundtrip(self, tmp_path):
        index = build_faiss_index(_fake_matrix(5, 4), metric="cosine")
        path = str(tmp_path / "test.index")
        save_faiss_index(index, path)
        loaded = load_faiss_index(path)
        assert loaded.ntotal == 5

    def test_loaded_index_dimension_preserved(self, tmp_path):
        index = build_faiss_index(_fake_matrix(5, 8), metric="cosine")
        path = str(tmp_path / "test_dim.index")
        save_faiss_index(index, path)
        loaded = load_faiss_index(path)
        assert loaded.d == 8

    def test_loaded_index_is_searchable(self, tmp_path):
        matrix = _fake_matrix(5, 4)
        index = build_faiss_index(matrix, metric="cosine")
        path = str(tmp_path / "search.index")
        save_faiss_index(index, path)
        loaded = load_faiss_index(path)
        scores, indices = loaded.search(matrix[:1], 1)
        assert int(indices[0][0]) == 0
