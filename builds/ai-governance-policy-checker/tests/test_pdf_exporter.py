"""
Tests for src/pdf_exporter.py — PDF Exporter
Build 6 · BrightPath ChatGPT Mastery Project
"""

import pytest

from src.pdf_exporter import (
    create_safe_pdf_filename,
    format_pdf_text,
    build_pdf_styles,
    export_governance_report_to_pdf_bytes,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def minimal_export_data():
    return {
        "organisation_name": "BrightPath Skills Training",
        "generated_date": "2026-06-17",
        "governance_report_markdown": (
            "# AI Governance Policy Review Report\n\n"
            "## 1. Executive Summary\n\n"
            "This report presents the findings of an AI governance policy review.\n\n"
            "## 9. Responsible-Use Boundaries\n\n"
            "Synthetic/demo policy text only. Human review required."
        ),
        "source_outputs_available": {"policy_pack": True},
    }


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
            "domain_results": [
                {
                    "domain_name": "Strategy and Ownership",
                    "priority_level": "High",
                    "coverage_score": 35,
                    "coverage_level": "Weak coverage",
                }
            ],
        },
        "gap_analysis": {
            "total_gaps": 3,
            "prioritised_gaps": [
                {
                    "gap_id": "GAP-001",
                    "domain_name": "Strategy and Ownership",
                    "gap_severity": "Critical gap",
                    "priority_level": "High",
                    "coverage_score": 35,
                }
            ],
        },
        "governance_maturity": {
            "overall_governance_score": 48,
            "overall_maturity_level": "Developing governance",
            "maturity_description": "Governance is developing.",
            "adoption_readiness_position": "Not yet ready for broad adoption.",
            "recommended_next_step": "Address critical gaps first.",
            "domain_maturity_scores": [],
        },
        "governance_report_markdown": (
            "# AI Governance Policy Review Report\n\n"
            "**Organisation:** BrightPath Skills Training\n\n"
            "---\n\n"
            "## 1. Executive Summary\n\n"
            "This report presents the findings of an AI governance policy review "
            "for BrightPath Skills Training.\n\n"
            "## 2. Policy Pack Overview\n\n"
            "| Policy | Type | Owner |\n"
            "|---|---|---|\n"
            "| AI Acceptable Use Policy | Acceptable Use | CEO |\n\n"
            "## 4. Policy Coverage Review\n\n"
            "Policy coverage score: 62/100.\n\n"
            "## 5. Policy Gap Analysis\n\n"
            "3 gaps identified.\n\n"
            "## 6. Policy Improvement Recommendations\n\n"
            "Recommendations generated.\n\n"
            "## 7. Governance Score and Maturity Summary\n\n"
            "Score: 48/100.\n\n"
            "## 9. Responsible-Use Boundaries\n\n"
            "Synthetic/demo policy text only.\n\n"
            "## 10. Prototype Limitations\n\n"
            "Human review required before any real-world use.\n\n"
            "## 11. Appendices\n\n"
            "A. Policy List\n\n"
            "> This is a blockquote note.\n\n"
            "1. First step\n"
            "2. Second step\n"
        ),
    }


@pytest.fixture
def sample_analytics():
    return {
        "export_completion": {
            "items": {
                "Policy Pack": True,
                "Governance Report": True,
            },
            "total": 2,
            "complete": 2,
            "incomplete": 0,
            "completion_percentage": 100.0,
        },
        "coverage_levels": {
            "counts": {
                "Strong coverage": 3,
                "Partial coverage": 5,
                "Weak coverage": 2,
                "Not covered": 2,
            },
            "total": 12,
        },
        "gap_severities": {
            "counts": {
                "Critical gap": 1,
                "High gap": 1,
                "Medium gap": 1,
                "Low gap": 0,
            },
            "total": 3,
        },
        "recommendation_priorities": {
            "counts": {
                "Urgent": 1,
                "High priority": 1,
                "Medium priority": 0,
                "Low priority": 0,
            },
            "total": 2,
        },
        "governance_scores": {
            "overall_governance_score": 48,
            "overall_coverage_score": 62,
            "overall_maturity_level": "Developing governance",
            "overall_coverage_level": "Partial coverage",
            "domain_maturity_scores": {},
        },
        "report_quality": {
            "sections_present": 8,
            "sections_total": 10,
            "quality_percentage": 80.0,
        },
    }


# ---------------------------------------------------------------------------
# create_safe_pdf_filename
# ---------------------------------------------------------------------------

