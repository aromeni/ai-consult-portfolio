"""Tests for logic/progress_report.py — Build 8 Phase 7."""

from data.synthetic_implementation_data import (
    get_synthetic_client_checkins,
    get_synthetic_delivery_organisations,
    get_synthetic_implementation_actions,
)
from logic.progress_report import (
    build_blocker_dependency_section,
    build_client_checkin_section,
    build_consulting_interpretation_section,
    build_delivery_progress_section,
    build_executive_summary,
    build_full_progress_report,
    build_governance_section,
    build_markdown_table,
    build_next_review_section,
    build_priority_next_actions_section,
    build_report_disclaimer,
    build_report_title,
    build_training_followup_section,
    get_organisation_actions,
)

ORGANISATIONS = get_synthetic_delivery_organisations()
ACTIONS = get_synthetic_implementation_actions()
CHECKINS = get_synthetic_client_checkins()


# 1. Organisation action filtering works
class TestGetOrganisationActions:
    def test_filters_by_organisation_id(self):
        result = get_organisation_actions(ACTIONS, "ORG001")
        assert all(a["organisation_id"] == "ORG001" for a in result)

    def test_returns_correct_count_for_org001(self):
        result = get_organisation_actions(ACTIONS, "ORG001")
        assert len(result) == 5

    def test_returns_empty_for_unknown_organisation(self):
        result = get_organisation_actions(ACTIONS, "UNKNOWN")
        assert result == []

    def test_org002_count_is_correct(self):
        result = get_organisation_actions(ACTIONS, "ORG002")
        assert len(result) == 5

    def test_org003_count_is_correct(self):
        result = get_organisation_actions(ACTIONS, "ORG003")
        assert len(result) == 5


# 2. Markdown table helper works
class TestBuildMarkdownTable:
    def test_returns_table_with_header_and_rows(self):
        rows = [{"name": "Alice", "score": 42}]
        result = build_markdown_table(rows, ["name", "score"])
        assert "| name | score |" in result
        assert "| Alice | 42 |" in result

    def test_preserves_column_order(self):
        rows = [{"b": "two", "a": "one"}]
        result = build_markdown_table(rows, ["a", "b"])
        header_line = result.split("\n")[0]
        assert header_line.index("a") < header_line.index("b")

    def test_handles_empty_rows(self):
        result = build_markdown_table([], ["name", "score"])
        assert "No records" in result

    def test_converts_integers_to_strings(self):
        rows = [{"count": 10}]
        result = build_markdown_table(rows, ["count"])
        assert "10" in result

    def test_converts_booleans_to_strings(self):
        rows = [{"flag": True}]
        result = build_markdown_table(rows, ["flag"])
        assert "True" in result

    def test_returns_separator_row(self):
        rows = [{"x": "v"}]
        result = build_markdown_table(rows, ["x"])
        assert "---" in result

    def test_missing_column_values_are_empty_string(self):
        rows = [{"a": "present"}]
        result = build_markdown_table(rows, ["a", "b"])
        assert "| present |  |" in result


# 3. Title generation works for portfolio and organisation
class TestBuildReportTitle:
    def test_portfolio_title_is_base_title(self):
        result = build_report_title()
        assert result == "# AI Adoption Implementation Progress Report"

    def test_organisation_title_includes_name(self):
        result = build_report_title("BrightPath Skills Training")
        assert "BrightPath Skills Training" in result
        assert result.startswith("# AI Adoption Implementation Progress Report")

    def test_organisation_title_uses_em_dash_separator(self):
        result = build_report_title("BrightPath Skills Training")
        assert "—" in result

    def test_none_argument_returns_base_title(self):
        result = build_report_title(None)
        assert "—" not in result


# 4. Disclaimer contains synthetic data warning
class TestBuildReportDisclaimer:
    def test_contains_synthetic_warning(self):
        result = build_report_disclaimer()
        assert "synthetic portfolio data" in result

    def test_contains_regulated_data_exclusion(self):
        result = build_report_disclaimer()
        assert "regulated data" in result

    def test_contains_demonstration_purposes_note(self):
        result = build_report_disclaimer()
        assert "demonstration purposes" in result


