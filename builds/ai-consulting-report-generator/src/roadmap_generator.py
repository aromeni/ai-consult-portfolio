"""30/60/90-Day AI Implementation Roadmap Generator — Build 5 Phase 5.

Converts synthetic audit findings, readiness summary, risk register, and
opportunity portfolio into a staged AI implementation roadmap.

All data is synthetic. No external AI calls. Deterministic and template-based.
"""

# ── Phase definitions ───────────────────────────────────────────────────────────

_PHASE_DEFINITIONS = [
    {
        "phase_label": "First 30 days",
        "phase_focus": "Foundation and risk control",
        "phase_id_prefix": "DAY30",
        "colour": "#1e3a5f",
    },
    {
        "phase_label": "Days 31–60",
        "phase_focus": "Pilot preparation and controlled delivery",
        "phase_id_prefix": "DAY60",
        "colour": "#166534",
    },
    {
        "phase_label": "Days 61–90",
        "phase_focus": "Review, refine, and scale decision",
        "phase_id_prefix": "DAY90",
        "colour": "#6d28d9",
    },
]

_PHASE_ID_PREFIXES = {d["phase_label"]: d["phase_id_prefix"] for d in _PHASE_DEFINITIONS}

_PRIORITY_COLOURS = {
    "High": "#dc2626",
    "Medium": "#ca8a04",
    "Low": "#16a34a",
}

_CROSS_CUTTING_CONTROLS = [
    "Use only approved AI tools with an appropriate Data Processing Agreement.",
    (
        "Never enter learner data, personal data, safeguarding case details, staff HR data, "
        "or confidential records into any AI tool."
    ),
    "Require human review and sign-off before any AI-generated output is used or shared.",
    (
        "Maintain clear escalation routes for safeguarding, data protection, quality, "
        "and compliance concerns."
    ),
    "Log AI tool use, outputs reviewed, and any incidents in a simple tracking system.",
    "Ensure manager oversight of all AI pilots throughout the 90-day period.",
    "Complete staff training before any new AI tool or workflow is introduced.",
    "Review AI use at least monthly and adjust controls as evidence emerges.",
    "Do not scale any pilot until evidence has been reviewed and a documented decision made.",
    (
        "Stop any pilot immediately if a safeguarding concern, data breach, or uncontrolled "
        "risk is identified."
    ),
]

_SUCCESS_MEASURES = [
    "Number of staff who have completed responsible AI use training.",
    "Percentage of pilot participants following data boundary guidelines (target: 100%).",
    "Number of AI outputs reviewed and approved before use.",
    "Time saved per week on pilot workflow tasks — track before and after the pilot.",
    "Quality issues or corrections identified in AI-generated outputs.",
    "Number of incidents or near misses reported during the pilot.",
    "Manager review and approval rate for AI-generated outputs.",
    "Stop, continue, or scale decision documented with evidence at Day 90.",
    "Staff AI confidence — survey before and after training and pilot.",
    "No unresolved data protection or safeguarding concerns at any review point.",
]

_DEPENDENCIES = [
    "AI governance owners must be confirmed before any pilot launches.",
    "Acceptable-use guidance must be approved and distributed before staff use AI tools.",
    "Data boundary guidelines must be confirmed and understood by all pilot participants.",
    "Staff training must be completed before pilot participants use AI tools.",
    "Pilot scope, success measures, and responsible owner must be agreed before launch.",
    "Human review process must be in place before any AI output is used.",
]

_RISKS_TO_MANAGE = [
    "Staff using AI tools without reading or following the acceptable-use guide.",
    "Learner data, personal data, or confidential records accidentally entered into AI tools.",
    "AI-generated outputs used without human review or approval.",
    (
        "Safeguarding concerns raised with AI tools instead of through "
        "proper escalation routes."
    ),
    "Pilot scope expanded before review evidence is collected and decisions documented.",
    "No AI governance owner identified or active before the pilot launches.",
    "Data boundary guidelines not communicated before pilot participants begin.",
    "Risk incidents not escalated promptly during the pilot.",
]


