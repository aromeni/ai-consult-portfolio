def get_responsible_ai_governance_framework() -> list:
    return [
        {
            "domain_id": "GOV-001",
            "domain_name": "Strategy and Ownership",
            "description": (
                "The organisation has a clear AI strategy and designated responsible owners "
                "for AI governance."
            ),
            "why_it_matters": (
                "Without clear ownership and strategic direction, AI use is ungoverned "
                "and accountability gaps emerge."
            ),
            "expected_policy_evidence": [
                "Named AI lead or governance owner",
                "Board or senior leadership approval of AI use",
                "AI strategy or roadmap document",
                "Regular governance review cadence",
            ],
            "example_controls": [
                "Appoint an AI governance lead",
                "Include AI governance in board or SLT agenda",
                "Publish an AI strategy or position statement",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-002",
            "domain_name": "Approved AI Tools",
            "description": (
                "Only approved AI tools are used, and a process exists to evaluate "
                "and approve new tools."
            ),
            "why_it_matters": (
                "Unapproved AI tools may expose the organisation to data protection, "
                "security, and governance risks."
            ),
            "expected_policy_evidence": [
                "Approved AI tools list",
                "Tool approval process or procedure",
                "Records of approved and rejected tools",
                "Regular review of the approved tools list",
            ],
            "example_controls": [
                "Maintain a published approved AI tools register",
                "Require data protection review before tool approval",
                "Include supplier contracts and data processing terms",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-003",
            "domain_name": "Prohibited AI Uses",
            "description": (
                "Clear prohibitions exist on harmful, inappropriate, or high-risk AI uses."
            ),
            "why_it_matters": (
                "Without explicit prohibitions, staff may unknowingly use AI in contexts "
                "where the risk is unacceptable."
            ),
            "expected_policy_evidence": [
                "Explicit list of prohibited AI uses",
                "Examples of prohibited use cases",
                "Consequences for breaching prohibitions",
                "Communication to all staff",
            ],
            "example_controls": [
                "List specific prohibited use cases in policy",
                "Include prohibited uses in staff training",
                "Include in disciplinary procedure where relevant",
            ],
            "priority_level": "Medium",
        },
        {
            "domain_id": "GOV-004",
            "domain_name": "Data Protection and Confidentiality",
            "description": (
                "AI use complies with data protection obligations and confidential data "
                "is protected."
            ),
            "why_it_matters": (
                "AI tools pose significant data protection risks if personal or confidential "
                "data is entered or processed without appropriate safeguards."
            ),
            "expected_policy_evidence": [
                "Data protection guidance for AI use",
                "Data minimisation requirements",
                "Approved data processing terms for AI tools",
                "Personal data prohibition in AI interactions",
            ],
            "example_controls": [
                "Prohibit personal data entry into AI tools without approval",
                "Review AI provider data processing terms",
                "Train staff on data minimisation when using AI",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-005",
            "domain_name": "Learner and Client Data Boundaries",
            "description": (
                "Specific protections exist for learner and client data in AI contexts."
            ),
            "why_it_matters": (
                "Learner and client data is often sensitive and subject to specific obligations. "
                "AI tools must not process this data without explicit governance approval."
            ),
            "expected_policy_evidence": [
                "Explicit prohibition on learner/client data in AI tools",
                "Guidance on anonymisation before AI use",
                "Approval process for AI use involving learner/client data",
            ],
            "example_controls": [
                "Explicitly prohibit learner/client data in AI tools",
                "Require data lead approval for any exceptions",
                "Anonymise examples before AI-assisted processing",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-006",
            "domain_name": "Safeguarding Boundaries",
            "description": (
                "AI is explicitly excluded from safeguarding decisions and safeguarding data."
            ),
            "why_it_matters": (
                "Safeguarding decisions require qualified human judgement. AI involvement "
                "in safeguarding contexts creates serious risk of harm."
            ),
            "expected_policy_evidence": [
                "Explicit prohibition on AI in safeguarding decisions",
                "Prohibition on AI access to safeguarding case records",
                "Designated Safeguarding Lead confirmation of boundaries",
                "Staff training on safeguarding and AI",
            ],
            "example_controls": [
                "Explicitly prohibit AI from safeguarding decision-making",
                "Exclude safeguarding records from AI-accessible systems",
                "Include in DSL responsibilities",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-007",
            "domain_name": "Human Review and Accountability",
            "description": (
                "All consequential AI outputs are reviewed by a qualified human before use."
            ),
            "why_it_matters": (
                "AI systems can produce errors, hallucinations, and biased outputs. "
                "Human review is essential before any AI output is used consequentially."
            ),
            "expected_policy_evidence": [
                "Human review requirement in policy",
                "Named accountable reviewer for AI outputs",
                "Checklist or procedure for AI output review",
                "Disclosure requirements for AI-assisted outputs",
            ],
            "example_controls": [
                "Require human sign-off before using AI outputs",
                "Publish an AI output review checklist",
                "Require disclosure when AI is used in professional outputs",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-008",
            "domain_name": "Accuracy and Hallucination Control",
            "description": (
                "Risks of AI inaccuracy and hallucination are understood and managed."
            ),
            "why_it_matters": (
                "Generative AI can produce plausible but false information. Without checks, "
                "inaccurate AI outputs may be used in professional or learner-facing contexts."
            ),
            "expected_policy_evidence": [
                "Guidance on verifying AI outputs",
                "Prohibition on unverified AI-generated facts",
                "Staff training on hallucination risk",
                "Review checklist addressing accuracy",
            ],
            "example_controls": [
                "Include accuracy verification in AI output review checklist",
                "Train staff on hallucination risk",
                "Prohibit citation of AI-generated statistics without verification",
            ],
            "priority_level": "Medium",
        },
        {
            "domain_id": "GOV-009",
            "domain_name": "Bias, Fairness, and Inclusion",
            "description": (
                "AI use does not introduce or amplify bias, and outputs are fair to all "
                "learners and clients."
            ),
            "why_it_matters": (
                "AI systems can reflect and amplify historical biases. This poses equality "
                "and inclusion risks, particularly in learner-facing and assessment contexts."
            ),
            "expected_policy_evidence": [
                "Bias awareness in policy or guidance",
                "Fairness check in AI output review",
                "Equality considerations in AI tool approval",
                "Training on bias and fairness risks",
            ],
            "example_controls": [
                "Include bias check in AI output review checklist",
                "Assess equality impact before deploying AI in learner-facing contexts",
                "Train staff on bias risks in generative AI",
            ],
            "priority_level": "Medium",
        },
        {
            "domain_id": "GOV-010",
            "domain_name": "Staff Training and Capability",
            "description": (
                "Staff are trained to use AI tools responsibly and to understand their "
                "limitations."
            ),
            "why_it_matters": (
                "Without training, staff may misuse AI tools, fail to recognise errors, "
                "or inadvertently breach data protection or safeguarding boundaries."
            ),
            "expected_policy_evidence": [
                "Mandatory AI awareness training requirement",
                "Training completion records",
                "Training content covering responsible AI use",
                "Refresher training schedule",
            ],
            "example_controls": [
                "Make AI awareness training mandatory before tool use",
                "Include training on data protection, hallucination, and safeguarding",
                "Keep training records and review annually",
            ],
            "priority_level": "Medium",
        },
        {
            "domain_id": "GOV-011",
            "domain_name": "Escalation and Incident Reporting",
            "description": (
                "A clear procedure exists for reporting and escalating AI-related incidents "
                "and near-misses."
            ),
            "why_it_matters": (
                "AI incidents and near-misses provide critical learning. Without a reporting "
                "procedure, risks remain hidden and repeat incidents are more likely."
            ),
            "expected_policy_evidence": [
                "AI incident reporting procedure",
                "Named escalation contacts",
                "Near-miss reporting encouraged",
                "Incident log maintained",
            ],
            "example_controls": [
                "Publish an AI incident and escalation procedure",
                "Name the escalation contacts for different incident types",
                "Maintain an AI incident log",
                "Report on incidents at governance meetings",
            ],
            "priority_level": "High",
        },
        {
            "domain_id": "GOV-012",
            "domain_name": "Monitoring, Review, and Continuous Improvement",
            "description": (
                "AI governance is subject to regular monitoring and review, and improvements "
                "are made over time."
            ),
            "why_it_matters": (
                "AI tools and risks evolve rapidly. Governance must be reviewed regularly "
                "to remain current and effective."
            ),
            "expected_policy_evidence": [
                "Annual policy review commitment",
                "Governance review meeting cadence",
                "Mechanism for triggering unplanned review",
                "Lessons learned process",
            ],
            "example_controls": [
                "Schedule annual AI policy review",
                "Include AI governance in quarterly SLT agenda",
                "Trigger review after any significant incident",
                "Publish and share lessons learned from incidents",
            ],
            "priority_level": "Medium",
        },
    ]


def get_framework_domain_ids() -> list:
    return [d["domain_id"] for d in get_responsible_ai_governance_framework()]


def get_framework_domain_names() -> list:
    return [d["domain_name"] for d in get_responsible_ai_governance_framework()]


def get_high_priority_domains() -> list:
    return [
        d for d in get_responsible_ai_governance_framework()
        if d["priority_level"] == "High"
    ]


def summarise_governance_framework(framework: list) -> dict:
    priority_counts: dict = {}
    for d in framework:
        p = d.get("priority_level", "Unknown")
        priority_counts[p] = priority_counts.get(p, 0) + 1
    return {
        "total_domains": len(framework),
        "high_priority_count": priority_counts.get("High", 0),
        "medium_priority_count": priority_counts.get("Medium", 0),
        "low_priority_count": priority_counts.get("Low", 0),
        "domain_names": [d["domain_name"] for d in framework],
        "domain_ids": [d["domain_id"] for d in framework],
    }


def format_governance_framework_as_markdown(framework: list) -> str:
    lines = [
        "# Responsible AI Governance Framework",
        "",
        "**BrightPath Skills Training — Synthetic Demo**",
        "",
        f"Total governance domains: {len(framework)}",
        "",
        "---",
        "",
    ]
    for domain in framework:
        lines.append(f"## {domain['domain_id']}: {domain['domain_name']}")
        lines.append(f"**Priority:** {domain['priority_level']}")
        lines.append("")
        lines.append(domain["description"])
        lines.append("")
        lines.append(f"**Why it matters:** {domain['why_it_matters']}")
        lines.append("")
        lines.append("**Expected policy evidence:**")
        for item in domain.get("expected_policy_evidence", []):
            lines.append(f"- {item}")
        lines.append("")
        lines.append("**Example controls:**")
        for item in domain.get("example_controls", []):
            lines.append(f"- {item}")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append(
        "*This governance framework is synthetic/demo content for portfolio demonstration only.*"
    )
    lines.append("*Human review is required before any real-world use.*")
    return "\n".join(lines)
