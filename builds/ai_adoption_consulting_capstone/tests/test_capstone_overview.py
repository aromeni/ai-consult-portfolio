"""Tests for logic/capstone_overview.py — Build 9 Phase 1."""

from data.synthetic_capstone_data import (
    get_synthetic_capstone_clients,
    get_synthetic_capstone_indicators,
    get_synthetic_cross_build_stages,
)
from logic.capstone_overview import (
    calculate_evidence_counts_by_strength,
    calculate_stage_counts_by_status,
    get_indicator_for_client,
    get_stages_for_client,
    summarise_phase_1_capstone,
    validate_all_capstone_data,
    validate_capstone_client,
    validate_capstone_indicator,
    validate_cross_build_stage,
)

CLIENTS = get_synthetic_capstone_clients()
STAGES = get_synthetic_cross_build_stages()
INDICATORS = get_synthetic_capstone_indicators()

VALID_CLIENT = {
    "client_id": "TST001",
    "organisation_name": "Test Organisation",
    "sector": "Test sector",
    "staff_count": 5,
    "capstone_stage": "Pilot",
    "primary_ai_goal": "Test AI goal.",
    "consulting_priority": "Test consulting priority.",
}

VALID_STAGE = {
    "stage_id": "TSTG001",
    "client_id": "TST001",
    "organisation_name": "Test Organisation",
    "build_number": "Build 1",
    "build_name": "AI Readiness / Workflow Audit Tool",
    "journey_stage": "Readiness diagnosis",
    "stage_status": "Completed",
    "stage_summary": "Test stage summary.",
    "evidence_strength": "Strong",
    "consulting_value": "Test consulting value.",
}

VALID_INDICATOR = {
    "client_id": "TST001",
    "organisation_name": "Test Organisation",
    "readiness_position": "Moderate readiness",
    "governance_position": "Controls in place",
    "training_position": "Staff trained",
    "roi_position": "Value emerging",
    "delivery_position": "Actions active",
    "commercial_position": "Good candidate for follow-up",
    "overall_capstone_status": "Portfolio-ready demo",
    "recommended_next_step": "Prepare a progress review.",
}

EXPECTED_SUMMARY_KEYS = {
    "total_clients",
    "total_cross_build_stages",
    "total_indicators",
    "completed_stage_count",
    "in_progress_stage_count",
    "needs_review_stage_count",
    "strong_or_very_strong_evidence_count",
    "portfolio_ready_or_strong_asset_count",
}

EXPECTED_VALIDATION_KEYS = {
    "total_clients",
    "total_stages",
    "total_indicators",
    "valid_clients",
    "valid_stages",
    "valid_indicators",
    "warnings",
}


class TestValidateCapstoneClient:
    def test_valid_client_returns_no_warnings(self):
        assert validate_capstone_client(VALID_CLIENT) == []

    def test_missing_required_field_is_caught(self):
        invalid = {k: v for k, v in VALID_CLIENT.items() if k != "organisation_name"}
        warnings = validate_capstone_client(invalid)
        assert any("organisation_name" in w for w in warnings)


class TestValidateCrossBuildStage:
    def test_valid_stage_returns_no_warnings(self):
        assert validate_cross_build_stage(VALID_STAGE) == []

    def test_invalid_stage_status_is_caught(self):
        invalid = {**VALID_STAGE, "stage_status": "Unknown status"}
        warnings = validate_cross_build_stage(invalid)
        assert any("stage_status" in w for w in warnings)

    def test_invalid_evidence_strength_is_caught(self):
        invalid = {**VALID_STAGE, "evidence_strength": "Excellent"}
        warnings = validate_cross_build_stage(invalid)
        assert any("evidence_strength" in w for w in warnings)


class TestValidateCapstoneIndicator:
    def test_valid_indicator_returns_no_warnings(self):
        assert validate_capstone_indicator(VALID_INDICATOR) == []

    def test_invalid_overall_capstone_status_is_caught(self):
        invalid = {**VALID_INDICATOR, "overall_capstone_status": "Unknown status"}
        warnings = validate_capstone_indicator(invalid)
        assert any("overall_capstone_status" in w for w in warnings)


class TestValidateAllCapstoneData:
    def test_all_data_validation_returns_expected_keys(self):
        result = validate_all_capstone_data(CLIENTS, STAGES, INDICATORS)
        assert EXPECTED_VALIDATION_KEYS.issubset(result.keys())


class TestGetStagesForClient:
    def test_client_stage_filtering_works(self):
        result = get_stages_for_client(STAGES, "CAP001")
        assert len(result) > 0
        assert all(s["client_id"] == "CAP001" for s in result)


class TestGetIndicatorForClient:
    def test_client_indicator_lookup_works(self):
        result = get_indicator_for_client(INDICATORS, "CAP001")
        assert result is not None
        assert result["client_id"] == "CAP001"

    def test_missing_client_returns_none(self):
        result = get_indicator_for_client(INDICATORS, "UNKNOWN")
        assert result is None


class TestCalculateStageCountsByStatus:
    def test_stage_status_counts_work(self):
        result = calculate_stage_counts_by_status(STAGES)
        assert "Completed" in result
        assert "In progress" in result
        assert "Not started" in result
        assert "Needs review" in result
        assert sum(result.values()) == len(STAGES)


class TestCalculateEvidenceCountsByStrength:
    def test_evidence_strength_counts_work(self):
        result = calculate_evidence_counts_by_strength(STAGES)
        assert "Strong" in result
        assert "Very strong" in result
        assert "Moderate" in result
        assert "Weak" in result
        assert sum(result.values()) == len(STAGES)


class TestSummarisePhase1Capstone:
    def test_phase_1_summary_returns_expected_keys(self):
        result = summarise_phase_1_capstone(CLIENTS, STAGES, INDICATORS)
        assert EXPECTED_SUMMARY_KEYS.issubset(result.keys())

    def test_all_synthetic_capstone_data_processes_without_errors(self):
        result = summarise_phase_1_capstone(CLIENTS, STAGES, INDICATORS)
        assert result["total_clients"] == 3
        assert result["total_cross_build_stages"] == 21
        assert result["total_indicators"] == 3
