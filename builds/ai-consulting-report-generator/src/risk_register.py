"""Risk register generator — Build 5, Phase 3.

Converts synthetic audit risk findings into a structured AI risk register
with likelihood/impact scoring, risk level classification, recommended controls,
owner suggestions, and Markdown export.

All content is deterministic and template-based — no external AI calls.
All data is synthetic. No real client, learner, HR, or personal data.
"""

# ── Score normalisation ────────────────────────────────────────────────────────

_TEXT_TO_SCORE = {
    "very low": 1,
    "very_low": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "very high": 5,
    "very_high": 5,
    "critical": 5,  # treat Critical impact as Very high for numeric scoring
}

_DEFAULT_SCORE = 3  # Medium


def normalise_risk_score(value) -> int:
    """Convert a likelihood or impact value to an integer 1–5.

    Accepts string labels (e.g. 'High'), numeric values, or None.
    Defaults to 3 (Medium) for missing or unrecognised values.
    """
    if value is None:
        return _DEFAULT_SCORE
    if isinstance(value, (int, float)):
        score = int(round(value))
        return max(1, min(5, score))
    if isinstance(value, str):
        normalised = value.strip().lower()
        if normalised in _TEXT_TO_SCORE:
            return _TEXT_TO_SCORE[normalised]
    return _DEFAULT_SCORE


def calculate_risk_score(likelihood, impact) -> int:
    """Return risk_score = likelihood_score * impact_score (range 1–25)."""
    return normalise_risk_score(likelihood) * normalise_risk_score(impact)


# ── Risk level classification ──────────────────────────────────────────────────

def classify_risk_level(risk_score: int) -> str:
    """Classify a numeric risk score into a risk level string.

    1–4:   Low
    5–9:   Medium
    10–16: High
    17–25: Critical
    """
    if risk_score <= 4:
        return "Low"
    if risk_score <= 9:
        return "Medium"
    if risk_score <= 16:
        return "High"
    return "Critical"


_LEVEL_DESCRIPTIONS = {
    "Critical": (
        "Immediate action required. This risk could cause significant harm, compliance breach, "
        "or reputational damage if not addressed before AI adoption continues."
    ),
    "High": (
        "Priority risk requiring action before scaling AI use or running wider pilots. "
        "Controls should be in place and monitored closely."
    ),
    "Medium": (
        "Manageable risk that can be addressed through policy, training, monitoring, and review. "
        "Should not be ignored but need not block early pilots."
    ),
    "Low": (
        "Low risk at this stage. Monitor periodically and review if the organisational "
        "context changes or AI use scales."
    ),
}

_LEVEL_COLOURS = {
    "Critical": "#dc2626",
    "High": "#ea580c",
    "Medium": "#ca8a04",
    "Low": "#16a34a",
}


def get_risk_level_description(risk_level: str) -> str:
    """Return a description of what the risk level means in practice."""
    return _LEVEL_DESCRIPTIONS.get(risk_level, "Risk level not recognised.")


def get_risk_level_colour(risk_level: str) -> str:
    """Return a hex colour for the risk level for UI display."""
    return _LEVEL_COLOURS.get(risk_level, "#64748b")


# ── Risk ID ────────────────────────────────────────────────────────────────────

def generate_risk_id(index: int) -> str:
    """Return a formatted risk ID, e.g. RISK-001."""
    return f"RISK-{index + 1:03d}"


# ── Control recommendations ────────────────────────────────────────────────────

