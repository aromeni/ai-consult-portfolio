"""Tests for logic/answer_generation.py — Phase 4.

All tests are deterministic and require no internet access.
No external LLM calls are made; answer generation is entirely extractive.
"""

from __future__ import annotations

from logic.answer_generation import (
    INSUFFICIENT_EVIDENCE_THRESHOLD,
    MIN_CHUNKS_FOR_ANSWER,
    _derive_confidence,
    build_citation,
    format_answer_for_display,
    generate_answer,
    insufficient_evidence_response,
)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

STRONG_RESULT = {
    "chunk_id": "policy_chunk_000",
    "document_id": "ai-policy",
    "source_name": "01-ai-acceptable-use-policy.md",
    "chunk_index": 0,
    "text": "Staff must not enter learner names or reference numbers into AI tools.",
    "word_count": 12,
    "score": 0.82,
    "rank": 1,
    "is_weak": False,
    "metadata": {},
}

MODERATE_RESULT = {
    "chunk_id": "guidance_chunk_001",
    "document_id": "staff-guidance",
    "source_name": "02-staff-chatgpt-guidance.md",
    "chunk_index": 1,
    "text": "Human review is required before any AI-generated content is shared externally.",
    "word_count": 13,
    "score": 0.55,
    "rank": 2,
    "is_weak": False,
    "metadata": {},
}

WEAK_RESULT = {
    "chunk_id": "safeguard_chunk_000",
    "document_id": "safeguarding",
    "source_name": "05-safeguarding-boundary-note.md",
    "chunk_index": 0,
    "text": "Safeguarding matters must never be processed using AI tools.",
    "word_count": 10,
    "score": 0.20,
    "rank": 1,
    "is_weak": True,
    "metadata": {},
}

BOUNDARY_RESULT = {
    "chunk_id": "policy_chunk_002",
    "document_id": "ai-policy",
    "source_name": "01-ai-acceptable-use-policy.md",
    "chunk_index": 2,
    "text": "All staff must complete the mandatory AI awareness module by end of term.",
    "word_count": 14,
    "score": 0.25,
    "rank": 1,
    "is_weak": False,
    "metadata": {},
}


# ---------------------------------------------------------------------------
# generate_answer — return structure
# ---------------------------------------------------------------------------


def test_generate_answer_returns_dict():
    result = generate_answer("What is the learner data policy?", [STRONG_RESULT])
    assert isinstance(result, dict)


def test_generate_answer_has_answer_key():
    result = generate_answer("query", [STRONG_RESULT])
    assert "answer" in result


def test_generate_answer_has_citations_key():
    result = generate_answer("query", [STRONG_RESULT])
    assert "citations" in result


def test_generate_answer_has_evidence_used_key():
    result = generate_answer("query", [STRONG_RESULT])
    assert "evidence_used" in result


def test_generate_answer_has_confidence_key():
    result = generate_answer("query", [STRONG_RESULT])
    assert "confidence" in result


def test_generate_answer_has_limitations_key():
    result = generate_answer("query", [STRONG_RESULT])
    assert "limitations" in result


def test_generate_answer_has_has_evidence_key():
    result = generate_answer("query", [STRONG_RESULT])
    assert "has_evidence" in result


# ---------------------------------------------------------------------------
# generate_answer — content correctness
# ---------------------------------------------------------------------------


def test_generate_answer_answer_is_string():
    result = generate_answer("query", [STRONG_RESULT])
    assert isinstance(result["answer"], str)


def test_generate_answer_answer_non_empty_when_evidence_present():
    result = generate_answer("What is the policy?", [STRONG_RESULT])
    assert len(result["answer"]) > 0


def test_generate_answer_contains_chunk_text():
    result = generate_answer("learner data", [STRONG_RESULT])
    assert STRONG_RESULT["text"] in result["answer"]


def test_generate_answer_has_evidence_true_for_strong_result():
    result = generate_answer("query", [STRONG_RESULT])
    assert result["has_evidence"] is True


def test_generate_answer_citations_list():
    result = generate_answer("query", [STRONG_RESULT])
    assert isinstance(result["citations"], list)


def test_generate_answer_one_citation_per_result():
    results = [STRONG_RESULT, MODERATE_RESULT]
    result = generate_answer("query", results)
    assert len(result["citations"]) == 2


def test_generate_answer_evidence_used_matches_result_texts():
    results = [STRONG_RESULT, MODERATE_RESULT]
    result = generate_answer("query", results)
    for r in results:
        assert r["text"] in result["evidence_used"]


