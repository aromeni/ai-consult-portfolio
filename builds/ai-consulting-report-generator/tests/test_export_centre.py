"""Tests for src/export_centre.py — Build 5 Phase 8."""

from src.sample_data import get_brightpath_audit_data
from src import export_centre as ec

_AUDIT = get_brightpath_audit_data()

_EMPTY_STATE: dict = {}

_MINIMAL_STATE = {
    "audit_data": _AUDIT,
}

_FULL_STATE = {
    "audit_data": _AUDIT,
    "readiness_summary": {
        "overall_score": 42,
        "overall_level": "Developing readiness",
        "overall_description": "Some foundations are in place.",
        "ranked_categories": [],
        "strategic_interpretation": "BrightPath is developing AI readiness.",
        "recommendations": ["Improve governance.", "Build data controls."],
    },
    "opportunity_summary": {
        "total_opportunities": 4,
        "total_pilots": 3,
        "strategic_priority_opportunities": 0,
        "high_priority_opportunities": 0,
        "medium_priority_opportunities": 4,
        "low_priority_opportunities": 0,
        "recommended_first_pilot_name": "AI-Assisted Lesson Plan Drafts",
        "overall_opportunity_position": "Start with narrow pilots.",
        "recommended_focus": [],
    },
    "opportunity_portfolio": {
        "recommended_pilot_sequence": [],
        "opportunities": [],
        "pilots": [],
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
    "risk_register": [],
    "implementation_roadmap_summary": {
        "total_actions": 24,
        "day_30_actions": 10,
        "day_60_actions": 7,
        "day_90_actions": 7,
        "high_priority_actions": 15,
        "recommended_first_pilot": "AI-Assisted Lesson Plan Drafts",
        "key_dependencies": [],
        "key_risks_to_manage": [],
        "overall_roadmap_position": "Governance before scaling.",
    },
    "implementation_roadmap": {"day_30": [], "day_60": [], "day_90": []},
    "report_sections": {
        "sections": {
            "key_findings": {"key_points": ["4 high risks."], "recommendations": []},
        }
    },
    "client_report_markdown": (
        "# AI Readiness and Responsible AI Adoption Report\n\n"
        "## 1. Executive Summary\n\nBrightPath is exploring AI.\n\n"
        "## 11. Responsible-Use Boundaries\n\nSynthetic data only.\n\n"
        "## 12. Prototype Limitations\n\n- Human review required.\n"
    ),
    "client_report_data": {
        "organisation_name": "BrightPath Skills Training",
        "report_title": "AI Readiness and Responsible AI Adoption Report",
    },
}

_MINIMAL_EXPORT = {
    "organisation_name": "BrightPath Skills Training",
    "generated_date": "2026-06-16",
    "audit_data": _AUDIT,
    "client_report_markdown": (
        "# AI Readiness and Responsible AI Adoption Report\n\n"
        "## 1. Executive Summary\n\nBrightPath.\n"
    ),
    "source_outputs_available": {"audit_data": True},
    "prototype_note": "Deterministic prototype.",
    "responsible_use_note": "Synthetic data only.",
}


class TestGetExportFormats:
    def test_returns_list(self):
        result = ec.get_export_formats()
        assert isinstance(result, list)

    def test_includes_markdown(self):
        result = ec.get_export_formats()
        assert "Markdown" in result

    def test_includes_pdf(self):
        result = ec.get_export_formats()
        assert "PDF" in result

    def test_includes_pptx(self):
        result = ec.get_export_formats()
        assert any("PowerPoint" in f or "PPTX" in f for f in result)


class TestCheckExportReadiness:
    def test_returns_dict(self):
        result = ec.check_export_readiness(_EMPTY_STATE)
        assert isinstance(result, dict)

    def test_handles_empty_session_state(self):
        result = ec.check_export_readiness(_EMPTY_STATE)
        assert result["is_ready"] is False

    def test_detects_client_report_markdown(self):
        state = {**_FULL_STATE}
        result = ec.check_export_readiness(state)
        assert result["is_ready"] is True

    def test_has_required_keys(self):
        result = ec.check_export_readiness(_EMPTY_STATE)
        assert "is_ready" in result
        assert "available_outputs" in result
        assert "missing_outputs" in result
        assert "can_export_markdown" in result
        assert "can_export_pdf" in result
        assert "can_export_pptx" in result

    def test_missing_outputs_when_empty(self):
        result = ec.check_export_readiness(_EMPTY_STATE)
        assert len(result["missing_outputs"]) > 0

    def test_audit_only_not_fully_ready(self):
        result = ec.check_export_readiness(_MINIMAL_STATE)
        assert result["is_ready"] is False


class TestBuildExportDataFromSessionState:
    def test_returns_dict(self):
        result = ec.build_export_data_from_session_state(_FULL_STATE)
        assert isinstance(result, dict)

    def test_includes_organisation_name(self):
        result = ec.build_export_data_from_session_state(_FULL_STATE)
        assert "organisation_name" in result

    def test_includes_generated_date(self):
        result = ec.build_export_data_from_session_state(_FULL_STATE)
        assert "generated_date" in result

    def test_includes_audit_data(self):
        result = ec.build_export_data_from_session_state(_FULL_STATE)
        assert "audit_data" in result

    def test_includes_responsible_use_note(self):
        result = ec.build_export_data_from_session_state(_FULL_STATE)
        assert "responsible_use_note" in result

    def test_handles_empty_state(self):
        result = ec.build_export_data_from_session_state(_EMPTY_STATE)
        assert isinstance(result, dict)


class TestGenerateExportQualityChecklist:
    def test_returns_list(self):
        result = ec.generate_export_quality_checklist(_MINIMAL_EXPORT)
        assert isinstance(result, list)

    def test_each_item_has_item_and_passed(self):
        result = ec.generate_export_quality_checklist(_MINIMAL_EXPORT)
        for item in result:
            assert "item" in item
            assert "passed" in item

    def test_passed_is_bool(self):
        result = ec.generate_export_quality_checklist(_MINIMAL_EXPORT)
        for item in result:
            assert isinstance(item["passed"], bool)

    def test_handles_empty_export_data(self):
        result = ec.generate_export_quality_checklist({})
        assert isinstance(result, list)
        assert len(result) > 0

    def test_minimum_items_returned(self):
        result = ec.generate_export_quality_checklist(_MINIMAL_EXPORT)
        assert len(result) >= 5


class TestSummariseExportPackage:
    def test_returns_dict(self):
        result = ec.summarise_export_package(_MINIMAL_EXPORT)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = ec.summarise_export_package(_MINIMAL_EXPORT)
        assert "organisation_name" in result
        assert "export_formats" in result
        assert "human_review_required" in result

    def test_human_review_required_is_true(self):
        result = ec.summarise_export_package(_MINIMAL_EXPORT)
        assert result["human_review_required"] is True

    def test_handles_empty(self):
        result = ec.summarise_export_package({})
        assert isinstance(result, dict)


class TestCreateExportFilenameBase:
    def test_returns_string(self):
        result = ec.create_export_filename_base("BrightPath Skills Training")
        assert isinstance(result, str)

    def test_no_spaces(self):
        result = ec.create_export_filename_base("BrightPath Skills Training")
        assert " " not in result

    def test_handles_empty(self):
        result = ec.create_export_filename_base("")
        assert isinstance(result, str)

    def test_handles_special_chars(self):
        result = ec.create_export_filename_base("Test & Co: Ltd.")
        assert " " not in result


class TestPrepareMarkdownExport:
    def test_returns_tuple(self):
        result = ec.prepare_markdown_export(_MINIMAL_EXPORT)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_string(self):
        text, filename = ec.prepare_markdown_export(_MINIMAL_EXPORT)
        assert isinstance(text, str)

    def test_second_element_is_filename(self):
        text, filename = ec.prepare_markdown_export(_MINIMAL_EXPORT)
        assert isinstance(filename, str)
        assert filename.endswith(".md")

    def test_markdown_contains_content(self):
        text, filename = ec.prepare_markdown_export(_MINIMAL_EXPORT)
        assert len(text) > 10

    def test_handles_empty_export_data(self):
        result = ec.prepare_markdown_export({})
        assert isinstance(result, tuple)


class TestPrepareAllExports:
    def test_returns_dict(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert isinstance(result, dict)

    def test_has_markdown_key(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert "markdown" in result

    def test_has_pdf_bytes_key(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert "pdf_bytes" in result

    def test_has_pptx_bytes_key(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert "pptx_bytes" in result

    def test_markdown_is_string(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert isinstance(result["markdown"], str)

    def test_pdf_bytes_is_bytes(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert isinstance(result["pdf_bytes"], bytes)

    def test_pptx_bytes_is_bytes(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT)
        assert isinstance(result["pptx_bytes"], bytes)

    def test_handles_minimal_data_safely(self):
        result = ec.prepare_all_exports({})
        assert isinstance(result, dict)

    def test_handles_none_analytics(self):
        result = ec.prepare_all_exports(_MINIMAL_EXPORT, analytics=None)
        assert isinstance(result, dict)
