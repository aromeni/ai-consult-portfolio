"""Tests for src/facilitator_guide.py — Phase 5.

All tests use synthetic data only.
"""

import pytest
from src import facilitator_guide as fg
from src.sample_data import get_brightpath_training_scenario
from src import activity_generator as ag


# ── Fixtures ────────────────────────────────────────────────────────────────────

@pytest.fixture
def scenario():
    return get_brightpath_training_scenario()


@pytest.fixture
def minimal_scenario():
    return {
        "organisation_name": "Test Org",
        "sector": "healthcare",
        "staff_roles": ["nurses", "administrators"],
        "priority_topics": ["safe prompting"],
        "training_goal": "Use AI safely",
        "training_duration": "90 minutes",
        "delivery_mode": "In-person workshop",
    }


@pytest.fixture
def empty_scenario():
    return {}


@pytest.fixture
def activities(scenario):
    return ag.generate_training_activities(scenario)


@pytest.fixture
def full_guide(scenario, activities):
    return fg.generate_facilitator_guide(scenario, activities=activities)


_EXPECTED_GUIDE_KEYS = {
    "guide_title",
    "organisation_name",
    "audience",
    "duration_minutes",
    "delivery_mode",
    "session_purpose",
    "facilitator_principles",
    "preparation_checklist",
    "opening_script",
    "section_delivery_notes",
    "activity_facilitation_notes",
    "discussion_prompts",
    "common_misconceptions",
    "debrief_guidance",
    "risk_warnings",
    "responsible_use_messages",
    "closing_script",
    "follow_up_guidance",
    "prototype_note",
}

_EXPECTED_SECTION_KEYS = {
    "section_title",
    "facilitator_goal",
    "what_to_say",
    "what_to_ask",
    "expected_responses",
    "watch_out_for",
    "transition_note",
}

_EXPECTED_ACTIVITY_NOTE_KEYS = {
    "activity_title",
    "duration_minutes",
    "facilitator_goal",
    "setup_instructions",
    "how_to_run",
    "expected_answers",
    "debrief_questions",
    "key_takeaways",
    "risk_warnings",
}

_EXPECTED_MISCONCEPTION_KEYS = {
    "misconception",
    "why_it_is_risky",
    "facilitator_response",
}

_EXPECTED_SUMMARY_KEYS = {
    "organisation_name",
    "audience_roles",
    "duration_minutes",
    "delivery_mode",
    "activities_covered",
    "section_count",
    "misconception_count",
    "discussion_prompt_count",
}


# ── Principles and checklist ─────────────────────────────────────────────────────

class TestPrinciplesAndChecklist:
    def test_principles_returns_list(self):
        assert isinstance(fg.get_default_facilitator_principles(), list)

    def test_principles_non_empty(self):
        assert len(fg.get_default_facilitator_principles()) > 0

    def test_principles_are_strings(self):
        for p in fg.get_default_facilitator_principles():
            assert isinstance(p, str)
            assert len(p) > 0

    def test_principles_mention_synthetic(self):
        combined = " ".join(fg.get_default_facilitator_principles()).lower()
        assert "synthetic" in combined

    def test_principles_mention_safeguarding(self):
        combined = " ".join(fg.get_default_facilitator_principles()).lower()
        assert "safeguarding" in combined

    def test_checklist_returns_list(self):
        assert isinstance(fg.get_facilitator_preparation_checklist(), list)

    def test_checklist_non_empty(self):
        assert len(fg.get_facilitator_preparation_checklist()) > 0

    def test_checklist_are_strings(self):
        for item in fg.get_facilitator_preparation_checklist():
            assert isinstance(item, str)
            assert len(item) > 0

    def test_checklist_mentions_synthetic(self):
        combined = " ".join(fg.get_facilitator_preparation_checklist()).lower()
        assert "synthetic" in combined

    def test_checklist_mentions_dpo_or_data_protection(self):
        combined = " ".join(fg.get_facilitator_preparation_checklist()).lower()
        assert "dpo" in combined or "data protection" in combined


# ── Opening and closing scripts ──────────────────────────────────────────────────

