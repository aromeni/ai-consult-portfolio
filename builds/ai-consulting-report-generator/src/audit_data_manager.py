"""Audit data validation, summarisation, and formatting — Build 5."""

from __future__ import annotations


def validate_audit_data(audit_data: dict) -> tuple[bool, str]:
    """Validate audit data structure and required fields."""
    if not isinstance(audit_data, dict):
        return False, "Audit data must be a dictionary."

    profile = audit_data.get("organisation_profile")
    if not profile or not isinstance(profile, dict):
        return False, "organisation_profile is missing or invalid."

    org_name = str(profile.get("organisation_name") or "").strip()
    if not org_name:
        return False, "organisation_name is missing or empty."

    staff_count = profile.get("staff_count")
    if staff_count is None:
        return False, "staff_count is missing."
    try:
        staff_int = int(staff_count)
    except (TypeError, ValueError):
        return False, "staff_count must be a number."
    if staff_int <= 0:
        return False, "staff_count must be a positive number."

    scores = audit_data.get("readiness_scores")
    if not scores or not isinstance(scores, dict):
        return False, "readiness_scores is missing or invalid."
    if scores.get("overall_readiness_score") is None:
        return False, "overall_readiness_score is missing."

    for key in ("workflow_findings", "risk_findings", "pilot_recommendations"):
        val = audit_data.get(key)
        if val is None:
            return False, f"{key} is missing."
        if not isinstance(val, list):
            return False, f"{key} must be a list."

    return True, "Valid"


def summarise_audit_data(audit_data: dict) -> dict:
    """Return a high-level summary dict of the audit data."""
    profile = audit_data.get("organisation_profile", {})
    scores = audit_data.get("readiness_scores", {})

    risk_findings = audit_data.get("risk_findings", [])
    governance_gaps = audit_data.get("governance_gaps", [])
    training_needs = audit_data.get("training_needs", [])

    critical_risks = [r for r in risk_findings if str(r.get("risk_level", "")).lower() == "critical"]
    high_risks = [r for r in risk_findings if str(r.get("risk_level", "")).lower() == "high"]
    critical_gaps = [g for g in governance_gaps if str(g.get("priority", "")).lower() == "critical"]
    high_priority_training = [t for t in training_needs if str(t.get("priority", "")).lower() == "high"]

    return {
        "organisation_name": profile.get("organisation_name", "Unknown"),
        "sector": profile.get("sector", "Unknown"),
        "staff_count": profile.get("staff_count", 0),
        "overall_readiness_score": scores.get("overall_readiness_score", 0),
        "workflow_count": len(audit_data.get("workflow_findings", [])),
        "risk_count": len(risk_findings),
        "pilot_count": len(audit_data.get("pilot_recommendations", [])),
        "training_count": len(training_needs),
        "governance_gap_count": len(governance_gaps),
        "critical_risk_count": len(critical_risks),
        "high_risk_count": len(high_risks),
        "critical_gap_count": len(critical_gaps),
        "high_priority_training_count": len(high_priority_training),
        "departments": profile.get("departments", []),
        "current_ai_use": profile.get("current_ai_use", ""),
    }


