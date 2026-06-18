"""Tests for src/recommendation_engine.py — Build 6 Phase 4."""
import pytest
from src.recommendation_engine import (
    generate_recommendation_id,
    classify_recommendation_priority,
    suggest_policy_action_type,
    suggest_policy_owner,
    suggest_target_policy,
    generate_recommendation_rationale,
    generate_policy_wording_direction,
    generate_implementation_steps,
    generate_review_questions,
    generate_success_criteria,
    generate_recommendation_from_gap,
    generate_policy_recommendations,
    summarise_policy_recommendations,
    prioritise_recommendations,
    format_policy_recommendations_as_markdown,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def critical_gap():
    return {
        "gap_id": "GAP-001",
        "domain_id": "GOV-001",
        "domain_name": "Strategy and Ownership",
        "priority_level": "High",
        "coverage_score": 10.0,
        "coverage_level": "Not covered",
        "gap_severity": "Critical gap",
        "gap_priority_score": 100,
        "matched_policies": [],
        "matched_keywords": [],
        "evidence_snippets": [],
        "expected_policy_evidence": ["Named responsible owner"],
        "risk_statement": "If this domain is missing, governance accountability is unclear.",
        "missing_evidence": "Add a named AI governance lead.",
        "action_hint": "Add a dedicated policy section.",
    }


@pytest.fixture
def high_gap():
    return {
        "gap_id": "GAP-002",
        "domain_id": "GOV-006",
        "domain_name": "Safeguarding Boundaries",
        "priority_level": "High",
        "coverage_score": 30.0,
        "coverage_level": "Weak coverage",
        "gap_severity": "High gap",
        "gap_priority_score": 85,
        "matched_policies": ["POL-003"],
        "matched_keywords": ["safeguarding"],
        "evidence_snippets": [],
        "expected_policy_evidence": ["Clear safeguarding boundary statement"],
        "risk_statement": "If this domain is weak, safeguarding decisions may rely on AI.",
        "missing_evidence": "Strengthen safeguarding escalation routes.",
        "action_hint": "Add escalation routes.",
    }


@pytest.fixture
def medium_gap():
    return {
        "gap_id": "GAP-003",
        "domain_id": "GOV-009",
        "domain_name": "Bias, Fairness, and Inclusion",
        "priority_level": "Medium",
        "coverage_score": 35.0,
        "coverage_level": "Weak coverage",
        "gap_severity": "Medium gap",
        "gap_priority_score": 55,
        "matched_policies": [],
        "matched_keywords": [],
        "evidence_snippets": [],
        "expected_policy_evidence": ["Bias review process"],
        "risk_statement": "If this domain is weak, bias may go undetected.",
        "missing_evidence": "Add bias review process.",
        "action_hint": "Strengthen bias review wording.",
    }


@pytest.fixture
def sample_gap_analysis(critical_gap, high_gap, medium_gap):
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "Synthetic Responsible AI Policy Pack",
        "overall_coverage_score": 45.0,
        "overall_coverage_level": "Weak coverage",
        "total_domains_reviewed": 12,
        "critical_gaps": [critical_gap],
        "high_gaps": [high_gap],
        "medium_gaps": [medium_gap],
        "low_gaps": [],
        "prioritised_gaps": [critical_gap, high_gap, medium_gap],
        "covered_domains": [],
        "responsible_use_note": "Synthetic demo only.",
        "prototype_note": "Not a compliance system.",
    }


@pytest.fixture
def sample_policy_pack():
    return {
        "organisation_name": "BrightPath Skills Training",
        "policies": [
            {"policy_id": "POL-001", "policy_title": "AI Acceptable Use Policy"},
            {"policy_id": "POL-002", "policy_title": "Data Protection and AI Use Guidance"},
            {"policy_id": "POL-003", "policy_title": "Safeguarding and AI Boundary Policy"},
            {"policy_id": "POL-004", "policy_title": "Staff AI Tool Use Procedure"},
            {"policy_id": "POL-005", "policy_title": "AI Output Review Checklist"},
            {"policy_id": "POL-006", "policy_title": "AI Incident and Escalation Procedure"},
        ],
    }


