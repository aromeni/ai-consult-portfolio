"""Tests for src/completion_review.py - Build 5 Phase 9."""

from src import completion_review as cr


_FULL_STATE = {
    "audit_data": {"organisation_profile": {"organisation_name": "BrightPath"}},
    "audit_summary": {"organisation_name": "BrightPath"},
    "readiness_summary": {"overall_score": 42},
    "readiness_summary_markdown": "# Readiness",
    "risk_register": [{"risk_id": "RISK-001"}],
    "risk_register_summary": {"total_risks": 5},
    "risk_register_markdown": "# Risk Register",
    "opportunity_portfolio": {"pilots": [{"pilot_id": "PILOT-001"}]},
    "opportunity_summary": {"total_pilots": 3},
    "opportunity_portfolio_markdown": "# Opportunities",
    "implementation_roadmap": {"phase_30_days": [{"action": "Create AI policy"}]},
    "implementation_roadmap_summary": {"total_actions": 24},
    "implementation_roadmap_markdown": "# Roadmap",
    "report_sections": {"sections": {"executive_summary": {}}},
    "report_sections_summary": {"section_count": 11},
    "report_sections_markdown": "# Report Sections",
    "client_report_data": {"organisation_name": "BrightPath"},
    "client_report_markdown": "# Client Report",
    "client_report_filename": "brightpath.md",
    "export_data": {"organisation_name": "BrightPath"},
    "client_report_analytics": {"completion_status": {"Audit Data": True}},
    "client_report_chart_paths": {"readiness_scores": "readiness_scores.png"},
    "client_report_pdf_bytes": b"%PDF-test",
    "client_report_pptx_bytes": b"PK-test",
}


def test_get_build5_phase_checklist_returns_9_phases():
    result = cr.get_build5_phase_checklist()
    assert len(result) == 9
    assert result[-1]["phase"] == "Phase 9"


def test_get_expected_build5_outputs_returns_non_empty_list():
    result = cr.get_expected_build5_outputs()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(item["key"] == "client_report_pdf_bytes" for item in result)


def test_check_session_state_outputs_handles_empty_session_state():
    result = cr.check_session_state_outputs({})
    assert result["available_count"] == 0
    assert result["missing_count"] == result["total_expected"]
    assert result["completion_percentage"] == 0


def test_check_session_state_outputs_detects_available_outputs():
    result = cr.check_session_state_outputs(_FULL_STATE)
    assert result["available_count"] == result["total_expected"]
    assert result["completion_percentage"] == 100


def test_check_session_state_outputs_handles_missing_outputs_safely():
    result = cr.check_session_state_outputs({"audit_data": {"ok": True}})
    assert result["available_count"] == 1
    assert result["missing_count"] > 0
    assert result["recommended_next_actions"]


def test_check_documentation_files_returns_expected_keys(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text("# Test", encoding="utf-8")
    result = cr.check_documentation_files(str(tmp_path))
    assert "existing_files" in result
    assert "missing_files" in result
    assert "documentation_completion_percentage" in result


def test_generate_completion_score_returns_expected_keys():
    phases = cr.get_build5_phase_checklist()
    outputs = cr.check_session_state_outputs(_FULL_STATE)
    docs = {
        "documentation_completion_percentage": 100,
        "missing_files": [],
    }
    result = cr.generate_completion_score(phases, outputs, docs)
    assert "overall_status" in result
    assert "phase_completion_percentage" in result
    assert "output_completion_percentage" in result
    assert "documentation_completion_percentage" in result
    assert "final_readiness_label" in result
    assert "recommended_final_actions" in result


def test_generate_build5_completion_review_returns_expected_keys(tmp_path):
    result = cr.generate_build5_completion_review(_FULL_STATE, str(tmp_path))
    assert result["build_number"] == "Build 5"
    assert "completion_status" in result
    assert "phase_checklist" in result
    assert "output_status" in result
    assert "documentation_status" in result
    assert "responsible_use_position" in result


def test_generate_portfolio_summary_returns_expected_keys():
    result = cr.generate_portfolio_summary()
    assert "project_name" in result
    assert "one_line_summary" in result
    assert "target_users" in result
    assert "core_workflow" in result
    assert "what_this_demonstrates" in result


def test_generate_case_study_summary_returns_expected_keys():
    result = cr.generate_case_study_summary()
    assert "case_study_title" in result
    assert "client_context" in result
    assert "outputs_generated" in result
    assert "responsible_use_controls" in result
    assert "limitations" in result


def test_format_completion_review_as_markdown_returns_markdown(tmp_path):
    review = cr.generate_build5_completion_review(_FULL_STATE, str(tmp_path))
    result = cr.format_completion_review_as_markdown(review)
    assert isinstance(result, str)
    assert result.startswith("# Build 5 Completion Review")


def test_completion_markdown_includes_build5_completion_review(tmp_path):
    review = cr.generate_build5_completion_review(_FULL_STATE, str(tmp_path))
    result = cr.format_completion_review_as_markdown(review)
    assert "Build 5 Completion Review" in result


def test_completion_markdown_includes_responsible_use_position(tmp_path):
    review = cr.generate_build5_completion_review(_FULL_STATE, str(tmp_path))
    result = cr.format_completion_review_as_markdown(review)
    assert "Responsible-Use Position" in result


def test_format_portfolio_notes_as_markdown_returns_markdown():
    result = cr.format_portfolio_notes_as_markdown(
        cr.generate_portfolio_summary(),
        cr.generate_case_study_summary(),
    )
    assert isinstance(result, str)
    assert result.startswith("# Build 5 Portfolio Notes")


def test_portfolio_markdown_includes_build5_portfolio_notes():
    result = cr.format_portfolio_notes_as_markdown(
        cr.generate_portfolio_summary(),
        cr.generate_case_study_summary(),
    )
    assert "Build 5 Portfolio Notes" in result


def test_missing_outputs_are_handled_safely(tmp_path):
    review = cr.generate_build5_completion_review({}, str(tmp_path))
    markdown = cr.format_completion_review_as_markdown(review)
    assert review["output_status"]["missing_count"] > 0
    assert "Missing" in markdown
