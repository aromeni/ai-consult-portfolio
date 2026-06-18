"""Tests for src/needs_assessment.py — Phase 2."""

import pytest
from src.needs_assessment import (
    get_training_topic_catalogue,
    assess_topic_priority,
    generate_training_needs_assessment,
    summarise_training_needs,
    generate_learning_outcomes,
    generate_role_specific_needs,
    format_needs_assessment_as_markdown,
)
from src.sample_data import get_brightpath_training_scenario


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def brightpath():
    return get_brightpath_training_scenario()


@pytest.fixture
def minimal_scenario():
    return {
        "organisation_name": "Test Org",
        "organisation_type": "Test type",
        "staff_count": 5,
        "current_ai_use": "Some use",
        "training_goal": "Help staff use AI safely",
        "priority_topics": ["safe prompting"],
        "staff_roles": ["tutors"],
        "main_concerns": ["data"],
    }


@pytest.fixture
def full_assessment(brightpath):
    return generate_training_needs_assessment(brightpath)


# ── get_training_topic_catalogue ───────────────────────────────────────────────

class TestGetTrainingTopicCatalogue:
    def test_returns_dict(self):
        result = get_training_topic_catalogue()
        assert isinstance(result, dict)

    def test_non_empty(self):
        result = get_training_topic_catalogue()
        assert len(result) > 0

    def test_contains_safe_prompting(self):
        result = get_training_topic_catalogue()
        assert "safe prompting" in result

    def test_contains_learner_data_boundaries(self):
        result = get_training_topic_catalogue()
        assert "learner data boundaries" in result

    def test_contains_safeguarding_boundaries(self):
        result = get_training_topic_catalogue()
        assert "safeguarding boundaries" in result

    def test_contains_hallucination_and_accuracy(self):
        result = get_training_topic_catalogue()
        assert "hallucination and accuracy" in result

    def test_contains_escalation_routes(self):
        result = get_training_topic_catalogue()
        assert "escalation routes" in result

    def test_each_entry_has_required_keys(self):
        result = get_training_topic_catalogue()
        required_keys = {
            "title", "description", "risk_level",
            "why_it_matters", "example_staff_behaviour", "recommended_training_angle",
        }
        for topic, data in result.items():
            for key in required_keys:
                assert key in data, f"Topic '{topic}' is missing key '{key}'"

    def test_risk_level_values_are_valid(self):
        result = get_training_topic_catalogue()
        valid_levels = {"low", "medium", "high"}
        for topic, data in result.items():
            assert data["risk_level"] in valid_levels, (
                f"Topic '{topic}' has invalid risk_level '{data['risk_level']}'"
            )

    def test_all_descriptions_are_non_empty_strings(self):
        result = get_training_topic_catalogue()
        for topic, data in result.items():
            assert isinstance(data["description"], str)
            assert len(data["description"]) > 0


# ── assess_topic_priority ──────────────────────────────────────────────────────

class TestAssessTopicPriority:
    def test_returns_dict(self, brightpath):
        result = assess_topic_priority(brightpath, "safe prompting")
        assert isinstance(result, dict)

    def test_required_keys_present(self, brightpath):
        result = assess_topic_priority(brightpath, "safe prompting")
        for key in ("topic", "title", "priority_level", "risk_level",
                    "why_it_matters", "training_need",
                    "example_staff_behaviour", "recommended_training_angle"):
            assert key in result, f"Key '{key}' missing from topic assessment"

    def test_topic_field_matches_input(self, brightpath):
        result = assess_topic_priority(brightpath, "safe prompting")
        assert result["topic"] == "safe prompting"

    def test_priority_level_is_valid(self, brightpath):
        result = assess_topic_priority(brightpath, "safe prompting")
        assert result["priority_level"] in ("high", "medium", "low")

    def test_learner_data_boundaries_high_for_brightpath(self, brightpath):
        result = assess_topic_priority(brightpath, "learner data boundaries")
        assert result["priority_level"] == "high"

    def test_safeguarding_boundaries_high_for_brightpath(self, brightpath):
        result = assess_topic_priority(brightpath, "safeguarding boundaries")
        assert result["priority_level"] == "high"

    def test_safe_prompting_high_for_brightpath(self, brightpath):
        result = assess_topic_priority(brightpath, "safe prompting")
        assert result["priority_level"] == "high"

    def test_hallucination_high_for_brightpath(self, brightpath):
        result = assess_topic_priority(brightpath, "hallucination and accuracy")
        assert result["priority_level"] == "high"

    def test_approved_tools_high_for_brightpath(self, brightpath):
        result = assess_topic_priority(brightpath, "approved tools")
        assert result["priority_level"] == "high"

    def test_unknown_topic_returns_dict(self, brightpath):
        result = assess_topic_priority(brightpath, "some unknown topic")
        assert isinstance(result, dict)
        assert result["topic"] == "some unknown topic"

    def test_topic_not_in_priority_list_can_be_lower_priority(self):
        scenario = {
            "organisation_name": "Test",
            "priority_topics": [],
            "main_concerns": [],
            "staff_roles": [],
        }
        result = assess_topic_priority(scenario, "time-saving and workflow discipline")
        assert result["priority_level"] in ("low", "medium")


