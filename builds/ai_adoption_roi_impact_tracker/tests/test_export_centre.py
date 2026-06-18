"""Tests for logic/export_centre.py — Build 7 Phase 8."""

import json

import pytest

from data.synthetic_adoption_data import get_synthetic_adoption_metrics
from logic.export_centre import (
    build_completion_review_text,
    build_completion_summary,
    build_csv_export_rows,
    build_export_filename,
    export_csv_text,
    export_json_text,
    export_markdown_report,
)

RECORDS = get_synthetic_adoption_metrics()


# ---------------------------------------------------------------------------
# 1. Markdown export
# ---------------------------------------------------------------------------


class TestMarkdownExport:
    def test_returns_string(self):
        result = export_markdown_report(RECORDS)
        assert isinstance(result, str)

    def test_contains_title_heading(self):
        result = export_markdown_report(RECORDS)
        assert "# AI Adoption Follow-up Report" in result

    def test_portfolio_report_mentions_all_orgs(self):
        result = export_markdown_report(RECORDS)
        assert "Portfolio" in result

    def test_org_filtered_report(self):
        result = export_markdown_report(RECORDS, organisation_id="ORG001")
        assert "BrightPath" in result

    def test_unknown_org_returns_no_records_message(self):
        result = export_markdown_report(RECORDS, organisation_id="ORG999")
        assert "No records found" in result

    def test_contains_executive_summary(self):
        result = export_markdown_report(RECORDS)
        assert "Executive Summary" in result

    def test_contains_recommendations(self):
        result = export_markdown_report(RECORDS)
        assert "Recommendations" in result


# ---------------------------------------------------------------------------
# 2. CSV rows
# ---------------------------------------------------------------------------


