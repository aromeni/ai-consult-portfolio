"""Tests for src/scoring_summary.py — Phase 2."""

import pytest
from src import scoring_summary as ss

_SCORES = {
    "strategy_score": 32,
    "data_governance_score": 28,
    "staff_capability_score": 45,
    "workflow_opportunity_score": 68,
    "risk_management_score": 25,
    "leadership_alignment_score": 52,
    "overall_readiness_score": 42,
}

_SCORES_NO_OVERALL = {k: v for k, v in _SCORES.items() if k != "overall_readiness_score"}

_HIGH_SCORES = {
    "strategy_score": 85,
    "data_governance_score": 78,
    "staff_capability_score": 72,
    "workflow_opportunity_score": 91,
    "risk_management_score": 65,
    "leadership_alignment_score": 80,
    "overall_readiness_score": 82,
}


class TestCalculateAverageReadinessScore:
    def test_returns_float(self):
        assert isinstance(ss.calculate_average_readiness_score(_SCORES), float)

    def test_correct_average(self):
        result = ss.calculate_average_readiness_score(_SCORES)
        expected = round((32 + 28 + 45 + 68 + 25 + 52) / 6, 1)
        assert result == expected

    def test_excludes_overall_score_key(self):
        only_overall = {"overall_readiness_score": 80}
        assert ss.calculate_average_readiness_score(only_overall) == 0.0

    def test_empty_returns_zero(self):
        assert ss.calculate_average_readiness_score({}) == 0.0

    def test_single_valid_score(self):
        assert ss.calculate_average_readiness_score({"strategy_score": 60}) == 60.0

    def test_ignores_none_values(self):
        scores = dict(_SCORES)
        scores["strategy_score"] = None
        result = ss.calculate_average_readiness_score(scores)
        assert isinstance(result, float)

    def test_ignores_non_numeric_values(self):
        scores = dict(_SCORES)
        scores["strategy_score"] = "not a number"
        result = ss.calculate_average_readiness_score(scores)
        assert isinstance(result, float)


class TestClassifyReadinessLevel:
    def test_low_at_0(self):
        assert ss.classify_readiness_level(0) == "Low readiness"

    def test_low_at_39(self):
        assert ss.classify_readiness_level(39) == "Low readiness"

    def test_developing_at_40(self):
        assert ss.classify_readiness_level(40) == "Developing readiness"

    def test_developing_at_59(self):
        assert ss.classify_readiness_level(59) == "Developing readiness"

    def test_moderate_at_60(self):
        assert ss.classify_readiness_level(60) == "Moderate readiness"

    def test_moderate_at_79(self):
        assert ss.classify_readiness_level(79) == "Moderate readiness"

    def test_strong_at_80(self):
        assert ss.classify_readiness_level(80) == "Strong readiness"

    def test_strong_at_100(self):
        assert ss.classify_readiness_level(100) == "Strong readiness"


class TestGetReadinessLevelDescription:
    def test_returns_string(self):
        for level in ["Low readiness", "Developing readiness", "Moderate readiness", "Strong readiness"]:
            result = ss.get_readiness_level_description(level)
            assert isinstance(result, str)
            assert len(result) > 20

    def test_low_readiness_description(self):
        desc = ss.get_readiness_level_description("Low readiness")
        assert "governance" in desc.lower() or "early stage" in desc.lower()

    def test_strong_readiness_description(self):
        desc = ss.get_readiness_level_description("Strong readiness")
        assert "positioned" in desc.lower() or "strong" in desc.lower()

    def test_unknown_level_returns_fallback(self):
        result = ss.get_readiness_level_description("Unknown level")
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetReadinessBandColour:
    def test_returns_hex_string(self):
        for level in ["Low readiness", "Developing readiness", "Moderate readiness", "Strong readiness"]:
            colour = ss.get_readiness_band_colour(level)
            assert isinstance(colour, str)
            assert colour.startswith("#")

    def test_low_readiness_is_red(self):
        colour = ss.get_readiness_band_colour("Low readiness")
        assert colour == "#dc2626"

    def test_unknown_returns_fallback_colour(self):
        colour = ss.get_readiness_band_colour("Unknown")
        assert isinstance(colour, str)
        assert colour.startswith("#")


