"""Tests for src/report_builder.py — Build 5 Phase 7."""

import pytest

from src.sample_data import get_brightpath_audit_data
from src import report_builder as rb

# ── Module-level fixtures ──────────────────────────────────────────────────────

_AUDIT = get_brightpath_audit_data()

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
    "category_scores": [
        {"label": "Strategy", "score": 32, "level": "Low readiness", "interpretation": "..."},
        {"label": "Data Governance", "score": 28, "level": "Low readiness", "interpretation": "..."},
    ],
    "strengths": [],
    "gaps": [
        {"category": "Risk management", "score": 25, "risk": "...", "recommended_action": "..."},
    ],
    "strategic_interpretation": "BrightPath shows developing AI readiness.",
    "recommendations": ["Improve governance.", "Build data controls."],
    "responsible_use_note": "Synthetic data only.",
    "prototype_note": "Human review required.",
}

_RISK_SUMMARY = {
    "total_risks": 5,
    "critical_risks": 0,
    "high_risks": 4,
    "medium_risks": 1,
    "low_risks": 0,
    "overall_risk_position": "Address risks before scaling.",
    "recommended_focus": ["Resolve 4 high risks.", "Establish data protection controls."],
    "highest_risk": {
        "risk_id": "RISK-001",
        "risk_title": "Learner Data in Unapproved AI Tools",
        "risk_level": "High",
        "risk_score": 16,
        "likelihood": "High",
        "impact": "High",
    },
}

_RISK_REGISTER = [
    {
        "risk_id": "RISK-001",
        "risk_title": "Learner Data in Unapproved AI Tools",
        "risk_category": "Data Protection",
        "risk_level": "High",
        "risk_score": 16,
        "likelihood": "High",
        "likelihood_score": 4,
        "impact": "High",
        "impact_score": 4,
        "recommended_control": "Prohibit learner data in AI tools.",
        "owner": "Quality and Compliance Lead",
        "status": "Open",
        "priority_action": "Address before scaling.",
        "review_frequency": "Monthly",
        "description": "Staff entering learner data into unapproved AI systems.",
    },
    {
        "risk_id": "RISK-002",
        "risk_title": "Absence of AI Use Policy",
        "risk_category": "Governance",
        "risk_level": "High",
        "risk_score": 12,
        "likelihood": "High",
        "likelihood_score": 4,
        "impact": "Medium",
        "impact_score": 3,
        "recommended_control": "Draft and approve an AI Use Policy.",
        "owner": "Senior Leadership Team",
        "status": "Open",
        "priority_action": "Address before scaling.",
        "review_frequency": "Monthly",
        "description": "No formal AI Use Policy is in place.",
    },
]

_OPP_SUMMARY = {
    "total_opportunities": 4,
    "total_pilots": 3,
    "strategic_priority_opportunities": 0,
    "high_priority_opportunities": 0,
    "recommended_first_pilot_name": "AI-Assisted Lesson Plan Drafts",
    "overall_opportunity_position": "Start with narrow pilots.",
    "recommended_focus": ["Plan 4 medium-priority opportunities.", "Start with lesson plan drafts."],
}

_OPP_PORTFOLIO = {
    "recommended_first_pilot": {
        "pilot_id": "PILOT-001",
        "pilot_name": "AI-Assisted Lesson Plan Drafts",
        "pilot_priority": "Medium",
        "complexity": "Low",
        "risk_level": "Low",
        "suggested_timeline": "Month 1–2",
    },
    "recommended_pilot_sequence": [
        {
            "position": 1,
            "pilot_name": "AI-Assisted Lesson Plan Drafts",
            "pilot_priority": "Medium",
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1–2",
        },
        {
            "position": 2,
            "pilot_name": "Email Response Templates",
            "pilot_priority": "Medium",
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 2–3",
        },
    ],
    "opportunities": [
        {
            "opportunity_id": "OPP-001",
            "workflow_name": "Course Material Development",
            "priority": "Medium",
            "opportunity_score": 12,
            "ai_opportunity": "AI-assisted first-draft generation.",
            "potential_value": "High",
            "value_score": 4,
            "complexity": "Medium",
            "complexity_score": 3,
            "risk_level": "Medium",
            "risk_score": 3,
            "recommended_action": "Run a controlled pilot.",
            "success_measures": ["Time saved per lesson plan."],
            "responsible_use_controls": ["Human review required."],
        }
    ],
    "pilots": [
        {
            "pilot_id": "PILOT-001",
            "pilot_name": "AI-Assisted Lesson Plan Drafts",
            "pilot_priority": "Medium",
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1–2",
            "business_problem": "Tutors spend 8–12 hours creating course units.",
            "proposed_solution": "AI draft, then tutor review.",
            "expected_benefits": ["Reduce drafting time by 40%."],
            "recommended_scope": "One tutor team.",
            "success_measures": ["40% time reduction."],
            "responsible_use_controls": ["No real learner data."],
            "human_review_requirements": ["All outputs reviewed before use."],
        }
    ],
}

