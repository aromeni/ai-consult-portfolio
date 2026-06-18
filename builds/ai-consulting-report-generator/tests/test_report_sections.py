"""Tests for src/report_sections.py."""

import pytest
from src import report_sections as rs
from src.sample_data import get_brightpath_audit_data

_AUDIT = get_brightpath_audit_data()
_EMPTY = {}

# ── Minimal fixtures for enrichment outputs ───────────────────────────────────

_READINESS = {
    "overall_score": 42,
    "overall_level": "Developing readiness",
    "overall_description": "Some foundations are in place.",
    "ranked_categories": [
        {"label": "Workflow opportunity", "score": 68, "level": "Moderate readiness"},
        {"label": "Leadership alignment", "score": 52, "level": "Developing readiness"},
        {"label": "Staff capability", "score": 45, "level": "Developing readiness"},
        {"label": "Strategy", "score": 32, "level": "Low readiness"},
        {"label": "Data governance", "score": 28, "level": "Low readiness"},
        {"label": "Risk management", "score": 25, "level": "Low readiness"},
    ],
    "strengths": [],
    "gaps": [
        {
            "category": "Risk management",
            "score": 25,
            "risk": "Inadequate controls.",
            "recommended_action": "Complete a risk register.",
        }
    ],
    "strategic_interpretation": "Developing AI readiness with governance gaps.",
    "recommendations": ["Improve governance.", "Build data controls."],
}

_RISK_SUMMARY = {
    "total_risks": 5,
    "critical_risks": 0,
    "high_risks": 4,
    "medium_risks": 1,
    "low_risks": 0,
    "overall_risk_position": "Address risks before scaling.",
    "recommended_focus": ["Resolve 4 high risks.", "Establish data protection controls."],
}

_RISK_REGISTER = [
    {
        "risk_id": "RISK-001",
        "risk_title": "Learner Data in Unapproved AI Tools",
        "risk_category": "Data Protection",
        "risk_level": "High",
        "risk_score": 16,
        "recommended_control": "Prohibit learner data in AI tools.",
        "owner": "Quality and Compliance Lead",
    },
    {
        "risk_id": "RISK-002",
        "risk_title": "No Approved AI Tools List",
        "risk_category": "Governance",
        "risk_level": "High",
        "risk_score": 12,
        "recommended_control": "Establish an approved tools list.",
        "owner": "Senior Leadership Team",
    },
]

_OPP_SUMMARY = {
    "total_opportunities": 4,
    "total_pilots": 3,
    "recommended_first_pilot_name": "AI-Assisted Lesson Plan Drafts",
    "overall_opportunity_position": "Start with narrow pilots.",
    "recommended_focus": ["Plan 4 medium-priority opportunities.", "Start with lesson plan drafts."],
}

_OPP_PORTFOLIO = {
    "recommended_first_pilot": {
        "pilot_name": "AI-Assisted Lesson Plan Drafts",
        "pilot_priority": "Medium priority",
        "complexity": "Low",
        "risk_level": "Low",
        "suggested_timeline": "Month 1–2",
    },
    "recommended_pilot_sequence": [
        {
            "position": 1,
            "pilot_name": "AI-Assisted Lesson Plan Drafts",
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1–2",
        },
        {
            "position": 2,
            "pilot_name": "Email Response Templates",
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1",
        },
    ],
}

_ROADMAP_SUMMARY = {
    "total_actions": 24,
    "day_30_actions": 10,
    "day_60_actions": 7,
    "day_90_actions": 7,
    "high_priority_actions": 15,
    "recommended_first_pilot": "AI-Assisted Lesson Plan Drafts",
    "key_dependencies": ["Staff training must be completed before pilot launch."],
    "key_risks_to_manage": ["Learner data entering AI tools."],
    "overall_roadmap_position": "Governance before scaling.",
}

_ROADMAP = {
    "phase_30_days": [],
    "phase_60_days": [],
    "phase_90_days": [],
}

_SECTION_KEYS = {
    "section_id",
    "section_title",
    "section_purpose",
    "content",
    "key_points",
    "recommendations",
    "source_outputs_used",
    "review_note",
}


# ── Phase 1 Backward-Compatibility Tests ──────────────────────────────────────

