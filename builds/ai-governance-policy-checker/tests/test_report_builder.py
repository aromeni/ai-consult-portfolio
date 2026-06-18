"""
Tests for report_builder.py — Build 6 Phase 6
BrightPath ChatGPT Mastery Project
"""

import pytest

from src.report_builder import (
    get_governance_report_required_sections,
    get_governance_report_optional_sections,
    check_governance_report_readiness,
    build_governance_report_data_from_session_state,
    generate_report_cover_section,
    generate_report_table_of_contents,
    generate_report_executive_summary_section,
    generate_report_policy_pack_section,
    generate_report_framework_section,
    generate_report_coverage_section,
    generate_report_gap_analysis_section,
    generate_report_recommendations_section,
    generate_report_maturity_section,
    generate_report_next_steps_section,
    generate_report_appendices_section,
    generate_report_responsible_use_section,
    generate_report_prototype_limitations_section,
    generate_markdown_governance_report,
    summarise_governance_report,
    create_governance_report_filename,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def minimal_policy_pack():
    return {
        "organisation_name": "BrightPath Skills Training",
        "organisation_type": "Training Provider",
        "sector": "Education and Training",
        "country_context": "England",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "policies": [
            {
                "policy_id": "POL-001",
                "policy_title": "AI Acceptable Use Policy",
                "policy_type": "Acceptable Use",
                "owner": "Chief Executive Officer",
                "status": "Approved",
                "last_reviewed": "2024-09-01",
                "summary": "Governs acceptable AI use.",
                "related_risk_areas": ["Data protection", "Safeguarding"],
            }
        ],
    }


@pytest.fixture
def minimal_policy_pack_summary():
    return {
        "total_policies": 1,
        "policy_types": ["Acceptable Use"],
        "risk_areas": ["Data protection", "Safeguarding"],
    }


@pytest.fixture
def sample_framework():
    return [
        {
            "domain_id": "GOV-001",
            "domain_name": "Strategy and Ownership",
            "priority_level": "High",
            "description": "AI strategy and governance ownership.",
            "why_it_matters": "Accountability.",
            "expected_policy_evidence": ["Named owner"],
            "example_controls": ["AI governance owner named"],
        },
        {
            "domain_id": "GOV-006",
            "domain_name": "Safeguarding Boundaries",
            "priority_level": "High",
            "description": "Safeguarding boundaries.",
            "why_it_matters": "Safety.",
            "expected_policy_evidence": ["Escalation route"],
            "example_controls": ["Human-led safeguarding"],
        },
    ]


@pytest.fixture
def sample_framework_summary():
    return {"total_domains": 2, "high_priority_count": 2, "medium_priority_count": 0}


@pytest.fixture
def sample_coverage_results():
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "overall_coverage_score": 55,
        "overall_coverage_level": "Partial coverage",
        "total_domains_checked": 2,
        "total_policies_reviewed": 1,
        "domain_results": [
            {
                "domain_id": "GOV-001",
                "domain_name": "Strategy and Ownership",
                "priority_level": "High",
                "coverage_score": 60,
                "coverage_level": "Partial coverage",
                "coverage_explanation": "Some evidence found.",
                "review_note": "Review required.",
                "matched_policies": ["POL-001"],
                "matched_keywords": ["owner"],
                "evidence_snippets": ["Named owner clause."],
            },
            {
                "domain_id": "GOV-006",
                "domain_name": "Safeguarding Boundaries",
                "priority_level": "High",
                "coverage_score": 20,
                "coverage_level": "Weak coverage",
                "coverage_explanation": "Little evidence found.",
                "review_note": "Review required.",
                "matched_policies": [],
                "matched_keywords": [],
                "evidence_snippets": [],
            },
        ],
    }


@pytest.fixture
def sample_coverage_summary():
    return {
        "strong_count": 0,
        "partial_count": 1,
        "weak_count": 1,
        "not_covered_count": 0,
        "high_priority_gaps": ["Safeguarding Boundaries"],
        "recommended_focus": ["Strengthen safeguarding wording"],
        "best_covered_domains": ["Strategy and Ownership"],
        "weakest_domains": ["Safeguarding Boundaries"],
    }


