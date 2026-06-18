"""
Tests for src/evidence_extractor.py

Run from the project root:  pytest
"""

from src.evidence_extractor import (
    TOPIC_KEYWORDS,
    get_supported_topics,
    get_topic_keywords,
    extract_sentences_with_keywords,
    extract_policy_evidence,
    extract_evidence_from_documents,
)

SAMPLE_TEXT = """\
This document covers our approach to learner data protection.
Staff must not enter safeguarding case details into any AI tool.
All AI-generated outputs require human review before use.
Only approved tools may be used for AI-related work.
Staff should escalate concerns to the designated safeguarding lead.
AI tools may hallucinate or produce inaccurate outputs.
Copyright and intellectual property rights must be respected.
Accountability for AI use rests with the individual member of staff.
AI outputs should be reviewed for bias and fairness before sharing.
Data minimisation applies: only include necessary learner information.
All personal data must be anonymised before processing.
Retention periods apply: data should be deleted after the storage period ends.
Staff must report any data breach or incident immediately.
"""


# ── TOPIC_KEYWORDS ────────────────────────────────────────────────────────────

def test_topic_keywords_is_dict():
    assert isinstance(TOPIC_KEYWORDS, dict)


def test_topic_keywords_contains_all_required_topics():
    required = [
        "learner data",
        "safeguarding",
        "human review",
        "approved tools",
        "accountability",
        "bias",
        "hallucination",
        "copyright",
        "escalation",
        "data minimisation",
        "anonymisation",
        "retention",
        "incident reporting",
    ]
    for topic in required:
        assert topic in TOPIC_KEYWORDS, f"Missing topic: {topic}"


def test_topic_keywords_each_value_is_nonempty_list():
    for topic, keywords in TOPIC_KEYWORDS.items():
        assert isinstance(keywords, list), f"Topic '{topic}' value is not a list"
        assert len(keywords) >= 1, f"Topic '{topic}' has no keywords"


# ── get_supported_topics ──────────────────────────────────────────────────────

def test_get_supported_topics_returns_list():
    assert isinstance(get_supported_topics(), list)


def test_get_supported_topics_contains_all_required_topics():
    topics = get_supported_topics()
    required = [
        "learner data", "safeguarding", "human review", "approved tools",
        "accountability", "bias", "hallucination", "copyright", "escalation",
        "data minimisation", "anonymisation", "retention", "incident reporting",
    ]
    for topic in required:
        assert topic in topics, f"Missing topic: {topic}"


def test_get_supported_topics_returns_at_least_13():
    assert len(get_supported_topics()) >= 13


# ── get_topic_keywords ────────────────────────────────────────────────────────

def test_get_topic_keywords_returns_list():
    assert isinstance(get_topic_keywords("learner data"), list)


def test_get_topic_keywords_learner_data_is_nonempty():
    assert len(get_topic_keywords("learner data")) >= 1


def test_get_topic_keywords_unsupported_topic_returns_empty_list():
    assert get_topic_keywords("xyz_unknown_topic_123") == []


def test_get_topic_keywords_is_case_insensitive():
    assert get_topic_keywords("safeguarding") == get_topic_keywords("SAFEGUARDING")


# ── extract_sentences_with_keywords ──────────────────────────────────────────

def test_extract_sentences_returns_list():
    assert isinstance(extract_sentences_with_keywords(SAMPLE_TEXT, ["safeguarding"]), list)


def test_extract_sentences_finds_matching_sentence():
    result = extract_sentences_with_keywords(SAMPLE_TEXT, ["safeguarding"])
    assert len(result) >= 1


def test_extract_sentences_is_case_insensitive():
    lower = extract_sentences_with_keywords(SAMPLE_TEXT, ["safeguarding"])
    upper = extract_sentences_with_keywords(SAMPLE_TEXT, ["SAFEGUARDING"])
    assert len(lower) == len(upper)


def test_extract_sentences_no_match_returns_empty_list():
    assert extract_sentences_with_keywords(SAMPLE_TEXT, ["blockchain"]) == []


def test_extract_sentences_multiple_keywords_finds_more_results():
    single = extract_sentences_with_keywords(SAMPLE_TEXT, ["safeguarding"])
    multi  = extract_sentences_with_keywords(SAMPLE_TEXT, ["safeguarding", "learner data"])
    assert len(multi) >= len(single)


def test_extract_sentences_with_empty_keywords_returns_empty():
    assert extract_sentences_with_keywords(SAMPLE_TEXT, []) == []


def test_extract_sentences_with_empty_text_returns_empty():
    assert extract_sentences_with_keywords("", ["safeguarding"]) == []


# ── extract_policy_evidence ───────────────────────────────────────────────────

def test_extract_policy_evidence_returns_list():
    assert isinstance(extract_policy_evidence(SAMPLE_TEXT, "safeguarding"), list)


def test_extract_policy_evidence_finds_safeguarding_evidence():
    result = extract_policy_evidence(SAMPLE_TEXT, "safeguarding")
    assert len(result) >= 1


def test_extract_policy_evidence_result_has_required_keys():
    result = extract_policy_evidence(SAMPLE_TEXT, "safeguarding")
    assert result
    for key in ("topic", "document_name", "line_number", "evidence_text", "matched_keywords", "relevance_count"):
        assert key in result[0], f"Missing key: {key}"


def test_extract_policy_evidence_topic_matches_requested_topic():
    result = extract_policy_evidence(SAMPLE_TEXT, "hallucination")
    assert result
    assert all(r["topic"] == "hallucination" for r in result)


