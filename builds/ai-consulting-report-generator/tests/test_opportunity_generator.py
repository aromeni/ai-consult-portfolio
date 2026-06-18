"""Tests for src/opportunity_generator.py — Build 5 Phase 4."""

import pytest
from src.opportunity_generator import (
    normalise_priority_value,
    classify_complexity,
    classify_potential_value,
    classify_pilot_risk,
    calculate_opportunity_score,
    classify_opportunity_priority,
    generate_opportunity_id,
    get_opportunity_priority_colour,
    generate_opportunity_from_workflow_finding,
    generate_pilot_from_recommendation,
    generate_ai_opportunity_portfolio,
    prioritise_opportunities,
    prioritise_pilots,
    summarise_opportunity_portfolio,
    generate_pilot_success_measures,
    generate_responsible_pilot_controls,
    format_opportunity_portfolio_as_markdown,
)
from src.sample_data import get_brightpath_audit_data


# ── Fixtures ────────────────────────────────────────────────────────────────────

@pytest.fixture
def brightpath_audit():
    return get_brightpath_audit_data()


@pytest.fixture
def brightpath_portfolio(brightpath_audit):
    return generate_ai_opportunity_portfolio(brightpath_audit)


@pytest.fixture
def brightpath_summary(brightpath_portfolio):
    return summarise_opportunity_portfolio(brightpath_portfolio)


@pytest.fixture
def brightpath_markdown(brightpath_portfolio, brightpath_summary):
    return format_opportunity_portfolio_as_markdown(brightpath_portfolio, brightpath_summary)


@pytest.fixture
def sample_workflow_finding():
    return {
        "workflow_name": "Course Material Development",
        "current_process": "Tutors draft lesson plans manually.",
        "pain_points": ["High time cost", "Inconsistency"],
        "ai_opportunity": "AI-assisted lesson plan drafts.",
        "risk_level": "Medium",
        "potential_value": "High — could save 3–5 hours per unit",
        "recommended_action": "Run a lesson plan pilot with tutor review.",
    }


@pytest.fixture
def sample_pilot():
    return {
        "pilot_name": "AI-Assisted Lesson Plan Drafts",
        "business_problem": "Tutors spend 8–12 hours creating course units.",
        "proposed_solution": "Approved AI-assisted lesson plan generator.",
        "expected_benefits": ["Reduce drafting time by 40–60%"],
        "complexity": "Low",
        "risk_level": "Low",
        "suggested_timeline": "Month 1–2",
        "success_measures": [
            "Lesson plan drafting time reduced",
            "All tutor sign-offs completed",
        ],
    }


@pytest.fixture
def empty_portfolio():
    return generate_ai_opportunity_portfolio({})


# ── TestNormalisePriorityValue ───────────────────────────────────────────────────

class TestNormalisePriorityValue:
    def test_low_string(self):
        assert normalise_priority_value("Low") == 2

    def test_medium_string(self):
        assert normalise_priority_value("Medium") == 3

    def test_high_string(self):
        assert normalise_priority_value("High") == 4

    def test_very_low_string(self):
        assert normalise_priority_value("Very low") == 1

    def test_very_high_string(self):
        assert normalise_priority_value("Very high") == 5

    def test_case_insensitive_high(self):
        assert normalise_priority_value("HIGH") == 4

    def test_case_insensitive_medium(self):
        assert normalise_priority_value("MEDIUM") == 3

    def test_numeric_int_3(self):
        assert normalise_priority_value(3) == 3

    def test_numeric_float(self):
        assert normalise_priority_value(4.0) == 4

    def test_numeric_clamp_high(self):
        assert normalise_priority_value(10) == 5

    def test_numeric_clamp_low(self):
        assert normalise_priority_value(-1) == 1

    def test_none_defaults_to_medium(self):
        assert normalise_priority_value(None) == 3

    def test_invalid_string_defaults_to_medium(self):
        assert normalise_priority_value("unknown_value") == 3

    def test_high_with_em_dash_description(self):
        assert normalise_priority_value("High — could save 3–5 hours per unit per tutor") == 4

    def test_medium_with_em_dash_description(self):
        assert normalise_priority_value("Medium — reduces report writing time") == 3

    def test_empty_string_defaults_to_medium(self):
        assert normalise_priority_value("") == 3

    def test_numeric_1(self):
        assert normalise_priority_value(1) == 1

    def test_numeric_5(self):
        assert normalise_priority_value(5) == 5


