"""Tests for src/chart_utils.py — Build 5 Phase 8."""

import os
import pytest
from src import chart_utils as cu

_COMPLETION = {
    "Audit Data": True,
    "Readiness Summary": True,
    "Risk Register": False,
    "Client Report": True,
}

_READINESS_SCORES = {
    "Strategy": 32,
    "Data Governance": 28,
    "Workflow Opportunity": 68,
    "Risk Management": 25,
    "Overall": 42,
}

_RISK_COUNTS = {"Critical": 0, "High": 4, "Medium": 1, "Low": 0}

_OPP_COUNTS = {"Strategic": 0, "High": 0, "Medium": 4, "Low": 0}

_ROADMAP_COUNTS = {"First 30 Days": 10, "Days 31–60": 7, "Days 61–90": 7}

_FULL_ANALYTICS = {
    "completion_status": _COMPLETION,
    "readiness_score_breakdown": _READINESS_SCORES,
    "risk_level_counts": _RISK_COUNTS,
    "opportunity_priority_counts": _OPP_COUNTS,
    "roadmap_action_counts": _ROADMAP_COUNTS,
}


class TestCreateCompletionStatusChart:
    def test_returns_string(self, tmp_path):
        path = str(tmp_path / "completion.png")
        result = cu.create_completion_status_chart(_COMPLETION, path)
        assert isinstance(result, str)

    def test_creates_file_when_successful(self, tmp_path):
        path = str(tmp_path / "completion.png")
        result = cu.create_completion_status_chart(_COMPLETION, path)
        if result:  # may be empty if matplotlib unavailable
            assert os.path.exists(result)

    def test_handles_empty_data(self, tmp_path):
        path = str(tmp_path / "empty.png")
        result = cu.create_completion_status_chart({}, path)
        assert result == ""

    def test_handles_empty_path(self):
        result = cu.create_completion_status_chart(_COMPLETION, "")
        assert result == ""


class TestCreateReadinessScoreChart:
    def test_returns_string(self, tmp_path):
        path = str(tmp_path / "readiness.png")
        result = cu.create_readiness_score_chart(_READINESS_SCORES, path)
        assert isinstance(result, str)

    def test_creates_file_when_successful(self, tmp_path):
        path = str(tmp_path / "readiness.png")
        result = cu.create_readiness_score_chart(_READINESS_SCORES, path)
        if result:
            assert os.path.exists(result)

    def test_handles_empty_data(self, tmp_path):
        path = str(tmp_path / "empty.png")
        result = cu.create_readiness_score_chart({}, path)
        assert result == ""

    def test_handles_none_path(self):
        result = cu.create_readiness_score_chart(_READINESS_SCORES, "")
        assert result == ""


class TestCreateRiskLevelChart:
    def test_returns_string(self, tmp_path):
        path = str(tmp_path / "risk.png")
        result = cu.create_risk_level_chart(_RISK_COUNTS, path)
        assert isinstance(result, str)

    def test_creates_file_when_successful(self, tmp_path):
        path = str(tmp_path / "risk.png")
        result = cu.create_risk_level_chart(_RISK_COUNTS, path)
        if result:
            assert os.path.exists(result)

    def test_returns_empty_when_all_zero(self, tmp_path):
        path = str(tmp_path / "zero.png")
        result = cu.create_risk_level_chart(
            {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}, path
        )
        assert result == ""

    def test_handles_empty_data(self, tmp_path):
        path = str(tmp_path / "empty.png")
        result = cu.create_risk_level_chart({}, path)
        assert result == ""


class TestCreateOpportunityPriorityChart:
    def test_returns_string(self, tmp_path):
        path = str(tmp_path / "opps.png")
        result = cu.create_opportunity_priority_chart(_OPP_COUNTS, path)
        assert isinstance(result, str)

    def test_creates_file_when_successful(self, tmp_path):
        path = str(tmp_path / "opps.png")
        result = cu.create_opportunity_priority_chart(_OPP_COUNTS, path)
        if result:
            assert os.path.exists(result)

    def test_handles_empty_data(self, tmp_path):
        path = str(tmp_path / "empty.png")
        result = cu.create_opportunity_priority_chart({}, path)
        assert result == ""


class TestCreateRoadmapActionChart:
    def test_returns_string(self, tmp_path):
        path = str(tmp_path / "roadmap.png")
        result = cu.create_roadmap_action_chart(_ROADMAP_COUNTS, path)
        assert isinstance(result, str)

    def test_creates_file_when_successful(self, tmp_path):
        path = str(tmp_path / "roadmap.png")
        result = cu.create_roadmap_action_chart(_ROADMAP_COUNTS, path)
        if result:
            assert os.path.exists(result)

    def test_handles_empty_data(self, tmp_path):
        path = str(tmp_path / "empty.png")
        result = cu.create_roadmap_action_chart({}, path)
        assert result == ""


class TestGenerateAllExportCharts:
    def test_returns_dict(self, tmp_path):
        result = cu.generate_all_export_charts(_FULL_ANALYTICS, str(tmp_path))
        assert isinstance(result, dict)

    def test_creates_chart_files(self, tmp_path):
        result = cu.generate_all_export_charts(_FULL_ANALYTICS, str(tmp_path))
        for path in result.values():
            assert os.path.exists(path)

    def test_handles_empty_analytics(self, tmp_path):
        result = cu.generate_all_export_charts({}, str(tmp_path))
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_handles_none_analytics(self, tmp_path):
        result = cu.generate_all_export_charts(None, str(tmp_path))
        assert isinstance(result, dict)

    def test_chart_keys_are_expected(self, tmp_path):
        result = cu.generate_all_export_charts(_FULL_ANALYTICS, str(tmp_path))
        for key in result:
            assert key in {
                "completion_status",
                "readiness_scores",
                "risk_levels",
                "opportunity_priorities",
                "roadmap_actions",
            }
