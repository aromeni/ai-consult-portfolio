"""Tests for src/report_analytics.py — Build 5 Phase 8."""

from src.sample_data import get_brightpath_audit_data
from src import report_analytics as ra

_AUDIT = get_brightpath_audit_data()

_RR_SUMMARY = {
    "total_risks": 5,
    "critical_risks": 0,
    "high_risks": 4,
    "medium_risks": 1,
    "low_risks": 0,
    "overall_risk_position": "Address risks before scaling.",
    "recommended_focus": [],
    "highest_risk": {},
}

_RISK_REGISTER = [
    {"risk_id": "RISK-001", "risk_title": "Data Risk", "risk_level": "High", "risk_score": 16},
    {"risk_id": "RISK-002", "risk_title": "Policy Risk", "risk_level": "High", "risk_score": 12},
    {"risk_id": "RISK-003", "risk_title": "Training Risk", "risk_level": "Medium", "risk_score": 9},
]

_OPP_SUMMARY = {
    "total_opportunities": 4,
    "total_pilots": 3,
    "strategic_priority_opportunities": 0,
    "high_priority_opportunities": 0,
    "medium_priority_opportunities": 4,
    "low_priority_opportunities": 0,
    "recommended_first_pilot_name": "AI-Assisted Lesson Plan Drafts",
    "overall_opportunity_position": "Start with narrow pilots.",
    "recommended_focus": [],
}

_RM_SUMMARY = {
    "total_actions": 24,
    "day_30_actions": 10,
    "day_60_actions": 7,
    "day_90_actions": 7,
    "high_priority_actions": 15,
    "recommended_first_pilot": "AI-Assisted Lesson Plan Drafts",
    "key_dependencies": [],
    "key_risks_to_manage": [],
    "overall_roadmap_position": "Governance before scaling.",
}

_FULL_EXPORT = {
    "audit_data": _AUDIT,
    "risk_register_summary": _RR_SUMMARY,
    "risk_register": _RISK_REGISTER,
    "opportunity_summary": _OPP_SUMMARY,
    "implementation_roadmap_summary": _RM_SUMMARY,
    "client_report_markdown": (
        "# AI Readiness Report\n"
        "## Executive Summary\nBrightPath.\n"
        "## Responsible-Use Boundaries\nSynthetic data.\n"
        "## Prototype Limitations\n- Human review required."
    ),
    "source_outputs_available": {
        "audit_data": True,
        "readiness_summary": True,
        "risk_register": True,
        "opportunity_portfolio": True,
        "implementation_roadmap": True,
        "report_sections": True,
    },
}


class TestCalculateExportCompletionStatus:
    def test_returns_dict(self):
        result = ra.calculate_export_completion_status(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_handles_empty_data(self):
        result = ra.calculate_export_completion_status({})
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_detects_audit_data(self):
        result = ra.calculate_export_completion_status(_FULL_EXPORT)
        assert result["Audit Data"] is True

    def test_detects_missing_outputs(self):
        result = ra.calculate_export_completion_status({"audit_data": _AUDIT})
        assert result.get("Readiness Summary") is False

    def test_handles_none(self):
        result = ra.calculate_export_completion_status(None)
        assert isinstance(result, dict)

    def test_client_report_detected(self):
        result = ra.calculate_export_completion_status(_FULL_EXPORT)
        assert result["Client Report"] is True


class TestCalculateReadinessScoreBreakdown:
    def test_returns_dict(self):
        result = ra.calculate_readiness_score_breakdown(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_includes_overall(self):
        result = ra.calculate_readiness_score_breakdown(_FULL_EXPORT)
        assert "Overall" in result

    def test_scores_are_integers(self):
        result = ra.calculate_readiness_score_breakdown(_FULL_EXPORT)
        for v in result.values():
            assert isinstance(v, int)

    def test_handles_empty(self):
        result = ra.calculate_readiness_score_breakdown({})
        assert isinstance(result, dict)

    def test_includes_categories(self):
        result = ra.calculate_readiness_score_breakdown(_FULL_EXPORT)
        assert "Strategy" in result or "Workflow Opportunity" in result


class TestCalculateRiskLevelCounts:
    def test_returns_dict(self):
        result = ra.calculate_risk_level_counts(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_uses_summary_when_available(self):
        result = ra.calculate_risk_level_counts(_FULL_EXPORT)
        assert result["High"] == 4
        assert result["Critical"] == 0

    def test_fallback_from_register_list(self):
        data = {"risk_register": _RISK_REGISTER}
        result = ra.calculate_risk_level_counts(data)
        assert result["High"] == 2
        assert result["Medium"] == 1

    def test_handles_empty(self):
        result = ra.calculate_risk_level_counts({})
        assert isinstance(result, dict)
        assert "High" in result


class TestCalculateOpportunityPriorityCounts:
    def test_returns_dict(self):
        result = ra.calculate_opportunity_priority_counts(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_uses_summary_when_available(self):
        result = ra.calculate_opportunity_priority_counts(_FULL_EXPORT)
        assert result["Medium"] == 4
        assert result["Strategic"] == 0

    def test_handles_empty(self):
        result = ra.calculate_opportunity_priority_counts({})
        assert isinstance(result, dict)

    def test_all_levels_present(self):
        result = ra.calculate_opportunity_priority_counts(_FULL_EXPORT)
        assert "Strategic" in result
        assert "High" in result
        assert "Medium" in result
        assert "Low" in result


class TestCalculateRoadmapActionCounts:
    def test_returns_dict(self):
        result = ra.calculate_roadmap_action_counts(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_uses_summary_when_available(self):
        result = ra.calculate_roadmap_action_counts(_FULL_EXPORT)
        assert result["First 30 Days"] == 10
        assert result["Days 31–60"] == 7

    def test_handles_empty(self):
        result = ra.calculate_roadmap_action_counts({})
        assert isinstance(result, dict)

    def test_three_phases(self):
        result = ra.calculate_roadmap_action_counts(_FULL_EXPORT)
        assert len(result) == 3


class TestCalculateReportQualitySummary:
    def test_returns_dict(self):
        result = ra.calculate_report_quality_summary(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = ra.calculate_report_quality_summary(_FULL_EXPORT)
        assert "executive_summary_included" in result
        assert "responsible_use_included" in result
        assert "prototype_limitations_included" in result
        assert "human_review_note_included" in result

    def test_detects_executive_summary(self):
        result = ra.calculate_report_quality_summary(_FULL_EXPORT)
        assert result["executive_summary_included"] is True

    def test_detects_responsible_use(self):
        result = ra.calculate_report_quality_summary(_FULL_EXPORT)
        assert result["responsible_use_included"] is True

    def test_handles_empty(self):
        result = ra.calculate_report_quality_summary({})
        assert isinstance(result, dict)
        assert result["executive_summary_included"] is False


class TestBuildClientReportAnalytics:
    def test_returns_dict(self):
        result = ra.build_client_report_analytics(_FULL_EXPORT)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = ra.build_client_report_analytics(_FULL_EXPORT)
        assert "completion_status" in result
        assert "readiness_score_breakdown" in result
        assert "risk_level_counts" in result
        assert "opportunity_priority_counts" in result
        assert "roadmap_action_counts" in result
        assert "report_quality_summary" in result

    def test_handles_empty(self):
        result = ra.build_client_report_analytics({})
        assert isinstance(result, dict)

    def test_all_values_are_dicts(self):
        result = ra.build_client_report_analytics(_FULL_EXPORT)
        for v in result.values():
            assert isinstance(v, dict)