# ── generate_training_needs_assessment ────────────────────────────────────────

class TestGenerateTrainingNeedsAssessment:
    def test_returns_dict(self, brightpath):
        result = generate_training_needs_assessment(brightpath)
        assert isinstance(result, dict)

    def test_required_keys_present(self, full_assessment):
        required = [
            "organisation_name",
            "training_goal",
            "staff_roles",
            "priority_topics",
            "topic_assessments",
            "role_specific_needs",
            "recommended_learning_outcomes",
            "overall_training_focus",
            "risk_summary",
            "recommended_session_type",
            "responsible_use_note",
        ]
        for key in required:
            assert key in full_assessment, f"Key '{key}' missing from assessment"

    def test_organisation_name_matches(self, brightpath, full_assessment):
        assert full_assessment["organisation_name"] == brightpath["organisation_name"]

    def test_topic_assessments_is_list(self, full_assessment):
        assert isinstance(full_assessment["topic_assessments"], list)

    def test_topic_assessments_non_empty(self, full_assessment):
        assert len(full_assessment["topic_assessments"]) > 0

    def test_includes_recommended_learning_outcomes(self, full_assessment):
        outcomes = full_assessment["recommended_learning_outcomes"]
        assert isinstance(outcomes, list)
        assert len(outcomes) >= 3

    def test_includes_role_specific_needs(self, full_assessment):
        needs = full_assessment["role_specific_needs"]
        assert isinstance(needs, list)
        assert len(needs) > 0

    def test_risk_summary_is_non_empty_string(self, full_assessment):
        assert isinstance(full_assessment["risk_summary"], str)
        assert len(full_assessment["risk_summary"]) > 0

    def test_responsible_use_note_is_present(self, full_assessment):
        note = full_assessment["responsible_use_note"]
        assert isinstance(note, str)
        assert len(note) > 0

    def test_responsible_use_note_mentions_synthetic(self, full_assessment):
        note = full_assessment["responsible_use_note"].lower()
        assert "synthetic" in note

    def test_responsible_use_note_mentions_no_real_data(self, full_assessment):
        note = full_assessment["responsible_use_note"].lower()
        assert "learner data" in note or "personal data" in note

    def test_empty_scenario_does_not_crash(self):
        result = generate_training_needs_assessment({})
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_missing_priority_topics_does_not_crash(self):
        scenario = {"organisation_name": "Test Org", "training_goal": "Learn AI"}
        result = generate_training_needs_assessment(scenario)
        assert isinstance(result, dict)

    def test_missing_staff_roles_does_not_crash(self):
        scenario = {
            "organisation_name": "Test Org",
            "priority_topics": ["safe prompting"],
        }
        result = generate_training_needs_assessment(scenario)
        assert isinstance(result, dict)
        assert len(result["role_specific_needs"]) > 0

    def test_high_risk_topics_appear_in_high_priority(self, full_assessment):
        high_topics = [
            t["topic"] for t in full_assessment["topic_assessments"]
            if t["priority_level"] == "high"
        ]
        assert "safe prompting" in high_topics or "learner data boundaries" in high_topics


# ── summarise_training_needs ───────────────────────────────────────────────────

