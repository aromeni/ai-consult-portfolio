"""Tests for src/pdf_exporter.py — reusable professional PDF export."""

from src import pdf_exporter as pe


SAMPLE_MARKDOWN = """# Training Needs Assessment

**Organisation:** BrightPath Skills Training

## Topic Priorities

- Learner data protection — HIGH
- Safeguarding boundaries — HIGH
- Approved tools — MEDIUM

## Priority Table

| Topic | Priority | Risk |
|---|---|---|
| Learner data | HIGH | HIGH |
| Safeguarding | HIGH | HIGH |

> Human review is required before use.

1. Review all sections.
2. Confirm synthetic data only.

---

*Synthetic scenario prototype.*
"""


class TestCreateSafeFilename:
    def test_returns_string(self):
        assert isinstance(pe.create_safe_filename("Report"), str)

    def test_lowercase_kebab_case(self):
        assert pe.create_safe_filename("Training Needs Assessment") == "training-needs-assessment.pdf"

    def test_default_extension_is_pdf(self):
        assert pe.create_safe_filename("report").endswith(".pdf")

    def test_custom_extension(self):
        assert pe.create_safe_filename("report", "md").endswith(".md")

    def test_extension_with_dot(self):
        assert pe.create_safe_filename("report", ".pdf") == "report.pdf"

    def test_strips_special_characters(self):
        result = pe.create_safe_filename("Report: AI & Staff (2026)!")
        assert result == "report-ai-staff-2026.pdf"

    def test_non_string_title(self):
        assert pe.create_safe_filename(None) == "report.pdf"

    def test_empty_title(self):
        assert pe.create_safe_filename("") == "report.pdf"

    def test_long_title_truncated(self):
        result = pe.create_safe_filename("x" * 200)
        assert len(result) <= 64


class TestNormaliseReportText:
    def test_returns_string(self):
        assert isinstance(pe.normalise_report_text("text"), str)

    def test_strips_bold(self):
        assert pe.normalise_report_text("**bold** text") == "bold text"

    def test_strips_italic(self):
        assert pe.normalise_report_text("*italic* text") == "italic text"

    def test_strips_headings(self):
        assert pe.normalise_report_text("## Heading") == "Heading"

    def test_strips_code(self):
        assert pe.normalise_report_text("`code` here") == "code here"

    def test_none_returns_empty_string(self):
        assert pe.normalise_report_text(None) == ""

    def test_non_string_returns_empty_string(self):
        assert pe.normalise_report_text(123) == ""


class TestBuildPdfStyles:
    def test_returns_dict(self):
        assert isinstance(pe.build_pdf_styles(), dict)

    def test_has_expected_style_keys(self):
        styles = pe.build_pdf_styles()
        for key in ["title", "h1", "h2", "h3", "body", "bullet", "small", "notice"]:
            assert key in styles


class TestExportMarkdownReportToPdfBytes:
    def test_returns_bytes(self):
        result = pe.export_markdown_report_to_pdf_bytes(SAMPLE_MARKDOWN, "Test Report")
        assert isinstance(result, bytes)

    def test_pdf_bytes_non_empty(self):
        result = pe.export_markdown_report_to_pdf_bytes(SAMPLE_MARKDOWN, "Test Report")
        assert len(result) > 1000

    def test_pdf_magic_bytes(self):
        result = pe.export_markdown_report_to_pdf_bytes(SAMPLE_MARKDOWN, "Test Report")
        assert result.startswith(b"%PDF")

    def test_with_organisation_and_subtitle(self):
        result = pe.export_markdown_report_to_pdf_bytes(
            SAMPLE_MARKDOWN, "Test Report",
            organisation_name="BrightPath", subtitle="Synthetic prototype",
        )
        assert result.startswith(b"%PDF")

    def test_without_cover_page(self):
        result = pe.export_markdown_report_to_pdf_bytes(
            SAMPLE_MARKDOWN, "Test Report", include_cover_page=False
        )
        assert result.startswith(b"%PDF")

    def test_empty_markdown(self):
        result = pe.export_markdown_report_to_pdf_bytes("", "Empty Report")
        assert result.startswith(b"%PDF")

    def test_none_markdown_does_not_crash(self):
        result = pe.export_markdown_report_to_pdf_bytes(None, "None Report")
        assert result.startswith(b"%PDF")

    def test_markdown_with_special_characters(self):
        md = "# Heading & <Tags>\n\nBody with & ampersand < less > greater."
        result = pe.export_markdown_report_to_pdf_bytes(md, "Special & Chars")
        assert result.startswith(b"%PDF")

    def test_markdown_table_renders(self):
        md = "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
        result = pe.export_markdown_report_to_pdf_bytes(md, "Table Report")
        assert result.startswith(b"%PDF")


class TestExportStructuredReportToPdfBytes:
    def test_minimal_report_data(self):
        result = pe.export_structured_report_to_pdf_bytes(
            {"organisation_name": "BrightPath"}, "needs_assessment"
        )
        assert result.startswith(b"%PDF")

    def test_empty_report_data(self):
        result = pe.export_structured_report_to_pdf_bytes({}, "workshop_plan")
        assert result.startswith(b"%PDF")

    def test_none_report_data_does_not_crash(self):
        result = pe.export_structured_report_to_pdf_bytes(None, "activities")
        assert result.startswith(b"%PDF")

    def test_unknown_report_type(self):
        result = pe.export_structured_report_to_pdf_bytes({}, "mystery_report")
        assert result.startswith(b"%PDF")

    def test_prefers_markdown_when_supplied(self):
        result = pe.export_structured_report_to_pdf_bytes(
            {"organisation_name": "BrightPath"},
            "staff_handout",
            markdown_text=SAMPLE_MARKDOWN,
        )
        assert result.startswith(b"%PDF")

    def test_mixed_value_types_do_not_crash(self):
        report_data = {
            "organisation_name": "BrightPath",
            "count": 5,
            "items": ["one", "two"],
            "nested": {"key": "value", "deep": ["x"]},
            "records": [{"a": 1}, {"b": 2}],
            "empty_list": [],
            "empty_string": "",
            "none_value": None,
        }
        result = pe.export_structured_report_to_pdf_bytes(report_data, "knowledge_check")
        assert result.startswith(b"%PDF")

    def test_all_known_report_types(self):
        for report_type in pe.REPORT_TITLES:
            result = pe.export_structured_report_to_pdf_bytes(
                {"organisation_name": "BrightPath"}, report_type
            )
            assert result.startswith(b"%PDF")
