"""Tests for src/activity_generator.py — Phase 4.

All tests use synthetic data only.
"""

import pytest
from src import activity_generator as ag
from src.sample_data import get_brightpath_training_scenario


# ── Fixtures ────────────────────────────────────────────────────────────────────

@pytest.fixture
def scenario():
    return get_brightpath_training_scenario()


@pytest.fixture
def minimal_scenario():
    return {
        "organisation_name": "Test Org",
        "sector": "training",
        "staff_roles": ["tutors", "administrators"],
        "priority_topics": ["safe prompting"],
        "main_concerns": [],
    }


@pytest.fixture
def empty_scenario():
    return {}


_EXPECTED_ACTIVITY_KEYS = {
    "activity_id",
    "activity_title",
    "activity_type",
    "duration_minutes",
    "target_roles",
    "learning_objective",
    "materials_needed",
    "instructions_for_trainer",
    "instructions_for_participants",
    "activity_steps",
    "scenario_cards",
    "expected_answers",
    "debrief_questions",
    "key_takeaways",
    "risk_warnings",
    "responsible_use_note",
}


# ── Catalogue ────────────────────────────────────────────────────────────────────

class TestCatalogue:
    def test_returns_dict(self):
        assert isinstance(ag.get_activity_type_catalogue(), dict)

    def test_contains_expected_types(self):
        cat = ag.get_activity_type_catalogue()
        expected = {
            "safe_unsafe_prompt_sorting",
            "risky_prompt_rewrite",
            "hallucination_review",
            "learner_data_boundary",
            "safeguarding_escalation",
            "human_review_checklist",
            "approved_tools_decision",
            "bias_fairness_review",
        }
        assert expected.issubset(set(cat.keys()))

    def test_each_entry_has_required_keys(self):
        cat = ag.get_activity_type_catalogue()
        for activity_id, info in cat.items():
            assert "title" in info, f"Missing title in {activity_id}"
            assert "type" in info, f"Missing type in {activity_id}"
            assert "recommended_duration" in info, f"Missing recommended_duration in {activity_id}"
            assert "description" in info, f"Missing description in {activity_id}"

    def test_recommended_durations_are_positive(self):
        cat = ag.get_activity_type_catalogue()
        for activity_id, info in cat.items():
            assert info["recommended_duration"] > 0, f"Duration must be positive: {activity_id}"

    def test_titles_are_strings(self):
        cat = ag.get_activity_type_catalogue()
        for activity_id, info in cat.items():
            assert isinstance(info["title"], str)
            assert len(info["title"]) > 0


class TestDefaultActivityTypes:
    def test_returns_list(self):
        assert isinstance(ag.get_default_activity_types(), list)

    def test_returns_non_empty_list(self):
        assert len(ag.get_default_activity_types()) > 0

    def test_all_defaults_in_catalogue(self):
        cat = ag.get_activity_type_catalogue()
        for activity_type in ag.get_default_activity_types():
            assert activity_type in cat

    def test_includes_core_defaults(self):
        defaults = ag.get_default_activity_types()
        assert "safe_unsafe_prompt_sorting" in defaults
        assert "safeguarding_escalation" in defaults
        assert "human_review_checklist" in defaults


# ── Individual activity creators ─────────────────────────────────────────────────