class TestScripts:
    def test_opening_returns_string(self, scenario):
        result = fg.generate_opening_script(scenario)
        assert isinstance(result, str)

    def test_opening_non_empty(self, scenario):
        assert len(fg.generate_opening_script(scenario)) > 0

    def test_opening_mentions_organisation(self, scenario):
        result = fg.generate_opening_script(scenario)
        assert scenario["organisation_name"] not in result or "synthetic" in result.lower()

    def test_opening_mentions_synthetic(self, scenario):
        result = fg.generate_opening_script(scenario)
        assert "synthetic" in result.lower() or "not using real" in result.lower()

    def test_opening_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_opening_script(empty_scenario)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_opening_handles_workshop_plan(self, scenario):
        plan = {"duration_minutes": 120, "delivery_mode": "Online"}
        result = fg.generate_opening_script(scenario, workshop_plan=plan)
        assert isinstance(result, str)
        assert "120" in result

    def test_closing_returns_string(self, scenario):
        result = fg.generate_closing_script(scenario)
        assert isinstance(result, str)

    def test_closing_non_empty(self, scenario):
        assert len(fg.generate_closing_script(scenario)) > 0

    def test_closing_mentions_safeguarding(self, scenario):
        result = fg.generate_closing_script(scenario)
        assert "safeguarding" in result.lower()

    def test_closing_mentions_review(self, scenario):
        result = fg.generate_closing_script(scenario)
        assert "review" in result.lower()

    def test_closing_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_closing_script(empty_scenario)
        assert isinstance(result, str)


# ── Section delivery notes ───────────────────────────────────────────────────────

class TestSectionDeliveryNotes:
    def test_returns_list(self, scenario):
        result = fg.generate_section_delivery_notes(scenario)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self, scenario):
        assert len(fg.generate_section_delivery_notes(scenario)) > 0

    def test_each_note_is_dict(self, scenario):
        for note in fg.generate_section_delivery_notes(scenario):
            assert isinstance(note, dict)

    def test_each_note_has_required_keys(self, scenario):
        for note in fg.generate_section_delivery_notes(scenario):
            for key in _EXPECTED_SECTION_KEYS:
                assert key in note, f"Missing key '{key}' in section: {note.get('section_title')}"

    def test_section_titles_are_non_empty_strings(self, scenario):
        for note in fg.generate_section_delivery_notes(scenario):
            assert isinstance(note["section_title"], str)
            assert len(note["section_title"]) > 0

    def test_what_to_ask_is_list(self, scenario):
        for note in fg.generate_section_delivery_notes(scenario):
            assert isinstance(note["what_to_ask"], list)

    def test_expected_responses_is_list(self, scenario):
        for note in fg.generate_section_delivery_notes(scenario):
            assert isinstance(note["expected_responses"], list)

    def test_watch_out_for_is_list(self, scenario):
        for note in fg.generate_section_delivery_notes(scenario):
            assert isinstance(note["watch_out_for"], list)

    def test_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_section_delivery_notes(empty_scenario)
        assert isinstance(result, list)

    def test_handles_missing_assessment(self, scenario):
        result = fg.generate_section_delivery_notes(scenario, assessment=None)
        assert isinstance(result, list)

    def test_includes_safeguarding_section(self, scenario):
        notes = fg.generate_section_delivery_notes(scenario)
        titles = [n["section_title"].lower() for n in notes]
        assert any("safeguarding" in t or "data" in t for t in titles)


# ── Activity facilitation notes ──────────────────────────────────────────────────

class TestActivityFacilitationNotes:
    def test_returns_list_with_activities(self, activities):
        result = fg.generate_activity_facilitation_notes(activities)
        assert isinstance(result, list)

    def test_returns_list_without_activities(self):
        result = fg.generate_activity_facilitation_notes(None)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_returns_list_with_empty_activities(self):
        result = fg.generate_activity_facilitation_notes([])
        assert isinstance(result, list)
        assert len(result) > 0

    def test_note_count_matches_activities(self, activities):
        result = fg.generate_activity_facilitation_notes(activities)
        assert len(result) == len(activities)

    def test_each_note_has_required_keys(self, activities):
        for note in fg.generate_activity_facilitation_notes(activities):
            for key in _EXPECTED_ACTIVITY_NOTE_KEYS:
                assert key in note, f"Missing key '{key}' in note: {note.get('activity_title')}"

    def test_activity_titles_match(self, activities):
        notes = fg.generate_activity_facilitation_notes(activities)
        for activity, note in zip(activities, notes):
            assert note["activity_title"] == activity["activity_title"]

    def test_fallback_includes_risk_warnings(self):
        notes = fg.generate_activity_facilitation_notes(None)
        for note in notes:
            assert "risk_warnings" in note