# ── Core builders ───────────────────────────────────────────────────────────────

def get_roadmap_phase_definitions() -> list:
    """Return the three 30/60/90-day phase definitions."""
    return list(_PHASE_DEFINITIONS)


def generate_roadmap_action_id(phase_label: str, index: int) -> str:
    """Return a formatted action ID, e.g. DAY30-001."""
    prefix = _PHASE_ID_PREFIXES.get(phase_label, "ACT")
    return f"{prefix}-{index + 1:03d}"


def generate_roadmap_action(
    action_id: str,
    phase: str,
    title: str,
    description: str,
    owner: str,
    priority: str,
    success_measure: str,
    dependency: str = "",
    risk_reduction: str = "",
    related_output: str = "",
) -> dict:
    """Build a single roadmap action dict."""
    return {
        "action_id": action_id,
        "phase": phase,
        "title": title,
        "description": description,
        "owner": owner,
        "priority": priority,
        "success_measure": success_measure,
        "dependency": dependency,
        "risk_reduction": risk_reduction,
        "related_output": related_output,
    }


def get_priority_colour(priority: str) -> str:
    """Return hex colour for a priority label."""
    return _PRIORITY_COLOURS.get(priority, "#64748b")


def get_phase_colour(phase_label: str) -> str:
    """Return hex colour for a phase label."""
    for d in _PHASE_DEFINITIONS:
        if d["phase_label"] == phase_label:
            return d["colour"]
    return "#1a2744"


# ── Private helpers ─────────────────────────────────────────────────────────────

def _get_cross_cutting_controls() -> list:
    return list(_CROSS_CUTTING_CONTROLS)


def _get_success_measures() -> list:
    return list(_SUCCESS_MEASURES)


def _get_dependencies() -> list:
    return list(_DEPENDENCIES)


def _get_risks_to_manage() -> list:
    return list(_RISKS_TO_MANAGE)


def _derive_roadmap_position(
    readiness_summary: dict | None,
    risk_summary: dict | None,
) -> str:
    if risk_summary and (
        risk_summary.get("critical_risks", 0) > 0
        or risk_summary.get("high_risks", 0) > 0
    ):
        return (
            "The roadmap should prioritise governance, data boundaries, safeguarding escalation, "
            "and human-review controls before wider AI scaling."
        )
    if readiness_summary:
        level = readiness_summary.get("overall_level") or ""
        if "Low" in level or "Developing" in level:
            return (
                "The roadmap should focus on foundations, staff training, and a narrow "
                "controlled pilot before scaling."
            )
        if "Moderate" in level or "Strong" in level:
            return (
                "The organisation can progress to controlled pilots while maintaining "
                "governance, monitoring, and responsible-owner review."
            )
    return (
        "The roadmap should prioritise foundations, responsible-use governance, and a narrow "
        "controlled pilot before any scaling."
    )


def _first_pilot_name_from(
    audit_data: dict,
    opportunity_portfolio: dict | None,
) -> str:
    if opportunity_portfolio:
        first = opportunity_portfolio.get("recommended_first_pilot") or {}
        name = first.get("pilot_name")
        if name:
            return name
    pilots = audit_data.get("pilot_recommendations") or []
    if pilots:
        name = pilots[0].get("pilot_name")
        if name:
            return name
    return "a low-risk pilot workflow"


def _renumber_actions(actions: list, phase_label: str) -> list:
    result = []
    for i, action in enumerate(actions):
        new_action = dict(action)
        new_action["action_id"] = generate_roadmap_action_id(phase_label, i)
        result.append(new_action)
    return result


# ── Phase action generators ─────────────────────────────────────────────────────

