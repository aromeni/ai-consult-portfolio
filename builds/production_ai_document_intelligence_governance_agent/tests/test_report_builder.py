"""Tests for logic/report_builder.py — Phase 6.

All tests are deterministic and require no internet access.
Report generation is pure string assembly — no external dependencies.
"""

from __future__ import annotations

from logic.report_builder import (
    _section_citations,
    _section_documents,
    _section_evidence,
    _section_limitations,
    _section_risk_flags,
    build_report,
)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

SAMPLE_DOCUMENTS = [
    {
        "document_id": "ai-policy",
        "source_name": "01-ai-acceptable-use-policy.md",
        "word_count": 888,
    },
    {
        "document_id": "staff-guidance",
        "source_name": "02-staff-chatgpt-guidance.md",
        "word_count": 805,
    },
]

SAMPLE_RESULTS = [
    {
        "chunk_id": "policy_chunk_000",
        "document_id": "ai-policy",
        "source_name": "01-ai-acceptable-use-policy.md",
        "text": "Staff must not enter learner names or reference numbers into AI tools.",
        "score": 0.82,
        "rank": 1,
        "is_weak": False,
    },
    {
        "chunk_id": "guidance_chunk_001",
        "document_id": "staff-guidance",
        "source_name": "02-staff-chatgpt-guidance.md",
        "text": "Human review is required before any AI-generated content is shared.",
        "score": 0.61,
        "rank": 2,
        "is_weak": False,
    },
]

SAMPLE_ANSWER_DICT = {
    "answer": "Staff must not enter learner names into AI tools. Human review is required.",
    "citations": [
        {
            "source_name": "01-ai-acceptable-use-policy.md",
            "chunk_id": "policy_chunk_000",
            "document_id": "ai-policy",
            "score": 0.82,
            "rank": 1,
            "excerpt": "Staff must not enter learner names or reference numbers into AI tools.",
        }
    ],
    "evidence_used": ["Staff must not enter learner names or reference numbers into AI tools."],
    "confidence": "strong",
    "limitations": "This answer is drawn directly from the documents in the library.",
    "has_evidence": True,
}

INSUFFICIENT_ANSWER_DICT = {
    "answer": "No relevant documents found.",
    "citations": [],
    "evidence_used": [],
    "confidence": "insufficient",
    "limitations": "No evidence found for this query.",
    "has_evidence": False,
}

SAMPLE_RISK_FLAGS = [
    {
        "category": "learner_data",
        "risk_level": "High",
        "matched_terms": ["learner name"],
        "recommended_action": "Do not process identifiable learner data.",
    },
    {
        "category": "personal_data",
        "risk_level": "Medium",
        "matched_terms": ["personal data"],
        "recommended_action": "Review before processing.",
    },
]

SAMPLE_QUERY = "Can staff use ChatGPT with learner data?"


# ---------------------------------------------------------------------------
# build_report — return type and non-empty
# ---------------------------------------------------------------------------


def test_build_report_returns_string():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert isinstance(result, str)


def test_build_report_non_empty():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert len(result) > 0


def test_build_report_default_org_name():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, [])
    assert "BrightPath Skills Training" in result


def test_build_report_custom_org_name():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, [], organisation_name="Acme Training Ltd")
    assert "Acme Training Ltd" in result


def test_build_report_contains_query():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, [])
    assert SAMPLE_QUERY in result


# ---------------------------------------------------------------------------
# build_report — all 10 sections present
# ---------------------------------------------------------------------------


def test_build_report_has_executive_summary():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Executive Summary" in result


def test_build_report_has_documents_analysed():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Documents Analysed" in result


def test_build_report_has_question_asked():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Question Asked" in result


def test_build_report_has_evidence_retrieved():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Evidence Retrieved" in result


def test_build_report_has_grounded_answer():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Grounded Answer" in result


def test_build_report_has_citations_section():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Citations" in result


def test_build_report_has_governance_risk_flags():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Governance and Risk Flags" in result


def test_build_report_has_recommended_next_steps():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Recommended Next Steps" in result


def test_build_report_has_human_review_checklist():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Human Review Checklist" in result


def test_build_report_has_limitations_section():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Limitations" in result


# ---------------------------------------------------------------------------
# build_report — content correctness
# ---------------------------------------------------------------------------


def test_build_report_contains_document_name():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, [])
    assert "01-ai-acceptable-use-policy.md" in result


def test_build_report_contains_answer_text():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, [])
    assert "Staff must not enter learner names" in result


def test_build_report_contains_risk_flag_category():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "Learner Data" in result or "learner_data" in result


def test_build_report_contains_risk_level():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "High" in result


