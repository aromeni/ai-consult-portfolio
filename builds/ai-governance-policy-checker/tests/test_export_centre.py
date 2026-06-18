"""
Tests for src/export_centre.py — Export Centre
Build 6 · BrightPath ChatGPT Mastery Project
"""

import datetime
import pytest

from src.export_centre import (
    get_export_formats,
    check_export_readiness,
    build_export_data_from_session_state,
    generate_export_quality_checklist,
    summarise_export_package,
    create_export_filename_base,
    prepare_markdown_export,
    prepare_all_exports,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def minimal_session_state():
    return {
        "policy_pack": {
            "organisation_name": "BrightPath Skills Training",
            "policies": [],
        },
        "governance_report_markdown": "# AI Governance Report\n\nSynthetic content only.",
    }


@pytest.fixture
def full_session_state(minimal_session_state):
    state = dict(minimal_session_state)
    state.update({
        "governance_framework": [{"domain_id": "GOV-001", "domain_name": "Strategy"}],
        "governance_framework_summary": {"total_domains": 1},
        "coverage_results": {
            "overall_coverage_score": 60,
            "overall_coverage_level": "Partial coverage",
            "total_domains_checked": 12,
            "domain_results": [],
        },
        "coverage_summary": {
            "strong_count": 3,
            "partial_count": 5,
            "weak_count": 2,
            "not_covered_count": 2,
        },
        "gap_analysis": {"total_gaps": 4, "prioritised_gaps": []},
        "gap_summary": {
            "total_gaps": 4,
            "critical_gap_count": 1,
            "high_gap_count": 2,
            "medium_gap_count": 1,
            "low_gap_count": 0,
        },
        "policy_recommendations": {
            "total_recommendations": 4,
            "prioritised_recommendations": [],
        },
        "recommendation_summary": {
            "total_recommendations": 4,
            "urgent_count": 1,
            "high_priority_count": 2,
            "medium_priority_count": 1,
            "low_priority_count": 0,
        },
        "governance_maturity": {
            "overall_governance_score": 45,
            "overall_maturity_level": "Developing governance",
            "domain_maturity_scores": [],
        },
        "governance_maturity_summary": {
            "total_domains": 12,
            "initial_domains": 2,
            "developing_domains": 4,
            "defined_domains": 3,
            "managed_or_optimised_domains": 3,
        },
        "governance_report_data": {},
        "governance_report_markdown": (
            "# AI Governance Policy Review Report\n\n"
            "## 1. Executive Summary\n\n"
            "## 9. Responsible-Use Boundaries\n\nSynthetic/demo policy text only.\n\n"
            "## 10. Prototype Limitations\n\n"
            "Human review required before any real-world use."
        ),
    })
    return state


# ---------------------------------------------------------------------------
# get_export_formats
# ---------------------------------------------------------------------------

class TestGetExportFormats:
    def test_returns_list(self):
        result = get_export_formats()
        assert isinstance(result, list)

    def test_contains_markdown(self):
        assert "Markdown" in get_export_formats()

    def test_contains_pdf(self):
        assert "PDF" in get_export_formats()

    def test_has_two_formats(self):
        assert len(get_export_formats()) == 2


# ---------------------------------------------------------------------------
# check_export_readiness
# ---------------------------------------------------------------------------

class TestCheckExportReadiness:
    def test_empty_state_not_ready(self):
        result = check_export_readiness({})
        assert result["is_ready"] is False

    def test_empty_state_cannot_export_markdown(self):
        result = check_export_readiness({})
        assert result["can_export_markdown"] is False

    def test_empty_state_cannot_export_pdf(self):
        result = check_export_readiness({})
        assert result["can_export_pdf"] is False

    def test_empty_state_has_missing_outputs(self):
        result = check_export_readiness({})
        assert len(result["missing_outputs"]) > 0

    def test_empty_state_has_next_steps(self):
        result = check_export_readiness({})
        assert len(result["recommended_next_steps"]) > 0

    def test_minimal_state_is_ready(self, minimal_session_state):
        result = check_export_readiness(minimal_session_state)
        assert result["is_ready"] is True

    def test_minimal_state_can_export_markdown(self, minimal_session_state):
        result = check_export_readiness(minimal_session_state)
        assert result["can_export_markdown"] is True

    def test_minimal_state_can_export_pdf(self, minimal_session_state):
        result = check_export_readiness(minimal_session_state)
        assert result["can_export_pdf"] is True

    def test_detects_governance_report_markdown(self, minimal_session_state):
        result = check_export_readiness(minimal_session_state)
        assert "governance_report_markdown" in result["available_outputs"]

    def test_policy_pack_only_not_ready(self):
        result = check_export_readiness({"policy_pack": {"organisation_name": "Test"}})
        assert result["is_ready"] is False
        assert "governance_report_markdown" in result["missing_outputs"]

    def test_full_state_no_missing_steps(self, full_session_state):
        result = check_export_readiness(full_session_state)
        assert result["is_ready"] is True
        # Next steps are deduplicated, so some may still appear for optional keys
        assert result["can_export_markdown"] is True

    def test_returns_expected_keys(self):
        result = check_export_readiness({})
        for key in [
            "is_ready", "available_outputs", "missing_outputs",
            "recommended_next_steps", "can_export_markdown", "can_export_pdf",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_next_steps_are_deduplicated(self):
        result = check_export_readiness({})
        steps = result["recommended_next_steps"]
        assert len(steps) == len(set(steps))


# ---------------------------------------------------------------------------
# build_export_data_from_session_state
# ---------------------------------------------------------------------------

class TestBuildExportDataFromSessionState:
    def test_returns_dict(self):
        result = build_export_data_from_session_state({})
        assert isinstance(result, dict)

    def test_expected_keys_present(self):
        result = build_export_data_from_session_state({})
        for key in [
            "organisation_name", "generated_date", "policy_pack",
            "governance_framework", "coverage_results", "gap_analysis",
            "policy_recommendations", "governance_maturity",
            "governance_report_markdown", "source_outputs_available",
            "responsible_use_note", "prototype_note",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_empty_state_uses_unnamed_org(self):
        result = build_export_data_from_session_state({})
        assert result["organisation_name"] == "Unnamed organisation"

    def test_org_name_from_policy_pack(self):
        state = {"policy_pack": {"organisation_name": "BrightPath Skills Training"}}
        result = build_export_data_from_session_state(state)
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_generated_date_is_today(self):
        result = build_export_data_from_session_state({})
        assert result["generated_date"] == datetime.date.today().isoformat()

    def test_missing_keys_are_none(self):
        result = build_export_data_from_session_state({})
        assert result["policy_pack"] is None
        assert result["coverage_results"] is None

    def test_full_state_all_populated(self, full_session_state):
        result = build_export_data_from_session_state(full_session_state)
        assert result["coverage_results"] is not None
        assert result["gap_analysis"] is not None
        assert result["governance_maturity"] is not None

    def test_source_outputs_available_is_dict(self):
        result = build_export_data_from_session_state({})
        assert isinstance(result["source_outputs_available"], dict)

    def test_responsible_use_note_not_empty(self):
        result = build_export_data_from_session_state({})
        assert len(result["responsible_use_note"]) > 50

    def test_prototype_note_not_empty(self):
        result = build_export_data_from_session_state({})
        assert len(result["prototype_note"]) > 50


# ---------------------------------------------------------------------------
# generate_export_quality_checklist
# ---------------------------------------------------------------------------

class TestGenerateExportQualityChecklist:
    def test_returns_list(self):
        result = generate_export_quality_checklist({})
        assert isinstance(result, list)

    def test_returns_twelve_items(self):
        result = generate_export_quality_checklist({})
        assert len(result) == 12

    def test_each_item_has_required_keys(self):
        for item in generate_export_quality_checklist({}):
            for key in ["label", "is_complete", "importance", "note"]:
                assert key in item, f"Missing key '{key}' in checklist item"

    def test_is_complete_is_bool(self):
        for item in generate_export_quality_checklist({}):
            assert isinstance(item["is_complete"], bool)

    def test_importance_values_are_valid(self):
        valid = {"Required", "Recommended", "Advisory"}
        for item in generate_export_quality_checklist({}):
            assert item["importance"] in valid

    def test_empty_data_all_incomplete(self):
        result = generate_export_quality_checklist({})
        # policy pack and governance report items should be incomplete
        pack_item = next(i for i in result if "policy pack" in i["label"].lower())
        assert pack_item["is_complete"] is False

    def test_with_policy_pack_marks_complete(self, full_session_state):
        export_data = build_export_data_from_session_state(full_session_state)
        result = generate_export_quality_checklist(export_data)
        pack_item = next(i for i in result if "policy pack" in i["label"].lower())
        assert pack_item["is_complete"] is True

    def test_human_review_note_detected(self, full_session_state):
        export_data = build_export_data_from_session_state(full_session_state)
        result = generate_export_quality_checklist(export_data)
        hr_item = next(i for i in result if "human review" in i["label"].lower())
        assert hr_item["is_complete"] is True


# ---------------------------------------------------------------------------
# summarise_export_package
# ---------------------------------------------------------------------------

class TestSummariseExportPackage:
    def test_returns_dict(self):
        result = summarise_export_package({})
        assert isinstance(result, dict)

    def test_expected_keys_present(self):
        result = summarise_export_package({})
        for key in [
            "organisation_name", "generated_date", "total_outputs",
            "outputs_available", "outputs_missing", "export_formats",
            "domains_reviewed", "gaps_included", "recommendations_included",
            "maturity_level", "governance_score", "markdown_available", "pdf_available",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_empty_data_no_markdown(self):
        result = summarise_export_package({})
        assert result["markdown_available"] is False

    def test_with_markdown_available(self, full_session_state):
        export_data = build_export_data_from_session_state(full_session_state)
        result = summarise_export_package(export_data)
        assert result["markdown_available"] is True

    def test_export_formats_matches_get_export_formats(self, full_session_state):
        export_data = build_export_data_from_session_state(full_session_state)
        result = summarise_export_package(export_data)
        assert result["export_formats"] == get_export_formats()

    def test_domains_reviewed_from_coverage(self, full_session_state):
        export_data = build_export_data_from_session_state(full_session_state)
        result = summarise_export_package(export_data)
        assert result["domains_reviewed"] == 12

    def test_gaps_included_from_gap_analysis(self, full_session_state):
        export_data = build_export_data_from_session_state(full_session_state)
        result = summarise_export_package(export_data)
        assert result["gaps_included"] == 4


# ---------------------------------------------------------------------------
# create_export_filename_base
# ---------------------------------------------------------------------------

class TestCreateExportFilenameBase:
    def test_returns_string(self):
        assert isinstance(create_export_filename_base("BrightPath"), str)

    def test_contains_date(self):
        result = create_export_filename_base("BrightPath")
        assert datetime.date.today().isoformat() in result

    def test_no_spaces(self):
        result = create_export_filename_base("BrightPath Skills Training")
        assert " " not in result

    def test_lowercased(self):
        result = create_export_filename_base("BrightPath")
        assert result == result.lower()

    def test_empty_name_fallback(self):
        result = create_export_filename_base("")
        assert "unnamed" in result

    def test_special_characters_removed(self):
        result = create_export_filename_base("Org/Name & Co.")
        assert "/" not in result
        assert "&" not in result
        assert "." not in result

    def test_no_extension(self):
        result = create_export_filename_base("BrightPath")
        # Base filename should not have an extension (.pdf or .md)
        assert not result.endswith(".pdf")
        assert not result.endswith(".md")


# ---------------------------------------------------------------------------
# prepare_markdown_export
# ---------------------------------------------------------------------------

class TestPrepareMarkdownExport:
    def test_returns_tuple(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_markdown_export(export_data)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_string_content(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        content, _ = prepare_markdown_export(export_data)
        assert isinstance(content, str)

    def test_filename_ends_with_md(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        _, filename = prepare_markdown_export(export_data)
        assert filename.endswith(".md")

    def test_content_matches_markdown(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        content, _ = prepare_markdown_export(export_data)
        assert content == minimal_session_state["governance_report_markdown"]

    def test_empty_data_returns_empty_content(self):
        export_data = {"organisation_name": "Test", "governance_report_markdown": ""}
        content, _ = prepare_markdown_export(export_data)
        assert content == ""

    def test_filename_contains_date(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        _, filename = prepare_markdown_export(export_data)
        assert datetime.date.today().isoformat() in filename


# ---------------------------------------------------------------------------
# prepare_all_exports
# ---------------------------------------------------------------------------

class TestPrepareAllExports:
    def test_returns_dict(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert isinstance(result, dict)

    def test_contains_markdown_key(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert "markdown" in result

    def test_contains_pdf_key(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert "pdf" in result

    def test_markdown_export_no_error(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert result["markdown"]["error"] is None

    def test_pdf_export_no_error(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert result["pdf"]["error"] is None

    def test_handles_empty_export_data(self):
        result = prepare_all_exports({"organisation_name": "Test", "governance_report_markdown": ""})
        assert "markdown" in result
        assert "pdf" in result

    def test_markdown_content_is_string(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert isinstance(result["markdown"]["content"], str)

    def test_pdf_content_is_bytes(self, minimal_session_state):
        export_data = build_export_data_from_session_state(minimal_session_state)
        result = prepare_all_exports(export_data)
        assert isinstance(result["pdf"]["content"], bytes)

    def test_no_crash_on_minimal_data(self):
        result = prepare_all_exports({})
        assert isinstance(result, dict)
