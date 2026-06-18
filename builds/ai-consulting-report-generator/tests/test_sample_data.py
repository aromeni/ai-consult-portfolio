"""Tests for src/sample_data.py."""

import pytest
from src import sample_data as sd


class TestGetBrightpathAuditData:
    def test_returns_dict(self):
        result = sd.get_brightpath_audit_data()
        assert isinstance(result, dict)

    def test_has_organisation_profile(self):
        result = sd.get_brightpath_audit_data()
        assert "organisation_profile" in result
        assert isinstance(result["organisation_profile"], dict)

    def test_has_readiness_scores(self):
        result = sd.get_brightpath_audit_data()
        assert "readiness_scores" in result
        assert isinstance(result["readiness_scores"], dict)

    def test_workflow_findings_non_empty(self):
        result = sd.get_brightpath_audit_data()
        assert "workflow_findings" in result
        assert len(result["workflow_findings"]) > 0

    def test_risk_findings_non_empty(self):
        result = sd.get_brightpath_audit_data()
        assert "risk_findings" in result
        assert len(result["risk_findings"]) > 0

    def test_pilot_recommendations_non_empty(self):
        result = sd.get_brightpath_audit_data()
        assert "pilot_recommendations" in result
        assert len(result["pilot_recommendations"]) > 0

    def test_training_needs_non_empty(self):
        result = sd.get_brightpath_audit_data()
        assert "training_needs" in result
        assert len(result["training_needs"]) > 0

    def test_governance_gaps_non_empty(self):
        result = sd.get_brightpath_audit_data()
        assert "governance_gaps" in result
        assert len(result["governance_gaps"]) > 0

    def test_organisation_name(self):
        result = sd.get_brightpath_audit_data()
        assert result["organisation_profile"]["organisation_name"] == "BrightPath Skills Training"

    def test_overall_readiness_score_valid_range(self):
        result = sd.get_brightpath_audit_data()
        score = result["readiness_scores"].get("overall_readiness_score")
        assert score is not None
        assert 0 <= score <= 100


class TestGetDefaultReadinessCategories:
    def test_returns_list(self):
        result = sd.get_default_readiness_categories()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(sd.get_default_readiness_categories()) > 0

    def test_contains_strategy(self):
        assert "Strategy" in sd.get_default_readiness_categories()

    def test_contains_data_governance(self):
        assert "Data Governance" in sd.get_default_readiness_categories()


class TestGetDefaultReportSections:
    def test_returns_list(self):
        result = sd.get_default_report_sections()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(sd.get_default_report_sections()) > 0

    def test_contains_executive_summary(self):
        assert "Executive Summary" in sd.get_default_report_sections()

    def test_contains_risk_register(self):
        assert "Risk Register" in sd.get_default_report_sections()


class TestDemoDataHelpers:
    def test_workflow_findings_have_required_keys(self):
        result = sd.get_demo_workflow_findings()
        assert len(result) > 0
        assert "workflow_name" in result[0]
        assert "ai_opportunity" in result[0]
        assert "risk_level" in result[0]

    def test_risk_findings_have_required_keys(self):
        result = sd.get_demo_risk_findings()
        assert len(result) > 0
        assert "risk_title" in result[0]
        assert "risk_level" in result[0]
        assert "risk_category" in result[0]

    def test_pilot_recommendations_have_required_keys(self):
        result = sd.get_demo_pilot_recommendations()
        assert len(result) > 0
        assert "pilot_name" in result[0]
        assert "suggested_timeline" in result[0]

    def test_training_needs_have_required_keys(self):
        result = sd.get_demo_training_needs()
        assert len(result) > 0
        assert "topic" in result[0]
        assert "audience" in result[0]
        assert "priority" in result[0]

    def test_governance_gaps_have_required_keys(self):
        result = sd.get_demo_governance_gaps()
        assert len(result) > 0
        assert "gap_title" in result[0]
        assert "priority" in result[0]

    def test_risk_findings_include_critical(self):
        result = sd.get_demo_risk_findings()
        levels = [r.get("risk_level", "") for r in result]
        assert "Critical" in levels

    def test_governance_gaps_include_critical(self):
        result = sd.get_demo_governance_gaps()
        priorities = [g.get("priority", "") for g in result]
        assert "Critical" in priorities