# ── TestClassifyComplexity ───────────────────────────────────────────────────────

class TestClassifyComplexity:
    def test_very_low(self):
        assert classify_complexity("Very low") == "Very low"

    def test_low(self):
        assert classify_complexity("Low") == "Low"

    def test_medium(self):
        assert classify_complexity("Medium") == "Medium"

    def test_high(self):
        assert classify_complexity("High") == "High"

    def test_very_high(self):
        assert classify_complexity("Very high") == "Very high"

    def test_numeric_2(self):
        assert classify_complexity(2) == "Low"

    def test_none_defaults_to_medium(self):
        assert classify_complexity(None) == "Medium"


# ── TestClassifyPotentialValue ───────────────────────────────────────────────────

class TestClassifyPotentialValue:
    def test_very_low(self):
        assert classify_potential_value("Very low") == "Very low"

    def test_low(self):
        assert classify_potential_value("Low") == "Low"

    def test_medium(self):
        assert classify_potential_value("Medium") == "Medium"

    def test_high(self):
        assert classify_potential_value("High") == "High"

    def test_very_high(self):
        assert classify_potential_value("Very high") == "Very high"

    def test_high_with_description(self):
        assert classify_potential_value("High — could save hours") == "High"

    def test_none_defaults_to_medium(self):
        assert classify_potential_value(None) == "Medium"


# ── TestClassifyPilotRisk ────────────────────────────────────────────────────────

class TestClassifyPilotRisk:
    def test_very_low(self):
        assert classify_pilot_risk("Very low") == "Very low"

    def test_low(self):
        assert classify_pilot_risk("Low") == "Low"

    def test_medium(self):
        assert classify_pilot_risk("Medium") == "Medium"

    def test_high(self):
        assert classify_pilot_risk("High") == "High"

    def test_very_high(self):
        assert classify_pilot_risk("Very high") == "Very high"

    def test_none_defaults_to_medium(self):
        assert classify_pilot_risk(None) == "Medium"


# ── TestCalculateOpportunityScore ────────────────────────────────────────────────

class TestCalculateOpportunityScore:
    def test_high_value_low_complexity_low_risk(self):
        # 4*2 - 2 - 2 + 10 = 14
        assert calculate_opportunity_score("High", "Low", "Low") == 14

    def test_all_medium(self):
        # 3*2 - 3 - 3 + 10 = 10
        assert calculate_opportunity_score("Medium", "Medium", "Medium") == 10

    def test_returns_int(self):
        assert isinstance(calculate_opportunity_score("High", "Low", "Low"), int)

    def test_very_high_value_very_low_risk_complexity(self):
        # 5*2 - 1 - 1 + 10 = 18
        assert calculate_opportunity_score("Very high", "Very low", "Very low") == 18

    def test_very_low_value_very_high_risk_complexity(self):
        # 1*2 - 5 - 5 + 10 = 2
        assert calculate_opportunity_score("Very low", "Very high", "Very high") == 2

    def test_result_within_0_and_20(self):
        score = calculate_opportunity_score("Low", "High", "Medium")
        assert 0 <= score <= 20

    def test_numeric_inputs(self):
        # 4*2 - 2 - 2 + 10 = 14
        assert calculate_opportunity_score(4, 2, 2) == 14

    def test_clamp_maximum(self):
        # 5*2 - 1 - 1 + 10 = 18; not exceeding 20
        assert calculate_opportunity_score("Very high", "Very low", "Very low") <= 20

    def test_clamp_minimum(self):
        assert calculate_opportunity_score("Very low", "Very high", "Very high") >= 0

    def test_brightpath_course_material(self):
        # High value (4), Medium complexity (3), Medium risk (3) → 4*2-3-3+10 = 12
        score = calculate_opportunity_score(
            "High — could save 3–5 hours per unit per tutor", "Medium", "Medium"
        )
        assert score == 12

    def test_brightpath_enquiry_low_risk(self):
        # Medium value (3), Medium complexity (3), Low risk (2) → 3*2-3-2+10 = 11
        score = calculate_opportunity_score(
            "Medium — improves responsiveness", "Medium", "Low"
        )
        assert score == 11


