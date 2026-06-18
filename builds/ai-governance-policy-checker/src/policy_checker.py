import re


def normalise_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def count_keyword_matches(text: str, keywords: list) -> int:
    if not text or not keywords:
        return 0
    normalised = normalise_text(text)
    count = 0
    for keyword in keywords:
        kw = normalise_text(keyword)
        if not kw:
            continue
        start = 0
        while True:
            idx = normalised.find(kw, start)
            if idx == -1:
                break
            count += 1
            start = idx + len(kw)
    return count


def extract_matching_policy_snippets(
    policy_text: str, keywords: list, max_snippets: int = 3
) -> list:
    if not policy_text or not keywords:
        return []
    snippets = []
    lines = policy_text.split("\n")
    for line in lines:
        if len(snippets) >= max_snippets:
            break
        stripped = line.strip()
        if not stripped:
            continue
        line_lower = stripped.lower()
        for keyword in keywords:
            kw = keyword.lower().strip()
            if kw and kw in line_lower:
                snippet = stripped[:200]
                if snippet not in snippets:
                    snippets.append(snippet)
                break
    return snippets[:max_snippets]


def get_domain_keyword_map() -> dict:
    return {
        "Strategy and Ownership": [
            "responsible owner",
            "governance lead",
            "senior leadership",
            "senior management",
            "accountability",
            "governance owner",
            "named lead",
            "board approval",
            "governance oversight",
            "designated lead",
        ],
        "Approved AI Tools": [
            "approved tool",
            "approved list",
            "approved ai",
            "authorised tool",
            "permitted tool",
            "approved system",
            "tool approval",
            "supplier review",
            "procurement",
            "approved for use",
        ],
        "Prohibited AI Uses": [
            "prohibited",
            "must not",
            "not permitted",
            "must never",
            "not allowed",
            "forbidden",
            "banned",
            "restricted",
            "unacceptable use",
            "do not",
        ],
        "Data Protection and Confidentiality": [
            "personal data",
            "confidential",
            "data protection",
            "sensitive data",
            "identifiers",
            "anonymised",
            "data minimisation",
            "minimise data",
            "private information",
            "identifiable",
        ],
        "Learner and Client Data Boundaries": [
            "learner data",
            "client data",
            "learner name",
            "learner record",
            "identifiable learner",
            "individual learner",
            "client record",
            "case detail",
            "learner information",
            "assessment record",
        ],
        "Safeguarding Boundaries": [
            "safeguarding",
            "safeguarding concern",
            "designated safeguarding",
            "dsl",
            "safeguarding case",
            "safeguarding decision",
            "safeguarding referral",
            "safeguarding risk",
        ],
        "Human Review and Accountability": [
            "human review",
            "human sign-off",
            "qualified staff",
            "qualified human",
            "accountable",
            "professional responsibility",
            "reviewed and approved",
            "final decision",
            "manager review",
            "sign-off",
        ],
        "Accuracy and Hallucination Control": [
            "accuracy",
            "hallucination",
            "fact check",
            "verify",
            "verified",
            "source check",
            "output review",
            "error",
            "inaccurate",
            "correction",
        ],
        "Bias, Fairness, and Inclusion": [
            "bias",
            "fairness",
            "inclusion",
            "equality",
            "discrimination",
            "protected characteristic",
            "inclusive language",
            "unfair",
            "stereotype",
        ],
        "Staff Training and Capability": [
            "staff training",
            "training",
            "capability",
            "awareness",
            "ai awareness",
            "training completion",
            "induction",
            "guidance",
            "safe prompting",
        ],
        "Escalation and Incident Reporting": [
            "incident",
            "near miss",
            "near-miss",
            "escalation",
            "report concern",
            "safeguarding lead",
            "data protection lead",
            "ai incident",
            "breach",
        ],
        "Monitoring, Review, and Continuous Improvement": [
            "monitoring",
            "reviewed annually",
            "continuous improvement",
            "lessons learned",
            "periodic review",
            "governance meeting",
            "audit",
            "update",
            "review cadence",
        ],
    }