class TestRankReadinessCategories:
    def test_returns_list(self):
        result = ss.rank_readiness_categories(_SCORES)
        assert isinstance(result, list)

    def test_sorted_highest_first(self):
        result = ss.rank_readiness_categories(_SCORES)
        scores = [c["score"] for c in result]
        assert scores == sorted(scores, reverse=True)

    def test_top_is_workflow_opportunity(self):
        result = ss.rank_readiness_categories(_SCORES)
        assert result[0]["key"] == "workflow_opportunity_score"

    def test_bottom_is_risk_management(self):
        result = ss.rank_readiness_categories(_SCORES)
        assert result[-1]["key"] == "risk_management_score"

    def test_each_item_has_required_keys(self):
        result = ss.rank_readiness_categories(_SCORES)
        for item in result:
            assert "key" in item
            assert "label" in item
            assert "score" in item
            assert "level" in item
            assert "interpretation" in item

    def test_six_categories_returned(self):
        result = ss.rank_readiness_categories(_SCORES)
        assert len(result) == 6

    def test_empty_scores_returns_empty(self):
        result = ss.rank_readiness_categories({})
        assert result == []


class TestIdentifyReadinessStrengths:
    def test_returns_list(self):
        assert isinstance(ss.identify_readiness_strengths(_SCORES), list)

    def test_no_strengths_at_default_threshold_for_brightpath(self):
        result = ss.identify_readiness_strengths(_SCORES)
        assert len(result) == 0

    def test_returns_strengths_at_lower_threshold(self):
        result = ss.identify_readiness_strengths(_SCORES, threshold=60)
        assert len(result) >= 1
        labels = [s["category"] for s in result]
        assert "Workflow opportunity" in labels

    def test_each_strength_has_required_keys(self):
        result = ss.identify_readiness_strengths(_SCORES, threshold=40)
        for s in result:
            assert "category" in s
            assert "score" in s
            assert "reason" in s

    def test_all_categories_above_threshold_returned(self):
        result = ss.identify_readiness_strengths(_HIGH_SCORES, threshold=60)
        assert len(result) == 6

    def test_sorted_highest_first(self):
        result = ss.identify_readiness_strengths(_HIGH_SCORES, threshold=60)
        scores = [s["score"] for s in result]
        assert scores == sorted(scores, reverse=True)


class TestIdentifyReadinessGaps:
    def test_returns_list(self):
        assert isinstance(ss.identify_readiness_gaps(_SCORES), list)

    def test_brightpath_has_five_gaps_at_default_threshold(self):
        result = ss.identify_readiness_gaps(_SCORES)
        assert len(result) == 5

    def test_workflow_opportunity_not_in_gaps(self):
        result = ss.identify_readiness_gaps(_SCORES)
        labels = [g["category"] for g in result]
        assert "Workflow opportunity" not in labels

    def test_each_gap_has_required_keys(self):
        result = ss.identify_readiness_gaps(_SCORES)
        for g in result:
            assert "category" in g
            assert "score" in g
            assert "risk" in g
            assert "recommended_action" in g

    def test_sorted_lowest_first(self):
        result = ss.identify_readiness_gaps(_SCORES)
        scores = [g["score"] for g in result]
        assert scores == sorted(scores)

    def test_lowest_gap_is_risk_management(self):
        result = ss.identify_readiness_gaps(_SCORES)
        assert result[0]["score"] == 25

    def test_no_gaps_with_high_scores(self):
        result = ss.identify_readiness_gaps(_HIGH_SCORES)
        assert len(result) == 0


class TestGenerateCategoryInterpretation:
    def test_returns_string_for_each_category(self):
        for key in [
            "strategy_score", "data_governance_score", "staff_capability_score",
            "workflow_opportunity_score", "risk_management_score", "leadership_alignment_score",
        ]:
            result = ss.generate_category_interpretation(key, 50)
            assert isinstance(result, str)
            assert len(result) > 10

    def test_low_score_returns_low_interpretation(self):
        result = ss.generate_category_interpretation("data_governance_score", 20)
        assert "key constraint" in result.lower() or "data governance" in result.lower()

    def test_strong_score_returns_strong_interpretation(self):
        result = ss.generate_category_interpretation("staff_capability_score", 90)
        assert "strong" in result.lower() or "capable" in result.lower()

    def test_unknown_category_returns_fallback(self):
        result = ss.generate_category_interpretation("unknown_category", 50)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_different_bands_return_different_text(self):
        low = ss.generate_category_interpretation("risk_management_score", 20)
        high = ss.generate_category_interpretation("risk_management_score", 90)
        assert low != high