def test_build_report_no_evidence_mentions_insufficient():
    result = build_report([], SAMPLE_QUERY, INSUFFICIENT_ANSWER_DICT, [], [])
    assert "No" in result


def test_build_report_high_risk_flags_mentioned_in_summary():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, SAMPLE_RISK_FLAGS)
    assert "1 High-risk flag" in result


def test_build_report_zero_risk_flags_summary():
    result = build_report(SAMPLE_DOCUMENTS, SAMPLE_QUERY, SAMPLE_ANSWER_DICT, SAMPLE_RESULTS, [])
    assert "0 risk flag" in result


# ---------------------------------------------------------------------------
# _section_documents
# ---------------------------------------------------------------------------


def test_section_documents_returns_string():
    result = _section_documents(SAMPLE_DOCUMENTS)
    assert isinstance(result, str)


def test_section_documents_non_empty():
    result = _section_documents(SAMPLE_DOCUMENTS)
    assert len(result) > 0


def test_section_documents_contains_source_name():
    result = _section_documents(SAMPLE_DOCUMENTS)
    assert "01-ai-acceptable-use-policy.md" in result


def test_section_documents_empty_list():
    result = _section_documents([])
    assert isinstance(result, str)
    assert len(result) > 0


def test_section_documents_lists_both_documents():
    result = _section_documents(SAMPLE_DOCUMENTS)
    assert "01-ai-acceptable-use-policy.md" in result
    assert "02-staff-chatgpt-guidance.md" in result


def test_section_documents_shows_word_count():
    result = _section_documents(SAMPLE_DOCUMENTS)
    assert "888" in result


# ---------------------------------------------------------------------------
# _section_evidence
# ---------------------------------------------------------------------------


def test_section_evidence_returns_string():
    result = _section_evidence(SAMPLE_RESULTS)
    assert isinstance(result, str)


def test_section_evidence_non_empty_with_results():
    result = _section_evidence(SAMPLE_RESULTS)
    assert len(result) > 0


def test_section_evidence_contains_source_name():
    result = _section_evidence(SAMPLE_RESULTS)
    assert "01-ai-acceptable-use-policy.md" in result


def test_section_evidence_empty_list():
    result = _section_evidence([])
    assert isinstance(result, str)
    assert len(result) > 0


def test_section_evidence_contains_chunk_id():
    result = _section_evidence(SAMPLE_RESULTS)
    assert "policy_chunk_000" in result


def test_section_evidence_contains_score():
    result = _section_evidence(SAMPLE_RESULTS)
    assert "0.820" in result


# ---------------------------------------------------------------------------
# _section_citations (internal helper)
# ---------------------------------------------------------------------------


def test_section_citations_returns_string():
    result = _section_citations(SAMPLE_ANSWER_DICT)
    assert isinstance(result, str)


def test_section_citations_non_empty_when_citations_present():
    result = _section_citations(SAMPLE_ANSWER_DICT)
    assert len(result) > 0


def test_section_citations_contains_source_name():
    result = _section_citations(SAMPLE_ANSWER_DICT)
    assert "01-ai-acceptable-use-policy.md" in result


def test_section_citations_no_citations():
    result = _section_citations(INSUFFICIENT_ANSWER_DICT)
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# _section_risk_flags
# ---------------------------------------------------------------------------


def test_section_risk_flags_returns_string():
    result = _section_risk_flags(SAMPLE_RISK_FLAGS)
    assert isinstance(result, str)


def test_section_risk_flags_non_empty_with_flags():
    result = _section_risk_flags(SAMPLE_RISK_FLAGS)
    assert len(result) > 0


def test_section_risk_flags_contains_risk_level():
    result = _section_risk_flags(SAMPLE_RISK_FLAGS)
    assert "High" in result


def test_section_risk_flags_empty_list():
    result = _section_risk_flags([])
    assert isinstance(result, str)
    assert len(result) > 0


def test_section_risk_flags_contains_recommended_action():
    result = _section_risk_flags(SAMPLE_RISK_FLAGS)
    assert "Do not process identifiable learner data" in result


def test_section_risk_flags_contains_matched_terms():
    result = _section_risk_flags(SAMPLE_RISK_FLAGS)
    assert "learner name" in result


# ---------------------------------------------------------------------------
# _section_limitations
# ---------------------------------------------------------------------------


def test_section_limitations_returns_string():
    result = _section_limitations()
    assert isinstance(result, str)


def test_section_limitations_non_empty():
    result = _section_limitations()
    assert len(result) > 0


def test_section_limitations_mentions_human_review():
    result = _section_limitations()
    assert "review" in result.lower() or "reviewed" in result.lower()


def test_section_limitations_mentions_demonstration():
    result = _section_limitations()
    assert "demonstration" in result.lower() or "synthetic" in result.lower()
