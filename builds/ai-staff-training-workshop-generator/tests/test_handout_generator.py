"""Tests for src/handout_generator.py — Phase 6: Staff Handout Generator."""

import pytest
from src import handout_generator as hg


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
        "agenda": [
            {"section_title": "Introduction", "time_range": "0:00–0:10"},
        ],
    }


@pytest.fixture
def activities():
    return [
        {
            "activity_id": "safe_unsafe_prompt_sorting",
            "activity_title": "Safe vs Unsafe Prompt Sorting",
            "activity_type": "safe_unsafe_prompt_sorting",
            "duration_minutes": 20,
            "scenario_cards": [
                {
                    "card_id": "A",
                    "prompt": "Create a generic lesson outline on communication skills.",
                    "classification": "SAFE",
                    "reason": "No personal data included.",
                },
                {
                    "card_id": "E",
                    "prompt": "Decide whether this safeguarding concern should be reported.",
                    "classification": "PROHIBITED",
                    "reason": "Safeguarding decisions must be made by humans.",
                },
            ],
        },
        {
            "activity_id": "risky_prompt_rewrite",
            "activity_title": "Rewrite a Risky Prompt Safely",
            "activity_type": "risky_prompt_rewrite",
            "duration_minutes": 15,
            "scenario_cards": [
                {
                    "card_id": "R1",
                    "original_prompt": "Write a report on learner James Collins, BTEC Level 2, who missed 5 sessions.",
                    "safe_rewrite": "Create a generic attendance report template for a BTEC learner. Do not include names.",
                    "what_changed": ["Removed learner name.", "Converted to a generic template."],
                },
            ],
        },
    ]


@pytest.fixture
def full_handout(scenario, assessment, workshop_plan, activities):
    return hg.generate_staff_handout(
        scenario,
        assessment=assessment,
        workshop_plan=workshop_plan,
        activities=activities,
    )


# ── TestGetDefaultSafeUsePrinciples ───────────────────────────────────────────

class TestGetDefaultSafeUsePrinciples:
    def test_returns_list(self):
        result = hg.get_default_safe_use_principles()
        assert isinstance(result, list)

    def test_non_empty(self):
        assert len(hg.get_default_safe_use_principles()) > 0

    def test_all_strings(self):
        for item in hg.get_default_safe_use_principles():
            assert isinstance(item, str)

    def test_mentions_human_review(self):
        principles = hg.get_default_safe_use_principles()
        assert any("review" in p.lower() or "human" in p.lower() for p in principles)

    def test_mentions_learner_data(self):
        principles = hg.get_default_safe_use_principles()
        assert any("learner" in p.lower() or "personal" in p.lower() for p in principles)

    def test_mentions_approved_tools(self):
        principles = hg.get_default_safe_use_principles()
        assert any("approved" in p.lower() for p in principles)


# ── TestGenerateAllowedAiUses ─────────────────────────────────────────────────

class TestGenerateAllowedAiUses:
    def test_returns_list(self, scenario):
        result = hg.generate_allowed_ai_uses(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_allowed_ai_uses(scenario)) > 0

    def test_all_strings(self, scenario):
        for item in hg.generate_allowed_ai_uses(scenario):
            assert isinstance(item, str)

    def test_mentions_generic(self, scenario):
        result = hg.generate_allowed_ai_uses(scenario)
        assert any("generic" in item.lower() for item in result)

    def test_with_assessment(self, scenario, assessment):
        result = hg.generate_allowed_ai_uses(scenario, assessment)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_with_minimal_scenario(self, minimal_scenario):
        result = hg.generate_allowed_ai_uses(minimal_scenario)
        assert len(result) > 0

    def test_with_none_assessment(self, scenario):
        result = hg.generate_allowed_ai_uses(scenario, assessment=None)
        assert isinstance(result, list)


# ── TestGenerateProhibitedAiUses ──────────────────────────────────────────────

class TestGenerateProhibitedAiUses:
    def test_returns_list(self, scenario):
        result = hg.generate_prohibited_ai_uses(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_prohibited_ai_uses(scenario)) > 0

    def test_all_strings(self, scenario):
        for item in hg.generate_prohibited_ai_uses(scenario):
            assert isinstance(item, str)

    def test_mentions_safeguarding(self, scenario):
        result = hg.generate_prohibited_ai_uses(scenario)
        assert any("safeguarding" in item.lower() for item in result)

    def test_mentions_learner_data(self, scenario):
        result = hg.generate_prohibited_ai_uses(scenario)
        assert any("learner" in item.lower() for item in result)

    def test_with_assessment(self, scenario, assessment):
        result = hg.generate_prohibited_ai_uses(scenario, assessment)
        assert isinstance(result, list)
        assert len(result) >= len(hg.generate_prohibited_ai_uses(scenario))

    def test_with_none_assessment(self, scenario):
        result = hg.generate_prohibited_ai_uses(scenario, assessment=None)
        assert isinstance(result, list)