_ROADMAP_SUMMARY = {
    "total_actions": 24,
    "day_30_actions": 10,
    "day_60_actions": 7,
    "day_90_actions": 7,
    "high_priority_actions": 15,
    "recommended_first_pilot": "AI-Assisted Lesson Plan Drafts",
    "key_dependencies": ["AI Use Policy must be approved first."],
    "key_risks_to_manage": ["Staff using AI before training."],
    "overall_roadmap_position": "Governance before scaling.",
}

_IMPLEMENTATION_ROADMAP = {
    "organisation_name": "BrightPath Skills Training",
    "phase_30_days": [
        {
            "action_id": "DAY30-001",
            "title": "Assign governance owner",
            "priority": "High",
            "description": "Assign a named AI governance owner.",
            "owner": "Senior Leadership Team",
            "success_measure": "Named owner confirmed.",
            "dependency": None,
            "risk_reduction": "Reduces governance risk.",
            "related_output": None,
        }
    ],
    "phase_60_days": [
        {
            "action_id": "DAY60-001",
            "title": "Deliver staff training",
            "priority": "High",
            "description": "Deliver responsible AI use training to all staff.",
            "owner": "HR / L&D Lead",
            "success_measure": "All staff trained.",
            "dependency": "AI Use Policy approved.",
            "risk_reduction": "Reduces misuse risk.",
            "related_output": None,
        }
    ],
    "phase_90_days": [
        {
            "action_id": "DAY90-001",
            "title": "Review pilot outcomes",
            "priority": "High",
            "description": "Review first pilot evidence before scaling.",
            "owner": "Senior Leadership Team",
            "success_measure": "Pilot review completed.",
            "dependency": "Pilot completed.",
            "risk_reduction": "Evidence-based scaling.",
            "related_output": None,
        }
    ],
    "cross_cutting_controls": ["Human review at every step."],
    "success_measures": ["Governance owner confirmed by Day 30."],
    "dependencies": ["AI Use Policy approved before pilot."],
    "risks_to_manage": ["Staff using AI before training."],
    "recommended_first_pilot": {
        "pilot_name": "AI-Assisted Lesson Plan Drafts",
        "complexity": "Low",
        "risk_level": "Low",
        "suggested_timeline": "Month 1–2",
    },
}

_REPORT_SECTIONS = {
    "organisation_name": "BrightPath Skills Training",
    "report_title": "AI Readiness and Responsible AI Adoption Report",
    "sections": {
        "executive_summary": {
            "section_id": "executive_summary",
            "section_title": "Executive Summary",
            "section_purpose": "High-level overview.",
            "content": "BrightPath is beginning to explore AI adoption.",
            "key_points": ["Score: 42/100.", "4 high risks identified."],
            "recommendations": ["Strengthen governance.", "Run a controlled pilot."],
            "source_outputs_used": ["audit_data", "readiness_summary"],
            "review_note": "Human review required.",
        },
        "organisation_context": {
            "section_id": "organisation_context",
            "section_title": "Organisation Context",
            "section_purpose": "Describes the organisation.",
            "content": "BrightPath is a private training provider in Education and Training.",
            "key_points": ["24 staff.", "Informal ChatGPT use."],
            "recommendations": [],
            "source_outputs_used": ["audit_data"],
            "review_note": "Human review required.",
        },
    },
    "section_order": ["executive_summary", "organisation_context"],
    "source_outputs_available": {
        "audit_data": True,
        "readiness_summary": True,
        "risk_register": True,
        "opportunity_portfolio": True,
        "implementation_roadmap": True,
    },
    "prototype_note": "Deterministic prototype.",
}

_FULL_SESSION = {
    "audit_data": _AUDIT,
    "readiness_summary": _READINESS,
    "risk_register": _RISK_REGISTER,
    "risk_register_summary": _RISK_SUMMARY,
    "opportunity_portfolio": _OPP_PORTFOLIO,
    "opportunity_summary": _OPP_SUMMARY,
    "implementation_roadmap": _IMPLEMENTATION_ROADMAP,
    "implementation_roadmap_summary": _ROADMAP_SUMMARY,
    "report_sections": _REPORT_SECTIONS,
}


