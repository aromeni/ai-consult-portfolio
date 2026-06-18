"""
Tests for src/completion_review.py — Build 6 Phase 8.
"""

import pytest
from src.completion_review import (
    get_build6_phase_checklist,
    get_expected_build6_outputs,
    check_session_state_outputs,
    check_documentation_files,
    generate_completion_score,
    generate_build6_completion_review,
    generate_portfolio_summary,
    generate_case_study_summary,
    format_completion_review_as_markdown,
    format_portfolio_notes_as_markdown,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def minimal_session_state():
    return {
        "policy_pack": {"organisation_name": "BrightPath Skills Training", "policies": []},
        "governance_report_markdown": "# Governance Report\n\nSynthetic content.",
    }


@pytest.fixture
def full_session_state():
    return {
        "policy_pack": {"organisation_name": "BrightPath Skills Training", "policies": []},
        "policy_pack_summary": {"total_policies": 6},
        "policy_pack_markdown": "# Policy Pack",
        "governance_framework": [{"domain_id": "GOV-001"}],
        "governance_framework_summary": {"total_domains": 12},
        "governance_framework_markdown": "# Framework",
        "coverage_results": {"overall_coverage_score": 60, "domain_results": []},
        "coverage_summary": {"strong_count": 3},
        "coverage_markdown": "# Coverage",
        "gap_analysis": {"prioritised_gaps": []},
        "gap_summary": {"total_gaps": 5},
        "gap_analysis_markdown": "# Gaps",
        "policy_recommendations": {"prioritised_recommendations": []},
        "recommendation_summary": {"total_recommendations": 4},
        "policy_recommendations_markdown": "# Recommendations",
        "governance_maturity": {"overall_governance_score": 65, "overall_maturity_level": "Defined"},
        "governance_maturity_summary": {"total_domains": 12},
        "governance_maturity_markdown": "# Maturity",
        "governance_report_data": {"organisation_name": "BrightPath Skills Training"},
        "governance_report_summary": {"sections_available": 10},
        "governance_report_markdown": "# Governance Report\n\nContent here.",
        "governance_report_filename": "brightpath-governance-report.md",
        "export_data": {"organisation_name": "BrightPath Skills Training"},
        "export_readiness": {"is_ready": True},
        "governance_report_analytics": {"export_completion": {}},
        "governance_report_chart_paths": {"coverage_levels": "outputs/charts/coverage_levels.png"},
        "governance_report_pdf_bytes": b"%PDF-1.4 mock",
        "governance_report_pdf_filename": "brightpath-governance-report.pdf",
    }


# ── Phase checklist ───────────────────────────────────────────────────────────

class TestGetBuild6PhaseChecklist:
    def test_returns_8_phases(self):
        result = get_build6_phase_checklist()
        assert len(result) == 8

    def test_all_items_are_dicts(self):
        for item in get_build6_phase_checklist():
            assert isinstance(item, dict)

    def test_required_keys_present(self):
        for item in get_build6_phase_checklist():
            assert "phase" in item
            assert "name" in item
            assert "purpose" in item
            assert "status" in item
            assert "evidence" in item

    def test_phases_labelled_correctly(self):
        phases = [p["phase"] for p in get_build6_phase_checklist()]
        assert "Phase 1" in phases
        assert "Phase 8" in phases

    def test_all_phases_complete(self):
        for item in get_build6_phase_checklist():
            assert item["status"] == "Complete"

    def test_phase_names_are_non_empty(self):
        for item in get_build6_phase_checklist():
            assert len(item["name"]) > 0

    def test_phase8_is_completion_review(self):
        phase8 = get_build6_phase_checklist()[-1]
        assert "completion" in phase8["name"].lower() or "portfolio" in phase8["name"].lower()


# ── Expected outputs ──────────────────────────────────────────────────────────

class TestGetExpectedBuild6Outputs:
    def test_returns_non_empty_list(self):
        result = get_expected_build6_outputs()
        assert len(result) > 0

    def test_all_items_have_required_keys(self):
        for item in get_expected_build6_outputs():
            assert "key" in item
            assert "label" in item
            assert "importance" in item

    def test_importance_values_are_valid(self):
        valid = {"Required", "Recommended", "Advisory"}
        for item in get_expected_build6_outputs():
            assert item["importance"] in valid

    def test_policy_pack_is_required(self):
        items = {i["key"]: i for i in get_expected_build6_outputs()}
        assert items["policy_pack"]["importance"] == "Required"

    def test_governance_report_markdown_is_required(self):
        items = {i["key"]: i for i in get_expected_build6_outputs()}
        assert items["governance_report_markdown"]["importance"] == "Required"

    def test_includes_pdf_bytes(self):
        keys = [i["key"] for i in get_expected_build6_outputs()]
        assert "governance_report_pdf_bytes" in keys

    def test_includes_chart_paths(self):
        keys = [i["key"] for i in get_expected_build6_outputs()]
        assert "governance_report_chart_paths" in keys


# ── Session state output check ────────────────────────────────────────────────

class TestCheckSessionStateOutputs:
    def test_empty_session_state_returns_dict(self):
        result = check_session_state_outputs({})
        assert isinstance(result, dict)

    def test_empty_state_has_zero_available(self):
        result = check_session_state_outputs({})
        assert result["available_count"] == 0

    def test_empty_state_completion_is_zero(self):
        result = check_session_state_outputs({})
        assert result["completion_percentage"] == 0

    def test_full_state_has_high_completion(self, full_session_state):
        result = check_session_state_outputs(full_session_state)
        assert result["completion_percentage"] > 80

    def test_full_state_missing_count_is_low(self, full_session_state):
        result = check_session_state_outputs(full_session_state)
        assert result["missing_count"] < 5

    def test_returns_next_actions(self):
        result = check_session_state_outputs({})
        assert "recommended_next_actions" in result
        assert isinstance(result["recommended_next_actions"], list)

    def test_returns_required_missing(self):
        result = check_session_state_outputs({})
        assert "required_missing" in result
        assert len(result["required_missing"]) > 0

    def test_minimal_state_detects_available(self, minimal_session_state):
        result = check_session_state_outputs(minimal_session_state)
        keys = [i["key"] for i in result["available_outputs"]]
        assert "policy_pack" in keys
        assert "governance_report_markdown" in keys

    def test_total_outputs_matches_expected(self):
        result = check_session_state_outputs({})
        expected = get_expected_build6_outputs()
        assert result["total_outputs"] == len(expected)


# ── Documentation file check ──────────────────────────────────────────────────

class TestCheckDocumentationFiles:
    def test_returns_dict(self, tmp_path):
        result = check_documentation_files(str(tmp_path))
        assert isinstance(result, dict)

    def test_returns_required_keys(self, tmp_path):
        result = check_documentation_files(str(tmp_path))
        assert "existing_files" in result
        assert "missing_files" in result
        assert "documentation_completion_percentage" in result
        assert "total_docs" in result

    def test_empty_dir_all_missing(self, tmp_path):
        result = check_documentation_files(str(tmp_path))
        assert result["existing_count"] == 0
        assert result["documentation_completion_percentage"] == 0

    def test_detects_existing_readme(self, tmp_path):
        (tmp_path / "README.md").write_text("# Test")
        result = check_documentation_files(str(tmp_path))
        existing_paths = [d["path"] for d in result["existing_files"]]
        assert "README.md" in existing_paths

    def test_total_docs_is_positive(self, tmp_path):
        result = check_documentation_files(str(tmp_path))
        assert result["total_docs"] > 5

    def test_detects_docs_subdir_files(self, tmp_path):
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "build-notes.md").write_text("# Build Notes")
        result = check_documentation_files(str(tmp_path))
        existing_paths = [d["path"] for d in result["existing_files"]]
        assert "docs/build-notes.md" in existing_paths


