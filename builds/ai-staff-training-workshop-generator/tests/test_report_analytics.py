"""Tests for src/report_analytics.py.

All tests use synthetic data. No external APIs. No real data.
"""

import pytest
from src import report_analytics as ra


# ── Fixtures ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_session_state():
    return {
        "training_scenario": {"organisation_name": "BrightPath"},
        "training_needs_assessment": {"topic_assessments": []},
        "workshop_plan": {"agenda": []},
        "training_activities": [{"activity_type": "sorting"}, {"activity_type": "rewrite"}],
        "facilitator_guide": {"guide_title": "Guide"},
        "staff_handout": {"handout_title": "Handout"},
        "knowledge_check": {"multiple_choice_questions": []},
    }


@pytest.fixture
def sample_pack_data():
    return {
        "scenario": {
            "organisation_name": "BrightPath",
            "priority_topics": ["learner data", "safeguarding", "hallucination"],
        },
        "training_needs_assessment": {
            "topic_assessments": [
                {"title": "Learner Data", "priority_level": "high"},
                {"title": "Safeguarding", "priority_level": "high"},
            ],
            "recommended_learning_outcomes": ["Outcome 1", "Outcome 2"],
        },
        "workshop_plan": {
            "workshop_title": "AI Safe Use",
            "duration_minutes": 90,
            "agenda": [
                {"section_title": "Welcome", "duration_minutes": 10},
                {"section_title": "Safe Prompting", "duration_minutes": 20},
            ],
        },
        "training_activities": [
            {"activity_type": "sorting", "activity_title": "Sort Prompts"},
            {"activity_type": "rewrite", "activity_title": "Rewrite Prompt"},
            {"activity_type": "sorting", "activity_title": "More Sorting"},
        ],
        "facilitator_guide": {"guide_title": "Facilitator Guide"},
        "staff_handout": {"handout_title": "Staff Handout"},
        "knowledge_check": {
            "multiple_choice_questions": [
                {"question_id": "mcq001", "topic": "learner data", "question": "Q1?"},
                {"question_id": "mcq002", "topic": "safeguarding", "question": "Q2?"},
            ],
            "scenario_questions": [
                {"question_id": "sq001", "topic": "hallucination", "question": "Scenario?"},
            ],
            "answer_key": {"multiple_choice_answers": []},
        },
    }


# ── calculate_section_completion_status ──────────────────────────────────────────

class TestCalculateSectionCompletionStatus:
    def test_returns_dict(self, sample_session_state):
        result = ra.calculate_section_completion_status(sample_session_state)
        assert isinstance(result, dict)

    def test_all_sections_present(self, sample_session_state):
        result = ra.calculate_section_completion_status(sample_session_state)
        assert "Organisation Scenario" in result
        assert "Training Needs Assessment" in result
        assert "Workshop Plan" in result
        assert "Training Activities" in result
        assert "Facilitator Guide" in result
        assert "Staff Handout" in result
        assert "Knowledge Check" in result

    def test_complete_when_loaded(self, sample_session_state):
        result = ra.calculate_section_completion_status(sample_session_state)
        assert result["Organisation Scenario"] is True
        assert result["Training Activities"] is True

    def test_incomplete_when_missing(self):
        result = ra.calculate_section_completion_status({})
        assert result["Organisation Scenario"] is False
        assert result["Knowledge Check"] is False

    def test_handles_empty_dict(self):
        result = ra.calculate_section_completion_status({})
        assert isinstance(result, dict)
        assert all(v is False for v in result.values())

    def test_values_are_booleans(self, sample_session_state):
        result = ra.calculate_section_completion_status(sample_session_state)
        for v in result.values():
            assert isinstance(v, bool)


# ── calculate_training_topic_counts ─────────────────────────────────────────────

