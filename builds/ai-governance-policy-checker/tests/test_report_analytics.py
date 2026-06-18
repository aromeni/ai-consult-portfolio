"""
Tests for src/report_analytics.py — Report Analytics
Build 6 · BrightPath ChatGPT Mastery Project
"""

import pytest

from src.report_analytics import (
    calculate_export_completion_status,
    calculate_coverage_level_counts,
    calculate_gap_severity_counts,
    calculate_recommendation_priority_counts,
    calculate_maturity_level_counts,
    calculate_governance_score_breakdown,
    calculate_report_quality_summary,
    build_governance_report_analytics,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def empty_export_data():
    return {}


@pytest.fixture
def full_export_data():
    return {
        "organisation_name": "BrightPath Skills Training",
        "generated_date": "2026-06-17",
        "source_outputs_available": {
            "policy_pack": True,
            "governance_framework": True,
            "coverage_results": True,
            "gap_analysis": True,
            "policy_recommendations": True,
            "governance_maturity": True,
            "governance_report_markdown": True,
        },
        "coverage_results": {
            "overall_coverage_score": 62,
            "overall_coverage_level": "Partial coverage",
            "total_domains_checked": 12,
            "domain_results": [],
        },
        "coverage_summary": {
            "strong_count": 3,
            "partial_count": 5,
            "weak_count": 2,
            "not_covered_count": 2,
        },
        "gap_analysis": {
            "total_gaps": 5,
            "prioritised_gaps": [
                {"gap_severity": "Critical gap"},
                {"gap_severity": "High gap"},
                {"gap_severity": "High gap"},
                {"gap_severity": "Medium gap"},
                {"gap_severity": "Low gap"},
            ],
        },
        "gap_summary": {
            "total_gaps": 5,
            "critical_gap_count": 1,
            "high_gap_count": 2,
            "medium_gap_count": 1,
            "low_gap_count": 1,
        },
        "policy_recommendations": {
            "total_recommendations": 5,
            "prioritised_recommendations": [
                {"recommendation_priority": "Urgent"},
                {"recommendation_priority": "High priority"},
                {"recommendation_priority": "High priority"},
                {"recommendation_priority": "Medium priority"},
                {"recommendation_priority": "Low priority"},
            ],
        },
        "recommendation_summary": {
            "total_recommendations": 5,
            "urgent_count": 1,
            "high_priority_count": 2,
            "medium_priority_count": 1,
            "low_priority_count": 1,
        },
        "governance_maturity": {
            "overall_governance_score": 48,
            "overall_maturity_level": "Developing governance",
            "domain_maturity_scores": [
                {"domain_name": "Strategy and Ownership", "maturity_score": 35, "maturity_level": "Developing governance"},
                {"domain_name": "Approved AI Tools", "maturity_score": 70, "maturity_level": "Defined governance"},
                {"domain_name": "Data Protection", "maturity_score": 80, "maturity_level": "Managed governance"},
            ],
        },
        "governance_maturity_summary": {
            "total_domains": 12,
            "initial_domains": 2,
            "developing_domains": 4,
            "defined_domains": 3,
            "managed_or_optimised_domains": 3,
        },
        "governance_report_markdown": (
            "# AI Governance Policy Review Report\n\n"
            "## 1. Executive Summary\n\n"
            "## 2. Policy Pack Overview\n\n"
            "## 3. Responsible AI Governance Framework\n\n"
            "## 4. Policy Coverage Review\n\n"
            "## 5. Policy Gap Analysis\n\n"
            "## 6. Policy Improvement Recommendations\n\n"
            "## 7. Governance Score and Maturity Summary\n\n"
            "## 9. Responsible-Use Boundaries\n\nSynthetic/demo policy text only.\n\n"
            "## 10. Prototype Limitations\n\n"
            "Human review required before any real-world use."
        ),
    }


# ---------------------------------------------------------------------------
# calculate_export_completion_status
# ---------------------------------------------------------------------------

class TestCalculateExportCompletionStatus:
    def test_returns_dict(self, empty_export_data):
        result = calculate_export_completion_status(empty_export_data)
        assert isinstance(result, dict)

    def test_expected_keys(self, empty_export_data):
        result = calculate_export_completion_status(empty_export_data)
        for key in ["items", "total", "complete", "incomplete", "completion_percentage"]:
            assert key in result

    def test_empty_data_zero_complete(self, empty_export_data):
        result = calculate_export_completion_status(empty_export_data)
        assert result["complete"] == 0

    def test_empty_data_completion_percentage_zero(self, empty_export_data):
        result = calculate_export_completion_status(empty_export_data)
        assert result["completion_percentage"] == 0.0

    def test_full_data_all_complete(self, full_export_data):
        result = calculate_export_completion_status(full_export_data)
        assert result["complete"] == result["total"]

    def test_full_data_completion_percentage_100(self, full_export_data):
        result = calculate_export_completion_status(full_export_data)
        assert result["completion_percentage"] == 100.0

    def test_items_is_dict(self, full_export_data):
        result = calculate_export_completion_status(full_export_data)
        assert isinstance(result["items"], dict)

    def test_items_values_are_bool(self, full_export_data):
        result = calculate_export_completion_status(full_export_data)
        for v in result["items"].values():
            assert isinstance(v, bool)

    def test_partial_completion(self):
        data = {
            "source_outputs_available": {
                "policy_pack": True,
                "governance_framework": False,
                "coverage_results": False,
                "gap_analysis": False,
                "policy_recommendations": False,
                "governance_maturity": False,
                "governance_report_markdown": True,
            }
        }
        result = calculate_export_completion_status(data)
        assert 0 < result["complete"] < result["total"]


# ---------------------------------------------------------------------------
# calculate_coverage_level_counts
# ---------------------------------------------------------------------------

class TestCalculateCoverageLevelCounts:
    def test_returns_dict(self, empty_export_data):
        result = calculate_coverage_level_counts(empty_export_data)
        assert isinstance(result, dict)

    def test_expected_keys(self, empty_export_data):
        result = calculate_coverage_level_counts(empty_export_data)
        assert "counts" in result
        assert "total" in result

    def test_empty_data_zeros(self, empty_export_data):
        result = calculate_coverage_level_counts(empty_export_data)
        assert result["total"] == 0

    def test_counts_from_summary(self, full_export_data):
        result = calculate_coverage_level_counts(full_export_data)
        assert result["counts"]["Strong coverage"] == 3
        assert result["counts"]["Partial coverage"] == 5
        assert result["counts"]["Weak coverage"] == 2
        assert result["counts"]["Not covered"] == 2

    def test_total_sums_counts(self, full_export_data):
        result = calculate_coverage_level_counts(full_export_data)
        assert result["total"] == sum(result["counts"].values())

    def test_counts_has_four_levels(self, full_export_data):
        result = calculate_coverage_level_counts(full_export_data)
        assert len(result["counts"]) == 4


# ---------------------------------------------------------------------------
# calculate_gap_severity_counts
# ---------------------------------------------------------------------------

class TestCalculateGapSeverityCounts:
    def test_returns_dict(self, empty_export_data):
        result = calculate_gap_severity_counts(empty_export_data)
        assert isinstance(result, dict)

    def test_empty_data_zeros(self, empty_export_data):
        result = calculate_gap_severity_counts(empty_export_data)
        assert result["total"] == 0

    def test_counts_from_summary(self, full_export_data):
        result = calculate_gap_severity_counts(full_export_data)
        assert result["counts"]["Critical gap"] == 1
        assert result["counts"]["High gap"] == 2
        assert result["counts"]["Medium gap"] == 1
        assert result["counts"]["Low gap"] == 1

    def test_total_sums_counts(self, full_export_data):
        result = calculate_gap_severity_counts(full_export_data)
        assert result["total"] == sum(result["counts"].values())

    def test_counts_has_four_severities(self, full_export_data):
        result = calculate_gap_severity_counts(full_export_data)
        assert len(result["counts"]) == 4


# ---------------------------------------------------------------------------
# calculate_recommendation_priority_counts
# ---------------------------------------------------------------------------

class TestCalculateRecommendationPriorityCounts:
    def test_returns_dict(self, empty_export_data):
        result = calculate_recommendation_priority_counts(empty_export_data)
        assert isinstance(result, dict)

    def test_empty_data_zeros(self, empty_export_data):
        result = calculate_recommendation_priority_counts(empty_export_data)
        assert result["total"] == 0

    def test_counts_from_summary(self, full_export_data):
        result = calculate_recommendation_priority_counts(full_export_data)
        assert result["counts"]["Urgent"] == 1
        assert result["counts"]["High priority"] == 2
        assert result["counts"]["Medium priority"] == 1
        assert result["counts"]["Low priority"] == 1

    def test_total_sums_counts(self, full_export_data):
        result = calculate_recommendation_priority_counts(full_export_data)
        assert result["total"] == sum(result["counts"].values())

    def test_counts_has_four_priorities(self, full_export_data):
        result = calculate_recommendation_priority_counts(full_export_data)
        assert len(result["counts"]) == 4


# ---------------------------------------------------------------------------
# calculate_maturity_level_counts
# ---------------------------------------------------------------------------

class TestCalculateMaturityLevelCounts:
    def test_returns_dict(self, empty_export_data):
        result = calculate_maturity_level_counts(empty_export_data)
        assert isinstance(result, dict)

    def test_empty_data_zeros(self, empty_export_data):
        result = calculate_maturity_level_counts(empty_export_data)
        assert result["total"] == 0

    def test_counts_from_summary(self, full_export_data):
        result = calculate_maturity_level_counts(full_export_data)
        assert result["counts"]["Initial governance"] == 2
        assert result["counts"]["Developing governance"] == 4
        assert result["counts"]["Defined governance"] == 3

    def test_counts_has_five_levels(self, full_export_data):
        result = calculate_maturity_level_counts(full_export_data)
        assert len(result["counts"]) == 5


# ---------------------------------------------------------------------------
# calculate_governance_score_breakdown
# ---------------------------------------------------------------------------

class TestCalculateGovernanceScoreBreakdown:
    def test_returns_dict(self, empty_export_data):
        result = calculate_governance_score_breakdown(empty_export_data)
        assert isinstance(result, dict)

    def test_expected_keys(self, empty_export_data):
        result = calculate_governance_score_breakdown(empty_export_data)
        for key in [
            "overall_governance_score", "overall_coverage_score",
            "overall_maturity_level", "overall_coverage_level",
            "domain_maturity_scores",
        ]:
            assert key in result

    def test_empty_data_zero_scores(self, empty_export_data):
        result = calculate_governance_score_breakdown(empty_export_data)
        assert result["overall_governance_score"] == 0
        assert result["overall_coverage_score"] == 0

    def test_scores_from_full_data(self, full_export_data):
        result = calculate_governance_score_breakdown(full_export_data)
        assert result["overall_governance_score"] == 48
        assert result["overall_coverage_score"] == 62

    def test_domain_scores_is_dict(self, full_export_data):
        result = calculate_governance_score_breakdown(full_export_data)
        assert isinstance(result["domain_maturity_scores"], dict)

    def test_domain_scores_populated(self, full_export_data):
        result = calculate_governance_score_breakdown(full_export_data)
        assert "Strategy and Ownership" in result["domain_maturity_scores"]
        assert result["domain_maturity_scores"]["Strategy and Ownership"] == 35


# ---------------------------------------------------------------------------
# calculate_report_quality_summary
# ---------------------------------------------------------------------------

class TestCalculateReportQualitySummary:
    def test_returns_dict(self, empty_export_data):
        result = calculate_report_quality_summary(empty_export_data)
        assert isinstance(result, dict)

    def test_expected_keys(self, empty_export_data):
        result = calculate_report_quality_summary(empty_export_data)
        for key in [
            "executive_summary_included", "policy_pack_overview_included",
            "framework_section_included", "coverage_section_included",
            "gap_analysis_section_included", "recommendations_section_included",
            "maturity_section_included", "responsible_use_boundaries_included",
            "prototype_limitations_included", "human_review_note_included",
            "sections_present", "sections_total", "quality_percentage",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_empty_markdown_all_false(self, empty_export_data):
        result = calculate_report_quality_summary(empty_export_data)
        assert result["sections_present"] == 0

    def test_full_markdown_all_present(self, full_export_data):
        result = calculate_report_quality_summary(full_export_data)
        assert result["executive_summary_included"] is True
        assert result["coverage_section_included"] is True
        assert result["responsible_use_boundaries_included"] is True
        assert result["human_review_note_included"] is True

    def test_quality_percentage_is_float(self, full_export_data):
        result = calculate_report_quality_summary(full_export_data)
        assert isinstance(result["quality_percentage"], float)

    def test_quality_percentage_range(self, full_export_data):
        result = calculate_report_quality_summary(full_export_data)
        assert 0.0 <= result["quality_percentage"] <= 100.0


# ---------------------------------------------------------------------------
# build_governance_report_analytics
# ---------------------------------------------------------------------------

class TestBuildGovernanceReportAnalytics:
    def test_returns_dict(self, empty_export_data):
        result = build_governance_report_analytics(empty_export_data)
        assert isinstance(result, dict)

    def test_expected_top_level_keys(self, empty_export_data):
        result = build_governance_report_analytics(empty_export_data)
        for key in [
            "export_completion", "coverage_levels", "gap_severities",
            "recommendation_priorities", "maturity_levels",
            "governance_scores", "report_quality",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_each_section_is_dict(self, full_export_data):
        result = build_governance_report_analytics(full_export_data)
        for key in result:
            assert isinstance(result[key], dict), f"Section '{key}' is not a dict"

    def test_no_crash_on_empty_data(self, empty_export_data):
        result = build_governance_report_analytics(empty_export_data)
        assert result is not None

    def test_full_data_populates_all_sections(self, full_export_data):
        result = build_governance_report_analytics(full_export_data)
        assert result["export_completion"]["complete"] == result["export_completion"]["total"]
        assert result["coverage_levels"]["total"] == 12
        assert result["gap_severities"]["total"] == 5
        assert result["recommendation_priorities"]["total"] == 5
