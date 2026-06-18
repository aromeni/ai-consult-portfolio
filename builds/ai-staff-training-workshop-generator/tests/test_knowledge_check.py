"""Tests for src/knowledge_check.py — Phase 7: Knowledge Check Generator."""

import pytest
from src import knowledge_check as kc


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def scenario():
    return {
        "organisation_name": "BrightPath Skills Training",
        "organisation_type": "Private training provider",
        "sector": "Education and training",
        "staff_count": 8,
        "staff_roles": ["Tutors", "Administrators", "Team Leaders", "Quality Lead"],
        "main_concerns": [
            "Learner data", "Safeguarding", "Hallucination", "Bias",
            "Data protection", "Policy alignment",
        ],
        "priority_topics": [
            "Safe Prompting",
            "Learner Data and Privacy",
            "Safeguarding and AI",
            "Hallucination and Accuracy",
            "Bias and Fairness",
        ],
        "training_goal": "Equip all staff with practical responsible AI safe-use skills.",
        "current_ai_use": "Informal ChatGPT use for lesson planning and emails.",
        "country_context": "England",
    }


@pytest.fixture
def minimal_scenario():
    return {"organisation_name": "Acme Ltd"}


@pytest.fixture
def assessment():
    return {
        "topic_assessments": [
            {
                "title": "Hallucination and Accuracy",
                "priority_level": "high",
                "risk_level": "high",
                "training_need": "Staff must verify AI outputs.",
            },
            {
                "title": "Bias and Fairness",
                "priority_level": "high",
                "risk_level": "high",
                "training_need": "Staff must check for bias.",
            },
            {
                "title": "Safe Prompting",
                "priority_level": "high",
                "risk_level": "medium",
                "training_need": "Staff must write safe prompts.",
            },
        ],
        "recommended_learning_outcomes": [
            "Identify safe vs unsafe prompts.",
            "Apply human review before using AI outputs.",
        ],
    }


@pytest.fixture
def workshop_plan():
    return {
        "workshop_title": "Responsible AI for BrightPath Staff",
        "duration_minutes": 90,
    }


@pytest.fixture
def activities():
    return [
        {
            "activity_id": "safe_unsafe_prompt_sorting",
            "activity_title": "Safe vs Unsafe Prompt Sorting",
            "activity_type": "safe_unsafe_prompt_sorting",
        },
    ]


@pytest.fixture
def full_check(scenario, assessment, workshop_plan, activities):
    return kc.generate_knowledge_check(
        scenario,
        assessment=assessment,
        workshop_plan=workshop_plan,
        activities=activities,
        question_count=10,
    )


# ── TestGetDefaultQuestionTopics ──────────────────────────────────────────────

class TestGetDefaultQuestionTopics:
    def test_returns_list(self):
        result = kc.get_default_question_topics()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(kc.get_default_question_topics()) > 0

    def test_all_strings(self):
        for topic in kc.get_default_question_topics():
            assert isinstance(topic, str)

    def test_contains_safe_prompting(self):
        topics = kc.get_default_question_topics()
        assert any("prompting" in t.lower() or "prompt" in t.lower() for t in topics)

    def test_contains_safeguarding(self):
        topics = kc.get_default_question_topics()
        assert any("safeguarding" in t.lower() for t in topics)

    def test_contains_human_review(self):
        topics = kc.get_default_question_topics()
        assert any("human" in t.lower() or "review" in t.lower() for t in topics)


# ── TestGenerateMultipleChoiceQuestions ───────────────────────────────────────

