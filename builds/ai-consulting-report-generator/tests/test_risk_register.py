"""Tests for src/risk_register.py — Build 5, Phase 3.

BrightPath synthetic data risk findings:
  1. Learner Data in Unapproved AI Tools — Likelihood: High (4), Impact: High (4)  → score 16 → High
  2. No Approved AI Tools List           — Likelihood: High (4), Impact: Medium (3) → score 12 → High
  3. AI Hallucination in Training Mat.   — Likelihood: Medium (3), Impact: High (4) → score 12 → High
  4. Safeguarding Decisions Delegated    — Likelihood: Low (2), Impact: Critical (5) → score 10 → High
  5. Inconsistent AI Use Across Depts   — Likelihood: High (4), Impact: Low (2)    → score  8 → Medium
"""

import pytest
from src import risk_register as rr
from src.sample_data import get_brightpath_audit_data


# ── normalise_risk_score ───────────────────────────────────────────────────────

class TestNormaliseRiskScore:
    def test_very_low_text(self):
        assert rr.normalise_risk_score("Very low") == 1

    def test_low_text(self):
        assert rr.normalise_risk_score("Low") == 2

    def test_medium_text(self):
        assert rr.normalise_risk_score("Medium") == 3

    def test_high_text(self):
        assert rr.normalise_risk_score("High") == 4

    def test_very_high_text(self):
        assert rr.normalise_risk_score("Very high") == 5

    def test_critical_text_maps_to_five(self):
        assert rr.normalise_risk_score("Critical") == 5

    def test_numeric_int(self):
        assert rr.normalise_risk_score(3) == 3

    def test_numeric_float(self):
        assert rr.normalise_risk_score(4.0) == 4

    def test_numeric_clamped_above_five(self):
        assert rr.normalise_risk_score(10) == 5

    def test_numeric_clamped_below_one(self):
        assert rr.normalise_risk_score(0) == 1

    def test_none_defaults_to_medium(self):
        assert rr.normalise_risk_score(None) == 3

    def test_invalid_string_defaults_to_medium(self):
        assert rr.normalise_risk_score("unknown") == 3

    def test_empty_string_defaults_to_medium(self):
        assert rr.normalise_risk_score("") == 3

    def test_case_insensitive(self):
        assert rr.normalise_risk_score("HIGH") == 4


# ── calculate_risk_score ───────────────────────────────────────────────────────

class TestCalculateRiskScore:
    def test_high_high_returns_sixteen(self):
        assert rr.calculate_risk_score("High", "High") == 16

    def test_medium_medium_returns_nine(self):
        assert rr.calculate_risk_score("Medium", "Medium") == 9

    def test_low_low_returns_four(self):
        assert rr.calculate_risk_score("Low", "Low") == 4

    def test_very_high_very_high_returns_twenty_five(self):
        assert rr.calculate_risk_score("Very high", "Very high") == 25

    def test_numeric_inputs(self):
        assert rr.calculate_risk_score(3, 4) == 12

    def test_mixed_string_and_numeric(self):
        assert rr.calculate_risk_score("High", 3) == 12

    def test_none_inputs_default_safely(self):
        assert rr.calculate_risk_score(None, None) == 9  # 3 * 3 (Medium * Medium)


# ── classify_risk_level ────────────────────────────────────────────────────────

class TestClassifyRiskLevel:
    def test_score_1_is_low(self):
        assert rr.classify_risk_level(1) == "Low"

    def test_score_4_is_low(self):
        assert rr.classify_risk_level(4) == "Low"

    def test_score_5_is_medium(self):
        assert rr.classify_risk_level(5) == "Medium"

    def test_score_9_is_medium(self):
        assert rr.classify_risk_level(9) == "Medium"

    def test_score_10_is_high(self):
        assert rr.classify_risk_level(10) == "High"

    def test_score_16_is_high(self):
        assert rr.classify_risk_level(16) == "High"

    def test_score_17_is_critical(self):
        assert rr.classify_risk_level(17) == "Critical"

    def test_score_25_is_critical(self):
        assert rr.classify_risk_level(25) == "Critical"


# ── get_risk_level_description ─────────────────────────────────────────────────

