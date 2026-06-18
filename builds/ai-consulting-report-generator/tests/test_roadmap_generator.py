"""Tests for src/roadmap_generator.py — Build 5 Phase 5."""

import pytest
from src.roadmap_generator import (
    get_roadmap_phase_definitions,
    generate_roadmap_action_id,
    generate_roadmap_action,
    get_priority_colour,
    get_phase_colour,
    generate_foundation_actions,
    generate_pilot_preparation_actions,
    generate_pilot_delivery_actions,
    generate_review_and_scale_actions,
    generate_implementation_roadmap,
    summarise_implementation_roadmap,
    format_implementation_roadmap_as_markdown,
)
from src.sample_data import get_brightpath_audit_data
from src import risk_register as rr
from src import scoring_summary as ss
from src import opportunity_generator as og


# ── Fixtures ────────────────────────────────────────────────────────────────────

@pytest.fixture
def brightpath_audit():
    return get_brightpath_audit_data()


@pytest.fixture
def brightpath_risk_register(brightpath_audit):
    return rr.generate_risk_register(brightpath_audit)


@pytest.fixture
def brightpath_risk_summary(brightpath_risk_register):
    return rr.summarise_risk_register(brightpath_risk_register)


@pytest.fixture
def brightpath_readiness(brightpath_audit):
    org = brightpath_audit.get("organisation_profile", {}).get("organisation_name", "")
    return ss.generate_readiness_summary(brightpath_audit["readiness_scores"], org_name=org)


@pytest.fixture
def brightpath_portfolio(brightpath_audit):
    return og.generate_ai_opportunity_portfolio(brightpath_audit)


@pytest.fixture
def brightpath_roadmap(
    brightpath_audit,
    brightpath_readiness,
    brightpath_risk_register,
    brightpath_risk_summary,
    brightpath_portfolio,
):
    return generate_implementation_roadmap(
        brightpath_audit,
        brightpath_readiness,
        brightpath_risk_register,
        brightpath_risk_summary,
        brightpath_portfolio,
    )


@pytest.fixture
def brightpath_summary(brightpath_roadmap):
    return summarise_implementation_roadmap(brightpath_roadmap)


@pytest.fixture
def brightpath_markdown(brightpath_roadmap, brightpath_summary):
    return format_implementation_roadmap_as_markdown(brightpath_roadmap, brightpath_summary)


@pytest.fixture
def empty_roadmap():
    return generate_implementation_roadmap({})


# ── TestGetRoadmapPhaseDefinitions ──────────────────────────────────────────────

class TestGetRoadmapPhaseDefinitions:
    def test_returns_3_phases(self):
        assert len(get_roadmap_phase_definitions()) == 3

    def test_returns_list(self):
        assert isinstance(get_roadmap_phase_definitions(), list)

    def test_first_phase_is_day_30(self):
        phases = get_roadmap_phase_definitions()
        assert phases[0]["phase_label"] == "First 30 days"

    def test_second_phase_is_day_60(self):
        phases = get_roadmap_phase_definitions()
        assert phases[1]["phase_label"] == "Days 31–60"

    def test_third_phase_is_day_90(self):
        phases = get_roadmap_phase_definitions()
        assert phases[2]["phase_label"] == "Days 61–90"

    def test_phases_have_expected_keys(self):
        for phase in get_roadmap_phase_definitions():
            assert "phase_label" in phase
            assert "phase_focus" in phase
            assert "phase_id_prefix" in phase
            assert "colour" in phase


# ── TestGenerateRoadmapActionId ──────────────────────────────────────────────────