def test_generate_answer_limitations_is_string():
    result = generate_answer("query", [STRONG_RESULT])
    assert isinstance(result["limitations"], str)


def test_generate_answer_limitations_non_empty():
    result = generate_answer("query", [STRONG_RESULT])
    assert len(result["limitations"]) > 0


# ---------------------------------------------------------------------------
# generate_answer — confidence levels
# ---------------------------------------------------------------------------


def test_generate_answer_strong_confidence():
    result = generate_answer("query", [STRONG_RESULT])
    assert result["confidence"] == "strong"


def test_generate_answer_moderate_confidence():
    result = generate_answer("query", [MODERATE_RESULT])
    assert result["confidence"] == "moderate"


def test_generate_answer_weak_confidence_when_score_below_half():
    low_score_result = {**STRONG_RESULT, "score": 0.35, "rank": 1}
    result = generate_answer("query", [low_score_result])
    assert result["confidence"] == "weak"


def test_generate_answer_boundary_score_at_threshold_returns_evidence():
    result = generate_answer("query", [BOUNDARY_RESULT])
    assert result["has_evidence"] is True


# ---------------------------------------------------------------------------
# generate_answer — insufficient evidence cases
# ---------------------------------------------------------------------------


def test_generate_answer_empty_results_returns_insufficient():
    result = generate_answer("What is the AI policy?", [])
    assert result["has_evidence"] is False


def test_generate_answer_empty_results_confidence_insufficient():
    result = generate_answer("query", [])
    assert result["confidence"] == "insufficient"


def test_generate_answer_weak_top_score_returns_insufficient():
    result = generate_answer("obscure question", [WEAK_RESULT])
    assert result["has_evidence"] is False


def test_generate_answer_weak_top_score_empty_citations():
    result = generate_answer("obscure question", [WEAK_RESULT])
    assert result["citations"] == []


def test_generate_answer_weak_top_score_empty_evidence_used():
    result = generate_answer("obscure question", [WEAK_RESULT])
    assert result["evidence_used"] == []


def test_generate_answer_insufficient_confidence_label():
    result = generate_answer("query", [WEAK_RESULT])
    assert result["confidence"] == "insufficient"


# ---------------------------------------------------------------------------
# build_citation
# ---------------------------------------------------------------------------


def test_build_citation_returns_dict():
    cit = build_citation(STRONG_RESULT)
    assert isinstance(cit, dict)


def test_build_citation_has_source_name():
    cit = build_citation(STRONG_RESULT)
    assert "source_name" in cit


def test_build_citation_has_chunk_id():
    cit = build_citation(STRONG_RESULT)
    assert "chunk_id" in cit


def test_build_citation_has_document_id():
    cit = build_citation(STRONG_RESULT)
    assert "document_id" in cit


def test_build_citation_has_score():
    cit = build_citation(STRONG_RESULT)
    assert "score" in cit


def test_build_citation_has_rank():
    cit = build_citation(STRONG_RESULT)
    assert "rank" in cit


def test_build_citation_has_excerpt():
    cit = build_citation(STRONG_RESULT)
    assert "excerpt" in cit


def test_build_citation_source_name_matches():
    cit = build_citation(STRONG_RESULT)
    assert cit["source_name"] == STRONG_RESULT["source_name"]


def test_build_citation_chunk_id_matches():
    cit = build_citation(STRONG_RESULT)
    assert cit["chunk_id"] == STRONG_RESULT["chunk_id"]


def test_build_citation_score_matches():
    cit = build_citation(STRONG_RESULT)
    assert cit["score"] == STRONG_RESULT["score"]


def test_build_citation_rank_matches():
    cit = build_citation(STRONG_RESULT)
    assert cit["rank"] == STRONG_RESULT["rank"]


def test_build_citation_excerpt_is_string():
    cit = build_citation(STRONG_RESULT)
    assert isinstance(cit["excerpt"], str)


def test_build_citation_excerpt_max_200_chars():
    long_text = "word " * 100
    result = {**STRONG_RESULT, "text": long_text}
    cit = build_citation(result)
    assert len(cit["excerpt"]) <= 200


def test_build_citation_excerpt_contains_start_of_text():
    cit = build_citation(STRONG_RESULT)
    assert cit["excerpt"] in STRONG_RESULT["text"] or STRONG_RESULT["text"].startswith(cit["excerpt"])


def test_build_citation_missing_fields_use_defaults():
    cit = build_citation({})
    assert cit["source_name"] == "Unknown"
    assert cit["chunk_id"] == ""
    assert cit["score"] == 0.0


# ---------------------------------------------------------------------------
# format_answer_for_display
# ---------------------------------------------------------------------------