class TestSafeUnsafePromptSorting:
    def test_returns_dict(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert result["activity_id"] == "safe_unsafe_prompt_sorting"

    def test_activity_type_is_sorting(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert result["activity_type"] == "sorting"

    def test_has_scenario_cards(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert len(result["scenario_cards"]) > 0

    def test_scenario_cards_have_classification(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        for card in result["scenario_cards"]:
            assert "classification" in card
            assert card["classification"] in {"SAFE", "RISKY", "PROHIBITED"}

    def test_includes_prohibited_card(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        classifications = [c["classification"] for c in result["scenario_cards"]]
        assert "PROHIBITED" in classifications

    def test_has_responsible_use_note(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert len(result["responsible_use_note"]) > 0

    def test_has_risk_warnings(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        assert len(result["risk_warnings"]) > 0

    def test_works_with_empty_scenario(self, empty_scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(empty_scenario)
        assert isinstance(result, dict)

    def test_works_without_assessment(self, scenario):
        result = ag.create_safe_unsafe_prompt_sorting_activity(scenario, assessment=None)
        assert isinstance(result, dict)


class TestRiskyPromptRewrite:
    def test_returns_dict(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        assert result["activity_id"] == "risky_prompt_rewrite"

    def test_activity_type_is_rewrite(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        assert result["activity_type"] == "rewrite"

    def test_scenario_cards_have_safe_rewrite(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        for card in result["scenario_cards"]:
            assert "safe_rewrite" in card
            assert len(card["safe_rewrite"]) > 0

    def test_scenario_cards_have_original_prompt(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        for card in result["scenario_cards"]:
            assert "original_prompt" in card

    def test_duration_is_15(self, scenario):
        result = ag.create_risky_prompt_rewrite_activity(scenario)
        assert result["duration_minutes"] == 15


class TestHallucinationReview:
    def test_returns_dict(self, scenario):
        result = ag.create_hallucination_review_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_hallucination_review_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_hallucination_review_activity(scenario)
        assert result["activity_id"] == "hallucination_review"

    def test_activity_type_is_review(self, scenario):
        result = ag.create_hallucination_review_activity(scenario)
        assert result["activity_type"] == "review"

    def test_scenario_cards_have_ai_output(self, scenario):
        result = ag.create_hallucination_review_activity(scenario)
        for card in result["scenario_cards"]:
            assert "ai_output" in card
            assert len(card["ai_output"]) > 0

    def test_scenario_cards_have_hallucination_flags(self, scenario):
        result = ag.create_hallucination_review_activity(scenario)
        for card in result["scenario_cards"]:
            assert "hallucination_flags" in card
            assert len(card["hallucination_flags"]) > 0


class TestLearnerDataBoundary:
    def test_returns_dict(self, scenario):
        result = ag.create_learner_data_boundary_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_learner_data_boundary_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_learner_data_boundary_activity(scenario)
        assert result["activity_id"] == "learner_data_boundary"

    def test_activity_type_is_scenario(self, scenario):
        result = ag.create_learner_data_boundary_activity(scenario)
        assert result["activity_type"] == "scenario"

    def test_scenario_cards_have_boundary_rule(self, scenario):
        result = ag.create_learner_data_boundary_activity(scenario)
        for card in result["scenario_cards"]:
            assert "boundary_rule" in card
            assert len(card["boundary_rule"]) > 0


class TestSafeguardingEscalation:
    def test_returns_dict(self, scenario):
        result = ag.create_safeguarding_escalation_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_safeguarding_escalation_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_safeguarding_escalation_activity(scenario)
        assert result["activity_id"] == "safeguarding_escalation"

    def test_correct_action_mentions_dsl(self, scenario):
        result = ag.create_safeguarding_escalation_activity(scenario)
        for card in result["scenario_cards"]:
            assert "DSL" in card.get("correct_action", "") or "safeguarding" in card.get("correct_action", "").lower()

    def test_risk_warnings_mention_safeguarding(self, scenario):
        result = ag.create_safeguarding_escalation_activity(scenario)
        combined = " ".join(result["risk_warnings"]).lower()
        assert "safeguarding" in combined

    def test_key_takeaways_mention_human_led(self, scenario):
        result = ag.create_safeguarding_escalation_activity(scenario)
        combined = " ".join(result["key_takeaways"]).lower()
        assert "human" in combined


class TestHumanReviewChecklist:
    def test_returns_dict(self, scenario):
        result = ag.create_human_review_checklist_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_human_review_checklist_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_human_review_checklist_activity(scenario)
        assert result["activity_id"] == "human_review_checklist"

    def test_activity_type_is_checklist(self, scenario):
        result = ag.create_human_review_checklist_activity(scenario)
        assert result["activity_type"] == "checklist"

    def test_scenario_cards_present(self, scenario):
        result = ag.create_human_review_checklist_activity(scenario)
        assert len(result["scenario_cards"]) > 0


class TestApprovedToolsDecision:
    def test_returns_dict(self, scenario):
        result = ag.create_approved_tools_decision_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_approved_tools_decision_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_approved_tools_decision_activity(scenario)
        assert result["activity_id"] == "approved_tools_decision"

    def test_activity_type_is_decision(self, scenario):
        result = ag.create_approved_tools_decision_activity(scenario)
        assert result["activity_type"] == "decision"

    def test_scenario_cards_have_decision(self, scenario):
        result = ag.create_approved_tools_decision_activity(scenario)
        for card in result["scenario_cards"]:
            assert "decision" in card
            assert card["decision"] in {"APPROVED", "ESCALATE", "STOP"}

    def test_includes_all_three_decisions(self, scenario):
        result = ag.create_approved_tools_decision_activity(scenario)
        decisions = {c["decision"] for c in result["scenario_cards"]}
        assert "APPROVED" in decisions
        assert "ESCALATE" in decisions
        assert "STOP" in decisions


class TestBiasFairnessReview:
    def test_returns_dict(self, scenario):
        result = ag.create_bias_fairness_review_activity(scenario)
        assert isinstance(result, dict)

    def test_has_required_keys(self, scenario):
        result = ag.create_bias_fairness_review_activity(scenario)
        assert _EXPECTED_ACTIVITY_KEYS.issubset(set(result.keys()))

    def test_activity_id(self, scenario):
        result = ag.create_bias_fairness_review_activity(scenario)
        assert result["activity_id"] == "bias_fairness_review"

    def test_scenario_cards_have_bias_flags(self, scenario):
        result = ag.create_bias_fairness_review_activity(scenario)
        for card in result["scenario_cards"]:
            assert "bias_flags" in card
            assert len(card["bias_flags"]) > 0

    def test_scenario_cards_have_fair_rewrite(self, scenario):
        result = ag.create_bias_fairness_review_activity(scenario)
        for card in result["scenario_cards"]:
            assert "fair_rewrite" in card


# ── generate_training_activities ─────────────────────────────────────────────────

class TestGenerateTrainingActivities:
    def test_returns_list(self, scenario):
        result = ag.generate_training_activities(scenario)
        assert isinstance(result, list)

    def test_returns_non_empty_list_with_defaults(self, scenario):
        result = ag.generate_training_activities(scenario)
        assert len(result) > 0

    def test_respects_selected_activity_types(self, scenario):
        result = ag.generate_training_activities(
            scenario,
            selected_activity_types=["safe_unsafe_prompt_sorting"],
        )
        assert len(result) == 1
        assert result[0]["activity_id"] == "safe_unsafe_prompt_sorting"

    def test_ignores_unknown_activity_types(self, scenario):
        result = ag.generate_training_activities(
            scenario,
            selected_activity_types=["safe_unsafe_prompt_sorting", "nonexistent_type"],
        )
        assert len(result) == 1

    def test_empty_selected_types_uses_defaults(self, scenario):
        result = ag.generate_training_activities(scenario, selected_activity_types=[])
        defaults = ag.get_default_activity_types()
        assert len(result) == len(defaults)

    def test_handles_none_assessment(self, scenario):
        result = ag.generate_training_activities(scenario, assessment=None)
        assert isinstance(result, list)

    def test_handles_none_workshop_plan(self, scenario):
        result = ag.generate_training_activities(scenario, workshop_plan=None)
        assert isinstance(result, list)

    def test_handles_empty_scenario(self, empty_scenario):
        result = ag.generate_training_activities(empty_scenario)
        assert isinstance(result, list)

    def test_handles_none_scenario(self):
        result = ag.generate_training_activities(None)
        assert isinstance(result, list)

    def test_all_activities_have_responsible_use_note(self, scenario):
        result = ag.generate_training_activities(scenario)
        for activity in result:
            assert "responsible_use_note" in activity
            assert len(activity["responsible_use_note"]) > 0

    def test_all_activities_have_risk_warnings(self, scenario):
        result = ag.generate_training_activities(scenario)
        for activity in result:
            assert "risk_warnings" in activity
            assert len(activity["risk_warnings"]) > 0

    def test_all_activities_have_required_keys(self, scenario):
        result = ag.generate_training_activities(scenario)
        for activity in result:
            assert _EXPECTED_ACTIVITY_KEYS.issubset(set(activity.keys()))

    def test_all_default_types_generated(self, scenario):
        result = ag.generate_training_activities(scenario)
        generated_ids = {a["activity_id"] for a in result}
        for default_type in ag.get_default_activity_types():
            assert default_type in generated_ids

    def test_full_catalogue_generates_all_types(self, scenario):
        all_types = list(ag.get_activity_type_catalogue().keys())
        result = ag.generate_training_activities(scenario, selected_activity_types=all_types)
        assert len(result) == len(all_types)


# ── summarise_training_activities ────────────────────────────────────────────────

class TestSummariseTrainingActivities:
    def test_returns_dict(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.summarise_training_activities(activities)
        assert isinstance(result, dict)

    def test_has_expected_keys(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.summarise_training_activities(activities)
        assert "activity_count" in result
        assert "estimated_total_minutes" in result
        assert "activity_types" in result
        assert "target_roles" in result

    def test_activity_count_is_correct(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.summarise_training_activities(activities)
        assert result["activity_count"] == len(activities)

    def test_estimated_total_minutes_is_positive(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.summarise_training_activities(activities)
        assert result["estimated_total_minutes"] > 0

    def test_handles_empty_list(self):
        result = ag.summarise_training_activities([])
        assert result["activity_count"] == 0
        assert result["estimated_total_minutes"] == 0

    def test_activity_types_are_list(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.summarise_training_activities(activities)
        assert isinstance(result["activity_types"], list)

    def test_target_roles_are_list(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.summarise_training_activities(activities)
        assert isinstance(result["target_roles"], list)


# ── format_activity_as_markdown ───────────────────────────────────────────────────

class TestFormatActivityAsMarkdown:
    def test_returns_string(self, scenario):
        activity = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        result = ag.format_activity_as_markdown(activity)
        assert isinstance(result, str)

    def test_contains_activity_title(self, scenario):
        activity = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        result = ag.format_activity_as_markdown(activity)
        assert "Safe vs Unsafe Prompt Sorting" in result

    def test_contains_learning_objective(self, scenario):
        activity = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        result = ag.format_activity_as_markdown(activity)
        assert "Learning objective" in result

    def test_contains_trainer_instructions(self, scenario):
        activity = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        result = ag.format_activity_as_markdown(activity)
        assert "Trainer instructions" in result

    def test_contains_debrief_questions(self, scenario):
        activity = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        result = ag.format_activity_as_markdown(activity)
        assert "Debrief questions" in result

    def test_contains_responsible_use_note(self, scenario):
        activity = ag.create_safe_unsafe_prompt_sorting_activity(scenario)
        result = ag.format_activity_as_markdown(activity)
        assert "Responsible use note" in result


# ── format_activities_as_markdown ─────────────────────────────────────────────────

class TestFormatActivitiesAsMarkdown:
    def test_returns_string(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.format_activities_as_markdown(activities)
        assert isinstance(result, str)

    def test_contains_main_heading(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.format_activities_as_markdown(activities)
        assert "# Responsible AI Staff Training Activities" in result

    def test_contains_activity_summary(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.format_activities_as_markdown(activities)
        assert "Activity Summary" in result

    def test_contains_prototype_boundaries(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.format_activities_as_markdown(activities)
        assert "Prototype and Responsible-Use Boundaries" in result

    def test_boundaries_mention_synthetic_data(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.format_activities_as_markdown(activities)
        assert "synthetic" in result.lower()

    def test_handles_empty_activities(self):
        result = ag.format_activities_as_markdown([])
        assert isinstance(result, str)
        assert "No activities generated" in result

    def test_contains_all_activity_titles(self, scenario):
        activities = ag.generate_training_activities(scenario)
        result = ag.format_activities_as_markdown(activities)
        for activity in activities:
            assert activity["activity_title"] in result


# ── create_activities_filename ────────────────────────────────────────────────────

class TestCreateActivitiesFilename:
    def test_returns_string(self):
        assert isinstance(ag.create_activities_filename("BrightPath Skills Training"), str)

    def test_starts_with_prefix(self):
        filename = ag.create_activities_filename("BrightPath Skills Training")
        assert filename.startswith("training-activities-")

    def test_ends_with_md(self):
        filename = ag.create_activities_filename("BrightPath Skills Training")
        assert filename.endswith(".md")

    def test_is_lowercase(self):
        filename = ag.create_activities_filename("BrightPath Skills Training")
        assert filename == filename.lower()

    def test_no_spaces(self):
        filename = ag.create_activities_filename("BrightPath Skills Training")
        assert " " not in filename

    def test_handles_special_characters(self):
        filename = ag.create_activities_filename("Test & Org (UK)")
        assert " " not in filename
        assert "&" not in filename
        assert "(" not in filename

    def test_handles_empty_name(self):
        filename = ag.create_activities_filename("")
        assert filename.endswith(".md")
        assert "training-activities-" in filename

    def test_handles_none_name(self):
        filename = ag.create_activities_filename(None)
        assert filename.endswith(".md")