def _score_domain(total_matches: int, matching_policies: int, total_policies: int) -> float:
    if total_matches == 0:
        return 0.0
    if total_matches <= 2:
        base = 25.0
    elif total_matches <= 6:
        base = 50.0
    else:
        base = 72.0
    policy_ratio = matching_policies / max(total_policies, 1)
    if total_matches <= 2:
        bonus = policy_ratio * 10.0
        return min(base + bonus, 49.0)
    elif total_matches <= 6:
        bonus = policy_ratio * 20.0
        return min(base + bonus, 74.0)
    else:
        bonus = policy_ratio * 25.0
        return min(base + bonus, 100.0)


def check_domain_coverage(domain: dict, policies: list) -> dict:
    domain_id = domain.get("domain_id", "")
    domain_name = domain.get("domain_name", "")
    priority_level = domain.get("priority_level", "Medium")
    expected_policy_evidence = domain.get("expected_policy_evidence", [])

    keyword_map = get_domain_keyword_map()

    # Direct lookup first, then substring fallback
    keywords = keyword_map.get(domain_name, [])
    if not keywords:
        for key in keyword_map:
            if key.lower() in domain_name.lower() or domain_name.lower() in key.lower():
                keywords = keyword_map[key]
                break

    # Final fallback: extract meaningful words from domain metadata
    if not keywords:
        words = [w for w in domain_name.lower().split() if len(w) > 4]
        for item in expected_policy_evidence:
            words.extend(w for w in item.lower().split() if len(w) > 4)
        keywords = list(dict.fromkeys(words))

    matched_policies: list = []
    matched_keywords_found: set = set()
    all_snippets: list = []
    total_matches = 0

    safe_policies = policies if isinstance(policies, list) else []

    for policy in safe_policies:
        if not isinstance(policy, dict):
            continue
        policy_text = policy.get("policy_text", "") or ""
        policy_title = policy.get("policy_title", "")

        match_count = count_keyword_matches(policy_text, keywords)
        if match_count > 0:
            matched_policies.append(policy_title)
            total_matches += match_count

            norm_text = normalise_text(policy_text)
            for kw in keywords:
                if normalise_text(kw) in norm_text:
                    matched_keywords_found.add(kw)

            snippets = extract_matching_policy_snippets(policy_text, keywords, max_snippets=2)
            all_snippets.extend(snippets)

    matched_keywords = sorted(matched_keywords_found)
    evidence_snippets = list(dict.fromkeys(all_snippets))[:5]

    coverage_score = round(
        _score_domain(total_matches, len(matched_policies), len(safe_policies)), 1
    )
    coverage_level = classify_coverage_level(coverage_score)

    explanations = {
        "Strong coverage": (
            "The synthetic policy pack includes multiple references that appear to address "
            "this governance domain. Human review is still required to confirm whether the "
            "wording is sufficient and operationally usable."
        ),
        "Partial coverage": (
            "The synthetic policy pack contains some relevant wording, but the domain may "
            "need clearer controls, ownership, examples, or escalation routes."
        ),
        "Weak coverage": (
            "The synthetic policy pack contains limited wording for this domain. The "
            "organisation should strengthen this area before relying on the policy pack."
        ),
        "Not covered": (
            "No clear evidence was found for this domain in the synthetic policy pack. "
            "This should be treated as a priority gap for review."
        ),
    }

    return {
        "domain_id": domain_id,
        "domain_name": domain_name,
        "priority_level": priority_level,
        "coverage_score": coverage_score,
        "coverage_level": coverage_level,
        "matched_policies": matched_policies,
        "matched_keywords": matched_keywords,
        "evidence_snippets": evidence_snippets,
        "expected_policy_evidence": expected_policy_evidence,
        "coverage_explanation": explanations.get(coverage_level, ""),
        "review_note": (
            "This is a deterministic keyword-based review of synthetic policy text only. "
            "It is not a legal, compliance, safeguarding, HR, data-protection, or "
            "professional governance assessment."
        ),
    }