@pytest.fixture
def sample_gap_analysis():
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "total_domains_reviewed": 2,
        "total_gaps": 1,
        "overall_coverage_score": 55,
        "overall_coverage_level": "Partial coverage",
        "critical_gaps": [],
        "high_gaps": [
            {
                "gap_id": "GAP-001",
                "domain_name": "Safeguarding Boundaries",
                "gap_severity": "High gap",
                "gap_type": "Weak coverage",
                "priority_level": "High",
                "coverage_score": 20,
                "coverage_level": "Weak coverage",
                "gap_priority_score": 90,
                "matched_policies": [],
                "matched_keywords": [],
                "evidence_snippets": [],
                "missing_evidence": "Escalation route missing.",
                "risk_statement": "Safeguarding risk.",
                "action_hint": "Add safeguarding escalation.",
                "review_note": "Review required.",
            }
        ],
        "medium_gaps": [],
        "low_gaps": [],
        "prioritised_gaps": [
            {
                "gap_id": "GAP-001",
                "domain_name": "Safeguarding Boundaries",
                "gap_severity": "High gap",
                "gap_type": "Weak coverage",
                "priority_level": "High",
                "coverage_score": 20,
                "coverage_level": "Weak coverage",
                "gap_priority_score": 90,
                "matched_policies": [],
                "matched_keywords": [],
                "evidence_snippets": [],
                "missing_evidence": "Escalation route missing.",
                "risk_statement": "Safeguarding risk.",
                "action_hint": "Add safeguarding escalation.",
                "review_note": "Review required.",
            }
        ],
        "covered_domains": [],
    }


@pytest.fixture
def sample_gap_summary():
    return {
        "total_gaps": 1,
        "critical_gap_count": 0,
        "high_gap_count": 1,
        "medium_gap_count": 0,
        "low_gap_count": 0,
        "covered_domain_count": 0,
        "highest_priority_gap": {},
        "top_gap_domains": ["Safeguarding Boundaries"],
        "gap_themes": ["Safeguarding governance"],
        "overall_gap_position": "High-priority gaps require attention.",
        "recommended_focus": ["Address Safeguarding Boundaries"],
    }


@pytest.fixture
def sample_recommendations():
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "total_recommendations": 1,
        "urgent_recommendations": [],
        "high_priority_recommendations": [
            {
                "recommendation_id": "REC-001",
                "domain_name": "Safeguarding Boundaries",
                "gap_severity": "High gap",
                "gap_priority_score": 90,
                "recommendation_priority": "High priority",
                "policy_action_type": "Add escalation route",
                "target_policy": "Safeguarding and AI Boundary Policy",
                "suggested_owner": "Designated Safeguarding Lead",
                "recommendation_title": "Add AI safeguarding escalation route",
                "rationale": "High gap in safeguarding.",
                "suggested_wording_direction": "Add an escalation route.",
                "implementation_steps": ["Step 1", "Step 2"],
                "review_questions": ["Has the escalation route been added?"],
                "success_criteria": ["Escalation route documented."],
                "responsible_use_note": "x",
                "review_note": "Review required.",
            }
        ],
        "medium_priority_recommendations": [],
        "low_priority_recommendations": [],
        "prioritised_recommendations": [
            {
                "recommendation_id": "REC-001",
                "domain_name": "Safeguarding Boundaries",
                "gap_severity": "High gap",
                "gap_priority_score": 90,
                "recommendation_priority": "High priority",
                "policy_action_type": "Add escalation route",
                "target_policy": "Safeguarding and AI Boundary Policy",
                "suggested_owner": "Designated Safeguarding Lead",
                "recommendation_title": "Add AI safeguarding escalation route",
                "rationale": "High gap in safeguarding.",
                "suggested_wording_direction": "Add an escalation route.",
                "implementation_steps": ["Step 1", "Step 2"],
                "review_questions": ["Has the escalation route been added?"],
                "success_criteria": ["Escalation route documented."],
                "responsible_use_note": "x",
                "review_note": "Review required.",
            }
        ],
        "quick_wins": [],
        "policy_update_themes": ["Safeguarding governance"],
        "owner_summary": {"Designated Safeguarding Lead": ["REC-001"]},
        "recommended_sequence": [],
    }