def test_format_answer_for_display_returns_string():
    answer_dict = generate_answer("query", [STRONG_RESULT])
    result = format_answer_for_display(answer_dict)
    assert isinstance(result, str)


def test_format_answer_for_display_non_empty():
    answer_dict = generate_answer("query", [STRONG_RESULT])
    result = format_answer_for_display(answer_dict)
    assert len(result) > 0


def test_format_answer_for_display_contains_answer_text():
    answer_dict = generate_answer("learner data", [STRONG_RESULT])
    result = format_answer_for_display(answer_dict)
    assert STRONG_RESULT["text"] in result


def test_format_answer_for_display_contains_source_name():
    answer_dict = generate_answer("query", [STRONG_RESULT])
    result = format_answer_for_display(answer_dict)
    assert STRONG_RESULT["source_name"] in result


def test_format_answer_for_display_contains_confidence():
    answer_dict = generate_answer("query", [STRONG_RESULT])
    result = format_answer_for_display(answer_dict)
    assert "Strong" in result


def test_format_answer_for_display_insufficient_evidence_label():
    answer_dict = insufficient_evidence_response("unknown topic")
    result = format_answer_for_display(answer_dict)
    assert "Insufficient" in result or "insufficient" in result.lower()


def test_format_answer_for_display_insufficient_no_citations_section():
    answer_dict = insufficient_evidence_response("unknown topic")
    result = format_answer_for_display(answer_dict)
    assert "Sources" not in result or result.count("Sources") == 0


def test_format_answer_for_display_multiple_results_lists_all_sources():
    answer_dict = generate_answer("query", [STRONG_RESULT, MODERATE_RESULT])
    result = format_answer_for_display(answer_dict)
    assert STRONG_RESULT["source_name"] in result
    assert MODERATE_RESULT["source_name"] in result


def test_format_answer_for_display_contains_limitations():
    answer_dict = generate_answer("query", [STRONG_RESULT])
    result = format_answer_for_display(answer_dict)
    assert answer_dict["limitations"] in result


# ---------------------------------------------------------------------------
# insufficient_evidence_response
# ---------------------------------------------------------------------------


def test_insufficient_evidence_response_returns_dict():
    result = insufficient_evidence_response("test query")
    assert isinstance(result, dict)


def test_insufficient_evidence_response_has_evidence_false():
    result = insufficient_evidence_response("test query")
    assert result["has_evidence"] is False


def test_insufficient_evidence_response_confidence_is_insufficient():
    result = insufficient_evidence_response("test query")
    assert result["confidence"] == "insufficient"


def test_insufficient_evidence_response_empty_citations():
    result = insufficient_evidence_response("test query")
    assert result["citations"] == []


def test_insufficient_evidence_response_empty_evidence_used():
    result = insufficient_evidence_response("test query")
    assert result["evidence_used"] == []


def test_insufficient_evidence_response_answer_is_string():
    result = insufficient_evidence_response("test query")
    assert isinstance(result["answer"], str)


def test_insufficient_evidence_response_answer_non_empty():
    result = insufficient_evidence_response("test query")
    assert len(result["answer"]) > 0


def test_insufficient_evidence_response_limitations_is_string():
    result = insufficient_evidence_response("test query")
    assert isinstance(result["limitations"], str)


def test_insufficient_evidence_response_limitations_contains_query():
    query = "What is the GDPR policy for learner data?"
    result = insufficient_evidence_response(query)
    assert query in result["limitations"]


# ---------------------------------------------------------------------------
# _derive_confidence
# ---------------------------------------------------------------------------


def test_derive_confidence_strong_at_070():
    assert _derive_confidence(0.70) == "strong"


def test_derive_confidence_strong_above_070():
    assert _derive_confidence(0.90) == "strong"


def test_derive_confidence_moderate_at_050():
    assert _derive_confidence(0.50) == "moderate"


def test_derive_confidence_moderate_between_050_and_070():
    assert _derive_confidence(0.60) == "moderate"


def test_derive_confidence_weak_just_above_threshold():
    assert _derive_confidence(0.30) == "weak"


def test_derive_confidence_weak_at_threshold():
    assert _derive_confidence(0.25) == "weak"


def test_derive_confidence_weak_below_050():
    assert _derive_confidence(0.40) == "weak"


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_insufficient_evidence_threshold_value():
    assert INSUFFICIENT_EVIDENCE_THRESHOLD == 0.25


def test_min_chunks_for_answer_value():
    assert MIN_CHUNKS_FOR_ANSWER == 1
