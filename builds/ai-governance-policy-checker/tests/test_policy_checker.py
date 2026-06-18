import pytest
from src.governance_framework import get_responsible_ai_governance_framework
from src.sample_policies import get_brightpath_policy_pack
from src.policy_checker import (
    normalise_text,
    count_keyword_matches,
    extract_matching_policy_snippets,
    get_domain_keyword_map,
    classify_coverage_level,
    calculate_coverage_score,
    check_domain_coverage,
    check_policy_pack_coverage,
    summarise_policy_coverage,
    format_policy_coverage_as_markdown,
)


@pytest.fixture
def policy_pack():
    return get_brightpath_policy_pack()


@pytest.fixture
def framework():
    return get_responsible_ai_governance_framework()


@pytest.fixture
def coverage_results(policy_pack, framework):
    return check_policy_pack_coverage(policy_pack, framework)


class TestNormaliseText:
    def test_lowercases_text(self):
        assert normalise_text("HELLO WORLD") == "hello world"

    def test_strips_leading_trailing_whitespace(self):
        assert normalise_text("  hello  ") == "hello"

    def test_collapses_multiple_spaces(self):
        assert normalise_text("hello   world") == "hello world"

    def test_handles_empty_string(self):
        assert normalise_text("") == ""

    def test_handles_none(self):
        assert normalise_text(None) == ""

    def test_handles_mixed_case_and_whitespace(self):
        result = normalise_text("  AI Policy   REVIEW  ")
        assert result == "ai policy review"


class TestCountKeywordMatches:
    def test_returns_expected_count(self):
        text = "human review is required. human review checklist."
        count = count_keyword_matches(text, ["human review"])
        assert count == 2

    def test_handles_empty_text(self):
        assert count_keyword_matches("", ["keyword"]) == 0

    def test_handles_empty_keywords(self):
        assert count_keyword_matches("some text", []) == 0

    def test_handles_none_text(self):
        assert count_keyword_matches(None, ["keyword"]) == 0

    def test_counts_multiple_keywords(self):
        text = "training is required. staff training matters. bias risk."
        count = count_keyword_matches(text, ["training", "bias"])
        assert count >= 3

    def test_case_insensitive(self):
        text = "SAFEGUARDING is important."
        count = count_keyword_matches(text, ["safeguarding"])
        assert count == 1

    def test_no_match_returns_zero(self):
        assert count_keyword_matches("this text has nothing relevant", ["blockchain"]) == 0


class TestExtractMatchingPolicySnippets:
    def test_returns_list(self):
        result = extract_matching_policy_snippets("some text here", ["text"])
        assert isinstance(result, list)

    def test_finds_matching_line(self):
        text = "Line one.\nHuman review is required here.\nLine three."
        result = extract_matching_policy_snippets(text, ["human review"])
        assert len(result) >= 1
        assert any("human review" in s.lower() for s in result)

    def test_handles_no_matches(self):
        result = extract_matching_policy_snippets("unrelated content", ["blockchain"])
        assert result == []

    def test_respects_max_snippets(self):
        lines = "\n".join(f"Line {i} with keyword here." for i in range(10))
        result = extract_matching_policy_snippets(lines, ["keyword"], max_snippets=2)
        assert len(result) <= 2

    def test_handles_empty_text(self):
        result = extract_matching_policy_snippets("", ["keyword"])
        assert result == []

    def test_handles_empty_keywords(self):
        result = extract_matching_policy_snippets("some text", [])
        assert result == []

    def test_default_max_snippets_is_three(self):
        lines = "\n".join(f"keyword found on line {i}." for i in range(10))
        result = extract_matching_policy_snippets(lines, ["keyword"])
        assert len(result) <= 3