@pytest.fixture
def sample_recommendation_summary():
    return {
        "total_recommendations": 1,
        "urgent_count": 0,
        "high_priority_count": 1,
        "medium_priority_count": 0,
        "low_priority_count": 0,
        "quick_win_count": 0,
        "top_policy_update_themes": ["Safeguarding governance"],
        "top_owners": ["Designated Safeguarding Lead"],
        "highest_priority_recommendation": {},
        "overall_recommendation_position": "High-priority recommendations exist.",
        "recommended_focus": ["Address Safeguarding Boundaries"],
    }


@pytest.fixture
def sample_maturity():
    return {
        "organisation_name": "BrightPath Skills Training",
        "policy_pack_title": "BrightPath AI Policy Pack",
        "overall_governance_score": 38.0,
        "overall_maturity_level": "Developing governance",
        "maturity_description": "Some foundations present.",
        "domain_maturity_scores": [
            {
                "domain_id": "GOV-001",
                "domain_name": "Strategy and Ownership",
                "priority_level": "High",
                "coverage_score": 60,
                "coverage_level": "Partial coverage",
                "maturity_score": 60,
                "maturity_level": "Defined governance",
                "related_gap_severity": "",
                "related_recommendation_priority": "",
                "maturity_explanation": "Some coverage.",
                "recommended_focus": "Review wording.",
            }
        ],
        "maturity_strengths": [],
        "maturity_weaknesses": [
            {
                "domain_id": "GOV-006",
                "domain_name": "Safeguarding Boundaries",
                "priority_level": "High",
                "coverage_score": 20,
                "coverage_level": "Weak coverage",
                "maturity_score": 5,
                "maturity_level": "Initial governance",
                "related_gap_severity": "High gap",
                "related_recommendation_priority": "High priority",
                "maturity_explanation": "Very weak.",
                "recommended_focus": "Address high gap.",
            }
        ],
        "maturity_blockers": [],
        "improvement_priorities": ["Strengthen safeguarding policy."],
        "adoption_readiness_position": "Limited pilots only after gaps are addressed.",
        "recommended_next_step": "Close the Safeguarding Boundaries gap.",
        "responsible_use_note": "Synthetic data only.",
        "prototype_note": "Not production.",
    }


@pytest.fixture
def sample_maturity_summary():
    return {
        "overall_governance_score": 38.0,
        "overall_maturity_level": "Developing governance",
        "total_domains": 2,
        "managed_or_optimised_domains": 0,
        "defined_domains": 1,
        "developing_domains": 0,
        "initial_domains": 1,
        "strength_count": 0,
        "weakness_count": 1,
        "blocker_count": 0,
        "strongest_domain": {},
        "weakest_domain": {},
        "overall_position": "Score 38/100, Developing governance.",
        "recommended_focus": ["Strengthen Safeguarding Boundaries"],
    }


@pytest.fixture
def full_session_state(
    minimal_policy_pack,
    minimal_policy_pack_summary,
    sample_framework,
    sample_framework_summary,
    sample_coverage_results,
    sample_coverage_summary,
    sample_gap_analysis,
    sample_gap_summary,
    sample_recommendations,
    sample_recommendation_summary,
    sample_maturity,
    sample_maturity_summary,
):
    return {
        "policy_pack": minimal_policy_pack,
        "policy_pack_summary": minimal_policy_pack_summary,
        "governance_framework": sample_framework,
        "governance_framework_summary": sample_framework_summary,
        "coverage_results": sample_coverage_results,
        "coverage_summary": sample_coverage_summary,
        "gap_analysis": sample_gap_analysis,
        "gap_summary": sample_gap_summary,
        "policy_recommendations": sample_recommendations,
        "recommendation_summary": sample_recommendation_summary,
        "governance_maturity": sample_maturity,
        "governance_maturity_summary": sample_maturity_summary,
    }


@pytest.fixture
def minimal_session_state(minimal_policy_pack):
    return {"policy_pack": minimal_policy_pack}


@pytest.fixture
def full_report_data(full_session_state):
    return build_governance_report_data_from_session_state(full_session_state)


@pytest.fixture
def minimal_report_data(minimal_session_state):
    return build_governance_report_data_from_session_state(minimal_session_state)


# ---------------------------------------------------------------------------
# get_governance_report_required_sections
# ---------------------------------------------------------------------------

