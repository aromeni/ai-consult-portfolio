"""Tests for logic/evaluation.py — Phase 6.

All tests are deterministic and require no internet access.
Evaluation functions are pure computations over dicts.
"""

from __future__ import annotations

from logic.evaluation import (
    evaluation_summary,
    groundedness_checklist,
    record_manual_evaluation,
    retrieval_coverage,
    risk_summary,
)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

STRONG_RESULT = {
    "chunk_id": "policy_chunk_000",
    "source_name": "01-ai-acceptable-use-policy.md",
    "score": 0.82,
    "rank": 1,
}

MODERATE_RESULT = {
    "chunk_id": "guidance_chunk_001",
    "source_name": "02-staff-chatgpt-guidance.md",
    "score": 0.61,
    "rank": 2,
}

WEAK_RESULT = {
    "chunk_id": "safeguard_chunk_000",
    "source_name": "05-safeguarding-boundary-note.md",
    "score": 0.20,
    "rank": 1,
}

ANSWER_WITH_EVIDENCE = {
    "answer": "Staff must not enter learner names into AI tools.",
    "citations": [
        {"source_name": "01-ai-acceptable-use-policy.md", "chunk_id": "policy_chunk_000", "score": 0.82, "rank": 1, "excerpt": ""},
        {"source_name": "02-staff-chatgpt-guidance.md", "chunk_id": "guidance_chunk_001", "score": 0.61, "rank": 2, "excerpt": ""},
    ],
    "evidence_used": ["Staff must not enter learner names into AI tools."],
    "confidence": "strong",
    "limitations": "This answer is drawn directly from documents.",
    "has_evidence": True,
}

ANSWER_INSUFFICIENT = {
    "answer": "No relevant documents found.",
    "citations": [],
    "evidence_used": [],
    "confidence": "insufficient",
    "limitations": "No evidence found.",
    "has_evidence": False,
}

HIGH_FLAG = {
    "category": "safeguarding",
    "risk_level": "High",
    "matched_terms": ["safeguarding"],
    "recommended_action": "Do not use AI.",
}

MEDIUM_FLAG = {
    "category": "personal_data",
    "risk_level": "Medium",
    "matched_terms": ["personal data"],
    "recommended_action": "Review before processing.",
}

SAMPLE_DOCUMENTS = [
    {"document_id": "doc1", "source_name": "doc1.md", "word_count": 500},
    {"document_id": "doc2", "source_name": "doc2.md", "word_count": 800},
]

SAMPLE_CHUNKS = [{"chunk_id": f"doc_chunk_{i:03d}"} for i in range(12)]


# ---------------------------------------------------------------------------
# retrieval_coverage — return structure
# ---------------------------------------------------------------------------


def test_retrieval_coverage_returns_dict():
    assert isinstance(retrieval_coverage([STRONG_RESULT]), dict)


def test_retrieval_coverage_has_result_count():
    assert "result_count" in retrieval_coverage([STRONG_RESULT])


def test_retrieval_coverage_has_top_score():
    assert "top_score" in retrieval_coverage([STRONG_RESULT])


def test_retrieval_coverage_has_avg_score():
    assert "avg_score" in retrieval_coverage([STRONG_RESULT])


def test_retrieval_coverage_has_unique_sources():
    assert "unique_sources" in retrieval_coverage([STRONG_RESULT])


def test_retrieval_coverage_has_coverage_grade():
    assert "coverage_grade" in retrieval_coverage([STRONG_RESULT])


# ---------------------------------------------------------------------------
# retrieval_coverage — empty input
# ---------------------------------------------------------------------------


def test_retrieval_coverage_empty_result_count_zero():
    assert retrieval_coverage([])["result_count"] == 0


def test_retrieval_coverage_empty_top_score_zero():
    assert retrieval_coverage([])["top_score"] == 0.0


def test_retrieval_coverage_empty_avg_score_zero():
    assert retrieval_coverage([])["avg_score"] == 0.0


def test_retrieval_coverage_empty_unique_sources_zero():
    assert retrieval_coverage([])["unique_sources"] == 0


def test_retrieval_coverage_empty_grade_poor():
    assert retrieval_coverage([])["coverage_grade"] == "Poor"


# ---------------------------------------------------------------------------
# retrieval_coverage — values
# ---------------------------------------------------------------------------


def test_retrieval_coverage_result_count():
    assert retrieval_coverage([STRONG_RESULT, MODERATE_RESULT])["result_count"] == 2


def test_retrieval_coverage_top_score():
    cov = retrieval_coverage([STRONG_RESULT, MODERATE_RESULT])
    assert cov["top_score"] == 0.82