class TestGetRiskLevelDescription:
    def test_critical_returns_non_empty_string(self):
        desc = rr.get_risk_level_description("Critical")
        assert isinstance(desc, str)
        assert len(desc) > 10

    def test_high_returns_non_empty_string(self):
        desc = rr.get_risk_level_description("High")
        assert isinstance(desc, str)
        assert len(desc) > 10

    def test_medium_returns_string(self):
        assert isinstance(rr.get_risk_level_description("Medium"), str)

    def test_low_returns_string(self):
        assert isinstance(rr.get_risk_level_description("Low"), str)

    def test_unknown_returns_fallback_string(self):
        desc = rr.get_risk_level_description("Unknown")
        assert isinstance(desc, str)
        assert len(desc) > 0


# ── get_risk_level_colour ──────────────────────────────────────────────────────

class TestGetRiskLevelColour:
    def test_critical_returns_hex(self):
        assert rr.get_risk_level_colour("Critical").startswith("#")

    def test_high_returns_hex(self):
        assert rr.get_risk_level_colour("High").startswith("#")

    def test_medium_returns_hex(self):
        assert rr.get_risk_level_colour("Medium").startswith("#")

    def test_low_returns_hex(self):
        assert rr.get_risk_level_colour("Low").startswith("#")

    def test_unknown_returns_fallback_hex(self):
        assert rr.get_risk_level_colour("Unknown").startswith("#")


# ── generate_risk_id ───────────────────────────────────────────────────────────

class TestGenerateRiskId:
    def test_index_zero_is_risk_001(self):
        assert rr.generate_risk_id(0) == "RISK-001"

    def test_index_one_is_risk_002(self):
        assert rr.generate_risk_id(1) == "RISK-002"

    def test_index_nine_is_risk_010(self):
        assert rr.generate_risk_id(9) == "RISK-010"

    def test_format_starts_with_risk_prefix(self):
        assert rr.generate_risk_id(0).startswith("RISK-")


# ── generate_risk_control_recommendation ──────────────────────────────────────

class TestGenerateRiskControlRecommendation:
    def test_data_protection_returns_string(self):
        result = rr.generate_risk_control_recommendation({"risk_category": "Data Protection"})
        assert isinstance(result, str)
        assert len(result) > 20

    def test_safeguarding_mentions_safeguarding(self):
        result = rr.generate_risk_control_recommendation({"risk_category": "Safeguarding"})
        assert "safeguarding" in result.lower()

    def test_governance_returns_string(self):
        result = rr.generate_risk_control_recommendation({"risk_category": "Governance"})
        assert isinstance(result, str)

    def test_unknown_category_returns_default(self):
        result = rr.generate_risk_control_recommendation({"risk_category": "Unknown Category"})
        assert isinstance(result, str)
        assert len(result) > 20

    def test_missing_category_returns_default(self):
        result = rr.generate_risk_control_recommendation({})
        assert isinstance(result, str)
        assert len(result) > 20


# ── generate_risk_owner_suggestion ────────────────────────────────────────────

class TestGenerateRiskOwnerSuggestion:
    def test_data_protection_returns_string(self):
        result = rr.generate_risk_owner_suggestion({"risk_category": "Data Protection"})
        assert isinstance(result, str)
        assert len(result) > 5

    def test_safeguarding_mentions_safeguarding(self):
        result = rr.generate_risk_owner_suggestion({"risk_category": "Safeguarding"})
        assert "safeguarding" in result.lower()

    def test_unknown_category_returns_default(self):
        result = rr.generate_risk_owner_suggestion({"risk_category": "Unknown"})
        assert isinstance(result, str)

    def test_missing_category_returns_default(self):
        result = rr.generate_risk_owner_suggestion({})
        assert isinstance(result, str)


# ── generate_risk_register ─────────────────────────────────────────────────────