class TestGetGovernanceReportRequiredSections:
    def test_returns_non_empty_list(self):
        result = get_governance_report_required_sections()
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_contains_policy_pack(self):
        result = get_governance_report_required_sections()
        assert "policy_pack" in result


# ---------------------------------------------------------------------------
# get_governance_report_optional_sections
# ---------------------------------------------------------------------------

class TestGetGovernanceReportOptionalSections:
    def test_returns_non_empty_list(self):
        result = get_governance_report_optional_sections()
        assert isinstance(result, list)
        assert len(result) >= 5

    def test_contains_executive_summary(self):
        result = get_governance_report_optional_sections()
        assert "executive_summary" in result

    def test_contains_appendices(self):
        result = get_governance_report_optional_sections()
        assert "appendices" in result


# ---------------------------------------------------------------------------
# check_governance_report_readiness
# ---------------------------------------------------------------------------

class TestCheckGovernanceReportReadiness:
    def test_empty_session_state_not_ready(self):
        result = check_governance_report_readiness({})
        assert result["is_ready"] is False

    def test_with_policy_pack_is_ready(self, minimal_session_state):
        result = check_governance_report_readiness(minimal_session_state)
        assert result["is_ready"] is True

    def test_detects_available_policy_pack(self, minimal_session_state):
        result = check_governance_report_readiness(minimal_session_state)
        assert "policy_pack" in result["available_sections"]

    def test_detects_missing_coverage_results(self, minimal_session_state):
        result = check_governance_report_readiness(minimal_session_state)
        assert "coverage_results" in result["missing_sections"]

    def test_full_session_state_has_no_missing(self, full_session_state):
        result = check_governance_report_readiness(full_session_state)
        assert len(result["missing_sections"]) == 0

    def test_returns_expected_keys(self, minimal_session_state):
        result = check_governance_report_readiness(minimal_session_state)
        for key in ["is_ready", "available_sections", "missing_sections", "recommended_next_steps"]:
            assert key in result

    def test_recommended_next_steps_is_list(self, minimal_session_state):
        result = check_governance_report_readiness(minimal_session_state)
        assert isinstance(result["recommended_next_steps"], list)


# ---------------------------------------------------------------------------
# build_governance_report_data_from_session_state
# ---------------------------------------------------------------------------

class TestBuildGovernanceReportDataFromSessionState:
    def test_returns_expected_keys(self, full_report_data):
        for key in [
            "report_title", "organisation_name", "generated_date",
            "policy_pack", "policy_pack_summary", "governance_framework",
            "governance_framework_summary", "coverage_results", "coverage_summary",
            "gap_analysis", "gap_summary", "policy_recommendations",
            "recommendation_summary", "governance_maturity", "governance_maturity_summary",
            "source_outputs_available", "responsible_use_note", "prototype_note",
        ]:
            assert key in full_report_data, f"Missing key: {key}"

    def test_org_name_populated(self, full_report_data):
        assert full_report_data["organisation_name"] == "BrightPath Skills Training"

    def test_handles_missing_values_safely(self):
        result = build_governance_report_data_from_session_state({})
        assert result["organisation_name"] == "Unnamed organisation"
        assert result["policy_pack"] is None

    def test_source_outputs_available_reflects_session(self, full_report_data):
        avail = full_report_data["source_outputs_available"]
        assert avail["policy_pack"] is True
        assert avail["coverage_results"] is True

    def test_source_outputs_false_when_missing(self, minimal_report_data):
        avail = minimal_report_data["source_outputs_available"]
        assert avail["coverage_results"] is False
        assert avail["gap_analysis"] is False

    def test_generated_date_is_string(self, full_report_data):
        assert isinstance(full_report_data["generated_date"], str)
        assert len(full_report_data["generated_date"]) == 10  # ISO date


# ---------------------------------------------------------------------------
# generate_report_cover_section
# ---------------------------------------------------------------------------

class TestGenerateReportCoverSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_cover_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_cover_page_heading(self, full_report_data):
        result = generate_report_cover_section(full_report_data)
        assert "Cover Page" in result

    def test_contains_org_name(self, full_report_data):
        result = generate_report_cover_section(full_report_data)
        assert "BrightPath" in result

    def test_contains_prototype_status(self, full_report_data):
        result = generate_report_cover_section(full_report_data)
        assert "Prototype status" in result or "prototype" in result.lower()

    def test_contains_date(self, full_report_data):
        result = generate_report_cover_section(full_report_data)
        assert full_report_data["generated_date"] in result