class TestGenerateExecutiveSummaryPlaceholder:
    def test_returns_string(self):
        assert isinstance(rs.generate_executive_summary_placeholder(_AUDIT), str)

    def test_non_empty(self):
        assert len(rs.generate_executive_summary_placeholder(_AUDIT)) > 20

    def test_contains_org_name(self):
        assert "BrightPath" in rs.generate_executive_summary_placeholder(_AUDIT)

    def test_contains_heading(self):
        assert "Executive Summary" in rs.generate_executive_summary_placeholder(_AUDIT)

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_executive_summary_placeholder(_EMPTY)
        assert isinstance(result, str)
        assert len(result) > 0


class TestGenerateContextSectionPlaceholder:
    def test_returns_string(self):
        assert isinstance(rs.generate_context_section_placeholder(_AUDIT), str)

    def test_non_empty(self):
        assert len(rs.generate_context_section_placeholder(_AUDIT)) > 20

    def test_contains_org_name(self):
        assert "BrightPath" in rs.generate_context_section_placeholder(_AUDIT)

    def test_contains_heading(self):
        assert "Organisation Context" in rs.generate_context_section_placeholder(_AUDIT)

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_context_section_placeholder(_EMPTY)
        assert isinstance(result, str)


class TestGenerateRiskSectionPlaceholder:
    def test_returns_string(self):
        assert isinstance(rs.generate_risk_section_placeholder(_AUDIT), str)

    def test_non_empty(self):
        assert len(rs.generate_risk_section_placeholder(_AUDIT)) > 20

    def test_contains_heading(self):
        assert "Risk" in rs.generate_risk_section_placeholder(_AUDIT)

    def test_contains_risk_titles(self):
        result = rs.generate_risk_section_placeholder(_AUDIT)
        assert "Learner Data" in result

    def test_empty_audit_returns_no_findings_message(self):
        result = rs.generate_risk_section_placeholder(_EMPTY)
        assert isinstance(result, str)
        assert "No risk findings" in result


class TestGenerateOpportunitySectionPlaceholder:
    def test_returns_string(self):
        assert isinstance(rs.generate_opportunity_section_placeholder(_AUDIT), str)

    def test_non_empty(self):
        assert len(rs.generate_opportunity_section_placeholder(_AUDIT)) > 20

    def test_contains_heading(self):
        assert "Opportunit" in rs.generate_opportunity_section_placeholder(_AUDIT)

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_opportunity_section_placeholder(_EMPTY)
        assert isinstance(result, str)


class TestGenerateRecommendationsSectionPlaceholder:
    def test_returns_string(self):
        assert isinstance(rs.generate_recommendations_section_placeholder(_AUDIT), str)

    def test_non_empty(self):
        assert len(rs.generate_recommendations_section_placeholder(_AUDIT)) > 20

    def test_contains_heading(self):
        assert "Recommendation" in rs.generate_recommendations_section_placeholder(_AUDIT)

    def test_contains_critical_actions(self):
        result = rs.generate_recommendations_section_placeholder(_AUDIT)
        assert "Critical" in result

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_recommendations_section_placeholder(_EMPTY)
        assert isinstance(result, str)


# ── Phase 6: New Section Tests ────────────────────────────────────────────────