# ── Completion score ──────────────────────────────────────────────────────────

class TestGenerateCompletionScore:
    def test_returns_required_keys(self):
        phases = get_build6_phase_checklist()
        output_status = check_session_state_outputs({})
        doc_status = {"documentation_completion_percentage": 50, "missing_count": 0, "missing_files": []}
        result = generate_completion_score(phases, output_status, doc_status)
        assert "overall_status" in result
        assert "phase_completion_percentage" in result
        assert "output_completion_percentage" in result
        assert "documentation_completion_percentage" in result
        assert "final_readiness_label" in result
        assert "recommended_final_actions" in result

    def test_all_phases_complete_gives_100_percent(self):
        phases = get_build6_phase_checklist()
        output_status = {"completion_percentage": 100, "recommended_next_actions": []}
        doc_status = {"documentation_completion_percentage": 100, "missing_count": 0, "missing_files": []}
        result = generate_completion_score(phases, output_status, doc_status)
        assert result["phase_completion_percentage"] == 100

    def test_high_completion_gives_complete_status(self):
        phases = get_build6_phase_checklist()
        output_status = {"completion_percentage": 90, "recommended_next_actions": []}
        doc_status = {"documentation_completion_percentage": 90, "missing_count": 0, "missing_files": []}
        result = generate_completion_score(phases, output_status, doc_status)
        assert result["overall_status"] == "Complete"

    def test_low_completion_gives_in_progress_status(self):
        phases = []
        output_status = {"completion_percentage": 10, "recommended_next_actions": []}
        doc_status = {"documentation_completion_percentage": 10, "missing_count": 5, "missing_files": []}
        result = generate_completion_score(phases, output_status, doc_status)
        assert result["overall_status"] == "In progress"

    def test_readiness_label_is_non_empty(self):
        phases = get_build6_phase_checklist()
        output_status = {"completion_percentage": 50, "recommended_next_actions": []}
        doc_status = {"documentation_completion_percentage": 50, "missing_count": 0, "missing_files": []}
        result = generate_completion_score(phases, output_status, doc_status)
        assert len(result["final_readiness_label"]) > 10