# ── TestGetSectionLists ────────────────────────────────────────────────────────

class TestGetSectionLists:
    def test_required_sections_non_empty(self):
        result = rb.get_client_report_required_sections()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_required_sections_contains_executive_summary(self):
        assert "executive_summary" in rb.get_client_report_required_sections()

    def test_optional_sections_non_empty(self):
        result = rb.get_client_report_optional_sections()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_optional_sections_contains_readiness(self):
        assert "readiness_summary" in rb.get_client_report_optional_sections()

    def test_required_and_optional_disjoint(self):
        req = set(rb.get_client_report_required_sections())
        opt = set(rb.get_client_report_optional_sections())
        assert not req.intersection(opt)


# ── TestCheckClientReportReadiness ────────────────────────────────────────────

class TestCheckClientReportReadiness:
    def test_empty_session_state_is_not_ready(self):
        result = rb.check_client_report_readiness({})
        assert result["is_ready"] is False

    def test_empty_session_state_has_next_steps(self):
        result = rb.check_client_report_readiness({})
        assert len(result["recommended_next_steps"]) > 0

    def test_none_session_state_is_not_ready(self):
        result = rb.check_client_report_readiness(None)
        assert result["is_ready"] is False

    def test_with_audit_data_is_ready(self):
        result = rb.check_client_report_readiness({"audit_data": _AUDIT})
        assert result["is_ready"] is True

    def test_with_audit_data_detects_missing_recommended(self):
        result = rb.check_client_report_readiness({"audit_data": _AUDIT})
        assert len(result["missing_sections"]) > 0

    def test_full_session_has_available_sections(self):
        result = rb.check_client_report_readiness(_FULL_SESSION)
        assert len(result["available_sections"]) > 0

    def test_full_session_missing_is_empty_or_small(self):
        result = rb.check_client_report_readiness(_FULL_SESSION)
        assert len(result["missing_sections"]) == 0

    def test_result_has_required_keys(self):
        result = rb.check_client_report_readiness({})
        assert "is_ready" in result
        assert "available_sections" in result
        assert "missing_sections" in result
        assert "recommended_next_steps" in result

    def test_available_sections_is_list(self):
        result = rb.check_client_report_readiness(_FULL_SESSION)
        assert isinstance(result["available_sections"], list)

    def test_missing_sections_is_list(self):
        result = rb.check_client_report_readiness({})
        assert isinstance(result["missing_sections"], list)


# ── TestBuildClientReportData ─────────────────────────────────────────────────

class TestBuildClientReportData:
    def _build(self, ss=None):
        return rb.build_client_report_data_from_session_state(ss or _FULL_SESSION)

    def test_returns_dict(self):
        assert isinstance(self._build(), dict)

    def test_has_report_title(self):
        result = self._build()
        assert "report_title" in result
        assert result["report_title"]

    def test_has_organisation_name(self):
        result = self._build()
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_has_generated_date(self):
        result = self._build()
        assert "generated_date" in result
        assert result["generated_date"]

    def test_has_source_outputs_available(self):
        result = self._build()
        assert "source_outputs_available" in result
        assert isinstance(result["source_outputs_available"], dict)

    def test_has_responsible_use_note(self):
        result = self._build()
        assert "responsible_use_note" in result
        assert "synthetic" in result["responsible_use_note"].lower()

    def test_has_prototype_note(self):
        result = self._build()
        assert "prototype_note" in result

    def test_handles_empty_session_state(self):
        result = rb.build_client_report_data_from_session_state({})
        assert result["organisation_name"] == "Unnamed organisation"

    def test_handles_none_session_state(self):
        result = rb.build_client_report_data_from_session_state(None)
        assert isinstance(result, dict)

    def test_audit_data_key_present(self):
        result = self._build()
        assert "audit_data" in result

    def test_source_outputs_audit_data_true(self):
        result = self._build()
        assert result["source_outputs_available"]["audit_data"] is True

    def test_source_outputs_all_true_for_full_session(self):
        result = self._build()
        assert all(result["source_outputs_available"].values())


# ── TestGenerateReportCoverSection ────────────────────────────────────────────