def generate_foundation_actions(
    audit_data: dict,
    readiness_summary: dict | None = None,
    risk_summary: dict | None = None,
) -> list:
    """Return actions for the first 30 days — foundation and risk control."""
    phase = "First 30 days"
    actions = []

    def _a(title, description, owner, priority, success_measure, **kwargs):
        i = len(actions)
        actions.append(generate_roadmap_action(
            generate_roadmap_action_id(phase, i),
            phase, title, description, owner, priority, success_measure, **kwargs,
        ))

    _a(
        "Confirm AI governance and escalation owners",
        (
            "Identify who owns AI governance, data protection, safeguarding escalation, "
            "quality review, and pilot approval. Record names and communicate them to all "
            "staff before AI use continues."
        ),
        "Senior Leadership Team / AI Governance Owner",
        "High",
        "Named owners are recorded in writing and all staff know where to escalate concerns.",
        risk_reduction="Removes accountability gap",
    )

    _a(
        "Define approved and prohibited AI use cases",
        (
            "Create a clear list of what staff can and cannot use AI for. Explicitly prohibit "
            "entry of learner data, safeguarding case details, confidential records, staff HR data, "
            "and personal data into any AI tool."
        ),
        "Senior Manager / Data Protection Lead",
        "High",
        "Approved and prohibited use case list circulated and acknowledged by all staff.",
        risk_reduction="Reduces data protection and governance risk",
    )

    _a(
        "Clarify data boundaries for all AI tools",
        (
            "Define and document what data must never enter AI tools — learner names, attendance, "
            "progress records, safeguarding information, staff HR data, personal data, and regulated "
            "information. Include this in all guidance materials."
        ),
        "Data Protection Lead / DPO",
        "High",
        "Data boundary guidelines distributed and confirmed by all staff before any pilot begins.",
        risk_reduction="Reduces GDPR, data protection, and learner privacy risk",
    )

    _a(
        "Confirm safeguarding escalation routes alongside AI guidance",
        (
            "Explicitly prohibit AI from any safeguarding concern, disclosure, or decision. "
            "Communicate the safeguarding escalation routes to all staff at the same time as "
            "any AI guidance is issued."
        ),
        "Designated Safeguarding Lead",
        "High",
        "All staff briefed. Safeguarding escalation routes clearly communicated and documented.",
        risk_reduction="Mitigates safeguarding risk",
    )

    _a(
        "Create or approve acceptable-use guidance",
        (
            "Draft a short responsible AI use guide covering approved uses, prohibited uses, "
            "data boundaries, escalation contacts, and review requirements. "
            "Keep it to one page for ease of use."
        ),
        "Senior Manager / Quality Lead",
        "High",
        "Guide shared with all staff and acknowledgement recorded before any pilot launches.",
    )

    _a(
        "Select one low-risk pilot and define its scope",
        (
            "Choose one low-complexity, low-risk workflow as the first AI pilot. Define its scope, "
            "participants, timeline, approved tools, and content boundaries before AI use begins. "
            "Do not start multiple pilots at the same time."
        ),
        "Pilot Lead / Senior Manager",
        "Medium",
        "Pilot scope documented and approved by the responsible owner.",
        related_output="Opportunity Portfolio",
    )

    _a(
        "Plan staff training for responsible AI use",
        (
            "Design training covering responsible AI use, data boundaries, safeguarding and AI, "
            "how to spot hallucinations, and practical skills for the pilot workflow. "
            "Schedule sessions for all pilot participants before the pilot begins."
        ),
        "Quality Lead / Training Lead",
        "Medium",
        "Training plan approved and all sessions scheduled before the pilot launches.",
    )

    _a(
        "Define success measures for the first pilot",
        (
            "Agree what success looks like before the pilot launches — time saved, quality issues "
            "identified, incident count, staff confidence, review completion rate, and a documented "
            "stop, continue, or scale decision criterion."
        ),
        "Pilot Lead / Quality Lead",
        "Medium",
        "Success measures documented, agreed with the responsible owner, and shared with participants.",
        related_output="Opportunity Portfolio",
    )

    # Adaptive: add governance policy action if audit shows a critical policy gap
    governance_gaps = audit_data.get("governance_gaps") or []
    has_policy_gap = any(
        "policy" in g.get("gap_title", "").lower()
        and g.get("priority") == "Critical"
        for g in governance_gaps
    )
    if has_policy_gap:
        _a(
            "Draft and approve a formal AI use policy",
            (
                "Develop a formal AI use policy covering: approved tools list, prohibited uses, "
                "data boundaries, human-review requirements, safeguarding restrictions, incident "
                "reporting, and responsible-owner sign-off. Have it reviewed and approved before "
                "any pilot launches."
            ),
            "Senior Leadership Team / Data Protection Lead",
            "High",
            "AI use policy drafted, approved, and distributed before the pilot begins.",
            dependency="Define approved/prohibited use cases (DAY30-002)",
            risk_reduction="Addresses critical governance gap — No AI Use Policy",
            related_output="Audit Data",
        )

    # Adaptive: highlight top risks if risk summary shows high or critical items
    if risk_summary and (
        risk_summary.get("critical_risks", 0) > 0
        or risk_summary.get("high_risks", 0) > 0
    ):
        critical_n = risk_summary.get("critical_risks", 0)
        high_n = risk_summary.get("high_risks", 0)
        risk_text_parts = []
        if critical_n:
            risk_text_parts.append(f"{critical_n} critical risk(s)")
        if high_n:
            risk_text_parts.append(f"{high_n} high risk(s)")
        risk_text = " and ".join(risk_text_parts)
        _a(
            "Address top priority AI governance and data risks",
            (
                f"The risk register identifies {risk_text}. Ensure the highest-priority risks — "
                "particularly data protection and safeguarding — are addressed through documented "
                "controls before any pilot launches or expands."
            ),
            "Senior Manager / Data Protection Lead",
            "High",
            "Top priority risks have assigned owners, documented controls, and review dates.",
            dependency="Complete risk register review",
            risk_reduction=f"Addresses {risk_text} identified in the risk register",
            related_output="Risk Register",
        )

    return actions


