"""
Report Analytics — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Generates deterministic analytics from Build 6 governance review outputs.
No external AI, LLM, or API calls. Synthetic/demo data only.
"""


def calculate_export_completion_status(export_data: dict) -> dict:
    """Calculate which outputs are available in the export data."""
    checks = {
        "Policy Pack": "policy_pack",
        "Governance Framework": "governance_framework",
        "Coverage Review": "coverage_results",
        "Gap Analysis": "gap_analysis",
        "Recommendations": "policy_recommendations",
        "Governance Maturity": "governance_maturity",
        "Governance Report": "governance_report_markdown",
    }
    available = export_data.get("source_outputs_available", {})

    status: dict[str, bool] = {}
    for label, key in checks.items():
        status[label] = bool(available.get(key)) or bool(export_data.get(key))

    total = len(status)
    complete = sum(1 for v in status.values() if v)

    return {
        "items": status,
        "total": total,
        "complete": complete,
        "incomplete": total - complete,
        "completion_percentage": round((complete / total * 100) if total > 0 else 0, 1),
    }


def calculate_coverage_level_counts(export_data: dict) -> dict:
    """Count domains by coverage level from coverage results."""
    summary = export_data.get("coverage_summary") or {}
    coverage = export_data.get("coverage_results") or {}

    if summary:
        counts = {
            "Strong coverage": summary.get("strong_count", 0),
            "Partial coverage": summary.get("partial_count", 0),
            "Weak coverage": summary.get("weak_count", 0),
            "Not covered": summary.get("not_covered_count", 0),
        }
    else:
        counts = {
            "Strong coverage": 0,
            "Partial coverage": 0,
            "Weak coverage": 0,
            "Not covered": 0,
        }
        for dr in coverage.get("domain_results", []):
            level = dr.get("coverage_level", "")
            if level in counts:
                counts[level] += 1

    total = sum(counts.values())
    return {"counts": counts, "total": total}


def calculate_gap_severity_counts(export_data: dict) -> dict:
    """Count gaps by severity from gap analysis."""
    gap_summary = export_data.get("gap_summary") or {}
    gap_analysis = export_data.get("gap_analysis") or {}

    if gap_summary:
        counts = {
            "Critical gap": gap_summary.get("critical_gap_count", 0),
            "High gap": gap_summary.get("high_gap_count", 0),
            "Medium gap": gap_summary.get("medium_gap_count", 0),
            "Low gap": gap_summary.get("low_gap_count", 0),
        }
    else:
        counts = {"Critical gap": 0, "High gap": 0, "Medium gap": 0, "Low gap": 0}
        for gap in gap_analysis.get("prioritised_gaps", []):
            sev = gap.get("gap_severity", "")
            if sev in counts:
                counts[sev] += 1

    total = sum(counts.values())
    return {"counts": counts, "total": total}


def calculate_recommendation_priority_counts(export_data: dict) -> dict:
    """Count recommendations by priority."""
    rec_summary = export_data.get("recommendation_summary") or {}
    recs = export_data.get("policy_recommendations") or {}

    if rec_summary:
        counts = {
            "Urgent": rec_summary.get("urgent_count", 0),
            "High priority": rec_summary.get("high_priority_count", 0),
            "Medium priority": rec_summary.get("medium_priority_count", 0),
            "Low priority": rec_summary.get("low_priority_count", 0),
        }
    else:
        counts = {"Urgent": 0, "High priority": 0, "Medium priority": 0, "Low priority": 0}
        for rec in recs.get("prioritised_recommendations", []):
            pri = rec.get("recommendation_priority", "")
            if pri in counts:
                counts[pri] += 1

    total = sum(counts.values())
    return {"counts": counts, "total": total}


def calculate_maturity_level_counts(export_data: dict) -> dict:
    """Count domains by maturity level."""
    maturity_sum = export_data.get("governance_maturity_summary") or {}
    maturity = export_data.get("governance_maturity") or {}

    if maturity_sum:
        # managed_or_optimised_domains bundles both; split is not available from summary
        counts = {
            "Initial governance": maturity_sum.get("initial_domains", 0),
            "Developing governance": maturity_sum.get("developing_domains", 0),
            "Defined governance": maturity_sum.get("defined_domains", 0),
            "Managed governance": maturity_sum.get("managed_or_optimised_domains", 0),
            "Optimised governance": 0,
        }
    else:
        counts = {
            "Initial governance": 0,
            "Developing governance": 0,
            "Defined governance": 0,
            "Managed governance": 0,
            "Optimised governance": 0,
        }
        for ds in maturity.get("domain_maturity_scores", []):
            level = ds.get("maturity_level", "")
            if level in counts:
                counts[level] += 1

    total = sum(counts.values())
    return {"counts": counts, "total": total}


def calculate_governance_score_breakdown(export_data: dict) -> dict:
    """Extract governance scores for display and charting."""
    maturity = export_data.get("governance_maturity") or {}
    coverage = export_data.get("coverage_results") or {}

    domain_scores: dict[str, int] = {}
    for ds in maturity.get("domain_maturity_scores", []):
        name = ds.get("domain_name", "")
        if name:
            domain_scores[name] = ds.get("maturity_score", 0)

    return {
        "overall_governance_score": maturity.get("overall_governance_score", 0),
        "overall_coverage_score": coverage.get("overall_coverage_score", 0),
        "overall_maturity_level": maturity.get("overall_maturity_level", ""),
        "overall_coverage_level": coverage.get("overall_coverage_level", ""),
        "domain_maturity_scores": domain_scores,
    }


def calculate_report_quality_summary(export_data: dict) -> dict:
    """Check which sections are present in the governance report Markdown."""
    markdown = (export_data.get("governance_report_markdown") or "").lower()

    def contains(phrase: str) -> bool:
        return phrase.lower() in markdown

    checks = {
        "executive_summary_included": contains("executive summary"),
        "policy_pack_overview_included": contains("policy pack overview"),
        "framework_section_included": contains("governance framework"),
        "coverage_section_included": contains("policy coverage review"),
        "gap_analysis_section_included": contains("gap analysis"),
        "recommendations_section_included": contains("policy improvement recommendations"),
        "maturity_section_included": contains("maturity summary"),
        "responsible_use_boundaries_included": contains("responsible-use boundaries"),
        "prototype_limitations_included": contains("prototype limitations"),
        "human_review_note_included": contains("human review"),
    }

    total = len(checks)
    present = sum(1 for v in checks.values() if v)

    return {
        **checks,
        "sections_present": present,
        "sections_total": total,
        "quality_percentage": round((present / total * 100) if total > 0 else 0, 1),
    }


def build_governance_report_analytics(export_data: dict) -> dict:
    """Build the complete analytics dict from all available export data."""
    return {
        "export_completion": calculate_export_completion_status(export_data),
        "coverage_levels": calculate_coverage_level_counts(export_data),
        "gap_severities": calculate_gap_severity_counts(export_data),
        "recommendation_priorities": calculate_recommendation_priority_counts(export_data),
        "maturity_levels": calculate_maturity_level_counts(export_data),
        "governance_scores": calculate_governance_score_breakdown(export_data),
        "report_quality": calculate_report_quality_summary(export_data),
    }