class TestCalculateTrainingTopicCounts:
    def test_returns_dict(self, sample_pack_data):
        result = ra.calculate_training_topic_counts(sample_pack_data)
        assert isinstance(result, dict)

    def test_counts_topics(self, sample_pack_data):
        result = ra.calculate_training_topic_counts(sample_pack_data)
        assert "learner data" in result
        assert "safeguarding" in result
        assert "hallucination" in result

    def test_each_topic_count_is_1(self, sample_pack_data):
        result = ra.calculate_training_topic_counts(sample_pack_data)
        for v in result.values():
            assert v == 1

    def test_empty_scenario(self):
        result = ra.calculate_training_topic_counts({"scenario": {}})
        assert result == {}

    def test_no_scenario(self):
        result = ra.calculate_training_topic_counts({})
        assert result == {}

    def test_returns_strings_as_keys(self, sample_pack_data):
        result = ra.calculate_training_topic_counts(sample_pack_data)
        for k in result.keys():
            assert isinstance(k, str)


# ── calculate_activity_type_counts ───────────────────────────────────────────────

class TestCalculateActivityTypeCounts:
    def test_returns_dict(self, sample_pack_data):
        result = ra.calculate_activity_type_counts(sample_pack_data["training_activities"])
        assert isinstance(result, dict)

    def test_counts_types(self, sample_pack_data):
        result = ra.calculate_activity_type_counts(sample_pack_data["training_activities"])
        assert result.get("sorting") == 2
        assert result.get("rewrite") == 1

    def test_empty_list(self):
        result = ra.calculate_activity_type_counts([])
        assert result == {}

    def test_none_returns_empty(self):
        result = ra.calculate_activity_type_counts(None)
        assert result == {}

    def test_skips_non_dict_items(self):
        result = ra.calculate_activity_type_counts([{"activity_type": "sorting"}, "not a dict"])
        assert result.get("sorting") == 1

    def test_missing_activity_type_uses_other(self):
        result = ra.calculate_activity_type_counts([{"no_type": True}])
        assert "other" in result


# ── calculate_workshop_time_allocation ───────────────────────────────────────────

class TestCalculateWorkshopTimeAllocation:
    def test_returns_list(self, sample_pack_data):
        result = ra.calculate_workshop_time_allocation(sample_pack_data["workshop_plan"])
        assert isinstance(result, list)

    def test_list_items_have_section_and_minutes(self, sample_pack_data):
        result = ra.calculate_workshop_time_allocation(sample_pack_data["workshop_plan"])
        for item in result:
            assert "section" in item
            assert "minutes" in item

    def test_correct_count(self, sample_pack_data):
        result = ra.calculate_workshop_time_allocation(sample_pack_data["workshop_plan"])
        assert len(result) == 2

    def test_empty_workshop_plan(self):
        result = ra.calculate_workshop_time_allocation({})
        assert result == []

    def test_none_returns_empty(self):
        result = ra.calculate_workshop_time_allocation(None)
        assert result == []

    def test_minutes_are_integers(self, sample_pack_data):
        result = ra.calculate_workshop_time_allocation(sample_pack_data["workshop_plan"])
        for item in result:
            assert isinstance(item["minutes"], int)


# ── calculate_knowledge_check_topic_counts ───────────────────────────────────────

class TestCalculateKnowledgeCheckTopicCounts:
    def test_returns_dict(self, sample_pack_data):
        result = ra.calculate_knowledge_check_topic_counts(sample_pack_data["knowledge_check"])
        assert isinstance(result, dict)

    def test_counts_mcq_and_scenario_topics(self, sample_pack_data):
        result = ra.calculate_knowledge_check_topic_counts(sample_pack_data["knowledge_check"])
        assert result.get("learner data") == 1
        assert result.get("safeguarding") == 1
        assert result.get("hallucination") == 1

    def test_empty_knowledge_check(self):
        result = ra.calculate_knowledge_check_topic_counts({})
        assert result == {}

    def test_none_returns_empty(self):
        result = ra.calculate_knowledge_check_topic_counts(None)
        assert result == {}

    def test_accumulates_counts(self):
        kc = {
            "multiple_choice_questions": [
                {"topic": "bias"}, {"topic": "bias"}, {"topic": "safeguarding"},
            ],
            "scenario_questions": [],
        }
        result = ra.calculate_knowledge_check_topic_counts(kc)
        assert result.get("bias") == 2
        assert result.get("safeguarding") == 1


