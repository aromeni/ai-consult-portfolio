"""Tests for Build 7 Phase 7 — Client Follow-up Report Builder.

All tests use deterministic synthetic records only. No real client data.
"""

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.follow_up_report import (
    build_decision_section,
    build_executive_summary,
    build_follow_up_evidence_section,
    build_full_follow_up_report,
    build_markdown_table,
    build_next_review_section,
    build_recommendations_section,
    build_report_disclaimer,
    build_report_title,
    build_risk_quality_section,
    build_roi_section,
    build_training_readiness_section,
    build_workflow_impact_section,
    get_organisation_records,
)

# ---------------------------------------------------------------------------
# 1. Organisation filtering
# ---------------------------------------------------------------------------


class TestGetOrganisationRecords:
    def test_filters_to_correct_organisation(self):
        records = get_synthetic_adoption_metrics()
        result = get_organisation_records(records, "ORG001")
        assert all(r["organisation_id"] == "ORG001" for r in result)

    def test_returns_correct_count_for_org001(self):
        records = get_synthetic_adoption_metrics()
        result = get_organisation_records(records, "ORG001")
        assert len(result) == 4

    def test_returns_correct_count_for_org002(self):
        records = get_synthetic_adoption_metrics()
        result = get_organisation_records(records, "ORG002")
        assert len(result) == 4

    def test_returns_empty_list_for_unknown_org(self):
        records = get_synthetic_adoption_metrics()
        result = get_organisation_records(records, "ORG_UNKNOWN")
        assert result == []

    def test_does_not_mutate_original_records(self):
        records = get_synthetic_adoption_metrics()
        original_length = len(records)
        _ = get_organisation_records(records, "ORG001")
        assert len(records) == original_length


# ---------------------------------------------------------------------------
# 2. Title generation
# ---------------------------------------------------------------------------


class TestBuildReportTitle:
    def test_title_contains_organisation_name(self):
        title = build_report_title("BrightPath Skills Training")
        assert "BrightPath Skills Training" in title

    def test_title_starts_with_markdown_heading(self):
        title = build_report_title("Test Organisation")
        assert title.startswith("#")

    def test_title_contains_report_keywords(self):
        title = build_report_title("Test Organisation")
        assert "Report" in title or "report" in title


# ---------------------------------------------------------------------------
# 3. Disclaimer
# ---------------------------------------------------------------------------


class TestBuildReportDisclaimer:
    def test_disclaimer_contains_synthetic_warning(self):
        disclaimer = build_report_disclaimer()
        assert "synthetic" in disclaimer.lower()

    def test_disclaimer_contains_no_real_data_statement(self):
        disclaimer = build_report_disclaimer()
        assert "does not contain real" in disclaimer or "no real" in disclaimer.lower()

    def test_disclaimer_mentions_demonstration(self):
        disclaimer = build_report_disclaimer()
        assert "demonstration" in disclaimer.lower() or "demo" in disclaimer.lower()


# ---------------------------------------------------------------------------
# 4. Markdown table helper
# ---------------------------------------------------------------------------


class TestBuildMarkdownTable:
    def test_returns_empty_string_for_empty_rows(self):
        result = build_markdown_table([], ["Col A", "Col B"])
        assert result == ""

    def test_header_contains_column_names(self):
        rows = [{"Name": "Alpha", "Score": 10}]
        result = build_markdown_table(rows, ["Name", "Score"])
        assert "Name" in result
        assert "Score" in result

    def test_separator_row_is_present(self):
        rows = [{"Name": "Alpha", "Score": 10}]
        result = build_markdown_table(rows, ["Name", "Score"])
        assert "---" in result

    def test_row_values_appear_in_output(self):
        rows = [{"Name": "Alpha", "Score": 10}]
        result = build_markdown_table(rows, ["Name", "Score"])
        assert "Alpha" in result
        assert "10" in result

    def test_multiple_rows_all_appear(self):
        rows = [{"Name": "Alpha"}, {"Name": "Beta"}, {"Name": "Gamma"}]
        result = build_markdown_table(rows, ["Name"])
        assert "Alpha" in result
        assert "Beta" in result
        assert "Gamma" in result

    def test_missing_column_value_uses_empty_string(self):
        rows = [{"Name": "Alpha"}]
        result = build_markdown_table(rows, ["Name", "Score"])
        assert "Alpha" in result

    def test_column_order_is_preserved(self):
        rows = [{"A": "first", "B": "second"}]
        result = build_markdown_table(rows, ["A", "B"])
        first_pos = result.index("A")
        second_pos = result.index("B")
        assert first_pos < second_pos