# ── TestGenerateSafePromptExamples ────────────────────────────────────────────

class TestGenerateSafePromptExamples:
    def test_returns_list(self, scenario):
        result = hg.generate_safe_prompt_examples(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_safe_prompt_examples(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in hg.generate_safe_prompt_examples(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in hg.generate_safe_prompt_examples(scenario):
            assert "title" in item
            assert "prompt" in item
            assert "why_it_is_safe" in item

    def test_with_activities(self, scenario, activities):
        result = hg.generate_safe_prompt_examples(scenario, activities)
        assert isinstance(result, list)
        assert len(result) >= len(hg.generate_safe_prompt_examples(scenario))

    def test_with_none_activities(self, scenario):
        result = hg.generate_safe_prompt_examples(scenario, activities=None)
        assert isinstance(result, list)


# ── TestGenerateUnsafePromptExamples ──────────────────────────────────────────

class TestGenerateUnsafePromptExamples:
    def test_returns_list(self, scenario):
        result = hg.generate_unsafe_prompt_examples(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_unsafe_prompt_examples(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in hg.generate_unsafe_prompt_examples(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in hg.generate_unsafe_prompt_examples(scenario):
            assert "title" in item
            assert "prompt" in item
            assert "why_it_is_risky" in item

    def test_with_activities(self, scenario, activities):
        result = hg.generate_unsafe_prompt_examples(scenario, activities)
        assert isinstance(result, list)
        assert len(result) >= len(hg.generate_unsafe_prompt_examples(scenario))

    def test_with_none_activities(self, scenario):
        result = hg.generate_unsafe_prompt_examples(scenario, activities=None)
        assert isinstance(result, list)


# ── TestGenerateSaferRewrittenPromptExamples ──────────────────────────────────

class TestGenerateSaferRewrittenPromptExamples:
    def test_returns_list(self, scenario):
        result = hg.generate_safer_rewritten_prompt_examples(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_safer_rewritten_prompt_examples(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in hg.generate_safer_rewritten_prompt_examples(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in hg.generate_safer_rewritten_prompt_examples(scenario):
            assert "unsafe_prompt" in item
            assert "safer_prompt" in item
            assert "what_changed" in item

    def test_what_changed_is_list(self, scenario):
        for item in hg.generate_safer_rewritten_prompt_examples(scenario):
            assert isinstance(item["what_changed"], list)

    def test_with_activities(self, scenario, activities):
        result = hg.generate_safer_rewritten_prompt_examples(scenario, activities)
        assert isinstance(result, list)
        assert len(result) >= len(hg.generate_safer_rewritten_prompt_examples(scenario))

    def test_with_none_activities(self, scenario):
        result = hg.generate_safer_rewritten_prompt_examples(scenario, activities=None)
        assert isinstance(result, list)


# ── TestGenerateHumanReviewChecklist ──────────────────────────────────────────

class TestGenerateHumanReviewChecklist:
    def test_returns_list(self, scenario):
        result = hg.generate_human_review_checklist(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_human_review_checklist(scenario)) > 0

    def test_all_strings(self, scenario):
        for item in hg.generate_human_review_checklist(scenario):
            assert isinstance(item, str)

    def test_with_assessment(self, scenario, assessment):
        result = hg.generate_human_review_checklist(scenario, assessment)
        assert isinstance(result, list)
        assert len(result) >= len(hg.generate_human_review_checklist(scenario))

    def test_with_none_assessment(self, scenario):
        result = hg.generate_human_review_checklist(scenario, assessment=None)
        assert isinstance(result, list)

    def test_mentions_approved_tool(self, scenario):
        result = hg.generate_human_review_checklist(scenario)
        assert any("approved" in item.lower() for item in result)

    def test_mentions_human_responsibility(self, scenario):
        result = hg.generate_human_review_checklist(scenario)
        assert any("human" in item.lower() or "responsibility" in item.lower() for item in result)


# ── TestGenerateEscalationGuidance ────────────────────────────────────────────

class TestGenerateEscalationGuidance:
    def test_returns_list(self, scenario):
        result = hg.generate_escalation_guidance(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_escalation_guidance(scenario)) > 0

    def test_each_item_is_dict(self, scenario):
        for item in hg.generate_escalation_guidance(scenario):
            assert isinstance(item, dict)

    def test_required_keys(self, scenario):
        for item in hg.generate_escalation_guidance(scenario):
            assert "issue" in item
            assert "what_to_do" in item
            assert "who_to_contact" in item

    def test_safeguarding_item_present(self, scenario):
        result = hg.generate_escalation_guidance(scenario)
        issues = [item["issue"].lower() for item in result]
        assert any("safeguarding" in issue for issue in issues)

    def test_data_protection_item_present(self, scenario):
        result = hg.generate_escalation_guidance(scenario)
        issues = [item["issue"].lower() for item in result]
        assert any("data" in issue for issue in issues)

    def test_with_none_assessment(self, scenario):
        result = hg.generate_escalation_guidance(scenario, assessment=None)
        assert isinstance(result, list)

    def test_organisation_name_in_contacts(self, scenario):
        result = hg.generate_escalation_guidance(scenario)
        org = scenario["organisation_name"]
        assert any(org in item["who_to_contact"] for item in result)


# ── TestGenerateKeyTakeaways ──────────────────────────────────────────────────

class TestGenerateKeyTakeaways:
    def test_returns_list(self, scenario):
        result = hg.generate_key_takeaways(scenario)
        assert isinstance(result, list)

    def test_non_empty(self, scenario):
        assert len(hg.generate_key_takeaways(scenario)) > 0

    def test_all_strings(self, scenario):
        for item in hg.generate_key_takeaways(scenario):
            assert isinstance(item, str)

    def test_with_assessment(self, scenario, assessment):
        result = hg.generate_key_takeaways(scenario, assessment)
        assert isinstance(result, list)
        assert len(result) >= len(hg.generate_key_takeaways(scenario))

    def test_with_none_assessment(self, scenario):
        result = hg.generate_key_takeaways(scenario, assessment=None)
        assert isinstance(result, list)

    def test_mentions_human_responsibility(self, scenario):
        result = hg.generate_key_takeaways(scenario)
        assert any("human" in item.lower() for item in result)


# ── TestGenerateStaffHandout ──────────────────────────────────────────────────

class TestGenerateStaffHandout:
    def test_returns_dict(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert isinstance(result, dict)

    def test_expected_keys(self, scenario):
        result = hg.generate_staff_handout(scenario)
        expected_keys = [
            "handout_title",
            "organisation_name",
            "audience",
            "purpose",
            "safe_use_principles",
            "allowed_ai_uses",
            "prohibited_ai_uses",
            "safe_prompt_examples",
            "unsafe_prompt_examples",
            "safer_rewritten_prompt_examples",
            "human_review_checklist",
            "escalation_guidance",
            "key_takeaways",
            "responsible_use_warning",
            "prototype_note",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_handout_title_contains_org_name(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert scenario["organisation_name"] in result["handout_title"]

    def test_organisation_name(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert result["organisation_name"] == scenario["organisation_name"]

    def test_audience_is_list(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert isinstance(result["audience"], list)

    def test_audience_populated(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["audience"]) > 0

    def test_safe_use_principles_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["safe_use_principles"]) > 0

    def test_allowed_ai_uses_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["allowed_ai_uses"]) > 0

    def test_prohibited_ai_uses_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["prohibited_ai_uses"]) > 0

    def test_safe_prompt_examples_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["safe_prompt_examples"]) > 0

    def test_unsafe_prompt_examples_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["unsafe_prompt_examples"]) > 0

    def test_human_review_checklist_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["human_review_checklist"]) > 0

    def test_escalation_guidance_non_empty(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["escalation_guidance"]) > 0

    def test_prototype_note_present(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["prototype_note"]) > 0

    def test_responsible_use_warning_present(self, scenario):
        result = hg.generate_staff_handout(scenario)
        assert len(result["responsible_use_warning"]) > 0

    def test_handles_none_assessment(self, scenario):
        result = hg.generate_staff_handout(scenario, assessment=None)
        assert isinstance(result, dict)
        assert len(result["allowed_ai_uses"]) > 0

    def test_handles_none_workshop_plan(self, scenario):
        result = hg.generate_staff_handout(scenario, workshop_plan=None)
        assert isinstance(result, dict)

    def test_handles_none_activities(self, scenario):
        result = hg.generate_staff_handout(scenario, activities=None)
        assert isinstance(result, dict)
        assert len(result["safe_prompt_examples"]) > 0

    def test_handles_none_facilitator_guide(self, scenario):
        result = hg.generate_staff_handout(scenario, facilitator_guide=None)
        assert isinstance(result, dict)

    def test_handles_none_scenario(self):
        result = hg.generate_staff_handout(None)
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_empty_scenario(self):
        result = hg.generate_staff_handout({})
        assert isinstance(result, dict)
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_missing_staff_roles(self, scenario):
        s = {**scenario, "staff_roles": []}
        result = hg.generate_staff_handout(s)
        assert isinstance(result["audience"], list)
        assert len(result["audience"]) > 0

    def test_full_generation(self, scenario, assessment, workshop_plan, activities):
        result = hg.generate_staff_handout(
            scenario,
            assessment=assessment,
            workshop_plan=workshop_plan,
            activities=activities,
        )
        assert isinstance(result, dict)
        assert len(result["allowed_ai_uses"]) > 0

    def test_workshop_plan_referenced_in_purpose(self, scenario, workshop_plan):
        result = hg.generate_staff_handout(scenario, workshop_plan=workshop_plan)
        assert workshop_plan["workshop_title"] in result["purpose"]


# ── TestSummariseStaffHandout ─────────────────────────────────────────────────

class TestSummariseStaffHandout:
    def test_returns_dict(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        assert isinstance(result, dict)

    def test_expected_keys(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        expected = [
            "organisation_name",
            "audience_roles",
            "safe_prompt_count",
            "unsafe_prompt_count",
            "safer_rewrite_count",
            "checklist_item_count",
            "escalation_item_count",
            "key_takeaway_count",
        ]
        for key in expected:
            assert key in result, f"Missing key: {key}"

    def test_safe_prompt_count_is_int(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        assert isinstance(result["safe_prompt_count"], int)

    def test_safe_prompt_count_matches(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        assert result["safe_prompt_count"] == len(full_handout["safe_prompt_examples"])

    def test_escalation_count_matches(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        assert result["escalation_item_count"] == len(full_handout["escalation_guidance"])

    def test_audience_roles_is_list(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        assert isinstance(result["audience_roles"], list)

    def test_organisation_name_correct(self, full_handout):
        result = hg.summarise_staff_handout(full_handout)
        assert result["organisation_name"] == full_handout["organisation_name"]


# ── TestFormatStaffHandoutAsMarkdown ──────────────────────────────────────────

class TestFormatStaffHandoutAsMarkdown:
    def test_returns_string(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert isinstance(result, str)

    def test_non_empty(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert len(result) > 0

    def test_contains_main_heading(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "# Responsible AI Staff Handout" in result

    def test_contains_organisation_section(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Organisation" in result

    def test_contains_purpose_section(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Purpose" in result

    def test_contains_safe_use_principles(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Safe-Use Principles" in result

    def test_contains_allowed_uses(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## What Staff Can Use AI For" in result

    def test_contains_prohibited_uses(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## What Staff Must Not Use AI For" in result

    def test_contains_safe_prompt_examples(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Safe Prompt Examples" in result

    def test_contains_unsafe_prompt_examples(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Unsafe Prompt Examples" in result

    def test_contains_safer_rewritten_prompts(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Safer Rewritten Prompt Examples" in result

    def test_contains_human_review_checklist(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Human Review Checklist" in result

    def test_contains_escalation_guidance(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Escalation Guidance" in result

    def test_contains_key_takeaways(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Key Takeaways" in result

    def test_contains_prototype_boundaries(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "## Prototype and Responsible-Use Boundaries" in result

    def test_contains_responsible_use_note(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "synthetic" in result.lower()

    def test_checklist_items_formatted(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert "- [ ]" in result

    def test_org_name_in_output(self, full_handout):
        result = hg.format_staff_handout_as_markdown(full_handout)
        assert full_handout["organisation_name"] in result


# ── TestCreateStaffHandoutFilename ────────────────────────────────────────────

class TestCreateStaffHandoutFilename:
    def test_returns_string(self):
        result = hg.create_staff_handout_filename("BrightPath Skills Training")
        assert isinstance(result, str)

    def test_starts_with_staff_handout(self):
        result = hg.create_staff_handout_filename("BrightPath Skills Training")
        assert result.startswith("staff-handout-")

    def test_ends_with_md(self):
        result = hg.create_staff_handout_filename("BrightPath Skills Training")
        assert result.endswith(".md")

    def test_lowercase(self):
        result = hg.create_staff_handout_filename("BrightPath Skills Training")
        assert result == result.lower()

    def test_spaces_replaced_with_hyphens(self):
        result = hg.create_staff_handout_filename("BrightPath Skills Training")
        assert " " not in result

    def test_special_characters_removed(self):
        result = hg.create_staff_handout_filename("BrightPath & Associates (UK)")
        assert "&" not in result
        assert "(" not in result
        assert ")" not in result

    def test_empty_string(self):
        result = hg.create_staff_handout_filename("")
        assert result == "staff-handout-organisation.md"

    def test_single_word(self):
        result = hg.create_staff_handout_filename("Acme")
        assert result == "staff-handout-acme.md"