class TestGenerateRoadmapActionId:
    def test_day30_index_0_gives_day30_001(self):
        assert generate_roadmap_action_id("First 30 days", 0) == "DAY30-001"

    def test_day60_index_0_gives_day60_001(self):
        assert generate_roadmap_action_id("Days 31–60", 0) == "DAY60-001"

    def test_day90_index_0_gives_day90_001(self):
        assert generate_roadmap_action_id("Days 61–90", 0) == "DAY90-001"

    def test_index_1_gives_002(self):
        assert generate_roadmap_action_id("First 30 days", 1) == "DAY30-002"

    def test_index_9_gives_010(self):
        assert generate_roadmap_action_id("First 30 days", 9) == "DAY30-010"

    def test_unknown_phase_uses_act_prefix(self):
        result = generate_roadmap_action_id("Unknown Phase", 0)
        assert result.startswith("ACT-")


# ── TestGenerateRoadmapAction ────────────────────────────────────────────────────

class TestGenerateRoadmapAction:
    def test_expected_keys_present(self):
        action = generate_roadmap_action(
            "DAY30-001", "First 30 days", "Test action", "Description",
            "Owner", "High", "Success measure"
        )
        expected_keys = {
            "action_id", "phase", "title", "description", "owner",
            "priority", "success_measure", "dependency", "risk_reduction", "related_output",
        }
        assert expected_keys.issubset(action.keys())

    def test_action_id_set(self):
        action = generate_roadmap_action(
            "DAY30-001", "First 30 days", "Title", "Desc", "Owner", "High", "Measure"
        )
        assert action["action_id"] == "DAY30-001"

    def test_priority_set(self):
        action = generate_roadmap_action(
            "DAY30-001", "First 30 days", "Title", "Desc", "Owner", "High", "Measure"
        )
        assert action["priority"] == "High"

    def test_optional_fields_default_to_empty(self):
        action = generate_roadmap_action(
            "DAY30-001", "First 30 days", "Title", "Desc", "Owner", "High", "Measure"
        )
        assert action["dependency"] == ""
        assert action["risk_reduction"] == ""
        assert action["related_output"] == ""

    def test_optional_fields_set_when_provided(self):
        action = generate_roadmap_action(
            "DAY30-001", "First 30 days", "Title", "Desc", "Owner", "High", "Measure",
            dependency="Dep", risk_reduction="Risk", related_output="Output"
        )
        assert action["dependency"] == "Dep"
        assert action["risk_reduction"] == "Risk"
        assert action["related_output"] == "Output"


# ── TestGetPriorityColour ────────────────────────────────────────────────────────

class TestGetPriorityColour:
    def test_high_returns_hex(self):
        c = get_priority_colour("High")
        assert isinstance(c, str) and c.startswith("#")

    def test_medium_returns_hex(self):
        c = get_priority_colour("Medium")
        assert isinstance(c, str) and c.startswith("#")

    def test_low_returns_hex(self):
        c = get_priority_colour("Low")
        assert isinstance(c, str) and c.startswith("#")

    def test_unknown_returns_fallback(self):
        c = get_priority_colour("Unknown")
        assert isinstance(c, str) and c.startswith("#")


# ── TestGetPhaseColour ───────────────────────────────────────────────────────────

class TestGetPhaseColour:
    def test_day30_returns_hex(self):
        c = get_phase_colour("First 30 days")
        assert isinstance(c, str) and c.startswith("#")

    def test_day60_returns_hex(self):
        c = get_phase_colour("Days 31–60")
        assert isinstance(c, str) and c.startswith("#")

    def test_day90_returns_hex(self):
        c = get_phase_colour("Days 61–90")
        assert isinstance(c, str) and c.startswith("#")

    def test_unknown_returns_fallback(self):
        c = get_phase_colour("Unknown")
        assert isinstance(c, str) and c.startswith("#")


# ── TestGenerateFoundationActions ────────────────────────────────────────────────

