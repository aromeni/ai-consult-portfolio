"""Tests for src/gap_analysis.py — Build 6 Phase 3."""
import pytest
from src.gap_analysis import (
    classify_gap_severity,
    calculate_gap_priority_score,
    generate_gap_id,
    identify_gap_type,
    generate_gap_risk_statement,
    generate_missing_evidence_statement,
    generate_gap_action_hint,
    generate_domain_gap,
    generate_policy_gap_analysis,
    summarise_gap_analysis,
    prioritise_gaps,
    format_gap_analysis_as_markdown,
)


class TestClassifyGapSeverity:
    def test_not_covered_high_is_critical(self):
        assert classify_gap_severity("Not covered", "High") == "Critical gap"

    def test_weak_high_is_high(self):
        assert classify_gap_severity("Weak coverage", "High") == "High gap"

    def test_partial_high_is_medium(self):
        assert classify_gap_severity("Partial coverage", "High") == "Medium gap"

    def test_not_covered_medium_is_high(self):
        assert classify_gap_severity("Not covered", "Medium") == "High gap"

    def test_weak_medium_is_medium(self):
        assert classify_gap_severity("Weak coverage", "Medium") == "Medium gap"

    def test_partial_medium_is_low(self):
        assert classify_gap_severity("Partial coverage", "Medium") == "Low gap"

    def test_strong_coverage_any_is_no_significant_gap(self):
        assert classify_gap_severity("Strong coverage", "High") == "No significant gap"
        assert classify_gap_severity("Strong coverage", "Medium") == "No significant gap"
        assert classify_gap_severity("Strong coverage", "Low") == "No significant gap"

    def test_not_covered_low_is_medium(self):
        assert classify_gap_severity("Not covered", "Low") == "Medium gap"

    def test_weak_low_is_low(self):
        assert classify_gap_severity("Weak coverage", "Low") == "Low gap"

    def test_partial_low_is_low(self):
        assert classify_gap_severity("Partial coverage", "Low") == "Low gap"


class TestCalculateGapPriorityScore:
    def test_returns_integer(self):
        result = calculate_gap_priority_score(50.0, "High")
        assert isinstance(result, int)

    def test_high_priority_zero_coverage_is_100(self):
        result = calculate_gap_priority_score(0.0, "High")
        assert result == 100

    def test_returns_between_0_and_100(self):
        for score in [0, 25, 50, 75, 100]:
            for priority in ["High", "Medium", "Low"]:
                result = calculate_gap_priority_score(float(score), priority)
                assert 0 <= result <= 100

    def test_high_priority_scores_higher_than_medium(self):
        high = calculate_gap_priority_score(50.0, "High")
        medium = calculate_gap_priority_score(50.0, "Medium")
        assert high > medium

    def test_medium_priority_scores_higher_than_low(self):
        medium = calculate_gap_priority_score(50.0, "Medium")
        low = calculate_gap_priority_score(50.0, "Low")
        assert medium > low

    def test_full_coverage_high_priority_still_clamped(self):
        result = calculate_gap_priority_score(100.0, "High")
        assert 0 <= result <= 100


class TestGenerateGapId:
    def test_formats_single_digit(self):
        assert generate_gap_id(1) == "GAP-001"

    def test_formats_two_digit(self):
        assert generate_gap_id(12) == "GAP-012"

    def test_formats_three_digit(self):
        assert generate_gap_id(100) == "GAP-100"


class TestIdentifyGapType:
    def test_not_covered_maps_to_missing(self):
        result = identify_gap_type({"coverage_level": "Not covered"})
        assert result == "Missing policy evidence"

    def test_weak_maps_to_weak(self):
        result = identify_gap_type({"coverage_level": "Weak coverage"})
        assert result == "Weak policy evidence"

    def test_partial_maps_to_partial(self):
        result = identify_gap_type({"coverage_level": "Partial coverage"})
        assert result == "Partial policy evidence"

    def test_strong_maps_to_covered(self):
        result = identify_gap_type({"coverage_level": "Strong coverage"})
        assert result == "Covered sufficiently"

    def test_unknown_level_maps_to_unknown(self):
        result = identify_gap_type({"coverage_level": "something else"})
        assert result == "Unknown"

    def test_missing_key_maps_to_unknown(self):
        result = identify_gap_type({})
        assert result == "Unknown"


