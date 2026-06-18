"""Tests for src/report_generator.py — Phase 8: Mini Answer Report."""

import pytest
from src.report_generator import (
    create_report_filename,
    generate_markdown_answer_report,
    get_default_report_limitations,
    format_detected_topics,
    format_evidence_items,
    format_limitations,
    format_retrieval_comparison_section,
    build_report_data_from_session_state,
)


# ── create_report_filename ────────────────────────────────────────────────────


def test_filename_returns_string():
    assert isinstance(create_report_filename("My Report"), str)


def test_filename_ends_with_md():
    assert create_report_filename("My Report").endswith(".md")


def test_filename_lowercase():
    result = create_report_filename("My Report")
    assert result == result.lower()


def test_filename_spaces_replaced():
    result = create_report_filename("learner data policy")
    assert " " not in result


def test_filename_empty_title_defaults():
    assert create_report_filename("") == "semantic-rag-answer-report.md"


def test_filename_whitespace_title_defaults():
    assert create_report_filename("   ") == "semantic-rag-answer-report.md"


def test_filename_none_like_empty():
    assert create_report_filename("") == "semantic-rag-answer-report.md"


def test_filename_preserves_meaningful_slug():
    result = create_report_filename("safeguarding policy review")
    assert "safeguarding" in result
    assert "policy" in result


def test_filename_special_chars_removed():
    result = create_report_filename("test! report@2026")
    assert "!" not in result
    assert "@" not in result


# ── get_default_report_limitations ───────────────────────────────────────────


def test_default_limitations_returns_list():
    result = get_default_report_limitations()
    assert isinstance(result, list)


def test_default_limitations_non_empty():
    result = get_default_report_limitations()
    assert len(result) > 0


def test_default_limitations_returns_strings():
    result = get_default_report_limitations()
    assert all(isinstance(item, str) for item in result)


# ── format_detected_topics ────────────────────────────────────────────────────


def test_format_detected_topics_returns_string():
    assert isinstance(format_detected_topics(["learner data", "safeguarding"]), str)


def test_format_detected_topics_includes_topic():
    result = format_detected_topics(["learner data", "safeguarding"])
    assert "learner data" in result


def test_format_detected_topics_empty_list_fallback():
    result = format_detected_topics([])
    assert "No specific topics" in result


def test_format_detected_topics_single_topic():
    result = format_detected_topics(["bias"])
    assert "bias" in result


# ── format_evidence_items ─────────────────────────────────────────────────────


def _fake_evidence_items(n=3):
    return [
        {
            "rank": i + 1,
            "score": round(0.9 - i * 0.1, 2),
            "document_name": f"synthetic-policy-{i}.md",
            "chunk_id": f"synthetic-policy-{i}__chunk_{i:03d}",
            "chunk_index": i,
            "evidence_text": f"Policy evidence text for item {i}",
        }
        for i in range(n)
    ]


def test_format_evidence_items_returns_string():
    assert isinstance(format_evidence_items(_fake_evidence_items()), str)


def test_format_evidence_items_includes_document_name():
    result = format_evidence_items(_fake_evidence_items())
    assert "synthetic-policy-0.md" in result


def test_format_evidence_items_includes_chunk_id():
    result = format_evidence_items(_fake_evidence_items())
    assert "synthetic-policy-0__chunk_000" in result


def test_format_evidence_items_empty_list_fallback():
    result = format_evidence_items([])
    assert "No evidence items available" in result


def test_format_evidence_items_respects_max_items():
    items = _fake_evidence_items(10)
    result = format_evidence_items(items, max_items=2)
    assert "synthetic-policy-0.md" in result
    assert "synthetic-policy-9.md" not in result


# ── format_limitations ────────────────────────────────────────────────────────


def test_format_limitations_returns_string():
    assert isinstance(format_limitations(["Test limitation."]), str)


def test_format_limitations_includes_text():
    result = format_limitations(["This prototype uses synthetic documents only."])
    assert "This prototype uses synthetic documents only." in result


def test_format_limitations_empty_uses_defaults():
    result = format_limitations([])
    assert "synthetic" in result.lower()


def test_format_limitations_formats_as_bullets():
    result = format_limitations(["First limit.", "Second limit."])
    assert "- First limit." in result
    assert "- Second limit." in result


# ── format_retrieval_comparison_section ──────────────────────────────────────


def _fake_comparison_result():
    return {
        "keyword_summary": {"result_count": 3, "unique_documents": 2},
        "semantic_summary": {"result_count": 4, "unique_documents": 2},
        "overlap": [{"chunk_id": "doc__chunk_000"}],
        "comparison_insight": "Both methods found the same chunks.",
    }


def test_format_comparison_section_returns_string():
    assert isinstance(format_retrieval_comparison_section(_fake_comparison_result()), str)


def test_format_comparison_section_includes_insight():
    result = format_retrieval_comparison_section(_fake_comparison_result())
    assert "Both methods found the same chunks." in result