class TestGenerateRiskRegister:
    def setup_method(self):
        self.audit_data = get_brightpath_audit_data()
        self.register = rr.generate_risk_register(self.audit_data)

    def test_returns_list(self):
        assert isinstance(self.register, list)

    def test_brightpath_has_five_risks(self):
        assert len(self.register) == 5

    def test_first_risk_id_is_risk_001(self):
        assert self.register[0]["risk_id"] == "RISK-001"

    def test_each_risk_has_risk_id(self):
        for risk in self.register:
            assert "risk_id" in risk
            assert risk["risk_id"].startswith("RISK-")

    def test_each_risk_has_risk_title(self):
        for risk in self.register:
            assert "risk_title" in risk
            assert isinstance(risk["risk_title"], str)

    def test_each_risk_has_risk_category(self):
        for risk in self.register:
            assert "risk_category" in risk

    def test_each_risk_has_likelihood_score(self):
        for risk in self.register:
            assert "likelihood_score" in risk
            assert 1 <= risk["likelihood_score"] <= 5

    def test_each_risk_has_impact_score(self):
        for risk in self.register:
            assert "impact_score" in risk
            assert 1 <= risk["impact_score"] <= 5

    def test_each_risk_has_risk_score(self):
        for risk in self.register:
            assert "risk_score" in risk
            assert 1 <= risk["risk_score"] <= 25

    def test_risk_score_equals_likelihood_times_impact(self):
        for risk in self.register:
            expected = risk["likelihood_score"] * risk["impact_score"]
            assert risk["risk_score"] == expected

    def test_each_risk_has_valid_risk_level(self):
        for risk in self.register:
            assert risk["risk_level"] in ("Low", "Medium", "High", "Critical")

    def test_each_risk_has_recommended_control(self):
        for risk in self.register:
            assert "recommended_control" in risk
            assert isinstance(risk["recommended_control"], str)
            assert len(risk["recommended_control"]) > 10

    def test_each_risk_has_owner(self):
        for risk in self.register:
            assert "owner" in risk
            assert isinstance(risk["owner"], str)

    def test_each_risk_has_priority_action(self):
        for risk in self.register:
            assert "priority_action" in risk
            assert isinstance(risk["priority_action"], str)

    def test_status_is_open(self):
        for risk in self.register:
            assert risk["status"] == "Open"

    def test_source_is_synthetic(self):
        for risk in self.register:
            assert "Synthetic" in risk["source"]

    def test_empty_risk_findings_returns_empty_list(self):
        result = rr.generate_risk_register({"risk_findings": []})
        assert result == []

    def test_missing_risk_findings_returns_empty_list(self):
        result = rr.generate_risk_register({})
        assert result == []

    def test_risk_with_missing_likelihood_defaults_safely(self):
        audit = {"risk_findings": [{"risk_title": "Test Risk", "risk_category": "Governance"}]}
        result = rr.generate_risk_register(audit)
        assert len(result) == 1
        assert result[0]["likelihood_score"] == 3
        assert result[0]["impact_score"] == 3

    def test_risk_with_missing_title_gets_placeholder(self):
        audit = {"risk_findings": [{"risk_category": "Governance"}]}
        result = rr.generate_risk_register(audit)
        assert isinstance(result[0]["risk_title"], str)

    # BrightPath-specific score checks
    def test_first_risk_high_high_gives_score_16(self):
        # Learner Data: High (4) * High (4) = 16
        assert self.register[0]["risk_score"] == 16

    def test_last_risk_high_low_gives_score_8(self):
        # Inconsistent AI Use: High (4) * Low (2) = 8
        assert self.register[4]["risk_score"] == 8

    def test_safeguarding_risk_has_low_critical_score_10(self):
        # Safeguarding: Low (2) * Critical→VeryHigh (5) = 10
        safeguarding = next(
            r for r in self.register if "Safeguarding" in r["risk_category"]
        )
        assert safeguarding["risk_score"] == 10


# ── summarise_risk_register ────────────────────────────────────────────────────