class TestGenerateGapRiskStatement:
    def test_returns_string(self):
        result = generate_gap_risk_statement({"domain_name": "Safeguarding Boundaries"})
        assert isinstance(result, str)

    def test_safeguarding_mentions_safeguarding(self):
        result = generate_gap_risk_statement({"domain_name": "Safeguarding Boundaries"})
        assert "safeguarding" in result.lower()

    def test_data_protection_mentions_data(self):
        result = generate_gap_risk_statement(
            {"domain_name": "Data Protection and Confidentiality"}
        )
        assert "data" in result.lower()

    def test_human_review_mentions_human(self):
        result = generate_gap_risk_statement({"domain_name": "Human Review and Accountability"})
        assert "human" in result.lower() or "sign-off" in result.lower()

    def test_escalation_mentions_reporting(self):
        result = generate_gap_risk_statement({"domain_name": "Escalation and Incident Reporting"})
        assert "report" in result.lower() or "escalation" in result.lower() or "concern" in result.lower()

    def test_unknown_domain_returns_fallback(self):
        result = generate_gap_risk_statement({"domain_name": "Unknown Domain XYZ"})
        assert isinstance(result, str)
        assert len(result) > 10

    def test_empty_domain_returns_fallback(self):
        result = generate_gap_risk_statement({})
        assert isinstance(result, str)
        assert len(result) > 10


class TestGenerateMissingEvidenceStatement:
    def test_returns_string(self):
        result = generate_missing_evidence_statement({})
        assert isinstance(result, str)

    def test_uses_expected_evidence_when_available(self):
        domain_result = {
            "expected_policy_evidence": ["named responsible owner", "approved tools list"]
        }
        result = generate_missing_evidence_statement(domain_result)
        assert "named responsible owner" in result or "approved tools list" in result

    def test_fallback_when_no_expected_evidence(self):
        result = generate_missing_evidence_statement({"expected_policy_evidence": []})
        assert isinstance(result, str)
        assert len(result) > 10

    def test_fallback_when_key_missing(self):
        result = generate_missing_evidence_statement({})
        assert isinstance(result, str)
        assert len(result) > 10


class TestGenerateGapActionHint:
    def test_returns_string(self):
        result = generate_gap_action_hint({"coverage_level": "Not covered", "priority_level": "High"})
        assert isinstance(result, str)

    def test_not_covered_mentions_add(self):
        result = generate_gap_action_hint(
            {"coverage_level": "Not covered", "priority_level": "Medium"}
        )
        assert "add" in result.lower() or "dedicated" in result.lower()

    def test_weak_mentions_strengthen(self):
        result = generate_gap_action_hint(
            {"coverage_level": "Weak coverage", "priority_level": "Medium"}
        )
        assert "strengthen" in result.lower()

    def test_partial_mentions_clarify(self):
        result = generate_gap_action_hint(
            {"coverage_level": "Partial coverage", "priority_level": "Medium"}
        )
        assert "clarify" in result.lower()

    def test_high_priority_includes_scaling_note(self):
        result = generate_gap_action_hint(
            {"coverage_level": "Not covered", "priority_level": "High"}
        )
        assert "scaling" in result.lower() or "adoption" in result.lower()

    def test_non_high_priority_no_scaling_note(self):
        result = generate_gap_action_hint(
            {"coverage_level": "Not covered", "priority_level": "Medium"}
        )
        assert "scaling" not in result.lower()