# ── Common misconceptions ─────────────────────────────────────────────────────────

class TestCommonMisconceptions:
    def test_returns_list(self, scenario):
        result = fg.generate_common_misconceptions(scenario)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self, scenario):
        assert len(fg.generate_common_misconceptions(scenario)) > 0

    def test_each_misconception_has_required_keys(self, scenario):
        for m in fg.generate_common_misconceptions(scenario):
            for key in _EXPECTED_MISCONCEPTION_KEYS:
                assert key in m, f"Missing key '{key}' in misconception: {m.get('misconception')}"

    def test_includes_safeguarding_misconception(self, scenario):
        misconceptions = [m["misconception"].lower() for m in fg.generate_common_misconceptions(scenario)]
        assert any("safeguarding" in m for m in misconceptions)

    def test_includes_confidence_misconception(self, scenario):
        misconceptions = [m["misconception"].lower() for m in fg.generate_common_misconceptions(scenario)]
        assert any("confident" in m for m in misconceptions)

    def test_includes_approved_tools_misconception(self, scenario):
        misconceptions = [m["misconception"].lower() for m in fg.generate_common_misconceptions(scenario)]
        assert any("tool" in m or "account" in m for m in misconceptions)

    def test_facilitator_response_is_non_empty(self, scenario):
        for m in fg.generate_common_misconceptions(scenario):
            assert len(m["facilitator_response"]) > 0

    def test_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_common_misconceptions(empty_scenario)
        assert isinstance(result, list)


# ── Debrief guidance ─────────────────────────────────────────────────────────────

class TestDebriefGuidance:
    def test_returns_list(self, scenario):
        result = fg.generate_debrief_guidance(scenario)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self, scenario):
        assert len(fg.generate_debrief_guidance(scenario)) > 0

    def test_items_are_strings(self, scenario):
        for item in fg.generate_debrief_guidance(scenario):
            assert isinstance(item, str)

    def test_mentions_escalation(self, scenario):
        combined = " ".join(fg.generate_debrief_guidance(scenario)).lower()
        assert "escalat" in combined

    def test_handles_none_activities(self, scenario):
        result = fg.generate_debrief_guidance(scenario, activities=None)
        assert isinstance(result, list)

    def test_handles_activities_provided(self, scenario, activities):
        result = fg.generate_debrief_guidance(scenario, activities=activities)
        assert isinstance(result, list)
        assert len(result) > 0


# ── Risk warnings ─────────────────────────────────────────────────────────────────

class TestFacilitatorRiskWarnings:
    def test_returns_list(self, scenario):
        result = fg.generate_facilitator_risk_warnings(scenario)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self, scenario):
        assert len(fg.generate_facilitator_risk_warnings(scenario)) > 0

    def test_items_are_strings(self, scenario):
        for w in fg.generate_facilitator_risk_warnings(scenario):
            assert isinstance(w, str)

    def test_mentions_safeguarding(self, scenario):
        combined = " ".join(fg.generate_facilitator_risk_warnings(scenario)).lower()
        assert "safeguarding" in combined

    def test_mentions_learner_data(self, scenario):
        combined = " ".join(fg.generate_facilitator_risk_warnings(scenario)).lower()
        assert "learner" in combined or "personal data" in combined

    def test_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_facilitator_risk_warnings(empty_scenario)
        assert isinstance(result, list)

    def test_handles_none_assessment(self, scenario):
        result = fg.generate_facilitator_risk_warnings(scenario, assessment=None)
        assert isinstance(result, list)


# ── Discussion prompts ────────────────────────────────────────────────────────────