class TestGenerateReportCoverSection:
    def _data(self):
        return rb.build_client_report_data_from_session_state(_FULL_SESSION)

    def test_returns_string(self):
        assert isinstance(rb.generate_report_cover_section(self._data()), str)

    def test_contains_org_name(self):
        result = rb.generate_report_cover_section(self._data())
        assert "BrightPath" in result

    def test_contains_report_title(self):
        result = rb.generate_report_cover_section(self._data())
        assert "AI Readiness" in result

    def test_contains_generated_date(self):
        result = rb.generate_report_cover_section(self._data())
        assert "Generated Date" in result

    def test_contains_prototype_status(self):
        result = rb.generate_report_cover_section(self._data())
        assert "prototype" in result.lower()

    def test_handles_empty_data(self):
        result = rb.generate_report_cover_section({})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_staff_count(self):
        result = rb.generate_report_cover_section(self._data())
        assert "24" in result


# ── TestGenerateReportTableOfContents ─────────────────────────────────────────

class TestGenerateReportTableOfContents:
    def _data(self):
        return rb.build_client_report_data_from_session_state(_FULL_SESSION)

    def test_returns_string(self):
        assert isinstance(rb.generate_report_table_of_contents(self._data()), str)

    def test_contains_executive_summary(self):
        result = rb.generate_report_table_of_contents(self._data())
        assert "Executive Summary" in result

    def test_contains_responsible_use(self):
        result = rb.generate_report_table_of_contents(self._data())
        assert "Responsible-Use" in result

    def test_omits_excluded_section(self):
        result = rb.generate_report_table_of_contents(
            self._data(), include_sections={"appendices": False}
        )
        assert "Appendices" not in result

    def test_default_includes_all(self):
        result = rb.generate_report_table_of_contents(self._data())
        assert "Appendices" in result

    def test_handles_empty_data(self):
        result = rb.generate_report_table_of_contents({})
        assert isinstance(result, str)


# ── TestGenerateReportExecutiveSummarySection ─────────────────────────────────