class TestGenerateMultipleChoiceQuestions:
    def test_returns_list(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(kc.generate_multiple_choice_questions(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in kc.generate_multiple_choice_questions(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in kc.generate_multiple_choice_questions(scenario):
            assert "question_id" in item
            assert "topic" in item
            assert "question" in item
            assert "options" in item
            assert "correct_answer" in item
            assert "explanation" in item

    def test_options_is_dict_with_abcd(self, scenario):
        for item in kc.generate_multiple_choice_questions(scenario):
            opts = item["options"]
            assert isinstance(opts, dict)
            assert "A" in opts
            assert "B" in opts
            assert "C" in opts
            assert "D" in opts

    def test_correct_answer_in_options(self, scenario):
        for item in kc.generate_multiple_choice_questions(scenario):
            assert item["correct_answer"] in item["options"]

    def test_question_count_10(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario, question_count=10)
        assert len(result) == 10

    def test_question_count_5(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario, question_count=5)
        assert len(result) == 5

    def test_question_count_15(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario, question_count=15)
        assert len(result) == 15

    def test_invalid_question_count_defaults_to_10(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario, question_count=0)
        assert len(result) == 10

    def test_negative_question_count_defaults_to_10(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario, question_count=-3)
        assert len(result) == 10

    def test_question_ids_are_strings(self, scenario):
        for item in kc.generate_multiple_choice_questions(scenario):
            assert isinstance(item["question_id"], str)

    def test_with_assessment(self, scenario, assessment):
        result = kc.generate_multiple_choice_questions(scenario, assessment=assessment)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_with_none_assessment(self, scenario):
        result = kc.generate_multiple_choice_questions(scenario, assessment=None)
        assert isinstance(result, list)


# ── TestGenerateScenarioQuestions ─────────────────────────────────────────────

class TestGenerateScenarioQuestions:
    def test_returns_list(self, scenario):
        result = kc.generate_scenario_questions(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(kc.generate_scenario_questions(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in kc.generate_scenario_questions(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in kc.generate_scenario_questions(scenario):
            assert "question_id" in item
            assert "topic" in item
            assert "scenario" in item
            assert "question" in item
            assert "expected_answer_points" in item
            assert "risk_flags" in item
            assert "model_answer" in item

    def test_expected_answer_points_is_list(self, scenario):
        for item in kc.generate_scenario_questions(scenario):
            assert isinstance(item["expected_answer_points"], list)
            assert len(item["expected_answer_points"]) > 0

    def test_risk_flags_is_list(self, scenario):
        for item in kc.generate_scenario_questions(scenario):
            assert isinstance(item["risk_flags"], list)
            assert len(item["risk_flags"]) > 0

    def test_includes_safeguarding_scenario(self, scenario):
        result = kc.generate_scenario_questions(scenario)
        topics = [q["topic"].lower() for q in result]
        assert any("safeguarding" in t for t in topics)

    def test_includes_learner_data_scenario(self, scenario):
        result = kc.generate_scenario_questions(scenario)
        topics = [q["topic"].lower() for q in result]
        assert any("learner" in t or "data" in t for t in topics)

    def test_with_none_assessment(self, scenario):
        result = kc.generate_scenario_questions(scenario, assessment=None)
        assert isinstance(result, list)

    def test_with_none_activities(self, scenario):
        result = kc.generate_scenario_questions(scenario, activities=None)
        assert isinstance(result, list)


# ── TestGenerateShortReflectionQuestions ──────────────────────────────────────

class TestGenerateShortReflectionQuestions:
    def test_returns_list(self, scenario):
        result = kc.generate_short_reflection_questions(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(kc.generate_short_reflection_questions(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in kc.generate_short_reflection_questions(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in kc.generate_short_reflection_questions(scenario):
            assert "question_id" in item
            assert "topic" in item
            assert "question" in item
            assert "guidance_points" in item

    def test_guidance_points_is_list(self, scenario):
        for item in kc.generate_short_reflection_questions(scenario):
            assert isinstance(item["guidance_points"], list)
            assert len(item["guidance_points"]) > 0

    def test_with_assessment_enrichment(self, scenario, assessment):
        result = kc.generate_short_reflection_questions(scenario, assessment)
        assert isinstance(result, list)
        assert len(result) >= len(kc.generate_short_reflection_questions(scenario))

    def test_with_none_assessment(self, scenario):
        result = kc.generate_short_reflection_questions(scenario, assessment=None)
        assert isinstance(result, list)


# ── TestGenerateAnswerKey ─────────────────────────────────────────────────────

class TestGenerateAnswerKey:
    def test_returns_dict(self, scenario):
        mcqs = kc.generate_multiple_choice_questions(scenario)
        scenarios = kc.generate_scenario_questions(scenario)
        reflections = kc.generate_short_reflection_questions(scenario)
        result = kc.generate_answer_key(mcqs, scenarios, reflections)
        assert isinstance(result, dict)

    def test_expected_keys(self, scenario):
        mcqs = kc.generate_multiple_choice_questions(scenario)
        scenarios = kc.generate_scenario_questions(scenario)
        reflections = kc.generate_short_reflection_questions(scenario)
        result = kc.generate_answer_key(mcqs, scenarios, reflections)
        assert "multiple_choice_answers" in result
        assert "scenario_answer_guidance" in result
        assert "reflection_guidance" in result
        assert "marking_note" in result

    def test_mcq_answers_count_matches_input(self, scenario):
        mcqs = kc.generate_multiple_choice_questions(scenario, question_count=5)
        result = kc.generate_answer_key(mcqs, [], [])
        assert len(result["multiple_choice_answers"]) == 5

    def test_marking_note_is_string(self, scenario):
        result = kc.generate_answer_key([], [], [])
        assert isinstance(result["marking_note"], str)
        assert len(result["marking_note"]) > 0

    def test_mcq_answers_include_correct_answer(self, scenario):
        mcqs = kc.generate_multiple_choice_questions(scenario)
        result = kc.generate_answer_key(mcqs, [], [])
        for answer in result["multiple_choice_answers"]:
            assert "correct_answer" in answer

    def test_scenario_guidance_includes_model_answer(self, scenario):
        scenarios = kc.generate_scenario_questions(scenario)
        result = kc.generate_answer_key([], scenarios, [])
        for guidance in result["scenario_answer_guidance"]:
            assert "model_answer" in guidance

    def test_empty_inputs(self):
        result = kc.generate_answer_key([], [], [])
        assert result["multiple_choice_answers"] == []
        assert result["scenario_answer_guidance"] == []
        assert result["reflection_guidance"] == []


# ── TestGenerateKnowledgeCheck ────────────────────────────────────────────────

class TestGenerateKnowledgeCheck:
    def test_returns_dict(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert isinstance(result, dict)

    def test_expected_keys(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        expected_keys = [
            "knowledge_check_title",
            "organisation_name",
            "audience",
            "purpose",
            "instructions",
            "multiple_choice_questions",
            "scenario_questions",
            "reflection_questions",
            "answer_key",
            "pass_guidance",
            "review_guidance",
            "responsible_use_warning",
            "prototype_note",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_title_is_correct(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert result["knowledge_check_title"] == "Responsible AI Staff Knowledge Check"

    def test_organisation_name(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert result["organisation_name"] == scenario["organisation_name"]

    def test_audience_is_list(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert isinstance(result["audience"], list)

    def test_audience_populated(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert len(result["audience"]) > 0

    def test_mcq_count_respects_question_count(self, scenario):
        result = kc.generate_knowledge_check(scenario, question_count=5)
        assert len(result["multiple_choice_questions"]) == 5

    def test_mcq_count_default_10(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert len(result["multiple_choice_questions"]) == 10

    def test_scenario_questions_non_empty(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert len(result["scenario_questions"]) > 0

    def test_reflection_questions_non_empty(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert len(result["reflection_questions"]) > 0

    def test_answer_key_is_dict(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert isinstance(result["answer_key"], dict)

    def test_prototype_note_present(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert len(result["prototype_note"]) > 0

    def test_responsible_use_warning_present(self, scenario):
        result = kc.generate_knowledge_check(scenario)
        assert len(result["responsible_use_warning"]) > 0

    def test_handles_none_assessment(self, scenario):
        result = kc.generate_knowledge_check(scenario, assessment=None)
        assert isinstance(result, dict)

    def test_handles_none_workshop_plan(self, scenario):
        result = kc.generate_knowledge_check(scenario, workshop_plan=None)
        assert isinstance(result, dict)

    def test_handles_none_activities(self, scenario):
        result = kc.generate_knowledge_check(scenario, activities=None)
        assert isinstance(result, dict)

    def test_handles_none_facilitator_guide(self, scenario):
        result = kc.generate_knowledge_check(scenario, facilitator_guide=None)
        assert isinstance(result, dict)

    def test_handles_none_handout(self, scenario):
        result = kc.generate_knowledge_check(scenario, handout=None)
        assert isinstance(result, dict)

    def test_handles_none_scenario(self):
        result = kc.generate_knowledge_check(None)
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_empty_scenario(self):
        result = kc.generate_knowledge_check({})
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_invalid_question_count(self, scenario):
        result = kc.generate_knowledge_check(scenario, question_count=0)
        assert len(result["multiple_choice_questions"]) == 10

    def test_handles_missing_staff_roles(self, scenario):
        s = {**scenario, "staff_roles": []}
        result = kc.generate_knowledge_check(s)
        assert isinstance(result["audience"], list)
        assert len(result["audience"]) > 0

    def test_workshop_plan_referenced_in_purpose(self, scenario, workshop_plan):
        result = kc.generate_knowledge_check(scenario, workshop_plan=workshop_plan)
        assert workshop_plan["workshop_title"] in result["purpose"]

    def test_full_generation(self, scenario, assessment, workshop_plan, activities):
        result = kc.generate_knowledge_check(
            scenario,
            assessment=assessment,
            workshop_plan=workshop_plan,
            activities=activities,
            question_count=10,
        )
        assert isinstance(result, dict)
        assert len(result["multiple_choice_questions"]) == 10

    def test_pass_guidance_mentions_threshold(self, scenario):
        result = kc.generate_knowledge_check(scenario, question_count=10)
        assert "10" in result["pass_guidance"]


# ── TestSummariseKnowledgeCheck ───────────────────────────────────────────────

class TestSummariseKnowledgeCheck:
    def test_returns_dict(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        assert isinstance(result, dict)

    def test_expected_keys(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        expected = [
            "organisation_name",
            "audience_roles",
            "mcq_count",
            "scenario_question_count",
            "reflection_question_count",
            "answer_key_included",
            "total_question_count",
        ]
        for key in expected:
            assert key in result, f"Missing key: {key}"

    def test_mcq_count_is_int(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        assert isinstance(result["mcq_count"], int)

    def test_mcq_count_matches(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        assert result["mcq_count"] == len(full_check["multiple_choice_questions"])

    def test_total_question_count(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        expected_total = (
            len(full_check["multiple_choice_questions"])
            + len(full_check["scenario_questions"])
            + len(full_check["reflection_questions"])
        )
        assert result["total_question_count"] == expected_total

    def test_answer_key_included_is_bool(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        assert isinstance(result["answer_key_included"], bool)

    def test_answer_key_included_true(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        assert result["answer_key_included"] is True

    def test_organisation_name_correct(self, full_check):
        result = kc.summarise_knowledge_check(full_check)
        assert result["organisation_name"] == full_check["organisation_name"]


# ── TestFormatKnowledgeCheckAsMarkdown ────────────────────────────────────────

class TestFormatKnowledgeCheckAsMarkdown:
    def test_returns_string(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert isinstance(result, str)

    def test_non_empty(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert len(result) > 0

    def test_contains_main_heading(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "# Responsible AI Staff Knowledge Check" in result

    def test_contains_organisation_section(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Organisation" in result

    def test_contains_purpose_section(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Purpose" in result

    def test_contains_instructions(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Instructions" in result

    def test_contains_mcq_section(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Multiple-Choice Questions" in result

    def test_contains_scenario_section(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Scenario Questions" in result

    def test_contains_reflection_section(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Reflection Questions" in result

    def test_contains_answer_key_when_included(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check, include_answer_key=True)
        assert "## Answer Key" in result

    def test_excludes_answer_key_when_not_included(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check, include_answer_key=False)
        assert "## Answer Key" not in result

    def test_contains_pass_guidance_section(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Pass and Review Guidance" in result

    def test_contains_prototype_boundaries(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "## Prototype and Responsible-Use Boundaries" in result

    def test_contains_synthetic_note(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "synthetic" in result.lower()

    def test_org_name_in_output(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert full_check["organisation_name"] in result

    def test_options_abcd_in_mcq_output(self, full_check):
        result = kc.format_knowledge_check_as_markdown(full_check)
        assert "A." in result
        assert "B." in result
        assert "C." in result
        assert "D." in result


# ── TestCreateKnowledgeCheckFilename ──────────────────────────────────────────

class TestCreateKnowledgeCheckFilename:
    def test_returns_string(self):
        result = kc.create_knowledge_check_filename("BrightPath Skills Training")
        assert isinstance(result, str)

    def test_starts_with_knowledge_check(self):
        result = kc.create_knowledge_check_filename("BrightPath Skills Training")
        assert result.startswith("knowledge-check-")

    def test_ends_with_md(self):
        result = kc.create_knowledge_check_filename("BrightPath Skills Training")
        assert result.endswith(".md")

    def test_lowercase(self):
        result = kc.create_knowledge_check_filename("BrightPath Skills Training")
        assert result == result.lower()

    def test_spaces_replaced_with_hyphens(self):
        result = kc.create_knowledge_check_filename("BrightPath Skills Training")
        assert " " not in result

    def test_special_characters_removed(self):
        result = kc.create_knowledge_check_filename("BrightPath & Associates (UK)")
        assert "&" not in result
        assert "(" not in result
        assert ")" not in result

    def test_empty_string(self):
        result = kc.create_knowledge_check_filename("")
        assert result == "knowledge-check-organisation.md"

    def test_single_word(self):
        result = kc.create_knowledge_check_filename("Acme")
        assert result == "knowledge-check-acme.md"
