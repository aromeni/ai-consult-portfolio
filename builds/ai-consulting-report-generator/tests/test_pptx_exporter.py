"""Tests for src/pptx_exporter.py — Build 5 Phase 8."""

from src.sample_data import get_brightpath_audit_data
from src import pptx_exporter as pe

_AUDIT = get_brightpath_audit_data()

_MINIMAL_EXPORT = {
    "organisation_name": "BrightPath Skills Training",
    "generated_date": "2026-06-16",
    "audit_data": _AUDIT,
    "client_report_markdown": "# Report\n\n## Executive Summary\n\nBrightPath.\n",
    "source_outputs_available": {"audit_data": True},
    "prototype_note": "Deterministic prototype.",
}

_FULL_EXPORT = {
    "organisation_name": "BrightPath Skills Training",
    "generated_date": "2026-06-16",
    "audit_data": _AUDIT,
    "readiness_summary": {
        "overall_score": 42,
        "overall_level": "Developing readiness",
        "overall_description": "Some foundations are in place.",
        "ranked_categories": [
            {"label": "Workflow opportunity", "score": 68, "level": "Moderate readiness"},
            {"label": "Risk management", "score": 25, "level": "Low readiness"},
        ],
        "strategic_interpretation": "BrightPath shows developing AI readiness.",
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
        "recommended_pilot_sequence": [
            {
                "position": 1,
                "pilot_name": "AI-Assisted Lesson Plan Drafts",
                "pilot_priority": "Medium",
                "complexity": "Low",
                "risk_level": "Low",
                "suggested_timeline": "Month 1–2",
            }
        ],
        "opportunities": [],
        "pilots": [{"pilot_id": "PILOT-001", "pilot_name": "Lesson Plans"}],
    },
    "risk_register_summary": {
        "total_risks": 5,
        "critical_risks": 0,
        "high_risks": 4,
        "medium_risks": 1,
        "low_risks": 0,
        "overall_risk_position": "Address risks before scaling.",
        "recommended_focus": ["Resolve 4 high risks."],
    },
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
    "report_sections": {
        "sections": {
            "key_findings": {
                "key_points": ["4 high risks identified.", "Controlled pilots recommended."],
                "recommendations": ["Strengthen governance."],
            },
            "governance_recommendations": {
                "recommendations": ["Define AI Use Policy.", "Clarify data boundaries."],
            },
            "immediate_next_steps": {
                "key_points": ["Confirm governance owner.", "Run controlled pilot."],
            },
        }
    },
    "client_report_markdown": "# Report\n\n## Executive Summary\n\nBrightPath.\n",
    "source_outputs_available": {
        "audit_data": True,
        "readiness_summary": True,
        "risk_register": True,
    },
    "prototype_note": "Deterministic prototype.",
}

_ANALYTICS = {
    "readiness_score_breakdown": {
        "Strategy": 32,
        "Data Governance": 28,
        "Workflow Opportunity": 68,
        "Overall": 42,
    },
    "risk_level_counts": {"Critical": 0, "High": 4, "Medium": 1, "Low": 0},
    "opportunity_priority_counts": {"Strategic": 0, "High": 0, "Medium": 4, "Low": 0},
    "roadmap_action_counts": {"First 30 Days": 10, "Days 31–60": 7, "Days 61–90": 7},
}


class TestCreateSafePptxFilename:
    def test_returns_string(self):
        assert isinstance(pe.create_safe_pptx_filename("test"), str)

    def test_ends_with_pptx(self):
        assert pe.create_safe_pptx_filename("BrightPath").endswith(".pptx")

    def test_no_spaces(self):
        result = pe.create_safe_pptx_filename("BrightPath Skills Training")
        assert " " not in result

    def test_handles_empty(self):
        result = pe.create_safe_pptx_filename("")
        assert result.endswith(".pptx")


class TestFormatSlideText:
    def test_strips_markdown(self):
        result = pe.format_slide_text("## My Heading")
        assert "##" not in result
        assert "My Heading" in result

    def test_truncates_long_text(self):
        result = pe.format_slide_text("x" * 1000, max_chars=100)
        assert len(result) <= 105  # allow for ellipsis

    def test_handles_empty(self):
        result = pe.format_slide_text("")
        assert result == ""

    def test_handles_bold_markers(self):
        result = pe.format_slide_text("**bold** text")
        assert "**" not in result
        assert "bold" in result


class TestExtractSlideBullets:
    def test_returns_list(self):
        result = pe.extract_slide_bullets(["item 1", "item 2"])
        assert isinstance(result, list)

    def test_respects_max_items(self):
        result = pe.extract_slide_bullets(list(range(10)), max_items=6)
        assert len(result) <= 6

    def test_handles_string_input(self):
        result = pe.extract_slide_bullets("- item 1\n- item 2\n- item 3")
        assert isinstance(result, list)
        assert len(result) <= 6

    def test_handles_empty_list(self):
        result = pe.extract_slide_bullets([])
        assert result == []

    def test_handles_none(self):
        result = pe.extract_slide_bullets(None)
        assert result == []


class TestExportClientReportToPptxBytes:
    def test_returns_bytes(self):
        result = pe.export_client_report_to_pptx_bytes(_MINIMAL_EXPORT)
        assert isinstance(result, bytes)

    def test_non_empty_bytes(self):
        result = pe.export_client_report_to_pptx_bytes(_MINIMAL_EXPORT)
        assert len(result) > 1000

    def test_with_full_export_data(self):
        result = pe.export_client_report_to_pptx_bytes(_FULL_EXPORT)
        assert isinstance(result, bytes)
        assert len(result) > 1000

    def test_handles_missing_analytics(self):
        result = pe.export_client_report_to_pptx_bytes(_MINIMAL_EXPORT, analytics=None)
        assert isinstance(result, bytes)

    def test_handles_missing_chart_paths(self):
        result = pe.export_client_report_to_pptx_bytes(_MINIMAL_EXPORT, chart_paths=None)
        assert isinstance(result, bytes)

    def test_with_analytics(self):
        result = pe.export_client_report_to_pptx_bytes(
            _FULL_EXPORT, analytics=_ANALYTICS
        )
        assert isinstance(result, bytes)
        assert len(result) > 1000

    def test_handles_empty_export_data(self):
        result = pe.export_client_report_to_pptx_bytes({})
        assert isinstance(result, bytes)

    def test_handles_none_export_data(self):
        result = pe.export_client_report_to_pptx_bytes(None)
        assert isinstance(result, bytes)

    def test_pptx_starts_with_pk_header(self):
        result = pe.export_client_report_to_pptx_bytes(_MINIMAL_EXPORT)
        # PPTX is a ZIP file — starts with PK
        assert result[:2] == b"PK"
