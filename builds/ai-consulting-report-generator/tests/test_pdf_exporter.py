"""Tests for src/pdf_exporter.py — Build 5 Phase 8."""

from src.sample_data import get_brightpath_audit_data
from src import pdf_exporter as pe

_AUDIT = get_brightpath_audit_data()

_MINIMAL_EXPORT = {
    "organisation_name": "BrightPath Skills Training",
    "generated_date": "2026-06-16",
    "audit_data": _AUDIT,
    "client_report_markdown": (
        "# AI Readiness and Responsible AI Adoption Report\n\n"
        "## 1. Executive Summary\n\nBrightPath is exploring AI adoption.\n\n"
        "## 11. Responsible-Use Boundaries\n\nSynthetic data only.\n\n"
        "## 12. Prototype Limitations\n\n- Human review required.\n"
    ),
    "source_outputs_available": {
        "audit_data": True,
        "readiness_summary": False,
        "risk_register": False,
        "opportunity_portfolio": False,
        "implementation_roadmap": False,
        "report_sections": False,
    },
    "responsible_use_note": "Synthetic data only.",
    "prototype_note": "Deterministic prototype.",
}

_FULL_EXPORT = {
    "organisation_name": "BrightPath Skills Training",
    "generated_date": "2026-06-16",
    "audit_data": _AUDIT,
    "readiness_summary": {
        "overall_score": 42,
        "overall_level": "Developing readiness",
        "ranked_categories": [],
    },
    "risk_register_summary": {
        "total_risks": 5,
        "critical_risks": 0,
        "high_risks": 4,
        "medium_risks": 1,
        "low_risks": 0,
        "overall_risk_position": "Address risks before scaling.",
        "recommended_focus": [],
    },
    "client_report_markdown": (
        "# AI Readiness and Responsible AI Adoption Report\n\n"
        "## Cover Page\n\nOrganisation: BrightPath\n\n"
        "## 1. Executive Summary\n\nBrightPath is beginning to explore AI adoption.\n\n"
        "## 2. Organisation Context\n\nPrivate training provider.\n\n"
        "## 11. Responsible-Use Boundaries\n\nSynthetic data only. Human review required.\n\n"
        "## 12. Prototype Limitations\n\n- Not production deployed.\n"
    ),
    "source_outputs_available": {
        "audit_data": True,
        "readiness_summary": True,
        "risk_register": True,
        "opportunity_portfolio": False,
        "implementation_roadmap": False,
        "report_sections": False,
    },
    "responsible_use_note": "Synthetic data only.",
    "prototype_note": "Deterministic prototype.",
}

_ANALYTICS = {
    "completion_status": {"Audit Data": True, "Risk Register": True},
    "readiness_score_breakdown": {"Strategy": 32, "Overall": 42},
    "risk_level_counts": {"Critical": 0, "High": 4, "Medium": 1, "Low": 0},
    "opportunity_priority_counts": {"Medium": 4, "High": 0},
    "roadmap_action_counts": {"First 30 Days": 10, "Days 31–60": 7, "Days 61–90": 7},
    "report_quality_summary": {
        "executive_summary_included": True,
        "responsible_use_included": True,
        "prototype_limitations_included": True,
        "human_review_note_included": True,
    },
}


class TestCreateSafePdfFilename:
    def test_returns_string(self):
        assert isinstance(pe.create_safe_pdf_filename("test"), str)

    def test_ends_with_pdf(self):
        assert pe.create_safe_pdf_filename("BrightPath").endswith(".pdf")

    def test_no_spaces(self):
        result = pe.create_safe_pdf_filename("BrightPath Skills Training")
        assert " " not in result

    def test_handles_empty(self):
        result = pe.create_safe_pdf_filename("")
        assert result.endswith(".pdf")

    def test_handles_special_chars(self):
        result = pe.create_safe_pdf_filename("Test & Co: Ltd.")
        assert " " not in result
        assert result.endswith(".pdf")


class TestFormatPdfText:
    def test_strips_heading_markers(self):
        result = pe.format_pdf_text("## My Heading")
        assert "##" not in result
        assert "My Heading" in result

    def test_converts_bold(self):
        result = pe.format_pdf_text("**bold text**")
        assert "<b>bold text</b>" in result

    def test_handles_empty(self):
        assert pe.format_pdf_text("") == ""

    def test_handles_none_like(self):
        assert pe.format_pdf_text(None) == ""


class TestBuildPdfStyles:
    def test_returns_dict(self):
        styles = pe.build_pdf_styles()
        assert isinstance(styles, dict)

    def test_has_required_keys(self):
        styles = pe.build_pdf_styles()
        assert "H1" in styles
        assert "H2" in styles
        assert "Body" in styles
        assert "Bullet" in styles

    def test_has_cover_style(self):
        styles = pe.build_pdf_styles()
        assert "CoverTitle" in styles


class TestExportClientReportToPdfBytes:
    def test_returns_bytes(self):
        result = pe.export_client_report_to_pdf_bytes(_MINIMAL_EXPORT)
        assert isinstance(result, bytes)

    def test_non_empty_bytes(self):
        result = pe.export_client_report_to_pdf_bytes(_MINIMAL_EXPORT)
        assert len(result) > 100

    def test_with_full_export_data(self):
        result = pe.export_client_report_to_pdf_bytes(_FULL_EXPORT)
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_handles_missing_analytics(self):
        result = pe.export_client_report_to_pdf_bytes(_MINIMAL_EXPORT, analytics=None)
        assert isinstance(result, bytes)

    def test_handles_missing_chart_paths(self):
        result = pe.export_client_report_to_pdf_bytes(_MINIMAL_EXPORT, chart_paths=None)
        assert isinstance(result, bytes)

    def test_with_analytics(self):
        result = pe.export_client_report_to_pdf_bytes(_FULL_EXPORT, analytics=_ANALYTICS)
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_handles_empty_export_data(self):
        result = pe.export_client_report_to_pdf_bytes({})
        assert isinstance(result, bytes)

    def test_handles_none_export_data(self):
        result = pe.export_client_report_to_pdf_bytes(None)
        assert isinstance(result, bytes)

    def test_pdf_starts_with_pdf_header(self):
        result = pe.export_client_report_to_pdf_bytes(_MINIMAL_EXPORT)
        assert result[:4] == b"%PDF"


class TestCreatePdfPlaceholder:
    def test_returns_bytes(self):
        result = pe.create_pdf_placeholder("Test Title", "Test body.")
        assert isinstance(result, bytes)

    def test_non_empty(self):
        result = pe.create_pdf_placeholder("Test Title", "Test body.")
        assert len(result) > 0