# 5. Executive summary
class TestBuildExecutiveSummary:
    def test_contains_expected_heading(self):
        result = build_executive_summary(ACTIONS)
        assert "## Executive Summary" in result

    def test_contains_total_action_count(self):
        result = build_executive_summary(ACTIONS)
        assert "**15**" in result

    def test_contains_all_required_fields(self):
        result = build_executive_summary(ACTIONS)
        assert "Completed" in result
        assert "Blocked" in result
        assert "Governance" in result
        assert "Training" in result
        assert "Client check-in" in result

    def test_works_with_empty_actions(self):
        result = build_executive_summary([])
        assert "## Executive Summary" in result
        assert "**0**" in result


# 6. Delivery progress section
class TestBuildDeliveryProgressSection:
    def test_contains_expected_heading(self):
        result = build_delivery_progress_section(ACTIONS)
        assert "## Delivery Progress" in result

    def test_contains_action_title_column(self):
        result = build_delivery_progress_section(ACTIONS)
        assert "action_title" in result

    def test_contains_recommendation_column(self):
        result = build_delivery_progress_section(ACTIONS)
        assert "action_recommendation" in result


# 7. Blocker section
class TestBuildBlockerDependencySection:
    def test_contains_expected_heading(self):
        result = build_blocker_dependency_section(ACTIONS)
        assert "## Blocker and Dependency Review" in result

    def test_contains_blocker_type_column(self):
        result = build_blocker_dependency_section(ACTIONS)
        assert "blocker_type" in result

    def test_contains_blocker_severity_column(self):
        result = build_blocker_dependency_section(ACTIONS)
        assert "blocker_severity" in result


# 8. Governance section
class TestBuildGovernanceSection:
    def test_contains_expected_heading(self):
        result = build_governance_section(ACTIONS)
        assert "## Governance Sign-off Position" in result

    def test_contains_signoff_urgency_column(self):
        result = build_governance_section(ACTIONS)
        assert "signoff_urgency" in result

    def test_contains_control_area_column(self):
        result = build_governance_section(ACTIONS)
        assert "control_area" in result


# 9. Training follow-up section
class TestBuildTrainingFollowupSection:
    def test_contains_expected_heading(self):
        result = build_training_followup_section(ACTIONS)
        assert "## Training Follow-up Plan" in result

    def test_contains_training_urgency_column(self):
        result = build_training_followup_section(ACTIONS)
        assert "training_followup_urgency" in result

    def test_contains_training_support_type_column(self):
        result = build_training_followup_section(ACTIONS)
        assert "training_support_type" in result


# 10. Client check-in section
class TestBuildClientCheckinSection:
    def test_organisation_level_contains_heading(self):
        org = ORGANISATIONS[0]
        result = build_client_checkin_section(org, ACTIONS, CHECKINS)
        assert "## Client Check-in Position" in result

    def test_organisation_level_contains_health(self):
        org = ORGANISATIONS[0]
        result = build_client_checkin_section(org, ACTIONS, CHECKINS)
        assert "Health" in result

    def test_portfolio_level_contains_heading(self):
        result = build_client_checkin_section(None, ACTIONS, CHECKINS)
        assert "## Client Check-in Position" in result

    def test_portfolio_level_contains_all_organisations(self):
        result = build_client_checkin_section(None, ACTIONS, CHECKINS)
        assert "BrightPath Skills Training" in result
        assert "Northside Community Advice" in result
        assert "Greenacre Dental Group" in result


# 11. Priority next actions section
class TestBuildPriorityNextActionsSection:
    def test_contains_expected_heading(self):
        result = build_priority_next_actions_section(ACTIONS)
        assert "## Priority Next Actions" in result

    def test_table_has_at_most_10_data_rows(self):
        result = build_priority_next_actions_section(ACTIONS)
        data_lines = [
            line for line in result.split("\n")
            if line.startswith("| ") and "---" not in line and "action_title" not in line
        ]
        assert len(data_lines) <= 10

    def test_contains_action_title_column(self):
        result = build_priority_next_actions_section(ACTIONS)
        assert "action_title" in result


