"""Tests for src/comparison.py — Phase 7: Retrieval Comparison."""

import pytest

faiss = pytest.importorskip("faiss")

from src.comparison import (
    summarise_keyword_results,
    summarise_semantic_results,
    find_overlap_between_results,
    generate_retrieval_comparison_insight,
    generate_retrieval_comparison_markdown,
    compare_retrieval_methods,
)


# ── Fake helpers ──────────────────────────────────────────────────────────────


def _fake_chunks(n=5):
    return [
        {
            "chunk_id": f"doc-a__chunk_{i:03d}",
            "document_name": "doc-a.md",
            "chunk_index": i,
            "text": f"Policy text about learner data and safeguarding chunk {i}",
            "word_count": 10,
            "character_count": 50,
            "start_word": i * 10,
            "end_word": (i + 1) * 10,
            "chunk_size": 10,
            "overlap": 2,
            "strategy": "word",
        }
        for i in range(n)
    ]


def _fake_keyword_results(n=3):
    return [
        {
            "chunk_id": f"doc-a__chunk_{i:03d}",
            "document_name": "doc-a.md",
            "chunk_index": i,
            "text": f"Policy text chunk {i}",
            "word_count": 8,
            "score": 3 - i,
            "matched_terms": ["learner", "data", "policy"],
        }
        for i in range(n)
    ]


def _fake_semantic_results(n=3, id_prefix="doc-b"):
    return [
        {
            "rank": i + 1,
            "score": round(0.9 - i * 0.1, 2),
            "chunk_id": f"{id_prefix}__chunk_{i:03d}",
            "document_name": f"{id_prefix}.md",
            "chunk_index": i,
            "text": f"Semantic chunk {i} about policy",
            "word_count": 8,
            "character_count": 40,
            "embedding_index": i,
            "source_label": f"From {id_prefix}.md · chunk {i}",
            "preview_text": f"Semantic chunk {i} about policy",
        }
        for i in range(n)
    ]


def _fake_vector_store():
    return {
        "index": object(),
        "embedded_chunks": _fake_chunks(),
        "metric": "cosine",
        "chunk_count": 5,
        "dimension": 4,
    }


def _make_fake_semantic_search(results=None):
    """Return a callable that mimics semantic_search without model downloads."""
    if results is None:
        results = _fake_semantic_results(3)

    def _fake(query, vector_store, model=None, model_name=None, top_k=5, normalise=True):
        return {
            "query": query,
            "model_name": "fake-model",
            "top_k": top_k,
            "results": results,
            "result_count": len(results),
            "query_embedding_dimension": 4,
            "metric": "cosine",
            "limitations": [],
        }

    return _fake


# ── TestSummariseKeywordResults ───────────────────────────────────────────────


class TestSummariseKeywordResults:
    def test_returns_dict(self):
        result = summarise_keyword_results([])
        assert isinstance(result, dict)

    def test_empty_list_result_count_zero(self):
        result = summarise_keyword_results([])
        assert result["result_count"] == 0

    def test_empty_list_has_expected_keys(self):
        result = summarise_keyword_results([])
        for key in ("result_count", "documents_found", "unique_documents", "top_score", "matched_terms", "method_note"):
            assert key in result

    def test_populated_result_count(self):
        result = summarise_keyword_results(_fake_keyword_results(3))
        assert result["result_count"] == 3

    def test_populated_unique_documents(self):
        kw = _fake_keyword_results(3)
        result = summarise_keyword_results(kw)
        assert result["unique_documents"] == 1

    def test_populated_top_score(self):
        kw = _fake_keyword_results(3)
        result = summarise_keyword_results(kw)
        assert result["top_score"] == 3

    def test_matched_terms_present(self):
        kw = _fake_keyword_results(3)
        result = summarise_keyword_results(kw)
        assert "learner" in result["matched_terms"]

    def test_method_note_present(self):
        result = summarise_keyword_results([])
        assert "Keyword retrieval" in result["method_note"]


# ── TestSummariseSemanticResults ──────────────────────────────────────────────


class TestSummariseSemanticResults:
    def test_returns_dict(self):
        result = summarise_semantic_results([])
        assert isinstance(result, dict)

    def test_empty_list_result_count_zero(self):
        result = summarise_semantic_results([])
        assert result["result_count"] == 0

    def test_empty_list_has_expected_keys(self):
        result = summarise_semantic_results([])
        for key in ("result_count", "documents_found", "unique_documents", "top_score", "method_note"):
            assert key in result

    def test_populated_result_count(self):
        result = summarise_semantic_results(_fake_semantic_results(3))
        assert result["result_count"] == 3

    def test_populated_unique_documents(self):
        result = summarise_semantic_results(_fake_semantic_results(3))
        assert result["unique_documents"] == 1

    def test_populated_top_score(self):
        sem = _fake_semantic_results(3)
        result = summarise_semantic_results(sem)
        assert result["top_score"] == pytest.approx(0.9, abs=0.01)

    def test_documents_found_present(self):
        sem = _fake_semantic_results(3)
        result = summarise_semantic_results(sem)
        assert len(result["documents_found"]) >= 1

    def test_method_note_present(self):
        result = summarise_semantic_results([])
        assert "Semantic retrieval" in result["method_note"]


# ── TestFindOverlapBetweenResults ─────────────────────────────────────────────


