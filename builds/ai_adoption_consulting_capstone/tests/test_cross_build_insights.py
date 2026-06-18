"""Tests for logic/cross_build_insights.py — Build 9 Phase 3."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_cross_build_stages,
)
from logic.cross_build_insights import (
    BUILD_ORDER,
    add_cross_build_recommendations,
    build_all_cross_build_summaries,
    build_client_build_matrix,
    build_cross_build_summary,
    calculate_build_average_evidence_score,
    calculate_build_completion_rate,
    classify_build_evidence_health,
    generate_cross_build_recommendation,
    get_stages_for_build,
    identify_build_gap,
    identify_strongest_build_area,
    identify_weakest_build_area,
    prioritise_build_areas_for_improvement,
    summarise_cross_build_insights,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()

# Controlled fixtures for deterministic tests

STAGES_VERY_STRONG = [
    {"stage_status": "Completed", "evidence_strength": "Very strong", "build_number": "Build 1"},
    {"stage_status": "Completed", "evidence_strength": "Very strong", "build_number": "Build 1"},
]

STAGES_WEAK = [
    {"stage_status": "In progress", "evidence_strength": "Weak", "build_number": "Build 6"},
]

STAGES_NOT_STARTED = [
    {"stage_status": "Not started", "evidence_strength": "Weak", "build_number": "Build 7"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "build_number": "Build 7"},
]

STAGES_NEEDS_REVIEW = [
    {"stage_status": "Needs review", "evidence_strength": "Moderate", "build_number": "Build 6"},
    {"stage_status": "Completed", "evidence_strength": "Strong", "build_number": "Build 6"},
]

EXPECTED_BUILD_SUMMARY_KEYS = {
    "build_number",
    "build_domain",
    "client_stage_count",
    "completed_count",
    "in_progress_count",
    "needs_review_count",
    "not_started_count",
    "completion_rate",
    "average_evidence_score",
    "evidence_health",
    "build_gap",
}

EXPECTED_INSIGHT_SUMMARY_KEYS = {
    "total_build_areas",
    "very_strong_evidence_count",
    "strong_evidence_count",
    "developing_evidence_count",
    "weak_evidence_count",
    "no_evidence_count",
    "strongest_build_area",
    "weakest_build_area",
}


class TestGetStagesForBuild:
    def test_build_stage_filtering_works(self):
        build_1_stages = get_stages_for_build(STAGES, "Build 1")
        # 3 clients, 1 Build 1 stage each = 3 stages
        assert len(build_1_stages) == 3
        assert all(s["build_number"] == "Build 1" for s in build_1_stages)

    def test_filtering_returns_empty_for_unknown_build(self):
        result = get_stages_for_build(STAGES, "Build 99")
        assert result == []


class TestCalculateBuildCompletionRate:
    def test_build_completion_rate_works(self):
        # STAGES_NOT_STARTED: 1 of 2 completed = 50.0
        result = calculate_build_completion_rate(STAGES_NOT_STARTED)
        assert result == 50.0

    def test_empty_completion_rate_returns_zero(self):
        assert calculate_build_completion_rate([]) == 0.0


class TestCalculateBuildAverageEvidenceScore:
    def test_average_evidence_score_works(self):
        # Very strong(4) + Very strong(4) = 8 / 2 = 4.0
        result = calculate_build_average_evidence_score(STAGES_VERY_STRONG)
        assert result == 4.0

    def test_empty_evidence_score_returns_zero(self):
        assert calculate_build_average_evidence_score([]) == 0.0


class TestClassifyBuildEvidenceHealth:
    def test_evidence_health_returns_very_strong(self):
        # STAGES_VERY_STRONG: 100% completion, avg 4.0 → Very strong
        result = classify_build_evidence_health(STAGES_VERY_STRONG)
        assert result == "Very strong evidence"

    def test_evidence_health_returns_weak(self):
        # STAGES_WEAK: 0% completion (In progress), avg 1.0 → Weak
        result = classify_build_evidence_health(STAGES_WEAK)
        assert result == "Weak evidence"

    def test_evidence_health_returns_no_evidence_for_empty(self):
        result = classify_build_evidence_health([])
        assert result == "No evidence"


class TestIdentifyBuildGap:
    def test_build_gap_detects_not_started(self):
        result = identify_build_gap(STAGES_NOT_STARTED)
        assert "not started" in result.lower()

    def test_build_gap_detects_needs_review(self):
        result = identify_build_gap(STAGES_NEEDS_REVIEW)
        assert "need review" in result.lower()

    def test_build_gap_returns_no_evidence_for_empty(self):
        result = identify_build_gap([])
        assert "no evidence" in result.lower()


class TestBuildCrossBuildSummary:
    def test_build_summary_has_expected_keys(self):
        build_1_stages = get_stages_for_build(STAGES, "Build 1")
        result = build_cross_build_summary(build_1_stages, "Build 1")
        assert EXPECTED_BUILD_SUMMARY_KEYS.issubset(result.keys())


class TestBuildAllCrossBuildSummaries:
    def test_all_cross_build_summaries_match_build_order_length(self):
        result = build_all_cross_build_summaries(STAGES)
        assert len(result) == len(BUILD_ORDER)

    def test_summaries_follow_build_order(self):
        result = build_all_cross_build_summaries(STAGES)
        for i, summary in enumerate(result):
            assert summary["build_number"] == BUILD_ORDER[i]


class TestIdentifyStrongestAndWeakestBuildArea:
    def test_strongest_build_area_returns_expected_value(self):
        summaries = build_all_cross_build_summaries(STAGES)
        result = identify_strongest_build_area(summaries)
        assert result == "Build 1"

    def test_weakest_build_area_returns_expected_value(self):
        summaries = build_all_cross_build_summaries(STAGES)
        result = identify_weakest_build_area(summaries)
        assert result == "Build 7"

    def test_returns_fallback_for_empty_list(self):
        assert identify_strongest_build_area([]) == "No build summaries available"
        assert identify_weakest_build_area([]) == "No build summaries available"


class TestSummariseCrossBuildInsights:
    def test_cross_build_insight_summary_has_expected_keys(self):
        summaries = build_all_cross_build_summaries(STAGES)
        result = summarise_cross_build_insights(summaries)
        assert EXPECTED_INSIGHT_SUMMARY_KEYS.issubset(result.keys())

    def test_total_build_areas_matches_build_order(self):
        summaries = build_all_cross_build_summaries(STAGES)
        result = summarise_cross_build_insights(summaries)
        assert result["total_build_areas"] == len(BUILD_ORDER)


class TestPrioritiseBuildAreasForImprovement:
    def test_prioritisation_puts_developing_areas_before_strong_areas(self):
        summaries = build_all_cross_build_summaries(STAGES)
        result = prioritise_build_areas_for_improvement(summaries)
        assert result[0]["evidence_health"] == "Developing evidence"
        assert result[-1]["evidence_health"] == "Strong evidence"


class TestGenerateCrossBuildRecommendation:
    def test_recommendation_generation_works(self):
        weak_summary = {"evidence_health": "Weak evidence"}
        result = generate_cross_build_recommendation(weak_summary)
        assert "strengthen" in result.lower()

        very_strong_summary = {"evidence_health": "Very strong evidence"}
        result = generate_cross_build_recommendation(very_strong_summary)
        assert "leading proof point" in result.lower()


class TestAddCrossBuildRecommendations:
    def test_recommendations_are_added_without_mutating_originals(self):
        summaries = build_all_cross_build_summaries(STAGES)
        original_keys = set(summaries[0].keys())
        result = add_cross_build_recommendations(summaries)
        assert "cross_build_recommendation" in result[0]
        assert "cross_build_recommendation" not in summaries[0]
        assert set(summaries[0].keys()) == original_keys


class TestBuildClientBuildMatrix:
    def test_client_build_matrix_returns_one_row_per_client(self):
        result = build_client_build_matrix(CLIENTS, STAGES)
        assert len(result) == len(CLIENTS)

    def test_matrix_contains_all_build_columns(self):
        result = build_client_build_matrix(CLIENTS, STAGES)
        for row in result:
            for build in BUILD_ORDER:
                assert build in row

    def test_matrix_stage_statuses_are_valid_or_not_available(self):
        valid_statuses = {"Completed", "In progress", "Needs review", "Not started", "Not available"}
        result = build_client_build_matrix(CLIENTS, STAGES)
        for row in result:
            for build in BUILD_ORDER:
                assert row[build] in valid_statuses


class TestSyntheticDataProcessing:
    def test_all_synthetic_capstone_data_processes_without_errors(self):
        summaries = build_all_cross_build_summaries(STAGES)
        summaries_with_rec = add_cross_build_recommendations(summaries)
        insight_summary = summarise_cross_build_insights(summaries)
        prioritised = prioritise_build_areas_for_improvement(summaries_with_rec)
        matrix = build_client_build_matrix(CLIENTS, STAGES)
        assert len(summaries_with_rec) == len(BUILD_ORDER)
        assert insight_summary["total_build_areas"] == len(BUILD_ORDER)
        assert len(prioritised) == len(BUILD_ORDER)
        assert len(matrix) == len(CLIENTS)
