"""
Tests for governance_maturity.py — Build 6 Phase 5
BrightPath ChatGPT Mastery Project
"""

import pytest

from src.governance_maturity import (
    classify_governance_maturity_level,
    get_maturity_level_description,
    get_maturity_level_colour,
    calculate_domain_maturity_score,
    calculate_overall_governance_score,
    identify_maturity_strengths,
    identify_maturity_weaknesses,
    identify_maturity_blockers,
    generate_maturity_improvement_priorities,
    generate_adoption_readiness_position,
    generate_governance_maturity_summary,
    summarise_governance_maturity,
    format_governance_maturity_as_markdown,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_domain_result_high():
    return {
        "domain_id": "GOV-006",
        "domain_name": "Safeguarding Boundaries",
        "priority_level": "High",
        "coverage_score": 30,
        "coverage_level": "Weak coverage",
    }


@pytest.fixture
def sample_domain_result_medium():
    return {
        "domain_id": "GOV-008",
        "domain_name": "Accuracy and Hallucination Control",
        "priority_level": "Medium",
        "coverage_score": 70,
        "coverage_level": "Partial coverage",
    }


@pytest.fixture
def sample_domain_result_strong():
    return {
        "domain_id": "GOV-007",
        "domain_name": "Human Review and Accountability",
        "priority_level": "High",
        "coverage_score": 85,
        "coverage_level": "Strong coverage",
    }


@pytest.fixture
def critical_gap():
    return {
        "gap_id": "GAP-001",
        "domain_name": "Safeguarding Boundaries",
        "gap_severity": "Critical gap",
        "coverage_score": 30,
        "priority_level": "High",
        "risk_statement": "Safeguarding is at risk.",
        "action_hint": "Add an escalation route.",
    }


@pytest.fixture
def high_gap():
    return {
        "gap_id": "GAP-002",
        "domain_name": "Escalation and Incident Reporting",
        "gap_severity": "High gap",
        "coverage_score": 20,
        "priority_level": "High",
        "risk_statement": "Incidents may go unreported.",
        "action_hint": "Add incident reporting guidance.",
    }


@pytest.fixture
def urgent_rec():
    return {
        "recommendation_id": "REC-001",
        "domain_name": "Safeguarding Boundaries",
        "recommendation_priority": "Urgent",
        "policy_action_type": "Add escalation route",
        "target_policy": "Safeguarding and AI Boundary Policy",
        "rationale": "Critical gap requires immediate action.",
    }


@pytest.fixture
def high_rec():
    return {
        "recommendation_id": "REC-002",
        "domain_name": "Data Protection and Confidentiality",
        "recommendation_priority": "High priority",
        "policy_action_type": "Strengthen existing wording",
        "target_policy": "Data Protection and AI Use Guidance",
        "rationale": "High gap in data protection coverage.",
    }


@pytest.fixture
def sample_coverage_results(sample_domain_result_high, sample_domain_result_medium, sample_domain_result_strong):
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "overall_coverage_score": 62,
        "overall_coverage_level": "Partial coverage",
        "total_policies_reviewed": 6,
        "total_domains_checked": 3,
        "domain_results": [
            sample_domain_result_high,
            sample_domain_result_medium,
            sample_domain_result_strong,
        ],
    }


@pytest.fixture
def sample_gap_analysis(critical_gap, high_gap):
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "prioritised_gaps": [critical_gap, high_gap],
        "covered_domains": [],
        "total_domains_reviewed": 3,
        "total_gaps": 2,
        "critical_gaps": [critical_gap],
        "high_gaps": [high_gap],
    }


@pytest.fixture
def sample_recommendations(urgent_rec, high_rec):
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "prioritised_recommendations": [urgent_rec, high_rec],
        "total_recommendations": 2,
        "urgent_recommendations": [urgent_rec],
        "high_priority_recommendations": [high_rec],
    }


# ---------------------------------------------------------------------------
# classify_governance_maturity_level
# ---------------------------------------------------------------------------

