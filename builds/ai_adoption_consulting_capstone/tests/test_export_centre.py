"""Tests for logic/export_centre.py — Build 9 Phase 7."""

import json

import pytest

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.export_centre import (
    build_csv_evidence_rows,
    build_export_filename,
    build_portfolio_evidence_summary,
    build_portfolio_evidence_summary_text,
    export_csv_text,
    export_json_evidence_pack,
    export_markdown_capstone_report,
    export_pdf_bytes,
    export_summary_chart_png_bytes,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()

_EXPECTED_EVIDENCE_SUMMARY_KEYS = {
    "total_clients",
    "total_cross_build_stages",
    "total_build_areas",
    "completed_stage_count",
    "in_progress_stage_count",
    "needs_review_stage_count",
    "strong_or_very_strong_evidence_count",
    "capstone_ready_count",
    "nearly_ready_count",
    "needs_strengthening_count",
    "not_ready_count",
    "strongest_build_area",
    "weakest_build_area",
    "dashboard_status",
}

_EXPECTED_JSON_KEYS = {
    "clients",
    "cross_build_stages",
    "capstone_indicators",
    "phase_1_summary",
    "client_journey_summaries",
    "cross_build_summaries",
    "consulting_recommendations",
    "dashboard_snapshot",
    "portfolio_evidence_summary",
}


class TestExportMarkdownCapstoneReport:
    def test_returns_non_empty_string(self):
        result = export_markdown_capstone_report(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_includes_report_heading(self):
        result = export_markdown_capstone_report(CLIENTS, STAGES, INDICATORS)
        assert "# AI Adoption Consulting Capstone Report" in result


class TestBuildCsvEvidenceRows:
    def test_returns_list_of_dicts(self):
        result = build_csv_evidence_rows(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_row_count_matches_stage_count(self):
        result = build_csv_evidence_rows(CLIENTS, STAGES, INDICATORS)
        assert len(result) == len(STAGES)

    def test_rows_include_expected_keys(self):
        result = build_csv_evidence_rows(CLIENTS, STAGES, INDICATORS)
        expected_keys = {
            "client_id",
            "organisation_name",
            "sector",
            "staff_count",
            "capstone_stage",
            "build_number",
            "build_name",
            "journey_stage",
            "stage_status",
            "evidence_strength",
            "consulting_value",
            "readiness_position",
            "governance_position",
            "training_position",
            "roi_position",
            "delivery_position",
            "commercial_position",
            "overall_capstone_status",
            "recommended_next_step",
        }
        assert expected_keys <= set(result[0].keys())


class TestExportCsvText:
    def test_returns_non_empty_string(self):
        result = export_csv_text(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_includes_csv_headers(self):
        result = export_csv_text(CLIENTS, STAGES, INDICATORS)
        assert "client_id" in result
        assert "organisation_name" in result
        assert "evidence_strength" in result

    def test_includes_client_data(self):
        result = export_csv_text(CLIENTS, STAGES, INDICATORS)
        assert "BrightPath Skills Training" in result
        assert "CAP001" in result


class TestExportJsonEvidencePack:
    def test_returns_valid_json_string(self):
        result = export_json_evidence_pack(CLIENTS, STAGES, INDICATORS)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_includes_expected_top_level_keys(self):
        result = export_json_evidence_pack(CLIENTS, STAGES, INDICATORS)
        parsed = json.loads(result)
        assert _EXPECTED_JSON_KEYS <= set(parsed.keys())

    def test_clients_list_has_expected_count(self):
        result = export_json_evidence_pack(CLIENTS, STAGES, INDICATORS)
        parsed = json.loads(result)
        assert len(parsed["clients"]) == 3


class TestBuildExportFilename:
    def test_lowercases_name(self):
        result = build_export_filename("Build 9 Capstone Evidence Pack", "json")
        assert result == result.lower()

    def test_replaces_spaces_with_underscores(self):
        result = build_export_filename("capstone evidence", "csv")
        assert " " not in result
        assert "_" in result

    def test_appends_extension(self):
        result = build_export_filename("capstone_report", "md")
        assert result.endswith(".md")

    def test_does_not_duplicate_extension(self):
        result = build_export_filename("report.json", "json")
        assert result.endswith(".json")
        assert result.count(".json") == 1


class TestBuildPortfolioEvidenceSummary:
    def test_returns_dict(self):
        result = build_portfolio_evidence_summary(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, dict)

    def test_includes_all_expected_keys(self):
        result = build_portfolio_evidence_summary(CLIENTS, STAGES, INDICATORS)
        assert _EXPECTED_EVIDENCE_SUMMARY_KEYS <= set(result.keys())

    def test_total_clients_matches_input(self):
        result = build_portfolio_evidence_summary(CLIENTS, STAGES, INDICATORS)
        assert result["total_clients"] == len(CLIENTS)

    def test_total_build_areas_is_seven(self):
        result = build_portfolio_evidence_summary(CLIENTS, STAGES, INDICATORS)
        assert result["total_build_areas"] == 7


class TestBuildPortfolioEvidenceSummaryText:
    def test_returns_non_empty_string(self):
        result = build_portfolio_evidence_summary_text(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_includes_build_9_reference(self):
        result = build_portfolio_evidence_summary_text(CLIENTS, STAGES, INDICATORS)
        assert "Build 9" in result

    def test_includes_synthetic_data_disclaimer(self):
        result = build_portfolio_evidence_summary_text(CLIENTS, STAGES, INDICATORS)
        assert "synthetic portfolio data" in result

    def test_includes_readiness_information(self):
        result = build_portfolio_evidence_summary_text(CLIENTS, STAGES, INDICATORS)
        assert "Capstone readiness" in result or "capstone ready" in result.lower()


class TestOptionalPdfExport:
    def test_pdf_export_returns_bytes(self):
        markdown = "# Test Report\n\n## Section\n\nSome content.\n"
        result = export_pdf_bytes(markdown)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_pdf_export_produces_valid_pdf_header(self):
        markdown = "# Test\n\nContent.\n"
        result = export_pdf_bytes(markdown)
        assert result[:4] == b"%PDF"


class TestOptionalChartExport:
    def test_chart_export_returns_bytes(self):
        result = export_summary_chart_png_bytes(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_chart_export_produces_valid_png_header(self):
        result = export_summary_chart_png_bytes(CLIENTS, STAGES, INDICATORS)
        assert result[:8] == b"\x89PNG\r\n\x1a\n"


class TestSyntheticDataProcessing:
    def test_all_exports_process_without_errors(self):
        md = export_markdown_capstone_report(CLIENTS, STAGES, INDICATORS)
        csv_text = export_csv_text(CLIENTS, STAGES, INDICATORS)
        json_text = export_json_evidence_pack(CLIENTS, STAGES, INDICATORS)
        summary = build_portfolio_evidence_summary(CLIENTS, STAGES, INDICATORS)
        summary_text = build_portfolio_evidence_summary_text(CLIENTS, STAGES, INDICATORS)

        assert "Executive Summary" in md
        assert "client_id" in csv_text
        assert "dashboard_snapshot" in json_text
        assert "dashboard_status" in summary
        assert "Build 9" in summary_text