class TestGenerateExecutiveSummary:
    def test_returns_dict(self):
        result = rs.generate_executive_summary(_AUDIT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = rs.generate_executive_summary(_AUDIT)
        assert _SECTION_KEYS.issubset(result.keys())

    def test_section_id(self):
        assert rs.generate_executive_summary(_AUDIT)["section_id"] == "executive_summary"

    def test_content_contains_org_name(self):
        result = rs.generate_executive_summary(_AUDIT)
        assert "BrightPath" in result["content"]

    def test_content_mentions_governance(self):
        result = rs.generate_executive_summary(_AUDIT)
        assert "governance" in result["content"].lower()

    def test_with_readiness_summary_uses_score(self):
        result = rs.generate_executive_summary(_AUDIT, readiness_summary=_READINESS)
        assert "42" in result["content"]

    def test_with_risk_summary_mentions_high_risks(self):
        result = rs.generate_executive_summary(_AUDIT, risk_summary=_RISK_SUMMARY)
        assert "4" in result["content"] and "high" in result["content"].lower()

    def test_with_opportunity_summary_mentions_first_pilot(self):
        result = rs.generate_executive_summary(_AUDIT, opportunity_summary=_OPP_SUMMARY)
        assert "Lesson Plan" in result["content"]

    def test_key_points_non_empty(self):
        assert len(rs.generate_executive_summary(_AUDIT)["key_points"]) >= 4

    def test_recommendations_non_empty(self):
        assert len(rs.generate_executive_summary(_AUDIT)["recommendations"]) >= 4

    def test_source_outputs_includes_audit_data(self):
        result = rs.generate_executive_summary(_AUDIT)
        assert "audit_data" in result["source_outputs_used"]

    def test_source_outputs_includes_enrichment_when_provided(self):
        result = rs.generate_executive_summary(
            _AUDIT, readiness_summary=_READINESS, risk_summary=_RISK_SUMMARY
        )
        assert "readiness_summary" in result["source_outputs_used"]
        assert "risk_summary" in result["source_outputs_used"]

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_executive_summary(_EMPTY)
        assert isinstance(result, dict)
        assert result["content"]

    def test_none_audit_does_not_crash(self):
        result = rs.generate_executive_summary(None)
        assert isinstance(result, dict)


class TestGenerateOrganisationContextSection:
    def test_returns_dict(self):
        result = rs.generate_organisation_context_section(_AUDIT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = rs.generate_organisation_context_section(_AUDIT)
        assert _SECTION_KEYS.issubset(result.keys())

    def test_section_id(self):
        assert (
            rs.generate_organisation_context_section(_AUDIT)["section_id"]
            == "organisation_context"
        )

    def test_content_contains_org_name(self):
        result = rs.generate_organisation_context_section(_AUDIT)
        assert "BrightPath" in result["content"]

    def test_content_contains_sector(self):
        result = rs.generate_organisation_context_section(_AUDIT)
        assert "Education" in result["content"]

    def test_content_contains_staff_count(self):
        result = rs.generate_organisation_context_section(_AUDIT)
        assert "24" in result["content"]

    def test_key_points_non_empty(self):
        assert len(rs.generate_organisation_context_section(_AUDIT)["key_points"]) >= 2

    def test_source_outputs_is_audit_data(self):
        result = rs.generate_organisation_context_section(_AUDIT)
        assert result["source_outputs_used"] == ["audit_data"]

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_organisation_context_section(_EMPTY)
        assert isinstance(result, dict)
        assert result["content"]

    def test_none_audit_does_not_crash(self):
        result = rs.generate_organisation_context_section(None)
        assert isinstance(result, dict)


class TestGenerateReadinessInterpretationSection:
    def test_returns_dict(self):
        result = rs.generate_readiness_interpretation_section()
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = rs.generate_readiness_interpretation_section()
        assert _SECTION_KEYS.issubset(result.keys())

    def test_section_id(self):
        assert (
            rs.generate_readiness_interpretation_section()["section_id"]
            == "readiness_interpretation"
        )

    def test_missing_readiness_shows_message(self):
        result = rs.generate_readiness_interpretation_section(None)
        assert "not yet been generated" in result["content"]

    def test_missing_readiness_has_recommendation(self):
        result = rs.generate_readiness_interpretation_section(None)
        assert len(result["recommendations"]) > 0

    def test_with_readiness_summary_shows_score(self):
        result = rs.generate_readiness_interpretation_section(_READINESS)
        assert "42" in result["content"]

    def test_with_readiness_summary_shows_level(self):
        result = rs.generate_readiness_interpretation_section(_READINESS)
        assert "Developing" in result["content"]

    def test_with_readiness_summary_includes_categories(self):
        result = rs.generate_readiness_interpretation_section(_READINESS)
        assert "Workflow opportunity" in result["content"]

    def test_with_readiness_summary_key_points_non_empty(self):
        result = rs.generate_readiness_interpretation_section(_READINESS)
        assert len(result["key_points"]) >= 2

    def test_source_outputs_includes_readiness_summary(self):
        result = rs.generate_readiness_interpretation_section(_READINESS)
        assert "readiness_summary" in result["source_outputs_used"]


class TestGenerateKeyFindingsSection:
    def test_returns_dict(self):
        result = rs.generate_key_findings_section(_AUDIT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        assert _SECTION_KEYS.issubset(rs.generate_key_findings_section(_AUDIT).keys())

    def test_section_id(self):
        assert rs.generate_key_findings_section(_AUDIT)["section_id"] == "key_findings"

    def test_key_points_non_empty(self):
        result = rs.generate_key_findings_section(_AUDIT)
        assert len(result["key_points"]) >= 5

    def test_content_mentions_governance(self):
        result = rs.generate_key_findings_section(_AUDIT)
        assert "governance" in result["content"].lower()

    def test_with_risk_summary_mentions_high_risks(self):
        result = rs.generate_key_findings_section(_AUDIT, risk_summary=_RISK_SUMMARY)
        combined = result["content"] + " ".join(result["key_points"])
        assert "4" in combined or "high" in combined.lower()

    def test_recommendations_non_empty(self):
        assert len(rs.generate_key_findings_section(_AUDIT)["recommendations"]) >= 3

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_key_findings_section(_EMPTY)
        assert isinstance(result, dict)
        assert result["content"]


class TestGenerateRiskSummarySection:
    def test_returns_dict(self):
        assert isinstance(rs.generate_risk_summary_section(), dict)

    def test_has_required_keys(self):
        assert _SECTION_KEYS.issubset(rs.generate_risk_summary_section().keys())

    def test_section_id(self):
        assert rs.generate_risk_summary_section()["section_id"] == "risk_summary"

    def test_missing_data_shows_message(self):
        result = rs.generate_risk_summary_section(None, None)
        assert "not yet been generated" in result["content"]

    def test_with_risk_summary_shows_counts(self):
        result = rs.generate_risk_summary_section(risk_summary=_RISK_SUMMARY)
        assert "5" in result["content"]

    def test_with_risk_summary_shows_high_count(self):
        result = rs.generate_risk_summary_section(risk_summary=_RISK_SUMMARY)
        assert "4" in result["content"]

    def test_with_risk_register_shows_top_risks(self):
        result = rs.generate_risk_summary_section(risk_register=_RISK_REGISTER)
        assert "RISK-001" in result["content"]

    def test_key_points_non_empty_with_data(self):
        result = rs.generate_risk_summary_section(
            _RISK_REGISTER, _RISK_SUMMARY
        )
        assert len(result["key_points"]) >= 2

    def test_source_outputs_with_both(self):
        result = rs.generate_risk_summary_section(_RISK_REGISTER, _RISK_SUMMARY)
        assert "risk_register" in result["source_outputs_used"]
        assert "risk_summary" in result["source_outputs_used"]

    def test_recommendations_non_empty_with_data(self):
        result = rs.generate_risk_summary_section(risk_summary=_RISK_SUMMARY)
        assert len(result["recommendations"]) >= 3


class TestGenerateOpportunitySummarySection:
    def test_returns_dict(self):
        assert isinstance(rs.generate_opportunity_summary_section(), dict)

    def test_has_required_keys(self):
        assert _SECTION_KEYS.issubset(rs.generate_opportunity_summary_section().keys())

    def test_section_id(self):
        assert rs.generate_opportunity_summary_section()["section_id"] == "opportunity_summary"

    def test_missing_data_shows_message(self):
        result = rs.generate_opportunity_summary_section(None, None)
        assert "not yet been generated" in result["content"]

    def test_with_opportunity_summary_shows_counts(self):
        result = rs.generate_opportunity_summary_section(
            opportunity_summary=_OPP_SUMMARY
        )
        assert "4" in result["content"]
        assert "3" in result["content"]

    def test_with_opportunity_summary_shows_first_pilot(self):
        result = rs.generate_opportunity_summary_section(
            opportunity_summary=_OPP_SUMMARY
        )
        assert "Lesson Plan" in result["content"]

    def test_with_portfolio_shows_pilot_sequence(self):
        result = rs.generate_opportunity_summary_section(
            opportunity_portfolio=_OPP_PORTFOLIO,
            opportunity_summary=_OPP_SUMMARY,
        )
        assert "Email Response" in result["content"]

    def test_key_points_non_empty_with_data(self):
        result = rs.generate_opportunity_summary_section(
            opportunity_summary=_OPP_SUMMARY
        )
        assert len(result["key_points"]) >= 3

    def test_source_outputs_with_both(self):
        result = rs.generate_opportunity_summary_section(
            _OPP_PORTFOLIO, _OPP_SUMMARY
        )
        assert "opportunity_portfolio" in result["source_outputs_used"]
        assert "opportunity_summary" in result["source_outputs_used"]


class TestGenerateRoadmapSummarySection:
    def test_returns_dict(self):
        assert isinstance(rs.generate_roadmap_summary_section(), dict)

    def test_has_required_keys(self):
        assert _SECTION_KEYS.issubset(rs.generate_roadmap_summary_section().keys())

    def test_section_id(self):
        assert rs.generate_roadmap_summary_section()["section_id"] == "roadmap_summary"

    def test_missing_data_shows_message(self):
        result = rs.generate_roadmap_summary_section(None, None)
        assert "not yet been generated" in result["content"]

    def test_with_roadmap_summary_shows_total_actions(self):
        result = rs.generate_roadmap_summary_section(roadmap_summary=_ROADMAP_SUMMARY)
        assert "24" in result["content"]

    def test_with_roadmap_summary_shows_phase_actions(self):
        result = rs.generate_roadmap_summary_section(roadmap_summary=_ROADMAP_SUMMARY)
        assert "10" in result["content"]
        assert "7" in result["content"]

    def test_with_roadmap_summary_shows_first_pilot(self):
        result = rs.generate_roadmap_summary_section(roadmap_summary=_ROADMAP_SUMMARY)
        assert "Lesson Plan" in result["content"]

    def test_key_points_non_empty_with_data(self):
        result = rs.generate_roadmap_summary_section(roadmap_summary=_ROADMAP_SUMMARY)
        assert len(result["key_points"]) >= 4

    def test_source_outputs_with_both(self):
        result = rs.generate_roadmap_summary_section(_ROADMAP, _ROADMAP_SUMMARY)
        assert "implementation_roadmap" in result["source_outputs_used"]
        assert "roadmap_summary" in result["source_outputs_used"]


class TestGenerateTrainingNeedsSection:
    def test_returns_dict(self):
        result = rs.generate_training_needs_section(_AUDIT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        assert _SECTION_KEYS.issubset(rs.generate_training_needs_section(_AUDIT).keys())

    def test_section_id(self):
        assert rs.generate_training_needs_section(_AUDIT)["section_id"] == "training_needs"

    def test_content_contains_training_topics(self):
        result = rs.generate_training_needs_section(_AUDIT)
        assert "Responsible AI" in result["content"]

    def test_content_mentions_build4(self):
        result = rs.generate_training_needs_section(_AUDIT)
        assert "Build 4" in result["content"]

    def test_key_points_non_empty(self):
        assert len(rs.generate_training_needs_section(_AUDIT)["key_points"]) >= 2

    def test_recommendations_non_empty(self):
        assert len(rs.generate_training_needs_section(_AUDIT)["recommendations"]) >= 3

    def test_source_outputs_is_audit_data(self):
        assert rs.generate_training_needs_section(_AUDIT)["source_outputs_used"] == ["audit_data"]

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_training_needs_section(_EMPTY)
        assert isinstance(result, dict)
        assert result["content"]


class TestGenerateGovernanceRecommendationsSection:
    def test_returns_dict(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert _SECTION_KEYS.issubset(result.keys())

    def test_section_id(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert result["section_id"] == "governance_recommendations"

    def test_recommendations_at_least_ten(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert len(result["recommendations"]) >= 10

    def test_content_contains_governance_gaps(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert "No AI Use Policy" in result["content"]

    def test_content_mentions_data_boundaries(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert "data" in result["content"].lower()

    def test_source_outputs_includes_audit_data(self):
        result = rs.generate_governance_recommendations_section(_AUDIT)
        assert "audit_data" in result["source_outputs_used"]

    def test_enrichment_sources_added_when_provided(self):
        result = rs.generate_governance_recommendations_section(
            _AUDIT, risk_summary=_RISK_SUMMARY, readiness_summary=_READINESS
        )
        assert "risk_summary" in result["source_outputs_used"]
        assert "readiness_summary" in result["source_outputs_used"]

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_governance_recommendations_section(_EMPTY)
        assert isinstance(result, dict)


class TestGenerateImmediateNextStepsSection:
    def test_returns_dict(self):
        result = rs.generate_immediate_next_steps_section(_AUDIT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = rs.generate_immediate_next_steps_section(_AUDIT)
        assert _SECTION_KEYS.issubset(result.keys())

    def test_section_id(self):
        result = rs.generate_immediate_next_steps_section(_AUDIT)
        assert result["section_id"] == "immediate_next_steps"

    def test_recommendations_non_empty(self):
        result = rs.generate_immediate_next_steps_section(_AUDIT)
        assert len(result["recommendations"]) >= 7

    def test_content_mentions_pilot(self):
        result = rs.generate_immediate_next_steps_section(_AUDIT)
        assert "pilot" in result["content"].lower()

    def test_with_opportunity_summary_uses_pilot_name(self):
        result = rs.generate_immediate_next_steps_section(
            _AUDIT, opportunity_summary=_OPP_SUMMARY
        )
        assert "Lesson Plan" in result["content"]

    def test_key_points_non_empty(self):
        assert len(rs.generate_immediate_next_steps_section(_AUDIT)["key_points"]) >= 4

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_immediate_next_steps_section(_EMPTY)
        assert isinstance(result, dict)


class TestGenerateResponsibleUseSection:
    def test_returns_dict(self):
        result = rs.generate_responsible_use_section()
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        assert _SECTION_KEYS.issubset(rs.generate_responsible_use_section().keys())

    def test_section_id(self):
        assert rs.generate_responsible_use_section()["section_id"] == "responsible_use"

    def test_content_mentions_synthetic_data(self):
        result = rs.generate_responsible_use_section()
        assert "synthetic" in result["content"].lower()

    def test_content_mentions_human_review(self):
        result = rs.generate_responsible_use_section()
        assert "human review" in result["content"].lower()

    def test_content_mentions_no_legal_advice(self):
        result = rs.generate_responsible_use_section()
        assert "legal" in result["content"].lower()

    def test_content_mentions_safeguarding(self):
        result = rs.generate_responsible_use_section()
        assert "safeguarding" in result["content"].lower()

    def test_key_points_non_empty(self):
        assert len(rs.generate_responsible_use_section()["key_points"]) >= 4

    def test_recommendations_non_empty(self):
        assert len(rs.generate_responsible_use_section()["recommendations"]) >= 3

    def test_source_outputs_empty(self):
        assert rs.generate_responsible_use_section()["source_outputs_used"] == []


class TestGenerateAllReportSections:
    def test_returns_dict(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert isinstance(result, dict)

    def test_has_organisation_name(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_has_report_title(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert "AI Readiness" in result["report_title"]

    def test_sections_key_present(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert "sections" in result
        assert isinstance(result["sections"], dict)

    def test_all_eleven_sections_present(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert len(result["sections"]) == 11

    def test_section_order_length(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert len(result["section_order"]) == 11

    def test_source_outputs_available_has_five_keys(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert len(result["source_outputs_available"]) == 5

    def test_audit_data_marked_available(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert result["source_outputs_available"]["audit_data"] is True

    def test_missing_outputs_marked_false(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert result["source_outputs_available"]["readiness_summary"] is False
        assert result["source_outputs_available"]["risk_register"] is False

    def test_enrichment_outputs_marked_true(self):
        result = rs.generate_all_report_sections(
            _AUDIT,
            readiness_summary=_READINESS,
            risk_register=_RISK_REGISTER,
        )
        assert result["source_outputs_available"]["readiness_summary"] is True
        assert result["source_outputs_available"]["risk_register"] is True

    def test_prototype_note_present(self):
        result = rs.generate_all_report_sections(_AUDIT)
        assert result["prototype_note"]

    def test_empty_audit_does_not_crash(self):
        result = rs.generate_all_report_sections(_EMPTY)
        assert isinstance(result, dict)
        assert len(result["sections"]) == 11

    def test_all_none_inputs_does_not_crash(self):
        result = rs.generate_all_report_sections(None)
        assert isinstance(result, dict)


class TestSummariseReportSections:
    def _make_report(self, with_enrichment=False):
        kwargs = {"audit_data": _AUDIT}
        if with_enrichment:
            kwargs.update(
                readiness_summary=_READINESS,
                risk_register=_RISK_REGISTER,
                risk_summary=_RISK_SUMMARY,
                opportunity_portfolio=_OPP_PORTFOLIO,
                opportunity_summary=_OPP_SUMMARY,
                implementation_roadmap=_ROADMAP,
                roadmap_summary=_ROADMAP_SUMMARY,
            )
        return rs.generate_all_report_sections(**kwargs)

    def test_returns_dict(self):
        report = self._make_report()
        assert isinstance(rs.summarise_report_sections(report), dict)

    def test_has_required_keys(self):
        result = rs.summarise_report_sections(self._make_report())
        expected = {
            "total_sections",
            "sections_with_content",
            "source_outputs_used",
            "missing_source_outputs",
            "review_required",
            "overall_report_readiness",
        }
        assert expected.issubset(result.keys())

    def test_total_sections_is_eleven(self):
        result = rs.summarise_report_sections(self._make_report())
        assert result["total_sections"] == 11

    def test_sections_with_content_is_eleven(self):
        result = rs.summarise_report_sections(self._make_report())
        assert result["sections_with_content"] == 11

    def test_review_required_is_true(self):
        result = rs.summarise_report_sections(self._make_report())
        assert result["review_required"] is True

    def test_source_outputs_used_is_list(self):
        result = rs.summarise_report_sections(self._make_report())
        assert isinstance(result["source_outputs_used"], list)

    def test_audit_data_in_source_outputs_used(self):
        result = rs.summarise_report_sections(self._make_report())
        assert "audit_data" in result["source_outputs_used"]

    def test_missing_source_outputs_with_audit_only(self):
        result = rs.summarise_report_sections(self._make_report())
        missing = result["missing_source_outputs"]
        assert "readiness_summary" in missing or "risk_register" in missing

    def test_no_missing_outputs_when_all_provided(self):
        result = rs.summarise_report_sections(self._make_report(with_enrichment=True))
        assert result["missing_source_outputs"] == []

    def test_readiness_message_when_all_present(self):
        result = rs.summarise_report_sections(self._make_report(with_enrichment=True))
        assert "ready to be assembled" in result["overall_report_readiness"]

    def test_readiness_message_when_missing(self):
        result = rs.summarise_report_sections(self._make_report())
        assert "stronger" in result["overall_report_readiness"]

    def test_empty_dict_does_not_crash(self):
        result = rs.summarise_report_sections({})
        assert isinstance(result, dict)


class TestFormatReportSectionsAsMarkdown:
    def _make_report(self):
        return rs.generate_all_report_sections(_AUDIT)

    def test_returns_string(self):
        assert isinstance(rs.format_report_sections_as_markdown(self._make_report()), str)

    def test_non_empty(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert len(result) > 200

    def test_contains_main_heading(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "# AI Consulting Report Sections" in result

    def test_contains_executive_summary(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Executive Summary" in result

    def test_contains_org_context(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Organisation Context" in result

    def test_contains_key_findings(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Key Findings" in result

    def test_contains_risk_summary(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Risk Summary" in result

    def test_contains_opportunity_summary(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Opportunity and Pilot Summary" in result

    def test_contains_roadmap_summary(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## 30/60/90-Day Roadmap Summary" in result

    def test_contains_responsible_use_boundaries(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Responsible-Use Boundaries" in result

    def test_contains_source_outputs_section(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Source Outputs Used" in result

    def test_contains_org_name(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "BrightPath" in result

    def test_contains_governance_recommendations(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Governance Recommendations" in result

    def test_contains_immediate_next_steps(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "## Immediate Next Steps" in result

    def test_contains_prototype_note(self):
        result = rs.format_report_sections_as_markdown(self._make_report())
        assert "prototype" in result.lower()

    def test_empty_dict_does_not_crash(self):
        result = rs.format_report_sections_as_markdown({})
        assert isinstance(result, str)
