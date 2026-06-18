import pytest
from src.sample_policies import (
    get_brightpath_policy_pack,
    get_demo_policy_list,
    get_default_policy_types,
    get_default_risk_areas,
)


class TestGetBrightpathPolicyPack:
    def test_returns_dict(self):
        assert isinstance(get_brightpath_policy_pack(), dict)

    def test_has_organisation_name(self):
        result = get_brightpath_policy_pack()
        assert "organisation_name" in result
        assert result["organisation_name"]

    def test_has_policy_pack_title(self):
        result = get_brightpath_policy_pack()
        assert "policy_pack_title" in result
        assert result["policy_pack_title"]

    def test_has_policies_list(self):
        result = get_brightpath_policy_pack()
        assert "policies" in result
        assert isinstance(result["policies"], list)

    def test_policies_list_is_non_empty(self):
        result = get_brightpath_policy_pack()
        assert len(result["policies"]) > 0

    def test_has_responsible_use_note(self):
        result = get_brightpath_policy_pack()
        assert "responsible_use_note" in result
        assert result["responsible_use_note"]

    def test_has_sector(self):
        result = get_brightpath_policy_pack()
        assert "sector" in result

    def test_has_country_context(self):
        result = get_brightpath_policy_pack()
        assert "country_context" in result


class TestPolicyItems:
    def test_each_policy_has_policy_id(self):
        pack = get_brightpath_policy_pack()
        for policy in pack["policies"]:
            assert "policy_id" in policy
            assert policy["policy_id"]

    def test_each_policy_has_policy_title(self):
        pack = get_brightpath_policy_pack()
        for policy in pack["policies"]:
            assert "policy_title" in policy
            assert policy["policy_title"]

    def test_each_policy_has_policy_text(self):
        pack = get_brightpath_policy_pack()
        for policy in pack["policies"]:
            assert "policy_text" in policy
            assert policy["policy_text"]

    def test_each_policy_has_owner(self):
        pack = get_brightpath_policy_pack()
        for policy in pack["policies"]:
            assert "owner" in policy

    def test_each_policy_has_related_risk_areas(self):
        pack = get_brightpath_policy_pack()
        for policy in pack["policies"]:
            assert "related_risk_areas" in policy
            assert isinstance(policy["related_risk_areas"], list)


class TestGetDemoPolicyList:
    def test_returns_list(self):
        assert isinstance(get_demo_policy_list(), list)

    def test_returns_non_empty_list(self):
        assert len(get_demo_policy_list()) > 0

    def test_each_item_is_dict(self):
        for item in get_demo_policy_list():
            assert isinstance(item, dict)


class TestGetDefaultPolicyTypes:
    def test_returns_non_empty_list(self):
        result = get_default_policy_types()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_all_strings(self):
        for item in get_default_policy_types():
            assert isinstance(item, str)


class TestGetDefaultRiskAreas:
    def test_returns_non_empty_list(self):
        result = get_default_risk_areas()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_all_strings(self):
        for item in get_default_risk_areas():
            assert isinstance(item, str)
