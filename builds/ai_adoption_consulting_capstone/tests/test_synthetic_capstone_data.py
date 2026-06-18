"""Tests for data/synthetic_capstone_data.py — Build 9 Phase 1."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.capstone_dashboard import (
    build_capstone_snapshot,
    build_portfolio_dashboard_context,
)
from logic.capstone_overview import validate_all_capstone_data
from logic.client_journey import build_all_client_journey_summaries
from logic.cross_build_insights import build_all_cross_build_summaries
from logic.recommendation_pathway import build_all_consulting_recommendations

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()

EXPECTED_BUILD_NUMBERS = {
    "Build 1",
    "Build 2/3",
    "Build 4",
    "Build 5",
    "Build 6",
    "Build 7",
    "Build 8",
}


class TestSyntheticCapstoneClients:
    def test_returns_at_least_three_clients(self):
        assert len(CLIENTS) >= 3

    def test_client_ids_are_unique(self):
        ids = [c["client_id"] for c in CLIENTS]
        assert len(ids) == len(set(ids))


class TestSyntheticCrossBuildStages:
    def test_returns_stage_records(self):
        assert len(STAGES) > 0

    def test_stage_ids_are_unique(self):
        ids = [s["stage_id"] for s in STAGES]
        assert len(ids) == len(set(ids))

    def test_each_client_has_all_build_coverage(self):
        for client in CLIENTS:
            client_id = client["client_id"]
            client_stages = [s for s in STAGES if s["client_id"] == client_id]
            build_numbers = {s["build_number"] for s in client_stages}
            missing = EXPECTED_BUILD_NUMBERS - build_numbers
            assert not missing, (
                f"Client {client_id} is missing build coverage for: {missing}"
            )

    def test_all_stage_client_ids_exist_in_client_list(self):
        client_ids = {c["client_id"] for c in CLIENTS}
        for stage in STAGES:
            assert stage["client_id"] in client_ids, (
                f"Stage {stage['stage_id']} references unknown client_id: {stage['client_id']}"
            )


class TestSyntheticCapstoneIndicators:
    def test_returns_one_indicator_per_client(self):
        client_ids = {c["client_id"] for c in CLIENTS}
        indicator_client_ids = {i["client_id"] for i in INDICATORS}
        assert client_ids == indicator_client_ids

    def test_all_synthetic_data_passes_validation(self):
        result = validate_all_capstone_data(CLIENTS, STAGES, INDICATORS)
        assert result["warnings"] == [], (
            f"Unexpected validation warnings: {result['warnings']}"
        )
        assert result["valid_clients"] == result["total_clients"]
        assert result["valid_stages"] == result["total_stages"]
        assert result["valid_indicators"] == result["total_indicators"]


class TestSyntheticDemonstrationRange:
    def test_includes_positive_and_review_needed_readiness_cases(self):
        journey_summaries = build_all_client_journey_summaries(
            CLIENTS, STAGES, INDICATORS
        )
        recommendations = build_all_consulting_recommendations(journey_summaries)
        readiness = {r["capstone_readiness"] for r in recommendations}
        assert readiness & {"Capstone ready", "Nearly ready"}
        assert readiness & {"Needs strengthening", "Not ready"}

    def test_includes_strong_and_developing_build_evidence(self):
        summaries = build_all_cross_build_summaries(STAGES)
        evidence_health = {summary["evidence_health"] for summary in summaries}
        assert evidence_health & {"Strong evidence", "Very strong evidence"}
        assert evidence_health & {"Developing evidence", "Weak evidence"}

    def test_dashboard_supports_positive_and_review_needed_states(self):
        portfolio_context = build_portfolio_dashboard_context(
            CLIENTS, STAGES, INDICATORS
        )
        portfolio_snapshot = build_capstone_snapshot(portfolio_context)
        assert portfolio_snapshot["dashboard_status"] != "Needs review"

        client_statuses = set()
        for client in CLIENTS:
            client_id = client["client_id"]
            client_stages = [
                stage for stage in STAGES if stage["client_id"] == client_id
            ]
            client_indicators = [
                indicator
                for indicator in INDICATORS
                if indicator["client_id"] == client_id
            ]
            context = build_portfolio_dashboard_context(
                [client], client_stages, client_indicators
            )
            client_statuses.add(build_capstone_snapshot(context)["dashboard_status"])

        assert "Strong capstone dashboard" in client_statuses
        assert "Needs review" in client_statuses
