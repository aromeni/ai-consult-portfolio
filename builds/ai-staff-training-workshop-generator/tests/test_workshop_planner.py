"""Tests for src/workshop_planner.py — Phase 3."""

import pytest
from src.workshop_planner import (
    normalise_duration_to_minutes,
    create_workshop_title,
    get_default_workshop_resources,
    get_default_workshop_ground_rules,
    generate_learning_outcome_section,
    generate_timed_agenda,
    generate_trainer_notes,
    generate_discussion_prompts,
    generate_follow_up_actions,
    generate_workshop_plan,
    summarise_workshop_plan,
    format_workshop_plan_as_markdown,
    create_workshop_plan_filename,
)
from src.sample_data import get_brightpath_training_scenario
from src.needs_assessment import generate_training_needs_assessment


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def brightpath():
    return get_brightpath_training_scenario()


@pytest.fixture
def assessment(brightpath):
    return generate_training_needs_assessment(brightpath)


@pytest.fixture
def plan(brightpath, assessment):
    return generate_workshop_plan(brightpath, assessment=assessment)


# ── normalise_duration_to_minutes ──────────────────────────────────────────────

class TestNormaliseDurationToMinutes:
    def test_integer_90(self):
        assert normalise_duration_to_minutes(90) == 90

    def test_integer_60(self):
        assert normalise_duration_to_minutes(60) == 60

    def test_string_90_minutes(self):
        assert normalise_duration_to_minutes("90 minutes") == 90

    def test_string_60_minutes(self):
        assert normalise_duration_to_minutes("60 minutes") == 60

    def test_string_120_minutes(self):
        assert normalise_duration_to_minutes("120 minutes") == 120

    def test_string_90_mins(self):
        assert normalise_duration_to_minutes("90 mins") == 90

    def test_string_1_hour(self):
        assert normalise_duration_to_minutes("1 hour") == 60

    def test_string_2_hours(self):
        assert normalise_duration_to_minutes("2 hours") == 120

    def test_string_1_hour_30_minutes(self):
        assert normalise_duration_to_minutes("1 hour 30 minutes") == 90

    def test_float_1_point_5_hours(self):
        assert normalise_duration_to_minutes("1.5 hours") == 90

    def test_none_defaults_to_90(self):
        assert normalise_duration_to_minutes(None) == 90

    def test_zero_defaults_to_90(self):
        assert normalise_duration_to_minutes(0) == 90

    def test_negative_defaults_to_90(self):
        assert normalise_duration_to_minutes(-10) == 90

    def test_invalid_string_defaults_to_90(self):
        assert normalise_duration_to_minutes("half a day") == 90

    def test_empty_string_defaults_to_90(self):
        assert normalise_duration_to_minutes("") == 90

    def test_returns_int(self):
        result = normalise_duration_to_minutes(90)
        assert isinstance(result, int)


# ── create_workshop_title ──────────────────────────────────────────────────────

class TestCreateWorkshopTitle:
    def test_returns_string(self, brightpath):
        result = create_workshop_title(brightpath)
        assert isinstance(result, str)

    def test_non_empty(self, brightpath):
        result = create_workshop_title(brightpath)
        assert len(result) > 0

    def test_education_sector_returns_lesson_title(self, brightpath):
        result = create_workshop_title(brightpath)
        assert "lesson" in result.lower() or "planning" in result.lower()

    def test_custom_sector_returns_org_name(self):
        scenario = {
            "organisation_name": "Acme Corp",
            "training_goal": "Improve staff safety",
            "sector": "manufacturing",
        }
        result = create_workshop_title(scenario)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_scenario_does_not_crash(self):
        result = create_workshop_title({})
        assert isinstance(result, str)
        assert len(result) > 0


# ── get_default_workshop_resources ────────────────────────────────────────────

class TestGetDefaultWorkshopResources:
    def test_returns_list(self):
        result = get_default_workshop_resources()
        assert isinstance(result, list)

    def test_non_empty(self):
        result = get_default_workshop_resources()
        assert len(result) > 0

    def test_all_strings(self):
        result = get_default_workshop_resources()
        for item in result:
            assert isinstance(item, str)
            assert len(item) > 0

    def test_in_person_includes_flip_chart(self):
        result = get_default_workshop_resources("In-person workshop")
        combined = " ".join(result).lower()
        assert "flip chart" in combined or "whiteboard" in combined

    def test_online_includes_video(self):
        result = get_default_workshop_resources("Online workshop")
        combined = " ".join(result).lower()
        assert "video" in combined or "conferencing" in combined

    def test_hybrid_returns_non_empty(self):
        result = get_default_workshop_resources("Hybrid workshop")
        assert len(result) > 0


# ── get_default_workshop_ground_rules ─────────────────────────────────────────