# 12. Consulting interpretation section
class TestBuildConsultingInterpretationSection:
    def test_contains_expected_heading(self):
        result = build_consulting_interpretation_section()
        assert "## Consulting Interpretation" in result

    def test_contains_expected_text(self):
        result = build_consulting_interpretation_section()
        assert "recommendations to managed implementation" in result

    def test_mentions_blocked_items(self):
        result = build_consulting_interpretation_section()
        assert "blocked" in result.lower()

    def test_mentions_client_checkpoint(self):
        result = build_consulting_interpretation_section()
        assert "client checkpoint" in result


# 13. Next review section
class TestBuildNextReviewSection:
    def test_contains_expected_heading(self):
        result = build_next_review_section()
        assert "## Next Review" in result

    def test_contains_blocked_actions_reference(self):
        result = build_next_review_section()
        assert "blocked actions" in result

    def test_contains_sign_offs_reference(self):
        result = build_next_review_section()
        assert "sign-offs" in result


# 14 & 15. Full portfolio and organisation reports
class TestBuildFullProgressReport:
    def test_full_portfolio_report_builds_and_is_non_empty(self):
        result = build_full_progress_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert isinstance(result, str)
        assert len(result) > 500

    def test_full_organisation_report_builds(self):
        result = build_full_progress_report(
            ORGANISATIONS, ACTIONS, CHECKINS, organisation_id="ORG001"
        )
        assert isinstance(result, str)
        assert len(result) > 100

    def test_organisation_report_title_contains_org_name(self):
        result = build_full_progress_report(
            ORGANISATIONS, ACTIONS, CHECKINS, organisation_id="ORG001"
        )
        assert "BrightPath Skills Training" in result

    def test_org002_report_contains_org_name(self):
        result = build_full_progress_report(
            ORGANISATIONS, ACTIONS, CHECKINS, organisation_id="ORG002"
        )
        assert "Northside Community Advice" in result

    def test_org003_report_contains_org_name(self):
        result = build_full_progress_report(
            ORGANISATIONS, ACTIONS, CHECKINS, organisation_id="ORG003"
        )
        assert "Greenacre Dental Group" in result


# 16. Full report contains all major headings
class TestFullReportHeadings:
    def test_portfolio_report_contains_all_major_headings(self):
        result = build_full_progress_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "## Executive Summary" in result
        assert "## Delivery Progress" in result
        assert "## Blocker and Dependency Review" in result
        assert "## Governance Sign-off Position" in result
        assert "## Training Follow-up Plan" in result
        assert "## Client Check-in Position" in result
        assert "## Priority Next Actions" in result
        assert "## Consulting Interpretation" in result
        assert "## Next Review" in result

    def test_organisation_report_contains_all_major_headings(self):
        result = build_full_progress_report(
            ORGANISATIONS, ACTIONS, CHECKINS, organisation_id="ORG001"
        )
        assert "## Executive Summary" in result
        assert "## Delivery Progress" in result
        assert "## Governance Sign-off Position" in result
        assert "## Next Review" in result


# 17. All synthetic records process without errors
class TestAllSyntheticRecordsProcess:
    def test_all_organisations_produce_valid_reports(self):
        for org in ORGANISATIONS:
            result = build_full_progress_report(
                ORGANISATIONS, ACTIONS, CHECKINS,
                organisation_id=org["organisation_id"],
            )
            assert isinstance(result, str)
            assert len(result) > 100

    def test_portfolio_report_processes_all_actions_and_checkins(self):
        result = build_full_progress_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert isinstance(result, str)

    def test_report_contains_synthetic_disclaimer(self):
        result = build_full_progress_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "synthetic portfolio data" in result