# ---------------------------------------------------------------------------
# generate_report_table_of_contents
# ---------------------------------------------------------------------------

class TestGenerateReportTableOfContents:
    def test_returns_string(self, full_report_data):
        result = generate_report_table_of_contents(full_report_data)
        assert isinstance(result, str)

    def test_contains_toc_heading(self, full_report_data):
        result = generate_report_table_of_contents(full_report_data)
        assert "Table of Contents" in result

    def test_contains_executive_summary_entry(self, full_report_data):
        result = generate_report_table_of_contents(full_report_data)
        assert "Executive Summary" in result

    def test_contains_appendices_entry(self, full_report_data):
        result = generate_report_table_of_contents(full_report_data)
        assert "Appendices" in result


# ---------------------------------------------------------------------------
# generate_report_executive_summary_section
# ---------------------------------------------------------------------------

class TestGenerateReportExecutiveSummarySections:
    def test_returns_string(self, full_report_data):
        result = generate_report_executive_summary_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_executive_summary_heading(self, full_report_data):
        result = generate_report_executive_summary_section(full_report_data)
        assert "Executive Summary" in result

    def test_contains_org_name(self, full_report_data):
        result = generate_report_executive_summary_section(full_report_data)
        assert "BrightPath" in result

    def test_contains_human_review_note(self, full_report_data):
        result = generate_report_executive_summary_section(full_report_data)
        assert "human review" in result.lower() or "Human review" in result

    def test_handles_minimal_data(self, minimal_report_data):
        result = generate_report_executive_summary_section(minimal_report_data)
        assert isinstance(result, str)
        assert len(result) > 10


# ---------------------------------------------------------------------------
# generate_report_policy_pack_section
# ---------------------------------------------------------------------------

class TestGenerateReportPolicyPackSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_policy_pack_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_policy_pack_heading(self, full_report_data):
        result = generate_report_policy_pack_section(full_report_data)
        assert "Policy Pack" in result

    def test_handles_missing_policy_pack_safely(self):
        result = generate_report_policy_pack_section({"policy_pack": None})
        assert "No synthetic policy pack" in result

    def test_contains_policy_titles(self, full_report_data):
        result = generate_report_policy_pack_section(full_report_data)
        assert "AI Acceptable Use Policy" in result


# ---------------------------------------------------------------------------
# generate_report_framework_section
# ---------------------------------------------------------------------------

class TestGenerateReportFrameworkSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_framework_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_framework_heading(self, full_report_data):
        result = generate_report_framework_section(full_report_data)
        assert "Governance Framework" in result

    def test_handles_missing_framework_safely(self):
        result = generate_report_framework_section({"governance_framework": None})
        assert "No governance framework" in result

    def test_contains_domain_names(self, full_report_data):
        result = generate_report_framework_section(full_report_data)
        assert "Safeguarding Boundaries" in result


# ---------------------------------------------------------------------------
# generate_report_coverage_section
# ---------------------------------------------------------------------------

class TestGenerateReportCoverageSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_coverage_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_coverage_heading(self, full_report_data):
        result = generate_report_coverage_section(full_report_data)
        assert "Coverage Review" in result

    def test_handles_missing_coverage_safely(self):
        result = generate_report_coverage_section({"coverage_results": None})
        assert "No Policy Coverage Review" in result

    def test_contains_overall_score(self, full_report_data):
        result = generate_report_coverage_section(full_report_data)
        assert "55" in result


# ---------------------------------------------------------------------------
# generate_report_gap_analysis_section
# ---------------------------------------------------------------------------

class TestGenerateReportGapAnalysisSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_gap_analysis_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_gap_analysis_heading(self, full_report_data):
        result = generate_report_gap_analysis_section(full_report_data)
        assert "Gap Analysis" in result

    def test_handles_missing_gap_analysis_safely(self):
        result = generate_report_gap_analysis_section({"gap_analysis": None})
        assert "No Gap Analysis" in result

    def test_contains_gap_count(self, full_report_data):
        result = generate_report_gap_analysis_section(full_report_data)
        assert "1" in result  # total_gaps = 1