class TestGenerateReadinessSummary:
    def setup_method(self):
        self.summary = ss.generate_readiness_summary(_SCORES, org_name="BrightPath")

    def test_returns_dict(self):
        assert isinstance(self.summary, dict)

    def test_has_overall_score(self):
        assert "overall_score" in self.summary
        assert self.summary["overall_score"] == 42.0

    def test_has_overall_level(self):
        assert "overall_level" in self.summary
        assert self.summary["overall_level"] == "Developing readiness"

    def test_has_overall_description(self):
        assert "overall_description" in self.summary
        assert len(self.summary["overall_description"]) > 20

    def test_has_six_category_scores(self):
        assert "category_scores" in self.summary
        assert len(self.summary["category_scores"]) == 6

    def test_category_scores_have_key_label_score_level_interpretation(self):
        for cat in self.summary["category_scores"]:
            assert "key" in cat
            assert "label" in cat
            assert "score" in cat
            assert "level" in cat
            assert "interpretation" in cat

    def test_has_ranked_categories(self):
        assert "ranked_categories" in self.summary
        assert len(self.summary["ranked_categories"]) == 6

    def test_has_strengths(self):
        assert "strengths" in self.summary
        assert isinstance(self.summary["strengths"], list)

    def test_has_gaps(self):
        assert "gaps" in self.summary
        assert len(self.summary["gaps"]) > 0

    def test_has_strategic_interpretation(self):
        assert "strategic_interpretation" in self.summary
        assert "BrightPath" in self.summary["strategic_interpretation"]

    def test_has_recommendations(self):
        assert "recommendations" in self.summary
        assert len(self.summary["recommendations"]) > 0

    def test_has_responsible_use_note(self):
        assert "responsible_use_note" in self.summary
        assert len(self.summary["responsible_use_note"]) > 20

    def test_has_prototype_note(self):
        assert "prototype_note" in self.summary
        assert len(self.summary["prototype_note"]) > 20

    def test_missing_overall_score_calculates_from_categories(self):
        summary = ss.generate_readiness_summary(_SCORES_NO_OVERALL)
        expected = ss.calculate_average_readiness_score(_SCORES_NO_OVERALL)
        assert summary["overall_score"] == expected

    def test_empty_scores_returns_safe_summary(self):
        summary = ss.generate_readiness_summary({})
        assert summary["overall_score"] == 0.0
        assert isinstance(summary["overall_level"], str)
        assert isinstance(summary["recommendations"], list)


class TestGenerateReadinessRecommendations:
    def test_returns_list(self):
        summary = ss.generate_readiness_summary(_SCORES)
        result = ss.generate_readiness_recommendations(summary)
        assert isinstance(result, list)

    def test_non_empty(self):
        summary = ss.generate_readiness_summary(_SCORES)
        result = ss.generate_readiness_recommendations(summary)
        assert len(result) > 0

    def test_all_items_are_strings(self):
        summary = ss.generate_readiness_summary(_SCORES)
        for rec in ss.generate_readiness_recommendations(summary):
            assert isinstance(rec, str)
            assert len(rec) > 10

    def test_data_governance_gap_generates_data_rec(self):
        summary = ss.generate_readiness_summary(_SCORES)
        recs = ss.generate_readiness_recommendations(summary)
        combined = " ".join(recs).lower()
        assert "data" in combined or "dpia" in combined

    def test_empty_summary_returns_recommendations(self):
        empty_summary = {"gaps": [], "strengths": [], "overall_score": 0}
        result = ss.generate_readiness_recommendations(empty_summary)
        assert isinstance(result, list)
        assert len(result) >= 1


class TestFormatReadinessSummaryAsMarkdown:
    def setup_method(self):
        self.summary = ss.generate_readiness_summary(_SCORES)
        self.md = ss.format_readiness_summary_as_markdown(self.summary)

    def test_returns_string(self):
        assert isinstance(self.md, str)

    def test_non_empty(self):
        assert len(self.md) > 100

    def test_contains_main_heading(self):
        assert "# AI Readiness Summary" in self.md

    def test_contains_overall_readiness_section(self):
        assert "## Overall Readiness" in self.md

    def test_contains_category_scores_section(self):
        assert "## Category Scores" in self.md

    def test_contains_strengths_section(self):
        assert "## Strengths" in self.md

    def test_contains_priority_gaps_section(self):
        assert "## Priority Gaps" in self.md

    def test_contains_strategic_interpretation_section(self):
        assert "## Strategic Interpretation" in self.md

    def test_contains_recommendations_section(self):
        assert "## Recommendations" in self.md

    def test_contains_responsible_use_boundaries(self):
        assert "## Responsible-Use Boundaries" in self.md

    def test_responsible_use_note_in_markdown(self):
        assert "synthetic/demo audit data" in self.md.lower() or "synthetic" in self.md.lower()

    def test_overall_score_in_markdown(self):
        assert "42" in self.md