class TestGetDefaultWorkshopGroundRules:
    def test_returns_list(self):
        result = get_default_workshop_ground_rules()
        assert isinstance(result, list)

    def test_non_empty(self):
        result = get_default_workshop_ground_rules()
        assert len(result) > 0

    def test_all_strings(self):
        result = get_default_workshop_ground_rules()
        for item in result:
            assert isinstance(item, str)
            assert len(item) > 0

    def test_contains_confidentiality_rule(self):
        result = get_default_workshop_ground_rules()
        combined = " ".join(result).lower()
        assert "confidential" in combined


# ── generate_learning_outcome_section ─────────────────────────────────────────

class TestGenerateLearningOutcomeSection:
    def test_returns_list(self, brightpath):
        result = generate_learning_outcome_section(brightpath)
        assert isinstance(result, list)

    def test_non_empty(self, brightpath):
        result = generate_learning_outcome_section(brightpath)
        assert len(result) > 0

    def test_at_most_8(self, brightpath):
        result = generate_learning_outcome_section(brightpath)
        assert len(result) <= 8

    def test_uses_assessment_outcomes_when_available(self, brightpath, assessment):
        result = generate_learning_outcome_section(brightpath, assessment=assessment)
        assert result == assessment["recommended_learning_outcomes"]

    def test_all_strings(self, brightpath):
        result = generate_learning_outcome_section(brightpath)
        for item in result:
            assert isinstance(item, str)
            assert len(item) > 0

    def test_empty_scenario_returns_defaults(self):
        result = generate_learning_outcome_section({})
        assert isinstance(result, list)
        assert len(result) > 0


# ── generate_timed_agenda ──────────────────────────────────────────────────────