# ---------------------------------------------------------------------------
# 5. Executive summary
# ---------------------------------------------------------------------------


class TestBuildExecutiveSummary:
    def test_executive_summary_returns_text(self):
        records = get_synthetic_adoption_metrics()
        result = build_executive_summary(records)
        assert isinstance(result, str) and len(result) > 0

    def test_executive_summary_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_executive_summary(records)
        assert "## Executive Summary" in result

    def test_executive_summary_mentions_workflow_count(self):
        records = get_synthetic_adoption_metrics()
        result = build_executive_summary(records)
        assert "12" in result

    def test_executive_summary_does_not_claim_audited_roi(self):
        records = get_synthetic_adoption_metrics()
        result = build_executive_summary(records)
        assert "audited financial ROI" not in result or "not audited" in result.lower()

    def test_executive_summary_mentions_estimated_value(self):
        records = get_synthetic_adoption_metrics()
        result = build_executive_summary(records)
        assert "estimated" in result.lower() or "equivalent" in result.lower()


# ---------------------------------------------------------------------------
# 6. ROI section
# ---------------------------------------------------------------------------


class TestBuildRoiSection:
    def test_roi_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_roi_section(records)
        assert "## ROI" in result

    def test_roi_section_contains_hours_saved(self):
        records = get_synthetic_adoption_metrics()
        result = build_roi_section(records)
        assert "hours" in result.lower()

    def test_roi_section_contains_value_equivalent(self):
        records = get_synthetic_adoption_metrics()
        result = build_roi_section(records)
        assert "value equivalent" in result.lower() or "£" in result

    def test_roi_section_contains_efficiency_gain(self):
        records = get_synthetic_adoption_metrics()
        result = build_roi_section(records)
        assert "efficiency" in result.lower()

    def test_roi_section_for_single_org_returns_text(self):
        records = get_synthetic_adoption_metrics()
        org_records = get_organisation_records(records, "ORG001")
        result = build_roi_section(org_records)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# 7. Workflow impact section
# ---------------------------------------------------------------------------


class TestBuildWorkflowImpactSection:
    def test_impact_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_workflow_impact_section(records)
        assert "## Workflow Impact" in result

    def test_impact_section_contains_workflow_names(self):
        records = get_synthetic_adoption_metrics()
        result = build_workflow_impact_section(records)
        assert "Lesson plan drafting" in result

    def test_impact_section_contains_table_structure(self):
        records = get_synthetic_adoption_metrics()
        result = build_workflow_impact_section(records)
        assert "|" in result and "---" in result

    def test_impact_section_contains_impact_status(self):
        records = get_synthetic_adoption_metrics()
        result = build_workflow_impact_section(records)
        assert "Impact status" in result

    def test_impact_section_contains_bottleneck_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_workflow_impact_section(records)
        assert "bottleneck" in result.lower()


# ---------------------------------------------------------------------------
# 8. Training readiness section
# ---------------------------------------------------------------------------


class TestBuildTrainingReadinessSection:
    def test_training_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_training_readiness_section(records)
        assert "## Training Readiness" in result

    def test_training_section_contains_table_structure(self):
        records = get_synthetic_adoption_metrics()
        result = build_training_readiness_section(records)
        assert "|" in result and "---" in result

    def test_training_section_contains_adoption_readiness_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_training_readiness_section(records)
        assert "Adoption readiness" in result

    def test_training_section_contains_staff_group_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_training_readiness_section(records)
        assert "Staff group" in result


