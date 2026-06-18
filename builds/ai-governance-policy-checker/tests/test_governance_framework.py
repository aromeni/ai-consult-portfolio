import pytest
from src.governance_framework import (
    get_responsible_ai_governance_framework,
    get_framework_domain_ids,
    get_framework_domain_names,
    get_high_priority_domains,
    summarise_governance_framework,
    format_governance_framework_as_markdown,
)


class TestGetResponsibleAiGovernanceFramework:
    def test_returns_non_empty_list(self):
        result = get_responsible_ai_governance_framework()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_each_domain_has_domain_id(self):
        for domain in get_responsible_ai_governance_framework():
            assert "domain_id" in domain
            assert domain["domain_id"]

    def test_each_domain_has_domain_name(self):
        for domain in get_responsible_ai_governance_framework():
            assert "domain_name" in domain
            assert domain["domain_name"]

    def test_each_domain_has_description(self):
        for domain in get_responsible_ai_governance_framework():
            assert "description" in domain

    def test_each_domain_has_expected_policy_evidence(self):
        for domain in get_responsible_ai_governance_framework():
            assert "expected_policy_evidence" in domain
            assert isinstance(domain["expected_policy_evidence"], list)

    def test_each_domain_has_valid_priority_level(self):
        for domain in get_responsible_ai_governance_framework():
            assert "priority_level" in domain
            assert domain["priority_level"] in ("High", "Medium", "Low")

    def test_each_domain_has_example_controls(self):
        for domain in get_responsible_ai_governance_framework():
            assert "example_controls" in domain
            assert isinstance(domain["example_controls"], list)


class TestGetFrameworkDomainIds:
    def test_returns_list(self):
        assert isinstance(get_framework_domain_ids(), list)

    def test_non_empty(self):
        assert len(get_framework_domain_ids()) > 0

    def test_all_strings(self):
        for item in get_framework_domain_ids():
            assert isinstance(item, str)


class TestGetFrameworkDomainNames:
    def test_returns_list(self):
        assert isinstance(get_framework_domain_names(), list)

    def test_non_empty(self):
        assert len(get_framework_domain_names()) > 0

    def test_all_strings(self):
        for item in get_framework_domain_names():
            assert isinstance(item, str)


class TestGetHighPriorityDomains:
    def test_returns_list(self):
        assert isinstance(get_high_priority_domains(), list)

    def test_all_high_priority(self):
        for domain in get_high_priority_domains():
            assert domain["priority_level"] == "High"

    def test_non_empty(self):
        assert len(get_high_priority_domains()) > 0


class TestSummariseGovernanceFramework:
    def setup_method(self):
        self.framework = get_responsible_ai_governance_framework()
        self.summary = summarise_governance_framework(self.framework)

    def test_returns_dict(self):
        assert isinstance(self.summary, dict)

    def test_has_total_domains(self):
        assert "total_domains" in self.summary
        assert self.summary["total_domains"] == len(self.framework)

    def test_has_high_priority_count(self):
        assert "high_priority_count" in self.summary

    def test_has_domain_names(self):
        assert "domain_names" in self.summary
        assert isinstance(self.summary["domain_names"], list)

    def test_has_domain_ids(self):
        assert "domain_ids" in self.summary
        assert isinstance(self.summary["domain_ids"], list)


class TestFormatGovernanceFrameworkAsMarkdown:
    def setup_method(self):
        self.framework = get_responsible_ai_governance_framework()
        self.result = format_governance_framework_as_markdown(self.framework)

    def test_returns_string(self):
        assert isinstance(self.result, str)

    def test_non_empty(self):
        assert len(self.result) > 0

    def test_includes_title(self):
        assert "Responsible AI Governance Framework" in self.result

    def test_includes_all_domain_names(self):
        for domain in self.framework:
            assert domain["domain_name"] in self.result

    def test_includes_responsible_use_note(self):
        lower = self.result.lower()
        assert "synthetic" in lower or "human review" in lower