# ── Full completion review ────────────────────────────────────────────────────

class TestGenerateBuild6CompletionReview:
    def test_returns_dict(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert isinstance(result, dict)

    def test_required_keys_present(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert "build_title" in result
        assert "build_number" in result
        assert "completion_status" in result
        assert "phase_checklist" in result
        assert "output_status" in result
        assert "documentation_status" in result
        assert "portfolio_value" in result
        assert "commercial_value" in result
        assert "technical_value" in result
        assert "responsible_use_position" in result
        assert "prototype_note" in result
        assert "human_review_note" in result

    def test_build_title_is_correct(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert result["build_title"] == "AI Governance Policy Checker"

    def test_build_number_is_correct(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert result["build_number"] == "Build 6"

    def test_portfolio_value_is_non_empty(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert len(result["portfolio_value"]) > 50

    def test_responsible_use_position_mentions_synthetic(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert "synthetic" in result["responsible_use_position"].lower()

    def test_handles_full_session_state(self, full_session_state, tmp_path):
        result = generate_build6_completion_review(full_session_state, str(tmp_path))
        assert result["output_status"]["available_count"] > 0

    def test_phase_checklist_has_8_items(self, tmp_path):
        result = generate_build6_completion_review({}, str(tmp_path))
        assert len(result["phase_checklist"]) == 8


# ── Portfolio summary ─────────────────────────────────────────────────────────

class TestGeneratePortfolioSummary:
    def test_returns_dict(self):
        result = generate_portfolio_summary()
        assert isinstance(result, dict)

    def test_required_keys_present(self):
        result = generate_portfolio_summary()
        for key in [
            "project_name", "one_line_summary", "problem_solved", "target_users",
            "core_workflow", "key_features", "technical_stack", "responsible_ai_features",
            "portfolio_positioning", "what_this_demonstrates",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_target_users_is_list(self):
        result = generate_portfolio_summary()
        assert isinstance(result["target_users"], list)
        assert len(result["target_users"]) > 0

    def test_core_workflow_includes_export(self):
        result = generate_portfolio_summary()
        workflow = result["core_workflow"]
        assert any("export" in step.lower() for step in workflow)

    def test_one_line_summary_is_non_empty(self):
        result = generate_portfolio_summary()
        assert len(result["one_line_summary"]) > 30

    def test_technical_stack_mentions_streamlit(self):
        result = generate_portfolio_summary()
        stack_text = " ".join(result["technical_stack"]).lower()
        assert "streamlit" in stack_text

    def test_technical_stack_mentions_pytest(self):
        result = generate_portfolio_summary()
        stack_text = " ".join(result["technical_stack"]).lower()
        assert "pytest" in stack_text

    def test_responsible_ai_features_mentions_synthetic(self):
        result = generate_portfolio_summary()
        features_text = " ".join(result["responsible_ai_features"]).lower()
        assert "synthetic" in features_text


# ── Case study summary ────────────────────────────────────────────────────────

class TestGenerateCaseStudySummary:
    def test_returns_dict(self):
        result = generate_case_study_summary()
        assert isinstance(result, dict)

    def test_required_keys_present(self):
        result = generate_case_study_summary()
        for key in [
            "case_study_title", "client_context", "challenge", "solution",
            "outputs_generated", "responsible_use_controls", "consulting_value", "limitations",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_title_mentions_brightpath(self):
        result = generate_case_study_summary()
        assert "BrightPath" in result["case_study_title"]

    def test_client_context_mentions_synthetic(self):
        result = generate_case_study_summary()
        assert "synthetic" in result["client_context"].lower()

    def test_outputs_generated_is_list(self):
        result = generate_case_study_summary()
        assert isinstance(result["outputs_generated"], list)
        assert len(result["outputs_generated"]) > 0

    def test_limitations_is_list(self):
        result = generate_case_study_summary()
        assert isinstance(result["limitations"], list)
        assert len(result["limitations"]) > 0

    def test_responsible_use_controls_is_list(self):
        result = generate_case_study_summary()
        assert isinstance(result["responsible_use_controls"], list)
        assert len(result["responsible_use_controls"]) > 0


# ── Markdown: completion review ───────────────────────────────────────────────

class TestFormatCompletionReviewAsMarkdown:
    @pytest.fixture
    def review(self, tmp_path):
        return generate_build6_completion_review({}, str(tmp_path))

    def test_returns_string(self, review):
        result = format_completion_review_as_markdown(review)
        assert isinstance(result, str)

    def test_includes_h1_title(self, review):
        result = format_completion_review_as_markdown(review)
        assert "# Build 6 Completion Review" in result

    def test_includes_portfolio_value_heading(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Portfolio Value" in result

    def test_includes_commercial_value_heading(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Commercial Value" in result

    def test_includes_technical_value_heading(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Technical Value" in result

    def test_includes_responsible_use_position(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Responsible-Use Position" in result

    def test_includes_prototype_limitations(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Prototype Limitations" in result

    def test_includes_human_review_requirement(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Human Review Requirement" in result

    def test_includes_phase_checklist_heading(self, review):
        result = format_completion_review_as_markdown(review)
        assert "## Phase Completion Checklist" in result

    def test_includes_all_8_phases(self, review):
        result = format_completion_review_as_markdown(review)
        for i in range(1, 9):
            assert f"Phase {i}" in result


# ── Markdown: portfolio notes ─────────────────────────────────────────────────

class TestFormatPortfolioNotesAsMarkdown:
    @pytest.fixture
    def portfolio(self):
        return generate_portfolio_summary()

    @pytest.fixture
    def case_study(self):
        return generate_case_study_summary()

    def test_returns_string(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert isinstance(result, str)

    def test_includes_h1_title(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "# Build 6 Portfolio Notes" in result

    def test_includes_one_line_summary(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "## One-Line Summary" in result

    def test_includes_problem_solved(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "## Problem Solved" in result

    def test_includes_target_users(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "## Target Users" in result

    def test_includes_technical_stack(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "## Technical Stack" in result

    def test_includes_case_study(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "BrightPath" in result

    def test_includes_limitations(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "## Limitations" in result

    def test_includes_how_to_demo(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "## How To Demo" in result

    def test_includes_linkedin_description(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "LinkedIn" in result or "GitHub" in result

    def test_includes_streamlit_run_command(self, portfolio, case_study):
        result = format_portfolio_notes_as_markdown(portfolio, case_study)
        assert "streamlit run app.py" in result
