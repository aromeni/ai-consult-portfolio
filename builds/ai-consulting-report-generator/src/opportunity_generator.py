"""Opportunity and Pilot Recommendation Generator — Build 5.

Converts synthetic audit workflow findings and pilot recommendations into a
client-facing AI opportunity portfolio with scoring, sequencing, and
responsible-use controls.

All data is synthetic. No external AI calls. Deterministic and template-based.
"""

_TEXT_TO_INT = {
    "very low": 1,
    "very_low": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "very high": 5,
    "very_high": 5,
}

_INT_TO_TEXT = {1: "Very low", 2: "Low", 3: "Medium", 4: "High", 5: "Very high"}

_DEFAULT_INT = 3

_PRIORITY_COLOURS = {
    "Strategic priority": "#7c3aed",
    "High priority": "#ea580c",
    "Medium priority": "#ca8a04",
    "Low priority": "#16a34a",
}

# Keyword-keyed recommended actions — ordered from most specific to least
_RECOMMENDED_ACTIONS = {
    "lesson plan": (
        "Start with a controlled pilot using generic lesson topics only. "
        "Require all tutors to review and sign off AI-generated materials before learner delivery. "
        "Use only approved tools and synthetic content. "
        "Do not enter learner names, IDs, or records into any AI tool."
    ),
    "email": (
        "Use AI only for generic wording improvements or approved templates. "
        "Do not include learner names, personal data, HR data, or confidential details in any prompt. "
        "All templates must be reviewed and approved by a named responsible owner before use."
    ),
    "safeguard": (
        "AI must not be used for any safeguarding concern, disclosure, or decision. "
        "Follow the organisation's designated safeguarding escalation route at all times. "
        "Include explicit prohibition in the AI use policy."
    ),
    "quality": (
        "Introduce an AI use policy and use log before any AI-assisted quality or compliance work begins. "
        "Use only approved internal documents as inputs. "
        "Require the Quality Lead to review and approve all AI outputs before use."
    ),
    "compliance": (
        "Introduce an AI use policy and use log before any AI-assisted compliance work begins. "
        "Use only approved internal documents as inputs. "
        "Require manager review and sign-off before sharing any AI-assisted compliance output."
    ),
    "report": (
        "Use AI for structure and wording support only. "
        "Do not include confidential records, personal data, or learner information in any prompt. "
        "Require manager review and sign-off before sharing any AI-assisted report."
    ),
    "policy": (
        "Use approved synthetic or pre-approved documents only. "
        "Require human review against the original policy document before relying on any AI-generated summary."
    ),
    "document": (
        "Use only approved documents as input. "
        "Treat AI retrieval or summarisation as evidence support only — not final advice. "
        "Require human review before acting on any AI-generated summary."
    ),
    "enquiry": (
        "Draft AI-generated email response templates for common enquiry types. "
        "Review all templates before deployment. "
        "Do not automate any response without a human review step."
    ),
    "admin": (
        "Use AI to draft generic templates only. "
        "Do not include personal data, learner names, or financial information in any prompt. "
        "Review all outputs before sending or publishing."
    ),
    "default": (
        "Identify the responsible owner, define the scope and data boundaries, "
        "and run a small controlled pilot with human review of all outputs before wider adoption."
    ),
}

_STANDARD_PILOT_CONTROLS = [
    "Use synthetic, anonymised, or pre-approved content only.",
    (
        "Do not enter learner names, safeguarding case details, staff HR data, "
        "confidential records, personal data, or regulated information into any AI tool."
    ),
    "Use only approved AI tools with an appropriate Data Processing Agreement.",
    "Require human review and sign-off before any AI-generated output is used or shared.",
    "Define a named responsible owner for this pilot before it begins.",
    "Track issues, errors, time saved, and staff feedback throughout the pilot.",
    (
        "Escalate any safeguarding, data protection, HR, compliance, or accuracy concerns "
        "to the appropriate human owner immediately."
    ),
    "Stop the pilot if risks cannot be adequately controlled.",
]


# ── Core scoring functions ──────────────────────────────────────────────────────

