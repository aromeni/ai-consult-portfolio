"""Tests for src/sample_data.py — Phase 1."""

import pytest
from src.sample_data import (
    get_brightpath_training_scenario,
    get_default_priority_topics,
    get_default_staff_roles,
    get_responsible_ai_topic_descriptions,
)


class TestBrightpathScenario:
    def test_returns_dict(self):
        result = get_brightpath_training_scenario()
        assert isinstance(result, dict)

    def test_required_keys_present(self):
        result = get_brightpath_training_scenario()
        required = [
            "organisation_name",
            "organisation_type",
            "staff_count",
            "sector",
            "country_context",
            "current_ai_use",
            "main_concerns",
            "staff_roles",
            "training_goal",
            "training_duration",
            "delivery_mode",
            "priority_topics",
        ]
        for key in required:
            assert key in result, f"Key '{key}' missing from scenario"

    def test_organisation_name_is_brightpath(self):
        result = get_brightpath_training_scenario()
        assert "BrightPath" in result["organisation_name"]

    def test_staff_count_is_positive_int(self):
        result = get_brightpath_training_scenario()
        assert isinstance(result["staff_count"], int)
        assert result["staff_count"] > 0

    def test_priority_topics_non_empty(self):
        result = get_brightpath_training_scenario()
        topics = result["priority_topics"]
        assert isinstance(topics, list)
        assert len(topics) > 0

    def test_staff_roles_non_empty(self):
        result = get_brightpath_training_scenario()
        roles = result["staff_roles"]
        assert isinstance(roles, list)
        assert len(roles) > 0

    def test_main_concerns_non_empty(self):
        result = get_brightpath_training_scenario()
        concerns = result["main_concerns"]
        assert isinstance(concerns, list)
        assert len(concerns) > 0

    def test_current_ai_use_is_string(self):
        result = get_brightpath_training_scenario()
        assert isinstance(result["current_ai_use"], str)
        assert len(result["current_ai_use"]) > 0

    def test_training_goal_is_string(self):
        result = get_brightpath_training_scenario()
        assert isinstance(result["training_goal"], str)
        assert len(result["training_goal"]) > 0


class TestDefaultPriorityTopics:
    def test_returns_list(self):
        result = get_default_priority_topics()
        assert isinstance(result, list)

    def test_non_empty(self):
        result = get_default_priority_topics()
        assert len(result) > 0

    def test_contains_safe_prompting(self):
        result = get_default_priority_topics()
        assert "safe prompting" in result

    def test_contains_learner_data_boundaries(self):
        result = get_default_priority_topics()
        assert "learner data boundaries" in result

    def test_all_items_are_strings(self):
        result = get_default_priority_topics()
        for item in result:
            assert isinstance(item, str)
            assert len(item) > 0


class TestDefaultStaffRoles:
    def test_returns_list(self):
        result = get_default_staff_roles()
        assert isinstance(result, list)

    def test_non_empty(self):
        result = get_default_staff_roles()
        assert len(result) > 0

    def test_contains_tutors(self):
        result = get_default_staff_roles()
        assert "tutors" in result

    def test_all_items_are_strings(self):
        result = get_default_staff_roles()
        for item in result:
            assert isinstance(item, str)
            assert len(item) > 0


class TestResponsibleAiTopicDescriptions:
    def test_returns_dict(self):
        result = get_responsible_ai_topic_descriptions()
        assert isinstance(result, dict)

    def test_non_empty(self):
        result = get_responsible_ai_topic_descriptions()
        assert len(result) > 0

    def test_safe_prompting_has_description(self):
        result = get_responsible_ai_topic_descriptions()
        assert "safe prompting" in result
        assert isinstance(result["safe prompting"], str)
        assert len(result["safe prompting"]) > 0

    def test_all_values_are_non_empty_strings(self):
        result = get_responsible_ai_topic_descriptions()
        for key, value in result.items():
            assert isinstance(value, str), f"Description for '{key}' is not a string"
            assert len(value) > 0, f"Description for '{key}' is empty"

    def test_priority_topics_have_descriptions(self):
        from src.sample_data import get_default_priority_topics
        topics = get_default_priority_topics()
        descriptions = get_responsible_ai_topic_descriptions()
        for topic in topics:
            assert topic in descriptions, f"No description found for topic '{topic}'"