class TestSummariseTrainingNeeds:
    def test_returns_dict(self, full_assessment):
        result = summarise_training_needs(full_assessment)
        assert isinstance(result, dict)

    def test_required_keys_present(self, full_assessment):
        result = summarise_training_needs(full_assessment)
        required = [
            "organisation_name",
            "staff_role_count",
            "priority_topic_count",
            "high_priority_count",
            "medium_priority_count",
            "learning_outcome_count",
            "recommended_session_type",
            "overall_training_focus",
        ]
        for key in required:
            assert key in result, f"Key '{key}' missing from summary"

    def test_high_priority_count_is_non_negative(self, full_assessment):
        result = summarise_training_needs(full_assessment)
        assert result["high_priority_count"] >= 0

    def test_counts_match_assessment(self, brightpath, full_assessment):
        result = summarise_training_needs(full_assessment)
        assert result["priority_topic_count"] == len(brightpath["priority_topics"])
        assert result["staff_role_count"] == len(brightpath["staff_roles"])

    def test_empty_assessment_returns_zeros(self):
        result = summarise_training_needs({})
        assert result["high_priority_count"] == 0
        assert result["priority_topic_count"] == 0


# ── generate_learning_outcomes ─────────────────────────────────────────────────

class TestGenerateLearningOutcomes:
    def test_returns_list(self, brightpath):
        result = generate_learning_outcomes(brightpath, brightpath["priority_topics"])
        assert isinstance(result, list)

    def test_returns_at_least_3_outcomes(self, brightpath):
        result = generate_learning_outcomes(brightpath, brightpath["priority_topics"])
        assert len(result) >= 3

    def test_returns_at_most_8_outcomes(self, brightpath):
        result = generate_learning_outcomes(brightpath, brightpath["priority_topics"])
        assert len(result) <= 8

    def test_all_outcomes_are_non_empty_strings(self, brightpath):
        result = generate_learning_outcomes(brightpath, brightpath["priority_topics"])
        for outcome in result:
            assert isinstance(outcome, str)
            assert len(outcome) > 0

    def test_empty_topics_returns_defaults(self, brightpath):
        result = generate_learning_outcomes(brightpath, [])
        assert isinstance(result, list)
        assert len(result) > 0


# ── generate_role_specific_needs ──────────────────────────────────────────────

class TestGenerateRoleSpecificNeeds:
    def test_returns_list(self, brightpath):
        result = generate_role_specific_needs(brightpath)
        assert isinstance(result, list)

    def test_non_empty_for_brightpath(self, brightpath):
        result = generate_role_specific_needs(brightpath)
        assert len(result) > 0

    def test_each_entry_has_required_keys(self, brightpath):
        result = generate_role_specific_needs(brightpath)
        for entry in result:
            assert "role" in entry
            assert "key_risks" in entry
            assert "training_focus" in entry
            assert "practical_guidance" in entry

    def test_tutors_entry_present_for_brightpath(self, brightpath):
        result = generate_role_specific_needs(brightpath)
        roles = [r["role"].lower() for r in result]
        assert "tutors" in roles

    def test_empty_roles_returns_fallback(self):
        scenario = {"organisation_name": "Test", "staff_roles": []}
        result = generate_role_specific_needs(scenario)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_unknown_role_returns_generic_entry(self):
        scenario = {"staff_roles": ["data analysts"]}
        result = generate_role_specific_needs(scenario)
        assert len(result) == 1
        assert isinstance(result[0]["training_focus"], str)


# ── format_needs_assessment_as_markdown ───────────────────────────────────────

class TestFormatNeedsAssessmentAsMarkdown:
    def test_returns_string(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert isinstance(result, str)

    def test_non_empty(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert len(result) > 0

    def test_starts_with_heading(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert result.startswith("# Training Needs Assessment")

    def test_contains_training_needs_assessment_heading(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "# Training Needs Assessment" in result

    def test_contains_organisation_section(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "## Organisation" in result

    def test_contains_priority_topics_section(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "## Priority Topics" in result

    def test_contains_learning_outcomes_section(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "## Recommended Learning Outcomes" in result

    def test_contains_role_specific_section(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "## Role-Specific Training Needs" in result

    def test_contains_risk_summary_section(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "## Risk Summary" in result

    def test_contains_responsible_use_section(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "## Responsible Use Boundaries" in result

    def test_responsible_use_section_contains_synthetic(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert "synthetic" in result.lower()

    def test_contains_organisation_name(self, full_assessment):
        result = format_needs_assessment_as_markdown(full_assessment)
        assert full_assessment["organisation_name"] in result

    def test_empty_assessment_does_not_crash(self):
        result = format_needs_assessment_as_markdown({})
        assert isinstance(result, str)
        assert len(result) > 0