class TestGenerateTimedAgenda:
    def test_returns_list(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        assert isinstance(result, list)

    def test_non_empty(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        assert len(result) > 0

    def test_has_7_sections(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        assert len(result) == 7

    def test_each_item_has_required_keys(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        required = {
            "time_range", "section_title", "purpose",
            "trainer_activity", "participant_activity", "key_message",
        }
        for item in result:
            for key in required:
                assert key in item, f"Agenda item missing key '{key}'"

    def test_time_ranges_are_strings(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        for item in result:
            assert isinstance(item["time_range"], str)
            assert "-" in item["time_range"]

    def test_materials_is_list(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        for item in result:
            assert isinstance(item["materials"], list)

    def test_60_minute_agenda(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=60)
        assert len(result) == 7
        # verify total time roughly sums to 60
        def parse_end(time_range):
            end = time_range.split("-")[1]
            h, m = map(int, end.split(":"))
            return h * 60 + m
        last_end = parse_end(result[-1]["time_range"])
        assert 55 <= last_end <= 65

    def test_120_minute_agenda(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=120)
        assert len(result) == 7
        def parse_end(time_range):
            end = time_range.split("-")[1]
            h, m = map(int, end.split(":"))
            return h * 60 + m
        last_end = parse_end(result[-1]["time_range"])
        assert 115 <= last_end <= 125

    def test_90_minute_agenda_ends_near_90(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        def parse_end(time_range):
            end = time_range.split("-")[1]
            h, m = map(int, end.split(":"))
            return h * 60 + m
        last_end = parse_end(result[-1]["time_range"])
        assert 85 <= last_end <= 95

    def test_zero_duration_falls_back(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=0)
        assert isinstance(result, list)
        assert len(result) == 7

    def test_section_titles_are_non_empty_strings(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        for item in result:
            assert isinstance(item["section_title"], str)
            assert len(item["section_title"]) > 0

    def test_first_section_is_welcome(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        assert "Welcome" in result[0]["section_title"] or "welcome" in result[0]["section_title"].lower()

    def test_last_section_is_close(self, brightpath):
        result = generate_timed_agenda(brightpath, duration_minutes=90)
        last = result[-1]["section_title"].lower()
        assert "commit" in last or "next step" in last or "close" in last or "question" in last


# ── generate_workshop_plan ────────────────────────────────────────────────────

class TestGenerateWorkshopPlan:
    def test_returns_dict(self, brightpath):
        result = generate_workshop_plan(brightpath)
        assert isinstance(result, dict)

    def test_required_keys_present(self, plan):
        required = [
            "workshop_title", "organisation_name", "audience",
            "duration_minutes", "delivery_mode", "training_goal",
            "learning_outcomes", "agenda", "resources_needed",
            "ground_rules", "trainer_notes", "discussion_prompts",
            "responsible_use_messages", "expected_outputs",
            "follow_up_actions", "prototype_note",
        ]
        for key in required:
            assert key in plan, f"Key '{key}' missing from workshop plan"

    def test_organisation_name_matches(self, brightpath, plan):
        assert plan["organisation_name"] == brightpath["organisation_name"]

    def test_default_duration_is_90(self, brightpath):
        result = generate_workshop_plan(brightpath)
        assert result["duration_minutes"] == 90

    def test_custom_duration_applied(self, brightpath):
        result = generate_workshop_plan(brightpath, duration_minutes=60)
        assert result["duration_minutes"] == 60

    def test_custom_delivery_mode_applied(self, brightpath):
        result = generate_workshop_plan(brightpath, delivery_mode="Online workshop")
        assert result["delivery_mode"] == "Online workshop"

    def test_agenda_is_non_empty_list(self, plan):
        assert isinstance(plan["agenda"], list)
        assert len(plan["agenda"]) > 0

    def test_learning_outcomes_is_non_empty_list(self, plan):
        assert isinstance(plan["learning_outcomes"], list)
        assert len(plan["learning_outcomes"]) > 0

    def test_responsible_use_messages_non_empty(self, plan):
        assert isinstance(plan["responsible_use_messages"], list)
        assert len(plan["responsible_use_messages"]) > 0

    def test_prototype_note_mentions_synthetic(self, plan):
        assert "synthetic" in plan["prototype_note"].lower()

    def test_handles_missing_assessment(self, brightpath):
        result = generate_workshop_plan(brightpath, assessment=None)
        assert isinstance(result, dict)
        assert len(result["agenda"]) > 0

    def test_empty_scenario_does_not_crash(self):
        result = generate_workshop_plan({})
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"
        assert result["duration_minutes"] == 90

    def test_audience_is_list(self, plan):
        assert isinstance(plan["audience"], list)

    def test_follow_up_actions_non_empty(self, plan):
        assert isinstance(plan["follow_up_actions"], list)
        assert len(plan["follow_up_actions"]) > 0


# ── summarise_workshop_plan ───────────────────────────────────────────────────

class TestSummariseWorkshopPlan:
    def test_returns_dict(self, plan):
        result = summarise_workshop_plan(plan)
        assert isinstance(result, dict)

    def test_required_keys_present(self, plan):
        result = summarise_workshop_plan(plan)
        required = [
            "workshop_title", "organisation_name", "duration_minutes",
            "delivery_mode", "audience_count", "agenda_section_count",
            "learning_outcome_count", "follow_up_action_count",
        ]
        for key in required:
            assert key in result, f"Key '{key}' missing from summary"

    def test_duration_matches_plan(self, plan):
        result = summarise_workshop_plan(plan)
        assert result["duration_minutes"] == plan["duration_minutes"]

    def test_agenda_count_matches(self, plan):
        result = summarise_workshop_plan(plan)
        assert result["agenda_section_count"] == len(plan["agenda"])

    def test_learning_outcome_count_matches(self, plan):
        result = summarise_workshop_plan(plan)
        assert result["learning_outcome_count"] == len(plan["learning_outcomes"])

    def test_empty_plan_returns_zeros(self):
        result = summarise_workshop_plan({})
        assert result["agenda_section_count"] == 0
        assert result["duration_minutes"] == 0


# ── format_workshop_plan_as_markdown ─────────────────────────────────────────

class TestFormatWorkshopPlanAsMarkdown:
    def test_returns_string(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert isinstance(result, str)

    def test_non_empty(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert len(result) > 0

    def test_starts_with_heading(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert result.startswith("# AI Staff Training Workshop Plan")

    def test_contains_timed_agenda_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Timed Agenda" in result

    def test_contains_learning_outcomes_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Learning Outcomes" in result

    def test_contains_responsible_use_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Responsible Use Messages" in result

    def test_contains_trainer_notes_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Trainer Notes" in result

    def test_contains_discussion_prompts_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Discussion Prompts" in result

    def test_contains_follow_up_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Follow-Up Actions" in result

    def test_contains_prototype_boundaries_section(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "## Prototype and Responsible-Use Boundaries" in result

    def test_responsible_use_messages_section_mentions_synthetic(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert "synthetic" in result.lower()

    def test_contains_organisation_name(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert plan["organisation_name"] in result

    def test_contains_workshop_title(self, plan):
        result = format_workshop_plan_as_markdown(plan)
        assert plan["workshop_title"] in result

    def test_empty_plan_does_not_crash(self):
        result = format_workshop_plan_as_markdown({})
        assert isinstance(result, str)
        assert len(result) > 0


# ── create_workshop_plan_filename ─────────────────────────────────────────────

class TestCreateWorkshopPlanFilename:
    def test_returns_string(self):
        result = create_workshop_plan_filename("Using AI Safely for Lesson Planning")
        assert isinstance(result, str)

    def test_starts_with_workshop_plan(self):
        result = create_workshop_plan_filename("Safe AI Workshop")
        assert result.startswith("workshop-plan-")

    def test_ends_with_md(self):
        result = create_workshop_plan_filename("Safe AI Workshop")
        assert result.endswith(".md")

    def test_lowercase(self):
        result = create_workshop_plan_filename("Safe AI Workshop")
        assert result == result.lower()

    def test_no_spaces(self):
        result = create_workshop_plan_filename("Safe AI Workshop")
        assert " " not in result

    def test_special_characters_removed(self):
        result = create_workshop_plan_filename("Using AI: Safely & Responsibly!")
        assert ":" not in result
        assert "!" not in result
        assert "&" not in result

    def test_empty_title_does_not_crash(self):
        result = create_workshop_plan_filename("")
        assert isinstance(result, str)
        assert result.endswith(".md")