def test_extract_policy_evidence_matched_keywords_is_list():
    result = extract_policy_evidence(SAMPLE_TEXT, "human review")
    assert result
    assert isinstance(result[0]["matched_keywords"], list)


def test_extract_policy_evidence_line_number_is_positive_int():
    result = extract_policy_evidence(SAMPLE_TEXT, "accountability")
    assert result
    assert all(isinstance(r["line_number"], int) and r["line_number"] >= 1 for r in result)


def test_extract_policy_evidence_relevance_count_is_positive_int():
    result = extract_policy_evidence(SAMPLE_TEXT, "safeguarding")
    assert result
    assert all(isinstance(r["relevance_count"], int) and r["relevance_count"] >= 1 for r in result)


def test_extract_policy_evidence_document_name_defaults_to_empty_string():
    result = extract_policy_evidence(SAMPLE_TEXT, "safeguarding")
    assert result
    assert result[0]["document_name"] == ""


def test_extract_policy_evidence_document_name_uses_provided_value():
    result = extract_policy_evidence(SAMPLE_TEXT, "safeguarding", document_name="policy.md")
    assert result
    assert result[0]["document_name"] == "policy.md"


def test_extract_policy_evidence_sorted_by_relevance_count_descending():
    text = (
        "safeguarding safeguarding safeguarding — three keyword occurrences.\n"
        "one safeguarding mention only.\n"
    )
    result = extract_policy_evidence(text, "safeguarding")
    if len(result) >= 2:
        assert result[0]["relevance_count"] >= result[1]["relevance_count"]


def test_extract_policy_evidence_deduplicates_identical_snippets():
    text = "Safeguarding is important.\nSafeguarding is important.\n"
    result = extract_policy_evidence(text, "safeguarding")
    snippets = [r["evidence_text"] for r in result]
    assert len(snippets) == len(set(snippets))


def test_extract_policy_evidence_unsupported_topic_returns_empty_list():
    assert extract_policy_evidence(SAMPLE_TEXT, "xyz_unknown_topic_abc") == []


def test_extract_policy_evidence_finds_copyright():
    result = extract_policy_evidence(SAMPLE_TEXT, "copyright")
    assert len(result) >= 1


def test_extract_policy_evidence_finds_escalation():
    result = extract_policy_evidence(SAMPLE_TEXT, "escalation")
    assert len(result) >= 1


def test_extract_policy_evidence_finds_bias():
    result = extract_policy_evidence(SAMPLE_TEXT, "bias")
    assert len(result) >= 1


def test_extract_policy_evidence_finds_data_minimisation():
    result = extract_policy_evidence(SAMPLE_TEXT, "data minimisation")
    assert len(result) >= 1


def test_extract_policy_evidence_finds_anonymisation():
    result = extract_policy_evidence(SAMPLE_TEXT, "anonymisation")
    assert len(result) >= 1


def test_extract_policy_evidence_finds_retention():
    result = extract_policy_evidence(SAMPLE_TEXT, "retention")
    assert len(result) >= 1


def test_extract_policy_evidence_finds_incident_reporting():
    result = extract_policy_evidence(SAMPLE_TEXT, "incident reporting")
    assert len(result) >= 1


# ── extract_evidence_from_documents ──────────────────────────────────────────

def test_extract_evidence_from_documents_returns_list():
    docs = {"policy.md": SAMPLE_TEXT}
    assert isinstance(extract_evidence_from_documents(docs, "safeguarding"), list)


def test_extract_evidence_from_documents_result_has_all_required_keys():
    docs = {"policy.md": SAMPLE_TEXT}
    results = extract_evidence_from_documents(docs, "safeguarding")
    assert results
    for key in ("topic", "document_name", "line_number", "evidence_text", "matched_keywords", "relevance_count"):
        assert key in results[0], f"Missing key: {key}"


def test_extract_evidence_from_documents_includes_document_name():
    docs = {"policy.md": SAMPLE_TEXT}
    results = extract_evidence_from_documents(docs, "safeguarding")
    assert results
    assert results[0]["document_name"] == "policy.md"


def test_extract_evidence_from_documents_searches_multiple_documents():
    docs = {
        "doc_a.md": SAMPLE_TEXT,
        "doc_b.md": "Safeguarding is a critical boundary. Staff must escalate all concerns.",
    }
    results = extract_evidence_from_documents(docs, "safeguarding")
    names = {r["document_name"] for r in results}
    assert "doc_a.md" in names
    assert "doc_b.md" in names


def test_extract_evidence_from_documents_excludes_non_matching_documents():
    docs = {
        "match.md": "Safeguarding is a core principle.",
        "no_match.md": "This document covers office supplies and stationery.",
    }
    results = extract_evidence_from_documents(docs, "safeguarding")
    names = [r["document_name"] for r in results]
    assert "no_match.md" not in names


def test_extract_evidence_from_documents_sorted_by_relevance_count_descending():
    docs = {
        "high.md": "safeguarding safeguarding safeguarding — three occurrences.",
        "low.md": "one mention of safeguarding here.",
    }
    results = extract_evidence_from_documents(docs, "safeguarding")
    assert len(results) >= 2
    assert results[0]["relevance_count"] >= results[1]["relevance_count"]


def test_extract_evidence_from_documents_empty_dict_returns_empty_list():
    assert extract_evidence_from_documents({}, "safeguarding") == []


def test_extract_evidence_from_documents_unsupported_topic_returns_empty_list():
    docs = {"policy.md": SAMPLE_TEXT}
    assert extract_evidence_from_documents(docs, "xyz_unknown_topic") == []