# ---------------------------------------------------------------------------
# generate_report_recommendations_section
# ---------------------------------------------------------------------------

class TestGenerateReportRecommendationsSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_recommendations_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_recommendations_heading(self, full_report_data):
        result = generate_report_recommendations_section(full_report_data)
        assert "Recommendations" in result

    def test_handles_missing_recommendations_safely(self):
        result = generate_report_recommendations_section({"policy_recommendations": None})
        assert "No Policy Recommendations" in result

    def test_contains_wording_direction_warning(self, full_report_data):
        result = generate_report_recommendations_section(full_report_data)
        assert "wording" in result.lower()


# ---------------------------------------------------------------------------
# generate_report_maturity_section
# ---------------------------------------------------------------------------

class TestGenerateReportMaturitySection:
    def test_returns_string(self, full_report_data):
        result = generate_report_maturity_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_maturity_heading(self, full_report_data):
        result = generate_report_maturity_section(full_report_data)
        assert "Maturity" in result

    def test_handles_missing_maturity_safely(self):
        result = generate_report_maturity_section({"governance_maturity": None})
        assert "No Governance Maturity Summary" in result

    def test_contains_maturity_level(self, full_report_data):
        result = generate_report_maturity_section(full_report_data)
        assert "Developing governance" in result


# ---------------------------------------------------------------------------
# generate_report_next_steps_section
# ---------------------------------------------------------------------------

class TestGenerateReportNextStepsSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_next_steps_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_next_steps_heading(self, full_report_data):
        result = generate_report_next_steps_section(full_report_data)
        assert "Next Steps" in result

    def test_contains_numbered_steps(self, full_report_data):
        result = generate_report_next_steps_section(full_report_data)
        assert "1." in result

    def test_returns_at_least_one_step(self, minimal_report_data):
        result = generate_report_next_steps_section(minimal_report_data)
        assert "1." in result


# ---------------------------------------------------------------------------
# generate_report_appendices_section
# ---------------------------------------------------------------------------

class TestGenerateReportAppendicesSection:
    def test_returns_string(self, full_report_data):
        result = generate_report_appendices_section(full_report_data)
        assert isinstance(result, str)

    def test_contains_appendices_heading(self, full_report_data):
        result = generate_report_appendices_section(full_report_data)
        assert "Appendices" in result

    def test_contains_policy_list(self, full_report_data):
        result = generate_report_appendices_section(full_report_data)
        assert "Policy List" in result

    def test_contains_domain_list(self, full_report_data):
        result = generate_report_appendices_section(full_report_data)
        assert "Domain List" in result

    def test_handles_missing_coverage_safely(self, minimal_report_data):
        result = generate_report_appendices_section(minimal_report_data)
        assert "Coverage results not available" in result or "not available" in result

    def test_contains_source_outputs_checklist(self, full_report_data):
        result = generate_report_appendices_section(full_report_data)
        assert "Source Outputs" in result


# ---------------------------------------------------------------------------
# generate_report_responsible_use_section
# ---------------------------------------------------------------------------

class TestGenerateReportResponsibleUseSection:
    def test_returns_string(self):
        result = generate_report_responsible_use_section()
        assert isinstance(result, str)

    def test_contains_responsible_use_heading(self):
        result = generate_report_responsible_use_section()
        assert "Responsible-Use Boundaries" in result

    def test_contains_synthetic_note(self):
        result = generate_report_responsible_use_section()
        assert "synthetic" in result.lower() or "demo" in result.lower()

    def test_contains_human_review_note(self):
        result = generate_report_responsible_use_section()
        assert "Human review" in result or "human review" in result


# ---------------------------------------------------------------------------
# generate_report_prototype_limitations_section
# ---------------------------------------------------------------------------

class TestGenerateReportPrototypeLimitationsSection:
    def test_returns_string(self):
        result = generate_report_prototype_limitations_section()
        assert isinstance(result, str)

    def test_contains_limitations_heading(self):
        result = generate_report_prototype_limitations_section()
        assert "Prototype Limitations" in result

    def test_contains_synthetic_data_note(self):
        result = generate_report_prototype_limitations_section()
        assert "synthetic" in result.lower() or "demo" in result.lower()

    def test_contains_no_llm_note(self):
        result = generate_report_prototype_limitations_section()
        assert "LLM" in result or "API" in result or "OpenAI" in result