def test_retrieval_coverage_avg_score():
    cov = retrieval_coverage([STRONG_RESULT, MODERATE_RESULT])
    expected = round((0.82 + 0.61) / 2, 4)
    assert cov["avg_score"] == expected


def test_retrieval_coverage_unique_sources_two():
    cov = retrieval_coverage([STRONG_RESULT, MODERATE_RESULT])
    assert cov["unique_sources"] == 2


def test_retrieval_coverage_unique_sources_one_when_same_source():
    same_source = {**MODERATE_RESULT, "source_name": STRONG_RESULT["source_name"]}
    cov = retrieval_coverage([STRONG_RESULT, same_source])
    assert cov["unique_sources"] == 1


def test_retrieval_coverage_good_grade_for_strong_results():
    results = [STRONG_RESULT, MODERATE_RESULT, STRONG_RESULT]
    cov = retrieval_coverage(results)
    assert cov["coverage_grade"] == "Good"


def test_retrieval_coverage_poor_grade_for_weak_result():
    cov = retrieval_coverage([WEAK_RESULT])
    assert cov["coverage_grade"] == "Poor"


def test_retrieval_coverage_weak_grade_for_borderline_result():
    borderline = {**STRONG_RESULT, "score": 0.30}
    cov = retrieval_coverage([borderline])
    assert cov["coverage_grade"] == "Weak"


# ---------------------------------------------------------------------------
# groundedness_checklist — return structure
# ---------------------------------------------------------------------------


def test_groundedness_checklist_returns_list():
    assert isinstance(groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT]), list)


def test_groundedness_checklist_non_empty():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    assert len(result) > 0


def test_groundedness_checklist_each_has_criterion():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    assert all("criterion" in item for item in result)


def test_groundedness_checklist_each_has_passed():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    assert all("passed" in item for item in result)


def test_groundedness_checklist_each_has_note():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    assert all("note" in item for item in result)


def test_groundedness_checklist_passed_is_bool():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    assert all(isinstance(item["passed"], bool) for item in result)


def test_groundedness_checklist_note_is_string():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    assert all(isinstance(item["note"], str) for item in result)


def test_groundedness_checklist_evidence_retrieved_passes_for_strong_answer():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    evidence_item = next(i for i in result if "Evidence retrieved" in i["criterion"])
    assert evidence_item["passed"] is True


def test_groundedness_checklist_evidence_retrieved_fails_for_insufficient():
    result = groundedness_checklist(ANSWER_INSUFFICIENT, [])
    evidence_item = next(i for i in result if "Evidence retrieved" in i["criterion"])
    assert evidence_item["passed"] is False


def test_groundedness_checklist_citations_passes_when_citations_present():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    cit_item = next(i for i in result if "Citations" in i["criterion"])
    assert cit_item["passed"] is True


def test_groundedness_checklist_citations_fails_when_no_citations():
    result = groundedness_checklist(ANSWER_INSUFFICIENT, [])
    cit_item = next(i for i in result if "Citations" in i["criterion"])
    assert cit_item["passed"] is False


def test_groundedness_checklist_confidence_passes_for_strong():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT])
    conf_item = next(i for i in result if "Confidence" in i["criterion"])
    assert conf_item["passed"] is True


def test_groundedness_checklist_confidence_fails_for_insufficient():
    result = groundedness_checklist(ANSWER_INSUFFICIENT, [])
    conf_item = next(i for i in result if "Confidence" in i["criterion"])
    assert conf_item["passed"] is False


def test_groundedness_checklist_multiple_sources_passes_for_two_citations():
    result = groundedness_checklist(ANSWER_WITH_EVIDENCE, [STRONG_RESULT, MODERATE_RESULT])
    multi_item = next(i for i in result if "Multiple" in i["criterion"])
    assert multi_item["passed"] is True


# ---------------------------------------------------------------------------
# risk_summary
# ---------------------------------------------------------------------------


def test_risk_summary_returns_dict():
    assert isinstance(risk_summary([HIGH_FLAG, MEDIUM_FLAG]), dict)


def test_risk_summary_has_total_flags():
    assert "total_flags" in risk_summary([HIGH_FLAG])


def test_risk_summary_has_high_count():
    assert "high_count" in risk_summary([HIGH_FLAG])


def test_risk_summary_has_medium_count():
    assert "medium_count" in risk_summary([MEDIUM_FLAG])


def test_risk_summary_has_highest_risk_level():
    assert "highest_risk_level" in risk_summary([HIGH_FLAG])


def test_risk_summary_has_categories():
    assert "categories" in risk_summary([HIGH_FLAG])


def test_risk_summary_total_flags_correct():
    assert risk_summary([HIGH_FLAG, MEDIUM_FLAG])["total_flags"] == 2