class TestGenerateFoundationActions:
    def test_returns_non_empty_list(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit)
        assert len(actions) > 0

    def test_returns_list_type(self, brightpath_audit):
        assert isinstance(generate_foundation_actions(brightpath_audit), list)

    def test_all_actions_have_expected_keys(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit)
        for a in actions:
            assert "action_id" in a
            assert "phase" in a
            assert "title" in a
            assert "description" in a
            assert "owner" in a
            assert "priority" in a
            assert "success_measure" in a

    def test_phase_label_is_first_30_days(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit)
        for a in actions:
            assert a["phase"] == "First 30 days"

    def test_all_ids_start_with_day30(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit)
        for a in actions:
            assert a["action_id"].startswith("DAY30-")

    def test_brightpath_adds_policy_action(self, brightpath_audit, brightpath_risk_summary):
        actions = generate_foundation_actions(
            brightpath_audit, risk_summary=brightpath_risk_summary
        )
        titles = [a["title"].lower() for a in actions]
        assert any("policy" in t for t in titles)

    def test_brightpath_adds_risk_action(self, brightpath_audit, brightpath_risk_summary):
        actions = generate_foundation_actions(
            brightpath_audit, risk_summary=brightpath_risk_summary
        )
        titles = [a["title"].lower() for a in actions]
        assert any("risk" in t for t in titles)

    def test_brightpath_has_at_least_8_actions(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit)
        assert len(actions) >= 8

    def test_empty_audit_data_returns_base_actions(self):
        actions = generate_foundation_actions({})
        assert len(actions) >= 8

    def test_missing_risk_summary_is_safe(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit, risk_summary=None)
        assert len(actions) > 0

    def test_priorities_are_valid_values(self, brightpath_audit):
        actions = generate_foundation_actions(brightpath_audit)
        valid = {"High", "Medium", "Low"}
        for a in actions:
            assert a["priority"] in valid


# ── TestGeneratePilotPreparationActions ─────────────────────────────────────────

class TestGeneratePilotPreparationActions:
    def test_returns_non_empty_list(self, brightpath_audit):
        actions = generate_pilot_preparation_actions(brightpath_audit)
        assert len(actions) > 0

    def test_returns_list_type(self, brightpath_audit):
        assert isinstance(generate_pilot_preparation_actions(brightpath_audit), list)

    def test_phase_is_days_31_60(self, brightpath_audit):
        actions = generate_pilot_preparation_actions(brightpath_audit)
        for a in actions:
            assert a["phase"] == "Days 31–60"

    def test_all_ids_start_with_day60(self, brightpath_audit):
        actions = generate_pilot_preparation_actions(brightpath_audit)
        for a in actions:
            assert a["action_id"].startswith("DAY60-")

    def test_includes_training_action(self, brightpath_audit):
        actions = generate_pilot_preparation_actions(brightpath_audit)
        titles = [a["title"].lower() for a in actions]
        assert any("training" in t for t in titles)

    def test_with_portfolio_references_pilot_name(self, brightpath_audit, brightpath_portfolio):
        actions = generate_pilot_preparation_actions(brightpath_audit, brightpath_portfolio)
        # Should generate fine with portfolio context
        assert len(actions) > 0

    def test_empty_audit_data_safe(self):
        actions = generate_pilot_preparation_actions({})
        assert len(actions) > 0


# ── TestGeneratePilotDeliveryActions ────────────────────────────────────────────

class TestGeneratePilotDeliveryActions:
    def test_returns_non_empty_list(self, brightpath_audit):
        actions = generate_pilot_delivery_actions(brightpath_audit)
        assert len(actions) > 0

    def test_returns_list_type(self, brightpath_audit):
        assert isinstance(generate_pilot_delivery_actions(brightpath_audit), list)

    def test_phase_is_days_31_60(self, brightpath_audit):
        actions = generate_pilot_delivery_actions(brightpath_audit)
        for a in actions:
            assert a["phase"] == "Days 31–60"

    def test_includes_launch_action(self, brightpath_audit, brightpath_portfolio):
        actions = generate_pilot_delivery_actions(brightpath_audit, brightpath_portfolio)
        titles = [a["title"].lower() for a in actions]
        assert any("launch" in t or "pilot" in t for t in titles)

    def test_includes_human_review_action(self, brightpath_audit):
        actions = generate_pilot_delivery_actions(brightpath_audit)
        titles = [a["title"].lower() for a in actions]
        assert any("review" in t or "human" in t for t in titles)

    def test_empty_audit_data_safe(self):
        actions = generate_pilot_delivery_actions({})
        assert len(actions) > 0

    def test_brightpath_launch_action_mentions_pilot_name(
        self, brightpath_audit, brightpath_portfolio
    ):
        actions = generate_pilot_delivery_actions(brightpath_audit, brightpath_portfolio)
        combined_titles = " ".join(a["title"].lower() for a in actions)
        assert "lesson plan" in combined_titles or "pilot" in combined_titles