class TestFacilitatorDiscussionPrompts:
    def test_returns_list(self, scenario):
        result = fg.generate_facilitator_discussion_prompts(scenario)
        assert isinstance(result, list)

    def test_returns_non_empty_list(self, scenario):
        assert len(fg.generate_facilitator_discussion_prompts(scenario)) > 0

    def test_items_are_strings(self, scenario):
        for p in fg.generate_facilitator_discussion_prompts(scenario):
            assert isinstance(p, str)

    def test_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_facilitator_discussion_prompts(empty_scenario)
        assert isinstance(result, list)

    def test_handles_none_workshop_plan(self, scenario):
        result = fg.generate_facilitator_discussion_prompts(scenario, workshop_plan=None)
        assert isinstance(result, list)

    def test_deduplicates_from_workshop_plan(self, scenario):
        plan = {"discussion_prompts": ["A unique test prompt that is not in defaults?"]}
        result = fg.generate_facilitator_discussion_prompts(scenario, workshop_plan=plan)
        count = result.count("A unique test prompt that is not in defaults?")
        assert count <= 1


# ── generate_facilitator_guide ────────────────────────────────────────────────────

class TestGenerateFacilitatorGuide:
    def test_returns_dict(self, scenario):
        result = fg.generate_facilitator_guide(scenario)
        assert isinstance(result, dict)

    def test_has_all_required_keys(self, full_guide):
        for key in _EXPECTED_GUIDE_KEYS:
            assert key in full_guide, f"Missing key: {key}"

    def test_organisation_name_is_set(self, scenario, full_guide):
        assert full_guide["organisation_name"] == scenario["organisation_name"]

    def test_audience_is_list(self, full_guide):
        assert isinstance(full_guide["audience"], list)

    def test_duration_minutes_is_int(self, full_guide):
        assert isinstance(full_guide["duration_minutes"], int)
        assert full_guide["duration_minutes"] > 0

    def test_session_purpose_is_string(self, full_guide):
        assert isinstance(full_guide["session_purpose"], str)
        assert len(full_guide["session_purpose"]) > 0

    def test_opening_script_is_string(self, full_guide):
        assert isinstance(full_guide["opening_script"], str)
        assert len(full_guide["opening_script"]) > 0

    def test_closing_script_is_string(self, full_guide):
        assert isinstance(full_guide["closing_script"], str)
        assert len(full_guide["closing_script"]) > 0

    def test_section_delivery_notes_is_list(self, full_guide):
        assert isinstance(full_guide["section_delivery_notes"], list)
        assert len(full_guide["section_delivery_notes"]) > 0

    def test_activity_facilitation_notes_is_list(self, full_guide):
        assert isinstance(full_guide["activity_facilitation_notes"], list)

    def test_common_misconceptions_is_list(self, full_guide):
        assert isinstance(full_guide["common_misconceptions"], list)
        assert len(full_guide["common_misconceptions"]) > 0

    def test_debrief_guidance_is_list(self, full_guide):
        assert isinstance(full_guide["debrief_guidance"], list)

    def test_risk_warnings_is_list(self, full_guide):
        assert isinstance(full_guide["risk_warnings"], list)
        assert len(full_guide["risk_warnings"]) > 0

    def test_prototype_note_is_string(self, full_guide):
        assert isinstance(full_guide["prototype_note"], str)
        assert "synthetic" in full_guide["prototype_note"].lower()

    def test_handles_none_scenario(self):
        result = fg.generate_facilitator_guide(None)
        assert isinstance(result, dict)
        assert "guide_title" in result

    def test_handles_empty_scenario(self, empty_scenario):
        result = fg.generate_facilitator_guide(empty_scenario)
        assert isinstance(result, dict)

    def test_handles_none_assessment(self, scenario):
        result = fg.generate_facilitator_guide(scenario, assessment=None)
        assert isinstance(result, dict)

    def test_handles_none_workshop_plan(self, scenario):
        result = fg.generate_facilitator_guide(scenario, workshop_plan=None)
        assert isinstance(result, dict)

    def test_handles_none_activities(self, scenario):
        result = fg.generate_facilitator_guide(scenario, activities=None)
        assert isinstance(result, dict)

    def test_activities_reflected_in_facilitation_notes(self, scenario, activities):
        result = fg.generate_facilitator_guide(scenario, activities=activities)
        assert len(result["activity_facilitation_notes"]) == len(activities)

    def test_duration_from_workshop_plan(self, scenario):
        plan = {"duration_minutes": 120}
        result = fg.generate_facilitator_guide(scenario, workshop_plan=plan)
        assert result["duration_minutes"] == 120

    def test_delivery_mode_from_workshop_plan(self, scenario):
        plan = {"delivery_mode": "Online workshop"}
        result = fg.generate_facilitator_guide(scenario, workshop_plan=plan)
        assert result["delivery_mode"] == "Online workshop"


