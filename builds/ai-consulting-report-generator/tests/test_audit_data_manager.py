"""Tests for src/audit_data_manager.py."""

import pytest
from src import audit_data_manager as adm
from src.sample_data import get_brightpath_audit_data


def _valid():
    return get_brightpath_audit_data()


class TestValidateAuditData:
    def test_valid_data_passes(self):
        ok, msg = adm.validate_audit_data(_valid())
        assert ok is True

    def test_non_dict_fails(self):
        ok, msg = adm.validate_audit_data("not a dict")
        assert ok is False

    def test_missing_organisation_profile_fails(self):
        data = _valid()
        del data["organisation_profile"]
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_empty_organisation_name_fails(self):
        data = _valid()
        data["organisation_profile"]["organisation_name"] = ""
        ok, msg = adm.validate_audit_data(data)
        assert ok is False
        assert "organisation_name" in msg.lower()

    def test_none_organisation_name_fails(self):
        data = _valid()
        data["organisation_profile"]["organisation_name"] = None
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_negative_staff_count_fails(self):
        data = _valid()
        data["organisation_profile"]["staff_count"] = -5
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_zero_staff_count_fails(self):
        data = _valid()
        data["organisation_profile"]["staff_count"] = 0
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_missing_readiness_scores_fails(self):
        data = _valid()
        del data["readiness_scores"]
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_missing_overall_score_fails(self):
        data = _valid()
        del data["readiness_scores"]["overall_readiness_score"]
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_missing_workflow_findings_fails(self):
        data = _valid()
        del data["workflow_findings"]
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_missing_risk_findings_fails(self):
        data = _valid()
        del data["risk_findings"]
        ok, _ = adm.validate_audit_data(data)
        assert ok is False

    def test_missing_pilot_recommendations_fails(self):
        data = _valid()
        del data["pilot_recommendations"]
        ok, _ = adm.validate_audit_data(data)
        assert ok is False


class TestSummariseAuditData:
    def setup_method(self):
        self.summary = adm.summarise_audit_data(_valid())

    def test_returns_dict(self):
        assert isinstance(self.summary, dict)

    def test_has_organisation_name(self):
        assert "organisation_name" in self.summary
        assert self.summary["organisation_name"] == "BrightPath Skills Training"

    def test_has_staff_count(self):
        assert "staff_count" in self.summary
        assert self.summary["staff_count"] == 24

    def test_has_workflow_count(self):
        assert "workflow_count" in self.summary
        assert self.summary["workflow_count"] > 0

    def test_has_risk_count(self):
        assert "risk_count" in self.summary
        assert self.summary["risk_count"] > 0

    def test_has_pilot_count(self):
        assert "pilot_count" in self.summary
        assert self.summary["pilot_count"] > 0

    def test_has_overall_readiness_score(self):
        assert "overall_readiness_score" in self.summary

    def test_has_critical_risk_count(self):
        assert "critical_risk_count" in self.summary
        assert self.summary["critical_risk_count"] >= 1

    def test_has_governance_gap_count(self):
        assert "governance_gap_count" in self.summary
        assert self.summary["governance_gap_count"] > 0

    def test_has_high_priority_training_count(self):
        assert "high_priority_training_count" in self.summary


class TestFormatAuditDataAsMarkdown:
    def test_returns_string(self):
        md = adm.format_audit_data_as_markdown(_valid())
        assert isinstance(md, str)

    def test_non_empty(self):
        md = adm.format_audit_data_as_markdown(_valid())
        assert len(md) > 100

    def test_contains_organisation_name(self):
        md = adm.format_audit_data_as_markdown(_valid())
        assert "BrightPath" in md

    def test_contains_readiness_scores_heading(self):
        md = adm.format_audit_data_as_markdown(_valid())
        assert "Readiness Scores" in md

    def test_contains_workflow_findings_heading(self):
        md = adm.format_audit_data_as_markdown(_valid())
        assert "Workflow Findings" in md

    def test_contains_risk_findings_heading(self):
        md = adm.format_audit_data_as_markdown(_valid())
        assert "Risk Findings" in md

    def test_empty_audit_does_not_crash(self):
        md = adm.format_audit_data_as_markdown({})
        assert isinstance(md, str)
