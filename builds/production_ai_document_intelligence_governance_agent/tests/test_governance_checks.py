"""Tests for logic/governance_checks.py — Phase 5.

All tests are deterministic and require no internet access.
Governance checks are rule-based (no ML, no external calls).
"""

from __future__ import annotations

from logic.governance_checks import (
    RISK_CATEGORIES,
    check_chunks,
    check_query,
    check_text,
    highest_risk_level,
    summarise_risk_flags,
)

# ---------------------------------------------------------------------------
# RISK_CATEGORIES structure
# ---------------------------------------------------------------------------

EXPECTED_CATEGORIES = {
    "learner_data",
    "safeguarding",
    "assessment_decisions",
    "disciplinary_complaints",
    "personal_data",
    "confidential_data",
    "funding_eligibility",
    "human_approval_missing",
}

HIGH_RISK_CATEGORIES = {
    "learner_data",
    "safeguarding",
    "assessment_decisions",
    "disciplinary_complaints",
}

MEDIUM_RISK_CATEGORIES = {
    "personal_data",
    "confidential_data",
    "funding_eligibility",
    "human_approval_missing",
}


def test_risk_categories_contains_all_expected_keys():
    assert set(RISK_CATEGORIES.keys()) == EXPECTED_CATEGORIES


def test_risk_categories_each_has_terms():
    for cat, config in RISK_CATEGORIES.items():
        assert "terms" in config, f"{cat} missing 'terms'"


def test_risk_categories_each_has_level():
    for cat, config in RISK_CATEGORIES.items():
        assert "level" in config, f"{cat} missing 'level'"


def test_risk_categories_each_has_action():
    for cat, config in RISK_CATEGORIES.items():
        assert "action" in config, f"{cat} missing 'action'"


def test_risk_categories_terms_are_non_empty_lists():
    for cat, config in RISK_CATEGORIES.items():
        assert isinstance(config["terms"], list), f"{cat} terms not a list"
        assert len(config["terms"]) > 0, f"{cat} terms is empty"


def test_risk_categories_high_risk_levels():
    for cat in HIGH_RISK_CATEGORIES:
        assert RISK_CATEGORIES[cat]["level"] == "High", f"{cat} should be High"


def test_risk_categories_medium_risk_levels():
    for cat in MEDIUM_RISK_CATEGORIES:
        assert RISK_CATEGORIES[cat]["level"] == "Medium", f"{cat} should be Medium"


def test_risk_categories_action_strings_non_empty():
    for cat, config in RISK_CATEGORIES.items():
        assert len(config["action"]) > 0, f"{cat} action is empty"


# ---------------------------------------------------------------------------
# check_text — return structure
# ---------------------------------------------------------------------------


def test_check_text_returns_list():
    assert isinstance(check_text("hello world"), list)


def test_check_text_clean_text_returns_empty():
    assert check_text("The weather is pleasant today.") == []


def test_check_text_flag_has_category_key():
    flags = check_text("safeguarding concern raised")
    assert all("category" in f for f in flags)


def test_check_text_flag_has_risk_level_key():
    flags = check_text("safeguarding concern raised")
    assert all("risk_level" in f for f in flags)


def test_check_text_flag_has_matched_terms_key():
    flags = check_text("safeguarding concern raised")
    assert all("matched_terms" in f for f in flags)


def test_check_text_flag_has_recommended_action_key():
    flags = check_text("safeguarding concern raised")
    assert all("recommended_action" in f for f in flags)


def test_check_text_matched_terms_is_list():
    flags = check_text("safeguarding matter")
    assert all(isinstance(f["matched_terms"], list) for f in flags)


def test_check_text_matched_terms_non_empty():
    flags = check_text("safeguarding matter")
    assert all(len(f["matched_terms"]) > 0 for f in flags)


# ---------------------------------------------------------------------------
# check_text — category detection
# ---------------------------------------------------------------------------


def test_check_text_detects_learner_data():
    flags = check_text("Please enter the learner name into the system.")
    categories = [f["category"] for f in flags]
    assert "learner_data" in categories


def test_check_text_detects_safeguarding():
    flags = check_text("A safeguarding concern has been raised.")
    categories = [f["category"] for f in flags]
    assert "safeguarding" in categories


def test_check_text_detects_assessment_decisions():
    flags = check_text("The AI system assigned a grade to the learner.")
    categories = [f["category"] for f in flags]
    assert "assessment_decisions" in categories