# ---------------------------------------------------------------------------
# TestGenerateRecommendationId
# ---------------------------------------------------------------------------

class TestGenerateRecommendationId:
    def test_formats_single_digit(self):
        assert generate_recommendation_id(1) == "REC-001"

    def test_formats_two_digit(self):
        assert generate_recommendation_id(12) == "REC-012"

    def test_formats_three_digit(self):
        assert generate_recommendation_id(100) == "REC-100"


# ---------------------------------------------------------------------------
# TestClassifyRecommendationPriority
# ---------------------------------------------------------------------------

class TestClassifyRecommendationPriority:
    def test_critical_gap_returns_urgent(self):
        result = classify_recommendation_priority("Critical gap", 50)
        assert result == "Urgent"

    def test_high_gap_returns_high_priority(self):
        result = classify_recommendation_priority("High gap", 50)
        assert result == "High priority"

    def test_medium_gap_returns_medium_priority(self):
        result = classify_recommendation_priority("Medium gap", 40)
        assert result == "Medium priority"

    def test_low_gap_returns_low_priority(self):
        result = classify_recommendation_priority("Low gap", 20)
        assert result == "Low priority"

    def test_high_score_overrides_low_severity(self):
        result = classify_recommendation_priority("Medium gap", 90)
        assert result == "Urgent"

    def test_score_85_returns_urgent(self):
        result = classify_recommendation_priority("Low gap", 85)
        assert result == "Urgent"

    def test_score_70_returns_high_priority(self):
        result = classify_recommendation_priority("Low gap", 70)
        assert result == "High priority"

    def test_score_45_returns_medium_priority(self):
        result = classify_recommendation_priority("Low gap", 45)
        assert result == "Medium priority"

    def test_score_below_45_returns_low_priority(self):
        result = classify_recommendation_priority("Low gap", 20)
        assert result == "Low priority"


# ---------------------------------------------------------------------------
# TestSuggestPolicyActionType
# ---------------------------------------------------------------------------

class TestSuggestPolicyActionType:
    def test_not_covered_returns_create(self):
        result = suggest_policy_action_type({"coverage_level": "Not covered", "domain_name": "Anything"})
        assert result == "Create new policy section"

    def test_weak_safeguarding_returns_escalation(self):
        result = suggest_policy_action_type({
            "coverage_level": "Weak coverage",
            "domain_name": "Safeguarding Boundaries",
        })
        assert result == "Add escalation route"

    def test_weak_human_review_returns_checklist(self):
        result = suggest_policy_action_type({
            "coverage_level": "Weak coverage",
            "domain_name": "Human Review and Accountability",
        })
        assert result == "Add checklist or control"

    def test_weak_training_returns_training_guidance(self):
        result = suggest_policy_action_type({
            "coverage_level": "Weak coverage",
            "domain_name": "Staff Training and Capability",
        })
        assert result == "Add staff training guidance"

    def test_weak_generic_returns_strengthen(self):
        result = suggest_policy_action_type({
            "coverage_level": "Weak coverage",
            "domain_name": "Strategy and Ownership",
        })
        assert result == "Strengthen existing wording"

    def test_partial_returns_review_and_clarify(self):
        result = suggest_policy_action_type({
            "coverage_level": "Partial coverage",
            "domain_name": "Approved AI Tools",
        })
        assert result == "Review and clarify existing wording"

    def test_returns_string(self):
        result = suggest_policy_action_type({})
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# TestSuggestPolicyOwner
# ---------------------------------------------------------------------------

class TestSuggestPolicyOwner:
    def test_safeguarding_returns_dsl(self):
        result = suggest_policy_owner({"domain_name": "Safeguarding Boundaries"})
        assert "Safeguarding" in result or "safeguarding" in result.lower()

    def test_data_protection_returns_dpo(self):
        result = suggest_policy_owner({"domain_name": "Data Protection and Confidentiality"})
        assert "Data Protection" in result

    def test_staff_training_returns_training_lead(self):
        result = suggest_policy_owner({"domain_name": "Staff Training and Capability"})
        assert "Training" in result or "training" in result.lower()

    def test_unknown_domain_returns_fallback(self):
        result = suggest_policy_owner({"domain_name": "Unknown Domain XYZ"})
        assert "Responsible Manager" in result or "AI Governance" in result

    def test_returns_string(self):
        result = suggest_policy_owner({})
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# TestSuggestTargetPolicy
# ---------------------------------------------------------------------------