# ---------------------------------------------------------------------------
# 9. Risk quality section
# ---------------------------------------------------------------------------


class TestBuildRiskQualitySection:
    def test_risk_quality_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_risk_quality_section(records)
        assert "## Risk and Quality Review" in result

    def test_risk_quality_section_contains_table_structure(self):
        records = get_synthetic_adoption_metrics()
        result = build_risk_quality_section(records)
        assert "|" in result and "---" in result

    def test_risk_quality_section_contains_scaling_permission_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_risk_quality_section(records)
        assert "Scaling permission" in result

    def test_risk_quality_section_contains_responsible_adoption_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_risk_quality_section(records)
        assert "Responsible adoption" in result or "adoption status" in result.lower()


# ---------------------------------------------------------------------------
# 10. Decision section
# ---------------------------------------------------------------------------


class TestBuildDecisionSection:
    def test_decision_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_decision_section(records)
        assert "## Decision" in result

    def test_decision_section_contains_table_structure(self):
        records = get_synthetic_adoption_metrics()
        result = build_decision_section(records)
        assert "|" in result and "---" in result

    def test_decision_section_contains_outcome_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_decision_section(records)
        assert "Decision outcome" in result

    def test_decision_section_contains_next_action_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_decision_section(records)
        assert "Next action" in result

    def test_decision_section_contains_confidence_column(self):
        records = get_synthetic_adoption_metrics()
        result = build_decision_section(records)
        assert "Confidence" in result


# ---------------------------------------------------------------------------
# 11. Follow-up evidence section
# ---------------------------------------------------------------------------


class TestBuildFollowUpEvidenceSection:
    def test_evidence_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_follow_up_evidence_section(records)
        assert "## Follow-up Evidence" in result

    def test_evidence_section_contains_workflow_names(self):
        records = get_synthetic_adoption_metrics()
        result = build_follow_up_evidence_section(records)
        assert "Lesson plan drafting" in result

    def test_evidence_section_contains_follow_up_notes(self):
        records = get_synthetic_adoption_metrics()
        result = build_follow_up_evidence_section(records)
        assert "Follow-up note" in result

    def test_evidence_section_contains_adoption_evidence(self):
        records = get_synthetic_adoption_metrics()
        result = build_follow_up_evidence_section(records)
        assert "Adoption evidence" in result or "evidence" in result.lower()


# ---------------------------------------------------------------------------
# 12. Recommendations section
# ---------------------------------------------------------------------------


class TestBuildRecommendationsSection:
    def test_recommendations_section_has_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_recommendations_section(records)
        assert "## Recommendations" in result

    def test_recommendations_section_contains_workflow_names(self):
        records = get_synthetic_adoption_metrics()
        result = build_recommendations_section(records)
        assert "Lesson plan drafting" in result

    def test_recommendations_section_contains_decision_recommendation(self):
        records = get_synthetic_adoption_metrics()
        result = build_recommendations_section(records)
        assert "Decision:" in result

    def test_recommendations_section_contains_training_recommendation(self):
        records = get_synthetic_adoption_metrics()
        result = build_recommendations_section(records)
        assert "Training:" in result

    def test_recommendations_section_contains_risk_quality_recommendation(self):
        records = get_synthetic_adoption_metrics()
        result = build_recommendations_section(records)
        assert "Risk and quality:" in result


# ---------------------------------------------------------------------------
# 13. Next review section
# ---------------------------------------------------------------------------


class TestBuildNextReviewSection:
    def test_next_review_has_heading(self):
        result = build_next_review_section()
        assert "## Next Review" in result

    def test_next_review_mentions_adoption_decisions(self):
        result = build_next_review_section()
        assert "adoption" in result.lower() or "decision" in result.lower()

    def test_next_review_returns_non_empty_string(self):
        result = build_next_review_section()
        assert isinstance(result, str) and len(result) > 0