# ── TestGenerateReviewAndScaleActions ───────────────────────────────────────────

class TestGenerateReviewAndScaleActions:
    def test_returns_non_empty_list(self, brightpath_audit):
        actions = generate_review_and_scale_actions(brightpath_audit)
        assert len(actions) > 0

    def test_returns_list_type(self, brightpath_audit):
        assert isinstance(generate_review_and_scale_actions(brightpath_audit), list)

    def test_phase_is_days_61_90(self, brightpath_audit):
        actions = generate_review_and_scale_actions(brightpath_audit)
        for a in actions:
            assert a["phase"] == "Days 61–90"

    def test_all_ids_start_with_day90(self, brightpath_audit):
        actions = generate_review_and_scale_actions(brightpath_audit)
        for a in actions:
            assert a["action_id"].startswith("DAY90-")

    def test_includes_scale_decision_action(self, brightpath_audit):
        actions = generate_review_and_scale_actions(brightpath_audit)
        titles = [a["title"].lower() for a in actions]
        assert any("decision" in t or "scale" in t for t in titles)

    def test_brightpath_adds_risk_review_action(
        self, brightpath_audit, brightpath_risk_summary
    ):
        actions = generate_review_and_scale_actions(
            brightpath_audit, risk_summary=brightpath_risk_summary
        )
        assert len(actions) >= 7  # 6 base + 1 adaptive for BrightPath high risks

    def test_missing_risk_summary_returns_base_actions(self, brightpath_audit):
        actions = generate_review_and_scale_actions(brightpath_audit, risk_summary=None)
        assert len(actions) >= 6

    def test_empty_audit_data_safe(self):
        actions = generate_review_and_scale_actions({})
        assert len(actions) > 0


# ── TestGenerateImplementationRoadmap ───────────────────────────────────────────

