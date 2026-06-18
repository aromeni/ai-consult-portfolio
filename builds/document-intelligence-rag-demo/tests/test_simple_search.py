"""
Tests for src/simple_search.py

Run from the project root:  pytest
"""

from src.simple_search import (
    normalise_text,
    tokenise_query,
    search_document,
    search_documents,
)

SAMPLE_TEXT = """\
This is a test document about AI policy.
Staff must not enter learner data into AI tools.
Safeguarding information must never be shared with AI tools.
Human review is required for all AI-generated outputs.
Only approved tools may be used for work purposes.
Contact your manager if you are unsure about any AI use.
This policy applies to all staff members without exception.
"""


# ── normalise_text ────────────────────────────────────────────────────────────

def test_normalise_text_returns_lowercase():
    assert normalise_text("SAFEGUARDING") == "safeguarding"


def test_normalise_text_strips_leading_and_trailing_whitespace():
    assert normalise_text("  learner data  ") == "learner data"


def test_normalise_text_empty_string_returns_empty():
    assert normalise_text("") == ""


def test_normalise_text_returns_string():
    assert isinstance(normalise_text("Test"), str)


# ── tokenise_query ────────────────────────────────────────────────────────────

def test_tokenise_query_returns_list():
    assert isinstance(tokenise_query("safeguarding"), list)


def test_tokenise_query_splits_on_whitespace():
    result = tokenise_query("learner data")
    assert "learner" in result
    assert "data" in result


def test_tokenise_query_is_lowercase():
    result = tokenise_query("Safeguarding Learner Data")
    assert all(t == t.lower() for t in result)


def test_tokenise_query_filters_stop_words():
    result = tokenise_query("what does the policy say about learner data")
    assert "what" not in result
    assert "the" not in result
    assert "does" not in result
    assert "say" not in result
    assert "learner" in result
    assert "data" in result


def test_tokenise_query_preserves_meaningful_policy_terms():
    result = tokenise_query("safeguarding learner data human review")
    assert "safeguarding" in result
    assert "learner" in result
    assert "data" in result
    assert "human" in result
    assert "review" in result


def test_tokenise_query_empty_string_returns_empty_list():
    assert tokenise_query("") == []


def test_tokenise_query_whitespace_only_returns_empty_list():
    assert tokenise_query("   ") == []


def test_tokenise_query_stop_words_only_returns_empty_list():
    assert tokenise_query("what does the") == []


# ── search_document ───────────────────────────────────────────────────────────

def test_search_document_returns_list():
    assert isinstance(search_document(SAMPLE_TEXT, "learner data"), list)


def test_search_document_finds_keyword():
    results = search_document(SAMPLE_TEXT, "learner data")
    assert len(results) >= 1


def test_search_document_result_has_required_keys():
    results = search_document(SAMPLE_TEXT, "safeguarding")
    assert results
    for key in ("document_name", "line_number", "snippet", "relevance_count", "matched_terms"):
        assert key in results[0], f"Missing key: {key}"


def test_search_document_is_case_insensitive():
    assert len(search_document(SAMPLE_TEXT, "SAFEGUARDING")) >= 1
    assert len(search_document(SAMPLE_TEXT, "Safeguarding")) >= 1


def test_search_document_no_match_returns_empty_list():
    assert search_document(SAMPLE_TEXT, "blockchain") == []


def test_search_document_empty_query_returns_empty_list():
    assert search_document(SAMPLE_TEXT, "") == []


def test_search_document_whitespace_query_returns_empty_list():
    assert search_document(SAMPLE_TEXT, "   ") == []


def test_search_document_relevance_count_is_positive_integer():
    results = search_document(SAMPLE_TEXT, "ai")
    for r in results:
        assert isinstance(r["relevance_count"], int)
        assert r["relevance_count"] >= 1


def test_search_document_line_number_is_one_based():
    results = search_document(SAMPLE_TEXT, "test document")
    assert results
    assert results[0]["line_number"] == 1


def test_search_document_snippet_contains_a_query_term():
    results = search_document(SAMPLE_TEXT, "approved tools")
    assert any("approved" in r["snippet"].lower() or "tools" in r["snippet"].lower()
               for r in results)


def test_search_document_matched_terms_is_list():
    results = search_document(SAMPLE_TEXT, "safeguarding")
    assert results
    assert isinstance(results[0]["matched_terms"], list)


def test_search_document_matched_terms_contains_expected_term():
    results = search_document(SAMPLE_TEXT, "safeguarding")
    assert results
    assert "safeguarding" in results[0]["matched_terms"]


def test_search_document_document_name_uses_provided_value():
    results = search_document(SAMPLE_TEXT, "safeguarding", document_name="policy.md")
    assert results
    assert results[0]["document_name"] == "policy.md"


def test_search_document_document_name_defaults_to_empty_string():
    results = search_document(SAMPLE_TEXT, "safeguarding")
    assert results
    assert results[0]["document_name"] == ""


def test_search_document_deduplicates_identical_snippets():
    repeated_text = "Safeguarding is important.\nSafeguarding is important.\n"
    results = search_document(repeated_text, "safeguarding")
    snippets = [r["snippet"] for r in results]
    assert len(snippets) == len(set(snippets))


def test_search_document_multi_term_query_finds_more_results():
    single = search_document(SAMPLE_TEXT, "safeguarding")
    multi  = search_document(SAMPLE_TEXT, "safeguarding learner")
    assert len(multi) >= len(single)


# ── search_documents ──────────────────────────────────────────────────────────

def test_search_documents_returns_list():
    docs = {"doc_a.md": SAMPLE_TEXT, "doc_b.md": SAMPLE_TEXT}
    assert isinstance(search_documents(docs, "safeguarding"), list)


def test_search_documents_result_has_all_required_keys():
    docs = {"policy.md": SAMPLE_TEXT}
    results = search_documents(docs, "safeguarding")
    assert results
    for key in ("document_name", "line_number", "snippet", "relevance_count", "matched_terms"):
        assert key in results[0], f"Missing key: {key}"


def test_search_documents_includes_document_name():
    docs = {"policy.md": SAMPLE_TEXT}
    results = search_documents(docs, "safeguarding")
    assert results
    assert results[0]["document_name"] == "policy.md"


def test_search_documents_finds_matches_across_multiple_docs():
    docs = {
        "doc_a.md": SAMPLE_TEXT,
        "doc_b.md": "Human review is essential for safe AI use. Review everything.",
    }
    results = search_documents(docs, "human review")
    doc_names_found = {r["document_name"] for r in results}
    assert "doc_a.md" in doc_names_found
    assert "doc_b.md" in doc_names_found


def test_search_documents_excludes_non_matching_docs():
    docs = {
        "match.md": "Safeguarding is a core principle.",
        "no_match.md": "Completely unrelated content about office supplies.",
    }
    results = search_documents(docs, "safeguarding")
    doc_names_found = [r["document_name"] for r in results]
    assert "no_match.md" not in doc_names_found


def test_search_documents_sorted_by_relevance_count_descending():
    docs = {
        "high.md": "safeguarding safeguarding safeguarding — three occurrences.",
        "low.md": "one mention of safeguarding here.",
    }
    results = search_documents(docs, "safeguarding")
    assert len(results) >= 2
    assert results[0]["relevance_count"] >= results[1]["relevance_count"]


def test_search_documents_empty_dict_returns_empty_list():
    assert search_documents({}, "safeguarding") == []


def test_search_documents_stop_word_only_query_returns_empty_list():
    docs = {"doc.md": SAMPLE_TEXT}
    assert search_documents(docs, "what the") == []
