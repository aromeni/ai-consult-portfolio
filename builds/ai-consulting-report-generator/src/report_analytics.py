"""Report analytics — Build 5 Phase 8.

Deterministic analytics calculated from generated Build 5 outputs only.
No external AI calls. No invented data. No real client data.
"""


def calculate_export_completion_status(export_data: dict) -> dict:
    """Return completion status for each Build 5 output."""
    ed = export_data or {}
    source = ed.get("source_outputs_available") or {}
    return {
        "Audit Data": source.get("audit_data", bool(ed.get("audit_data"))),
        "Readiness Summary": source.get(
            "readiness_summary", ed.get("readiness_summary") is not None
        ),
        "Risk Register": source.get(
            "risk_register", ed.get("risk_register") is not None
        ),
        "Opportunity Portfolio": source.get(
            "opportunity_portfolio", ed.get("opportunity_portfolio") is not None
        ),
        "Implementation Roadmap": source.get(
            "implementation_roadmap", ed.get("implementation_roadmap") is not None
        ),
        "Report Sections": source.get(
            "report_sections", ed.get("report_sections") is not None
        ),
        "Client Report": bool(ed.get("client_report_markdown")),
    }


def calculate_readiness_score_breakdown(export_data: dict) -> dict:
    """Return readiness scores by category from audit data."""
    ed = export_data or {}
    audit = ed.get("audit_data") or {}
    scores = audit.get("readiness_scores") or {}

    label_map = {
        "strategy_score": "Strategy",
        "data_governance_score": "Data Governance",
        "staff_capability_score": "Staff Capability",
        "workflow_opportunity_score": "Workflow Opportunity",
        "risk_management_score": "Risk Management",
        "leadership_alignment_score": "Leadership Alignment",
    }
    result = {}
    for key, label in label_map.items():
        val = scores.get(key)
        if val is not None:
            result[label] = int(val)
    overall = scores.get("overall_readiness_score")
    if overall is not None:
        result["Overall"] = int(overall)
    return result


def calculate_risk_level_counts(export_data: dict) -> dict:
    """Return counts of risks by level."""
    ed = export_data or {}
    rr_summary = ed.get("risk_register_summary") or {}
    if rr_summary:
        return {
            "Critical": int(rr_summary.get("critical_risks", 0)),
            "High": int(rr_summary.get("high_risks", 0)),
            "Medium": int(rr_summary.get("medium_risks", 0)),
            "Low": int(rr_summary.get("low_risks", 0)),
        }
    # Fallback: count from risk register list
    risk_register = ed.get("risk_register") or []
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for r in risk_register:
        level = str(r.get("risk_level", "")).strip().title()
        if level in counts:
            counts[level] += 1
    return counts


def calculate_opportunity_priority_counts(export_data: dict) -> dict:
    """Return counts of opportunities by priority."""
    ed = export_data or {}
    opp_summary = ed.get("opportunity_summary") or {}
    if opp_summary:
        return {
            "Strategic": int(opp_summary.get("strategic_priority_opportunities", 0)),
            "High": int(opp_summary.get("high_priority_opportunities", 0)),
            "Medium": int(opp_summary.get("medium_priority_opportunities", 0)),
            "Low": int(opp_summary.get("low_priority_opportunities", 0)),
        }
    # Fallback: count from portfolio
    portfolio = ed.get("opportunity_portfolio") or {}
    opps = portfolio.get("opportunities") or []
    counts = {"Strategic": 0, "High": 0, "Medium": 0, "Low": 0}
    for o in opps:
        priority = str(o.get("priority", ""))
        if "Strategic" in priority:
            counts["Strategic"] += 1
        elif "High" in priority:
            counts["High"] += 1
        elif "Medium" in priority:
            counts["Medium"] += 1
        elif "Low" in priority:
            counts["Low"] += 1
    return counts


def calculate_roadmap_action_counts(export_data: dict) -> dict:
    """Return action counts by roadmap phase."""
    ed = export_data or {}
    rm_summary = ed.get("implementation_roadmap_summary") or {}
    if rm_summary:
        return {
            "First 30 Days": int(rm_summary.get("day_30_actions", 0)),
            "Days 31–60": int(rm_summary.get("day_60_actions", 0)),
            "Days 61–90": int(rm_summary.get("day_90_actions", 0)),
        }
    # Fallback: count from roadmap
    roadmap = ed.get("implementation_roadmap") or {}
    return {
        "First 30 Days": len(roadmap.get("phase_30_days") or []),
        "Days 31–60": len(roadmap.get("phase_60_days") or []),
        "Days 61–90": len(roadmap.get("phase_90_days") or []),
    }


def calculate_report_quality_summary(export_data: dict) -> dict:
    """Return a quality checklist for the assembled client report."""
    ed = export_data or {}
    cr_md = ed.get("client_report_markdown") or ""
    rs = ed.get("report_sections") or {}
    sections = rs.get("sections") or {} if isinstance(rs, dict) else {}

    def _in_md(term: str) -> bool:
        return term.lower() in cr_md.lower()

    return {
        "executive_summary_included": bool(sections.get("executive_summary"))
        or _in_md("executive summary"),
        "readiness_section_included": bool(sections.get("readiness_interpretation"))
        or _in_md("readiness summary"),
        "risk_section_included": bool(sections.get("risk_summary"))
        or _in_md("risk register"),
        "opportunity_section_included": bool(sections.get("opportunity_summary"))
        or _in_md("opportunity"),
        "roadmap_section_included": bool(sections.get("roadmap_summary"))
        or _in_md("roadmap"),
        "responsible_use_included": _in_md("responsible-use")
        or _in_md("responsible use"),
        "prototype_limitations_included": _in_md("prototype limitations"),
        "human_review_note_included": _in_md("human review"),
    }


def build_client_report_analytics(export_data: dict) -> dict:
    """Build the full analytics dict for the export package."""
    return {
        "completion_status": calculate_export_completion_status(export_data),
        "readiness_score_breakdown": calculate_readiness_score_breakdown(export_data),
        "risk_level_counts": calculate_risk_level_counts(export_data),
        "opportunity_priority_counts": calculate_opportunity_priority_counts(export_data),
        "roadmap_action_counts": calculate_roadmap_action_counts(export_data),
        "report_quality_summary": calculate_report_quality_summary(export_data),
    }