class TestGetDomainKeywordMap:
    def test_returns_dictionary(self):
        assert isinstance(get_domain_keyword_map(), dict)

    def test_non_empty(self):
        assert len(get_domain_keyword_map()) > 0

    def test_each_value_is_non_empty_list(self):
        for key, value in get_domain_keyword_map().items():
            assert isinstance(value, list)
            assert len(value) > 0

    def test_includes_safeguarding_key(self):
        keyword_map = get_domain_keyword_map()
        keys_lower = [k.lower() for k in keyword_map]
        assert any("safeguarding" in k for k in keys_lower)

    def test_includes_data_protection_key(self):
        keyword_map = get_domain_keyword_map()
        keys_lower = [k.lower() for k in keyword_map]
        assert any("data protection" in k for k in keys_lower)


class TestClassifyCoverageLevel:
    def test_returns_not_covered_for_zero(self):
        assert classify_coverage_level(0) == "Not covered"

    def test_returns_not_covered_for_24(self):
        assert classify_coverage_level(24) == "Not covered"

    def test_returns_weak_coverage_for_25(self):
        assert classify_coverage_level(25) == "Weak coverage"

    def test_returns_weak_coverage_for_49(self):
        assert classify_coverage_level(49) == "Weak coverage"

    def test_returns_partial_coverage_for_50(self):
        assert classify_coverage_level(50) == "Partial coverage"

    def test_returns_partial_coverage_for_74(self):
        assert classify_coverage_level(74) == "Partial coverage"

    def test_returns_strong_coverage_for_75(self):
        assert classify_coverage_level(75) == "Strong coverage"

    def test_returns_strong_coverage_for_100(self):
        assert classify_coverage_level(100) == "Strong coverage"


class TestCalculateCoverageScore:
    def test_returns_number_between_0_and_100(self):
        domain_results = [
            {"coverage_score": 80.0},
            {"coverage_score": 40.0},
            {"coverage_score": 60.0},
        ]
        score = calculate_coverage_score(domain_results)
        assert 0 <= score <= 100

    def test_returns_average(self):
        domain_results = [
            {"coverage_score": 80.0},
            {"coverage_score": 40.0},
        ]
        score = calculate_coverage_score(domain_results)
        assert score == 60.0

    def test_handles_empty_list(self):
        assert calculate_coverage_score([]) == 0.0

    def test_handles_single_item(self):
        assert calculate_coverage_score([{"coverage_score": 75.0}]) == 75.0


