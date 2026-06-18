"""Tests for src/chart_utils.py — matplotlib chart file generation."""

import os

from src import chart_utils as cu


COMPLETION = {
    "Organisation Scenario": True,
    "Workshop Plan": True,
    "Knowledge Check": False,
}
ACTIVITY_COUNTS = {"sorting": 2, "rewrite": 1, "scenario": 3}
TIME_ALLOCATION = [
    {"section": "Welcome", "minutes": 10},
    {"section": "Safe Prompting", "minutes": 30},
    {"section": "Wrap-up", "minutes": 10},
]
TOPIC_COUNTS = {"learner_data": 3, "safeguarding": 2, "hallucination": 1}


class TestCreateSectionCompletionChart:
    def test_creates_png_file(self, tmp_path):
        path = cu.create_section_completion_chart(COMPLETION, str(tmp_path / "c.png"))
        assert os.path.isfile(path)

    def test_returns_path_string(self, tmp_path):
        path = cu.create_section_completion_chart(COMPLETION, str(tmp_path / "c.png"))
        assert isinstance(path, str) and path.endswith(".png")

    def test_empty_data_returns_empty_string(self, tmp_path):
        assert cu.create_section_completion_chart({}, str(tmp_path / "c.png")) == ""

    def test_file_has_png_magic_bytes(self, tmp_path):
        path = cu.create_section_completion_chart(COMPLETION, str(tmp_path / "c.png"))
        with open(path, "rb") as f:
            assert f.read(8).startswith(b"\x89PNG")


class TestCreateActivityMixChart:
    def test_creates_png_file(self, tmp_path):
        path = cu.create_activity_mix_chart(ACTIVITY_COUNTS, str(tmp_path / "a.png"))
        assert os.path.isfile(path)

    def test_empty_data_returns_empty_string(self, tmp_path):
        assert cu.create_activity_mix_chart({}, str(tmp_path / "a.png")) == ""


class TestCreateWorkshopTimeChart:
    def test_creates_png_file(self, tmp_path):
        path = cu.create_workshop_time_chart(TIME_ALLOCATION, str(tmp_path / "t.png"))
        assert os.path.isfile(path)

    def test_empty_data_returns_empty_string(self, tmp_path):
        assert cu.create_workshop_time_chart([], str(tmp_path / "t.png")) == ""

    def test_zero_minute_rows_skipped(self, tmp_path):
        rows = [{"section": "A", "minutes": 0}]
        assert cu.create_workshop_time_chart(rows, str(tmp_path / "t.png")) == ""


class TestCreateKnowledgeTopicChart:
    def test_creates_png_file(self, tmp_path):
        path = cu.create_knowledge_topic_chart(TOPIC_COUNTS, str(tmp_path / "k.png"))
        assert os.path.isfile(path)

    def test_empty_data_returns_empty_string(self, tmp_path):
        assert cu.create_knowledge_topic_chart({}, str(tmp_path / "k.png")) == ""


class TestGenerateAllReportCharts:
    def test_returns_dict(self, tmp_path):
        analytics = {
            "section_completion": COMPLETION,
            "activity_type_counts": ACTIVITY_COUNTS,
            "workshop_time_allocation": TIME_ALLOCATION,
            "knowledge_check_topic_counts": TOPIC_COUNTS,
        }
        charts = cu.generate_all_report_charts(analytics, output_dir=str(tmp_path))
        assert isinstance(charts, dict)
        assert "section_completion" in charts
        assert "activity_mix" in charts
        assert "workshop_time" in charts
        assert "knowledge_topics" in charts

    def test_all_paths_exist(self, tmp_path):
        analytics = {"section_completion": COMPLETION}
        charts = cu.generate_all_report_charts(analytics, output_dir=str(tmp_path))
        for path in charts.values():
            assert os.path.isfile(path)

    def test_empty_analytics_returns_empty_dict(self, tmp_path):
        assert cu.generate_all_report_charts({}, output_dir=str(tmp_path)) == {}

    def test_none_analytics_does_not_crash(self, tmp_path):
        assert cu.generate_all_report_charts(None, output_dir=str(tmp_path)) == {}