# ── TestClassifyOpportunityPriority ─────────────────────────────────────────────

class TestClassifyOpportunityPriority:
    def test_score_0_is_low(self):
        assert classify_opportunity_priority(0) == "Low priority"

    def test_score_6_is_low(self):
        assert classify_opportunity_priority(6) == "Low priority"

    def test_score_7_is_medium(self):
        assert classify_opportunity_priority(7) == "Medium priority"

    def test_score_12_is_medium(self):
        assert classify_opportunity_priority(12) == "Medium priority"

    def test_score_13_is_high(self):
        assert classify_opportunity_priority(13) == "High priority"

    def test_score_16_is_high(self):
        assert classify_opportunity_priority(16) == "High priority"

    def test_score_17_is_strategic(self):
        assert classify_opportunity_priority(17) == "Strategic priority"

    def test_score_20_is_strategic(self):
        assert classify_opportunity_priority(20) == "Strategic priority"

    def test_returns_string(self):
        assert isinstance(classify_opportunity_priority(10), str)


# ── TestGenerateOpportunityId ────────────────────────────────────────────────────

class TestGenerateOpportunityId:
    def test_index_0_gives_opp_001(self):
        assert generate_opportunity_id(0) == "OPP-001"

    def test_index_1_gives_opp_002(self):
        assert generate_opportunity_id(1) == "OPP-002"

    def test_index_9_gives_opp_010(self):
        assert generate_opportunity_id(9) == "OPP-010"

    def test_index_4_gives_opp_005(self):
        assert generate_opportunity_id(4) == "OPP-005"


# ── TestGetOpportunityPriorityColour ────────────────────────────────────────────

class TestGetOpportunityPriorityColour:
    def test_strategic_returns_string(self):
        c = get_opportunity_priority_colour("Strategic priority")
        assert isinstance(c, str) and c.startswith("#")

    def test_high_returns_string(self):
        c = get_opportunity_priority_colour("High priority")
        assert isinstance(c, str) and c.startswith("#")

    def test_medium_returns_string(self):
        c = get_opportunity_priority_colour("Medium priority")
        assert isinstance(c, str) and c.startswith("#")

    def test_low_returns_string(self):
        c = get_opportunity_priority_colour("Low priority")
        assert isinstance(c, str) and c.startswith("#")

    def test_unknown_returns_fallback(self):
        c = get_opportunity_priority_colour("Unknown")
        assert isinstance(c, str) and c.startswith("#")


# ── TestGenerateOpportunityFromWorkflowFinding ──────────────────────────────────

