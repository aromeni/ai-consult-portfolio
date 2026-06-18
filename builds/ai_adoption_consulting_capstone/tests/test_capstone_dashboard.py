"""Tests for logic/capstone_dashboard.py — Build 9 Phase 5."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.capstone_dashboard import (
    build_capstone_snapshot,
    build_client_dashboard_context,
    build_client_selector_options,
    build_dashboard_metric_summary,
    build_dashboard_table_rows,
    build_portfolio_dashboard_context,
    classify_dashboard_status,
    get_client_by_selector_label,
    identify_dashboard_focus,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()

EXPECTED_CLIENT_CONTEXT_KEYS = {
    "client",
    "client_stages",
    "indicator",
    "journey_summary",
    "recommendation_summary",
}

EXPECTED_PORTFOLIO_CONTEXT_KEYS = {
    "clients",
    "stages",
    "indicators",
    "phase_1_summary",
    "journey_summaries",
    "journey_health_summary",
    "cross_build_summaries",
    "cross_build_insight_summary",
    "recommendations",
    "recommendation_pathway_summary",
}

EXPECTED_METRIC_KEYS = {
    "total_clients",
    "total_build_areas",
    "total_cross_build_stages",
    "capstone_ready_count",
    "nearly_ready_count",
    "needs_strengthening_count",
    "not_ready_count",
    "strong_journey_count",
    "healthy_journey_count",
    "developing_journey_count",
    "needs_review_count",
    "blocked_journey_count",
    "very_strong_evidence_count",
    "strong_evidence_count",
    "developing_evidence_count",
    "weak_evidence_count",
}

EXPECTED_SNAPSHOT_KEYS = {
    "dashboard_status",
    "dashboard_focus",
    "strongest_build_area",
    "weakest_build_area",
    "recommended_dashboard_next_step",
}

EXPECTED_TABLE_ROW_KEYS = {
    "client_journey_rows",
    "cross_build_rows",
    "recommendation_rows",
}

# Controlled context fixtures

STRONG_PORTFOLIO_CONTEXT = {
    "clients": CLIENTS,
    "phases_1_summary": {},
    "recommendation_pathway_summary": {
        "capstone_ready_count": 1,
        "nearly_ready_count": 0,
        "needs_strengthening_count": 2,
        "not_ready_count": 0,
    },
    "journey_health_summary": {
        "strong_journey_count": 1,
        "healthy_journey_count": 0,
        "developing_journey_count": 2,
        "needs_review_count": 0,
        "blocked_journey_count": 0,
    },
    "cross_build_insight_summary": {
        "total_build_areas": 7,
        "very_strong_evidence_count": 2,
        "strong_evidence_count": 2,
        "developing_evidence_count": 3,
        "weak_evidence_count": 0,
        "no_evidence_count": 0,
        "strongest_build_area": "Build 4",
        "weakest_build_area": "Build 8",
    },
    "phase_1_summary": {
        "total_cross_build_stages": 21,
    },
    "journey_summaries": [],
    "cross_build_summaries": [],
    "recommendations": [],
}

NEEDS_REVIEW_CONTEXT = {
    "clients": CLIENTS,
    "recommendation_pathway_summary": {
        "capstone_ready_count": 0,
        "nearly_ready_count": 0,
        "needs_strengthening_count": 2,
        "not_ready_count": 1,
    },
    "journey_health_summary": {
        "strong_journey_count": 0,
        "healthy_journey_count": 0,
        "developing_journey_count": 2,
        "needs_review_count": 0,
        "blocked_journey_count": 1,
    },
    "cross_build_insight_summary": {
        "total_build_areas": 7,
        "very_strong_evidence_count": 0,
        "strong_evidence_count": 0,
        "developing_evidence_count": 4,
        "weak_evidence_count": 3,
        "no_evidence_count": 0,
        "strongest_build_area": "Build 4",
        "weakest_build_area": "Build 8",
    },
    "phase_1_summary": {
        "total_cross_build_stages": 21,
    },
    "journey_summaries": [],
    "cross_build_summaries": [],
    "recommendations": [],
}


class TestBuildClientDashboardContext:
    def test_client_dashboard_context_has_expected_keys(self):
        client = CLIENTS[0]
        result = build_client_dashboard_context(client, STAGES, INDICATORS)
        assert EXPECTED_CLIENT_CONTEXT_KEYS.issubset(result.keys())

    def test_client_spotlight_values_are_populated(self):
        client = CLIENTS[0]
        result = build_client_dashboard_context(client, STAGES, INDICATORS)
        recommendation = result["recommendation_summary"]
        assert result["client"]["consulting_priority"]
        assert recommendation["commercial_next_step"]
        assert recommendation["capstone_readiness"]
        assert recommendation["recommendation_priority"]


class TestBuildPortfolioDashboardContext:
    def test_portfolio_dashboard_context_has_expected_keys(self):
        result = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        assert EXPECTED_PORTFOLIO_CONTEXT_KEYS.issubset(result.keys())


class TestClassifyDashboardStatus:
    def test_returns_strong_capstone_dashboard(self):
        result = classify_dashboard_status(STRONG_PORTFOLIO_CONTEXT)
        assert result == "Strong capstone dashboard"

    def test_returns_needs_review(self):
        result = classify_dashboard_status(NEEDS_REVIEW_CONTEXT)
        assert result == "Needs review"


class TestIdentifyDashboardFocus:
    def test_detects_weak_evidence(self):
        result = identify_dashboard_focus(NEEDS_REVIEW_CONTEXT)
        assert "weak" in result.lower()

    def test_detects_blocked_journey_when_no_weak_evidence(self):
        context = {
            **NEEDS_REVIEW_CONTEXT,
            "cross_build_insight_summary": {
                **NEEDS_REVIEW_CONTEXT["cross_build_insight_summary"],
                "weak_evidence_count": 0,
            },
        }
        result = identify_dashboard_focus(context)
        assert "blocked" in result.lower()


class TestBuildDashboardMetricSummary:
    def test_metric_summary_has_expected_keys(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        result = build_dashboard_metric_summary(context)
        assert EXPECTED_METRIC_KEYS.issubset(result.keys())


class TestBuildCapstoneSnapshot:
    def test_capstone_snapshot_has_expected_keys(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        result = build_capstone_snapshot(context)
        assert EXPECTED_SNAPSHOT_KEYS.issubset(result.keys())


class TestBuildClientSelectorOptions:
    def test_selector_options_return_one_label_per_client(self):
        result = build_client_selector_options(CLIENTS)
        assert len(result) == len(CLIENTS)

    def test_selector_labels_contain_organisation_name(self):
        result = build_client_selector_options(CLIENTS)
        assert any("BrightPath Skills Training" in label for label in result)


class TestGetClientBySelectorLabel:
    def test_lookup_by_selector_label_returns_matching_client(self):
        options = build_client_selector_options(CLIENTS)
        first_label = options[0]
        result = get_client_by_selector_label(CLIENTS, first_label)
        assert result is not None
        assert result["client_id"] == CLIENTS[0]["client_id"]

    def test_lookup_by_unknown_label_returns_none(self):
        result = get_client_by_selector_label(CLIENTS, "Unknown Org — Unknown sector")
        assert result is None


class TestBuildDashboardTableRows:
    def test_dashboard_table_rows_have_expected_keys(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        result = build_dashboard_table_rows(context)
        assert EXPECTED_TABLE_ROW_KEYS.issubset(result.keys())

    def test_client_journey_rows_match_client_count(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        result = build_dashboard_table_rows(context)
        assert len(result["client_journey_rows"]) == len(CLIENTS)

    def test_cross_build_rows_match_build_count(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        result = build_dashboard_table_rows(context)
        assert len(result["cross_build_rows"]) == 7

    def test_recommendation_rows_match_client_count(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        result = build_dashboard_table_rows(context)
        assert len(result["recommendation_rows"]) == len(CLIENTS)


class TestSyntheticDataProcessing:
    def test_all_synthetic_capstone_data_processes_without_errors(self):
        context = build_portfolio_dashboard_context(CLIENTS, STAGES, INDICATORS)
        snapshot = build_capstone_snapshot(context)
        metrics = build_dashboard_metric_summary(context)
        table_rows = build_dashboard_table_rows(context)
        options = build_client_selector_options(CLIENTS)
        client = get_client_by_selector_label(CLIENTS, options[0])
        client_ctx = build_client_dashboard_context(client, STAGES, INDICATORS)

        assert snapshot["dashboard_status"] in (
            "Strong capstone dashboard",
            "Portfolio-ready dashboard",
            "Developing dashboard",
            "Needs review",
        )
        assert metrics["total_clients"] == 3
        assert len(table_rows["client_journey_rows"]) == 3
        assert len(table_rows["cross_build_rows"]) == 7
        assert len(table_rows["recommendation_rows"]) == 3
        assert len(options) == 3
        assert client is not None
        assert EXPECTED_CLIENT_CONTEXT_KEYS.issubset(client_ctx.keys())
