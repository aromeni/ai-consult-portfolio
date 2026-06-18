"""Tests for logic/capstone_report.py — Build 9 Phase 6."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.capstone_report import (
    build_ai_adoption_journey_section,
    build_capstone_snapshot_section,
    build_client_overview_section,
    build_consulting_interpretation_section,
    build_cross_build_evidence_section,
    build_executive_summary,
    build_full_capstone_report,
    build_markdown_table,
    build_next_steps_section,
    build_recommendation_pathway_section,
    build_report_disclaimer,
    build_report_title,
    get_client_by_id,
    get_report_indicators_for_client,
    get_report_stages_for_client,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()


class TestBuildMarkdownTable:
    def test_markdown_table_renders_header_and_rows(self):
        rows = [{"Name": "BrightPath", "Sector": "Training"}]
        result = build_markdown_table(rows, ["Name", "Sector"])
        assert "| Name | Sector |" in result
        assert "| BrightPath | Training |" in result
        assert "| --- | --- |" in result

    def test_markdown_table_returns_no_data_for_empty_rows(self):
        result = build_markdown_table([], ["Name", "Sector"])
        assert "No data" in result


class TestGetClientById:
    def test_returns_matching_client(self):
        result = get_client_by_id(CLIENTS, "CAP001")
        assert result is not None
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_returns_none_for_unknown_id(self):
        result = get_client_by_id(CLIENTS, "UNKNOWN")
        assert result is None


class TestGetReportStagesForClient:
    def test_returns_all_stages_when_no_client_id(self):
        result = get_report_stages_for_client(STAGES, client_id=None)
        assert len(result) == len(STAGES)

    def test_returns_filtered_stages_for_client_id(self):
        result = get_report_stages_for_client(STAGES, client_id="CAP001")
        assert all(s["client_id"] == "CAP001" for s in result)
        assert len(result) < len(STAGES)


class TestGetReportIndicatorsForClient:
    def test_returns_all_indicators_when_no_client_id(self):
        result = get_report_indicators_for_client(INDICATORS, client_id=None)
        assert len(result) == len(INDICATORS)

    def test_returns_only_selected_client_indicator(self):
        result = get_report_indicators_for_client(INDICATORS, client_id="CAP001")
        assert [i["client_id"] for i in result] == ["CAP001"]


class TestBuildReportTitle:
    def test_portfolio_title_has_no_client_name(self):
        result = build_report_title(client=None)
        assert result.startswith("# AI Adoption Consulting Capstone Report")
        assert "BrightPath" not in result

    def test_client_title_includes_organisation_name(self):
        client = get_client_by_id(CLIENTS, "CAP001")
        result = build_report_title(client=client)
        assert "BrightPath Skills Training" in result


class TestBuildReportDisclaimer:
    def test_disclaimer_contains_synthetic_data_warning(self):
        result = build_report_disclaimer()
        assert "synthetic portfolio data only" in result
        assert "demonstration purposes" in result
        assert "real client" in result


class TestBuildExecutiveSummary:
    def test_executive_summary_returns_expected_heading(self):
        result = build_executive_summary(CLIENTS, STAGES, INDICATORS)
        assert "## Executive Summary" in result

    def test_executive_summary_includes_key_items(self):
        result = build_executive_summary(CLIENTS, STAGES, INDICATORS)
        assert "Strongest build area" in result
        assert "Weakest build area" in result
        assert "Recommended next step" in result

    def test_portfolio_summary_uses_multiple_client_context(self):
        result = build_executive_summary(CLIENTS, STAGES, INDICATORS)
        assert "**Clients in scope:** 3" in result
        assert "**Portfolio readiness:**" in result
        assert "**Journey stages:** 21 total" in result

    def test_client_summary_is_scoped_to_selected_client(self):
        result = build_executive_summary(
            CLIENTS, STAGES, INDICATORS, client_id="CAP001"
        )
        assert "BrightPath Skills Training" in result
        assert "**Client readiness:**" in result
        assert "**Journey stages:** 7 total, 7 completed" in result
        assert "**Clients in scope:** 3" not in result
        assert "**Portfolio readiness:**" not in result


class TestBuildClientOverviewSection:
    def test_client_overview_returns_expected_heading(self):
        result = build_client_overview_section(CLIENTS)
        assert "## Client Overview" in result

    def test_portfolio_overview_includes_all_clients(self):
        result = build_client_overview_section(CLIENTS)
        assert "BrightPath Skills Training" in result
        assert "Northside Community Advice" in result
        assert "Greenacre Dental Group" in result

    def test_client_overview_filters_to_one_client(self):
        result = build_client_overview_section(CLIENTS, client_id="CAP001")
        assert "BrightPath Skills Training" in result
        assert "Northside Community Advice" not in result


class TestBuildAiAdoptionJourneySection:
    def test_journey_section_returns_expected_heading(self):
        result = build_ai_adoption_journey_section(CLIENTS, STAGES, INDICATORS)
        assert "## AI Adoption Journey" in result

    def test_journey_section_includes_journey_health_column(self):
        result = build_ai_adoption_journey_section(CLIENTS, STAGES, INDICATORS)
        assert "journey_health" in result


class TestBuildCrossBuildEvidenceSection:
    def test_cross_build_section_returns_expected_heading(self):
        result = build_cross_build_evidence_section(STAGES)
        assert "## Cross-Build Evidence" in result

    def test_cross_build_section_includes_evidence_health_column(self):
        result = build_cross_build_evidence_section(STAGES)
        assert "evidence_health" in result


class TestBuildRecommendationPathwaySection:
    def test_recommendation_pathway_returns_expected_heading(self):
        result = build_recommendation_pathway_section(CLIENTS, STAGES, INDICATORS)
        assert "## Consulting Recommendation Pathway" in result

    def test_recommendation_pathway_includes_capstone_readiness_column(self):
        result = build_recommendation_pathway_section(CLIENTS, STAGES, INDICATORS)
        assert "capstone_readiness" in result


class TestBuildCapstoneSnapshotSection:
    def test_capstone_snapshot_returns_expected_heading(self):
        result = build_capstone_snapshot_section(CLIENTS, STAGES, INDICATORS)
        assert "## Capstone Snapshot" in result

    def test_capstone_snapshot_includes_dashboard_status(self):
        result = build_capstone_snapshot_section(CLIENTS, STAGES, INDICATORS)
        assert "Dashboard status" in result

    def test_client_snapshot_uses_selected_client_evidence(self):
        result = build_capstone_snapshot_section(
            CLIENTS, STAGES, INDICATORS, client_id="CAP001"
        )
        assert "Strong capstone dashboard" in result
        assert "Build 1" in result
        assert "Build 6" in result


class TestBuildConsultingInterpretationSection:
    def test_interpretation_returns_expected_text(self):
        result = build_consulting_interpretation_section()
        assert "consulting narrative" in result
        assert "readiness" in result
        assert "governance" in result


class TestBuildNextStepsSection:
    def test_next_steps_returns_expected_heading(self):
        result = build_next_steps_section(CLIENTS, STAGES, INDICATORS)
        assert "## Next Steps" in result

    def test_next_steps_includes_each_client(self):
        result = build_next_steps_section(CLIENTS, STAGES, INDICATORS)
        assert "BrightPath Skills Training" in result
        assert "Northside Community Advice" in result
        assert "Greenacre Dental Group" in result


class TestBuildFullCapstoneReport:
    def test_full_portfolio_report_builds(self):
        result = build_full_capstone_report(CLIENTS, STAGES, INDICATORS)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_full_client_report_builds(self):
        result = build_full_capstone_report(CLIENTS, STAGES, INDICATORS, client_id="CAP001")
        assert isinstance(result, str)
        assert "BrightPath Skills Training" in result
        assert "Northside Community Advice" not in result
        assert "Greenacre Dental Group" not in result
        assert "**Clients in scope:** 3" not in result
        assert "**Journey stages:** 7 total, 7 completed" in result

    def test_full_report_contains_all_major_headings(self):
        result = build_full_capstone_report(CLIENTS, STAGES, INDICATORS)
        assert "# AI Adoption Consulting Capstone Report" in result
        assert "## Executive Summary" in result
        assert "## Client Overview" in result
        assert "## Capstone Snapshot" in result
        assert "## AI Adoption Journey" in result
        assert "## Cross-Build Evidence" in result
        assert "## Consulting Recommendation Pathway" in result
        assert "## Consulting Interpretation" in result
        assert "## Next Steps" in result


class TestSyntheticDataProcessing:
    def test_all_synthetic_capstone_data_processes_without_errors(self):
        portfolio_report = build_full_capstone_report(CLIENTS, STAGES, INDICATORS)
        cap001_report = build_full_capstone_report(CLIENTS, STAGES, INDICATORS, client_id="CAP001")
        cap002_report = build_full_capstone_report(CLIENTS, STAGES, INDICATORS, client_id="CAP002")
        cap003_report = build_full_capstone_report(CLIENTS, STAGES, INDICATORS, client_id="CAP003")

        assert "## Executive Summary" in portfolio_report
        assert "BrightPath Skills Training" in cap001_report
        assert "Northside Community Advice" in cap002_report
        assert "Greenacre Dental Group" in cap003_report
        assert "Northside Community Advice" not in cap001_report