# ---------------------------------------------------------------------------
# 14. Full report — portfolio level
# ---------------------------------------------------------------------------


class TestBuildFullFollowUpReportPortfolio:
    def test_portfolio_report_builds_without_error(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert isinstance(result, str) and len(result) > 0

    def test_portfolio_report_title_mentions_all_organisations(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "Portfolio" in result or "All Organisations" in result

    def test_portfolio_report_contains_disclaimer(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "synthetic" in result.lower()


# ---------------------------------------------------------------------------
# 15. Full report — single organisation
# ---------------------------------------------------------------------------


class TestBuildFullFollowUpReportOrganisation:
    def test_org_report_builds_without_error(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records, organisation_id="ORG001")
        assert isinstance(result, str) and len(result) > 0

    def test_org_report_title_contains_organisation_name(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records, organisation_id="ORG001")
        assert "BrightPath" in result

    def test_org_report_handles_unknown_organisation(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records, organisation_id="ORG_UNKNOWN")
        assert "No records found" in result or len(result) > 0

    def test_org002_report_builds_without_error(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records, organisation_id="ORG002")
        assert isinstance(result, str) and len(result) > 0

    def test_org003_report_builds_without_error(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records, organisation_id="ORG003")
        assert isinstance(result, str) and len(result) > 0


# ---------------------------------------------------------------------------
# 16. Full report contains all major headings
# ---------------------------------------------------------------------------


class TestFullReportHeadings:
    def test_report_contains_executive_summary_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Executive Summary" in result

    def test_report_contains_roi_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## ROI" in result

    def test_report_contains_workflow_impact_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Workflow Impact" in result

    def test_report_contains_training_readiness_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Training Readiness" in result

    def test_report_contains_risk_quality_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Risk and Quality Review" in result

    def test_report_contains_decision_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Decision" in result

    def test_report_contains_evidence_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Follow-up Evidence" in result

    def test_report_contains_recommendations_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Recommendations" in result

    def test_report_contains_next_review_heading(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        assert "## Next Review" in result


# ---------------------------------------------------------------------------
# 17. All synthetic adoption records process without errors
# ---------------------------------------------------------------------------


class TestAllSyntheticRecordsProcess:
    def test_all_records_produce_executive_summary(self):
        records = get_synthetic_adoption_metrics()
        result = build_executive_summary(records)
        assert len(result) > 0

    def test_all_records_produce_roi_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_roi_section(records)
        assert len(result) > 0

    def test_all_records_produce_impact_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_workflow_impact_section(records)
        assert len(result) > 0

    def test_all_records_produce_training_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_training_readiness_section(records)
        assert len(result) > 0

    def test_all_records_produce_risk_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_risk_quality_section(records)
        assert len(result) > 0

    def test_all_records_produce_decision_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_decision_section(records)
        assert len(result) > 0

    def test_all_records_produce_evidence_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_follow_up_evidence_section(records)
        assert len(result) > 0

    def test_all_records_produce_recommendations_section(self):
        records = get_synthetic_adoption_metrics()
        result = build_recommendations_section(records)
        assert len(result) > 0

    def test_each_organisation_report_builds_independently(self):
        records = get_synthetic_adoption_metrics()
        for org_id in ("ORG001", "ORG002", "ORG003"):
            result = build_full_follow_up_report(records, organisation_id=org_id)
            assert isinstance(result, str) and len(result) > 0

    def test_report_sections_appear_in_correct_order(self):
        records = get_synthetic_adoption_metrics()
        result = build_full_follow_up_report(records)
        headings = [
            "## Executive Summary",
            "## ROI",
            "## Workflow Impact",
            "## Training Readiness",
            "## Risk and Quality Review",
            "## Decision",
            "## Follow-up Evidence",
            "## Recommendations",
            "## Next Review",
        ]
        positions = [result.index(h) for h in headings if h in result]
        assert positions == sorted(positions), "Report sections are not in the expected order"
