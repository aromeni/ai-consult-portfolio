import pytest
from src.sample_policies import get_brightpath_policy_pack
from src.policy_data_manager import (
    validate_policy_pack,
    summarise_policy_pack,
    format_policy_pack_as_markdown,
    get_policy_by_id,
    search_policies_by_risk_area,
    extract_policy_titles,
)


@pytest.fixture
def valid_pack():
    return get_brightpath_policy_pack()


@pytest.fixture
def minimal_pack():
    return {
        "organisation_name": "Test Org",
        "policy_pack_title": "Test Pack",
        "policies": [
            {
                "policy_id": "T-001",
                "policy_title": "Test Policy",
                "policy_text": "Some policy text.",
            }
        ],
    }


class TestValidatePolicyPack:
    def test_valid_pack_passes(self, valid_pack):
        is_valid, msg = validate_policy_pack(valid_pack)
        assert is_valid is True

    def test_returns_tuple(self, valid_pack):
        result = validate_policy_pack(valid_pack)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_missing_organisation_name_fails(self, minimal_pack):
        del minimal_pack["organisation_name"]
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False

    def test_missing_policy_pack_title_fails(self, minimal_pack):
        del minimal_pack["policy_pack_title"]
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False

    def test_missing_policies_fails(self, minimal_pack):
        del minimal_pack["policies"]
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False

    def test_empty_policies_list_fails(self, minimal_pack):
        minimal_pack["policies"] = []
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False

    def test_policy_missing_policy_id_fails(self, minimal_pack):
        del minimal_pack["policies"][0]["policy_id"]
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False

    def test_policy_missing_policy_title_fails(self, minimal_pack):
        del minimal_pack["policies"][0]["policy_title"]
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False

    def test_policy_missing_policy_text_fails(self, minimal_pack):
        del minimal_pack["policies"][0]["policy_text"]
        is_valid, msg = validate_policy_pack(minimal_pack)
        assert is_valid is False


class TestSummarisePolicyPack:
    def setup_method(self):
        self.pack = get_brightpath_policy_pack()
        self.summary = summarise_policy_pack(self.pack)

    def test_returns_dict(self):
        assert isinstance(self.summary, dict)

    def test_has_organisation_name(self):
        assert "organisation_name" in self.summary

    def test_has_total_policies(self):
        assert "total_policies" in self.summary
        assert self.summary["total_policies"] == len(self.pack["policies"])

    def test_has_policy_types(self):
        assert "policy_types" in self.summary
        assert isinstance(self.summary["policy_types"], list)

    def test_has_risk_areas(self):
        assert "risk_areas" in self.summary
        assert isinstance(self.summary["risk_areas"], list)

    def test_has_synthetic_demo_only_flag(self):
        assert "synthetic_demo_only" in self.summary
        assert self.summary["synthetic_demo_only"] is True


class TestFormatPolicyPackAsMarkdown:
    def setup_method(self):
        self.pack = get_brightpath_policy_pack()
        self.result = format_policy_pack_as_markdown(self.pack)

    def test_returns_string(self):
        assert isinstance(self.result, str)

    def test_non_empty(self):
        assert len(self.result) > 0

    def test_includes_synthetic_policy_pack_heading(self):
        assert "Synthetic Policy Pack" in self.result

    def test_includes_organisation_name(self):
        assert self.pack["organisation_name"] in self.result

    def test_includes_responsible_use_section(self):
        assert "Responsible-Use Boundaries" in self.result

    def test_includes_human_review_note(self):
        assert "Human review" in self.result


class TestGetPolicyById:
    def test_finds_existing_policy(self, valid_pack):
        first_id = valid_pack["policies"][0]["policy_id"]
        result = get_policy_by_id(valid_pack, first_id)
        assert result is not None
        assert result["policy_id"] == first_id

    def test_returns_none_for_missing_policy(self, valid_pack):
        result = get_policy_by_id(valid_pack, "DOES-NOT-EXIST")
        assert result is None

    def test_returns_dict_for_found_policy(self, valid_pack):
        first_id = valid_pack["policies"][0]["policy_id"]
        result = get_policy_by_id(valid_pack, first_id)
        assert isinstance(result, dict)


class TestSearchPoliciesByRiskArea:
    def test_returns_list(self, valid_pack):
        result = search_policies_by_risk_area(valid_pack, "human review")
        assert isinstance(result, list)

    def test_finds_matching_policies(self, valid_pack):
        result = search_policies_by_risk_area(valid_pack, "human review")
        assert len(result) > 0

    def test_no_match_returns_empty_list(self, valid_pack):
        result = search_policies_by_risk_area(valid_pack, "completely-nonexistent-xyz-999")
        assert result == []


class TestExtractPolicyTitles:
    def test_returns_list(self, valid_pack):
        assert isinstance(extract_policy_titles(valid_pack), list)

    def test_non_empty(self, valid_pack):
        assert len(extract_policy_titles(valid_pack)) > 0

    def test_all_strings(self, valid_pack):
        for title in extract_policy_titles(valid_pack):
            assert isinstance(title, str)

    def test_count_matches_policies(self, valid_pack):
        result = extract_policy_titles(valid_pack)
        assert len(result) == len(valid_pack["policies"])