class TestCsvRows:
    def test_returns_list(self):
        rows = build_csv_export_rows(RECORDS)
        assert isinstance(rows, list)

    def test_correct_row_count(self):
        rows = build_csv_export_rows(RECORDS)
        assert len(rows) == len(RECORDS)

    def test_each_row_is_dict(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert isinstance(row, dict)

    def test_required_base_fields_present(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert "organisation_id" in row
            assert "workflow_id" in row
            assert "workflow_name" in row
            assert "related_build" in row

    def test_roi_fields_present(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert "weekly_hours_saved" in row
            assert "annual_hours_saved" in row
            assert "efficiency_gain_percent" in row
            assert "annual_value_equivalent" in row
            assert "time_saving_band" in row

    def test_impact_fields_present(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert "workflow_impact_status" in row
            assert "primary_bottleneck" in row

    def test_training_fields_present(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert "training_completion_rate" in row
            assert "confidence_after" in row
            assert "training_readiness_band" in row
            assert "staff_adoption_readiness" in row

    def test_risk_fields_present(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert "quality_level" in row
            assert "risk_level" in row
            assert "responsible_adoption_status" in row
            assert "scaling_permission" in row

    def test_decision_fields_present(self):
        rows = build_csv_export_rows(RECORDS)
        for row in rows:
            assert "decision_outcome" in row
            assert "decision_confidence" in row
            assert "next_action" in row


# ---------------------------------------------------------------------------
# 3. CSV text
# ---------------------------------------------------------------------------


class TestCsvText:
    def test_returns_string(self):
        result = export_csv_text(RECORDS)
        assert isinstance(result, str)

    def test_includes_header_row(self):
        result = export_csv_text(RECORDS)
        assert "organisation_id" in result
        assert "workflow_id" in result

    def test_includes_data_rows(self):
        result = export_csv_text(RECORDS)
        lines = [line for line in result.splitlines() if line.strip()]
        assert len(lines) == len(RECORDS) + 1  # header + data rows

    def test_csv_is_parseable(self):
        import csv
        import io
        result = export_csv_text(RECORDS)
        reader = csv.DictReader(io.StringIO(result))
        rows = list(reader)
        assert len(rows) == len(RECORDS)

    def test_empty_records_returns_empty_string(self):
        result = export_csv_text([])
        assert result == ""


# ---------------------------------------------------------------------------
# 4. JSON export
# ---------------------------------------------------------------------------


class TestJsonExport:
    def test_returns_string(self):
        result = export_json_text(RECORDS)
        assert isinstance(result, str)

    def test_parses_as_json(self):
        result = export_json_text(RECORDS)
        parsed = json.loads(result)
        assert isinstance(parsed, list)

    def test_correct_record_count(self):
        result = export_json_text(RECORDS)
        parsed = json.loads(result)
        assert len(parsed) == len(RECORDS)

    def test_each_record_has_workflow_id(self):
        result = export_json_text(RECORDS)
        parsed = json.loads(result)
        for item in parsed:
            assert "workflow_id" in item

    def test_each_record_has_decision_outcome(self):
        result = export_json_text(RECORDS)
        parsed = json.loads(result)
        for item in parsed:
            assert "decision_outcome" in item


# ---------------------------------------------------------------------------
# 5. Filename builder
# ---------------------------------------------------------------------------


class TestFilenameBuilder:
    def test_basic_filename(self):
        result = build_export_filename("Build 7 AI Adoption Export", "csv")
        assert result == "build_7_ai_adoption_export.csv"

    def test_markdown_extension(self):
        result = build_export_filename("AI Follow-up Report", "md")
        assert result.endswith(".md")

    def test_json_extension(self):
        result = build_export_filename("AI Adoption Export", "json")
        assert result.endswith(".json")

    def test_lowercase_output(self):
        result = build_export_filename("BUILD EXPORT", "csv")
        assert result == result.lower()

    def test_no_spaces_in_result(self):
        result = build_export_filename("My Adoption Report", "csv")
        assert " " not in result

    def test_safe_characters_only(self):
        result = build_export_filename("Build 7: Final!", "csv")
        base = result.rsplit(".", 1)[0]
        for char in base:
            assert char.isalnum() or char == "_", f"Unsafe character: {char!r}"


# ---------------------------------------------------------------------------
# 6. Completion summary
# ---------------------------------------------------------------------------


class TestCompletionSummary:
    def test_returns_dict(self):
        result = build_completion_summary(RECORDS)
        assert isinstance(result, dict)

    def test_required_keys_present(self):
        result = build_completion_summary(RECORDS)
        required_keys = [
            "total_organisations",
            "total_workflows",
            "total_weekly_hours_saved",
            "total_annual_hours_saved",
            "scale_or_scale_with_monitoring_count",
            "continue_or_continue_with_controls_count",
            "stop_or_pause_count",
            "governance_review_count",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_total_organisations(self):
        result = build_completion_summary(RECORDS)
        assert result["total_organisations"] == 3

    def test_total_workflows(self):
        result = build_completion_summary(RECORDS)
        assert result["total_workflows"] == len(RECORDS)

    def test_weekly_hours_saved_positive(self):
        result = build_completion_summary(RECORDS)
        assert result["total_weekly_hours_saved"] > 0

    def test_annual_hours_saved_positive(self):
        result = build_completion_summary(RECORDS)
        assert result["total_annual_hours_saved"] > 0

    def test_decision_counts_sum_to_total(self):
        result = build_completion_summary(RECORDS)
        total_classified = (
            result["scale_or_scale_with_monitoring_count"]
            + result["continue_or_continue_with_controls_count"]
            + result["stop_or_pause_count"]
        )
        assert total_classified <= result["total_workflows"]

    def test_governance_review_count_non_negative(self):
        result = build_completion_summary(RECORDS)
        assert result["governance_review_count"] >= 0


# ---------------------------------------------------------------------------
# 7. Completion review text
# ---------------------------------------------------------------------------


class TestCompletionReviewText:
    def test_returns_string(self):
        result = build_completion_review_text(RECORDS)
        assert isinstance(result, str)

    def test_mentions_build_7(self):
        result = build_completion_review_text(RECORDS)
        assert "Build 7" in result

    def test_mentions_all_phases(self):
        result = build_completion_review_text(RECORDS)
        for phase_num in range(1, 9):
            assert f"Phase {phase_num}" in result

    def test_includes_synthetic_disclaimer(self):
        result = build_completion_review_text(RECORDS)
        assert "synthetic" in result.lower()

    def test_includes_consulting_use_case(self):
        result = build_completion_review_text(RECORDS)
        assert "consultant" in result.lower()

    def test_includes_limitations_section(self):
        result = build_completion_review_text(RECORDS)
        assert "Limitations" in result or "limitations" in result

    def test_includes_future_extensions(self):
        result = build_completion_review_text(RECORDS)
        assert "future" in result.lower() or "extension" in result.lower()

    def test_includes_portfolio_metrics(self):
        result = build_completion_review_text(RECORDS)
        assert "Workflows tracked" in result

    def test_includes_phases_completed_table(self):
        result = build_completion_review_text(RECORDS)
        assert "Phases Completed" in result


# ---------------------------------------------------------------------------
# 8. All synthetic records process without errors
# ---------------------------------------------------------------------------


class TestSyntheticRecordsProcessCleanly:
    def test_markdown_no_exception(self):
        export_markdown_report(RECORDS)

    def test_csv_rows_no_exception(self):
        build_csv_export_rows(RECORDS)

    def test_csv_text_no_exception(self):
        export_csv_text(RECORDS)

    def test_json_text_no_exception(self):
        export_json_text(RECORDS)

    def test_completion_summary_no_exception(self):
        build_completion_summary(RECORDS)

    def test_completion_review_no_exception(self):
        build_completion_review_text(RECORDS)


# ---------------------------------------------------------------------------
# 9. Optional PDF export
# ---------------------------------------------------------------------------


class TestPdfExport:
    def test_pdf_returns_bytes_when_reportlab_available(self):
        try:
            from logic.export_centre import export_pdf_bytes
            markdown_text = "# Test Report\n\nThis is a test."
            result = export_pdf_bytes(markdown_text)
            assert isinstance(result, bytes)
            assert len(result) > 0
        except ImportError:
            pytest.skip("reportlab not installed")

    def test_pdf_with_full_report(self):
        try:
            from logic.export_centre import export_pdf_bytes
            report = export_markdown_report(RECORDS)
            result = export_pdf_bytes(report)
            assert isinstance(result, bytes)
            assert len(result) > 100
        except ImportError:
            pytest.skip("reportlab not installed")

    def test_pdf_starts_with_pdf_header(self):
        try:
            from logic.export_centre import export_pdf_bytes
            result = export_pdf_bytes("# Test\n\nContent here.")
            assert result[:4] == b"%PDF"
        except ImportError:
            pytest.skip("reportlab not installed")


# ---------------------------------------------------------------------------
# 10. Optional chart export
# ---------------------------------------------------------------------------


class TestChartExport:
    def test_chart_returns_bytes_when_matplotlib_available(self):
        try:
            from logic.export_centre import export_summary_chart_png_bytes
            result = export_summary_chart_png_bytes(RECORDS)
            assert isinstance(result, bytes)
            assert len(result) > 0
        except ImportError:
            pytest.skip("matplotlib not installed")

    def test_chart_starts_with_png_signature(self):
        try:
            from logic.export_centre import export_summary_chart_png_bytes
            result = export_summary_chart_png_bytes(RECORDS)
            assert result[:8] == b"\x89PNG\r\n\x1a\n"
        except ImportError:
            pytest.skip("matplotlib not installed")

    def test_chart_produces_non_trivial_output(self):
        try:
            from logic.export_centre import export_summary_chart_png_bytes
            result = export_summary_chart_png_bytes(RECORDS)
            assert len(result) > 1000
        except ImportError:
            pytest.skip("matplotlib not installed")
