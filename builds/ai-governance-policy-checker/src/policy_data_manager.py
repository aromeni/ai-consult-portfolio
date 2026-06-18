def validate_policy_pack(policy_pack: dict) -> tuple:
    if not isinstance(policy_pack, dict):
        return False, "Policy pack must be a dictionary."
    if not policy_pack.get("organisation_name"):
        return False, "Missing required field: organisation_name."
    if not policy_pack.get("policy_pack_title"):
        return False, "Missing required field: policy_pack_title."
    if "policies" not in policy_pack:
        return False, "Missing required field: policies."
    policies = policy_pack["policies"]
    if not isinstance(policies, list) or len(policies) == 0:
        return False, "policies must be a non-empty list."
    for i, policy in enumerate(policies):
        if not policy.get("policy_id"):
            return False, f"Policy at index {i} is missing policy_id."
        if not policy.get("policy_title"):
            return False, f"Policy at index {i} is missing policy_title."
        if not policy.get("policy_text"):
            return False, f"Policy at index {i} is missing policy_text."
    return True, "Valid."


def summarise_policy_pack(policy_pack: dict) -> dict:
    policies = policy_pack.get("policies", [])
    policy_types = list({p.get("policy_type", "Unknown") for p in policies})
    risk_areas: list = []
    for p in policies:
        for area in p.get("related_risk_areas", []):
            if area not in risk_areas:
                risk_areas.append(area)
    owners = list({p.get("owner", "Unknown") for p in policies})
    return {
        "organisation_name": policy_pack.get("organisation_name", ""),
        "policy_pack_title": policy_pack.get("policy_pack_title", ""),
        "total_policies": len(policies),
        "policy_types": sorted(policy_types),
        "risk_areas": sorted(risk_areas),
        "owners": sorted(owners),
        "synthetic_demo_only": True,
    }


def format_policy_pack_as_markdown(policy_pack: dict) -> str:
    org = policy_pack.get("organisation_name", "Unknown Organisation")
    title = policy_pack.get("policy_pack_title", "Policy Pack")
    policies = policy_pack.get("policies", [])
    lines = [
        "# Synthetic Policy Pack",
        "",
        "## Organisation",
        "",
        f"**Name:** {org}",
        f"**Type:** {policy_pack.get('organisation_type', '')}",
        f"**Sector:** {policy_pack.get('sector', '')}",
        f"**Country:** {policy_pack.get('country_context', '')}",
        "",
        "---",
        "",
        "## Policy Pack Summary",
        "",
        f"**Title:** {title}",
        f"**Status:** {policy_pack.get('policy_pack_status', '')}",
        f"**Total policies:** {len(policies)}",
        "",
        "---",
        "",
        "## Policies",
        "",
    ]
    for policy in policies:
        lines.append(f"### {policy.get('policy_id', '')}: {policy.get('policy_title', '')}")
        lines.append(f"**Type:** {policy.get('policy_type', '')}  ")
        lines.append(f"**Owner:** {policy.get('owner', '')}  ")
        lines.append(f"**Status:** {policy.get('status', '')}  ")
        lines.append(f"**Last reviewed:** {policy.get('last_reviewed', '')}  ")
        lines.append("")
        lines.append(policy.get("summary", ""))
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.extend([
        "## Responsible-Use Boundaries",
        "",
        (
            "This policy pack is synthetic/demo content only. It must not be treated as an "
            "approved organisational policy, legal advice, safeguarding guidance, HR advice, "
            "compliance advice, data-protection advice, or professional governance advice."
        ),
        "",
        (
            "Do not use this prototype with real client records, learner data, safeguarding "
            "case details, staff HR data, personal data, confidential data, or regulated "
            "information without appropriate governance, approvals, and responsible owners."
        ),
        "",
        "Human review remains required before any real-world use.",
    ])
    return "\n".join(lines)


def get_policy_by_id(policy_pack: dict, policy_id: str):
    for policy in policy_pack.get("policies", []):
        if policy.get("policy_id") == policy_id:
            return policy
    return None


def search_policies_by_risk_area(policy_pack: dict, risk_area: str) -> list:
    results = []
    risk_area_lower = risk_area.lower()
    for policy in policy_pack.get("policies", []):
        areas = [a.lower() for a in policy.get("related_risk_areas", [])]
        if any(risk_area_lower in a for a in areas):
            results.append(policy)
    return results


def extract_policy_titles(policy_pack: dict) -> list:
    return [p.get("policy_title", "") for p in policy_pack.get("policies", [])]