class TestGenerateDomainGap:
    @pytest.fixture
    def sample_domain_result(self):
        return {
            "domain_id": "GOV-001",
            "domain_name": "Strategy and Ownership",
            "priority_level": "High",
            "coverage_score": 20.0,
            "coverage_level": "Not covered",
            "matched_policies": [],
            "matched_keywords": [],
            "evidence_snippets": [],
            "expected_policy_evidence": ["Named responsible owner", "AI governance policy"],
        }

    def test_returns_expected_keys(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        expected_keys = [
            "gap_id", "domain_id", "domain_name", "priority_level",
            "coverage_score", "coverage_level", "gap_type", "gap_severity",
            "gap_priority_score", "matched_policies", "matched_keywords",
            "evidence_snippets", "expected_policy_evidence",
            "missing_evidence", "risk_statement", "action_hint", "review_note",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_gap_id_format(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert result["gap_id"] == "GAP-001"

    def test_gap_severity_not_covered_high_is_critical(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert result["gap_severity"] == "Critical gap"

    def test_gap_type_not_covered_is_missing(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert result["gap_type"] == "Missing policy evidence"

    def test_risk_statement_is_non_empty_string(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert isinstance(result["risk_statement"], str)
        assert len(result["risk_statement"]) > 10

    def test_missing_evidence_is_non_empty_string(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert isinstance(result["missing_evidence"], str)
        assert len(result["missing_evidence"]) > 10

    def test_action_hint_is_non_empty_string(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert isinstance(result["action_hint"], str)
        assert len(result["action_hint"]) > 10

    def test_gap_priority_score_between_0_and_100(self, sample_domain_result):
        result = generate_domain_gap(sample_domain_result, 1)
        assert 0 <= result["gap_priority_score"] <= 100


class TestGeneratePolicyGapAnalysis:
    @pytest.fixture
    def sample_coverage_results(self):
        return {
            "organisation_name": "BrightPath Skills Training",
            "policy_pack_title": "Synthetic Responsible AI Policy Pack",
            "overall_coverage_score": 45.0,
            "overall_coverage_level": "Weak coverage",
            "domain_results": [
                {
                    "domain_id": "GOV-001",
                    "domain_name": "Strategy and Ownership",
                    "priority_level": "High",
                    "coverage_score": 15.0,
                    "coverage_level": "Not covered",
                    "matched_policies": [],
                    "matched_keywords": [],
                    "evidence_snippets": [],
                    "expected_policy_evidence": ["Named responsible owner"],
                },
                {
                    "domain_id": "GOV-006",
                    "domain_name": "Safeguarding Boundaries",
                    "priority_level": "High",
                    "coverage_score": 85.0,
                    "coverage_level": "Strong coverage",
                    "matched_policies": ["POL-003"],
                    "matched_keywords": ["safeguarding"],
                    "evidence_snippets": ["Safeguarding decisions must be human-led."],
                    "expected_policy_evidence": ["Clear safeguarding boundary statement"],
                },
                {
                    "domain_id": "GOV-009",
                    "domain_name": "Bias, Fairness, and Inclusion",
                    "priority_level": "Medium",
                    "coverage_score": 35.0,
                    "coverage_level": "Weak coverage",
                    "matched_policies": ["POL-001"],
                    "matched_keywords": ["fairness"],
                    "evidence_snippets": [],
                    "expected_policy_evidence": ["Bias review process"],
                },
            ],
            "responsible_use_note": "Synthetic demo only.",
            "prototype_note": "Not a compliance system.",
        }

    def test_returns_expected_keys(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        expected_keys = [
            "organisation_name", "policy_pack_title", "overall_coverage_score",
            "overall_coverage_level", "total_domains_reviewed", "total_gaps",
            "critical_gaps", "high_gaps", "medium_gaps", "low_gaps",
            "prioritised_gaps", "covered_domains", "high_priority_gaps",
            "gap_themes", "recommended_focus", "responsible_use_note", "prototype_note",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_org_name_matches(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_strong_coverage_excluded_from_gaps(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        all_gaps = (
            result["critical_gaps"]
            + result["high_gaps"]
            + result["medium_gaps"]
            + result["low_gaps"]
        )
        gap_domain_names = [g["domain_name"] for g in all_gaps]
        assert "Safeguarding Boundaries" not in gap_domain_names

    def test_strong_coverage_in_covered_list(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        covered_names = [d["domain_name"] for d in result["covered_domains"]]
        assert "Safeguarding Boundaries" in covered_names

    def test_not_covered_high_produces_critical_gap(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        assert len(result["critical_gaps"]) >= 1

    def test_total_gaps_matches_severity_counts(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        expected = (
            len(result["critical_gaps"])
            + len(result["high_gaps"])
            + len(result["medium_gaps"])
            + len(result["low_gaps"])
        )
        assert result["total_gaps"] == expected

    def test_total_domains_reviewed_correct(self, sample_coverage_results):
        result = generate_policy_gap_analysis(sample_coverage_results)
        assert result["total_domains_reviewed"] == 3

    def test_handles_empty_coverage_results(self):
        result = generate_policy_gap_analysis({})
        assert result["total_gaps"] == 0
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_none_safely(self):
        result = generate_policy_gap_analysis(None)
        assert isinstance(result, dict)
        assert result["total_gaps"] == 0

    def test_all_strong_domains_produce_zero_gaps(self):
        coverage = {
            "organisation_name": "Test Org",
            "domain_results": [
                {
                    "domain_id": "GOV-001",
                    "domain_name": "Strategy and Ownership",
                    "priority_level": "High",
                    "coverage_score": 85.0,
                    "coverage_level": "Strong coverage",
                    "matched_policies": ["POL-001"],
                    "matched_keywords": ["governance"],
                    "evidence_snippets": [],
                    "expected_policy_evidence": [],
                },
                {
                    "domain_id": "GOV-006",
                    "domain_name": "Safeguarding Boundaries",
                    "priority_level": "High",
                    "coverage_score": 90.0,
                    "coverage_level": "Strong coverage",
                    "matched_policies": ["POL-003"],
                    "matched_keywords": ["safeguarding"],
                    "evidence_snippets": [],
                    "expected_policy_evidence": [],
                },
            ],
        }
        result = generate_policy_gap_analysis(coverage)
        assert result["total_gaps"] == 0
        assert len(result["covered_domains"]) == 2


class TestSummariseGapAnalysis:
    @pytest.fixture
    def sample_gap_analysis(self):
        return {
            "critical_gaps": [
                {
                    "gap_id": "GAP-001",
                    "domain_name": "Strategy and Ownership",
                    "gap_priority_score": 100,
                }
            ],
            "high_gaps": [
                {
                    "gap_id": "GAP-002",
                    "domain_name": "Approved AI Tools",
                    "gap_priority_score": 80,
                }
            ],
            "medium_gaps": [],
            "low_gaps": [],
            "covered_domains": [
                {"domain_name": "Safeguarding Boundaries", "coverage_score": 85.0}
            ],
            "prioritised_gaps": [
                {
                    "gap_id": "GAP-001",
                    "domain_name": "Strategy and Ownership",
                    "gap_priority_score": 100,
                },
                {
                    "gap_id": "GAP-002",
                    "domain_name": "Approved AI Tools",
                    "gap_priority_score": 80,
                },
            ],
            "gap_themes": ["AI governance strategy and ownership"],
            "recommended_focus": ["Address high-priority gaps first."],
        }

    def test_returns_expected_keys(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        expected_keys = [
            "total_gaps", "critical_gap_count", "high_gap_count",
            "medium_gap_count", "low_gap_count", "covered_domain_count",
            "highest_priority_gap", "top_gap_domains", "gap_themes",
            "overall_gap_position", "recommended_focus",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_total_gaps_correct(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        assert result["total_gaps"] == 2

    def test_critical_count(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        assert result["critical_gap_count"] == 1

    def test_high_count(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        assert result["high_gap_count"] == 1

    def test_medium_count_zero(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        assert result["medium_gap_count"] == 0

    def test_covered_domain_count(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        assert result["covered_domain_count"] == 1

    def test_overall_gap_position_mentions_priority(self, sample_gap_analysis):
        result = summarise_gap_analysis(sample_gap_analysis)
        assert "priority" in result["overall_gap_position"].lower()

    def test_handles_empty_gap_analysis(self):
        result = summarise_gap_analysis({})
        assert result["total_gaps"] == 0

    def test_handles_none_safely(self):
        result = summarise_gap_analysis(None)
        assert isinstance(result, dict)
        assert result["total_gaps"] == 0

    def test_no_gaps_produces_positive_gap_position(self):
        gap_analysis = {
            "critical_gaps": [],
            "high_gaps": [],
            "medium_gaps": [],
            "low_gaps": [],
            "covered_domains": [{"domain_name": "Safeguarding Boundaries"}],
            "prioritised_gaps": [],
            "gap_themes": [],
            "recommended_focus": [],
        }
        result = summarise_gap_analysis(gap_analysis)
        assert "cover" in result["overall_gap_position"].lower()


class TestPrioritiseGaps:
    def test_sorts_descending_by_priority_score(self):
        gaps = [
            {"gap_id": "GAP-001", "gap_priority_score": 40},
            {"gap_id": "GAP-002", "gap_priority_score": 90},
            {"gap_id": "GAP-003", "gap_priority_score": 60},
        ]
        result = prioritise_gaps(gaps)
        assert result[0]["gap_id"] == "GAP-002"
        assert result[1]["gap_id"] == "GAP-003"
        assert result[2]["gap_id"] == "GAP-001"

    def test_empty_list_returns_empty(self):
        assert prioritise_gaps([]) == []

    def test_single_gap_returns_single_item(self):
        gaps = [{"gap_id": "GAP-001", "gap_priority_score": 50}]
        result = prioritise_gaps(gaps)
        assert len(result) == 1

    def test_returns_list(self):
        result = prioritise_gaps([{"gap_priority_score": 50}])
        assert isinstance(result, list)

    def test_original_list_not_mutated(self):
        gaps = [
            {"gap_id": "GAP-001", "gap_priority_score": 40},
            {"gap_id": "GAP-002", "gap_priority_score": 90},
        ]
        original_order = [g["gap_id"] for g in gaps]
        prioritise_gaps(gaps)
        assert [g["gap_id"] for g in gaps] == original_order


class TestFormatGapAnalysisAsMarkdown:
    @pytest.fixture
    def sample_gap_analysis(self):
        return {
            "organisation_name": "BrightPath Skills Training",
            "policy_pack_title": "Synthetic Responsible AI Policy Pack",
            "overall_coverage_score": 45.0,
            "overall_coverage_level": "Weak coverage",
            "total_domains_reviewed": 12,
            "critical_gaps": [],
            "high_gaps": [
                {
                    "gap_id": "GAP-001",
                    "domain_id": "GOV-001",
                    "domain_name": "Strategy and Ownership",
                    "priority_level": "High",
                    "coverage_score": 20.0,
                    "coverage_level": "Not covered",
                    "gap_type": "Missing policy evidence",
                    "gap_severity": "Critical gap",
                    "gap_priority_score": 100,
                    "matched_policies": [],
                    "evidence_snippets": [],
                    "missing_evidence": "The policy pack should include clearer evidence.",
                    "risk_statement": "This creates a risk of inconsistent AI use.",
                    "action_hint": "Add a dedicated policy section.",
                    "review_note": "Human review required.",
                }
            ],
            "medium_gaps": [],
            "low_gaps": [],
            "prioritised_gaps": [],
            "covered_domains": [],
            "gap_themes": ["AI governance strategy"],
            "recommended_focus": ["Address high-priority gaps first."],
            "responsible_use_note": "Synthetic data only.",
            "prototype_note": "Not a compliance system.",
        }

    def test_returns_string(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert isinstance(result, str)

    def test_non_empty(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert len(result) > 100

    def test_title_present(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert "AI Governance Policy Gap Analysis" in result

    def test_responsible_use_boundaries_section_present(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert "Responsible-Use Boundaries" in result

    def test_org_name_present(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert "BrightPath Skills Training" in result

    def test_human_review_note_present(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert "human review" in result.lower()

    def test_responsible_use_text_mentions_synthetic(self, sample_gap_analysis):
        result = format_gap_analysis_as_markdown(sample_gap_analysis)
        assert "synthetic" in result.lower()

    def test_accepts_precomputed_summary(self, sample_gap_analysis):
        summary = summarise_gap_analysis(sample_gap_analysis)
        result = format_gap_analysis_as_markdown(sample_gap_analysis, summary)
        assert isinstance(result, str)

    def test_handles_none_gap_analysis(self):
        result = format_gap_analysis_as_markdown(None)
        assert isinstance(result, str)