def format_audit_data_as_markdown(audit_data: dict) -> str:
    """Return a Markdown representation of the full audit dataset."""
    profile = audit_data.get("organisation_profile", {})
    scores = audit_data.get("readiness_scores", {})
    workflow_findings = audit_data.get("workflow_findings", [])
    risk_findings = audit_data.get("risk_findings", [])
    pilots = audit_data.get("pilot_recommendations", [])
    training_needs = audit_data.get("training_needs", [])
    governance_gaps = audit_data.get("governance_gaps", [])

    org_name = profile.get("organisation_name", "Unknown Organisation")
    lines = [
        f"# AI Readiness Audit — {org_name}",
        "",
        "## Organisation Profile",
        "",
        f"- **Organisation:** {profile.get('organisation_name', '')}",
        f"- **Type:** {profile.get('organisation_type', '')}",
        f"- **Sector:** {profile.get('sector', '')}",
        f"- **Country:** {profile.get('country_context', '')}",
        f"- **Staff count:** {profile.get('staff_count', '')}",
        "",
        "**Departments:**",
    ]
    for dept in profile.get("departments", []):
        lines.append(f"- {dept}")
    lines += [
        "",
        f"**Current AI Use:** {profile.get('current_ai_use', '')}",
        "",
        "**Main Business Goals:**",
    ]
    for goal in profile.get("main_business_goals", []):
        lines.append(f"- {goal}")

    score_labels = {
        "strategy_score": "Strategy",
        "data_governance_score": "Data Governance",
        "staff_capability_score": "Staff Capability",
        "workflow_opportunity_score": "Workflow Opportunity",
        "risk_management_score": "Risk Management",
        "leadership_alignment_score": "Leadership Alignment",
        "overall_readiness_score": "**Overall Readiness**",
    }
    lines += ["", "## Readiness Scores", "", "| Category | Score |", "|---|---|"]
    for key, label in score_labels.items():
        lines.append(f"| {label} | {scores.get(key, '—')} |")

    lines += ["", "## Workflow Findings", ""]
    for wf in workflow_findings:
        lines.append(f"### {wf.get('workflow_name', 'Unnamed Workflow')}")
        lines.append(f"- **Risk Level:** {wf.get('risk_level', '')}")
        lines.append(f"- **AI Opportunity:** {wf.get('ai_opportunity', '')}")
        lines.append(f"- **Recommended Action:** {wf.get('recommended_action', '')}")
        lines.append("")

    lines += ["## Risk Findings", ""]
    for rf in risk_findings:
        lines.append(f"### {rf.get('risk_title', 'Unnamed Risk')}")
        lines.append(f"- **Level:** {rf.get('risk_level', '')}")
        lines.append(f"- **Category:** {rf.get('risk_category', '')}")
        lines.append(f"- **Recommended Control:** {rf.get('recommended_control', '')}")
        lines.append("")

    lines += ["## Pilot Recommendations", ""]
    for p in pilots:
        lines.append(f"### {p.get('pilot_name', 'Unnamed Pilot')}")
        lines.append(f"- **Timeline:** {p.get('suggested_timeline', '')}")
        lines.append(f"- **Complexity:** {p.get('complexity', '')} / Risk: {p.get('risk_level', '')}")
        lines.append("")

    lines += ["## Training Needs", ""]
    for t in training_needs:
        lines.append(
            f"- **{t.get('topic', '')}** ({t.get('audience', '')}) — Priority: {t.get('priority', '')}"
        )

    lines += ["", "## Governance Gaps", ""]
    for g in governance_gaps:
        lines.append(f"- **{g.get('gap_title', '')}** — Priority: {g.get('priority', '')}")

    lines += ["", "---", "", "*Synthetic scenario data. Human review required before real-world use.*"]
    return "\n".join(lines)


def create_audit_data_from_form_data(form_data: dict) -> dict:
    """Build a minimal audit data dict from UI form inputs."""
    from src.sample_data import (
        get_demo_workflow_findings,
        get_demo_risk_findings,
        get_demo_pilot_recommendations,
        get_demo_training_needs,
        get_demo_governance_gaps,
    )

    org_name = str(form_data.get("organisation_name") or "").strip() or "Unknown Organisation"

    readiness_scores = {
        "strategy_score": int(form_data.get("strategy_score", 50)),
        "data_governance_score": int(form_data.get("data_governance_score", 50)),
        "staff_capability_score": int(form_data.get("staff_capability_score", 50)),
        "workflow_opportunity_score": int(form_data.get("workflow_opportunity_score", 50)),
        "risk_management_score": int(form_data.get("risk_management_score", 50)),
        "leadership_alignment_score": int(form_data.get("leadership_alignment_score", 50)),
        "overall_readiness_score": int(form_data.get("overall_readiness_score", 50)),
    }

    return {
        "organisation_profile": {
            "organisation_name": org_name,
            "organisation_type": str(form_data.get("organisation_type") or "").strip(),
            "sector": str(form_data.get("sector") or "").strip(),
            "country_context": str(form_data.get("country_context") or "").strip(),
            "staff_count": int(form_data.get("staff_count", 0)),
            "departments": form_data.get("departments", []),
            "current_ai_use": str(form_data.get("current_ai_use") or "").strip(),
            "main_business_goals": form_data.get("main_business_goals", []),
        },
        "readiness_scores": readiness_scores,
        "workflow_findings": get_demo_workflow_findings(),
        "risk_findings": get_demo_risk_findings(),
        "pilot_recommendations": get_demo_pilot_recommendations(),
        "training_needs": get_demo_training_needs(),
        "governance_gaps": get_demo_governance_gaps(),
    }
