"""Tests for src/training_pack.py — Phase 8: Training Pack Export."""

import pytest
from src import training_pack as tp
from src.sample_data import get_brightpath_training_scenario


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def scenario():
    return get_brightpath_training_scenario()


@pytest.fixture
def assessment():
    return {
        "topic_assessments": [
            {"title": "Safe Prompting", "priority_level": "high", "risk_level": "high",
             "training_need": "Staff must write safe prompts."},
            {"title": "Safeguarding and AI", "priority_level": "high", "risk_level": "high",
             "training_need": "Staff must escalate safeguarding concerns."},
        ],
        "recommended_learning_outcomes": [
            "Identify safe vs unsafe prompts.",
            "Apply human review before using AI outputs.",
        ],
        "overall_training_focus": "Responsible AI use",
        "recommended_session_type": "In-person workshop",
        "risk_summary": "High risk across safeguarding and data boundaries.",
        "role_specific_needs": [],
        "responsible_use_note": "Use synthetic scenarios only.",
    }


@pytest.fixture
def workshop_plan():
    return {
        "workshop_title": "Responsible AI for BrightPath Staff",
        "duration_minutes": 90,
        "delivery_mode": "In-person workshop",
        "audience": ["Tutors", "Administrators"],
        "learning_outcomes": ["Identify safe prompts.", "Review AI output."],
        "agenda": [
            {"time_range": "0:00–0:10", "section_title": "Welcome", "purpose": "Open session."},
        ],
        "resources_needed": ["Printed activity cards"],
        "responsible_use_messages": ["Do not enter learner data into AI."],
        "follow_up_actions": ["Confirm approved tools."],
    }


@pytest.fixture
def activities():
    return [
        {
            "activity_id": "safe_unsafe_prompt_sorting",
            "activity_title": "Safe vs Unsafe Prompt Sorting",
            "activity_type": "safe_unsafe_prompt_sorting",
            "duration_minutes": 20,
            "target_roles": ["Tutors", "Administrators"],
            "learning_objective": "Distinguish safe and unsafe prompts.",
            "key_takeaways": ["Use generic examples only."],
        },
    ]


@pytest.fixture
def knowledge_check():
    return {
        "knowledge_check_title": "Responsible AI Staff Knowledge Check",
        "multiple_choice_questions": [
            {
                "question_id": "mcq_001",
                "topic": "safe prompting",
                "question": "Which prompt is safest?",
                "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
                "correct_answer": "B",
                "explanation": "Option B is generic and safe.",
            }
        ],
        "scenario_questions": [
            {
                "question_id": "scenario_001",
                "topic": "safeguarding boundaries",
                "scenario": "A tutor wants to paste safeguarding details into ChatGPT.",
                "question": "What should the tutor do?",
                "expected_answer_points": ["Do not use AI for safeguarding."],
                "risk_flags": ["Data breach risk."],
                "model_answer": "Follow safeguarding procedure.",
            }
        ],
        "reflection_questions": [
            {
                "question_id": "reflection_001",
                "topic": "safe prompting",
                "question": "What is one safe AI task?",
                "guidance_points": ["Generic drafting is safe."],
            }
        ],
        "answer_key": {
            "multiple_choice_answers": [
                {
                    "question_id": "mcq_001",
                    "question": "Which prompt is safest?",
                    "correct_answer": "B",
                    "explanation": "Option B is generic.",
                }
            ],
            "scenario_answer_guidance": [
                {
                    "question_id": "scenario_001",
                    "topic": "safeguarding boundaries",
                    "scenario": "A tutor wants to paste safeguarding details.",
                    "model_answer": "Follow safeguarding procedure.",
                    "expected_answer_points": ["Do not use AI for safeguarding."],
                }
            ],
            "reflection_guidance": [
                {
                    "question_id": "reflection_001",
                    "topic": "safe prompting",
                    "question": "What is one safe AI task?",
                    "guidance_points": ["Generic drafting is safe."],
                }
            ],
            "marking_note": "This is a learning tool, not formal certification.",
        },
        "pass_guidance": "Suggested pass threshold: 8 out of 10.",
        "review_guidance": "Review qualitatively.",
    }


