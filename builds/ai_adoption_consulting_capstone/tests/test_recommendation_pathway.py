"""Tests for logic/recommendation_pathway.py — Build 9 Phase 4."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.client_journey import build_all_client_journey_summaries
from logic.recommendation_pathway import (
    add_consulting_recommendation_text,
    build_all_consulting_recommendations,
    build_consulting_recommendation_summary,
    build_recommendation_pathway_matrix,
    classify_capstone_readiness,
    classify_recommendation_priority,
    generate_consulting_recommendation_text,
    identify_commercial_next_step,
    identify_consulting_pathway,
    identify_primary_improvement_area,
    prioritise_recommendations,
    summarise_recommendation_pathways,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()

# Controlled client summary fixtures

SUMMARY_CAPSTONE_READY = {
    "client_id": "TEST001",
    "organisation_name": "Strong Org",
    "sector": "Test",
    "capstone_stage": "Final review",
    "journey_health": "Strong journey",
    "stage_completion_rate": 90.0,
    "average_evidence_score": 3.6,
    "weakest_stage": "Delivery tracking",
    "recommended_next_step": "Prepare capstone presentation.",
}

SUMMARY_NEARLY_READY = {
    "client_id": "TEST002",
    "organisation_name": "Healthy Org",
    "sector": "Test",
    "capstone_stage": "Active rollout",
    "journey_health": "Healthy journey",
    "stage_completion_rate": 75.0,
    "average_evidence_score": 3.1,
    "weakest_stage": "Governance review",
    "recommended_next_step": "Confirm remaining evidence gaps.",
}

SUMMARY_NEEDS_STRENGTHENING = {
    "client_id": "TEST003",
    "organisation_name": "Developing Org",
    "sector": "Test",
    "capstone_stage": "Pilot phase",
    "journey_health": "Developing journey",
    "stage_completion_rate": 57.14,
    "average_evidence_score": 2.43,
    "weakest_stage": "Governance review",
    "recommended_next_step": "Continue building evidence.",
}

SUMMARY_NOT_READY = {
    "client_id": "TEST004",
    "organisation_name": "Blocked Org",
    "sector": "Test",
    "capstone_stage": "Early stage",
    "journey_health": "Blocked journey",
    "stage_completion_rate": 28.57,
    "average_evidence_score": 1.5,
    "weakest_stage": "Impact measurement",
    "recommended_next_step": "Resolve governance gaps first.",
}

EXPECTED_RECOMMENDATION_KEYS = {
    "client_id",
    "organisation_name",
    "sector",
    "capstone_stage",
    "journey_health",
    "stage_completion_rate",
    "average_evidence_score",
    "weakest_stage",
    "capstone_readiness",
    "consulting_pathway",
    "commercial_next_step",
    "primary_improvement_area",
    "recommendation_priority",
    "recommended_next_step",
}

EXPECTED_PATHWAY_SUMMARY_KEYS = {
    "total_clients",
    "capstone_ready_count",
    "nearly_ready_count",
    "needs_strengthening_count",
    "not_ready_count",
    "high_priority_count",
    "medium_priority_count",
    "low_priority_count",
}


class TestClassifyCapstoneReadiness:
    def test_returns_capstone_ready(self):
        result = classify_capstone_readiness(SUMMARY_CAPSTONE_READY)
        assert result == "Capstone ready"

    def test_returns_nearly_ready(self):
        result = classify_capstone_readiness(SUMMARY_NEARLY_READY)
        assert result == "Nearly ready"

    def test_returns_needs_strengthening(self):
        result = classify_capstone_readiness(SUMMARY_NEEDS_STRENGTHENING)
        assert result == "Needs strengthening"

    def test_returns_not_ready(self):
        result = classify_capstone_readiness(SUMMARY_NOT_READY)
        assert result == "Not ready"


class TestIdentifyConsultingPathway:
    def test_consulting_pathway_classification_works(self):
        assert identify_consulting_pathway(SUMMARY_NOT_READY) == "Complete missing journey stages"
        assert identify_consulting_pathway(SUMMARY_NEEDS_STRENGTHENING) == "Strengthen weak evidence"
        assert identify_consulting_pathway(SUMMARY_NEARLY_READY) == "Prepare client-facing follow-up"
        assert identify_consulting_pathway(SUMMARY_CAPSTONE_READY) == "Ready for capstone presentation"


class TestIdentifyCommercialNextStep:
    def test_commercial_next_step_classification_works(self):
        assert identify_commercial_next_step(SUMMARY_CAPSTONE_READY) == "Portfolio demonstration"
        assert identify_commercial_next_step(SUMMARY_NEARLY_READY) == "Paid implementation review"
        assert identify_commercial_next_step(SUMMARY_NEEDS_STRENGTHENING) == "Training and adoption support package"
        assert identify_commercial_next_step(SUMMARY_NOT_READY) == "Document intelligence upgrade"


class TestIdentifyPrimaryImprovementArea:
    def test_primary_improvement_area_returns_weakest_stage(self):
        result = identify_primary_improvement_area(SUMMARY_NEEDS_STRENGTHENING)
        assert result == "Governance review"

    def test_primary_improvement_area_falls_back_when_missing(self):
        result = identify_primary_improvement_area({"weakest_stage": "No stages available"})
        assert result == "Review full client journey"

    def test_primary_improvement_area_falls_back_when_empty(self):
        result = identify_primary_improvement_area({})
        assert result == "Review full client journey"


class TestClassifyRecommendationPriority:
    def test_recommendation_priority_classification_works(self):
        assert classify_recommendation_priority(SUMMARY_NOT_READY) == "High priority"
        assert classify_recommendation_priority({"journey_health": "Needs review"}) == "High priority"
        assert classify_recommendation_priority(SUMMARY_NEEDS_STRENGTHENING) == "Medium priority"
        assert classify_recommendation_priority(SUMMARY_NEARLY_READY) == "Low priority"
        assert classify_recommendation_priority(SUMMARY_CAPSTONE_READY) == "Low priority"


class TestBuildConsultingRecommendationSummary:
    def test_recommendation_summary_has_expected_keys(self):
        result = build_consulting_recommendation_summary(SUMMARY_NEEDS_STRENGTHENING)
        assert EXPECTED_RECOMMENDATION_KEYS.issubset(result.keys())


class TestBuildAllConsultingRecommendations:
    def test_all_recommendation_summaries_match_input_length(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        result = build_all_consulting_recommendations(client_summaries)
        assert len(result) == len(client_summaries)


class TestSummariseRecommendationPathways:
    def test_pathway_summary_returns_expected_keys(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        recommendations = build_all_consulting_recommendations(client_summaries)
        result = summarise_recommendation_pathways(recommendations)
        assert EXPECTED_PATHWAY_SUMMARY_KEYS.issubset(result.keys())

    def test_pathway_summary_counts_sum_to_total(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        recommendations = build_all_consulting_recommendations(client_summaries)
        result = summarise_recommendation_pathways(recommendations)
        readiness_total = (
            result["capstone_ready_count"]
            + result["nearly_ready_count"]
            + result["needs_strengthening_count"]
            + result["not_ready_count"]
        )
        assert readiness_total == result["total_clients"]


class TestPrioritiseRecommendations:
    def test_prioritisation_puts_weakest_demo_client_first(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        recommendations = build_all_consulting_recommendations(client_summaries)
        result = prioritise_recommendations(recommendations)
        assert result[0]["client_id"] == "CAP003"
        assert result[-1]["client_id"] == "CAP001"


class TestGenerateConsultingRecommendationText:
    def test_recommendation_text_generation_works(self):
        capstone_ready_rec = {"capstone_readiness": "Capstone ready"}
        result = generate_consulting_recommendation_text(capstone_ready_rec)
        assert "capstone demonstration" in result.lower()

        not_ready_rec = {"capstone_readiness": "Not ready"}
        result = generate_consulting_recommendation_text(not_ready_rec)
        assert "blocked stages" in result.lower()


class TestAddConsultingRecommendationText:
    def test_recommendation_text_is_added_without_mutating_originals(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        recommendations = build_all_consulting_recommendations(client_summaries)
        original_keys = set(recommendations[0].keys())
        result = add_consulting_recommendation_text(recommendations)
        assert "consulting_recommendation" in result[0]
        assert "consulting_recommendation" not in recommendations[0]
        assert set(recommendations[0].keys()) == original_keys


class TestBuildRecommendationPathwayMatrix:
    def test_pathway_matrix_returns_expected_fields(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        recommendations = build_all_consulting_recommendations(client_summaries)
        result = build_recommendation_pathway_matrix(recommendations)
        assert len(result) == len(recommendations)
        expected_fields = {
            "organisation_name",
            "capstone_readiness",
            "consulting_pathway",
            "commercial_next_step",
            "primary_improvement_area",
            "recommendation_priority",
        }
        for row in result:
            assert expected_fields.issubset(row.keys())


class TestSyntheticDataProcessing:
    def test_all_synthetic_capstone_data_processes_without_errors(self):
        client_summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        recommendations = build_all_consulting_recommendations(client_summaries)
        recommendations_with_text = add_consulting_recommendation_text(recommendations)
        pathway_summary = summarise_recommendation_pathways(recommendations)
        prioritised = prioritise_recommendations(recommendations_with_text)
        matrix = build_recommendation_pathway_matrix(recommendations_with_text)
        assert len(recommendations_with_text) == 3
        assert pathway_summary["total_clients"] == 3
        assert len(prioritised) == 3
        assert len(matrix) == 3