def check_policy_pack_coverage(policy_pack: dict, framework: list) -> dict:
    if not isinstance(policy_pack, dict):
        policy_pack = {}
    if not isinstance(framework, list):
        framework = []

    policies = policy_pack.get("policies", []) or []
    org_name = policy_pack.get("organisation_name", "Unknown")
    pack_title = policy_pack.get("policy_pack_title", "Unknown")

    domain_results = [check_domain_coverage(d, policies) for d in framework]

    strong = [d for d in domain_results if d["coverage_level"] == "Strong coverage"]
    partial = [d for d in domain_results if d["coverage_level"] == "Partial coverage"]
    weak = [d for d in domain_results if d["coverage_level"] == "Weak coverage"]
    not_covered = [d for d in domain_results if d["coverage_level"] == "Not covered"]
    high_priority = [d for d in domain_results if d["priority_level"] == "High"]

    overall_score = calculate_coverage_score(domain_results)
    overall_level = classify_coverage_level(overall_score)

    return {
        "organisation_name": org_name,
        "policy_pack_title": pack_title,
        "total_policies_reviewed": len(policies),
        "total_domains_checked": len(domain_results),
        "domain_results": domain_results,
        "overall_coverage_score": overall_score,
        "overall_coverage_level": overall_level,
        "high_priority_domains": [d["domain_name"] for d in high_priority],
        "strong_domains": [d["domain_name"] for d in strong],
        "partial_domains": [d["domain_name"] for d in partial],
        "weak_domains": [d["domain_name"] for d in weak],
        "not_covered_domains": [d["domain_name"] for d in not_covered],
        "responsible_use_note": (
            "This coverage review is generated from synthetic/demo policy text only. "
            "It must not be used with real client policies, learner data, safeguarding "
            "case details, staff HR data, personal data, confidential data, or regulated "
            "information without appropriate governance, approvals, and responsible owners."
        ),
        "prototype_note": (
            "This prototype does not provide legal, safeguarding, HR, compliance, "
            "data-protection, financial, medical, academic-integrity, or professional "
            "governance advice. This is a deterministic keyword-based policy review "
            "support tool, not a compliance certification system."
        ),
    }


def calculate_coverage_score(domain_results: list) -> float:
    if not domain_results:
        return 0.0
    scores = [d.get("coverage_score", 0.0) for d in domain_results]
    return round(sum(scores) / len(scores), 1)


def classify_coverage_level(coverage_score: float) -> str:
    if coverage_score >= 75:
        return "Strong coverage"
    elif coverage_score >= 50:
        return "Partial coverage"
    elif coverage_score >= 25:
        return "Weak coverage"
    else:
        return "Not covered"


def summarise_policy_coverage(coverage_results: dict) -> dict:
    domain_results = coverage_results.get("domain_results", []) or []
    strong = [d for d in domain_results if d["coverage_level"] == "Strong coverage"]
    partial = [d for d in domain_results if d["coverage_level"] == "Partial coverage"]
    weak = [d for d in domain_results if d["coverage_level"] == "Weak coverage"]
    not_covered = [d for d in domain_results if d["coverage_level"] == "Not covered"]

    high_priority_gaps = [
        d["domain_name"]
        for d in domain_results
        if d["priority_level"] == "High"
        and d["coverage_level"] in ("Not covered", "Weak coverage")
    ]

    sorted_asc = sorted(domain_results, key=lambda d: d.get("coverage_score", 0))
    sorted_desc = list(reversed(sorted_asc))
    best_covered = [d["domain_name"] for d in sorted_desc[:3]]
    weakest = [d["domain_name"] for d in sorted_asc[:3]]

    recommended_focus: list = []
    if not_covered:
        recommended_focus.append("Address domains with no coverage as a priority.")
    if high_priority_gaps:
        recommended_focus.append(
            "Strengthen high-priority domains with weak or no coverage."
        )
    if any("Learner" in d["domain_name"] for d in weak + not_covered):
        recommended_focus.append("Clarify learner/client data boundaries.")
    if any("Safeguarding" in d["domain_name"] for d in weak + not_covered):
        recommended_focus.append(
            "Clarify safeguarding boundaries and escalation routes."
        )
    if any("Approved" in d["domain_name"] for d in weak + not_covered):
        recommended_focus.append("Define approved and prohibited AI use cases.")
    if any("Human Review" in d["domain_name"] for d in weak + not_covered):
        recommended_focus.append("Add human review and accountability requirements.")
    if any("Escalation" in d["domain_name"] for d in weak + not_covered):
        recommended_focus.append("Add incident and near-miss reporting routes.")
    if not recommended_focus:
        recommended_focus.append(
            "Review partial coverage areas for clarity and completeness."
        )

    return {
        "overall_coverage_score": coverage_results.get("overall_coverage_score", 0.0),
        "overall_coverage_level": coverage_results.get("overall_coverage_level", ""),
        "total_domains": len(domain_results),
        "strong_count": len(strong),
        "partial_count": len(partial),
        "weak_count": len(weak),
        "not_covered_count": len(not_covered),
        "high_priority_gaps": high_priority_gaps,
        "best_covered_domains": best_covered,
        "weakest_domains": weakest,
        "recommended_focus": recommended_focus,
    }