class TestCheckDomainCoverage:
    def setup_method(self):
        self.domain = {
            "domain_id": "GOV-006",
            "domain_name": "Safeguarding Boundaries",
            "priority_level": "High",
            "expected_policy_evidence": [
                "Explicit prohibition on AI in safeguarding decisions",
                "Prohibition on AI access to safeguarding case records",
            ],
        }
        self.policies = get_brightpath_policy_pack()["policies"]

    def test_returns_dict(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert isinstance(result, dict)

    def test_has_domain_id(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "domain_id" in result
        assert result["domain_id"] == "GOV-006"

    def test_has_domain_name(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "domain_name" in result

    def test_has_coverage_score(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "coverage_score" in result
        assert 0 <= result["coverage_score"] <= 100

    def test_has_coverage_level(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "coverage_level" in result
        assert result["coverage_level"] in (
            "Strong coverage", "Partial coverage", "Weak coverage", "Not covered"
        )

    def test_has_matched_policies(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "matched_policies" in result
        assert isinstance(result["matched_policies"], list)

    def test_has_matched_keywords(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "matched_keywords" in result
        assert isinstance(result["matched_keywords"], list)

    def test_has_evidence_snippets(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "evidence_snippets" in result
        assert isinstance(result["evidence_snippets"], list)

    def test_has_coverage_explanation(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "coverage_explanation" in result
        assert result["coverage_explanation"]

    def test_has_review_note(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert "review_note" in result

    def test_safeguarding_domain_scores_above_zero(self):
        result = check_domain_coverage(self.domain, self.policies)
        assert result["coverage_score"] > 0

    def test_handles_empty_policies_list(self):
        result = check_domain_coverage(self.domain, [])
        assert result["coverage_score"] == 0.0
        assert result["coverage_level"] == "Not covered"
        assert result["matched_policies"] == []


class TestCheckPolicyPackCoverage:
    def test_returns_dict(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert isinstance(result, dict)

    def test_has_organisation_name(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "organisation_name" in result
        assert result["organisation_name"] == "BrightPath Skills Training"

    def test_has_total_policies_reviewed(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "total_policies_reviewed" in result
        assert result["total_policies_reviewed"] == len(policy_pack["policies"])

    def test_has_total_domains_checked(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "total_domains_checked" in result
        assert result["total_domains_checked"] == len(framework)

    def test_has_domain_results(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "domain_results" in result
        assert isinstance(result["domain_results"], list)
        assert len(result["domain_results"]) == len(framework)

    def test_has_overall_coverage_score(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "overall_coverage_score" in result
        assert 0 <= result["overall_coverage_score"] <= 100

    def test_has_overall_coverage_level(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "overall_coverage_level" in result

    def test_has_strong_domains(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "strong_domains" in result
        assert isinstance(result["strong_domains"], list)

    def test_has_responsible_use_note(self, policy_pack, framework):
        result = check_policy_pack_coverage(policy_pack, framework)
        assert "responsible_use_note" in result
        assert result["responsible_use_note"]

    def test_handles_missing_policies_safely(self, framework):
        empty_pack = {"organisation_name": "Test", "policy_pack_title": "Test Pack"}
        result = check_policy_pack_coverage(empty_pack, framework)
        assert result["total_policies_reviewed"] == 0
        assert result["overall_coverage_score"] == 0.0

    def test_handles_non_dict_policy_pack_safely(self, framework):
        result = check_policy_pack_coverage(None, framework)
        assert isinstance(result, dict)
        assert result["total_policies_reviewed"] == 0


class TestSummarisePolicyCoverage:
    def test_returns_dict(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert isinstance(result, dict)

    def test_has_overall_coverage_score(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "overall_coverage_score" in result

    def test_has_overall_coverage_level(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "overall_coverage_level" in result

    def test_has_total_domains(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "total_domains" in result
        assert result["total_domains"] > 0

    def test_has_strong_count(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "strong_count" in result

    def test_has_partial_count(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "partial_count" in result

    def test_has_weak_count(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "weak_count" in result

    def test_has_not_covered_count(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "not_covered_count" in result

    def test_counts_add_up_to_total(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        total = (
            result["strong_count"]
            + result["partial_count"]
            + result["weak_count"]
            + result["not_covered_count"]
        )
        assert total == result["total_domains"]

    def test_has_high_priority_gaps(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "high_priority_gaps" in result
        assert isinstance(result["high_priority_gaps"], list)

    def test_has_best_covered_domains(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "best_covered_domains" in result
        assert isinstance(result["best_covered_domains"], list)

    def test_has_weakest_domains(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "weakest_domains" in result

    def test_has_recommended_focus(self, coverage_results):
        result = summarise_policy_coverage(coverage_results)
        assert "recommended_focus" in result
        assert isinstance(result["recommended_focus"], list)
        assert len(result["recommended_focus"]) > 0


class TestFormatPolicyCoverageAsMarkdown:
    def test_returns_string(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert isinstance(result, str)

    def test_non_empty(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert len(result) > 0

    def test_includes_title(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert "AI Governance Policy Coverage Review" in result

    def test_includes_responsible_use_boundaries_section(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert "Responsible-Use Boundaries" in result

    def test_includes_overall_coverage_summary(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert "Overall Coverage Summary" in result

    def test_includes_domain_by_domain_section(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert "Domain-by-Domain Coverage Review" in result

    def test_includes_organisation_name(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert "BrightPath Skills Training" in result

    def test_includes_human_review_note(self, coverage_results):
        result = format_policy_coverage_as_markdown(coverage_results)
        assert "human review" in result.lower()

    def test_accepts_precomputed_summary(self, coverage_results):
        from src.policy_checker import summarise_policy_coverage
        summary = summarise_policy_coverage(coverage_results)
        result = format_policy_coverage_as_markdown(coverage_results, summary)
        assert isinstance(result, str)
        assert "AI Governance Policy Coverage Review" in result