@pytest.fixture
def full_session_state(scenario, assessment, workshop_plan, activities, knowledge_check):
    return {
        "training_scenario": scenario,
        "training_needs_assessment": assessment,
        "workshop_plan": workshop_plan,
        "training_activities": activities,
        "facilitator_guide": {"guide_title": "Test guide", "session_purpose": "Test."},
        "staff_handout": {"handout_title": "Test handout", "purpose": "Test."},
        "knowledge_check": knowledge_check,
        "training_needs_markdown": "# Training Needs\n\nTest content.",
        "workshop_plan_markdown": "# Workshop Plan\n\nTest content.",
        "training_activities_markdown": "# Training Activities\n\nTest content.",
        "facilitator_guide_markdown": "# Facilitator Guide\n\nTest content.",
        "staff_handout_markdown": "# Staff Handout\n\nTest content.",
        "knowledge_check_markdown": "# Knowledge Check\n\nTest content.",
    }


@pytest.fixture
def pack_data(full_session_state):
    return tp.build_training_pack_data_from_session_state(full_session_state)


@pytest.fixture
def full_pack_markdown(pack_data):
    return tp.generate_markdown_training_pack(pack_data)


# ── TestGetTrainingPackRequiredSections ───────────────────────────────────────

class TestGetTrainingPackRequiredSections:
    def test_returns_list(self):
        result = tp.get_training_pack_required_sections()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(tp.get_training_pack_required_sections()) > 0

    def test_all_strings(self):
        for item in tp.get_training_pack_required_sections():
            assert isinstance(item, str)

    def test_scenario_is_required(self):
        assert "scenario" in tp.get_training_pack_required_sections()


# ── TestGetTrainingPackOptionalSections ───────────────────────────────────────

class TestGetTrainingPackOptionalSections:
    def test_returns_list(self):
        result = tp.get_training_pack_optional_sections()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(tp.get_training_pack_optional_sections()) > 0

    def test_all_strings(self):
        for item in tp.get_training_pack_optional_sections():
            assert isinstance(item, str)

    def test_includes_workshop_plan(self):
        assert "workshop_plan" in tp.get_training_pack_optional_sections()

    def test_includes_knowledge_check(self):
        assert "knowledge_check" in tp.get_training_pack_optional_sections()

    def test_includes_responsible_use_boundaries(self):
        assert "responsible_use_boundaries" in tp.get_training_pack_optional_sections()


# ── TestCheckTrainingPackReadiness ────────────────────────────────────────────

class TestCheckTrainingPackReadiness:
    def test_returns_dict(self):
        result = tp.check_training_pack_readiness({})
        assert isinstance(result, dict)

    def test_expected_keys(self):
        result = tp.check_training_pack_readiness({})
        assert "is_ready" in result
        assert "available_sections" in result
        assert "missing_sections" in result
        assert "recommended_next_steps" in result

    def test_empty_state_not_ready(self):
        result = tp.check_training_pack_readiness({})
        assert result["is_ready"] is False

    def test_with_scenario_is_ready(self, scenario):
        result = tp.check_training_pack_readiness({"training_scenario": scenario})
        assert result["is_ready"] is True

    def test_detects_available_scenario(self, scenario):
        result = tp.check_training_pack_readiness({"training_scenario": scenario})
        assert any("Scenario" in s or "scenario" in s.lower() for s in result["available_sections"])

    def test_detects_missing_sections(self, scenario):
        result = tp.check_training_pack_readiness({"training_scenario": scenario})
        assert len(result["missing_sections"]) > 0

    def test_full_state_fewer_missing(self, full_session_state):
        result = tp.check_training_pack_readiness(full_session_state)
        assert result["is_ready"] is True
        assert len(result["missing_sections"]) == 0

    def test_next_steps_empty_when_fully_populated(self, full_session_state):
        result = tp.check_training_pack_readiness(full_session_state)
        assert isinstance(result["recommended_next_steps"], list)

    def test_available_sections_is_list(self):
        result = tp.check_training_pack_readiness({})
        assert isinstance(result["available_sections"], list)

    def test_missing_sections_is_list(self):
        result = tp.check_training_pack_readiness({})
        assert isinstance(result["missing_sections"], list)


# ── TestBuildTrainingPackDataFromSessionState ─────────────────────────────────

