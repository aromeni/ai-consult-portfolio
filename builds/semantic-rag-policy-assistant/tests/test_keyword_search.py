"""Tests for src/keyword_search.py."""

import os
import pytest
from src.keyword_search import tokenise_query, keyword_search_chunks
from src.chunker import chunk_documents
from src.document_loader import load_all_documents

SYNTHETIC_DOCS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "synthetic_documents"
)


def get_chunks():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    return chunk_documents(docs, chunk_size=300, overlap=50)


# ── tokenise_query ────────────────────────────────────────────────────────────

def test_tokenise_returns_list():
    assert isinstance(tokenise_query("safeguarding policy"), list)


def test_tokenise_lowercase():
    result = tokenise_query("Safeguarding POLICY")
    assert all(t == t.lower() for t in result)


def test_tokenise_removes_stopwords():
    result = tokenise_query("the policy is about safeguarding")
    assert "the" not in result
    assert "is" not in result
    assert "about" not in result


def test_tokenise_keeps_meaningful_terms():
    result = tokenise_query("safeguarding learner data")
    assert "safeguarding" in result
    assert "learner" in result
    assert "data" in result


def test_tokenise_empty_string_returns_empty():
    assert tokenise_query("") == []


def test_tokenise_whitespace_returns_empty():
    assert tokenise_query("   ") == []


def test_tokenise_punctuation_stripped():
    result = tokenise_query("safeguarding, policy!")
    assert "safeguarding," not in result
    assert "policy!" not in result


def test_tokenise_single_char_removed():
    result = tokenise_query("a b c safeguarding")
    for t in result:
        assert len(t) > 1


# ── keyword_search_chunks ─────────────────────────────────────────────────────

def test_search_returns_list():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "safeguarding", top_k=5)
    assert isinstance(result, list)


def test_search_finds_results_for_known_term():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "safeguarding", top_k=10)
    assert len(result) > 0


def test_search_result_has_required_keys():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "safeguarding", top_k=5)
    assert len(result) > 0
    for key in ("chunk_id", "document_name", "text", "score", "matched_terms"):
        assert key in result[0]


def test_search_results_have_positive_score():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "safeguarding learner", top_k=5)
    for r in result:
        assert r["score"] > 0


def test_search_results_sorted_by_score_desc():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "safeguarding learner data policy", top_k=10)
    scores = [r["score"] for r in result]
    assert scores == sorted(scores, reverse=True)


def test_search_matched_terms_non_empty():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "safeguarding", top_k=5)
    for r in result:
        assert len(r["matched_terms"]) > 0


def test_search_top_k_respected():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "policy data", top_k=3)
    assert len(result) <= 3


def test_search_empty_query_returns_empty():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "", top_k=5)
    assert result == []


def test_search_stopword_only_query_returns_empty():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "the and or", top_k=5)
    assert result == []


def test_search_no_match_returns_empty():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "zzzznotarealwordzzz", top_k=5)
    assert result == []


def test_search_empty_chunks_returns_empty():
    result = keyword_search_chunks([], "safeguarding", top_k=5)
    assert result == []


def test_search_learner_data_term():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "learner data", top_k=10)
    assert len(result) > 0


def test_search_hallucination_term():
    chunks = get_chunks()
    result = keyword_search_chunks(chunks, "hallucination", top_k=5)
    assert len(result) > 0
