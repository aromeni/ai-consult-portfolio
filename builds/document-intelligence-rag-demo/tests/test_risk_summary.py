"""
Tests for src/risk_summary.py

Run from the project root:  pytest
"""

from src.risk_summary import (
    get_risk_mapping,
    get_risk_summary_for_topic,
    summarise_evidence_for_topic,
    generate_risk_safeguard_summary,
    get_overall_summary,
    generate_risk_summary_markdown,
)

# Minimal evidence fixtures covering two topics
SAMPLE_EVIDENCE = [
    {
        "topic": "safeguarding",
        "document_name": "doc_a.md",
        "line_number": 2,
        "evidence_text": "Staff must not enter safeguarding case details into any AI tool.",
        "matched_keywords": ["safeguarding"],
        "relevance_count": 1,
    },
    {
        "topic": "safeguarding",
        "document_name": "doc_a.md",
        "line_number": 5,
        "evidence_text": "All safeguarding matters must be escalated to the safeguarding lead.",
        "matched_keywords": ["safeguarding", "safeguarding lead"],
        "relevance_count": 3,
    },
    {
        "topic": "hallucination",
        "document_name": "doc_a.md",
        "line_number": 6,
        "evidence_text": "AI tools may hallucinate or produce inaccurate outputs.",
        "matched_keywords": ["hallucination"],
        "relevance_count": 1,
    },
]


# ── get_risk_mapping ──────────────────────────────────────────────────────────

def test_get_risk_mapping_returns_dict():
    assert isinstance(get_risk_mapping(), dict)


def test_get_risk_mapping_contains_all_required_topics():
    mapping = get_risk_mapping()
    required = [
        "learner data", "safeguarding", "human review", "approved tools",
        "accountability", "bias", "hallucination", "copyright", "escalation",
        "data minimisation", "anonymisation", "retention", "incident reporting",
    ]
    for topic in required:
        assert topic in mapping, f"Missing topic: {topic}"


def test_get_risk_mapping_each_entry_has_required_keys():
    for topic, record in get_risk_mapping().items():
        for key in ("risk_title", "risk_description", "why_it_matters",
                    "recommended_safeguards", "suggested_owner"):
            assert key in record, f"Topic '{topic}' missing key: {key}"


# ── get_risk_summary_for_topic ────────────────────────────────────────────────

def test_get_risk_summary_for_topic_returns_dict_for_learner_data():
    result = get_risk_summary_for_topic("learner data")
    assert isinstance(result, dict) and result


def test_get_risk_summary_for_topic_has_required_keys():
    result = get_risk_summary_for_topic("learner data")
    for key in ("risk_title", "risk_description", "why_it_matters",
                "recommended_safeguards", "suggested_owner"):
        assert key in result, f"Missing key: {key}"


def test_get_risk_summary_for_topic_recommended_safeguards_is_nonempty_list():
    result = get_risk_summary_for_topic("safeguarding")
    assert isinstance(result["recommended_safeguards"], list)
    assert len(result["recommended_safeguards"]) >= 1


def test_get_risk_summary_for_topic_unsupported_returns_empty_dict():
    assert get_risk_summary_for_topic("xyz_unknown_topic_123") == {}


def test_get_risk_summary_for_topic_is_case_insensitive():
    lower = get_risk_summary_for_topic("safeguarding")
    upper = get_risk_summary_for_topic("SAFEGUARDING")
    assert lower == upper


# ── summarise_evidence_for_topic ─────────────────────────────────────────────

def test_summarise_evidence_for_topic_returns_list():
    assert isinstance(summarise_evidence_for_topic("safeguarding", SAMPLE_EVIDENCE), list)


def test_summarise_evidence_for_topic_returns_only_matching_topic():
    result = summarise_evidence_for_topic("safeguarding", SAMPLE_EVIDENCE)
    assert all(r["topic"] == "safeguarding" for r in result)


def test_summarise_evidence_for_topic_limits_to_max_items():
    result = summarise_evidence_for_topic("safeguarding", SAMPLE_EVIDENCE, max_items=1)
    assert len(result) <= 1


def test_summarise_evidence_for_topic_default_max_is_three():
    many = [
        {
            "topic": "safeguarding",
            "document_name": "doc.md",
            "line_number": i,
            "evidence_text": f"Line {i}",
            "matched_keywords": ["safeguarding"],
            "relevance_count": i,
        }
        for i in range(1, 7)
    ]
    result = summarise_evidence_for_topic("safeguarding", many)
    assert len(result) <= 3


def test_summarise_evidence_for_topic_sorted_by_relevance_count_descending():
    result = summarise_evidence_for_topic("safeguarding", SAMPLE_EVIDENCE)
    if len(result) >= 2:
        assert result[0]["relevance_count"] >= result[1]["relevance_count"]


def test_summarise_evidence_for_topic_unknown_topic_returns_empty_list():
    assert summarise_evidence_for_topic("xyz_unknown", SAMPLE_EVIDENCE) == []


# ── generate_risk_safeguard_summary ──────────────────────────────────────────

def test_generate_risk_safeguard_summary_returns_list():
    assert isinstance(generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE), list)


def test_generate_risk_safeguard_summary_one_item_per_supported_topic():
    result = generate_risk_safeguard_summary(["safeguarding", "hallucination"], SAMPLE_EVIDENCE)
    assert len(result) == 2


def test_generate_risk_safeguard_summary_item_has_required_keys():
    result = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    assert result
    for key in ("topic", "risk_title", "risk_description", "why_it_matters",
                "recommended_safeguards", "suggested_owner",
                "evidence_items", "evidence_count", "coverage_note"):
        assert key in result[0], f"Missing key: {key}"