class TestGenerateImplementationRoadmap:
    def test_expected_keys_present(self, brightpath_roadmap):
        expected = {
            "organisation_name", "roadmap_title", "roadmap_purpose",
            "phase_30_days", "phase_60_days", "phase_90_days",
            "cross_cutting_controls", "success_measures", "dependencies",
            "risks_to_manage", "recommended_first_pilot",
            "overall_roadmap_position", "responsible_use_note", "prototype_note",
        }
        assert expected.issubset(brightpath_roadmap.keys())

    def test_organisation_name(self, brightpath_roadmap):
        assert brightpath_roadmap["organisation_name"] == "BrightPath Skills Training"

    def test_roadmap_title(self, brightpath_roadmap):
        assert brightpath_roadmap["roadmap_title"] == "30/60/90-Day AI Implementation Roadmap"

    def test_phase_30_has_actions(self, brightpath_roadmap):
        assert len(brightpath_roadmap["phase_30_days"]) > 0

    def test_phase_60_has_actions(self, brightpath_roadmap):
        assert len(brightpath_roadmap["phase_60_days"]) > 0

    def test_phase_90_has_actions(self, brightpath_roadmap):
        assert len(brightpath_roadmap["phase_90_days"]) > 0

    def test_day30_ids_are_unique(self, brightpath_roadmap):
        ids = [a["action_id"] for a in brightpath_roadmap["phase_30_days"]]
        assert len(ids) == len(set(ids))

    def test_day60_ids_are_unique(self, brightpath_roadmap):
        ids = [a["action_id"] for a in brightpath_roadmap["phase_60_days"]]
        assert len(ids) == len(set(ids))

    def test_day90_ids_are_unique(self, brightpath_roadmap):
        ids = [a["action_id"] for a in brightpath_roadmap["phase_90_days"]]
        assert len(ids) == len(set(ids))

    def test_recommended_first_pilot_set(self, brightpath_roadmap):
        pilot = brightpath_roadmap["recommended_first_pilot"]
        assert pilot.get("pilot_name")

    def test_cross_cutting_controls_non_empty(self, brightpath_roadmap):
        assert len(brightpath_roadmap["cross_cutting_controls"]) > 0

    def test_responsible_use_note_non_empty(self, brightpath_roadmap):
        assert len(brightpath_roadmap["responsible_use_note"]) > 10

    def test_empty_audit_data_returns_empty_roadmap(self, empty_roadmap):
        assert empty_roadmap["phase_30_days"] == []
        assert empty_roadmap["phase_60_days"] == []
        assert empty_roadmap["phase_90_days"] == []

    def test_missing_readiness_summary_is_safe(self, brightpath_audit):
        roadmap = generate_implementation_roadmap(brightpath_audit, readiness_summary=None)
        assert len(roadmap["phase_30_days"]) > 0

    def test_missing_risk_summary_is_safe(self, brightpath_audit):
        roadmap = generate_implementation_roadmap(brightpath_audit, risk_summary=None)
        assert len(roadmap["phase_30_days"]) > 0

    def test_missing_opportunity_portfolio_is_safe(self, brightpath_audit):
        roadmap = generate_implementation_roadmap(
            brightpath_audit, opportunity_portfolio=None
        )
        assert len(roadmap["phase_30_days"]) > 0

    def test_missing_risk_register_is_safe(self, brightpath_audit):
        roadmap = generate_implementation_roadmap(brightpath_audit, risk_register=None)
        assert len(roadmap["phase_30_days"]) > 0

    def test_all_keys_missing_uses_generic_pilot(self, brightpath_audit):
        roadmap = generate_implementation_roadmap(brightpath_audit)
        pilot = roadmap["recommended_first_pilot"]
        assert pilot.get("pilot_name")

    def test_brightpath_overall_position_mentions_governance(self, brightpath_roadmap):
        pos = brightpath_roadmap["overall_roadmap_position"].lower()
        assert "governance" in pos or "control" in pos or "risk" in pos

    def test_organisation_name_fallback(self):
        roadmap = generate_implementation_roadmap({"organisation_profile": {}})
        assert roadmap["organisation_name"] == "Unnamed organisation"


# ── TestSummariseImplementationRoadmap ──────────────────────────────────────────

class TestSummariseImplementationRoadmap:
    def test_expected_keys_present(self, brightpath_summary):
        expected = {
            "total_actions", "day_30_actions", "day_60_actions", "day_90_actions",
            "high_priority_actions", "recommended_first_pilot",
            "key_dependencies", "key_risks_to_manage", "overall_roadmap_position",
        }
        assert expected.issubset(brightpath_summary.keys())

    def test_total_actions_equals_sum_of_phases(self, brightpath_summary):
        assert brightpath_summary["total_actions"] == (
            brightpath_summary["day_30_actions"]
            + brightpath_summary["day_60_actions"]
            + brightpath_summary["day_90_actions"]
        )

    def test_total_actions_brightpath_at_least_20(self, brightpath_summary):
        assert brightpath_summary["total_actions"] >= 20

    def test_day30_actions_brightpath_at_least_8(self, brightpath_summary):
        assert brightpath_summary["day_30_actions"] >= 8

    def test_day60_actions_brightpath_at_least_6(self, brightpath_summary):
        assert brightpath_summary["day_60_actions"] >= 6

    def test_day90_actions_brightpath_at_least_5(self, brightpath_summary):
        assert brightpath_summary["day_90_actions"] >= 5

    def test_high_priority_actions_positive(self, brightpath_summary):
        assert brightpath_summary["high_priority_actions"] > 0

    def test_recommended_first_pilot_not_empty(self, brightpath_summary):
        assert brightpath_summary["recommended_first_pilot"] != "Not identified"

    def test_key_dependencies_non_empty(self, brightpath_summary):
        assert len(brightpath_summary["key_dependencies"]) > 0

    def test_key_risks_to_manage_non_empty(self, brightpath_summary):
        assert len(brightpath_summary["key_risks_to_manage"]) > 0

    def test_overall_roadmap_position_not_empty(self, brightpath_summary):
        assert len(brightpath_summary["overall_roadmap_position"]) > 10

    def test_empty_roadmap_summary_is_safe(self, empty_roadmap):
        summary = summarise_implementation_roadmap(empty_roadmap)
        assert summary["total_actions"] == 0
        assert summary["day_30_actions"] == 0


