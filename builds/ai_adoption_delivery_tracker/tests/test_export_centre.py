"""Tests for logic/export_centre.py — Build 8 Phase 8."""

import json

from data.synthetic_implementation_data import (
    get_synthetic_client_checkins,
    get_synthetic_delivery_organisations,
    get_synthetic_implementation_actions,
)
from logic.export_centre import (
    build_completion_review_text,
    build_completion_summary,
    build_csv_export_rows,
    build_export_filename,
    export_csv_text,
    export_json_text,
    export_markdown_report,
    export_pdf_bytes,
    export_summary_chart_png_bytes,
)

ORGANISATIONS = get_synthetic_delivery_organisations()
ACTIONS = get_synthetic_implementation_actions()
CHECKINS = get_synthetic_client_checkins()

EXPECTED_JSON_KEYS = {
    "organisations",
    "implementation_actions",
    "client_checkins",
    "action_tracker_summaries",
    "blocker_review_summaries",
    "governance_summaries",
    "training_followup_summaries",
    "completion_summary",
}

EXPECTED_COMPLETION_KEYS = {
    "total_organisations",
    "total_actions",
    "total_checkins",
    "completed_actions",
    "blocked_actions",
    "in_progress_actions",
    "critical_or_high_priority_actions",
    "governance_signoff_required_actions",
    "training_followup_required_actions",
    "client_checkin_required_actions",
    "escalation_required_actions",
    "high_governance_risk_actions",
    "high_training_delivery_risk_actions",
}


