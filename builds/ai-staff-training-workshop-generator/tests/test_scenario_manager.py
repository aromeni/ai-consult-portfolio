"""Tests for src/scenario_manager.py — Phase 1."""

import pytest
from src.scenario_manager import (
    validate_training_scenario,
    summarise_training_scenario,
    format_scenario_as_markdown,
    create_scenario_from_form_data,
)
from src.sample_data import get_brightpath_training_scenario


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_scenario():
    return get_brightpath_training_scenario()


@pytest.fixture
def minimal_valid_scenario():
    return {
        "organisation_name": "Test Org",
        "organisation_type": "Test type",
        "staff_count": 5,
        "current_ai_use": "Some AI use",
        "training_goal": "Help staff use AI safely",
        "priority_topics": ["safe prompting"],
    }


# ── validate_training_scenario ─────────────────────────────────────────────────

class TestValidateTrainingScenario:
    def test_valid_scenario_passes(self, valid_scenario):
        is_valid, msg = validate_training_scenario(valid_scenario)
        assert is_valid is True
        assert "BrightPath" in msg

    def test_minimal_valid_scenario_passes(self, minimal_valid_scenario):
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is True

    def test_empty_scenario_fails(self):
        is_valid, msg = validate_training_scenario({})
        assert is_valid is False

    def test_none_scenario_fails(self):
        is_valid, msg = validate_training_scenario(None)
        assert is_valid is False

    def test_missing_organisation_name_fails(self, minimal_valid_scenario):
        del minimal_valid_scenario["organisation_name"]
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False
        assert "organisation name" in msg.lower()

    def test_empty_organisation_name_fails(self, minimal_valid_scenario):
        minimal_valid_scenario["organisation_name"] = "   "
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False

    def test_missing_organisation_type_fails(self, minimal_valid_scenario):
        del minimal_valid_scenario["organisation_type"]
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False
        assert "organisation type" in msg.lower()

    def test_missing_staff_count_fails(self, minimal_valid_scenario):
        del minimal_valid_scenario["staff_count"]
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False

    def test_zero_staff_count_fails(self, minimal_valid_scenario):
        minimal_valid_scenario["staff_count"] = 0
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False
        assert "positive" in msg.lower()

    def test_negative_staff_count_fails(self, minimal_valid_scenario):
        minimal_valid_scenario["staff_count"] = -1
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False
        assert "positive" in msg.lower()

    def test_non_numeric_staff_count_fails(self, minimal_valid_scenario):
        minimal_valid_scenario["staff_count"] = "many"
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False

    def test_missing_current_ai_use_fails(self, minimal_valid_scenario):
        del minimal_valid_scenario["current_ai_use"]
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False

    def test_missing_training_goal_fails(self, minimal_valid_scenario):
        del minimal_valid_scenario["training_goal"]
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False

    def test_empty_priority_topics_fails(self, minimal_valid_scenario):
        minimal_valid_scenario["priority_topics"] = []
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False
        assert "topic" in msg.lower()

    def test_missing_priority_topics_fails(self, minimal_valid_scenario):
        del minimal_valid_scenario["priority_topics"]
        is_valid, msg = validate_training_scenario(minimal_valid_scenario)
        assert is_valid is False

    def test_returns_tuple(self, valid_scenario):
        result = validate_training_scenario(valid_scenario)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_bool(self, valid_scenario):
        is_valid, _ = validate_training_scenario(valid_scenario)
        assert isinstance(is_valid, bool)

    def test_second_element_is_string(self, valid_scenario):
        _, msg = validate_training_scenario(valid_scenario)
        assert isinstance(msg, str)


# ── summarise_training_scenario ────────────────────────────────────────────────

class TestSummariseTrainingScenario:
    def test_returns_dict(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        assert isinstance(result, dict)

    def test_required_keys_present(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        expected_keys = [
            "organisation_name",
            "organisation_type",
            "staff_count",
            "sector",
            "country_context",
            "topic_count",
            "role_count",
            "training_duration",
            "delivery_mode",
            "concern_count",
        ]
        for key in expected_keys:
            assert key in result, f"Key '{key}' missing from summary"

    def test_organisation_name_matches(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        assert result["organisation_name"] == valid_scenario["organisation_name"]

    def test_staff_count_matches(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        assert result["staff_count"] == valid_scenario["staff_count"]

    def test_topic_count_is_correct(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        assert result["topic_count"] == len(valid_scenario["priority_topics"])

    def test_role_count_is_correct(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        assert result["role_count"] == len(valid_scenario["staff_roles"])

    def test_concern_count_is_correct(self, valid_scenario):
        result = summarise_training_scenario(valid_scenario)
        assert result["concern_count"] == len(valid_scenario["main_concerns"])

    def test_empty_scenario_returns_zeros(self):
        result = summarise_training_scenario({})
        assert result["topic_count"] == 0
        assert result["role_count"] == 0
        assert result["concern_count"] == 0


# ── format_scenario_as_markdown ────────────────────────────────────────────────

class TestFormatScenarioAsMarkdown:
    def test_returns_string(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert isinstance(result, str)

    def test_non_empty(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert len(result) > 0

    def test_contains_organisation_name(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert valid_scenario["organisation_name"] in result

    def test_contains_training_goal(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert valid_scenario["training_goal"] in result

    def test_contains_priority_topics(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        for topic in valid_scenario["priority_topics"]:
            assert topic in result

    def test_contains_synthetic_notice(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert "Synthetic" in result or "synthetic" in result

    def test_starts_with_heading(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert result.startswith("#")

    def test_contains_markdown_headings(self, valid_scenario):
        result = format_scenario_as_markdown(valid_scenario)
        assert "##" in result


# ── create_scenario_from_form_data ─────────────────────────────────────────────

class TestCreateScenarioFromFormData:
    def test_returns_dict(self):
        result = create_scenario_from_form_data({"organisation_name": "Test"})
        assert isinstance(result, dict)

    def test_staff_count_converted_to_int(self):
        result = create_scenario_from_form_data({"staff_count": "10"})
        assert result["staff_count"] == 10
        assert isinstance(result["staff_count"], int)

    def test_invalid_staff_count_becomes_zero(self):
        result = create_scenario_from_form_data({"staff_count": "not-a-number"})
        assert result["staff_count"] == 0

    def test_list_fields_preserved_as_lists(self):
        data = {
            "priority_topics": ["safe prompting", "human review"],
            "staff_roles": ["tutors"],
            "main_concerns": ["hallucination"],
        }
        result = create_scenario_from_form_data(data)
        assert isinstance(result["priority_topics"], list)
        assert isinstance(result["staff_roles"], list)
        assert isinstance(result["main_concerns"], list)

    def test_newline_string_split_into_list(self):
        data = {"main_concerns": "hallucination\nbias\napproved tools"}
        result = create_scenario_from_form_data(data)
        assert isinstance(result["main_concerns"], list)
        assert "hallucination" in result["main_concerns"]
        assert "bias" in result["main_concerns"]

    def test_empty_lines_stripped_from_list(self):
        data = {"main_concerns": "hallucination\n\nbias\n"}
        result = create_scenario_from_form_data(data)
        assert "" not in result["main_concerns"]
        assert len(result["main_concerns"]) == 2

    def test_original_fields_preserved(self):
        data = {
            "organisation_name": "Acme Training",
            "training_goal": "Teach safe AI use",
        }
        result = create_scenario_from_form_data(data)
        assert result["organisation_name"] == "Acme Training"
        assert result["training_goal"] == "Teach safe AI use"