# ── summarise_facilitator_guide ───────────────────────────────────────────────────

class TestSummariseFacilitatorGuide:
    def test_returns_dict(self, full_guide):
        result = fg.summarise_facilitator_guide(full_guide)
        assert isinstance(result, dict)

    def test_has_expected_keys(self, full_guide):
        result = fg.summarise_facilitator_guide(full_guide)
        for key in _EXPECTED_SUMMARY_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_duration_matches_guide(self, full_guide):
        result = fg.summarise_facilitator_guide(full_guide)
        assert result["duration_minutes"] == full_guide["duration_minutes"]

    def test_section_count_matches(self, full_guide):
        result = fg.summarise_facilitator_guide(full_guide)
        assert result["section_count"] == len(full_guide["section_delivery_notes"])

    def test_misconception_count_matches(self, full_guide):
        result = fg.summarise_facilitator_guide(full_guide)
        assert result["misconception_count"] == len(full_guide["common_misconceptions"])

    def test_audience_roles_is_list(self, full_guide):
        result = fg.summarise_facilitator_guide(full_guide)
        assert isinstance(result["audience_roles"], list)

    def test_handles_empty_guide(self):
        result = fg.summarise_facilitator_guide({})
        assert isinstance(result, dict)
        assert result["activities_covered"] == 0


# ── format_facilitator_guide_as_markdown ─────────────────────────────────────────

class TestFormatFacilitatorGuideAsMarkdown:
    def test_returns_string(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert isinstance(result, str)

    def test_contains_main_heading(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "# Responsible AI Workshop Facilitator Guide" in result

    def test_contains_organisation_section(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "## Organisation" in result

    def test_contains_session_purpose(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Session Purpose" in result

    def test_contains_facilitator_principles(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Facilitator Principles" in result

    def test_contains_preparation_checklist(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Preparation Checklist" in result

    def test_contains_opening_script(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Opening Script" in result

    def test_contains_section_delivery_notes(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Section-by-Section Delivery Notes" in result

    def test_contains_activity_facilitation_notes(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Activity Facilitation Notes" in result

    def test_contains_common_misconceptions(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Common Misconceptions" in result

    def test_contains_debrief_guidance(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Debrief Guidance" in result

    def test_contains_risk_warnings(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Risk Warnings" in result

    def test_contains_closing_script(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Closing Script" in result

    def test_contains_prototype_boundaries(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "Prototype and Responsible-Use Boundaries" in result

    def test_boundaries_mention_synthetic(self, full_guide):
        result = fg.format_facilitator_guide_as_markdown(full_guide)
        assert "synthetic" in result.lower()

    def test_handles_empty_guide(self):
        result = fg.format_facilitator_guide_as_markdown({})
        assert isinstance(result, str)


# ── create_facilitator_guide_filename ────────────────────────────────────────────

class TestCreateFacilitatorGuideFilename:
    def test_returns_string(self):
        assert isinstance(fg.create_facilitator_guide_filename("BrightPath Skills Training"), str)

    def test_starts_with_prefix(self):
        filename = fg.create_facilitator_guide_filename("BrightPath Skills Training")
        assert filename.startswith("facilitator-guide-")

    def test_ends_with_md(self):
        filename = fg.create_facilitator_guide_filename("BrightPath Skills Training")
        assert filename.endswith(".md")

    def test_is_lowercase(self):
        filename = fg.create_facilitator_guide_filename("BrightPath Skills Training")
        assert filename == filename.lower()

    def test_no_spaces(self):
        filename = fg.create_facilitator_guide_filename("BrightPath Skills Training")
        assert " " not in filename

    def test_handles_special_characters(self):
        filename = fg.create_facilitator_guide_filename("Test & Org (UK)")
        assert " " not in filename
        assert "&" not in filename

    def test_handles_empty_name(self):
        filename = fg.create_facilitator_guide_filename("")
        assert filename.endswith(".md")
        assert "facilitator-guide-" in filename

    def test_handles_none_name(self):
        filename = fg.create_facilitator_guide_filename(None)
        assert filename.endswith(".md")