def test_risk_summary_high_count_correct():
    assert risk_summary([HIGH_FLAG, MEDIUM_FLAG])["high_count"] == 1


def test_risk_summary_medium_count_correct():
    assert risk_summary([HIGH_FLAG, MEDIUM_FLAG])["medium_count"] == 1


def test_risk_summary_highest_risk_level_high():
    assert risk_summary([HIGH_FLAG, MEDIUM_FLAG])["highest_risk_level"] == "High"


def test_risk_summary_highest_risk_level_medium_only():
    assert risk_summary([MEDIUM_FLAG])["highest_risk_level"] == "Medium"


def test_risk_summary_empty_input():
    summary = risk_summary([])
    assert summary["total_flags"] == 0
    assert summary["highest_risk_level"] == "None"
    assert summary["categories"] == []


def test_risk_summary_categories_list():
    summary = risk_summary([HIGH_FLAG, MEDIUM_FLAG])
    assert "safeguarding" in summary["categories"]
    assert "personal_data" in summary["categories"]


# ---------------------------------------------------------------------------
# record_manual_evaluation
# ---------------------------------------------------------------------------


def test_record_manual_evaluation_returns_dict():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert isinstance(result, dict)


def test_record_manual_evaluation_has_query():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert "query" in result


def test_record_manual_evaluation_has_relevance_rating():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert "relevance_rating" in result


def test_record_manual_evaluation_has_answer_grounded():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert "answer_grounded" in result


def test_record_manual_evaluation_has_citations_useful():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert "citations_useful" in result


def test_record_manual_evaluation_has_missing_content():
    result = record_manual_evaluation("test query", 4, True, True, "none")
    assert "missing_content" in result


def test_record_manual_evaluation_has_timestamp():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert "timestamp" in result


def test_record_manual_evaluation_timestamp_is_string():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert isinstance(result["timestamp"], str)


def test_record_manual_evaluation_timestamp_non_empty():
    result = record_manual_evaluation("test query", 4, True, True, "")
    assert len(result["timestamp"]) > 0


def test_record_manual_evaluation_stores_query():
    result = record_manual_evaluation("What is the policy?", 3, False, True, "")
    assert result["query"] == "What is the policy?"


def test_record_manual_evaluation_stores_relevance_rating():
    result = record_manual_evaluation("query", 5, True, True, "")
    assert result["relevance_rating"] == 5


def test_record_manual_evaluation_stores_answer_grounded():
    result = record_manual_evaluation("query", 3, False, True, "")
    assert result["answer_grounded"] is False


def test_record_manual_evaluation_stores_citations_useful():
    result = record_manual_evaluation("query", 3, True, False, "")
    assert result["citations_useful"] is False


def test_record_manual_evaluation_stores_missing_content():
    result = record_manual_evaluation("query", 3, True, True, "More detail on data protection.")
    assert result["missing_content"] == "More detail on data protection."


# ---------------------------------------------------------------------------
# evaluation_summary
# ---------------------------------------------------------------------------


def test_evaluation_summary_returns_dict():
    assert isinstance(evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [HIGH_FLAG]), dict)


def test_evaluation_summary_has_doc_count():
    assert "doc_count" in evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])


def test_evaluation_summary_has_chunk_count():
    assert "chunk_count" in evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])


def test_evaluation_summary_has_embedding_dim():
    assert "embedding_dim" in evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])


def test_evaluation_summary_has_risk_flag_count():
    assert "risk_flag_count" in evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])


def test_evaluation_summary_has_risk_levels():
    assert "risk_levels" in evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])


def test_evaluation_summary_doc_count_correct():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])
    assert summary["doc_count"] == 2


def test_evaluation_summary_chunk_count_correct():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])
    assert summary["chunk_count"] == 12


def test_evaluation_summary_embedding_dim_correct():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])
    assert summary["embedding_dim"] == 384


def test_evaluation_summary_risk_flag_count_correct():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [HIGH_FLAG, MEDIUM_FLAG])
    assert summary["risk_flag_count"] == 2


def test_evaluation_summary_risk_levels_is_list():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [HIGH_FLAG])
    assert isinstance(summary["risk_levels"], list)


def test_evaluation_summary_risk_levels_contains_high():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [HIGH_FLAG])
    assert "High" in summary["risk_levels"]


def test_evaluation_summary_risk_levels_deduplicated():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [HIGH_FLAG, HIGH_FLAG])
    assert summary["risk_levels"].count("High") == 1


def test_evaluation_summary_empty_risk_flags():
    summary = evaluation_summary(SAMPLE_DOCUMENTS, SAMPLE_CHUNKS, 384, [])
    assert summary["risk_flag_count"] == 0
    assert summary["risk_levels"] == []