def normalise_priority_value(value) -> int:
    """Convert text or numeric value to an integer 1–5. Defaults to 3 (Medium)."""
    if value is None:
        return _DEFAULT_INT
    if isinstance(value, (int, float)):
        return max(1, min(5, int(round(value))))
    if isinstance(value, str):
        # Strip descriptive text after em-dash or " - " ("High — description")
        clean = value.split("—")[0].split(" - ")[0].strip().lower()
        parts = clean.split()
        # Try two-word match first ("very low", "very high")
        if len(parts) >= 2:
            two_word = f"{parts[0]} {parts[1]}"
            if two_word in _TEXT_TO_INT:
                return _TEXT_TO_INT[two_word]
        # Try single-word match
        if parts and parts[0] in _TEXT_TO_INT:
            return _TEXT_TO_INT[parts[0]]
    return _DEFAULT_INT


def classify_complexity(value) -> str:
    """Return a text label for a complexity value."""
    return _INT_TO_TEXT.get(normalise_priority_value(value), "Medium")


def classify_potential_value(value) -> str:
    """Return a text label for a potential value."""
    return _INT_TO_TEXT.get(normalise_priority_value(value), "Medium")


def classify_pilot_risk(value) -> str:
    """Return a text label for a risk level."""
    return _INT_TO_TEXT.get(normalise_priority_value(value), "Medium")


def calculate_opportunity_score(
    potential_value,
    complexity,
    risk_level,
) -> int:
    """Calculate opportunity score: value*2 - complexity - risk + 10, clamped 0–20."""
    v = normalise_priority_value(potential_value)
    c = normalise_priority_value(complexity)
    r = normalise_priority_value(risk_level)
    return max(0, min(20, v * 2 - c - r + 10))


def classify_opportunity_priority(score: int) -> str:
    """Classify a 0–20 opportunity score into a priority band."""
    if score <= 6:
        return "Low priority"
    if score <= 12:
        return "Medium priority"
    if score <= 16:
        return "High priority"
    return "Strategic priority"


def generate_opportunity_id(index: int) -> str:
    """Return a zero-padded opportunity ID, e.g. OPP-001."""
    return f"OPP-{index + 1:03d}"


def get_opportunity_priority_colour(priority: str) -> str:
    """Return hex colour for a priority label."""
    return _PRIORITY_COLOURS.get(priority, "#64748b")


# ── Private helpers ─────────────────────────────────────────────────────────────

def _get_recommended_action(workflow_name: str, ai_opportunity: str) -> str:
    combined = f"{workflow_name} {ai_opportunity}".lower()
    for keyword, action in _RECOMMENDED_ACTIONS.items():
        if keyword == "default":
            continue
        if keyword in combined:
            return action
    return _RECOMMENDED_ACTIONS["default"]


def _get_opportunity_success_measures(workflow_name: str) -> list:
    return [
        f"Time saved per week on {workflow_name.lower()} tasks (track before and after the pilot).",
        "Number of AI outputs reviewed and approved before use.",
        "Staff confidence with AI tools — survey before and after the pilot.",
        "Quality issues or corrections identified in AI outputs.",
        "Whether the pilot should stop, continue as-is, or be scaled.",
    ]


# ── Control and success measure generators ──────────────────────────────────────

def generate_responsible_pilot_controls(pilot: dict) -> list:
    """Return responsible-use controls for a pilot or workflow opportunity."""
    name = str(
        pilot.get("pilot_name")
        or pilot.get("workflow_name")
        or "this pilot"
    ).lower()
    controls = list(_STANDARD_PILOT_CONTROLS)
    if "learner" in name or "report" in name:
        controls.insert(
            0,
            "Do not enter learner names, IDs, attendance records, or progress data into any AI tool.",
        )
    if "quality" in name or "compliance" in name:
        controls.insert(
            0,
            "Use only approved internal documents. Do not include confidential learner or staff records.",
        )
    if "safeguard" in name:
        controls.insert(
            0,
            "AI must not be used for any safeguarding concern, disclosure, or decision.",
        )
    return controls


def generate_pilot_success_measures(pilot: dict) -> list:
    """Return combined success measures for a pilot (existing + standard extras)."""
    existing = list(pilot.get("success_measures") or [])
    pilot_name = pilot.get("pilot_name") or "this pilot"
    extras = [
        f"Staff confidence with AI tools in {pilot_name.lower()} before and after pilot (survey).",
        "Number of outputs reviewed and approved before use.",
        "Any incidents, near misses, or data concerns raised during the pilot.",
        "Whether the pilot should stop, continue as-is, or be scaled.",
    ]
    for measure in extras:
        if not any(measure.lower()[:30] in m.lower() for m in existing):
            existing.append(measure)
    return existing