class TestSuggestTargetPolicy:
    def test_safeguarding_returns_safeguarding_policy(self):
        gap = {"domain_name": "Safeguarding Boundaries"}
        result = suggest_target_policy(gap)
        assert "Safeguarding" in result or "safeguarding" in result.lower()

    def test_data_protection_returns_data_guidance(self):
        gap = {"domain_name": "Data Protection and Confidentiality"}
        result = suggest_target_policy(gap)
        assert "Data Protection" in result

    def test_escalation_returns_incident_procedure(self):
        gap = {"domain_name": "Escalation and Incident Reporting"}
        result = suggest_target_policy(gap)
        assert "Incident" in result or "Escalation" in result

    def test_missing_policy_pack_returns_generic(self):
        gap = {"domain_name": "Unknown Domain"}
        result = suggest_target_policy(gap)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_string(self):
        result = suggest_target_policy({})
        assert isinstance(result, str)

    def test_with_matching_policy_pack_title(self, sample_policy_pack):
        gap = {"domain_name": "Safeguarding Boundaries"}
        result = suggest_target_policy(gap, sample_policy_pack)
        assert "Safeguarding" in result


# ---------------------------------------------------------------------------
# TestGenerateRecommendationRationale
# ---------------------------------------------------------------------------

class TestGenerateRecommendationRationale:
    def test_returns_string(self, critical_gap):
        result = generate_recommendation_rationale(critical_gap)
        assert isinstance(result, str)

    def test_non_empty(self, critical_gap):
        result = generate_recommendation_rationale(critical_gap)
        assert len(result) > 20

    def test_critical_gap_mentions_high_priority_action(self, critical_gap):
        result = generate_recommendation_rationale(critical_gap)
        assert "critical" in result.lower() or "before" in result.lower()

    def test_uses_risk_statement_when_available(self, critical_gap):
        result = generate_recommendation_rationale(critical_gap)
        assert "governance accountability" in result.lower() or "missing" in result.lower()

    def test_handles_empty_gap(self):
        result = generate_recommendation_rationale({})
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# TestGeneratePolicyWordingDirection
# ---------------------------------------------------------------------------

class TestGeneratePolicyWordingDirection:
    def test_returns_string(self, critical_gap):
        result = generate_policy_wording_direction(critical_gap)
        assert isinstance(result, str)

    def test_safeguarding_mentions_human_led(self, high_gap):
        result = generate_policy_wording_direction(high_gap)
        assert "human" in result.lower() or "safeguarding" in result.lower()

    def test_data_protection_mentions_personal_data(self):
        gap = {"domain_name": "Data Protection and Confidentiality"}
        result = generate_policy_wording_direction(gap)
        assert "personal" in result.lower() or "data" in result.lower()

    def test_contains_suggested_wording_prefix(self, critical_gap):
        result = generate_policy_wording_direction(critical_gap)
        assert "Suggested wording direction" in result

    def test_unknown_domain_returns_fallback(self):
        result = generate_policy_wording_direction({"domain_name": "Unknown Domain"})
        assert "Suggested wording direction" in result
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# TestGenerateImplementationSteps
# ---------------------------------------------------------------------------