# ── calculate_report_quality_summary ────────────────────────────────────────────

class TestCalculateReportQualitySummary:
    def test_returns_dict(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert isinstance(result, dict)

    def test_required_keys_present(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert "sections_available" in result
        assert "sections_total" in result
        assert "completeness_pct" in result
        assert "has_responsible_use_boundaries" in result
        assert "has_human_review_requirement" in result
        assert "has_prototype_notice" in result
        assert "activity_count" in result
        assert "mcq_count" in result
        assert "answer_key_included" in result

    def test_completeness_full_pack(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert result["sections_available"] == 7
        assert result["completeness_pct"] == 100

    def test_completeness_empty_pack(self):
        result = ra.calculate_report_quality_summary({})
        assert result["sections_available"] == 0
        assert result["completeness_pct"] == 0

    def test_responsible_use_always_true(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert result["has_responsible_use_boundaries"] is True
        assert result["has_human_review_requirement"] is True
        assert result["has_prototype_notice"] is True

    def test_activity_count_correct(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert result["activity_count"] == 3

    def test_mcq_count_correct(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert result["mcq_count"] == 2

    def test_answer_key_included(self, sample_pack_data):
        result = ra.calculate_report_quality_summary(sample_pack_data)
        assert result["answer_key_included"] is True


# ── build_training_pack_analytics ────────────────────────────────────────────────

class TestBuildTrainingPackAnalytics:
    def test_returns_dict(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        assert isinstance(result, dict)

    def test_required_top_level_keys(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        assert "section_completion" in result
        assert "topic_counts" in result
        assert "activity_type_counts" in result
        assert "workshop_time_allocation" in result
        assert "knowledge_check_topic_counts" in result
        assert "report_quality" in result
        assert "organisation_name" in result
        assert "generated_date" in result

    def test_organisation_name_extracted(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        assert result["organisation_name"] == "BrightPath"

    def test_generated_date_is_string(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        assert isinstance(result["generated_date"], str)
        assert len(result["generated_date"]) == 10  # YYYY-MM-DD

    def test_section_completion_is_dict(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        assert isinstance(result["section_completion"], dict)

    def test_report_quality_is_dict(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        assert isinstance(result["report_quality"], dict)

    def test_handles_empty_pack_data(self):
        result = ra.build_training_pack_analytics({})
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Organisation"

    def test_handles_none_input(self):
        result = ra.build_training_pack_analytics(None)
        assert isinstance(result, dict)

    def test_section_completion_values_are_booleans(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        for v in result["section_completion"].values():
            assert isinstance(v, bool)

    def test_full_pack_all_sections_complete(self, sample_pack_data):
        result = ra.build_training_pack_analytics(sample_pack_data)
        completion = result["section_completion"]
        assert completion["Organisation Scenario"] is True
        assert completion["Training Activities"] is True
        assert completion["Knowledge Check"] is True


class TestCalculatePriorityTopicCounts:
    def test_returns_dict(self):
        assert isinstance(ra.calculate_priority_topic_counts({}), dict)

    def test_matches_training_topic_counts(self):
        pack_data = {"scenario": {"priority_topics": ["Learner data", "Safeguarding"]}}
        assert ra.calculate_priority_topic_counts(pack_data) == ra.calculate_training_topic_counts(pack_data)

    def test_empty_pack_data_returns_empty_dict(self):
        assert ra.calculate_priority_topic_counts({}) == {}

    def test_counts_each_topic(self):
        pack_data = {"scenario": {"priority_topics": ["A", "B", "C"]}}
        result = ra.calculate_priority_topic_counts(pack_data)
        assert len(result) == 3