# ── Opportunity and pilot builders ──────────────────────────────────────────────

def generate_opportunity_from_workflow_finding(finding: dict, index: int) -> dict:
    """Build a scored opportunity dict from a single workflow finding."""
    workflow_name = finding.get("workflow_name") or f"Workflow {index + 1}"
    potential_value_raw = finding.get("potential_value") or "Medium"
    risk_level_raw = finding.get("risk_level") or "Medium"
    complexity_raw = finding.get("complexity") or "Medium"

    value_score = normalise_priority_value(potential_value_raw)
    complexity_score = normalise_priority_value(complexity_raw)
    risk_score = normalise_priority_value(risk_level_raw)
    opportunity_score = calculate_opportunity_score(
        potential_value_raw, complexity_raw, risk_level_raw
    )

    recommended_action = finding.get("recommended_action") or _get_recommended_action(
        workflow_name, finding.get("ai_opportunity") or ""
    )

    return {
        "opportunity_id": generate_opportunity_id(index),
        "workflow_name": workflow_name,
        "current_process": finding.get("current_process") or "",
        "pain_points": finding.get("pain_points") or [],
        "ai_opportunity": finding.get("ai_opportunity") or "",
        "potential_value": classify_potential_value(potential_value_raw),
        "complexity": classify_complexity(complexity_raw),
        "risk_level": classify_pilot_risk(risk_level_raw),
        "value_score": value_score,
        "complexity_score": complexity_score,
        "risk_score": risk_score,
        "opportunity_score": opportunity_score,
        "priority": classify_opportunity_priority(opportunity_score),
        "recommended_action": recommended_action,
        "responsible_use_controls": generate_responsible_pilot_controls(finding),
        "success_measures": _get_opportunity_success_measures(workflow_name),
        "source": "Synthetic workflow finding",
    }


def generate_pilot_from_recommendation(pilot: dict, index: int) -> dict:
    """Build a structured pilot dict from a pilot recommendation."""
    pilot_name = pilot.get("pilot_name") or f"Pilot {index + 1}"
    complexity_raw = pilot.get("complexity") or "Medium"
    risk_raw = pilot.get("risk_level") or "Medium"

    # Pilot recommendations don't carry an explicit potential_value; default to Medium
    opportunity_score = calculate_opportunity_score("Medium", complexity_raw, risk_raw)

    return {
        "pilot_id": f"PILOT-{index + 1:03d}",
        "pilot_name": pilot_name,
        "business_problem": pilot.get("business_problem") or "",
        "proposed_solution": pilot.get("proposed_solution") or "",
        "expected_benefits": pilot.get("expected_benefits") or [],
        "complexity": classify_complexity(complexity_raw),
        "risk_level": classify_pilot_risk(risk_raw),
        "suggested_timeline": pilot.get("suggested_timeline") or "Month 1–3",
        "success_measures": generate_pilot_success_measures(pilot),
        "responsible_use_controls": generate_responsible_pilot_controls(pilot),
        "pilot_priority": classify_opportunity_priority(opportunity_score),
        "recommended_scope": (
            f"Small team pilot — 2–4 staff — using approved tools and synthetic content only. "
            f"Human review required for all outputs. "
            f"Timeline: {pilot.get('suggested_timeline') or 'Month 1–3'}."
        ),
        "human_review_requirements": [
            "All AI-generated outputs must be reviewed and approved by a named reviewer before use.",
            "The responsible owner must sign off on the pilot scope before it begins.",
            "Review and sign-off records must be kept for governance and compliance purposes.",
        ],
        "source": "Synthetic pilot recommendation",
    }


# ── Portfolio builders ──────────────────────────────────────────────────────────

def prioritise_opportunities(opportunities: list) -> list:
    """Return opportunities sorted by opportunity_score descending."""
    return sorted(
        opportunities, key=lambda o: o.get("opportunity_score", 0), reverse=True
    )


def prioritise_pilots(pilots: list) -> list:
    """Return pilots sorted by combined complexity + risk ascending (safest first)."""
    def _sort_key(p):
        return normalise_priority_value(
            p.get("complexity", "Medium")
        ) + normalise_priority_value(p.get("risk_level", "Medium"))

    return sorted(pilots, key=_sort_key)