_CONTROL_BY_CATEGORY = {
    "data protection": (
        "Define what data can and cannot be used with AI tools. Require only approved systems. "
        "Minimise data entry, remove identifiers where possible, and escalate any uncertainty "
        "to the data protection lead."
    ),
    "safeguarding": (
        "Do not enter safeguarding case details into AI tools under any circumstances. "
        "Keep all safeguarding decisions human-led and require escalation to the "
        "designated safeguarding lead."
    ),
    "accuracy and hallucination": (
        "Require human review, source checking, and clear labelling of all AI-assisted "
        "drafts before use. Do not publish AI-generated content without expert verification."
    ),
    "quality and accuracy": (
        "Require human review, source checking, and clear labelling of all AI-assisted "
        "content before use. Include a review checklist in the AI policy."
    ),
    "bias and fairness": (
        "Review AI-generated outputs for language bias, cultural assumptions, and "
        "demographic fairness before use. Assign a responsible owner to monitor outputs."
    ),
    "staff misuse": (
        "Create acceptable-use guidance, provide training, define prohibited use cases, "
        "and assign managers to review AI adoption across teams."
    ),
    "approved tools": (
        "Clarify which tools are approved for organisational use. Block or discourage "
        "personal accounts for work data. Define a procurement and review route for "
        "any new AI tool."
    ),
    "governance": (
        "Establish an AI use policy, an approved tools list, and a responsible-owner "
        "framework before extending AI use across the organisation."
    ),
    "accountability": (
        "Assign responsible owners for AI-assisted outputs. Require human sign-off "
        "for all decisions and external-facing materials."
    ),
    "cyber/security": (
        "Review data flows into AI tools. Ensure no sensitive system credentials, "
        "API keys, or infrastructure details are entered into external AI tools."
    ),
    "copyright/ip": (
        "Clarify ownership of AI-generated content with legal or policy owner. "
        "Avoid submitting proprietary content or third-party IP into external AI tools."
    ),
    "operational change": (
        "Communicate changes to AI use clearly and in advance. Provide training and "
        "support to affected teams. Monitor adoption and gather feedback."
    ),
    "training and adoption": (
        "Develop role-specific AI training and responsible-use guidance. Assign a "
        "training lead and schedule training before AI pilots begin."
    ),
    "operational": (
        "Communicate AI adoption plans clearly across all departments. Provide "
        "awareness training and consistent guidance to prevent uneven adoption."
    ),
}

_DEFAULT_CONTROL = (
    "Identify the responsible owner, document the risk, and establish a review schedule. "
    "Define clear controls in the AI use policy before wider adoption."
)


def generate_risk_control_recommendation(risk: dict) -> str:
    """Return a deterministic recommended control based on risk category."""
    category = str(risk.get("risk_category", "")).strip().lower()
    return _CONTROL_BY_CATEGORY.get(category, _DEFAULT_CONTROL)


# ── Owner suggestions ──────────────────────────────────────────────────────────

_OWNER_BY_CATEGORY = {
    "data protection": "Data Protection Lead / DPO / Manager",
    "safeguarding": "Designated Safeguarding Lead",
    "staff misuse": "Team Leaders / Manager",
    "accuracy and hallucination": "Quality Lead / Manager",
    "quality and accuracy": "Quality Lead / Manager",
    "bias and fairness": "Quality Lead / Equality Lead / Manager",
    "approved tools": "IT Lead / AI Governance Owner / Manager",
    "governance": "Senior Leadership Team / AI Governance Owner",
    "accountability": "Senior Responsible Owner / Manager",
    "cyber/security": "IT Lead / Information Security Manager",
    "copyright/ip": "Policy Owner / Manager",
    "operational change": "Operations Lead / Manager",
    "training and adoption": "Learning and Development Lead / Manager",
    "operational": "Operations Lead / All Department Heads",
}

_DEFAULT_OWNER = "Responsible Manager / AI Governance Owner"


def generate_risk_owner_suggestion(risk: dict) -> str:
    """Return a suggested owner based on risk category."""
    category = str(risk.get("risk_category", "")).strip().lower()
    return _OWNER_BY_CATEGORY.get(category, _DEFAULT_OWNER)


# ── Priority action and review frequency ──────────────────────────────────────

_PRIORITY_ACTIONS = {
    "Critical": "Immediate management review required before wider AI use.",
    "High": "Address before scaling AI adoption or running wider pilots.",
    "Medium": "Manage through policy, training, monitoring, and review.",
    "Low": "Monitor and review periodically.",
}