class TestGenerateReportExecutiveSummarySection:
    def _data(self):
        return rb.build_client_report_data_from_session_state(_FULL_SESSION)

    def test_returns_string(self):
        assert isinstance(rb.generate_report_executive_summary_section(self._data()), str)

    def test_non_empty(self):
        result = rb.generate_report_executive_summary_section(self._data())
        assert len(result) > 0

    def test_uses_report_sections_content_when_available(self):
        result = rb.generate_report_executive_summary_section(self._data())
        assert "BrightPath" in result

    def test_fallback_without_report_sections(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_executive_summary_section(data)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_handles_empty_data(self):
        result = rb.generate_report_executive_summary_section({})
        assert isinstance(result, str)


# ── TestGenerateReportContextSection ─────────────────────────────────────────

class TestGenerateReportContextSection:
    def _data(self):
        return rb.build_client_report_data_from_session_state(_FULL_SESSION)

    def test_returns_string(self):
        assert isinstance(rb.generate_report_context_section(self._data()), str)

    def test_non_empty(self):
        result = rb.generate_report_context_section(self._data())
        assert len(result) > 0

    def test_uses_report_sections_when_available(self):
        result = rb.generate_report_context_section(self._data())
        assert "BrightPath" in result or "training" in result.lower()

    def test_fallback_from_audit_data(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_context_section(data)
        assert "BrightPath" in result or "Training" in result

    def test_handles_empty_data(self):
        result = rb.generate_report_context_section({})
        assert isinstance(result, str)


# ── TestGenerateReportReadinessSection ────────────────────────────────────────

class TestGenerateReportReadinessSection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_readiness_section(data), str)

    def test_handles_missing_readiness_summary(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_readiness_section(data)
        assert "not available" in result.lower() or "run" in result.lower()

    def test_includes_score_when_available(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_readiness_section(data)
        assert "42" in result or "Developing" in result

    def test_handles_empty_data(self):
        result = rb.generate_report_readiness_section({})
        assert isinstance(result, str)

    def test_non_empty(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert len(rb.generate_report_readiness_section(data)) > 0


# ── TestGenerateReportRiskSection ─────────────────────────────────────────────

class TestGenerateReportRiskSection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_risk_section(data), str)

    def test_handles_missing_risk_register(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_risk_section(data)
        assert "not available" in result.lower() or "run" in result.lower()

    def test_includes_total_risks_when_available(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_risk_section(data)
        assert "5" in result or "Risk" in result

    def test_handles_empty_data(self):
        result = rb.generate_report_risk_section({})
        assert isinstance(result, str)

    def test_non_empty(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert len(rb.generate_report_risk_section(data)) > 0


# ── TestGenerateReportOpportunitySection ──────────────────────────────────────

class TestGenerateReportOpportunitySection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_opportunity_section(data), str)

    def test_handles_missing_opportunity_portfolio(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_opportunity_section(data)
        assert "not available" in result.lower() or "run" in result.lower()

    def test_includes_pilot_name_when_available(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_opportunity_section(data)
        assert "Lesson Plan" in result or "pilot" in result.lower()

    def test_handles_empty_data(self):
        result = rb.generate_report_opportunity_section({})
        assert isinstance(result, str)


# ── TestGenerateReportRoadmapSection ──────────────────────────────────────────

class TestGenerateReportRoadmapSection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_roadmap_section(data), str)

    def test_handles_missing_roadmap(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_roadmap_section(data)
        assert "not available" in result.lower() or "run" in result.lower()

    def test_includes_total_actions_when_available(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_roadmap_section(data)
        assert "24" in result or "action" in result.lower()

    def test_handles_empty_data(self):
        result = rb.generate_report_roadmap_section({})
        assert isinstance(result, str)


# ── TestGenerateReportTrainingSection ─────────────────────────────────────────

class TestGenerateReportTrainingSection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_training_needs_section(data), str)

    def test_non_empty(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert len(rb.generate_report_training_needs_section(data)) > 0

    def test_references_build_4(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_training_needs_section(data)
        assert "Build 4" in result

    def test_handles_empty_data(self):
        result = rb.generate_report_training_needs_section({})
        assert isinstance(result, str)

    def test_includes_training_topics(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_report_training_needs_section(data)
        assert len(result) > 0


# ── TestGenerateReportGovernanceSection ───────────────────────────────────────

class TestGenerateReportGovernanceSection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_governance_section(data), str)

    def test_includes_standard_recommendations(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_governance_section(data)
        assert "AI Use Policy" in result or "governance" in result.lower()

    def test_handles_empty_data(self):
        result = rb.generate_report_governance_section({})
        assert isinstance(result, str)
        assert len(result) > 0


# ── TestGenerateReportNextStepsSection ────────────────────────────────────────

class TestGenerateReportNextStepsSection:
    def test_returns_string(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert isinstance(rb.generate_report_next_steps_section(data), str)

    def test_non_empty(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        assert len(rb.generate_report_next_steps_section(data)) > 0

    def test_handles_empty_data(self):
        result = rb.generate_report_next_steps_section({})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_includes_next_steps(self):
        data = rb.build_client_report_data_from_session_state(_FULL_SESSION)
        result = rb.generate_report_next_steps_section(data)
        assert "pilot" in result.lower() or "governance" in result.lower()


# ── TestGenerateResponsibleUseSection ─────────────────────────────────────────

class TestGenerateResponsibleUseSection:
    def test_returns_string(self):
        assert isinstance(rb.generate_report_responsible_use_section(), str)

    def test_mentions_synthetic(self):
        result = rb.generate_report_responsible_use_section()
        assert "synthetic" in result.lower()

    def test_mentions_human_review(self):
        result = rb.generate_report_responsible_use_section()
        assert "human review" in result.lower()

    def test_mentions_no_legal_advice(self):
        result = rb.generate_report_responsible_use_section()
        assert "legal" in result.lower()

    def test_mentions_safeguarding(self):
        result = rb.generate_report_responsible_use_section()
        assert "safeguarding" in result.lower()

    def test_non_empty(self):
        assert len(rb.generate_report_responsible_use_section()) > 50


# ── TestGenerateMarkdownClientReport ─────────────────────────────────────────

class TestGenerateMarkdownClientReport:
    def _data(self):
        return rb.build_client_report_data_from_session_state(_FULL_SESSION)

    def test_returns_string(self):
        assert isinstance(rb.generate_markdown_client_report(self._data()), str)

    def test_non_empty(self):
        result = rb.generate_markdown_client_report(self._data())
        assert len(result) > 200

    def test_contains_report_title(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "AI Readiness and Responsible AI Adoption Report" in result

    def test_contains_executive_summary_heading(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Executive Summary" in result

    def test_contains_responsible_use_boundaries(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Responsible-Use Boundaries" in result

    def test_contains_prototype_limitations(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Prototype Limitations" in result

    def test_contains_organisation_context(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Organisation Context" in result

    def test_handles_missing_optional_sections_safely(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.generate_markdown_client_report(data)
        assert isinstance(result, str)
        assert "Executive Summary" in result

    def test_excludes_section_when_flagged_false(self):
        result = rb.generate_markdown_client_report(
            self._data(), include_sections={"appendices": False}
        )
        assert "## 13. Appendices" not in result

    def test_includes_appendices_by_default(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Appendices" in result

    def test_handles_empty_data(self):
        result = rb.generate_markdown_client_report({})
        assert isinstance(result, str)
        assert "Executive Summary" in result

    def test_contains_cover_page(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Cover Page" in result

    def test_contains_table_of_contents(self):
        result = rb.generate_markdown_client_report(self._data())
        assert "Table of Contents" in result

    def test_always_includes_responsible_use_and_prototype(self):
        result = rb.generate_markdown_client_report(
            self._data(),
            include_sections={"readiness_summary": False, "appendices": False},
        )
        assert "Responsible-Use Boundaries" in result
        assert "Prototype Limitations" in result


# ── TestSummariseClientReport ─────────────────────────────────────────────────

class TestSummariseClientReport:
    def _data(self):
        return rb.build_client_report_data_from_session_state(_FULL_SESSION)

    def test_returns_dict(self):
        assert isinstance(rb.summarise_client_report(self._data()), dict)

    def test_has_organisation_name(self):
        result = rb.summarise_client_report(self._data())
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_has_sections_available(self):
        result = rb.summarise_client_report(self._data())
        assert "sections_available" in result
        assert isinstance(result["sections_available"], int)

    def test_has_sections_missing(self):
        result = rb.summarise_client_report(self._data())
        assert "sections_missing" in result
        assert isinstance(result["sections_missing"], int)

    def test_has_risks_included(self):
        result = rb.summarise_client_report(self._data())
        assert "risks_included" in result
        assert result["risks_included"] == 2

    def test_has_opportunities_included(self):
        result = rb.summarise_client_report(self._data())
        assert "opportunities_included" in result

    def test_has_pilots_included(self):
        result = rb.summarise_client_report(self._data())
        assert "pilots_included" in result
        assert result["pilots_included"] == 1

    def test_has_roadmap_actions(self):
        result = rb.summarise_client_report(self._data())
        assert "roadmap_actions_included" in result
        assert result["roadmap_actions_included"] == 24

    def test_has_report_readiness(self):
        result = rb.summarise_client_report(self._data())
        assert "report_readiness" in result
        assert isinstance(result["report_readiness"], str)

    def test_human_review_always_true(self):
        result = rb.summarise_client_report(self._data())
        assert result["human_review_required"] is True

    def test_full_session_report_readiness_mentions_ready(self):
        result = rb.summarise_client_report(self._data())
        assert "ready" in result["report_readiness"].lower()

    def test_partial_session_report_readiness_mentions_partial(self):
        data = rb.build_client_report_data_from_session_state({"audit_data": _AUDIT})
        result = rb.summarise_client_report(data)
        assert "partial" in result["report_readiness"].lower() or "missing" in result["report_readiness"].lower()

    def test_handles_empty_data(self):
        result = rb.summarise_client_report({})
        assert isinstance(result, dict)
        assert result["human_review_required"] is True


# ── TestCreateClientReportFilename ────────────────────────────────────────────

class TestCreateClientReportFilename:
    def test_returns_string(self):
        assert isinstance(rb.create_client_report_filename("BrightPath"), str)

    def test_ends_with_md(self):
        result = rb.create_client_report_filename("BrightPath")
        assert result.endswith(".md")

    def test_contains_org_name_slug(self):
        result = rb.create_client_report_filename("BrightPath Skills Training")
        assert "brightpath" in result.lower()

    def test_no_spaces_in_filename(self):
        result = rb.create_client_report_filename("BrightPath Skills Training")
        assert " " not in result

    def test_handles_empty_name(self):
        result = rb.create_client_report_filename("")
        assert result.endswith(".md")
        assert len(result) > 5

    def test_handles_special_characters(self):
        result = rb.create_client_report_filename("Test & Organisation: Ltd.")
        assert " " not in result
        assert result.endswith(".md")


# ── TestBackwardCompatibility ─────────────────────────────────────────────────

class TestBackwardCompatibility:
    def test_build_report_placeholder_returns_string(self):
        result = rb.build_report_placeholder(_AUDIT)
        assert isinstance(result, str)

    def test_build_report_placeholder_contains_org_name(self):
        result = rb.build_report_placeholder(_AUDIT)
        assert "BrightPath" in result

    def test_build_report_placeholder_handles_empty(self):
        result = rb.build_report_placeholder({})
        assert isinstance(result, str)