def generate_pilot_preparation_actions(
    audit_data: dict,
    opportunity_portfolio: dict | None = None,
) -> list:
    """Return actions for Days 31–60 — pilot preparation."""
    phase = "Days 31–60"
    pilot_name = _first_pilot_name_from(audit_data, opportunity_portfolio)
    actions = []

    def _a(title, description, owner, priority, success_measure, **kwargs):
        i = len(actions)
        actions.append(generate_roadmap_action(
            generate_roadmap_action_id(phase, i),
            phase, title, description, owner, priority, success_measure, **kwargs,
        ))

    _a(
        "Deliver responsible AI use training to all pilot participants",
        (
            "Run the planned training sessions on responsible AI use, data boundaries, "
            "safeguarding and AI, and the acceptable-use guide. All pilot participants "
            "must complete training before using AI tools in the pilot."
        ),
        "Training Lead / Quality Lead",
        "High",
        "All pilot participants have completed training and confirmed their understanding of data boundaries.",
        dependency="Training plan approved (DAY30-007)",
    )

    _a(
        "Prepare and approve pilot materials using approved content only",
        (
            "Create and approve the content to be used in the pilot. Confirm in writing that "
            "no real learner data, personal data, or confidential records will be used. "
            "Use only synthetic, anonymised, or pre-approved documents."
        ),
        "Pilot Lead / Curriculum Lead",
        "High",
        "Pilot materials approved. Content boundaries confirmed in writing before launch.",
        dependency="Pilot scope approved (DAY30-006)",
    )

    _a(
        "Brief all pilot participants on data boundaries and escalation routes",
        (
            "Hold a short pre-pilot briefing for all participants covering: what AI can be used "
            "for, what is prohibited, how to escalate concerns, and what the review process is "
            "for AI-generated outputs."
        ),
        "Pilot Lead",
        "High",
        "All participants briefed and questions resolved before the pilot launches.",
        dependency="Acceptable-use guidance approved (DAY30-005)",
    )

    return actions