_REVIEW_FREQUENCIES = {
    "Critical": "Weekly until reduced",
    "High": "Monthly",
    "Medium": "Quarterly",
    "Low": "Every 6 months",
}


def _get_priority_action(risk_level: str) -> str:
    return _PRIORITY_ACTIONS.get(risk_level, "Review and document.")


def _get_review_frequency(risk_level: str) -> str:
    return _REVIEW_FREQUENCIES.get(risk_level, "Quarterly")


# ── Risk register generation ───────────────────────────────────────────────────

def generate_risk_register(audit_data: dict) -> list:
    """Build a structured risk register from audit risk findings.

    Returns a list of risk dicts with scoring, levels, controls, and owners.
    Returns an empty list if risk_findings is missing or empty.
    """
    risk_findings = audit_data.get("risk_findings", [])
    if not risk_findings:
        return []

    register = []
    for i, finding in enumerate(risk_findings):
        likelihood = finding.get("likelihood") or "Medium"
        impact = finding.get("impact") or "Medium"
        likelihood_score = normalise_risk_score(likelihood)
        impact_score = normalise_risk_score(impact)
        risk_score = likelihood_score * impact_score
        risk_level = classify_risk_level(risk_score)

        recommended_control = finding.get("recommended_control") or generate_risk_control_recommendation(finding)
        owner = finding.get("owner") or generate_risk_owner_suggestion(finding)

        register.append({
            "risk_id": generate_risk_id(i),
            "risk_title": finding.get("risk_title") or f"Risk {i + 1}",
            "risk_category": finding.get("risk_category") or "General",
            "description": finding.get("description") or "",
            "likelihood": str(likelihood),
            "impact": str(impact),
            "likelihood_score": likelihood_score,
            "impact_score": impact_score,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_level_description": get_risk_level_description(risk_level),
            "recommended_control": recommended_control,
            "owner": owner,
            "priority_action": _get_priority_action(risk_level),
            "review_frequency": _get_review_frequency(risk_level),
            "status": "Open",
            "source": "Synthetic audit finding",
        })

    return register


# ── Risk register summary ──────────────────────────────────────────────────────

def summarise_risk_register(risk_register: list) -> dict:
    """Return a high-level summary dict of the risk register."""
    if not risk_register:
        return {
            "total_risks": 0,
            "critical_risks": 0,
            "high_risks": 0,
            "medium_risks": 0,
            "low_risks": 0,
            "highest_risk": {},
            "top_risk_categories": [],
            "overall_risk_position": "No risk data available for this audit.",
            "recommended_focus": ["Load audit data to generate a risk register."],
        }

    critical = [r for r in risk_register if r.get("risk_level") == "Critical"]
    high = [r for r in risk_register if r.get("risk_level") == "High"]
    medium = [r for r in risk_register if r.get("risk_level") == "Medium"]
    low = [r for r in risk_register if r.get("risk_level") == "Low"]

    highest = max(risk_register, key=lambda r: r.get("risk_score", 0))

    category_counts: dict = {}
    for r in risk_register:
        cat = r.get("risk_category", "General")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    top_categories = sorted(
        category_counts.keys(),
        key=lambda c: category_counts[c],
        reverse=True,
    )[:3]

    if critical or high:
        position = (
            "The organisation should address priority AI governance, data, safeguarding, "
            "and human-review controls before scaling AI use."
        )
    elif medium:
        position = (
            "The organisation can consider controlled pilots, but should strengthen "
            "guidance, training, and monitoring."
        )
    else:
        position = (
            "The organisation appears to have manageable risk exposure, subject to "
            "continued review and responsible-owner oversight."
        )

    focus = []
    if critical:
        focus.append(
            f"Address {len(critical)} critical risk(s) immediately before wider AI adoption."
        )
    if high:
        focus.append(f"Resolve {len(high)} high risk(s) before scaling AI pilots.")
    if any(r.get("risk_category", "").lower() == "data protection" for r in critical + high):
        focus.append("Establish data protection controls and an approved AI use policy.")
    if any(r.get("risk_category", "").lower() == "safeguarding" for r in risk_register):
        focus.append("Brief all staff on safeguarding and AI boundaries.")
    if not focus:
        focus.append("Continue periodic review and monitoring of all risks.")

    return {
        "total_risks": len(risk_register),
        "critical_risks": len(critical),
        "high_risks": len(high),
        "medium_risks": len(medium),
        "low_risks": len(low),
        "highest_risk": highest,
        "top_risk_categories": top_categories,
        "overall_risk_position": position,
        "recommended_focus": focus,
    }