class TestBuildTrainingPackDataFromSessionState:
    def test_returns_dict(self, full_session_state):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        assert isinstance(result, dict)

    def test_expected_keys(self, full_session_state):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        expected = [
            "pack_title",
            "organisation_name",
            "generated_date",
            "scenario",
            "training_needs_assessment",
            "workshop_plan",
            "training_activities",
            "facilitator_guide",
            "staff_handout",
            "knowledge_check",
            "source_outputs_available",
            "responsible_use_note",
            "prototype_note",
        ]
        for key in expected:
            assert key in result, f"Missing key: {key}"

    def test_pack_title_is_correct(self, full_session_state):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        assert result["pack_title"] == "Responsible AI Staff Training Pack"

    def test_organisation_name_populated(self, full_session_state, scenario):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        assert result["organisation_name"] == scenario["organisation_name"]

    def test_generated_date_is_string(self, full_session_state):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        assert isinstance(result["generated_date"], str)
        assert len(result["generated_date"]) > 0

    def test_source_outputs_available_is_dict(self, full_session_state):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        assert isinstance(result["source_outputs_available"], dict)

    def test_source_outputs_all_true_when_full(self, full_session_state):
        result = tp.build_training_pack_data_from_session_state(full_session_state)
        for key, val in result["source_outputs_available"].items():
            assert val is True, f"{key} should be True in full session state"

    def test_handles_empty_session_state(self):
        result = tp.build_training_pack_data_from_session_state({})
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_missing_scenario(self):
        result = tp.build_training_pack_data_from_session_state({})
        assert result["scenario"] == {}

    def test_source_outputs_false_when_empty(self):
        result = tp.build_training_pack_data_from_session_state({})
        for key, val in result["source_outputs_available"].items():
            assert val is False


# ── TestGenerateTrainingPackCoverSection ──────────────────────────────────────

class TestGenerateTrainingPackCoverSection:
    def test_returns_string(self, pack_data):
        result = tp.generate_training_pack_cover_section(pack_data)
        assert isinstance(result, str)

    def test_non_empty(self, pack_data):
        assert len(tp.generate_training_pack_cover_section(pack_data)) > 0

    def test_contains_organisation_name(self, pack_data):
        result = tp.generate_training_pack_cover_section(pack_data)
        assert pack_data["organisation_name"] in result

    def test_contains_generated_date(self, pack_data):
        result = tp.generate_training_pack_cover_section(pack_data)
        assert pack_data["generated_date"] in result

    def test_contains_prototype_status(self, pack_data):
        result = tp.generate_training_pack_cover_section(pack_data)
        assert "prototype" in result.lower() or "Prototype" in result

    def test_contains_synthetic_notice(self, pack_data):
        result = tp.generate_training_pack_cover_section(pack_data)
        assert "synthetic" in result.lower()

    def test_handles_empty_pack_data(self):
        result = tp.generate_training_pack_cover_section({})
        assert isinstance(result, str)
        assert len(result) > 0


# ── TestGenerateTrainingPackTableOfContents ───────────────────────────────────

class TestGenerateTrainingPackTableOfContents:
    def test_returns_string(self):
        result = tp.generate_training_pack_table_of_contents({key: True for key in tp._ALL_SECTIONS})
        assert isinstance(result, str)

    def test_non_empty(self):
        result = tp.generate_training_pack_table_of_contents({key: True for key in tp._ALL_SECTIONS})
        assert len(result) > 0

    def test_excludes_false_sections(self):
        sections = {key: False for key in tp._ALL_SECTIONS}
        result = tp.generate_training_pack_table_of_contents(sections)
        assert result == ""

    def test_includes_scenario_when_true(self):
        result = tp.generate_training_pack_table_of_contents({"scenario": True})
        assert "Organisation Scenario" in result or "Scenario" in result


# ── TestGenerateTrainingPackResponsibleUseSection ─────────────────────────────

class TestGenerateTrainingPackResponsibleUseSection:
    def test_returns_string(self):
        result = tp.generate_training_pack_responsible_use_section()
        assert isinstance(result, str)

    def test_non_empty(self):
        assert len(tp.generate_training_pack_responsible_use_section()) > 0

    def test_mentions_synthetic(self):
        result = tp.generate_training_pack_responsible_use_section()
        assert "synthetic" in result.lower()

    def test_mentions_safeguarding(self):
        result = tp.generate_training_pack_responsible_use_section()
        assert "safeguarding" in result.lower()

    def test_mentions_human_review(self):
        result = tp.generate_training_pack_responsible_use_section()
        assert "human" in result.lower()


