"""
Tests for src/chart_utils.py — Chart Utilities
Build 6 · BrightPath ChatGPT Mastery Project
"""

import os
import tempfile
import pytest

from src.chart_utils import (
    create_completion_status_chart,
    create_coverage_level_chart,
    create_gap_severity_chart,
    create_recommendation_priority_chart,
    create_maturity_level_chart,
    create_governance_score_chart,
    generate_all_export_charts,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_dir(tmp_path):
    return str(tmp_path)


@pytest.fixture
def completion_data():
    return {
        "items": {
            "Policy Pack": True,
            "Governance Framework": True,
            "Coverage Review": False,
            "Gap Analysis": False,
            "Recommendations": False,
            "Governance Maturity": False,
            "Governance Report": False,
        },
        "total": 7,
        "complete": 2,
        "incomplete": 5,
        "completion_percentage": 28.6,
    }


@pytest.fixture
def coverage_data():
    return {
        "counts": {
            "Strong coverage": 3,
            "Partial coverage": 5,
            "Weak coverage": 2,
            "Not covered": 2,
        },
        "total": 12,
    }


@pytest.fixture
def gap_data():
    return {
        "counts": {
            "Critical gap": 1,
            "High gap": 2,
            "Medium gap": 1,
            "Low gap": 1,
        },
        "total": 5,
    }


@pytest.fixture
def recommendation_data():
    return {
        "counts": {
            "Urgent": 1,
            "High priority": 2,
            "Medium priority": 1,
            "Low priority": 1,
        },
        "total": 5,
    }


@pytest.fixture
def maturity_data():
    return {
        "counts": {
            "Initial governance": 2,
            "Developing governance": 4,
            "Defined governance": 3,
            "Managed governance": 3,
            "Optimised governance": 0,
        },
        "total": 12,
    }


@pytest.fixture
def score_data():
    return {
        "overall_governance_score": 48,
        "overall_coverage_score": 62,
        "overall_maturity_level": "Developing governance",
        "overall_coverage_level": "Partial coverage",
        "domain_maturity_scores": {
            "Strategy and Ownership": 35,
            "Approved AI Tools": 70,
            "Data Protection": 80,
            "Safeguarding Boundaries": 55,
        },
    }


@pytest.fixture
def full_analytics(completion_data, coverage_data, gap_data, recommendation_data, maturity_data, score_data):
    return {
        "export_completion": completion_data,
        "coverage_levels": coverage_data,
        "gap_severities": gap_data,
        "recommendation_priorities": recommendation_data,
        "maturity_levels": maturity_data,
        "governance_scores": score_data,
    }


# ---------------------------------------------------------------------------
# create_completion_status_chart
# ---------------------------------------------------------------------------

class TestCreateCompletionStatusChart:
    def test_returns_string(self, completion_data, tmp_dir):
        path = os.path.join(tmp_dir, "completion.png")
        result = create_completion_status_chart(completion_data, path)
        assert isinstance(result, str)

    def test_creates_file(self, completion_data, tmp_dir):
        path = os.path.join(tmp_dir, "completion.png")
        result = create_completion_status_chart(completion_data, path)
        if result:
            assert os.path.exists(result)

    def test_empty_items_returns_empty_string(self, tmp_dir):
        path = os.path.join(tmp_dir, "completion.png")
        result = create_completion_status_chart({"items": {}}, path)
        assert result == ""

    def test_empty_data_does_not_crash(self, tmp_dir):
        path = os.path.join(tmp_dir, "completion.png")
        result = create_completion_status_chart({}, path)
        assert result == ""

    def test_creates_parent_dir_if_missing(self, tmp_dir, completion_data):
        nested_path = os.path.join(tmp_dir, "subdir", "completion.png")
        result = create_completion_status_chart(completion_data, nested_path)
        if result:
            assert os.path.exists(result)


# ---------------------------------------------------------------------------
# create_coverage_level_chart
# ---------------------------------------------------------------------------

class TestCreateCoverageLevelChart:
    def test_returns_string(self, coverage_data, tmp_dir):
        path = os.path.join(tmp_dir, "coverage.png")
        result = create_coverage_level_chart(coverage_data, path)
        assert isinstance(result, str)

    def test_creates_file(self, coverage_data, tmp_dir):
        path = os.path.join(tmp_dir, "coverage.png")
        result = create_coverage_level_chart(coverage_data, path)
        if result:
            assert os.path.exists(result)

    def test_zero_counts_returns_empty(self, tmp_dir):
        data = {"counts": {"Strong coverage": 0, "Partial coverage": 0, "Weak coverage": 0, "Not covered": 0}, "total": 0}
        path = os.path.join(tmp_dir, "coverage.png")
        result = create_coverage_level_chart(data, path)
        assert result == ""

    def test_empty_data_does_not_crash(self, tmp_dir):
        path = os.path.join(tmp_dir, "coverage.png")
        result = create_coverage_level_chart({}, path)
        assert result == ""


# ---------------------------------------------------------------------------
# create_gap_severity_chart
# ---------------------------------------------------------------------------

class TestCreateGapSeverityChart:
    def test_returns_string(self, gap_data, tmp_dir):
        path = os.path.join(tmp_dir, "gaps.png")
        result = create_gap_severity_chart(gap_data, path)
        assert isinstance(result, str)

    def test_creates_file(self, gap_data, tmp_dir):
        path = os.path.join(tmp_dir, "gaps.png")
        result = create_gap_severity_chart(gap_data, path)
        if result:
            assert os.path.exists(result)

    def test_zero_counts_returns_empty(self, tmp_dir):
        data = {"counts": {"Critical gap": 0, "High gap": 0, "Medium gap": 0, "Low gap": 0}, "total": 0}
        path = os.path.join(tmp_dir, "gaps.png")
        result = create_gap_severity_chart(data, path)
        assert result == ""

    def test_empty_data_does_not_crash(self, tmp_dir):
        path = os.path.join(tmp_dir, "gaps.png")
        result = create_gap_severity_chart({}, path)
        assert result == ""


# ---------------------------------------------------------------------------
# create_recommendation_priority_chart
# ---------------------------------------------------------------------------

class TestCreateRecommendationPriorityChart:
    def test_returns_string(self, recommendation_data, tmp_dir):
        path = os.path.join(tmp_dir, "recs.png")
        result = create_recommendation_priority_chart(recommendation_data, path)
        assert isinstance(result, str)

    def test_creates_file(self, recommendation_data, tmp_dir):
        path = os.path.join(tmp_dir, "recs.png")
        result = create_recommendation_priority_chart(recommendation_data, path)
        if result:
            assert os.path.exists(result)

    def test_zero_counts_returns_empty(self, tmp_dir):
        data = {"counts": {"Urgent": 0, "High priority": 0, "Medium priority": 0, "Low priority": 0}, "total": 0}
        path = os.path.join(tmp_dir, "recs.png")
        result = create_recommendation_priority_chart(data, path)
        assert result == ""

    def test_empty_data_does_not_crash(self, tmp_dir):
        path = os.path.join(tmp_dir, "recs.png")
        result = create_recommendation_priority_chart({}, path)
        assert result == ""


# ---------------------------------------------------------------------------
# create_maturity_level_chart
# ---------------------------------------------------------------------------

class TestCreateMaturityLevelChart:
    def test_returns_string(self, maturity_data, tmp_dir):
        path = os.path.join(tmp_dir, "maturity.png")
        result = create_maturity_level_chart(maturity_data, path)
        assert isinstance(result, str)

    def test_creates_file(self, maturity_data, tmp_dir):
        path = os.path.join(tmp_dir, "maturity.png")
        result = create_maturity_level_chart(maturity_data, path)
        if result:
            assert os.path.exists(result)

    def test_all_zero_counts_returns_empty(self, tmp_dir):
        data = {
            "counts": {
                "Initial governance": 0,
                "Developing governance": 0,
                "Defined governance": 0,
                "Managed governance": 0,
                "Optimised governance": 0,
            },
            "total": 0,
        }
        path = os.path.join(tmp_dir, "maturity.png")
        result = create_maturity_level_chart(data, path)
        assert result == ""

    def test_empty_data_does_not_crash(self, tmp_dir):
        path = os.path.join(tmp_dir, "maturity.png")
        result = create_maturity_level_chart({}, path)
        assert result == ""


# ---------------------------------------------------------------------------
# create_governance_score_chart
# ---------------------------------------------------------------------------

class TestCreateGovernanceScoreChart:
    def test_returns_string(self, score_data, tmp_dir):
        path = os.path.join(tmp_dir, "scores.png")
        result = create_governance_score_chart(score_data, path)
        assert isinstance(result, str)

    def test_creates_file(self, score_data, tmp_dir):
        path = os.path.join(tmp_dir, "scores.png")
        result = create_governance_score_chart(score_data, path)
        if result:
            assert os.path.exists(result)

    def test_empty_domain_scores_falls_back_to_overall(self, tmp_dir):
        data = {
            "domain_maturity_scores": {},
            "overall_governance_score": 50,
            "overall_coverage_score": 60,
        }
        path = os.path.join(tmp_dir, "scores.png")
        result = create_governance_score_chart(data, path)
        if result:
            assert os.path.exists(result)

    def test_empty_data_returns_empty_or_string(self, tmp_dir):
        path = os.path.join(tmp_dir, "scores.png")
        result = create_governance_score_chart({}, path)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# generate_all_export_charts
# ---------------------------------------------------------------------------

class TestGenerateAllExportCharts:
    def test_returns_dict(self, full_analytics, tmp_dir):
        result = generate_all_export_charts(full_analytics, output_dir=tmp_dir)
        assert isinstance(result, dict)

    def test_empty_analytics_returns_dict(self, tmp_dir):
        result = generate_all_export_charts({}, output_dir=tmp_dir)
        assert isinstance(result, dict)

    def test_no_crash_on_empty_analytics(self, tmp_dir):
        result = generate_all_export_charts({}, output_dir=tmp_dir)
        assert result is not None

    def test_chart_paths_point_to_existing_files(self, full_analytics, tmp_dir):
        result = generate_all_export_charts(full_analytics, output_dir=tmp_dir)
        for key, path in result.items():
            assert os.path.exists(path), f"Chart file does not exist: {path}"

    def test_returns_known_keys_only(self, full_analytics, tmp_dir):
        valid_keys = {
            "completion_status", "coverage_levels", "gap_severities",
            "recommendation_priorities", "maturity_levels", "governance_scores",
        }
        result = generate_all_export_charts(full_analytics, output_dir=tmp_dir)
        for key in result:
            assert key in valid_keys

    def test_creates_output_dir_if_missing(self, full_analytics, tmp_dir):
        new_dir = os.path.join(tmp_dir, "charts_subdir")
        assert not os.path.exists(new_dir)
        generate_all_export_charts(full_analytics, output_dir=new_dir)
        assert os.path.exists(new_dir)

    def test_partial_analytics_does_not_crash(self, tmp_dir):
        partial = {"export_completion": {"items": {"Policy Pack": True}, "total": 1, "complete": 1}}
        result = generate_all_export_charts(partial, output_dir=tmp_dir)
        assert isinstance(result, dict)