class TestGenerateImplementationSteps:
    def test_returns_list(self, critical_gap):
        result = generate_implementation_steps(critical_gap)
        assert isinstance(result, list)

    def test_returns_non_empty(self, critical_gap):
        result = generate_implementation_steps(critical_gap)
        assert len(result) > 0

    def test_critical_gap_includes_pre_rollout_note(self, critical_gap):
        result = generate_implementation_steps(critical_gap)
        combined = " ".join(result).lower()
        assert "before" in combined or "scaling" in combined or "rollout" in combined

    def test_not_covered_mentions_create(self, critical_gap):
        result = generate_implementation_steps(critical_gap)
        combined = " ".join(result).lower()
        assert "create" in combined or "new policy section" in combined

    def test_weak_coverage_mentions_strengthen(self, medium_gap):
        medium_gap["coverage_level"] = "Weak coverage"
        medium_gap["gap_severity"] = "Medium gap"
        result = generate_implementation_steps(medium_gap)
        combined = " ".join(result).lower()
        assert "strengthen" in combined or "clarify" in combined

    def test_all_steps_are_strings(self, critical_gap):
        result = generate_implementation_steps(critical_gap)
        assert all(isinstance(s, str) for s in result)


# ---------------------------------------------------------------------------
# TestGenerateReviewQuestions
# ---------------------------------------------------------------------------

class TestGenerateReviewQuestions:
    def test_returns_list(self, critical_gap):
        result = generate_review_questions(critical_gap)
        assert isinstance(result, list)

    def test_returns_non_empty(self, critical_gap):
        result = generate_review_questions(critical_gap)
        assert len(result) > 0

    def test_safeguarding_includes_extra_question(self, high_gap):
        result = generate_review_questions(high_gap)
        combined = " ".join(result).lower()
        assert "safeguarding" in combined

    def test_all_questions_are_strings(self, critical_gap):
        result = generate_review_questions(critical_gap)
        assert all(isinstance(q, str) for q in result)


# ---------------------------------------------------------------------------
# TestGenerateSuccessCriteria
# ---------------------------------------------------------------------------

class TestGenerateSuccessCriteria:
    def test_returns_list(self, critical_gap):
        result = generate_success_criteria(critical_gap)
        assert isinstance(result, list)

    def test_returns_non_empty(self, critical_gap):
        result = generate_success_criteria(critical_gap)
        assert len(result) > 0

    def test_safeguarding_includes_escalation_criterion(self, high_gap):
        result = generate_success_criteria(high_gap)
        combined = " ".join(result).lower()
        assert "escalation" in combined or "safeguarding" in combined

    def test_all_criteria_are_strings(self, critical_gap):
        result = generate_success_criteria(critical_gap)
        assert all(isinstance(c, str) for c in result)


# ---------------------------------------------------------------------------
# TestGenerateRecommendationFromGap
# ---------------------------------------------------------------------------