class TestClassifyGovernanceMaturityLevel:
    def test_initial_at_zero(self):
        assert classify_governance_maturity_level(0) == "Initial governance"

    def test_initial_at_24(self):
        assert classify_governance_maturity_level(24) == "Initial governance"

    def test_developing_at_25(self):
        assert classify_governance_maturity_level(25) == "Developing governance"

    def test_developing_at_49(self):
        assert classify_governance_maturity_level(49) == "Developing governance"

    def test_defined_at_50(self):
        assert classify_governance_maturity_level(50) == "Defined governance"

    def test_defined_at_74(self):
        assert classify_governance_maturity_level(74) == "Defined governance"

    def test_managed_at_75(self):
        assert classify_governance_maturity_level(75) == "Managed governance"

    def test_managed_at_89(self):
        assert classify_governance_maturity_level(89) == "Managed governance"

    def test_optimised_at_90(self):
        assert classify_governance_maturity_level(90) == "Optimised governance"

    def test_optimised_at_100(self):
        assert classify_governance_maturity_level(100) == "Optimised governance"


# ---------------------------------------------------------------------------
# get_maturity_level_description
# ---------------------------------------------------------------------------

class TestGetMaturityLevelDescription:
    def test_initial_governance_description_is_nonempty(self):
        desc = get_maturity_level_description("Initial governance")
        assert len(desc) > 10

    def test_developing_governance_description_is_nonempty(self):
        desc = get_maturity_level_description("Developing governance")
        assert len(desc) > 10

    def test_defined_governance_description_is_nonempty(self):
        desc = get_maturity_level_description("Defined governance")
        assert len(desc) > 10

    def test_managed_governance_description_is_nonempty(self):
        desc = get_maturity_level_description("Managed governance")
        assert len(desc) > 10

    def test_optimised_governance_description_is_nonempty(self):
        desc = get_maturity_level_description("Optimised governance")
        assert len(desc) > 10

    def test_unknown_level_returns_fallback(self):
        desc = get_maturity_level_description("Unknown level")
        assert isinstance(desc, str)
        assert len(desc) > 0


# ---------------------------------------------------------------------------
# get_maturity_level_colour
# ---------------------------------------------------------------------------

class TestGetMaturityLevelColour:
    def test_initial_is_red(self):
        assert get_maturity_level_colour("Initial governance") == "red"

    def test_developing_is_orange(self):
        assert get_maturity_level_colour("Developing governance") == "orange"

    def test_optimised_is_green(self):
        assert get_maturity_level_colour("Optimised governance") == "green"

    def test_unknown_returns_string(self):
        result = get_maturity_level_colour("Unknown")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# calculate_domain_maturity_score
# ---------------------------------------------------------------------------