def generate_ai_opportunity_portfolio(audit_data: dict) -> dict:
    """Build the full AI opportunity portfolio from audit data."""
    if not audit_data:
        return _empty_portfolio("Unnamed organisation")

    org_name = (
        audit_data.get("organisation_profile", {}).get("organisation_name")
        or "Unnamed organisation"
    )

    workflow_findings = audit_data.get("workflow_findings") or []
    pilot_recs = audit_data.get("pilot_recommendations") or []

    opportunities = [
        generate_opportunity_from_workflow_finding(f, i)
        for i, f in enumerate(workflow_findings)
    ]
    pilots = [
        generate_pilot_from_recommendation(p, i)
        for i, p in enumerate(pilot_recs)
    ]

    prioritised_opps = prioritise_opportunities(opportunities)
    prioritised_pilots = prioritise_pilots(pilots)

    recommended_first_pilot = prioritised_pilots[0] if prioritised_pilots else {}

    recommended_pilot_sequence = [
        {
            "position": i + 1,
            "pilot_id": p["pilot_id"],
            "pilot_name": p["pilot_name"],
            "suggested_timeline": p["suggested_timeline"],
            "pilot_priority": p["pilot_priority"],
            "complexity": p["complexity"],
            "risk_level": p["risk_level"],
        }
        for i, p in enumerate(prioritised_pilots)
    ]

    portfolio = {
        "organisation_name": org_name,
        "opportunities": prioritised_opps,
        "pilots": prioritised_pilots,
        "recommended_first_pilot": recommended_first_pilot,
        "recommended_pilot_sequence": recommended_pilot_sequence,
        "opportunity_summary": {},
        "responsible_use_note": (
            "This opportunity portfolio is generated from synthetic/demo audit data only. "
            "It must not be used with real client records, learner data, safeguarding case details, "
            "staff HR data, personal data, confidential data, or regulated information without "
            "appropriate governance, approvals, and responsible owners."
        ),
        "prototype_note": (
            "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
            "financial, academic-integrity, or professional advice. "
            "Human review remains required before any real-world use."
        ),
    }
    portfolio["opportunity_summary"] = summarise_opportunity_portfolio(portfolio)
    return portfolio


def _empty_portfolio(org_name: str) -> dict:
    return {
        "organisation_name": org_name,
        "opportunities": [],
        "pilots": [],
        "recommended_first_pilot": {},
        "recommended_pilot_sequence": [],
        "opportunity_summary": {
            "total_opportunities": 0,
            "total_pilots": 0,
            "strategic_priority_opportunities": 0,
            "high_priority_opportunities": 0,
            "medium_priority_opportunities": 0,
            "low_priority_opportunities": 0,
            "recommended_first_pilot_name": "None identified",
            "overall_opportunity_position": "Load audit data to generate an opportunity portfolio.",
            "recommended_focus": ["Load audit data to identify AI opportunities."],
        },
        "responsible_use_note": (
            "This opportunity portfolio is generated from synthetic/demo audit data only."
        ),
        "prototype_note": (
            "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
            "financial, academic-integrity, or professional advice. "
            "Human review remains required before any real-world use."
        ),
    }