def generate_pilot_delivery_actions(
    audit_data: dict,
    opportunity_portfolio: dict | None = None,
) -> list:
    """Return actions for Days 31–60 — pilot delivery and data collection."""
    phase = "Days 31–60"
    pilot_name = _first_pilot_name_from(audit_data, opportunity_portfolio)
    actions = []

    def _a(title, description, owner, priority, success_measure, **kwargs):
        i = len(actions)
        actions.append(generate_roadmap_action(
            generate_roadmap_action_id(phase, i),
            phase, title, description, owner, priority, success_measure, **kwargs,
        ))

    _a(
        f"Launch controlled AI pilot — {pilot_name}",
        (
            f"Allow selected pilot participants to use approved AI tools for {pilot_name}. "
            "Use only approved tools and approved or synthetic content. "
            "Require human review and sign-off before any AI-generated output is used."
        ),
        "Pilot Lead",
        "High",
        "Pilot launched with all participants following agreed data boundaries and review process.",
        dependency="Training complete and materials approved (DAY60-001, DAY60-002)",
        risk_reduction="Narrow, controlled scope reduces data protection and quality risk",
    )

    _a(
        "Require and document human review of all AI outputs",
        (
            "Confirm that every AI-generated output is reviewed and approved by a named reviewer "
            "before it is used. Record the reviewer name, date, and outcome in the pilot log."
        ),
        "Pilot Lead / Quality Lead",
        "High",
        "100% of pilot outputs have a recorded human review before use.",
    )

    _a(
        "Track time saved, quality issues, and staff confidence weekly",
        (
            "Collect data every week throughout the pilot: time saved per task, quality issues "
            "found, corrections made, incidents raised, and staff confidence rating. "
            "A simple spreadsheet log is sufficient at this stage."
        ),
        "Pilot Lead",
        "Medium",
        "Weekly pilot log completed with data against all agreed success measures.",
    )

    _a(
        "Review any risk incidents, near misses, or data boundary concerns",
        (
            "Check weekly whether any data protection concerns, safeguarding issues, quality "
            "failures, or acceptable-use boundary breaches occurred. Escalate immediately if so. "
            "Do not wait until Day 60 to review incidents."
        ),
        "Senior Manager / Data Protection Lead",
        "High",
        "All incidents and near misses documented and escalated within 24 hours of identification.",
        risk_reduction="Prevents risk accumulation during the pilot",
    )

    return actions