class TestGenerateRecommendationFromGap:
    _EXPECTED_KEYS = [
        "recommendation_id", "related_gap_id", "domain_id", "domain_name",
        "gap_severity", "gap_priority_score", "recommendation_priority",
        "policy_action_type", "target_policy", "suggested_owner",
        "recommendation_title", "rationale", "suggested_wording_direction",
        "implementation_steps", "review_questions", "success_criteria",
        "responsible_use_note", "review_note",
    ]

    def test_returns_expected_keys(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        for key in self._EXPECTED_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_recommendation_id_format(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        assert result["recommendation_id"] == "REC-001"

    def test_critical_gap_produces_urgent(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        assert result["recommendation_priority"] == "Urgent"

    def test_high_gap_produces_high_or_urgent(self, high_gap):
        result = generate_recommendation_from_gap(high_gap, 2)
        assert result["recommendation_priority"] in ("Urgent", "High priority")

    def test_implementation_steps_non_empty(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        assert len(result["implementation_steps"]) > 0

    def test_review_questions_non_empty(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        assert len(result["review_questions"]) > 0

    def test_success_criteria_non_empty(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        assert len(result["success_criteria"]) > 0

    def test_wording_direction_is_string(self, critical_gap):
        result = generate_recommendation_from_gap(critical_gap, 1)
        assert isinstance(result["suggested_wording_direction"], str)

    def test_handles_empty_gap(self):
        result = generate_recommendation_from_gap({}, 1)
        assert isinstance(result, dict)
        assert result["recommendation_id"] == "REC-001"

    def test_target_policy_uses_policy_pack(self, high_gap, sample_policy_pack):
        result = generate_recommendation_from_gap(high_gap, 1, sample_policy_pack)
        assert "Safeguarding" in result["target_policy"]


# ---------------------------------------------------------------------------
# TestGeneratePolicyRecommendations
# ---------------------------------------------------------------------------

class TestGeneratePolicyRecommendations:
    _EXPECTED_KEYS = [
        "organisation_name", "policy_pack_title", "total_recommendations",
        "urgent_recommendations", "high_priority_recommendations",
        "medium_priority_recommendations", "low_priority_recommendations",
        "prioritised_recommendations", "quick_wins", "policy_update_themes",
        "owner_summary", "recommended_sequence", "responsible_use_note", "prototype_note",
    ]

    def test_returns_expected_keys(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        for key in self._EXPECTED_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_org_name_matches(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_total_recommendations_correct(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        expected = (
            len(result["urgent_recommendations"])
            + len(result["high_priority_recommendations"])
            + len(result["medium_priority_recommendations"])
            + len(result["low_priority_recommendations"])
        )
        assert result["total_recommendations"] == expected

    def test_critical_gap_produces_urgent_recommendation(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        assert len(result["urgent_recommendations"]) >= 1

    def test_prioritised_recommendations_non_empty(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        assert len(result["prioritised_recommendations"]) > 0

    def test_quick_wins_is_list(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        assert isinstance(result["quick_wins"], list)

    def test_owner_summary_is_dict(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis)
        assert isinstance(result["owner_summary"], dict)

    def test_handles_empty_gap_analysis(self):
        result = generate_policy_recommendations({})
        assert result["total_recommendations"] == 0
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_none_safely(self):
        result = generate_policy_recommendations(None)
        assert isinstance(result, dict)
        assert result["total_recommendations"] == 0

    def test_missing_policy_pack_still_generates(self, sample_gap_analysis):
        result = generate_policy_recommendations(sample_gap_analysis, policy_pack=None)
        assert result["total_recommendations"] > 0

    def test_with_policy_pack_uses_matching_titles(self, sample_gap_analysis, sample_policy_pack):
        result = generate_policy_recommendations(sample_gap_analysis, sample_policy_pack)
        assert result["total_recommendations"] > 0
        targets = [r["target_policy"] for r in result["prioritised_recommendations"]]
        assert any("Safeguarding" in t for t in targets)


# ---------------------------------------------------------------------------
# TestSummarisePolicyRecommendations
# ---------------------------------------------------------------------------

class TestSummarisePolicyRecommendations:
    _EXPECTED_KEYS = [
        "total_recommendations", "urgent_count", "high_priority_count",
        "medium_priority_count", "low_priority_count", "quick_win_count",
        "top_policy_update_themes", "top_owners", "highest_priority_recommendation",
        "overall_recommendation_position", "recommended_focus",
    ]

    @pytest.fixture
    def sample_recommendations(self, sample_gap_analysis):
        return generate_policy_recommendations(sample_gap_analysis)

    def test_returns_expected_keys(self, sample_recommendations):
        result = summarise_policy_recommendations(sample_recommendations)
        for key in self._EXPECTED_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_total_matches_counts(self, sample_recommendations):
        result = summarise_policy_recommendations(sample_recommendations)
        expected = (
            result["urgent_count"]
            + result["high_priority_count"]
            + result["medium_priority_count"]
            + result["low_priority_count"]
        )
        assert result["total_recommendations"] == expected

    def test_urgent_present_gives_action_required_position(self, sample_recommendations):
        result = summarise_policy_recommendations(sample_recommendations)
        if result["urgent_count"] > 0 or result["high_priority_count"] > 0:
            assert "urgent" in result["overall_recommendation_position"].lower() or \
                   "high-priority" in result["overall_recommendation_position"].lower()

    def test_recommended_focus_non_empty(self, sample_recommendations):
        result = summarise_policy_recommendations(sample_recommendations)
        assert len(result["recommended_focus"]) > 0

    def test_handles_empty_recommendations(self):
        result = summarise_policy_recommendations({})
        assert result["total_recommendations"] == 0

    def test_handles_none_safely(self):
        result = summarise_policy_recommendations(None)
        assert isinstance(result, dict)
        assert result["total_recommendations"] == 0

    def test_no_urgent_or_high_gives_positive_position(self):
        recs = {
            "urgent_recommendations": [],
            "high_priority_recommendations": [],
            "medium_priority_recommendations": [],
            "low_priority_recommendations": [],
            "quick_wins": [],
            "policy_update_themes": [],
            "owner_summary": {},
            "prioritised_recommendations": [],
        }
        result = summarise_policy_recommendations(recs)
        assert "cover" in result["overall_recommendation_position"].lower()

    def test_top_owners_is_list(self, sample_recommendations):
        result = summarise_policy_recommendations(sample_recommendations)
        assert isinstance(result["top_owners"], list)


# ---------------------------------------------------------------------------
# TestPrioritiseRecommendations
# ---------------------------------------------------------------------------

class TestPrioritiseRecommendations:
    def test_sorts_urgent_first(self):
        items = [
            {"recommendation_id": "REC-001", "recommendation_priority": "Low priority", "gap_priority_score": 10},
            {"recommendation_id": "REC-002", "recommendation_priority": "Urgent", "gap_priority_score": 90},
            {"recommendation_id": "REC-003", "recommendation_priority": "Medium priority", "gap_priority_score": 50},
        ]
        result = prioritise_recommendations(items)
        assert result[0]["recommendation_id"] == "REC-002"

    def test_empty_list_returns_empty(self):
        assert prioritise_recommendations([]) == []

    def test_single_item_returns_single(self):
        items = [{"recommendation_id": "REC-001", "recommendation_priority": "High priority", "gap_priority_score": 80}]
        result = prioritise_recommendations(items)
        assert len(result) == 1

    def test_returns_list(self):
        result = prioritise_recommendations([
            {"recommendation_priority": "Medium priority", "gap_priority_score": 50}
        ])
        assert isinstance(result, list)

    def test_same_priority_sorted_by_score_descending(self):
        items = [
            {"recommendation_id": "REC-001", "recommendation_priority": "High priority", "gap_priority_score": 70},
            {"recommendation_id": "REC-002", "recommendation_priority": "High priority", "gap_priority_score": 90},
        ]
        result = prioritise_recommendations(items)
        assert result[0]["recommendation_id"] == "REC-002"

    def test_original_list_not_mutated(self):
        items = [
            {"recommendation_id": "REC-001", "recommendation_priority": "Low priority", "gap_priority_score": 10},
            {"recommendation_id": "REC-002", "recommendation_priority": "Urgent", "gap_priority_score": 90},
        ]
        original_order = [r["recommendation_id"] for r in items]
        prioritise_recommendations(items)
        assert [r["recommendation_id"] for r in items] == original_order


# ---------------------------------------------------------------------------
# TestFormatPolicyRecommendationsAsMarkdown
# ---------------------------------------------------------------------------

class TestFormatPolicyRecommendationsAsMarkdown:
    @pytest.fixture
    def sample_recommendations(self, sample_gap_analysis):
        return generate_policy_recommendations(sample_gap_analysis)

    def test_returns_string(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert isinstance(result, str)

    def test_non_empty(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert len(result) > 100

    def test_title_present(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert "AI Governance Policy Improvement Recommendations" in result

    def test_responsible_use_boundaries_present(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert "Responsible-Use Boundaries" in result

    def test_synthetic_mentioned(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert "synthetic" in result.lower()

    def test_human_review_mentioned(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert "human review" in result.lower()

    def test_wording_direction_disclaimer_present(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert "not legally approved" in result.lower() or "wording direction" in result.lower()

    def test_accepts_precomputed_summary(self, sample_recommendations):
        summary = summarise_policy_recommendations(sample_recommendations)
        result = format_policy_recommendations_as_markdown(sample_recommendations, summary)
        assert isinstance(result, str)

    def test_handles_none_safely(self):
        result = format_policy_recommendations_as_markdown(None)
        assert isinstance(result, str)

    def test_org_name_in_output(self, sample_recommendations):
        result = format_policy_recommendations_as_markdown(sample_recommendations)
        assert "BrightPath Skills Training" in result