def format_policy_coverage_as_markdown(
    coverage_results: dict, summary: dict | None = None
) -> str:
    if summary is None:
        summary = summarise_policy_coverage(coverage_results)

    lines = [
        "# AI Governance Policy Coverage Review",
        "",
        "## Review Overview",
        "",
        f"**Organisation:** {coverage_results.get('organisation_name', '')}",
        f"**Policy Pack:** {coverage_results.get('policy_pack_title', '')}",
        f"**Policies reviewed:** {coverage_results.get('total_policies_reviewed', 0)}",
        f"**Governance domains checked:** {coverage_results.get('total_domains_checked', 0)}",
        "",
        "---",
        "",
        "## Overall Coverage Summary",
        "",
        f"**Overall coverage score:** {summary.get('overall_coverage_score', 0)}/100",
        f"**Overall coverage level:** {summary.get('overall_coverage_level', '')}",
        "",
        "---",
        "",
        "## Coverage Counts",
        "",
        "| Coverage Level | Count |",
        "|---|---|",
        f"| Strong coverage | {summary.get('strong_count', 0)} |",
        f"| Partial coverage | {summary.get('partial_count', 0)} |",
        f"| Weak coverage | {summary.get('weak_count', 0)} |",
        f"| Not covered | {summary.get('not_covered_count', 0)} |",
        "",
        "---",
        "",
        "## High-Priority Gaps",
        "",
    ]
    gaps = summary.get("high_priority_gaps", [])
    if gaps:
        lines.extend(f"- {g}" for g in gaps)
    else:
        lines.append("No high-priority gaps identified.")

    lines.extend([
        "",
        "---",
        "",
        "## Best-Covered Domains",
        "",
    ])
    lines.extend(f"- {d}" for d in summary.get("best_covered_domains", []))

    lines.extend([
        "",
        "---",
        "",
        "## Weakest Domains",
        "",
    ])
    lines.extend(f"- {d}" for d in summary.get("weakest_domains", []))

    lines.extend([
        "",
        "---",
        "",
        "## Recommended Focus Areas",
        "",
    ])
    lines.extend(f"- {f}" for f in summary.get("recommended_focus", []))

    lines.extend([
        "",
        "---",
        "",
        "## Domain-by-Domain Coverage Review",
        "",
    ])

    for result in coverage_results.get("domain_results", []):
        lines.append(
            f"### {result.get('domain_id', '')}: {result.get('domain_name', '')}"
        )
        lines.append(f"**Priority:** {result.get('priority_level', '')}  ")
        lines.append(f"**Coverage score:** {result.get('coverage_score', 0)}/100  ")
        lines.append(f"**Coverage level:** {result.get('coverage_level', '')}  ")
        lines.append("")

        matched = result.get("matched_policies", [])
        lines.append(
            f"**Matched policies:** {', '.join(matched)}" if matched
            else "**Matched policies:** None"
        )
        lines.append("")

        keywords = result.get("matched_keywords", [])
        lines.append(
            f"**Matched keywords:** {', '.join(keywords[:10])}" if keywords
            else "**Matched keywords:** None"
        )
        lines.append("")

        snippets = result.get("evidence_snippets", [])
        if snippets:
            lines.append("**Evidence snippets:**")
            lines.extend(f"> {s}" for s in snippets)
            lines.append("")

        lines.append(f"**Coverage explanation:** {result.get('coverage_explanation', '')}")
        lines.append("")
        lines.append(f"*{result.get('review_note', '')}*")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend([
        "## Responsible-Use Boundaries",
        "",
        coverage_results.get("responsible_use_note", ""),
        "",
        coverage_results.get("prototype_note", ""),
        "",
        "Human review remains required before any real-world use.",
        "",
        "---",
        "",
        "*Build 6 · AI Governance Policy Checker · BrightPath ChatGPT Mastery Project*",
        "*Synthetic scenarios only. Human review required before any real-world use.*",
    ])

    return "\n".join(lines)