def generate_review_and_scale_actions(
    audit_data: dict,
    opportunity_portfolio: dict | None = None,
    risk_summary: dict | None = None,
) -> list:
    """Return actions for Days 61–90 — review, refine, and scale decision."""
    phase = "Days 61–90"
    actions = []

    def _a(title, description, owner, priority, success_measure, **kwargs):
        i = len(actions)
        actions.append(generate_roadmap_action(
            generate_roadmap_action_id(phase, i),
            phase, title, description, owner, priority, success_measure, **kwargs,
        ))

    _a(
        "Review pilot evidence against agreed success measures",
        (
            "Compile and review all pilot data: time saved, output quality, staff confidence, "
            "risk incidents, near misses, and manager feedback. Compare against the success "
            "measures agreed before the pilot launched."
        ),
        "Senior Manager / Pilot Owner",
        "High",
        "Pilot review document completed with evidence against each agreed success measure.",
        dependency="Pilot completed and pilot log collected (DAY60 actions)",
        related_output="Opportunity Portfolio",
    )

    _a(
        "Make a documented stop, continue, or scale decision",
        (
            "Based on pilot evidence, make a documented decision: stop the pilot, continue at "
            "the same scale, or expand to more staff or workflows. Include the reasoning, "
            "evidence, and next actions. Do not scale before reviewing evidence."
        ),
        "Senior Leadership Team",
        "High",
        "Decision documented with clear evidence, reasons, and agreed next actions.",
        dependency="Pilot review completed (DAY90-001)",
    )

    _a(
        "Update policy and training materials based on pilot learnings",
        (
            "Revise the acceptable-use guide, training materials, and approved or prohibited "
            "use case list to reflect what was learned in the pilot — including any new risks, "
            "controls, or approved uses identified."
        ),
        "Quality Lead / Senior Manager",
        "Medium",
        "Updated guidance and training circulated to relevant staff.",
        dependency="Scale decision made (DAY90-002)",
    )

    _a(
        "Strengthen any control gaps identified during the pilot",
        (
            "Address any data boundary gaps, review process weaknesses, governance issues, or "
            "training gaps identified during the pilot before expanding AI use to additional "
            "staff or workflows."
        ),
        "Data Protection Lead / Quality Lead",
        "Medium",
        "All identified control gaps resolved or escalated to a named owner.",
        risk_reduction="Prevents known weaknesses from being carried into wider adoption",
    )

    _a(
        "Scope a second pilot if scale decision is positive",
        (
            "If the first pilot is successful, scope the next pilot workflow. Ensure the same "
            "governance foundations are in place — approved tools, data boundaries, training, "
            "and human review — before the second pilot begins. Do not rush to expand."
        ),
        "Pilot Lead / Senior Manager",
        "Low",
        "Second pilot scope documented and approved, or a decision to extend the first pilot made.",
        dependency="Scale decision positive (DAY90-002)",
        related_output="Opportunity Portfolio",
    )

    _a(
        "Report on AI governance and responsible-use progress to leadership",
        (
            "Produce a short governance summary: what was piloted, what was learned, what risks "
            "were managed, what the next steps are, and whether any policy or training updates "
            "are needed. Share with senior leadership."
        ),
        "Quality Lead / AI Governance Owner",
        "Medium",
        "Governance summary shared with senior leadership and agreed next actions documented.",
    )

    # Adaptive: add risk review action if unresolved high-priority risks remain
    if risk_summary and risk_summary.get("high_risks", 0) > 0:
        _a(
            "Address outstanding risk register items before scaling",
            (
                "Review the risk register for any unresolved high-priority items before scaling "
                "AI adoption further. Confirm that recommended controls have been implemented "
                "and that responsible owners have signed off."
            ),
            "Senior Manager / Data Protection Lead",
            "High",
            "All high-priority risk register items reviewed and controls confirmed.",
            risk_reduction="Prevents unresolved risks from scaling with wider adoption",
            related_output="Risk Register",
        )

    return actions


# ── Portfolio and summary builders ──────────────────────────────────────────────

