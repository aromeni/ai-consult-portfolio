"""
Tests for report generation functions in src/report_generator.py.

Run from the project root (brightpath-ai-readiness-tool/):  pytest
"""

from src.report_generator import (
    generate_markdown_report,
    generate_pdf_report_bytes,
    create_report_filename,
)


# ── Minimal synthetic sample data ────────────────────────────────────────────

SAMPLE_DATA = {
    "org_name": "Test Training Ltd",
    "org_type": "Small training provider",
    "staff_count": "10",
    "ai_use_summary": "Staff use ChatGPT informally.",
    "main_concerns": "Data privacy and output accuracy.",
    "readiness_score": 62,
    "readiness_category": "Pilot ready with safeguards",
    "workflow_name": "Generic lesson planning support",
    "workflow_owner": "Tutor team",
    "ai_support_idea": "Generate first-draft lesson plans.",
    "workflow_score": 40,
    "workflow_category": "Good pilot candidate",
    "highest_risk": "Moderate",
    "has_critical": False,
    "has_high": False,
    "key_risk_notes": "Review all outputs before use.",
    "safeguards_text": "- Use anonymised data.\n- Human review required.",
    "next_actions_text": "1. Train staff.\n2. Run pilot.",
    "recommendation": "Low-risk pilot candidate",
    "recommendation_explanation": "Good foundations for a scoped pilot.",
    "consultant_notes": "Start with lesson planning only.",
}


# ── generate_markdown_report — return type ────────────────────────────────────

def test_report_returns_string():
    assert isinstance(generate_markdown_report(SAMPLE_DATA), str)


def test_report_is_not_empty():
    assert len(generate_markdown_report(SAMPLE_DATA)) > 0


# ── generate_markdown_report — section headings ───────────────────────────────

def test_report_includes_title():
    assert "AI Readiness and Workflow Audit Mini Report" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_organisation_profile():
    assert "Organisation Profile" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_ai_readiness_summary():
    assert "AI Readiness Summary" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_workflow_audit_summary():
    assert "Workflow Audit Summary" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_risk_assessment_summary():
    assert "Risk Assessment Summary" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_pilot_recommendation():
    assert "Pilot Recommendation" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_responsible_use():
    assert "Responsible Use and Limitations" in generate_markdown_report(SAMPLE_DATA)


# ── generate_markdown_report — data values ────────────────────────────────────

def test_report_includes_org_name():
    assert "Test Training Ltd" in generate_markdown_report(SAMPLE_DATA)


def test_report_includes_recommendation_value():
    assert "Low-risk pilot candidate" in generate_markdown_report(SAMPLE_DATA)


def test_report_handles_missing_optional_fields():
    # Minimal data — only required fields — should not raise an error
    minimal = {"org_name": "Minimal Org"}
    result = generate_markdown_report(minimal)
    assert isinstance(result, str)
    assert "Minimal Org" in result


# ── create_report_filename ────────────────────────────────────────────────────

def test_filename_is_lowercase():
    assert create_report_filename("BrightPath Skills Training") == \
        create_report_filename("BrightPath Skills Training").lower()


def test_filename_contains_no_spaces():
    assert " " not in create_report_filename("BrightPath Skills Training")


def test_filename_ends_with_md():
    assert create_report_filename("BrightPath Skills Training").endswith(".md")


def test_filename_contains_slug_from_org_name():
    assert "brightpath" in create_report_filename("BrightPath Skills Training")


def test_filename_empty_string_returns_default():
    assert create_report_filename("") == "ai-readiness-mini-report.md"


def test_filename_whitespace_only_returns_default():
    assert create_report_filename("   ") == "ai-readiness-mini-report.md"


def test_filename_special_characters_replaced_with_hyphens():
    filename = create_report_filename("ABC & DEF Ltd.")
    assert "&" not in filename
    assert filename.count(".") == 1  # only the dot in .md; the dot from "Ltd." is removed


def test_filename_no_leading_or_trailing_hyphens():
    filename = create_report_filename("  BrightPath  ")
    assert not filename.startswith("-")
    assert not filename[:-3].endswith("-")  # check before the .md suffix


# ── generate_pdf_report_bytes ─────────────────────────────────────────────────

def test_pdf_returns_bytes():
    assert isinstance(generate_pdf_report_bytes(SAMPLE_DATA), bytes)


def test_pdf_is_not_empty():
    assert len(generate_pdf_report_bytes(SAMPLE_DATA)) > 0


def test_pdf_starts_with_pdf_magic():
    assert generate_pdf_report_bytes(SAMPLE_DATA)[:4] == b"%PDF"


def test_pdf_handles_missing_optional_fields():
    minimal = {"org_name": "Minimal Org"}
    result = generate_pdf_report_bytes(minimal)
    assert isinstance(result, bytes)
    assert len(result) > 0