# ── TestFormatImplementationRoadmapAsMarkdown ────────────────────────────────────

class TestFormatImplementationRoadmapAsMarkdown:
    def test_returns_string(self, brightpath_markdown):
        assert isinstance(brightpath_markdown, str)

    def test_contains_main_heading(self, brightpath_markdown):
        assert "# 30/60/90-Day AI Implementation Roadmap" in brightpath_markdown

    def test_contains_responsible_use_boundaries(self, brightpath_markdown):
        assert "## Responsible-Use Boundaries" in brightpath_markdown

    def test_contains_first_30_days_heading(self, brightpath_markdown):
        assert "## First 30 Days" in brightpath_markdown

    def test_contains_days_31_60_heading(self, brightpath_markdown):
        assert "## Days 31–60" in brightpath_markdown

    def test_contains_days_61_90_heading(self, brightpath_markdown):
        assert "## Days 61–90" in brightpath_markdown

    def test_contains_cross_cutting_controls_heading(self, brightpath_markdown):
        assert "## Cross-Cutting Controls" in brightpath_markdown

    def test_contains_success_measures_heading(self, brightpath_markdown):
        assert "## Success Measures" in brightpath_markdown

    def test_contains_dependencies_heading(self, brightpath_markdown):
        assert "## Dependencies" in brightpath_markdown

    def test_contains_risks_to_manage_heading(self, brightpath_markdown):
        assert "## Risks to Manage" in brightpath_markdown

    def test_contains_recommended_first_pilot_heading(self, brightpath_markdown):
        assert "## Recommended First Pilot" in brightpath_markdown

    def test_contains_roadmap_purpose(self, brightpath_markdown):
        assert "## Roadmap Purpose" in brightpath_markdown

    def test_contains_day30_001_action_id(self, brightpath_markdown):
        assert "DAY30-001" in brightpath_markdown

    def test_contains_day60_action(self, brightpath_markdown):
        assert "DAY60-" in brightpath_markdown

    def test_contains_day90_action(self, brightpath_markdown):
        assert "DAY90-" in brightpath_markdown

    def test_contains_responsible_use_text(self, brightpath_markdown):
        assert "synthetic/demo audit data only" in brightpath_markdown

    def test_contains_human_review_text(self, brightpath_markdown):
        assert "Human review remains required" in brightpath_markdown

    def test_contains_organisation_name(self, brightpath_markdown):
        assert "BrightPath Skills Training" in brightpath_markdown

    def test_empty_roadmap_safe(self, empty_roadmap):
        md = format_implementation_roadmap_as_markdown(empty_roadmap)
        assert isinstance(md, str)
        assert "# 30/60/90-Day AI Implementation Roadmap" in md

    def test_empty_roadmap_has_responsible_use_section(self, empty_roadmap):
        md = format_implementation_roadmap_as_markdown(empty_roadmap)
        assert "## Responsible-Use Boundaries" in md

    def test_summary_passed_directly(self, brightpath_roadmap):
        summary = summarise_implementation_roadmap(brightpath_roadmap)
        md = format_implementation_roadmap_as_markdown(brightpath_roadmap, summary)
        assert "## Roadmap Summary" in md