def test_check_text_detects_disciplinary_complaints():
    flags = check_text("A formal disciplinary process has been initiated.")
    categories = [f["category"] for f in flags]
    assert "disciplinary_complaints" in categories


def test_check_text_detects_personal_data():
    flags = check_text("The staff record contains personal data.")
    categories = [f["category"] for f in flags]
    assert "personal_data" in categories


def test_check_text_detects_confidential_data():
    flags = check_text("This document contains confidential information.")
    categories = [f["category"] for f in flags]
    assert "confidential_data" in categories


def test_check_text_detects_funding_eligibility():
    flags = check_text("The ESFA audit found compliance issues.")
    categories = [f["category"] for f in flags]
    assert "funding_eligibility" in categories


def test_check_text_detects_human_approval_missing():
    flags = check_text("The content was published without review.")
    categories = [f["category"] for f in flags]
    assert "human_approval_missing" in categories


def test_check_text_is_case_insensitive():
    flags_lower = check_text("safeguarding concern")
    flags_upper = check_text("SAFEGUARDING CONCERN")
    assert len(flags_lower) == len(flags_upper)


def test_check_text_detects_multiple_categories():
    text = "The learner name was used in a safeguarding referral."
    flags = check_text(text)
    categories = {f["category"] for f in flags}
    assert "learner_data" in categories
    assert "safeguarding" in categories


def test_check_text_matched_terms_contains_triggering_term():
    flags = check_text("There is a safeguarding concern.")
    safeguarding_flag = next(f for f in flags if f["category"] == "safeguarding")
    assert "safeguarding" in safeguarding_flag["matched_terms"]


def test_check_text_risk_level_correct_for_high_category():
    flags = check_text("A disclosure was made regarding abuse.")
    safeguarding_flag = next(f for f in flags if f["category"] == "safeguarding")
    assert safeguarding_flag["risk_level"] == "High"


def test_check_text_risk_level_correct_for_medium_category():
    flags = check_text("The document contains personal data and bank details.")
    personal_flag = next(f for f in flags if f["category"] == "personal_data")
    assert personal_flag["risk_level"] == "Medium"


def test_check_text_recommended_action_is_string():
    flags = check_text("safeguarding referral")
    assert all(isinstance(f["recommended_action"], str) for f in flags)


def test_check_text_recommended_action_non_empty():
    flags = check_text("safeguarding referral")
    assert all(len(f["recommended_action"]) > 0 for f in flags)


def test_check_text_multiple_matched_terms_same_category():
    text = "The learner name and learner id were both included."
    flags = check_text(text)
    learner_flag = next(f for f in flags if f["category"] == "learner_data")
    assert len(learner_flag["matched_terms"]) >= 2


# ---------------------------------------------------------------------------
# check_query
# ---------------------------------------------------------------------------


def test_check_query_returns_list():
    assert isinstance(check_query("any query"), list)


def test_check_query_clean_query_returns_empty():
    assert check_query("What time does the meeting start?") == []


def test_check_query_detects_risk():
    flags = check_query("Can I use ChatGPT to review a safeguarding case?")
    categories = [f["category"] for f in flags]
    assert "safeguarding" in categories


def test_check_query_same_result_as_check_text():
    query = "Enter learner name and attendance into the AI tool."
    assert check_query(query) == check_text(query)


# ---------------------------------------------------------------------------
# check_chunks
# ---------------------------------------------------------------------------

RISKY_CHUNK_A = {
    "chunk_id": "doc_chunk_000",
    "document_id": "policy",
    "source_name": "policy.md",
    "text": "Staff must not enter learner names into AI tools.",
}

RISKY_CHUNK_B = {
    "chunk_id": "doc_chunk_001",
    "document_id": "policy",
    "source_name": "policy.md",
    "text": "Safeguarding referrals must never be processed by AI.",
}

CLEAN_CHUNK = {
    "chunk_id": "doc_chunk_002",
    "document_id": "policy",
    "source_name": "policy.md",
    "text": "Staff should complete the online training module.",
}

DUPLICATE_LEARNER_CHUNK = {
    "chunk_id": "doc_chunk_003",
    "document_id": "policy",
    "source_name": "policy.md",
    "text": "The learner record and learner id must be kept secure.",
}


def test_check_chunks_returns_list():
    assert isinstance(check_chunks([RISKY_CHUNK_A]), list)


def test_check_chunks_empty_list_returns_empty():
    assert check_chunks([]) == []


def test_check_chunks_clean_chunks_return_empty():
    assert check_chunks([CLEAN_CHUNK]) == []