# ── Prioritise risks ───────────────────────────────────────────────────────────

def prioritise_risks(risk_register: list) -> list:
    """Return risk register sorted by risk_score descending (highest first)."""
    return sorted(risk_register, key=lambda r: r.get("risk_score", 0), reverse=True)


# ── Markdown export ────────────────────────────────────────────────────────────

def format_risk_register_as_markdown(
    risk_register: list,
    summary: dict | None = None,
) -> str:
    """Return the full risk register as a Markdown document."""
    lines = ["# AI Risk Register", ""]

    # Risk Summary
    lines += ["## Risk Summary", ""]
    if summary:
        lines += [
            f"- **Total risks:** {summary['total_risks']}",
            f"- **Critical:** {summary['critical_risks']}",
            f"- **High:** {summary['high_risks']}",
            f"- **Medium:** {summary['medium_risks']}",
            f"- **Low:** {summary['low_risks']}",
            "",
        ]
    else:
        lines += ["No summary available.", ""]

    # Overall Risk Position
    lines += ["## Overall Risk Position", ""]
    if summary:
        lines += [summary.get("overall_risk_position", ""), ""]
    else:
        lines += ["", ""]

    # Recommended Focus Areas
    lines += ["## Recommended Focus Areas", ""]
    if summary:
        for item in summary.get("recommended_focus", []):
            lines.append(f"- {item}")
        lines.append("")
    else:
        lines += ["", ""]

    # Risk Register Table
    lines += [
        "## Risk Register Table",
        "",
        "| ID | Risk | Category | Likelihood | Impact | Score | Level | Owner |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in risk_register:
        lines.append(
            f"| {r['risk_id']} | {r['risk_title']} | {r['risk_category']} | "
            f"{r['likelihood']} | {r['impact']} | {r['risk_score']} | "
            f"{r['risk_level']} | {r['owner']} |"
        )
    lines.append("")

    # Detailed Risk Notes
    lines += ["## Detailed Risk Notes", ""]
    for r in risk_register:
        lines += [
            f"### {r['risk_id']} — {r['risk_title']}",
            "",
            f"**Category:** {r['risk_category']}  ",
            f"**Risk level:** {r['risk_level']} (score: {r['risk_score']}/25)  ",
            (
                f"**Likelihood:** {r['likelihood']} ({r['likelihood_score']}/5) · "
                f"**Impact:** {r['impact']} ({r['impact_score']}/5)"
            ),
            "",
            f"**Description:** {r['description']}",
            "",
            f"**Recommended control:** {r['recommended_control']}",
            "",
            f"**Owner:** {r['owner']}  ",
            f"**Priority action:** {r['priority_action']}  ",
            f"**Review frequency:** {r['review_frequency']}  ",
            f"**Status:** {r['status']}",
            "",
        ]

    # Responsible-Use Boundaries
    lines += [
        "## Responsible-Use Boundaries",
        "",
        (
            "This risk register is generated from synthetic/demo audit data only. "
            "It must not be used with real client records, learner data, safeguarding case details, "
            "staff HR data, personal data, confidential data, or regulated information without "
            "appropriate governance, approvals, and responsible owners."
        ),
        "",
        (
            "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
            "financial, academic-integrity, or professional advice."
        ),
        "",
        "Human review remains required before any real-world use.",
        "",
        "*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*",
        "*All scenarios are synthetic. Outputs require human review before real-world use.*",
    ]

    return "\n".join(lines)