def summarise_opportunity_portfolio(portfolio: dict) -> dict:
    """Return a summary dict for the opportunity portfolio."""
    opportunities = portfolio.get("opportunities") or []
    pilots = portfolio.get("pilots") or []

    if not opportunities and not pilots:
        return {
            "total_opportunities": 0,
            "total_pilots": 0,
            "strategic_priority_opportunities": 0,
            "high_priority_opportunities": 0,
            "medium_priority_opportunities": 0,
            "low_priority_opportunities": 0,
            "recommended_first_pilot_name": "None identified",
            "overall_opportunity_position": (
                "Load audit data to generate an opportunity portfolio."
            ),
            "recommended_focus": ["Load audit data to identify AI opportunities."],
        }

    strategic = [o for o in opportunities if o.get("priority") == "Strategic priority"]
    high = [o for o in opportunities if o.get("priority") == "High priority"]
    medium = [o for o in opportunities if o.get("priority") == "Medium priority"]
    low = [o for o in opportunities if o.get("priority") == "Low priority"]

    first_pilot = portfolio.get("recommended_first_pilot") or {}
    first_pilot_name = first_pilot.get("pilot_name") or "None identified"

    if strategic or high:
        position = (
            "The organisation has several promising AI opportunities, but they should be "
            "introduced through controlled pilots with clear data boundaries, human review, "
            "and success measures."
        )
    elif medium:
        position = (
            "The organisation should start with one or two narrow pilots in low-risk workflows "
            "before wider adoption."
        )
    else:
        position = (
            "The organisation should clarify business goals and workflow pain points before "
            "investing heavily in AI pilots."
        )

    focus = []
    if strategic:
        count = len(strategic)
        focus.append(
            f"Prioritise {count} strategic AI {'opportunity' if count == 1 else 'opportunities'} for immediate planning."
        )
    if high:
        count = len(high)
        focus.append(
            f"Progress {count} high-priority {'opportunity' if count == 1 else 'opportunities'} through pilot scoping."
        )
    if medium:
        count = len(medium)
        focus.append(
            f"Plan {count} medium-priority {'opportunity' if count == 1 else 'opportunities'} for structured pilots."
        )
    pilot_names = [p.get("pilot_name", "") for p in pilots[:2] if p.get("pilot_name")]
    if pilot_names:
        focus.append(f"Start with a controlled pilot: {' and '.join(pilot_names)}.")
    focus.append(
        "Establish responsible-use controls and success measures before any pilot begins."
    )
    focus.append(
        "Review all AI outputs before use and track results throughout each pilot."
    )

    return {
        "total_opportunities": len(opportunities),
        "total_pilots": len(pilots),
        "strategic_priority_opportunities": len(strategic),
        "high_priority_opportunities": len(high),
        "medium_priority_opportunities": len(medium),
        "low_priority_opportunities": len(low),
        "recommended_first_pilot_name": first_pilot_name,
        "overall_opportunity_position": position,
        "recommended_focus": focus,
    }


# ── Markdown formatter ──────────────────────────────────────────────────────────