def generate_implementation_roadmap(
    audit_data: dict,
    readiness_summary: dict | None = None,
    risk_register: list | None = None,
    risk_summary: dict | None = None,
    opportunity_portfolio: dict | None = None,
) -> dict:
    """Build the full 30/60/90-day implementation roadmap from all available data."""
    if not audit_data:
        return _empty_roadmap("Unnamed organisation")

    org_name = (
        audit_data.get("organisation_profile", {}).get("organisation_name")
        or "Unnamed organisation"
    )

    day_30 = _renumber_actions(
        generate_foundation_actions(audit_data, readiness_summary, risk_summary),
        "First 30 days",
    )
    day_60 = _renumber_actions(
        generate_pilot_preparation_actions(audit_data, opportunity_portfolio)
        + generate_pilot_delivery_actions(audit_data, opportunity_portfolio),
        "Days 31–60",
    )
    day_90 = _renumber_actions(
        generate_review_and_scale_actions(audit_data, opportunity_portfolio, risk_summary),
        "Days 61–90",
    )

    # Recommended first pilot — prefer opportunity portfolio, fall back to audit data
    recommended_first_pilot: dict = {}
    if opportunity_portfolio:
        recommended_first_pilot = opportunity_portfolio.get("recommended_first_pilot") or {}
    if not recommended_first_pilot:
        pilots = audit_data.get("pilot_recommendations") or []
        if pilots:
            p = pilots[0]
            recommended_first_pilot = {
                "pilot_name": p.get("pilot_name", "Generic low-risk pilot"),
                "complexity": p.get("complexity", "Low"),
                "risk_level": p.get("risk_level", "Low"),
                "suggested_timeline": p.get("suggested_timeline", "Month 1–2"),
            }
    if not recommended_first_pilot:
        recommended_first_pilot = {
            "pilot_name": "Generic low-risk AI pilot",
            "complexity": "Low",
            "risk_level": "Low",
            "suggested_timeline": "Month 1–2",
        }

    overall_position = _derive_roadmap_position(readiness_summary, risk_summary)

    return {
        "organisation_name": org_name,
        "roadmap_title": "30/60/90-Day AI Implementation Roadmap",
        "roadmap_purpose": (
            f"This roadmap provides a staged approach for {org_name} to introduce AI safely, "
            "with clear governance, data boundaries, pilot controls, and review gates at each "
            "stage. It is based on the findings from a synthetic AI readiness audit and should "
            "be reviewed and adapted by a qualified consultant before use with any real organisation."
        ),
        "phase_30_days": day_30,
        "phase_60_days": day_60,
        "phase_90_days": day_90,
        "cross_cutting_controls": _get_cross_cutting_controls(),
        "success_measures": _get_success_measures(),
        "dependencies": _get_dependencies(),
        "risks_to_manage": _get_risks_to_manage(),
        "recommended_first_pilot": recommended_first_pilot,
        "overall_roadmap_position": overall_position,
        "responsible_use_note": (
            "This roadmap is generated from synthetic/demo audit data only. "
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


def _empty_roadmap(org_name: str) -> dict:
    return {
        "organisation_name": org_name,
        "roadmap_title": "30/60/90-Day AI Implementation Roadmap",
        "roadmap_purpose": "No audit data loaded. Please load audit data to generate a roadmap.",
        "phase_30_days": [],
        "phase_60_days": [],
        "phase_90_days": [],
        "cross_cutting_controls": [],
        "success_measures": [],
        "dependencies": [],
        "risks_to_manage": [],
        "recommended_first_pilot": {},
        "overall_roadmap_position": "Load audit data to generate a roadmap.",
        "responsible_use_note": (
            "This roadmap is generated from synthetic/demo audit data only."
        ),
        "prototype_note": (
            "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
            "financial, academic-integrity, or professional advice. "
            "Human review remains required before any real-world use."
        ),
    }


def summarise_implementation_roadmap(roadmap: dict) -> dict:
    """Return a summary dict for the implementation roadmap."""
    day_30 = roadmap.get("phase_30_days") or []
    day_60 = roadmap.get("phase_60_days") or []
    day_90 = roadmap.get("phase_90_days") or []
    all_actions = day_30 + day_60 + day_90

    high_count = sum(1 for a in all_actions if a.get("priority") == "High")

    first_pilot = roadmap.get("recommended_first_pilot") or {}
    first_pilot_name = first_pilot.get("pilot_name") or "Not identified"

    return {
        "total_actions": len(all_actions),
        "day_30_actions": len(day_30),
        "day_60_actions": len(day_60),
        "day_90_actions": len(day_90),
        "high_priority_actions": high_count,
        "recommended_first_pilot": first_pilot_name,
        "key_dependencies": roadmap.get("dependencies") or [],
        "key_risks_to_manage": roadmap.get("risks_to_manage") or [],
        "overall_roadmap_position": roadmap.get("overall_roadmap_position") or "",
    }


# ── Markdown formatter ──────────────────────────────────────────────────────────

def format_implementation_roadmap_as_markdown(
    roadmap: dict,
    summary: dict | None = None,
) -> str:
    """Format the implementation roadmap as a client-facing Markdown document."""
    org = roadmap.get("organisation_name") or "Unnamed organisation"
    day_30 = roadmap.get("phase_30_days") or []
    day_60 = roadmap.get("phase_60_days") or []
    day_90 = roadmap.get("phase_90_days") or []
    first_pilot = roadmap.get("recommended_first_pilot") or {}

    if summary is None:
        summary = summarise_implementation_roadmap(roadmap)

    lines = [
        "# 30/60/90-Day AI Implementation Roadmap",
        "",
        f"**Organisation:** {org}",
        "",
        "---",
        "",
        "## Roadmap Purpose",
        "",
        roadmap.get("roadmap_purpose", ""),
        "",
        "---",
        "",
        "## Roadmap Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total actions | {summary.get('total_actions', 0)} |",
        f"| First 30 days actions | {summary.get('day_30_actions', 0)} |",
        f"| Days 31–60 actions | {summary.get('day_60_actions', 0)} |",
        f"| Days 61–90 actions | {summary.get('day_90_actions', 0)} |",
        f"| High priority actions | {summary.get('high_priority_actions', 0)} |",
        f"| Recommended first pilot | {summary.get('recommended_first_pilot', '—')} |",
        "",
        f"**Overall position:** {summary.get('overall_roadmap_position', '')}",
        "",
        "---",
        "",
    ]

    # Phase sections
    phase_sections = [
        ("## First 30 Days: Foundation and Risk Control", day_30),
        ("## Days 31–60: Pilot Preparation and Controlled Delivery", day_60),
        ("## Days 61–90: Review, Refine, and Scale Decision", day_90),
    ]

    for heading, actions in phase_sections:
        lines.append(heading)
        lines.append("")
        if actions:
            lines += [
                "| ID | Action | Priority | Owner |",
                "|---|---|---|---|",
            ]
            for a in actions:
                lines.append(
                    f"| {a.get('action_id', '—')} "
                    f"| {a.get('title', '—')} "
                    f"| {a.get('priority', '—')} "
                    f"| {a.get('owner', '—')} |"
                )
            lines.append("")
            for a in actions:
                lines += [
                    f"### {a.get('action_id', '—')}: {a.get('title', '—')}",
                    "",
                    f"**Priority:** {a.get('priority', '—')} | **Owner:** {a.get('owner', '—')}",
                    "",
                    a.get("description", ""),
                    "",
                    f"**Success measure:** {a.get('success_measure', '')}",
                    "",
                ]
                if a.get("dependency"):
                    lines.append(f"**Dependency:** {a['dependency']}")
                    lines.append("")
                if a.get("risk_reduction"):
                    lines.append(f"**Risk reduction:** {a['risk_reduction']}")
                    lines.append("")
                if a.get("related_output"):
                    lines.append(f"**Related output:** {a['related_output']}")
                    lines.append("")
        else:
            lines.append("No actions generated.")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Cross-cutting controls
    lines += ["## Cross-Cutting Controls", ""]
    for c in roadmap.get("cross_cutting_controls") or []:
        lines.append(f"- {c}")
    lines += ["", "---", ""]

    # Success measures
    lines += ["## Success Measures", ""]
    for m in roadmap.get("success_measures") or []:
        lines.append(f"- {m}")
    lines += ["", "---", ""]

    # Dependencies
    lines += ["## Dependencies", ""]
    for d in roadmap.get("dependencies") or []:
        lines.append(f"- {d}")
    lines += ["", "---", ""]

    # Risks to manage
    lines += ["## Risks to Manage", ""]
    for r in roadmap.get("risks_to_manage") or []:
        lines.append(f"- {r}")
    lines += ["", "---", ""]

    # Recommended first pilot
    lines += ["## Recommended First Pilot", ""]
    if first_pilot:
        lines += [
            f"**{first_pilot.get('pilot_name', '—')}**",
            "",
            f"- **Complexity:** {first_pilot.get('complexity', '—')}",
            f"- **Risk level:** {first_pilot.get('risk_level', '—')}",
            f"- **Suggested timeline:** {first_pilot.get('suggested_timeline', '—')}",
        ]
    else:
        lines.append("No pilot identified.")
    lines += ["", "---", ""]

    # Responsible-use boundaries
    lines += [
        "## Responsible-Use Boundaries",
        "",
        roadmap.get("responsible_use_note", ""),
        "",
        roadmap.get("prototype_note", ""),
        "",
        "---",
        "",
        "*Build 5 · AI Consulting Report Generator · BrightPath ChatGPT Mastery Project*",
        "*All scenarios are synthetic. Outputs require human review before real-world use.*",
    ]

    return "\n".join(lines)