class TestFindOverlapBetweenResults:
    def test_returns_list(self):
        result = find_overlap_between_results([], [])
        assert isinstance(result, list)

    def test_empty_when_no_shared_ids(self):
        kw = _fake_keyword_results(3)
        sem = _fake_semantic_results(3, id_prefix="doc-b")
        result = find_overlap_between_results(kw, sem)
        assert result == []

    def test_detects_shared_chunk_id(self):
        kw = _fake_keyword_results(3)
        sem = _fake_semantic_results(3, id_prefix="doc-a")
        result = find_overlap_between_results(kw, sem)
        assert len(result) > 0

    def test_overlap_item_has_chunk_id(self):
        kw = _fake_keyword_results(3)
        sem = _fake_semantic_results(3, id_prefix="doc-a")
        result = find_overlap_between_results(kw, sem)
        assert "chunk_id" in result[0]

    def test_overlap_item_has_ranks(self):
        kw = _fake_keyword_results(3)
        sem = _fake_semantic_results(3, id_prefix="doc-a")
        result = find_overlap_between_results(kw, sem)
        assert "keyword_rank" in result[0]
        assert "semantic_rank" in result[0]

    def test_overlap_item_has_document_name(self):
        kw = _fake_keyword_results(3)
        sem = _fake_semantic_results(3, id_prefix="doc-a")
        result = find_overlap_between_results(kw, sem)
        assert "document_name" in result[0]


# ── TestGenerateRetrievalComparisonInsight ────────────────────────────────────


class TestGenerateRetrievalComparisonInsight:
    def _ks(self, n):
        return summarise_keyword_results(_fake_keyword_results(n))

    def _ss(self, n):
        return summarise_semantic_results(_fake_semantic_results(n))

    def test_semantic_only_mentions_semantic(self):
        insight = generate_retrieval_comparison_insight(
            "test query",
            summarise_keyword_results([]),
            self._ss(3),
            [],
        )
        assert "Semantic retrieval found evidence" in insight

    def test_both_with_overlap_mentions_both(self):
        kw = _fake_keyword_results(3)
        sem = _fake_semantic_results(3, id_prefix="doc-a")
        overlap = find_overlap_between_results(kw, sem)
        insight = generate_retrieval_comparison_insight(
            "test query", self._ks(3), self._ss(3), overlap
        )
        assert "Both retrieval methods" in insight

    def test_both_no_overlap_mentions_review(self):
        insight = generate_retrieval_comparison_insight(
            "test query", self._ks(3), self._ss(3), []
        )
        assert "Review both sets" in insight

    def test_neither_returns_rephrase_suggestion(self):
        insight = generate_retrieval_comparison_insight(
            "test query",
            summarise_keyword_results([]),
            summarise_semantic_results([]),
            [],
        )
        assert "Neither method" in insight

    def test_keyword_only_returns_string(self):
        insight = generate_retrieval_comparison_insight(
            "test query", self._ks(3), summarise_semantic_results([]), []
        )
        assert isinstance(insight, str)
        assert len(insight) > 0


# ── TestGenerateRetrievalComparisonMarkdown ───────────────────────────────────


class TestGenerateRetrievalComparisonMarkdown:
    def _sample_result(self):
        kw = _fake_keyword_results(2)
        sem = _fake_semantic_results(2)
        ks = summarise_keyword_results(kw)
        ss = summarise_semantic_results(sem)
        overlap = find_overlap_between_results(kw, sem)
        insight = generate_retrieval_comparison_insight("test", ks, ss, overlap)
        from src.comparison import _LIMITATIONS
        return {
            "query": "test query",
            "top_k": 5,
            "keyword_results": kw,
            "semantic_results": sem,
            "keyword_summary": ks,
            "semantic_summary": ss,
            "overlap": overlap,
            "comparison_insight": insight,
            "limitations": _LIMITATIONS,
        }

    def test_returns_string(self):
        assert isinstance(generate_retrieval_comparison_markdown(self._sample_result()), str)

    def test_has_main_header(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "# Retrieval Comparison Report" in md

    def test_has_query_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Query" in md

    def test_has_keyword_summary_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Keyword Retrieval Summary" in md

    def test_has_semantic_summary_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Semantic Retrieval Summary" in md

    def test_has_overlapping_results_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Overlapping Results" in md

    def test_has_comparison_insight_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Comparison Insight" in md

    def test_has_keyword_results_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Keyword Results" in md

    def test_has_semantic_results_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Semantic Results" in md

    def test_has_limitations_section(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "## Limitations" in md

    def test_query_text_appears_in_output(self):
        md = generate_retrieval_comparison_markdown(self._sample_result())
        assert "test query" in md


# ── TestCompareRetrievalMethods ───────────────────────────────────────────────


class TestCompareRetrievalMethods:
    def test_returns_dict(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert isinstance(result, dict)

    def test_has_query_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert result["query"] == "learner"

    def test_has_keyword_results_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "keyword_results" in result
        assert isinstance(result["keyword_results"], list)

    def test_has_semantic_results_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "semantic_results" in result
        assert isinstance(result["semantic_results"], list)

    def test_has_keyword_summary_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "keyword_summary" in result
        assert isinstance(result["keyword_summary"], dict)

    def test_has_semantic_summary_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "semantic_summary" in result
        assert isinstance(result["semantic_summary"], dict)

    def test_has_overlap_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "overlap" in result
        assert isinstance(result["overlap"], list)

    def test_has_comparison_insight_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "comparison_insight" in result
        assert isinstance(result["comparison_insight"], str)

    def test_has_limitations_key(self, monkeypatch):
        monkeypatch.setattr("src.comparison.semantic_search", _make_fake_semantic_search())
        result = compare_retrieval_methods("learner", _fake_chunks(), _fake_vector_store())
        assert "limitations" in result
        assert isinstance(result["limitations"], list)
        assert len(result["limitations"]) > 0