def test_generate_risk_safeguard_summary_evidence_count_is_total_not_capped():
    result = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    # SAMPLE_EVIDENCE has 2 safeguarding items
    assert result[0]["evidence_count"] == 2


def test_generate_risk_safeguard_summary_unsupported_topic_is_skipped():
    result = generate_risk_safeguard_summary(["xyz_unknown_topic"], SAMPLE_EVIDENCE)
    assert result == []


def test_generate_risk_safeguard_summary_empty_topics_returns_empty_list():
    result = generate_risk_safeguard_summary([], SAMPLE_EVIDENCE)
    assert result == []


def test_generate_risk_safeguard_summary_coverage_note_no_evidence():
    # copyright has no evidence in SAMPLE_EVIDENCE
    result = generate_risk_safeguard_summary(["copyright"], SAMPLE_EVIDENCE)
    assert result
    assert "No direct evidence" in result[0]["coverage_note"]


def test_generate_risk_safeguard_summary_coverage_note_limited_evidence():
    # hallucination has exactly 1 item in SAMPLE_EVIDENCE
    result = generate_risk_safeguard_summary(["hallucination"], SAMPLE_EVIDENCE)
    assert result
    assert "Limited evidence" in result[0]["coverage_note"]


def test_generate_risk_safeguard_summary_coverage_note_multiple_evidence():
    # safeguarding has 2 items in SAMPLE_EVIDENCE
    result = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    assert result
    assert "Multiple" in result[0]["coverage_note"]


def test_generate_risk_safeguard_summary_topic_field_matches_input():
    result = generate_risk_safeguard_summary(["hallucination"], SAMPLE_EVIDENCE)
    assert result[0]["topic"] == "hallucination"


# ── get_overall_summary ───────────────────────────────────────────────────────

def test_get_overall_summary_returns_dict():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    assert isinstance(get_overall_summary(items), dict)


def test_get_overall_summary_has_required_keys():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    result = get_overall_summary(items)
    for key in ("topics_reviewed", "topics_with_evidence", "topics_without_evidence",
                "total_evidence_snippets", "overall_note"):
        assert key in result, f"Missing key: {key}"


def test_get_overall_summary_topics_reviewed_count():
    items = generate_risk_safeguard_summary(["safeguarding", "hallucination"], SAMPLE_EVIDENCE)
    assert get_overall_summary(items)["topics_reviewed"] == 2


def test_get_overall_summary_topics_with_evidence_count():
    # safeguarding has evidence, copyright does not
    items = generate_risk_safeguard_summary(["safeguarding", "copyright"], SAMPLE_EVIDENCE)
    result = get_overall_summary(items)
    assert result["topics_with_evidence"] == 1
    assert result["topics_without_evidence"] == 1


def test_get_overall_summary_total_evidence_snippets():
    items = generate_risk_safeguard_summary(["safeguarding", "hallucination"], SAMPLE_EVIDENCE)
    result = get_overall_summary(items)
    # safeguarding=2, hallucination=1
    assert result["total_evidence_snippets"] == 3


def test_get_overall_summary_overall_note_no_evidence():
    items = generate_risk_safeguard_summary(["copyright"], SAMPLE_EVIDENCE)
    result = get_overall_summary(items)
    assert "No matching evidence" in result["overall_note"]


def test_get_overall_summary_overall_note_some_evidence():
    items = generate_risk_safeguard_summary(["safeguarding", "copyright"], SAMPLE_EVIDENCE)
    result = get_overall_summary(items)
    assert "some topics" in result["overall_note"]


def test_get_overall_summary_overall_note_all_evidence():
    items = generate_risk_safeguard_summary(["safeguarding", "hallucination"], SAMPLE_EVIDENCE)
    result = get_overall_summary(items)
    assert "all selected topics" in result["overall_note"]


def test_get_overall_summary_empty_items_returns_no_evidence_note():
    result = get_overall_summary([])
    assert result["topics_reviewed"] == 0
    assert "No matching evidence" in result["overall_note"]


# ── generate_risk_summary_markdown ────────────────────────────────────────────

def test_generate_risk_summary_markdown_returns_str():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    overall = get_overall_summary(items)
    assert isinstance(generate_risk_summary_markdown(items, overall), str)


def test_generate_risk_summary_markdown_contains_main_header():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    overall = get_overall_summary(items)
    md = generate_risk_summary_markdown(items, overall)
    assert "# Risk and Safeguard Summary" in md


def test_generate_risk_summary_markdown_contains_responsible_use_section():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    overall = get_overall_summary(items)
    md = generate_risk_summary_markdown(items, overall)
    assert "Responsible Use and Limitations" in md


def test_generate_risk_summary_markdown_contains_responsible_use_text():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    overall = get_overall_summary(items)
    md = generate_risk_summary_markdown(items, overall)
    assert "deterministic topic and keyword matching" in md


def test_generate_risk_summary_markdown_contains_topic_risk_title():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    overall = get_overall_summary(items)
    md = generate_risk_summary_markdown(items, overall)
    assert "Safeguarding information mishandled" in md


def test_generate_risk_summary_markdown_contains_overall_summary_section():
    items = generate_risk_safeguard_summary(["safeguarding"], SAMPLE_EVIDENCE)
    overall = get_overall_summary(items)
    md = generate_risk_summary_markdown(items, overall)
    assert "## Overall Summary" in md


def test_generate_risk_summary_markdown_empty_items_still_returns_string():
    overall = get_overall_summary([])
    md = generate_risk_summary_markdown([], overall)
    assert isinstance(md, str)
    assert "Responsible Use and Limitations" in md
