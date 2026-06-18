"""
Tests for scoring functions in src/scoring.py.

Run from the project root (brightpath-ai-readiness-tool/):  pytest
"""

from src.scoring import (
    calculate_readiness_score,
    get_readiness_category,
    calculate_workflow_suitability_score,
    get_workflow_suitability_category,
    calculate_risk_score,
    get_risk_level,
    get_pilot_recommendation,
)


# ── calculate_readiness_score ─────────────────────────────────────────────────

def test_readiness_score_sums_values():
    assert calculate_readiness_score({"a": 5, "b": 3, "c": 7}) == 15


def test_readiness_score_all_zero():
    assert calculate_readiness_score({k: 0 for k in range(10)}) == 0


def test_readiness_score_max():
    assert calculate_readiness_score({k: 10 for k in range(10)}) == 100


def test_readiness_score_brightpath_example():
    # BrightPath synthetic profile totals 35
    assert calculate_readiness_score({k: 0 for k in range(9)} | {"last": 35}) == 35


# ── get_readiness_category — band boundaries ──────────────────────────────────

def test_readiness_category_not_ready_at_0():
    assert get_readiness_category(0) == "Not ready"


def test_readiness_category_not_ready_at_25():
    assert get_readiness_category(25) == "Not ready"


def test_readiness_category_early_awareness_at_26():
    assert get_readiness_category(26) == "Early awareness"


def test_readiness_category_early_awareness_at_50():
    assert get_readiness_category(50) == "Early awareness"


def test_readiness_category_pilot_ready_at_51():
    assert get_readiness_category(51) == "Pilot ready with safeguards"


def test_readiness_category_pilot_ready_at_70():
    assert get_readiness_category(70) == "Pilot ready with safeguards"


def test_readiness_category_implementation_ready_at_71():
    assert get_readiness_category(71) == "Implementation ready"


def test_readiness_category_implementation_ready_at_85():
    assert get_readiness_category(85) == "Implementation ready"


def test_readiness_category_scaling_ready_at_86():
    assert get_readiness_category(86) == "Scaling ready"


def test_readiness_category_scaling_ready_at_100():
    assert get_readiness_category(100) == "Scaling ready"


# ── calculate_workflow_suitability_score ──────────────────────────────────────

def test_workflow_score_sums_values():
    assert calculate_workflow_suitability_score({"a": 3, "b": 4, "c": 5}) == 12


def test_workflow_score_all_zero():
    assert calculate_workflow_suitability_score({k: 0 for k in range(10)}) == 0


def test_workflow_score_max():
    assert calculate_workflow_suitability_score({k: 5 for k in range(10)}) == 50


# ── get_workflow_suitability_category — band boundaries ───────────────────────

def test_workflow_category_not_suitable_at_0():
    assert get_workflow_suitability_category(0) == "Not suitable"


def test_workflow_category_not_suitable_at_15():
    assert get_workflow_suitability_category(15) == "Not suitable"


def test_workflow_category_needs_governance_at_16():
    assert get_workflow_suitability_category(16) == "Needs governance first"


def test_workflow_category_needs_governance_at_25():
    assert get_workflow_suitability_category(25) == "Needs governance first"


def test_workflow_category_needs_redesign_at_26():
    assert get_workflow_suitability_category(26) == "Needs process redesign first"


def test_workflow_category_needs_redesign_at_35():
    assert get_workflow_suitability_category(35) == "Needs process redesign first"


def test_workflow_category_good_pilot_at_36():
    assert get_workflow_suitability_category(36) == "Good pilot candidate"


def test_workflow_category_good_pilot_at_42():
    assert get_workflow_suitability_category(42) == "Good pilot candidate"


def test_workflow_category_quick_win_at_43():
    assert get_workflow_suitability_category(43) == "Quick win"


def test_workflow_category_quick_win_at_50():
    assert get_workflow_suitability_category(50) == "Quick win"


# ── calculate_risk_score ──────────────────────────────────────────────────────

def test_risk_score_is_product():
    assert calculate_risk_score(3, 4) == 12


def test_risk_score_minimum():
    assert calculate_risk_score(1, 1) == 1


def test_risk_score_maximum():
    assert calculate_risk_score(5, 5) == 25


def test_risk_score_safeguarding_brightpath():
    # BrightPath safeguarding profile: likelihood 2, impact 5 → High (10)
    assert calculate_risk_score(2, 5) == 10


# ── get_risk_level — band boundaries ─────────────────────────────────────────

def test_risk_level_low_at_1():
    assert get_risk_level(1) == "Low"


def test_risk_level_low_at_4():
    assert get_risk_level(4) == "Low"


def test_risk_level_moderate_at_5():
    assert get_risk_level(5) == "Moderate"


def test_risk_level_moderate_at_9():
    assert get_risk_level(9) == "Moderate"


def test_risk_level_high_at_10():
    assert get_risk_level(10) == "High"


def test_risk_level_high_at_15():
    assert get_risk_level(15) == "High"


def test_risk_level_critical_at_16():
    assert get_risk_level(16) == "Critical"


def test_risk_level_critical_at_25():
    assert get_risk_level(25) == "Critical"


# ── get_pilot_recommendation ──────────────────────────────────────────────────

def test_pilot_critical_risk_overrides_high_scores():
    # Critical risk returns Not ready regardless of readiness or workflow score
    assert get_pilot_recommendation(95, 50, "Critical", True, False) == "Not ready for AI pilot"


def test_pilot_high_risk_overrides_high_scores():
    # High risk returns Governance-first regardless of readiness or workflow score
    assert get_pilot_recommendation(95, 50, "High", False, True) == "Governance-first before pilot"


def test_pilot_low_readiness_at_50():
    # Readiness 50 is below the 51 threshold
    assert get_pilot_recommendation(50, 45, "Low", False, False) == "Not ready for AI pilot"


def test_pilot_low_readiness_at_40():
    assert get_pilot_recommendation(40, 45, "Low", False, False) == "Not ready for AI pilot"


def test_pilot_low_workflow_score():
    # Workflow 25 is below the 26 threshold
    assert get_pilot_recommendation(60, 25, "Low", False, False) == "Process redesign before AI"


def test_pilot_low_risk_candidate():
    # readiness 62, workflow 40, Moderate → Low-risk pilot candidate
    assert get_pilot_recommendation(62, 40, "Moderate", False, False) == "Low-risk pilot candidate"


def test_pilot_strong_candidate():
    # readiness 80, workflow 45, Moderate → Strong pilot candidate
    assert get_pilot_recommendation(80, 45, "Moderate", False, False) == "Strong pilot candidate"


def test_pilot_ready_for_controlled_implementation():
    # readiness 90, workflow 45, Low → Ready for controlled implementation
    assert get_pilot_recommendation(90, 45, "Low", False, False) == "Ready for controlled implementation"