def test_format_comparison_section_includes_result_counts():
    result = format_retrieval_comparison_section(_fake_comparison_result())
    assert "3" in result
    assert "4" in result


def test_format_comparison_section_handles_none():
    result = format_retrieval_comparison_section(None)
    assert "No retrieval comparison" in result


def test_format_comparison_section_handles_empty_dict():
    result = format_retrieval_comparison_section({})
    assert isinstance(result, str)


# ── build_report_data_from_session_state ──────────────────────────────────────


def test_build_report_data_returns_dict():
    assert isinstance(build_report_data_from_session_state({}), dict)


def test_build_report_data_handles_empty_session_state():
    result = build_report_data_from_session_state({})
    assert result["question"] == ""
    assert result["answer"] == ""
    assert isinstance(result["limitations"], list)
    assert isinstance(result["reviewer_notes"], list)


def test_build_report_data_uses_last_rag_question():
    state = {"last_rag_question": "Can staff use ChatGPT?"}
    result = build_report_data_from_session_state(state)
    assert result["question"] == "Can staff use ChatGPT?"


def test_build_report_data_uses_last_rag_answer():
    state = {"last_rag_answer": "Staff must review AI outputs before use."}
    result = build_report_data_from_session_state(state)
    assert result["answer"] == "Staff must review AI outputs before use."


def test_build_report_data_uses_last_retrieval_comparison():
    comp = _fake_comparison_result()
    state = {"last_retrieval_comparison": comp}
    result = build_report_data_from_session_state(state)
    assert result["comparison_result"] is comp


def test_build_report_data_has_all_expected_keys():
    result = build_report_data_from_session_state({})
    for key in (
        "report_title", "generated_date", "question", "answer",
        "detected_topics", "question_type", "needs_caution", "caution_reason",
        "model_name", "retrieval_metric", "top_k", "evidence_items",
        "comparison_result", "limitations", "reviewer_notes",
    ):
        assert key in result, f"Missing key: {key}"


# ── generate_markdown_answer_report ──────────────────────────────────────────


def test_report_returns_string():
    result = generate_markdown_answer_report({})
    assert isinstance(result, str)


def test_report_non_empty():
    result = generate_markdown_answer_report({})
    assert len(result) > 0


def test_report_contains_mini_answer_report_header():
    result = generate_markdown_answer_report({})
    assert "Semantic RAG Mini Answer Report" in result


def test_report_contains_responsible_use_notice():
    result = generate_markdown_answer_report({})
    assert "synthetic documents" in result.lower() or "responsible" in result.lower()


def test_report_includes_question():
    data = {"question": "Can staff use AI for safeguarding decisions?"}
    result = generate_markdown_answer_report(data)
    assert "Can staff use AI for safeguarding decisions?" in result


def test_report_includes_answer():
    data = {"answer": "No. Safeguarding decisions must be made by a qualified professional."}
    result = generate_markdown_answer_report(data)
    assert "Safeguarding decisions must be made by a qualified professional." in result


def test_report_includes_sources_backward_compat():
    data = {
        "sources": [
            {
                "document_name": "synthetic-ai-acceptable-use-policy.md",
                "chunk_id": "chunk_001",
                "text": "Sample text",
            }
        ]
    }
    result = generate_markdown_answer_report(data)
    assert "synthetic-ai-acceptable-use-policy.md" in result


def test_report_includes_limitations():
    data = {"limitations": ["This prototype uses synthetic documents only."]}
    result = generate_markdown_answer_report(data)
    assert "This prototype uses synthetic documents only." in result


def test_report_empty_sources_no_crash():
    result = generate_markdown_answer_report({"sources": []})
    assert isinstance(result, str)


def test_report_empty_limitations_no_crash():
    result = generate_markdown_answer_report({"limitations": []})
    assert isinstance(result, str)


def test_report_includes_generated_date():
    data = {"generated_date": "2026-06-12"}
    result = generate_markdown_answer_report(data)
    assert "2026-06-12" in result


def test_report_includes_retrieval_method_backward_compat():
    data = {"retrieval_method": "keyword"}
    result = generate_markdown_answer_report(data)
    assert "keyword" in result


def test_report_has_question_section():
    result = generate_markdown_answer_report({})
    assert "## 1. Question" in result


def test_report_has_short_grounded_answer_section():
    result = generate_markdown_answer_report({})
    assert "Short Grounded Answer" in result


def test_report_has_retrieved_evidence_section():
    result = generate_markdown_answer_report({})
    assert "Retrieved Evidence" in result


def test_report_has_limitations_and_responsible_use_section():
    result = generate_markdown_answer_report({})
    assert "Limitations and Responsible Use" in result


def test_report_has_prototype_status_section():
    result = generate_markdown_answer_report({})
    assert "Prototype Status" in result


def test_report_no_question_shows_placeholder():
    result = generate_markdown_answer_report({"question": ""})
    assert "Run the RAG Q&A page" in result


def test_report_contains_policy_assistant_footer():
    result = generate_markdown_answer_report({})
    assert "Semantic RAG Policy Assistant" in result