# ---------------------------------------------------------------------------
# generate_markdown_governance_report
# ---------------------------------------------------------------------------

class TestGenerateMarkdownGovernanceReport:
    def test_returns_string(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert isinstance(result, str)

    def test_contains_main_title(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "AI Governance Policy Review Report" in result

    def test_contains_executive_summary(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Executive Summary" in result

    def test_contains_responsible_use_boundaries(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Responsible-Use Boundaries" in result

    def test_contains_prototype_limitations(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Prototype Limitations" in result

    def test_contains_policy_pack_section(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Policy Pack Overview" in result

    def test_contains_framework_section(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Governance Framework" in result

    def test_contains_coverage_section(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Coverage Review" in result

    def test_contains_gap_analysis_section(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Gap Analysis" in result

    def test_contains_recommendations_section(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Recommendations" in result

    def test_contains_maturity_section(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Maturity Summary" in result

    def test_handles_missing_optional_sections_safely(self, minimal_report_data):
        result = generate_markdown_governance_report(minimal_report_data)
        assert "AI Governance Policy Review Report" in result
        assert "No Gap Analysis" in result

    def test_section_exclusion_respected(self, full_report_data):
        include = {s: True for s in [
            "executive_summary", "policy_pack", "responsible_use", "prototype_limitations"
        ]}
        include["governance_framework"] = False
        include["coverage_review"] = False
        include["gap_analysis"] = False
        include["recommendations"] = False
        include["maturity_summary"] = False
        include["next_steps"] = False
        include["appendices"] = False
        result = generate_markdown_governance_report(full_report_data, include)
        # TOC always renders — check that the actual section heading is absent
        assert "## 3. Responsible AI Governance Framework" not in result
        assert "## 4. Policy Coverage Review" not in result

    def test_org_name_appears_in_report(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "BrightPath" in result

    def test_contains_table_of_contents(self, full_report_data):
        result = generate_markdown_governance_report(full_report_data)
        assert "Table of Contents" in result


# ---------------------------------------------------------------------------
# summarise_governance_report
# ---------------------------------------------------------------------------

class TestSummariseGovernanceReport:
    def test_returns_expected_keys(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        for key in [
            "organisation_name", "sections_available", "sections_missing",
            "domains_reviewed", "gaps_included", "recommendations_included",
            "maturity_level", "report_readiness", "human_review_required",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_human_review_required_is_true(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["human_review_required"] is True

    def test_org_name_is_populated(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_sections_available_positive_for_full(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["sections_available"] > 0

    def test_sections_missing_zero_for_full(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["sections_missing"] == 0

    def test_report_readiness_is_string(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert isinstance(result["report_readiness"], str)
        assert len(result["report_readiness"]) > 10

    def test_gaps_included_matches(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["gaps_included"] == 1

    def test_recs_included_matches(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["recommendations_included"] == 1

    def test_maturity_level_populated_when_available(self, full_report_data):
        result = summarise_governance_report(full_report_data)
        assert result["maturity_level"] == "Developing governance"


# ---------------------------------------------------------------------------
# create_governance_report_filename
# ---------------------------------------------------------------------------

class TestCreateGovernanceReportFilename:
    def test_returns_string(self):
        result = create_governance_report_filename("BrightPath Skills Training")
        assert isinstance(result, str)

    def test_ends_with_md(self):
        result = create_governance_report_filename("BrightPath Skills Training")
        assert result.endswith(".md")

    def test_contains_report(self):
        result = create_governance_report_filename("BrightPath Skills Training")
        assert "report" in result

    def test_handles_special_characters(self):
        result = create_governance_report_filename("Org & Partners Ltd.")
        assert isinstance(result, str)
        assert result.endswith(".md")
        assert "&" not in result

    def test_snake_case_org_name(self):
        result = create_governance_report_filename("BrightPath Skills Training")
        assert " " not in result

    def test_empty_org_name_does_not_crash(self):
        result = create_governance_report_filename("")
        assert result.endswith(".md")
