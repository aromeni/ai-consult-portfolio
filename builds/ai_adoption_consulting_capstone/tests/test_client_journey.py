"""Tests for logic/client_journey.py — Build 9 Phase 2."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.client_journey import (
    add_journey_recommendations,
    build_all_client_journey_summaries,
    build_client_journey_summary,
    calculate_average_evidence_score,
    calculate_stage_completion_rate,
    classify_journey_health,
    generate_client_journey_recommendation,
    identify_next_journey_step,
    identify_weakest_stage,
    prioritise_clients_for_review,
    sort_stages_by_journey_order,
    summarise_journey_health,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()

# Controlled stage fixtures for deterministic tests

STAGES_MIXED = [
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Readiness diagnosis"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Document intelligence"},
    {"stage_status": "In progress", "evidence_strength": "Moderate", "journey_stage": "Staff training"},
    {"stage_status": "Not started", "evidence_strength": "Weak", "journey_stage": "Consulting report"},
]

STAGES_STRONG = [
    {"stage_status": "Completed", "evidence_strength": "Very strong", "journey_stage": "Readiness diagnosis"},
    {"stage_status": "Completed", "evidence_strength": "Very strong", "journey_stage": "Document intelligence"},
    {"stage_status": "Completed", "evidence_strength": "Very strong", "journey_stage": "Staff training"},
    {"stage_status": "Completed", "evidence_strength": "Very strong", "journey_stage": "Consulting report"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Governance review"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "ROI and impact review"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Delivery tracking"},
]

STAGES_BLOCKED = [
    {"stage_status": "Not started", "evidence_strength": "Weak", "journey_stage": "Delivery tracking"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Readiness diagnosis"},
]

STAGES_NEEDS_REVIEW = [
    {"stage_status": "Needs review", "evidence_strength": "Weak", "journey_stage": "Governance review"},
    {"stage_status": "Needs review", "evidence_strength": "Moderate", "journey_stage": "Delivery tracking"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Readiness diagnosis"},
]

STAGES_IN_PROGRESS_ONLY = [
    {"stage_status": "In progress", "evidence_strength": "Moderate", "journey_stage": "Delivery tracking"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Readiness diagnosis"},
]

STAGES_ALL_COMPLETED = [
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Readiness diagnosis"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "journey_stage": "Delivery tracking"},
]

STAGES_FOR_WEAKEST = [
    {"stage_status": "Completed", "evidence_strength": "Very strong", "journey_stage": "Readiness diagnosis"},
    {"stage_status": "Not started", "evidence_strength": "Weak", "journey_stage": "Delivery tracking"},
    {"stage_status": "In progress", "evidence_strength": "Strong", "journey_stage": "Staff training"},
]

EXPECTED_SUMMARY_KEYS = {
    "client_id",
    "organisation_name",
    "sector",
    "staff_count",
    "capstone_stage",
    "primary_ai_goal",
    "consulting_priority",
    "total_stages",
    "completed_stage_count",
    "in_progress_stage_count",
    "needs_review_stage_count",
    "not_started_stage_count",
    "stage_completion_rate",
    "average_evidence_score",
    "journey_health",
    "weakest_stage",
    "next_journey_step",
    "overall_capstone_status",
    "recommended_next_step",
}

EXPECTED_HEALTH_SUMMARY_KEYS = {
    "total_clients",
    "strong_journey_count",
    "healthy_journey_count",
    "developing_journey_count",
    "needs_review_count",
    "blocked_journey_count",
}


class TestCalculateStageCompletionRate:
    def test_completion_rate_calculation_works(self):
        # 2 of 4 completed = 50.0
        result = calculate_stage_completion_rate(STAGES_MIXED)
        assert result == 50.0

    def test_empty_completion_rate_returns_zero(self):
        assert calculate_stage_completion_rate([]) == 0.0


class TestCalculateAverageEvidenceScore:
    def test_average_evidence_score_works(self):
        # Very strong(4), Weak(1), Strong(3) = 8/3 = 2.67
        result = calculate_average_evidence_score(STAGES_FOR_WEAKEST)
        assert result == round((4 + 1 + 3) / 3, 2)

    def test_empty_evidence_score_returns_zero(self):
        assert calculate_average_evidence_score([]) == 0.0


class TestClassifyJourneyHealth:
    def test_returns_strong_journey(self):
        # 7/7 completed = 100%, avg evidence = (4+4+4+4+3+3+3)/7 ≈ 3.57
        result = classify_journey_health(STAGES_STRONG)
        assert result == "Strong journey"

    def test_returns_blocked_journey(self):
        result = classify_journey_health(STAGES_BLOCKED)
        assert result == "Blocked journey"

    def test_returns_needs_review(self):
        result = classify_journey_health(STAGES_NEEDS_REVIEW)
        assert result == "Needs review"


class TestIdentifyNextJourneyStep:
    def test_detects_not_started(self):
        result = identify_next_journey_step(STAGES_BLOCKED)
        assert "missing journey stage" in result.lower()

    def test_detects_needs_review(self):
        result = identify_next_journey_step(STAGES_NEEDS_REVIEW)
        assert "weakest journey stage" in result.lower()

    def test_detects_in_progress(self):
        result = identify_next_journey_step(STAGES_IN_PROGRESS_ONLY)
        assert "in-progress" in result.lower()


class TestIdentifyWeakestStage:
    def test_weakest_stage_returns_expected_stage(self):
        # Not started + Weak = 0+1=1 → Delivery tracking is weakest
        result = identify_weakest_stage(STAGES_FOR_WEAKEST)
        assert result == "Delivery tracking"


class TestSortStagesByJourneyOrder:
    def test_stages_follow_defined_journey_order(self):
        shuffled = [
            {"journey_stage": "Delivery tracking"},
            {"journey_stage": "Staff training"},
            {"journey_stage": "Readiness diagnosis"},
            {"journey_stage": "Impact measurement"},
        ]
        result = sort_stages_by_journey_order(shuffled)
        assert [stage["journey_stage"] for stage in result] == [
            "Readiness diagnosis",
            "Staff training",
            "Impact measurement",
            "Delivery tracking",
        ]

    def test_unknown_stages_are_kept_at_the_end(self):
        stages = [
            {"journey_stage": "Custom review"},
            {"journey_stage": "Readiness diagnosis"},
        ]
        result = sort_stages_by_journey_order(stages)
        assert result[-1]["journey_stage"] == "Custom review"


class TestBuildClientJourneySummary:
    def test_client_journey_summary_has_expected_keys(self):
        client = CLIENTS[0]
        client_stages = [s for s in STAGES if s["client_id"] == client["client_id"]]
        indicator = next(
            (i for i in INDICATORS if i["client_id"] == client["client_id"]), None
        )
        result = build_client_journey_summary(client, client_stages, indicator)
        assert EXPECTED_SUMMARY_KEYS.issubset(result.keys())


class TestBuildAllClientJourneySummaries:
    def test_all_client_summaries_match_client_count(self):
        result = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        assert len(result) == len(CLIENTS)


class TestSummariseJourneyHealth:
    def test_journey_health_summary_returns_expected_keys(self):
        summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        result = summarise_journey_health(summaries)
        assert EXPECTED_HEALTH_SUMMARY_KEYS.issubset(result.keys())


class TestPrioritiseClientsForReview:
    def test_prioritisation_puts_weakest_demo_client_first(self):
        summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        result = prioritise_clients_for_review(summaries)
        assert result[0]["client_id"] == "CAP003"
        assert result[-1]["client_id"] == "CAP001"


class TestGenerateClientJourneyRecommendation:
    def test_recommendation_generation_works(self):
        blocked_summary = {"journey_health": "Blocked journey"}
        result = generate_client_journey_recommendation(blocked_summary)
        assert "missing journey stages" in result.lower()

        strong_summary = {"journey_health": "Strong journey"}
        result = generate_client_journey_recommendation(strong_summary)
        assert "strong capstone example" in result.lower()


class TestAddJourneyRecommendations:
    def test_recommendations_are_added_without_mutating_originals(self):
        summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        original_keys = set(summaries[0].keys())
        result = add_journey_recommendations(summaries)
        assert "journey_recommendation" in result[0]
        assert "journey_recommendation" not in summaries[0]
        assert set(summaries[0].keys()) == original_keys


class TestSyntheticDataProcessing:
    def test_all_synthetic_capstone_data_processes_without_errors(self):
        summaries = build_all_client_journey_summaries(CLIENTS, STAGES, INDICATORS)
        summaries_with_rec = add_journey_recommendations(summaries)
        health = summarise_journey_health(summaries)
        prioritised = prioritise_clients_for_review(summaries_with_rec)
        assert len(summaries_with_rec) == 3
        assert health["total_clients"] == 3
        assert len(prioritised) == 3