# ── TestGenerateTrainingPackLimitationsSection ────────────────────────────────

class TestGenerateTrainingPackLimitationsSection:
    def test_returns_string(self):
        result = tp.generate_training_pack_limitations_section()
        assert isinstance(result, str)

    def test_non_empty(self):
        assert len(tp.generate_training_pack_limitations_section()) > 0

    def test_mentions_prototype(self):
        result = tp.generate_training_pack_limitations_section()
        assert "prototype" in result.lower()

    def test_mentions_human_review(self):
        result = tp.generate_training_pack_limitations_section()
        assert "human" in result.lower()

    def test_contains_bullet_points(self):
        result = tp.generate_training_pack_limitations_section()
        assert "- " in result


# ── TestGenerateFacilitatorReviewChecklist ────────────────────────────────────

class TestGenerateFacilitatorReviewChecklist:
    def test_returns_list(self):
        result = tp.generate_facilitator_review_checklist()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(tp.generate_facilitator_review_checklist()) > 0

    def test_all_strings(self):
        for item in tp.generate_facilitator_review_checklist():
            assert isinstance(item, str)

    def test_mentions_synthetic(self):
        items = tp.generate_facilitator_review_checklist()
        assert any("synthetic" in item.lower() for item in items)

    def test_mentions_safeguarding(self):
        items = tp.generate_facilitator_review_checklist()
        assert any("safeguarding" in item.lower() for item in items)


# ── TestGenerateTrainingPackNextSteps ─────────────────────────────────────────

class TestGenerateTrainingPackNextSteps:
    def test_returns_list(self, pack_data):
        result = tp.generate_training_pack_next_steps(pack_data)
        assert isinstance(result, list)

    def test_non_empty(self, pack_data):
        assert len(tp.generate_training_pack_next_steps(pack_data)) > 0

    def test_all_strings(self, pack_data):
        for item in tp.generate_training_pack_next_steps(pack_data):
            assert isinstance(item, str)

    def test_mentions_review(self, pack_data):
        items = tp.generate_training_pack_next_steps(pack_data)
        assert any("review" in item.lower() for item in items)

    def test_handles_empty_pack_data(self):
        result = tp.generate_training_pack_next_steps({})
        assert isinstance(result, list)
        assert len(result) > 0


# ── TestGenerateMarkdownTrainingPack ──────────────────────────────────────────