class TestGenerateOpportunityFromWorkflowFinding:
    def test_expected_keys_present(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        expected_keys = {
            "opportunity_id", "workflow_name", "current_process", "pain_points",
            "ai_opportunity", "potential_value", "complexity", "risk_level",
            "value_score", "complexity_score", "risk_score", "opportunity_score",
            "priority", "recommended_action", "responsible_use_controls",
            "success_measures", "source",
        }
        assert expected_keys.issubset(opp.keys())

    def test_opportunity_id_format(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert opp["opportunity_id"] == "OPP-001"

    def test_opportunity_score_is_int(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert isinstance(opp["opportunity_score"], int)

    def test_opportunity_score_in_range(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert 0 <= opp["opportunity_score"] <= 20

    def test_brightpath_course_material_score(self, brightpath_audit):
        finding = brightpath_audit["workflow_findings"][0]
        opp = generate_opportunity_from_workflow_finding(finding, 0)
        assert opp["opportunity_score"] == 12

    def test_brightpath_enquiry_low_risk_score(self, brightpath_audit):
        finding = brightpath_audit["workflow_findings"][2]
        opp = generate_opportunity_from_workflow_finding(finding, 2)
        assert opp["opportunity_score"] == 11

    def test_responsible_use_controls_non_empty(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert len(opp["responsible_use_controls"]) > 0

    def test_success_measures_non_empty(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert len(opp["success_measures"]) > 0

    def test_source_is_synthetic(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert "synthetic" in opp["source"].lower()

    def test_empty_finding_safe(self):
        opp = generate_opportunity_from_workflow_finding({}, 0)
        assert opp["opportunity_id"] == "OPP-001"
        assert opp["opportunity_score"] == 10  # Medium/Medium/Medium = 3*2-3-3+10 = 10

    def test_uses_existing_recommended_action(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert opp["recommended_action"] == sample_workflow_finding["recommended_action"]

    def test_potential_value_label(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert opp["potential_value"] == "High"

    def test_priority_is_string(self, sample_workflow_finding):
        opp = generate_opportunity_from_workflow_finding(sample_workflow_finding, 0)
        assert isinstance(opp["priority"], str)


# ── TestGeneratePilotFromRecommendation ─────────────────────────────────────────

class TestGeneratePilotFromRecommendation:
    def test_expected_keys_present(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        expected_keys = {
            "pilot_id", "pilot_name", "business_problem", "proposed_solution",
            "expected_benefits", "complexity", "risk_level", "suggested_timeline",
            "success_measures", "responsible_use_controls", "pilot_priority",
            "recommended_scope", "human_review_requirements", "source",
        }
        assert expected_keys.issubset(pilot.keys())

    def test_pilot_id_format(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert pilot["pilot_id"] == "PILOT-001"

    def test_pilot_id_index_1(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 1)
        assert pilot["pilot_id"] == "PILOT-002"

    def test_success_measures_non_empty(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert len(pilot["success_measures"]) > 0

    def test_success_measures_includes_existing(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert "Lesson plan drafting time reduced" in pilot["success_measures"]

    def test_responsible_controls_non_empty(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert len(pilot["responsible_use_controls"]) > 0

    def test_human_review_requirements_non_empty(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert len(pilot["human_review_requirements"]) > 0

    def test_pilot_priority_is_string(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert isinstance(pilot["pilot_priority"], str)

    def test_complexity_label_low(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert pilot["complexity"] == "Low"

    def test_risk_level_label_low(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert pilot["risk_level"] == "Low"

    def test_source_is_synthetic(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert "synthetic" in pilot["source"].lower()

    def test_empty_pilot_safe(self):
        pilot = generate_pilot_from_recommendation({}, 0)
        assert pilot["pilot_id"] == "PILOT-001"

    def test_recommended_scope_not_empty(self, sample_pilot):
        pilot = generate_pilot_from_recommendation(sample_pilot, 0)
        assert len(pilot["recommended_scope"]) > 10


# ── TestGenerateAiOpportunityPortfolio ──────────────────────────────────────────

class TestGenerateAiOpportunityPortfolio:
    def test_expected_keys_present(self, brightpath_portfolio):
        expected_keys = {
            "organisation_name", "opportunities", "pilots",
            "recommended_first_pilot", "recommended_pilot_sequence",
            "opportunity_summary", "responsible_use_note", "prototype_note",
        }
        assert expected_keys.issubset(brightpath_portfolio.keys())

    def test_organisation_name(self, brightpath_portfolio):
        assert brightpath_portfolio["organisation_name"] == "BrightPath Skills Training"

    def test_opportunities_count(self, brightpath_portfolio):
        assert len(brightpath_portfolio["opportunities"]) == 4

    def test_pilots_count(self, brightpath_portfolio):
        assert len(brightpath_portfolio["pilots"]) == 3

    def test_recommended_first_pilot_set(self, brightpath_portfolio):
        assert brightpath_portfolio["recommended_first_pilot"] != {}

    def test_recommended_first_pilot_is_safest(self, brightpath_portfolio):
        first = brightpath_portfolio["recommended_first_pilot"]
        assert first.get("complexity") in ("Low", "Very low")

    def test_recommended_pilot_sequence_length(self, brightpath_portfolio):
        assert len(brightpath_portfolio["recommended_pilot_sequence"]) == 3

    def test_pilot_sequence_positions(self, brightpath_portfolio):
        positions = [s["position"] for s in brightpath_portfolio["recommended_pilot_sequence"]]
        assert positions == [1, 2, 3]

    def test_opportunity_summary_populated(self, brightpath_portfolio):
        assert brightpath_portfolio["opportunity_summary"] != {}

    def test_responsible_use_note_non_empty(self, brightpath_portfolio):
        assert len(brightpath_portfolio["responsible_use_note"]) > 10

    def test_prototype_note_non_empty(self, brightpath_portfolio):
        assert len(brightpath_portfolio["prototype_note"]) > 10

    def test_empty_audit_data_returns_portfolio(self):
        portfolio = generate_ai_opportunity_portfolio({})
        assert "opportunities" in portfolio
        assert portfolio["opportunities"] == []

    def test_none_workflow_findings_safe(self):
        portfolio = generate_ai_opportunity_portfolio(
            {"workflow_findings": None, "pilot_recommendations": []}
        )
        assert portfolio["opportunities"] == []

    def test_missing_pilot_recommendations_safe(self):
        portfolio = generate_ai_opportunity_portfolio({"workflow_findings": []})
        assert portfolio["pilots"] == []

    def test_organisation_name_fallback(self):
        portfolio = generate_ai_opportunity_portfolio({"organisation_profile": {}})
        assert portfolio["organisation_name"] == "Unnamed organisation"


# ── TestPrioritiseOpportunities ─────────────────────────────────────────────────

class TestPrioritiseOpportunities:
    def test_sorted_descending_by_score(self):
        opps = [
            {"opportunity_score": 8, "workflow_name": "B"},
            {"opportunity_score": 14, "workflow_name": "A"},
            {"opportunity_score": 10, "workflow_name": "C"},
        ]
        result = prioritise_opportunities(opps)
        assert result[0]["opportunity_score"] == 14
        assert result[1]["opportunity_score"] == 10
        assert result[2]["opportunity_score"] == 8

    def test_empty_input_returns_empty_list(self):
        assert prioritise_opportunities([]) == []

    def test_non_mutating(self):
        opps = [
            {"opportunity_score": 5},
            {"opportunity_score": 15},
        ]
        original_order = [o["opportunity_score"] for o in opps]
        prioritise_opportunities(opps)
        assert [o["opportunity_score"] for o in opps] == original_order

    def test_returns_list(self):
        result = prioritise_opportunities([{"opportunity_score": 10}])
        assert isinstance(result, list)

    def test_brightpath_first_opp_highest_score(self, brightpath_portfolio):
        opps = brightpath_portfolio["opportunities"]
        for i in range(len(opps) - 1):
            assert opps[i]["opportunity_score"] >= opps[i + 1]["opportunity_score"]


# ── TestPrioritisePilots ─────────────────────────────────────────────────────────

class TestPrioritisePilots:
    def test_returns_list(self):
        result = prioritise_pilots([{"complexity": "Low", "risk_level": "Low"}])
        assert isinstance(result, list)

    def test_empty_input_returns_empty_list(self):
        assert prioritise_pilots([]) == []

    def test_safest_pilot_comes_first(self):
        pilots = [
            {"complexity": "High", "risk_level": "High"},
            {"complexity": "Low", "risk_level": "Low"},
            {"complexity": "Medium", "risk_level": "Medium"},
        ]
        result = prioritise_pilots(pilots)
        assert result[0]["complexity"] == "Low"

    def test_brightpath_first_pilot_is_lesson_plan(self, brightpath_portfolio):
        first = brightpath_portfolio["recommended_first_pilot"]
        assert "Lesson Plan" in first.get("pilot_name", "")

    def test_brightpath_highest_complexity_is_last(self, brightpath_portfolio):
        pilots = brightpath_portfolio["pilots"]
        last = pilots[-1]
        assert last.get("complexity") in ("Medium", "High", "Very high")


# ── TestSummariseOpportunityPortfolio ───────────────────────────────────────────

class TestSummariseOpportunityPortfolio:
    def test_expected_keys_present(self, brightpath_summary):
        expected_keys = {
            "total_opportunities", "total_pilots",
            "strategic_priority_opportunities", "high_priority_opportunities",
            "medium_priority_opportunities", "low_priority_opportunities",
            "recommended_first_pilot_name", "overall_opportunity_position",
            "recommended_focus",
        }
        assert expected_keys.issubset(brightpath_summary.keys())

    def test_total_opportunities_brightpath(self, brightpath_summary):
        assert brightpath_summary["total_opportunities"] == 4

    def test_total_pilots_brightpath(self, brightpath_summary):
        assert brightpath_summary["total_pilots"] == 3

    def test_medium_priority_count_brightpath(self, brightpath_summary):
        assert brightpath_summary["medium_priority_opportunities"] == 4

    def test_strategic_priority_zero_brightpath(self, brightpath_summary):
        assert brightpath_summary["strategic_priority_opportunities"] == 0

    def test_high_priority_zero_brightpath(self, brightpath_summary):
        assert brightpath_summary["high_priority_opportunities"] == 0

    def test_recommended_first_pilot_name_not_empty(self, brightpath_summary):
        assert brightpath_summary["recommended_first_pilot_name"] != "None identified"

    def test_overall_opportunity_position_not_empty(self, brightpath_summary):
        assert len(brightpath_summary["overall_opportunity_position"]) > 10

    def test_recommended_focus_non_empty(self, brightpath_summary):
        assert len(brightpath_summary["recommended_focus"]) > 0

    def test_empty_portfolio_returns_safe_defaults(self, empty_portfolio):
        summary = summarise_opportunity_portfolio(empty_portfolio)
        assert summary["total_opportunities"] == 0
        assert summary["total_pilots"] == 0

    def test_empty_portfolio_has_expected_keys(self, empty_portfolio):
        summary = summarise_opportunity_portfolio(empty_portfolio)
        assert "overall_opportunity_position" in summary
        assert "recommended_focus" in summary

    def test_recommended_focus_is_list(self, brightpath_summary):
        assert isinstance(brightpath_summary["recommended_focus"], list)


# ── TestGeneratePilotSuccessMeasures ────────────────────────────────────────────

class TestGeneratePilotSuccessMeasures:
    def test_returns_non_empty_list(self, sample_pilot):
        measures = generate_pilot_success_measures(sample_pilot)
        assert len(measures) > 0

    def test_returns_list_type(self, sample_pilot):
        measures = generate_pilot_success_measures(sample_pilot)
        assert isinstance(measures, list)

    def test_includes_existing_measures(self, sample_pilot):
        measures = generate_pilot_success_measures(sample_pilot)
        assert "Lesson plan drafting time reduced" in measures

    def test_adds_extras_beyond_existing(self, sample_pilot):
        existing = sample_pilot.get("success_measures") or []
        measures = generate_pilot_success_measures(sample_pilot)
        assert len(measures) > len(existing)

    def test_empty_pilot_returns_extras(self):
        measures = generate_pilot_success_measures({})
        assert len(measures) > 0

    def test_no_duplicate_entries(self, sample_pilot):
        measures = generate_pilot_success_measures(sample_pilot)
        assert len(measures) == len(set(measures))


# ── TestGenerateResponsiblePilotControls ────────────────────────────────────────

class TestGenerateResponsiblePilotControls:
    def test_returns_non_empty_list(self, sample_pilot):
        controls = generate_responsible_pilot_controls(sample_pilot)
        assert len(controls) > 0

    def test_returns_list_type(self, sample_pilot):
        controls = generate_responsible_pilot_controls(sample_pilot)
        assert isinstance(controls, list)

    def test_length_at_least_five(self, sample_pilot):
        controls = generate_responsible_pilot_controls(sample_pilot)
        assert len(controls) >= 5

    def test_empty_pilot_returns_standard_controls(self):
        controls = generate_responsible_pilot_controls({})
        assert len(controls) > 0

    def test_learner_report_pilot_gets_extra_control(self):
        pilot = {"pilot_name": "Learner Progress Report Writing"}
        controls = generate_responsible_pilot_controls(pilot)
        assert any("learner" in c.lower() for c in controls)

    def test_quality_pilot_gets_extra_control(self):
        pilot = {"pilot_name": "Quality Report Structure Templates"}
        controls = generate_responsible_pilot_controls(pilot)
        assert any("approved internal" in c.lower() for c in controls)

    def test_safeguarding_pilot_gets_explicit_control(self):
        pilot = {"pilot_name": "Safeguarding Process Support"}
        controls = generate_responsible_pilot_controls(pilot)
        assert any("safeguarding" in c.lower() for c in controls)

    def test_workflow_finding_name_used(self):
        finding = {"workflow_name": "Learner Progress Report Writing"}
        controls = generate_responsible_pilot_controls(finding)
        assert len(controls) > 0


# ── TestFormatOpportunityPortfolioAsMarkdown ─────────────────────────────────────

class TestFormatOpportunityPortfolioAsMarkdown:
    def test_returns_string(self, brightpath_markdown):
        assert isinstance(brightpath_markdown, str)

    def test_contains_main_heading(self, brightpath_markdown):
        assert "# AI Opportunity and Pilot Recommendation Portfolio" in brightpath_markdown

    def test_contains_responsible_use_boundaries(self, brightpath_markdown):
        assert "## Responsible-Use Boundaries" in brightpath_markdown

    def test_contains_opp_001(self, brightpath_markdown):
        assert "OPP-001" in brightpath_markdown

    def test_contains_pilot_001(self, brightpath_markdown):
        assert "PILOT-001" in brightpath_markdown

    def test_contains_opportunity_summary_heading(self, brightpath_markdown):
        assert "## Opportunity Summary" in brightpath_markdown

    def test_contains_pilot_sequence_heading(self, brightpath_markdown):
        assert "## Recommended Pilot Sequence" in brightpath_markdown

    def test_contains_recommended_first_pilot_heading(self, brightpath_markdown):
        assert "## Recommended First Pilot" in brightpath_markdown

    def test_contains_detailed_opportunity_notes(self, brightpath_markdown):
        assert "## Detailed Opportunity Notes" in brightpath_markdown

    def test_contains_detailed_pilot_notes(self, brightpath_markdown):
        assert "## Detailed Pilot Notes" in brightpath_markdown

    def test_contains_responsible_use_text(self, brightpath_markdown):
        assert "synthetic/demo audit data only" in brightpath_markdown

    def test_contains_human_review_text(self, brightpath_markdown):
        assert "Human review remains required" in brightpath_markdown

    def test_contains_organisation_name(self, brightpath_markdown):
        assert "BrightPath Skills Training" in brightpath_markdown

    def test_empty_portfolio_safe(self):
        empty = generate_ai_opportunity_portfolio({})
        md = format_opportunity_portfolio_as_markdown(empty)
        assert isinstance(md, str)
        assert "# AI Opportunity and Pilot Recommendation Portfolio" in md

    def test_empty_portfolio_has_responsible_use_section(self):
        empty = generate_ai_opportunity_portfolio({})
        md = format_opportunity_portfolio_as_markdown(empty)
        assert "## Responsible-Use Boundaries" in md

    def test_summary_passed_directly(self, brightpath_portfolio):
        summary = summarise_opportunity_portfolio(brightpath_portfolio)
        md = format_opportunity_portfolio_as_markdown(brightpath_portfolio, summary)
        assert "## Opportunity Summary" in md