def format_opportunity_portfolio_as_markdown(
    portfolio: dict,
    summary: dict | None = None,
) -> str:
    """Format the opportunity portfolio as a client-facing Markdown document."""
    org = portfolio.get("organisation_name") or "Unnamed organisation"
    opportunities = portfolio.get("opportunities") or []
    pilots = portfolio.get("pilots") or []
    first_pilot = portfolio.get("recommended_first_pilot") or {}
    sequence = portfolio.get("recommended_pilot_sequence") or []

    if summary is None:
        summary = summarise_opportunity_portfolio(portfolio)

    lines = [
        "# AI Opportunity and Pilot Recommendation Portfolio",
        "",
        f"**Organisation:** {org}",
        "",
        "---",
        "",
        "## Opportunity Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total AI opportunities identified | {summary.get('total_opportunities', 0)} |",
        f"| Total pilots recommended | {summary.get('total_pilots', 0)} |",
        f"| Strategic priority opportunities | {summary.get('strategic_priority_opportunities', 0)} |",
        f"| High priority opportunities | {summary.get('high_priority_opportunities', 0)} |",
        f"| Medium priority opportunities | {summary.get('medium_priority_opportunities', 0)} |",
        f"| Low priority opportunities | {summary.get('low_priority_opportunities', 0)} |",
        f"| Recommended first pilot | {summary.get('recommended_first_pilot_name', '—')} |",
        "",
        "---",
        "",
        "## Overall Opportunity Position",
        "",
        summary.get("overall_opportunity_position", ""),
        "",
        "---",
        "",
        "## Recommended Focus Areas",
        "",
    ]
    for item in summary.get("recommended_focus") or []:
        lines.append(f"- {item}")
    lines += ["", "---", "", "## Recommended First Pilot", ""]

    if first_pilot:
        lines += [
            f"**{first_pilot.get('pilot_name', '—')}**",
            "",
            f"- **Pilot ID:** {first_pilot.get('pilot_id', '—')}",
            f"- **Complexity:** {first_pilot.get('complexity', '—')}",
            f"- **Risk level:** {first_pilot.get('risk_level', '—')}",
            f"- **Suggested timeline:** {first_pilot.get('suggested_timeline', '—')}",
            f"- **Priority:** {first_pilot.get('pilot_priority', '—')}",
        ]
    else:
        lines.append("No pilots identified.")

    lines += ["", "---", "", "## Recommended Pilot Sequence", ""]
    if sequence:
        lines += [
            "| # | Pilot | Timeline | Priority | Complexity | Risk |",
            "|---|---|---|---|---|---|",
        ]
        for item in sequence:
            lines.append(
                f"| {item.get('position', '')} "
                f"| {item.get('pilot_name', '—')} "
                f"| {item.get('suggested_timeline', '—')} "
                f"| {item.get('pilot_priority', '—')} "
                f"| {item.get('complexity', '—')} "
                f"| {item.get('risk_level', '—')} |"
            )
    else:
        lines.append("No pilot sequence generated.")

    lines += ["", "---", "", "## AI Opportunity Table", ""]
    if opportunities:
        lines += [
            "| ID | Workflow | Value | Complexity | Risk | Score | Priority |",
            "|---|---|---|---|---|---|---|",
        ]
        for o in opportunities:
            lines.append(
                f"| {o.get('opportunity_id', '—')} "
                f"| {o.get('workflow_name', '—')} "
                f"| {o.get('potential_value', '—')} "
                f"| {o.get('complexity', '—')} "
                f"| {o.get('risk_level', '—')} "
                f"| {o.get('opportunity_score', '—')}/20 "
                f"| {o.get('priority', '—')} |"
            )
    else:
        lines.append("No opportunities identified.")

    lines += ["", "---", "", "## Pilot Recommendation Table", ""]
    if pilots:
        lines += [
            "| Pilot ID | Pilot Name | Complexity | Risk | Timeline | Priority |",
            "|---|---|---|---|---|---|",
        ]
        for p in pilots:
            lines.append(
                f"| {p.get('pilot_id', '—')} "
                f"| {p.get('pilot_name', '—')} "
                f"| {p.get('complexity', '—')} "
                f"| {p.get('risk_level', '—')} "
                f"| {p.get('suggested_timeline', '—')} "
                f"| {p.get('pilot_priority', '—')} |"
            )
    else:
        lines.append("No pilots identified.")

    lines += ["", "---", "", "## Detailed Opportunity Notes", ""]
    for o in opportunities:
        lines += [
            f"### {o.get('opportunity_id', '—')} — {o.get('workflow_name', '—')}",
            "",
            (
                f"**Priority:** {o.get('priority', '—')} · "
                f"**Score:** {o.get('opportunity_score', '—')}/20 · "
                f"**Value:** {o.get('potential_value', '—')} · "
                f"**Complexity:** {o.get('complexity', '—')} · "
                f"**Risk:** {o.get('risk_level', '—')}"
            ),
            "",
            f"**AI opportunity:** {o.get('ai_opportunity', '')}",
            "",
            f"**Recommended action:** {o.get('recommended_action', '')}",
            "",
        ]
        if o.get("success_measures"):
            lines.append("**Success measures:**")
            for m in o["success_measures"]:
                lines.append(f"- {m}")
            lines.append("")
        if o.get("responsible_use_controls"):
            lines.append("**Responsible-use controls:**")
            for c in o["responsible_use_controls"]:
                lines.append(f"- {c}")
            lines.append("")

    lines += ["---", "", "## Detailed Pilot Notes", ""]
    for p in pilots:
        lines += [
            f"### {p.get('pilot_id', '—')} — {p.get('pilot_name', '—')}",
            "",
            (
                f"**Priority:** {p.get('pilot_priority', '—')} · "
                f"**Complexity:** {p.get('complexity', '—')} · "
                f"**Risk:** {p.get('risk_level', '—')} · "
                f"**Timeline:** {p.get('suggested_timeline', '—')}"
            ),
            "",
            f"**Business problem:** {p.get('business_problem', '')}",
            "",
            f"**Proposed solution:** {p.get('proposed_solution', '')}",
            "",
        ]
        if p.get("expected_benefits"):
            lines.append("**Expected benefits:**")
            for b in p["expected_benefits"]:
                lines.append(f"- {b}")
            lines.append("")
        if p.get("success_measures"):
            lines.append("**Success measures:**")
            for m in p["success_measures"]:
                lines.append(f"- {m}")
            lines.append("")
        if p.get("responsible_use_controls"):
            lines.append("**Responsible-use controls:**")
            for c in p["responsible_use_controls"]:
                lines.append(f"- {c}")
            lines.append("")
        if p.get("human_review_requirements"):
            lines.append("**Human review requirements:**")
            for h in p["human_review_requirements"]:
                lines.append(f"- {h}")
            lines.append("")

    lines += [
        "---",
        "",
        "## Responsible-Use Boundaries",
        "",
        portfolio.get("responsible_use_note", ""),
        "",
        portfolio.get("prototype_note", ""),
        "",
        "---",
        "",
        "*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*",
        "*All scenarios are synthetic. Outputs require human review before real-world use.*",
    ]

    return "\n".join(lines)