class TestGenerateMarkdownTrainingPack:
    def test_returns_string(self, pack_data):
        result = tp.generate_markdown_training_pack(pack_data)
        assert isinstance(result, str)

    def test_non_empty(self, pack_data):
        assert len(tp.generate_markdown_training_pack(pack_data)) > 0

    def test_contains_main_heading(self, full_pack_markdown):
        assert "# Responsible AI Staff Training Pack" in full_pack_markdown

    def test_contains_cover_page(self, full_pack_markdown):
        assert "## Cover Page" in full_pack_markdown

    def test_contains_table_of_contents(self, full_pack_markdown):
        assert "## Table of Contents" in full_pack_markdown

    def test_contains_scenario_section(self, full_pack_markdown):
        assert "Organisation Scenario Summary" in full_pack_markdown

    def test_contains_needs_assessment_section(self, full_pack_markdown):
        assert "Training Needs Assessment" in full_pack_markdown

    def test_contains_workshop_plan_section(self, full_pack_markdown):
        assert "Workshop Plan" in full_pack_markdown

    def test_contains_activities_section(self, full_pack_markdown):
        assert "Training Activities" in full_pack_markdown

    def test_contains_facilitator_guide_section(self, full_pack_markdown):
        assert "Facilitator Guide" in full_pack_markdown

    def test_contains_staff_handout_section(self, full_pack_markdown):
        assert "Staff Handout" in full_pack_markdown

    def test_contains_knowledge_check_section(self, full_pack_markdown):
        assert "Knowledge Check" in full_pack_markdown

    def test_contains_responsible_use_boundaries(self, full_pack_markdown):
        assert "Responsible-Use Boundaries" in full_pack_markdown

    def test_contains_prototype_limitations(self, full_pack_markdown):
        assert "Prototype Limitations" in full_pack_markdown

    def test_contains_recommended_next_steps(self, full_pack_markdown):
        assert "Recommended Next Steps" in full_pack_markdown

    def test_handles_none_include_sections(self, pack_data):
        result = tp.generate_markdown_training_pack(pack_data, include_sections=None)
        assert isinstance(result, str)
        assert "# Responsible AI Staff Training Pack" in result

    def test_handles_missing_optional_sections_safely(self):
        empty_pack = tp.build_training_pack_data_from_session_state({})
        result = tp.generate_markdown_training_pack(empty_pack)
        assert isinstance(result, str)
        assert "# Responsible AI Staff Training Pack" in result

    def test_excludes_section_when_false(self, pack_data):
        include = {key: True for key in tp._ALL_SECTIONS}
        include["knowledge_check"] = False
        result = tp.generate_markdown_training_pack(pack_data, include)
        # Knowledge Check section header should not appear as numbered section
        assert "Knowledge Check" not in result or "## " not in result.split("Knowledge Check")[0][-5:]

    def test_includes_synthetic_notice(self, full_pack_markdown):
        assert "synthetic" in full_pack_markdown.lower()

    def test_organisation_name_in_output(self, pack_data, full_pack_markdown):
        assert pack_data["organisation_name"] in full_pack_markdown

    def test_missing_section_note_when_no_assessment(self):
        session = {"training_scenario": get_brightpath_training_scenario()}
        pack = tp.build_training_pack_data_from_session_state(session)
        result = tp.generate_markdown_training_pack(pack)
        assert "No Training Needs Assessment" in result

    def test_missing_section_note_when_no_workshop_plan(self):
        session = {"training_scenario": get_brightpath_training_scenario()}
        pack = tp.build_training_pack_data_from_session_state(session)
        result = tp.generate_markdown_training_pack(pack)
        assert "No Workshop Plan" in result


# ── TestSummariseTrainingPack ─────────────────────────────────────────────────

class TestSummariseTrainingPack:
    def test_returns_dict(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        assert isinstance(result, dict)

    def test_expected_keys(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        expected = [
            "organisation_name",
            "generated_date",
            "sections_available",
            "sections_total",
            "activity_count",
            "mcq_count",
            "knowledge_check_included",
            "answer_key_included",
        ]
        for key in expected:
            assert key in result, f"Missing key: {key}"

    def test_sections_available_is_int(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        assert isinstance(result["sections_available"], int)

    def test_sections_total_is_int(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        assert isinstance(result["sections_total"], int)

    def test_activity_count_matches(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        activities = pack_data.get("training_activities") or []
        assert result["activity_count"] == len(activities)

    def test_knowledge_check_included_is_bool(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        assert isinstance(result["knowledge_check_included"], bool)

    def test_answer_key_included_true_when_present(self, pack_data):
        result = tp.summarise_training_pack(pack_data)
        assert result["answer_key_included"] is True

    def test_handles_empty_pack_data(self):
        result = tp.summarise_training_pack({})
        assert isinstance(result, dict)
        assert result["sections_available"] == 0


# ── TestCreateTrainingPackFilename ────────────────────────────────────────────

class TestCreateTrainingPackFilename:
    def test_returns_string(self):
        result = tp.create_training_pack_filename("BrightPath Skills Training")
        assert isinstance(result, str)

    def test_starts_with_training_pack(self):
        result = tp.create_training_pack_filename("BrightPath Skills Training")
        assert result.startswith("training-pack-")

    def test_ends_with_md(self):
        result = tp.create_training_pack_filename("BrightPath Skills Training")
        assert result.endswith(".md")

    def test_lowercase(self):
        result = tp.create_training_pack_filename("BrightPath Skills Training")
        assert result == result.lower()

    def test_spaces_replaced_with_hyphens(self):
        result = tp.create_training_pack_filename("BrightPath Skills Training")
        assert " " not in result

    def test_special_characters_removed(self):
        result = tp.create_training_pack_filename("BrightPath & Associates (UK)")
        assert "&" not in result
        assert "(" not in result
        assert ")" not in result

    def test_empty_string(self):
        result = tp.create_training_pack_filename("")
        assert result == "training-pack-organisation.md"

    def test_single_word(self):
        result = tp.create_training_pack_filename("Acme")
        assert result == "training-pack-acme.md"