class TestCreateSafePdfFilename:
    def test_returns_string(self):
        assert isinstance(create_safe_pdf_filename("Test Report"), str)

    def test_ends_with_pdf(self):
        assert create_safe_pdf_filename("Test Report").endswith(".pdf")

    def test_lowercased(self):
        result = create_safe_pdf_filename("BrightPath Report")
        assert result == result.lower()

    def test_spaces_replaced_with_dashes(self):
        result = create_safe_pdf_filename("Test Report")
        assert " " not in result

    def test_special_characters_removed(self):
        result = create_safe_pdf_filename("Report/Name & Co.")
        assert "/" not in result
        assert "&" not in result

    def test_empty_string_produces_pdf(self):
        result = create_safe_pdf_filename("")
        assert result.endswith(".pdf")

    def test_unicode_safe(self):
        result = create_safe_pdf_filename("Org — Report")
        assert isinstance(result, str)
        assert result.endswith(".pdf")


# ---------------------------------------------------------------------------
# format_pdf_text
# ---------------------------------------------------------------------------

class TestFormatPdfText:
    def test_strips_bold(self):
        result = format_pdf_text("**Bold Text**")
        assert "**" not in result
        assert "Bold Text" in result

    def test_strips_italic(self):
        result = format_pdf_text("*Italic Text*")
        assert "*" not in result

    def test_strips_code(self):
        result = format_pdf_text("`code`")
        assert "`" not in result
        assert "code" in result

    def test_strips_heading_markers(self):
        result = format_pdf_text("## Section Heading")
        assert "#" not in result

    def test_strips_blockquote_marker(self):
        result = format_pdf_text("> This is a note")
        assert ">" not in result

    def test_strips_bullet_marker(self):
        result = format_pdf_text("- List item")
        assert result[0] != "-"

    def test_returns_stripped_string(self):
        result = format_pdf_text("  some text  ")
        assert result == result.strip()

    def test_plain_text_unchanged(self):
        result = format_pdf_text("Plain text here")
        assert result == "Plain text here"


# ---------------------------------------------------------------------------
# build_pdf_styles
# ---------------------------------------------------------------------------

class TestBuildPdfStyles:
    def test_returns_dict(self):
        result = build_pdf_styles()
        assert isinstance(result, dict)

    def test_expected_style_keys(self):
        result = build_pdf_styles()
        for key in ["cover_title", "h1", "h2", "h3", "body", "bullet", "note",
                    "responsible_use", "caption"]:
            assert key in result, f"Missing style key: {key}"

    def test_style_values_not_none(self):
        result = build_pdf_styles()
        for key, value in result.items():
            assert value is not None, f"Style '{key}' is None"


# ---------------------------------------------------------------------------
# export_governance_report_to_pdf_bytes
# ---------------------------------------------------------------------------

class TestExportGovernanceReportToPdfBytes:
    def test_returns_bytes(self, minimal_export_data):
        result = export_governance_report_to_pdf_bytes(minimal_export_data)
        assert isinstance(result, bytes)

    def test_pdf_bytes_non_empty(self, minimal_export_data):
        result = export_governance_report_to_pdf_bytes(minimal_export_data)
        assert len(result) > 0

    def test_pdf_bytes_starts_with_pdf_header(self, minimal_export_data):
        result = export_governance_report_to_pdf_bytes(minimal_export_data)
        assert result[:4] == b"%PDF"

    def test_full_data_returns_bytes(self, full_export_data):
        result = export_governance_report_to_pdf_bytes(full_export_data)
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_handles_missing_analytics(self, minimal_export_data):
        result = export_governance_report_to_pdf_bytes(minimal_export_data, analytics=None)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_handles_missing_chart_paths(self, minimal_export_data):
        result = export_governance_report_to_pdf_bytes(minimal_export_data, chart_paths=None)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_handles_minimal_export_data(self):
        result = export_governance_report_to_pdf_bytes({})
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_with_analytics_returns_larger_pdf(self, full_export_data, sample_analytics):
        without = export_governance_report_to_pdf_bytes(full_export_data)
        with_analytics = export_governance_report_to_pdf_bytes(
            full_export_data, analytics=sample_analytics
        )
        assert len(with_analytics) >= len(without)

    def test_with_nonexistent_chart_paths_does_not_crash(self, minimal_export_data):
        result = export_governance_report_to_pdf_bytes(
            minimal_export_data,
            chart_paths={"coverage_levels": "/nonexistent/path/chart.png"},
        )
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_empty_markdown_still_produces_pdf(self):
        data = {
            "organisation_name": "Test Org",
            "generated_date": "2026-06-17",
            "governance_report_markdown": "",
        }
        result = export_governance_report_to_pdf_bytes(data)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_markdown_with_tables_produces_pdf(self, full_export_data):
        result = export_governance_report_to_pdf_bytes(full_export_data)
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_returns_bytes_with_all_sections(self, full_export_data, sample_analytics):
        result = export_governance_report_to_pdf_bytes(
            full_export_data, analytics=sample_analytics, chart_paths={}
        )
        assert isinstance(result, bytes)
        assert len(result) > 500