class TestCalculateDomainMaturityScore:
    def test_returns_expected_keys(self, sample_domain_result_high):
        result = calculate_domain_maturity_score(sample_domain_result_high)
        for key in [
            "domain_id", "domain_name", "priority_level", "coverage_score",
            "coverage_level", "maturity_score", "maturity_level",
            "related_gap_severity", "related_recommendation_priority",
            "maturity_explanation", "recommended_focus",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_score_within_bounds(self, sample_domain_result_high):
        result = calculate_domain_maturity_score(sample_domain_result_high)
        assert 0 <= result["maturity_score"] <= 100

    def test_critical_gap_applies_penalty(self, sample_domain_result_high, critical_gap):
        without = calculate_domain_maturity_score(sample_domain_result_high)
        with_gap = calculate_domain_maturity_score(sample_domain_result_high, [critical_gap])
        assert with_gap["maturity_score"] < without["maturity_score"]

    def test_high_priority_low_coverage_applies_extra_penalty(self, sample_domain_result_high):
        # coverage_score=30, High priority → extra -10 penalty
        result = calculate_domain_maturity_score(sample_domain_result_high)
        # 30 - 10 (High priority below 50) = 20
        assert result["maturity_score"] == 20

    def test_strong_domain_no_gap_has_high_score(self, sample_domain_result_strong):
        result = calculate_domain_maturity_score(sample_domain_result_strong)
        assert result["maturity_score"] >= 75

    def test_recommendation_penalty_applied(self, sample_domain_result_medium, urgent_rec):
        without = calculate_domain_maturity_score(sample_domain_result_medium)
        with_rec = calculate_domain_maturity_score(
            sample_domain_result_medium, None, [urgent_rec]
        )
        assert with_rec["maturity_score"] < without["maturity_score"]

    def test_score_clamped_at_zero(self):
        domain = {
            "domain_id": "GOV-X",
            "domain_name": "Test Domain",
            "priority_level": "High",
            "coverage_score": 0,
            "coverage_level": "Not covered",
        }
        gap = {"gap_severity": "Critical gap"}
        rec = {"recommendation_priority": "Urgent"}
        result = calculate_domain_maturity_score(domain, [gap], [rec])
        assert result["maturity_score"] >= 0

    def test_maturity_explanation_is_string(self, sample_domain_result_medium):
        result = calculate_domain_maturity_score(sample_domain_result_medium)
        assert isinstance(result["maturity_explanation"], str)
        assert len(result["maturity_explanation"]) > 10

    def test_recommended_focus_is_string(self, sample_domain_result_high):
        result = calculate_domain_maturity_score(sample_domain_result_high)
        assert isinstance(result["recommended_focus"], str)


# ---------------------------------------------------------------------------
# calculate_overall_governance_score
# ---------------------------------------------------------------------------

class TestCalculateOverallGovernanceScore:
    def test_returns_float(self):
        scores = [
            {"maturity_score": 60, "priority_level": "High"},
            {"maturity_score": 80, "priority_level": "Medium"},
        ]
        result = calculate_overall_governance_score(scores)
        assert isinstance(result, float)

    def test_within_bounds(self):
        scores = [
            {"maturity_score": 50, "priority_level": "High"},
            {"maturity_score": 90, "priority_level": "Medium"},
        ]
        result = calculate_overall_governance_score(scores)
        assert 0 <= result <= 100

    def test_empty_returns_zero(self):
        assert calculate_overall_governance_score([]) == 0.0

    def test_high_weight_affects_score(self):
        high_scores = [
            {"maturity_score": 100, "priority_level": "High"},
            {"maturity_score": 0, "priority_level": "Low"},
        ]
        result = calculate_overall_governance_score(high_scores)
        # 100*1.5 / (1.5+0.75) = 150/2.25 = 66.7
        assert result > 50.0

    def test_all_same_score_returns_that_score(self):
        scores = [
            {"maturity_score": 70, "priority_level": "High"},
            {"maturity_score": 70, "priority_level": "Medium"},
            {"maturity_score": 70, "priority_level": "Low"},
        ]
        result = calculate_overall_governance_score(scores)
        assert result == 70.0


# ---------------------------------------------------------------------------
# identify_maturity_strengths
# ---------------------------------------------------------------------------

class TestIdentifyMaturityStrengths:
    def test_returns_list(self):
        scores = [{"maturity_score": 80, "domain_name": "A", "priority_level": "High"}]
        result = identify_maturity_strengths(scores)
        assert isinstance(result, list)

    def test_excludes_below_threshold(self):
        scores = [
            {"maturity_score": 74, "domain_name": "A", "priority_level": "High"},
            {"maturity_score": 80, "domain_name": "B", "priority_level": "Medium"},
        ]
        result = identify_maturity_strengths(scores, threshold=75)
        assert len(result) == 1
        assert result[0]["domain_name"] == "B"

    def test_sorted_descending_by_score(self):
        scores = [
            {"maturity_score": 80, "domain_name": "A", "priority_level": "High"},
            {"maturity_score": 90, "domain_name": "B", "priority_level": "Medium"},
        ]
        result = identify_maturity_strengths(scores, threshold=75)
        assert result[0]["maturity_score"] == 90

    def test_empty_input_returns_empty(self):
        assert identify_maturity_strengths([]) == []


# ---------------------------------------------------------------------------
# identify_maturity_weaknesses
# ---------------------------------------------------------------------------

class TestIdentifyMaturityWeaknesses:
    def test_returns_list(self):
        scores = [{"maturity_score": 30, "domain_name": "A", "priority_level": "High"}]
        result = identify_maturity_weaknesses(scores)
        assert isinstance(result, list)

    def test_excludes_above_threshold(self):
        scores = [
            {"maturity_score": 50, "domain_name": "A", "priority_level": "High"},
            {"maturity_score": 30, "domain_name": "B", "priority_level": "Medium"},
        ]
        result = identify_maturity_weaknesses(scores, threshold=50)
        assert len(result) == 1
        assert result[0]["domain_name"] == "B"

    def test_sorted_ascending_by_score(self):
        scores = [
            {"maturity_score": 40, "domain_name": "A", "priority_level": "High"},
            {"maturity_score": 20, "domain_name": "B", "priority_level": "Medium"},
        ]
        result = identify_maturity_weaknesses(scores, threshold=50)
        assert result[0]["maturity_score"] == 20

    def test_empty_input_returns_empty(self):
        assert identify_maturity_weaknesses([]) == []


# ---------------------------------------------------------------------------
# identify_maturity_blockers
# ---------------------------------------------------------------------------

class TestIdentifyMaturityBlockers:
    def test_returns_list(self):
        result = identify_maturity_blockers()
        assert isinstance(result, list)

    def test_critical_gap_creates_blocker(self, sample_gap_analysis):
        result = identify_maturity_blockers(gap_analysis=sample_gap_analysis)
        assert any("Critical gap" in b.get("blocker_type", "") for b in result)

    def test_high_gap_creates_blocker(self, sample_gap_analysis):
        result = identify_maturity_blockers(gap_analysis=sample_gap_analysis)
        assert any("High gap" in b.get("blocker_type", "") for b in result)

    def test_urgent_rec_creates_blocker_if_no_gap_for_domain(self, sample_recommendations):
        result = identify_maturity_blockers(recommendations=sample_recommendations)
        # Safeguarding Boundaries urgent rec — no gap blocker yet
        types = [b.get("blocker_type", "") for b in result]
        assert any("Urgent" in t for t in types)

    def test_blocker_ids_are_sequential(self, sample_gap_analysis):
        result = identify_maturity_blockers(gap_analysis=sample_gap_analysis)
        ids = [b.get("blocker_id", "") for b in result]
        assert ids[0] == "BLOCKER-001"
        if len(ids) > 1:
            assert ids[1] == "BLOCKER-002"

    def test_each_blocker_has_required_keys(self, sample_gap_analysis):
        result = identify_maturity_blockers(gap_analysis=sample_gap_analysis)
        for b in result:
            for key in ["blocker_id", "domain_name", "blocker_type", "reason", "recommended_action"]:
                assert key in b, f"Missing key: {key}"

    def test_none_inputs_return_empty(self):
        result = identify_maturity_blockers(None, None)
        assert result == []


# ---------------------------------------------------------------------------
# generate_maturity_improvement_priorities
# ---------------------------------------------------------------------------

class TestGenerateMaturityImprovementPriorities:
    def test_returns_list(self):
        summary = {
            "overall_maturity_level": "Initial governance",
            "maturity_blockers": [],
            "maturity_weaknesses": [],
        }
        result = generate_maturity_improvement_priorities(summary)
        assert isinstance(result, list)

    def test_initial_governance_adds_standard_priorities(self):
        summary = {
            "overall_maturity_level": "Initial governance",
            "maturity_blockers": [],
            "maturity_weaknesses": [],
        }
        result = generate_maturity_improvement_priorities(summary)
        assert len(result) >= 1

    def test_blockers_appear_in_priorities(self, sample_gap_analysis):
        blockers = [
            {
                "blocker_id": "BLOCKER-001",
                "domain_name": "Safeguarding Boundaries",
                "blocker_type": "Critical gap",
                "reason": "Critical gap.",
                "recommended_action": "Fix it.",
            }
        ]
        summary = {
            "overall_maturity_level": "Developing governance",
            "maturity_blockers": blockers,
            "maturity_weaknesses": [],
        }
        result = generate_maturity_improvement_priorities(summary)
        assert any("Safeguarding" in p for p in result)

    def test_max_8_priorities(self):
        blockers = [
            {
                "blocker_id": f"BLOCKER-{i:03d}",
                "domain_name": f"Domain {i}",
                "blocker_type": "Critical gap",
                "reason": "x",
                "recommended_action": "y",
            }
            for i in range(1, 10)
        ]
        summary = {
            "overall_maturity_level": "Initial governance",
            "maturity_blockers": blockers,
            "maturity_weaknesses": [],
        }
        result = generate_maturity_improvement_priorities(summary)
        assert len(result) <= 8


# ---------------------------------------------------------------------------
# generate_adoption_readiness_position
# ---------------------------------------------------------------------------

class TestGenerateAdoptionReadinessPosition:
    def test_returns_string(self):
        result = generate_adoption_readiness_position("Defined governance", [])
        assert isinstance(result, str)

    def test_initial_governance_returns_nonempty(self):
        result = generate_adoption_readiness_position("Initial governance", [])
        assert len(result) > 10

    def test_optimised_governance_returns_positive_guidance(self):
        result = generate_adoption_readiness_position("Optimised governance", [])
        assert "monitoring" in result.lower() or "positioned" in result.lower()

    def test_critical_blockers_add_caution(self):
        blockers = [
            {
                "blocker_id": "BLOCKER-001",
                "domain_name": "Safeguarding Boundaries",
                "blocker_type": "Critical gap",
                "reason": "x",
                "recommended_action": "y",
            }
        ]
        result = generate_adoption_readiness_position("Defined governance", blockers)
        assert "blocker" in result.lower() or "critical" in result.lower() or "Safeguarding" in result

    def test_no_blockers_no_extra_caution(self):
        result = generate_adoption_readiness_position("Managed governance", [])
        assert "critical blockers" not in result.lower()


# ---------------------------------------------------------------------------
# generate_governance_maturity_summary
# ---------------------------------------------------------------------------

class TestGenerateGovernanceMaturitySummary:
    def test_returns_expected_keys(self, sample_coverage_results):
        result = generate_governance_maturity_summary(sample_coverage_results)
        for key in [
            "organisation_name", "policy_pack_title", "overall_governance_score",
            "overall_maturity_level", "maturity_description", "domain_maturity_scores",
            "maturity_strengths", "maturity_weaknesses", "maturity_blockers",
            "improvement_priorities", "adoption_readiness_position",
            "recommended_next_step", "responsible_use_note", "prototype_note",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_score_is_numeric(self, sample_coverage_results):
        result = generate_governance_maturity_summary(sample_coverage_results)
        assert isinstance(result["overall_governance_score"], (int, float))
        assert 0 <= result["overall_governance_score"] <= 100

    def test_domain_scores_count_matches_domain_results(self, sample_coverage_results):
        result = generate_governance_maturity_summary(sample_coverage_results)
        assert len(result["domain_maturity_scores"]) == len(
            sample_coverage_results["domain_results"]
        )

    def test_handles_missing_gap_analysis_safely(self, sample_coverage_results):
        result = generate_governance_maturity_summary(sample_coverage_results, None, None)
        assert result["overall_maturity_level"] in [
            "Initial governance", "Developing governance",
            "Defined governance", "Managed governance", "Optimised governance",
        ]

    def test_handles_missing_recommendations_safely(self, sample_coverage_results, sample_gap_analysis):
        result = generate_governance_maturity_summary(
            sample_coverage_results, sample_gap_analysis, None
        )
        assert "domain_maturity_scores" in result

    def test_org_name_populated(self, sample_coverage_results):
        result = generate_governance_maturity_summary(sample_coverage_results)
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_empty_domain_results_returns_safe_summary(self):
        coverage = {
            "organisation_name": "Test Org",
            "policy_pack_title": "Test Pack",
            "domain_results": [],
        }
        result = generate_governance_maturity_summary(coverage)
        assert result["overall_governance_score"] == 0.0
        assert result["overall_maturity_level"] == "Initial governance"

    def test_missing_org_name_uses_fallback(self):
        coverage = {"domain_results": []}
        result = generate_governance_maturity_summary(coverage)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_blockers_populated_from_gap_analysis(self, sample_coverage_results, sample_gap_analysis):
        result = generate_governance_maturity_summary(
            sample_coverage_results, sample_gap_analysis
        )
        assert len(result["maturity_blockers"]) > 0

    def test_full_run_with_gap_and_recs(
        self, sample_coverage_results, sample_gap_analysis, sample_recommendations
    ):
        result = generate_governance_maturity_summary(
            sample_coverage_results, sample_gap_analysis, sample_recommendations
        )
        assert result["overall_governance_score"] >= 0


# ---------------------------------------------------------------------------
# summarise_governance_maturity
# ---------------------------------------------------------------------------

class TestSummariseGovernanceMaturity:
    def test_returns_expected_keys(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = summarise_governance_maturity(maturity_summary)
        for key in [
            "overall_governance_score", "overall_maturity_level", "total_domains",
            "managed_or_optimised_domains", "defined_domains", "developing_domains",
            "initial_domains", "strength_count", "weakness_count", "blocker_count",
            "strongest_domain", "weakest_domain", "overall_position", "recommended_focus",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_total_domains_correct(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = summarise_governance_maturity(maturity_summary)
        assert result["total_domains"] == 3

    def test_level_counts_sum_to_total(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = summarise_governance_maturity(maturity_summary)
        total = (
            result["managed_or_optimised_domains"]
            + result["defined_domains"]
            + result["developing_domains"]
            + result["initial_domains"]
        )
        assert total == result["total_domains"]

    def test_overall_position_is_string(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = summarise_governance_maturity(maturity_summary)
        assert isinstance(result["overall_position"], str)
        assert len(result["overall_position"]) > 10

    def test_recommended_focus_is_list(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = summarise_governance_maturity(maturity_summary)
        assert isinstance(result["recommended_focus"], list)


# ---------------------------------------------------------------------------
# format_governance_maturity_as_markdown
# ---------------------------------------------------------------------------

class TestFormatGovernanceMaturityAsMarkdown:
    def test_returns_string(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert isinstance(result, str)

    def test_contains_title(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "AI Governance Maturity Summary" in result

    def test_contains_overall_score(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Overall Governance Score" in result

    def test_contains_maturity_level_section(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Maturity Level" in result

    def test_contains_adoption_readiness(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Adoption Readiness" in result

    def test_contains_strengths_section(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Governance Strengths" in result

    def test_contains_weaknesses_section(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Governance Weaknesses" in result

    def test_contains_blockers_section(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Maturity Blockers" in result

    def test_contains_domain_scores_table(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Domain Maturity Scores" in result

    def test_contains_responsible_use_boundaries(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Responsible-Use Boundaries" in result

    def test_contains_synthetic_note(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "synthetic" in result.lower() or "demo" in result.lower()

    def test_accepts_precomputed_summary(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        precomputed = summarise_governance_maturity(maturity_summary)
        result = format_governance_maturity_as_markdown(maturity_summary, precomputed)
        assert "AI Governance Maturity Summary" in result

    def test_contains_improvement_priorities(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "Improvement Priorities" in result

    def test_contains_org_name(self, sample_coverage_results):
        maturity_summary = generate_governance_maturity_summary(sample_coverage_results)
        result = format_governance_maturity_as_markdown(maturity_summary)
        assert "BrightPath" in result