def test_check_chunks_detects_risk_in_single_chunk():
    flags = check_chunks([RISKY_CHUNK_A])
    categories = [f["category"] for f in flags]
    assert "learner_data" in categories


def test_check_chunks_detects_risk_across_chunks():
    flags = check_chunks([RISKY_CHUNK_A, RISKY_CHUNK_B])
    categories = {f["category"] for f in flags}
    assert "learner_data" in categories
    assert "safeguarding" in categories


def test_check_chunks_deduplicates_same_category():
    flags = check_chunks([RISKY_CHUNK_A, DUPLICATE_LEARNER_CHUNK])
    learner_flags = [f for f in flags if f["category"] == "learner_data"]
    assert len(learner_flags) == 1


def test_check_chunks_merges_matched_terms_across_chunks():
    flags = check_chunks([RISKY_CHUNK_A, DUPLICATE_LEARNER_CHUNK])
    learner_flag = next(f for f in flags if f["category"] == "learner_data")
    assert "learner name" in learner_flag["matched_terms"]
    assert "learner record" in learner_flag["matched_terms"]


def test_check_chunks_each_flag_has_required_keys():
    flags = check_chunks([RISKY_CHUNK_A])
    for flag in flags:
        assert "category" in flag
        assert "risk_level" in flag
        assert "matched_terms" in flag
        assert "recommended_action" in flag


# ---------------------------------------------------------------------------
# summarise_risk_flags
# ---------------------------------------------------------------------------

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

ANOTHER_HIGH_FLAG = {
    "category": "assessment_decisions",
    "risk_level": "High",
    "matched_terms": ["grade"],
    "recommended_action": "Requires human review.",
}


def test_summarise_risk_flags_returns_dict():
    assert isinstance(summarise_risk_flags([HIGH_FLAG]), dict)


def test_summarise_risk_flags_empty_input():
    summary = summarise_risk_flags([])
    assert summary["total_flags"] == 0
    assert summary["high_count"] == 0
    assert summary["medium_count"] == 0
    assert summary["low_count"] == 0
    assert summary["categories"] == []


def test_summarise_risk_flags_total_flags():
    summary = summarise_risk_flags([HIGH_FLAG, MEDIUM_FLAG])
    assert summary["total_flags"] == 2


def test_summarise_risk_flags_high_count():
    summary = summarise_risk_flags([HIGH_FLAG, ANOTHER_HIGH_FLAG, MEDIUM_FLAG])
    assert summary["high_count"] == 2


def test_summarise_risk_flags_medium_count():
    summary = summarise_risk_flags([HIGH_FLAG, MEDIUM_FLAG])
    assert summary["medium_count"] == 1


def test_summarise_risk_flags_low_count_is_zero_when_no_low():
    summary = summarise_risk_flags([HIGH_FLAG, MEDIUM_FLAG])
    assert summary["low_count"] == 0


def test_summarise_risk_flags_categories_is_list():
    summary = summarise_risk_flags([HIGH_FLAG])
    assert isinstance(summary["categories"], list)


def test_summarise_risk_flags_categories_contains_flagged_categories():
    summary = summarise_risk_flags([HIGH_FLAG, MEDIUM_FLAG])
    assert "safeguarding" in summary["categories"]
    assert "personal_data" in summary["categories"]


def test_summarise_risk_flags_has_all_required_keys():
    summary = summarise_risk_flags([HIGH_FLAG])
    assert "total_flags" in summary
    assert "high_count" in summary
    assert "medium_count" in summary
    assert "low_count" in summary
    assert "categories" in summary


# ---------------------------------------------------------------------------
# highest_risk_level
# ---------------------------------------------------------------------------


def test_highest_risk_level_empty_returns_none_string():
    assert highest_risk_level([]) == "None"


def test_highest_risk_level_single_high_flag():
    assert highest_risk_level([HIGH_FLAG]) == "High"


def test_highest_risk_level_single_medium_flag():
    assert highest_risk_level([MEDIUM_FLAG]) == "Medium"


def test_highest_risk_level_high_beats_medium():
    assert highest_risk_level([MEDIUM_FLAG, HIGH_FLAG]) == "High"


def test_highest_risk_level_returns_string():
    assert isinstance(highest_risk_level([HIGH_FLAG]), str)


def test_highest_risk_level_multiple_high_flags():
    assert highest_risk_level([HIGH_FLAG, ANOTHER_HIGH_FLAG]) == "High"


def test_highest_risk_level_only_medium_flags():
    assert highest_risk_level([MEDIUM_FLAG]) == "Medium"