class TestSummariseRiskRegister:
    def setup_method(self):
        audit_data = get_brightpath_audit_data()
        self.register = rr.generate_risk_register(audit_data)
        self.summary = rr.summarise_risk_register(self.register)

    def test_has_total_risks_key(self):
        assert "total_risks" in self.summary

    def test_total_risks_is_five(self):
        assert self.summary["total_risks"] == 5

    def test_has_critical_risks_key(self):
        assert "critical_risks" in self.summary

    def test_has_high_risks_key(self):
        assert "high_risks" in self.summary

    def test_has_medium_risks_key(self):
        assert "medium_risks" in self.summary

    def test_has_low_risks_key(self):
        assert "low_risks" in self.summary

    def test_counts_sum_to_total(self):
        s = self.summary
        total = s["critical_risks"] + s["high_risks"] + s["medium_risks"] + s["low_risks"]
        assert total == s["total_risks"]

    def test_brightpath_has_four_high_risks(self):
        assert self.summary["high_risks"] == 4

    def test_brightpath_has_one_medium_risk(self):
        assert self.summary["medium_risks"] == 1

    def test_brightpath_has_zero_critical_risks(self):
        assert self.summary["critical_risks"] == 0

    def test_has_highest_risk(self):
        assert "highest_risk" in self.summary
        assert isinstance(self.summary["highest_risk"], dict)

    def test_highest_risk_has_score_16(self):
        assert self.summary["highest_risk"]["risk_score"] == 16

    def test_has_top_risk_categories(self):
        assert "top_risk_categories" in self.summary
        assert isinstance(self.summary["top_risk_categories"], list)

    def test_has_overall_risk_position(self):
        assert "overall_risk_position" in self.summary
        assert isinstance(self.summary["overall_risk_position"], str)
        assert len(self.summary["overall_risk_position"]) > 10

    def test_has_recommended_focus(self):
        assert "recommended_focus" in self.summary
        assert isinstance(self.summary["recommended_focus"], list)
        assert len(self.summary["recommended_focus"]) > 0

    def test_empty_register_returns_safe_summary(self):
        summary = rr.summarise_risk_register([])
        assert summary["total_risks"] == 0
        assert summary["highest_risk"] == {}
        assert summary["critical_risks"] == 0
        assert isinstance(summary["overall_risk_position"], str)
        assert isinstance(summary["recommended_focus"], list)


# ── prioritise_risks ───────────────────────────────────────────────────────────

class TestPrioritiseRisks:
    def setup_method(self):
        audit_data = get_brightpath_audit_data()
        self.register = rr.generate_risk_register(audit_data)

    def test_returns_list(self):
        assert isinstance(rr.prioritise_risks(self.register), list)

    def test_sorted_descending_by_risk_score(self):
        result = rr.prioritise_risks(self.register)
        scores = [r["risk_score"] for r in result]
        assert scores == sorted(scores, reverse=True)

    def test_first_risk_has_highest_score(self):
        result = rr.prioritise_risks(self.register)
        max_score = max(r["risk_score"] for r in self.register)
        assert result[0]["risk_score"] == max_score

    def test_same_length_as_input(self):
        result = rr.prioritise_risks(self.register)
        assert len(result) == len(self.register)

    def test_empty_input_returns_empty_list(self):
        assert rr.prioritise_risks([]) == []

    def test_does_not_mutate_original(self):
        original_first_id = self.register[0]["risk_id"]
        rr.prioritise_risks(self.register)
        assert self.register[0]["risk_id"] == original_first_id


# ── format_risk_register_as_markdown ──────────────────────────────────────────

class TestFormatRiskRegisterAsMarkdown:
    def setup_method(self):
        audit_data = get_brightpath_audit_data()
        self.register = rr.generate_risk_register(audit_data)
        self.summary = rr.summarise_risk_register(self.register)
        self.md = rr.format_risk_register_as_markdown(self.register, self.summary)

    def test_returns_string(self):
        assert isinstance(self.md, str)

    def test_contains_ai_risk_register_heading(self):
        assert "# AI Risk Register" in self.md

    def test_contains_risk_summary_heading(self):
        assert "## Risk Summary" in self.md

    def test_contains_overall_risk_position_heading(self):
        assert "## Overall Risk Position" in self.md

    def test_contains_recommended_focus_heading(self):
        assert "## Recommended Focus Areas" in self.md

    def test_contains_risk_register_table_heading(self):
        assert "## Risk Register Table" in self.md

    def test_contains_detailed_risk_notes_heading(self):
        assert "## Detailed Risk Notes" in self.md

    def test_contains_responsible_use_boundaries_heading(self):
        assert "## Responsible-Use Boundaries" in self.md

    def test_contains_responsible_use_text(self):
        assert "synthetic/demo audit data only" in self.md

    def test_contains_human_review_required(self):
        assert "Human review remains required" in self.md

    def test_contains_risk_ids(self):
        assert "RISK-001" in self.md

    def test_without_summary_still_returns_valid_markdown(self):
        md = rr.format_risk_register_as_markdown(self.register, None)
        assert "# AI Risk Register" in md
        assert "## Responsible-Use Boundaries" in md

    def test_empty_register_returns_valid_markdown(self):
        md = rr.format_risk_register_as_markdown([], None)
        assert "# AI Risk Register" in md
        assert "## Responsible-Use Boundaries" in md