# 1. Markdown export returns non-empty text
class TestExportMarkdownReport:
    def test_returns_string(self):
        result = export_markdown_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert isinstance(result, str)

    def test_returns_non_empty_text(self):
        result = export_markdown_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert len(result) > 500

    def test_organisation_scoped_report(self):
        result = export_markdown_report(
            ORGANISATIONS, ACTIONS, CHECKINS, organisation_id="ORG001"
        )
        assert "BrightPath Skills Training" in result

    def test_portfolio_report_contains_disclaimer(self):
        result = export_markdown_report(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "synthetic portfolio data" in result


# 2. CSV rows are generated
class TestBuildCsvExportRows:
    def test_returns_list_of_dicts(self):
        result = build_csv_export_rows(ACTIONS)
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_row_count_matches_action_count(self):
        result = build_csv_export_rows(ACTIONS)
        assert len(result) == len(ACTIONS)

    def test_rows_contain_action_id(self):
        result = build_csv_export_rows(ACTIONS)
        assert all("action_id" in row for row in result)

    def test_rows_contain_delivery_state(self):
        result = build_csv_export_rows(ACTIONS)
        assert all("delivery_state" in row for row in result)

    def test_rows_contain_blocker_type(self):
        result = build_csv_export_rows(ACTIONS)
        assert all("blocker_type" in row for row in result)

    def test_rows_contain_governance_fields(self):
        result = build_csv_export_rows(ACTIONS)
        assert all("signoff_urgency" in row for row in result)
        assert all("control_area" in row for row in result)

    def test_rows_contain_training_fields(self):
        result = build_csv_export_rows(ACTIONS)
        assert all("training_followup_urgency" in row for row in result)
        assert all("training_support_type" in row for row in result)

    def test_empty_actions_returns_empty_list(self):
        result = build_csv_export_rows([])
        assert result == []


# 3. CSV text includes headers
class TestExportCsvText:
    def test_returns_string(self):
        result = export_csv_text(ACTIONS)
        assert isinstance(result, str)

    def test_contains_action_id_header(self):
        result = export_csv_text(ACTIONS)
        assert "action_id" in result

    def test_contains_delivery_state_header(self):
        result = export_csv_text(ACTIONS)
        assert "delivery_state" in result

    def test_contains_data_rows(self):
        result = export_csv_text(ACTIONS)
        lines = [line for line in result.strip().split("\n") if line]
        # header + 15 data rows
        assert len(lines) == 16

    def test_empty_actions_returns_empty_string(self):
        result = export_csv_text([])
        assert result == ""


# 4 & 5. JSON text parses correctly and includes expected keys
class TestExportJsonText:
    def test_returns_valid_json_string(self):
        result = export_json_text(ORGANISATIONS, ACTIONS, CHECKINS)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_contains_expected_top_level_keys(self):
        result = export_json_text(ORGANISATIONS, ACTIONS, CHECKINS)
        parsed = json.loads(result)
        assert EXPECTED_JSON_KEYS.issubset(parsed.keys())

    def test_organisations_list_is_correct_length(self):
        result = export_json_text(ORGANISATIONS, ACTIONS, CHECKINS)
        parsed = json.loads(result)
        assert len(parsed["organisations"]) == 3

    def test_implementation_actions_list_is_correct_length(self):
        result = export_json_text(ORGANISATIONS, ACTIONS, CHECKINS)
        parsed = json.loads(result)
        assert len(parsed["implementation_actions"]) == 15

    def test_completion_summary_is_included(self):
        result = export_json_text(ORGANISATIONS, ACTIONS, CHECKINS)
        parsed = json.loads(result)
        assert "total_actions" in parsed["completion_summary"]


# 6. Filename builder works
class TestBuildExportFilename:
    def test_basic_filename_with_csv_extension(self):
        result = build_export_filename("build 8 export", "csv")
        assert result == "build_8_export.csv"

    def test_basic_filename_with_json_extension(self):
        result = build_export_filename("build 8 export", "json")
        assert result == "build_8_export.json"

    def test_extension_not_duplicated(self):
        result = build_export_filename("build_8_export.md", "md")
        assert result.count(".md") == 1

    def test_removes_unsafe_characters(self):
        result = build_export_filename("build@8 export!", "csv")
        assert "@" not in result
        assert "!" not in result

    def test_output_is_lowercase(self):
        result = build_export_filename("Build 8 Export", "csv")
        assert result == result.lower()

    def test_leading_dot_in_extension_handled(self):
        result = build_export_filename("build 8 export", ".csv")
        assert result.endswith(".csv")
        assert result.count(".csv") == 1


# 7. Completion summary returns expected keys and correct totals
class TestBuildCompletionSummary:
    def test_returns_dict(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        assert isinstance(result, dict)

    def test_contains_expected_keys(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        assert EXPECTED_COMPLETION_KEYS.issubset(result.keys())

    def test_total_organisations_is_three(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        assert result["total_organisations"] == 3

    def test_total_actions_is_fifteen(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        assert result["total_actions"] == 15

    def test_total_checkins_is_six(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        assert result["total_checkins"] == 6

    def test_numeric_values_are_non_negative(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        for key, value in result.items():
            assert isinstance(value, int)
            assert value >= 0


# 8. Completion review text includes Build 8 and expected content
class TestBuildCompletionReviewText:
    def test_returns_string(self):
        result = build_completion_review_text(ORGANISATIONS, ACTIONS, CHECKINS)
        assert isinstance(result, str)

    def test_contains_build_8_reference(self):
        result = build_completion_review_text(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "Build 8" in result

    def test_contains_all_phase_references(self):
        result = build_completion_review_text(ORGANISATIONS, ACTIONS, CHECKINS)
        for phase_number in range(1, 9):
            assert f"Phase {phase_number}" in result

    def test_contains_limitations_section(self):
        result = build_completion_review_text(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "Limitations" in result

    def test_contains_synthetic_disclaimer(self):
        result = build_completion_review_text(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "synthetic" in result.lower()

    def test_contains_completion_summary_figures(self):
        result = build_completion_review_text(ORGANISATIONS, ACTIONS, CHECKINS)
        assert "**15**" in result
        assert "**3**" in result


# 9. All synthetic records process without errors
class TestSyntheticRecordsProcess:
    def test_csv_export_processes_all_actions(self):
        result = export_csv_text(ACTIONS)
        assert len(result) > 0

    def test_json_export_processes_all_data(self):
        result = export_json_text(ORGANISATIONS, ACTIONS, CHECKINS)
        assert len(result) > 0

    def test_completion_summary_processes_all_data(self):
        result = build_completion_summary(ORGANISATIONS, ACTIONS, CHECKINS)
        assert result["total_actions"] == 15


# 10. Optional PDF function handles availability
class TestExportPdfBytes:
    def test_pdf_export_succeeds_or_raises_import_error(self):
        try:
            result = export_pdf_bytes("# Build 8 Test\n\nSynthetic data only.")
            assert isinstance(result, bytes)
            assert len(result) > 0
        except ImportError as error:
            assert "reportlab" in str(error).lower()

    def test_pdf_export_with_markdown_headings(self):
        try:
            markdown = "# Title\n\n## Section\n\nBody text here.\n"
            result = export_pdf_bytes(markdown)
            assert isinstance(result, bytes)
        except ImportError:
            pass


# 11. Optional chart function handles availability
class TestExportSummaryChartPngBytes:
    def test_chart_export_succeeds_or_raises_import_error(self):
        try:
            result = export_summary_chart_png_bytes(ACTIONS)
            assert isinstance(result, bytes)
            assert len(result) > 0
        except ImportError as error:
            assert "matplotlib" in str(error).lower()

    def test_chart_export_with_empty_actions(self):
        try:
            result = export_summary_chart_png_bytes([])
            assert isinstance(result, bytes)
        except ImportError:
            pass
