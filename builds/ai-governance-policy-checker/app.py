"""
AI Governance Policy Checker — Build 6
BrightPath ChatGPT Mastery Project

Phases 1–8: Scaffold, synthetic policy data, governance framework coverage checker,
policy gap analysis, policy improvement recommendation engine, governance maturity summary,
governance report builder, Export Centre with Markdown/PDF/charts, and Completion Review
with portfolio notes. All phases complete.
"""

import streamlit as st

from src.sample_policies import get_brightpath_policy_pack
from src.governance_framework import (
    get_responsible_ai_governance_framework,
    summarise_governance_framework,
    format_governance_framework_as_markdown,
)
from src.policy_data_manager import (
    validate_policy_pack,
    summarise_policy_pack,
    format_policy_pack_as_markdown,
)
from src.ui_components import (
    apply_global_styles,
    render_page_header,
    render_responsible_use_warning,
    render_prototype_notice,
    render_metric_row,
    render_completion_badge,
    render_workflow_steps,
)
from src.policy_checker import (
    check_policy_pack_coverage,
    summarise_policy_coverage,
    format_policy_coverage_as_markdown,
)
from src.gap_analysis import (
    generate_policy_gap_analysis,
    summarise_gap_analysis,
    format_gap_analysis_as_markdown,
)
from src.recommendation_engine import (
    generate_policy_recommendations,
    summarise_policy_recommendations,
    format_policy_recommendations_as_markdown,
)
from src.governance_maturity import (
    generate_governance_maturity_summary,
    summarise_governance_maturity,
    format_governance_maturity_as_markdown,
)
from src.report_builder import (
    check_governance_report_readiness,
    build_governance_report_data_from_session_state,
    generate_markdown_governance_report,
    summarise_governance_report,
    create_governance_report_filename,
    get_governance_report_optional_sections,
)
from src.export_centre import (
    check_export_readiness,
    build_export_data_from_session_state,
    generate_export_quality_checklist,
    summarise_export_package,
    prepare_markdown_export,
    prepare_pdf_export,
)
from src.report_analytics import build_governance_report_analytics
from src.chart_utils import generate_all_export_charts
from src.completion_review import (
    generate_build6_completion_review,
    generate_portfolio_summary,
    generate_case_study_summary,
    format_completion_review_as_markdown,
    format_portfolio_notes_as_markdown,
)

st.set_page_config(
    page_title="AI Governance Policy Checker",
    page_icon="🏛️",
    layout="wide",
)

apply_global_styles()

PAGES = [
    "Home",
    "Policy Library",
    "Governance Framework",
    "Policy Checker",
    "Gap Analysis",
    "Recommendations",
    "Governance Maturity",
    "Governance Report",
    "Export Centre",
    "Completion Review",
]

WORKFLOW_STEPS = [
    "Synthetic Policies",
    "Governance Framework",
    "Policy Coverage Review",
    "Gap Analysis",
    "Recommendations",
    "Governance Maturity",
    "Governance Report",
    "Export",
]


def render_sidebar():
    st.sidebar.title("AI Governance Policy Checker")
    st.sidebar.markdown("*Build 6 · BrightPath ChatGPT Mastery*")
    st.sidebar.divider()
    page = st.sidebar.radio("Navigate", PAGES)
    st.sidebar.divider()
    st.sidebar.markdown("**Progress**")
    render_completion_badge("Policy Library", "policy_pack" in st.session_state)
    render_completion_badge("Governance Framework", "governance_framework" in st.session_state)
    render_completion_badge("Policy Checker", "coverage_results" in st.session_state)
    render_completion_badge("Gap Analysis", "gap_analysis" in st.session_state)
    render_completion_badge("Recommendations", "policy_recommendations" in st.session_state)
    render_completion_badge("Governance Maturity", "governance_maturity" in st.session_state)
    render_completion_badge("Governance Report", "governance_report_markdown" in st.session_state)
    render_completion_badge("Export Centre", "export_data" in st.session_state)
    render_completion_badge("Completion Review", "completion_review" in st.session_state)
    st.sidebar.divider()
    st.sidebar.caption(
        "Synthetic data only. Not legal, safeguarding, HR, or compliance advice."
    )
    return page


def page_home():
    render_page_header(
        "AI Governance Policy Checker",
        "Build 6 · BrightPath ChatGPT Mastery Project",
    )
    render_prototype_notice()
    st.markdown("""
## What This Tool Does

The AI Governance Policy Checker is a portfolio-ready Streamlit prototype that helps an AI
consultant review whether a synthetic organisation's AI-related policies contain sufficient
responsible-use governance coverage.

It works through a structured governance review workflow:
    """)
    render_workflow_steps(WORKFLOW_STEPS, current_step=0)
    st.markdown("""
---

## Governance Review Workflow

| Step | Purpose |
|---|---|
| Policy Library | Load and preview the synthetic organisation's AI policy pack |
| Governance Framework | Load the responsible AI governance framework |
| Policy Checker | Compare policy text against each governance domain *(Phase 2)* |
| Gap Analysis | Identify missing, weak, and partially covered governance areas *(Phase 3)* |
| Recommendations | Generate policy improvement recommendations *(Phase 4)* |
| Governance Maturity | Governance maturity score, domain-level breakdown, and adoption readiness *(Phase 5)* |
| Governance Report | Assemble a client-facing governance review report *(Phase 6)* |
| Export Centre | Export Markdown and PDF reports with analytics and charts *(Phase 7)* |

---

## How This Connects to Builds 1–5

| Build | Connection |
|---|---|
| Build 1 · AI Readiness Audit | Readiness findings highlight governance gaps that this tool checks |
| Build 2 · Document Intelligence RAG Demo | Policy documents reviewed here could be retrieved as evidence in a RAG pipeline |
| Build 3 · Semantic RAG Policy Assistant | Future integration: retrieve policy evidence to support governance checks |
| Build 4 · AI Staff Training Generator | Training needs identified here can feed directly into Build 4 |
| Build 5 · AI Consulting Report Generator | Governance review outputs can be included in a consulting report |

---

## Responsible-Use Boundaries

- Synthetic/demo organisation data only
- No real client policies, learner data, safeguarding case information
- No staff HR data, personal data, confidential data, or regulated information
- Not legal, safeguarding, HR, compliance, financial, medical, or professional advice
- Not a compliance certification system
- Human review required before any real-world use

---
    """)
    render_responsible_use_warning()


def page_policy_library():
    render_page_header(
        "Policy Library",
        "Load and review the synthetic organisation's AI policy pack",
    )
    render_responsible_use_warning()
    st.markdown(
        "Load the BrightPath Skills Training synthetic policy pack to begin the governance review. "
        "This is synthetic demo content only — not real organisational policies."
    )

    if st.button("Load BrightPath Synthetic Policy Pack", type="primary"):
        policy_pack = get_brightpath_policy_pack()
        is_valid, validation_message = validate_policy_pack(policy_pack)
        if not is_valid:
            st.error(f"Policy pack validation failed: {validation_message}")
            return
        summary = summarise_policy_pack(policy_pack)
        markdown = format_policy_pack_as_markdown(policy_pack)
        st.session_state["policy_pack"] = policy_pack
        st.session_state["policy_pack_summary"] = summary
        st.session_state["policy_pack_markdown"] = markdown
        st.success("BrightPath synthetic policy pack loaded.")

    if "policy_pack" not in st.session_state:
        st.info("Click the button above to load the synthetic policy pack.")
        return

    policy_pack = st.session_state["policy_pack"]
    summary = st.session_state["policy_pack_summary"]

    st.markdown("---")
    st.markdown(f"### {policy_pack['organisation_name']}")
    st.caption(
        f"{policy_pack.get('organisation_type', '')} · "
        f"{policy_pack.get('sector', '')} · "
        f"{policy_pack.get('country_context', '')}"
    )

    render_metric_row([
        {"label": "Total Policies", "value": summary["total_policies"]},
        {"label": "Policy Types", "value": len(summary["policy_types"])},
        {"label": "Risk Areas", "value": len(summary["risk_areas"])},
    ])

    st.markdown("---")
    st.markdown("### Policies")
    for policy in policy_pack["policies"]:
        with st.expander(f"{policy['policy_id']} — {policy['policy_title']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type:** {policy.get('policy_type', '')}")
                st.markdown(f"**Owner:** {policy.get('owner', '')}")
            with col2:
                st.markdown(f"**Status:** {policy.get('status', '')}")
                st.markdown(f"**Last reviewed:** {policy.get('last_reviewed', '')}")
            st.markdown("**Summary:**")
            st.markdown(policy.get("summary", ""))
            st.markdown("**Related risk areas:**")
            for area in policy.get("related_risk_areas", []):
                st.markdown(f"- {area}")

    st.markdown("---")
    st.markdown("### Risk Areas Covered")
    for area in summary["risk_areas"]:
        st.markdown(f"- {area}")

    st.markdown("---")
    st.markdown("### Policy Pack Markdown Preview")
    st.download_button(
        label="Download Policy Pack Markdown",
        data=st.session_state["policy_pack_markdown"],
        file_name="brightpath-synthetic-policy-pack.md",
        mime="text/markdown",
    )
    with st.expander("Preview Markdown"):
        st.text(st.session_state["policy_pack_markdown"])

    st.markdown("---")
    st.warning(
        "**Synthetic data only.** This policy pack is demo content for portfolio demonstration. "
        "Not an approved organisational policy."
    )


def page_governance_framework():
    render_page_header(
        "Governance Framework",
        "Responsible AI governance domains for policy review",
    )
    render_responsible_use_warning()
    st.markdown(
        "Load the responsible AI governance framework. This framework defines the governance "
        "domains that the policy checker will use to assess the synthetic policy pack."
    )

    if st.button("Load Responsible AI Governance Framework", type="primary"):
        framework = get_responsible_ai_governance_framework()
        summary = summarise_governance_framework(framework)
        markdown = format_governance_framework_as_markdown(framework)
        st.session_state["governance_framework"] = framework
        st.session_state["governance_framework_summary"] = summary
        st.session_state["governance_framework_markdown"] = markdown
        st.success("Governance framework loaded.")

    if "governance_framework" not in st.session_state:
        st.info("Click the button above to load the governance framework.")
        return

    framework = st.session_state["governance_framework"]
    summary = st.session_state["governance_framework_summary"]

    st.markdown("---")
    st.markdown("### Framework Overview")
    render_metric_row([
        {"label": "Total Domains", "value": summary["total_domains"]},
        {"label": "High Priority", "value": summary["high_priority_count"]},
        {"label": "Medium Priority", "value": summary["medium_priority_count"]},
    ])

    st.markdown("---")
    st.markdown("### Governance Domains")

    priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    for domain in framework:
        icon = priority_icons.get(domain["priority_level"], "⬜")
        label = (
            f"{icon} {domain['domain_id']} — {domain['domain_name']} "
            f"({domain['priority_level']} priority)"
        )
        with st.expander(label):
            st.markdown(domain["description"])
            st.markdown(f"**Why it matters:** {domain['why_it_matters']}")
            st.markdown("**Expected policy evidence:**")
            for item in domain.get("expected_policy_evidence", []):
                st.markdown(f"- {item}")
            st.markdown("**Example controls:**")
            for item in domain.get("example_controls", []):
                st.markdown(f"- {item}")

    st.markdown("---")
    st.download_button(
        label="Download Framework Markdown",
        data=st.session_state["governance_framework_markdown"],
        file_name="responsible-ai-governance-framework.md",
        mime="text/markdown",
    )


def page_policy_checker():
    render_page_header(
        "Policy Checker",
        "Compare synthetic policy text against the governance framework",
    )
    render_responsible_use_warning()

    if "policy_pack" not in st.session_state:
        st.error("**Policy pack not loaded.** Please complete the following steps:")
        st.markdown(
            "1. Go to **Policy Library**.\n"
            "2. Click **Load BrightPath Synthetic Policy Pack**.\n"
            "3. Return to **Policy Checker**."
        )
        return

    if "governance_framework" not in st.session_state:
        st.error("**Governance framework not loaded.** Please complete the following steps:")
        st.markdown(
            "1. Go to **Governance Framework**.\n"
            "2. Click **Load Responsible AI Governance Framework**.\n"
            "3. Return to **Policy Checker**."
        )
        return

    policy_pack = st.session_state["policy_pack"]
    framework = st.session_state["governance_framework"]

    if st.button("Run Policy Coverage Check", type="primary"):
        with st.spinner("Checking policy coverage against 12 governance domains..."):
            coverage_results = check_policy_pack_coverage(policy_pack, framework)
            coverage_summary = summarise_policy_coverage(coverage_results)
            coverage_markdown = format_policy_coverage_as_markdown(
                coverage_results, coverage_summary
            )
            st.session_state["coverage_results"] = coverage_results
            st.session_state["coverage_summary"] = coverage_summary
            st.session_state["coverage_markdown"] = coverage_markdown
        st.success("Policy coverage check complete.")

    if "coverage_results" not in st.session_state:
        st.info(
            "Click **Run Policy Coverage Check** above to compare the synthetic policy pack "
            "against the 12 responsible AI governance domains."
        )
        return

    results = st.session_state["coverage_results"]
    summary = st.session_state["coverage_summary"]

    # Overall metrics
    st.markdown("---")
    st.markdown("### Overall Coverage")
    render_metric_row([
        {"label": "Overall Score", "value": f"{results['overall_coverage_score']}/100"},
        {"label": "Coverage Level", "value": results["overall_coverage_level"]},
        {"label": "Policies Reviewed", "value": results["total_policies_reviewed"]},
        {"label": "Domains Checked", "value": results["total_domains_checked"]},
    ])
    st.progress(int(results["overall_coverage_score"]) / 100)

    # Coverage counts
    st.markdown("---")
    st.markdown("### Coverage Counts")
    render_metric_row([
        {"label": "Strong Coverage", "value": summary["strong_count"]},
        {"label": "Partial Coverage", "value": summary["partial_count"]},
        {"label": "Weak Coverage", "value": summary["weak_count"]},
        {"label": "Not Covered", "value": summary["not_covered_count"]},
    ])

    # High-priority gaps
    st.markdown("---")
    st.markdown("### High-Priority Gaps")
    high_priority_gaps = summary.get("high_priority_gaps", [])
    if high_priority_gaps:
        for gap in high_priority_gaps:
            st.markdown(f"- 🔴 {gap}")
    else:
        st.success("No high-priority gaps identified in the synthetic policy pack.")

    # Recommended focus
    st.markdown("---")
    st.markdown("### Recommended Focus Areas")
    for focus in summary.get("recommended_focus", []):
        st.markdown(f"- {focus}")

    # Best and weakest side by side
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Best-Covered Domains")
        for domain in summary.get("best_covered_domains", []):
            st.markdown(f"- ✅ {domain}")
    with col2:
        st.markdown("### Weakest Domains")
        for domain in summary.get("weakest_domains", []):
            st.markdown(f"- ⚠️ {domain}")

    # Domain coverage detail
    st.markdown("---")
    st.markdown("### Domain Coverage Review")

    level_icons = {
        "Strong coverage": "✅",
        "Partial coverage": "🟡",
        "Weak coverage": "🔶",
        "Not covered": "❌",
    }
    priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    for result in results["domain_results"]:
        level = result["coverage_level"]
        priority = result["priority_level"]
        icon = level_icons.get(level, "⬜")
        p_icon = priority_icons.get(priority, "⬜")
        score_val = result["coverage_score"]
        label = (
            f"{icon} {result['domain_id']} — {result['domain_name']} "
            f"({score_val}/100)"
        )
        with st.expander(label):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**Priority:** {p_icon} {priority}")
                st.markdown(f"**Score:** {score_val}/100")
                st.markdown(f"**Level:** {level}")
            with col_b:
                matched = result.get("matched_policies", [])
                st.markdown(
                    f"**Matched policies:** {', '.join(matched)}"
                    if matched else "**Matched policies:** None found"
                )
            keywords = result.get("matched_keywords", [])
            if keywords:
                st.markdown(f"**Matched keywords:** {', '.join(keywords[:10])}")
            snippets = result.get("evidence_snippets", [])
            if snippets:
                st.markdown("**Evidence snippets:**")
                for snippet in snippets[:3]:
                    st.markdown(f"> *{snippet}*")
            st.info(result.get("coverage_explanation", ""))
            st.caption(result.get("review_note", ""))

    # Download
    st.markdown("---")
    st.download_button(
        label="Download Coverage Review Markdown",
        data=st.session_state["coverage_markdown"],
        file_name="brightpath-policy-coverage-review.md",
        mime="text/markdown",
    )


def page_gap_analysis():
    render_page_header(
        "Gap Analysis",
        "Identify missing, weak, and partially covered governance areas",
    )
    render_responsible_use_warning()

    if "coverage_results" not in st.session_state:
        st.error("**Coverage results not found.** Please complete the following steps first:")
        st.markdown(
            "1. Go to **Policy Library** and load the BrightPath synthetic policy pack.\n"
            "2. Go to **Governance Framework** and load the governance framework.\n"
            "3. Go to **Policy Checker** and run the policy coverage check.\n"
            "4. Return to **Gap Analysis**."
        )
        return

    coverage_results = st.session_state["coverage_results"]

    if "gap_analysis" not in st.session_state:
        with st.spinner("Generating gap analysis across all governance domains..."):
            gap_analysis = generate_policy_gap_analysis(coverage_results)
            gap_summary = summarise_gap_analysis(gap_analysis)
            gap_markdown = format_gap_analysis_as_markdown(gap_analysis, gap_summary)
            st.session_state["gap_analysis"] = gap_analysis
            st.session_state["gap_summary"] = gap_summary
            st.session_state["gap_analysis_markdown"] = gap_markdown
        st.success("Gap analysis complete.")

    gap_analysis = st.session_state["gap_analysis"]
    gap_summary = st.session_state["gap_summary"]

    # Summary metrics
    st.markdown("---")
    st.markdown("### Gap Summary")
    render_metric_row([
        {"label": "Total Gaps", "value": gap_summary["total_gaps"]},
        {"label": "Critical Gaps", "value": gap_summary["critical_gap_count"]},
        {"label": "High Gaps", "value": gap_summary["high_gap_count"]},
        {"label": "Medium Gaps", "value": gap_summary["medium_gap_count"]},
    ])
    render_metric_row([
        {"label": "Low Gaps", "value": gap_summary["low_gap_count"]},
        {"label": "Domains Covered", "value": gap_summary["covered_domain_count"]},
        {"label": "Domains Reviewed", "value": gap_analysis["total_domains_reviewed"]},
        {"label": "Overall Score", "value": f"{gap_analysis['overall_coverage_score']}/100"},
    ])

    # Overall gap position
    st.markdown("---")
    st.markdown("### Overall Gap Position")
    if gap_summary["critical_gap_count"] > 0 or gap_summary["high_gap_count"] > 0:
        st.error(gap_summary["overall_gap_position"])
    elif gap_summary["medium_gap_count"] > 0 or gap_summary["low_gap_count"] > 0:
        st.warning(gap_summary["overall_gap_position"])
    else:
        st.success(gap_summary["overall_gap_position"])

    # Highest priority gap
    highest = gap_summary.get("highest_priority_gap", {})
    if highest:
        st.markdown("---")
        st.markdown("### Highest Priority Gap")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{highest.get('gap_id', '')}**")
            st.markdown(highest.get("domain_name", ""))
        with col2:
            st.markdown(f"**Severity:** {highest.get('gap_severity', '')}")
            st.markdown(f"**Priority:** {highest.get('priority_level', '')}")
        with col3:
            st.markdown(f"**Score:** {highest.get('coverage_score', 0)}/100")
            st.markdown(f"**Priority score:** {highest.get('gap_priority_score', 0)}/100")

    # Recommended focus
    st.markdown("---")
    st.markdown("### Recommended Focus Areas")
    for focus in gap_summary.get("recommended_focus", []):
        st.markdown(f"- {focus}")

    # Gap themes
    st.markdown("---")
    st.markdown("### Gap Themes")
    themes = gap_summary.get("gap_themes", [])
    if themes:
        cols = st.columns(min(len(themes), 3))
        for i, theme in enumerate(themes):
            cols[i % 3].markdown(f"- {theme}")
    else:
        st.info("No gap themes identified.")

    # Prioritised gap table
    st.markdown("---")
    st.markdown("### Prioritised Gap Table")
    prioritised = gap_analysis.get("prioritised_gaps", [])
    if prioritised:
        severity_icons = {
            "Critical gap": "🔴",
            "High gap": "🟠",
            "Medium gap": "🟡",
            "Low gap": "🟢",
        }
        for gap in prioritised:
            sev = gap.get("gap_severity", "")
            icon = severity_icons.get(sev, "⬜")
            score = gap.get("coverage_score", 0)
            label = (
                f"{icon} {gap.get('gap_id', '')} — {gap.get('domain_name', '')} "
                f"({sev} · {gap.get('priority_level', '')} priority · {score}/100)"
            )
            with st.expander(label):
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.markdown(f"**Gap ID:** {gap.get('gap_id', '')}")
                    st.markdown(f"**Severity:** {sev}")
                    st.markdown(f"**Gap type:** {gap.get('gap_type', '')}")
                    st.markdown(f"**Priority score:** {gap.get('gap_priority_score', 0)}/100")
                with col_b:
                    st.markdown(f"**Coverage score:** {score}/100")
                    st.markdown(f"**Coverage level:** {gap.get('coverage_level', '')}")
                    matched = gap.get("matched_policies", [])
                    st.markdown(
                        f"**Matched policies:** {', '.join(matched)}"
                        if matched else "**Matched policies:** None found"
                    )
                st.markdown("**Missing evidence:**")
                st.markdown(gap.get("missing_evidence", ""))
                st.markdown("**Risk statement:**")
                st.info(gap.get("risk_statement", ""))
                st.markdown("**Action hint:**")
                st.markdown(f"> {gap.get('action_hint', '')}")
                snippets = gap.get("evidence_snippets", [])
                if snippets:
                    st.markdown("**Evidence snippets:**")
                    for snippet in snippets:
                        st.markdown(f"> *{snippet}*")
                st.caption(gap.get("review_note", ""))
    else:
        st.success("No gaps identified. All domains appear to have sufficient coverage.")

    # Covered domains
    st.markdown("---")
    st.markdown("### Domains with Sufficient Coverage")
    covered = gap_analysis.get("covered_domains", [])
    if covered:
        for domain in covered:
            st.markdown(
                f"✅ **{domain.get('domain_name', '')}** — "
                f"{domain.get('coverage_score', 0)}/100 · {domain.get('priority_level', '')} priority"
            )
    else:
        st.info("No domains with strong coverage identified in this review.")

    # Download
    st.markdown("---")
    st.download_button(
        label="Download Gap Analysis Markdown",
        data=st.session_state["gap_analysis_markdown"],
        file_name="brightpath-policy-gap-analysis.md",
        mime="text/markdown",
    )
    st.caption(
        "This gap analysis is a deterministic review of synthetic policy text only. "
        "Not legal, safeguarding, HR, compliance, or professional governance advice. "
        "Human review required before any real-world use."
    )


def page_recommendations():
    render_page_header(
        "Recommendations",
        "Policy improvement recommendations from gap analysis",
    )
    render_responsible_use_warning()

    if "gap_analysis" not in st.session_state:
        st.error("**Gap analysis not found.** Please complete the following steps first:")
        st.markdown(
            "1. Go to **Policy Library** and load the BrightPath synthetic policy pack.\n"
            "2. Go to **Governance Framework** and load the governance framework.\n"
            "3. Go to **Policy Checker** and run the policy coverage check.\n"
            "4. Go to **Gap Analysis** and generate the gap analysis.\n"
            "5. Return to **Recommendations**."
        )
        return

    gap_analysis = st.session_state["gap_analysis"]
    policy_pack = st.session_state.get("policy_pack")

    if "policy_recommendations" not in st.session_state:
        with st.spinner("Generating policy improvement recommendations..."):
            recommendations = generate_policy_recommendations(gap_analysis, policy_pack)
            rec_summary = summarise_policy_recommendations(recommendations)
            rec_markdown = format_policy_recommendations_as_markdown(
                recommendations, rec_summary
            )
            st.session_state["policy_recommendations"] = recommendations
            st.session_state["recommendation_summary"] = rec_summary
            st.session_state["policy_recommendations_markdown"] = rec_markdown
        st.success("Recommendations generated.")

    recommendations = st.session_state["policy_recommendations"]
    rec_summary = st.session_state["recommendation_summary"]

    # Summary metrics
    st.markdown("---")
    st.markdown("### Recommendation Summary")
    render_metric_row([
        {"label": "Total Recommendations", "value": rec_summary["total_recommendations"]},
        {"label": "Urgent", "value": rec_summary["urgent_count"]},
        {"label": "High Priority", "value": rec_summary["high_priority_count"]},
        {"label": "Medium Priority", "value": rec_summary["medium_priority_count"]},
    ])
    render_metric_row([
        {"label": "Low Priority", "value": rec_summary["low_priority_count"]},
        {"label": "Quick Wins", "value": rec_summary["quick_win_count"]},
        {"label": "Total Gaps Addressed", "value": recommendations["total_recommendations"]},
        {"label": "Policy Pack", "value": recommendations.get("organisation_name", "")},
    ])

    # Overall recommendation position
    st.markdown("---")
    st.markdown("### Overall Recommendation Position")
    position = rec_summary.get("overall_recommendation_position", "")
    if rec_summary["urgent_count"] > 0 or rec_summary["high_priority_count"] > 0:
        st.error(position)
    elif rec_summary["medium_priority_count"] > 0:
        st.warning(position)
    else:
        st.success(position)

    # Highest priority recommendation
    highest = rec_summary.get("highest_priority_recommendation", {})
    if highest:
        st.markdown("---")
        st.markdown("### Highest Priority Recommendation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{highest.get('recommendation_id', '')}**")
            st.markdown(highest.get("recommendation_title", ""))
        with col2:
            st.markdown(f"**Priority:** {highest.get('recommendation_priority', '')}")
            st.markdown(f"**Action:** {highest.get('policy_action_type', '')}")
        with col3:
            st.markdown(f"**Target:** {highest.get('target_policy', '')}")
            st.markdown(f"**Owner:** {highest.get('suggested_owner', '')}")

    # Recommended focus
    st.markdown("---")
    st.markdown("### Recommended Focus Areas")
    for focus in rec_summary.get("recommended_focus", []):
        st.markdown(f"- {focus}")

    # Recommended sequence
    st.markdown("---")
    st.markdown("### Recommended Sequence")
    for seq in recommendations.get("recommended_sequence", []):
        step_num = seq.get("sequence_step", "")
        title = seq.get("title", "")
        reason = seq.get("reason", "")
        rec_ids = seq.get("recommendations", [])
        with st.expander(f"Step {step_num}: {title}"):
            st.markdown(f"*{reason}*")
            st.markdown(f"**Recommendations:** {', '.join(rec_ids)}")

    # Quick wins
    st.markdown("---")
    st.markdown("### Quick Wins")
    quick_wins = recommendations.get("quick_wins", [])
    if quick_wins:
        for qw in quick_wins:
            st.markdown(
                f"- **{qw.get('recommendation_id', '')}** — "
                f"{qw.get('recommendation_title', '')} "
                f"({qw.get('recommendation_priority', '')})"
            )
    else:
        st.info("No quick wins identified from the current gap analysis.")

    # Policy update themes
    st.markdown("---")
    st.markdown("### Policy Update Themes")
    themes = rec_summary.get("top_policy_update_themes", [])
    if themes:
        cols = st.columns(min(len(themes), 3))
        for i, theme in enumerate(themes):
            cols[i % 3].markdown(f"- {theme}")

    # Owner summary
    st.markdown("---")
    st.markdown("### Owner Summary")
    owner_summary = recommendations.get("owner_summary", {})
    if owner_summary:
        for owner, rec_ids in owner_summary.items():
            st.markdown(f"**{owner}:** {', '.join(rec_ids)}")
    else:
        st.info("No owner assignments identified.")

    # Prioritised recommendations table
    st.markdown("---")
    st.markdown("### Prioritised Recommendations")
    priority_icons = {
        "Urgent": "🔴",
        "High priority": "🟠",
        "Medium priority": "🟡",
        "Low priority": "🟢",
    }
    prioritised = recommendations.get("prioritised_recommendations", [])
    if prioritised:
        for rec in prioritised:
            p = rec.get("recommendation_priority", "")
            icon = priority_icons.get(p, "⬜")
            label = (
                f"{icon} {rec.get('recommendation_id', '')} — "
                f"{rec.get('recommendation_title', '')} ({p})"
            )
            with st.expander(label):
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.markdown(f"**Priority:** {p}")
                    st.markdown(f"**Action:** {rec.get('policy_action_type', '')}")
                    st.markdown(f"**Gap:** {rec.get('related_gap_id', '')}")
                    st.markdown(f"**Priority score:** {rec.get('gap_priority_score', 0)}/100")
                with col_b:
                    st.markdown(f"**Target policy:** {rec.get('target_policy', '')}")
                    st.markdown(f"**Suggested owner:** {rec.get('suggested_owner', '')}")
                st.markdown("**Rationale:**")
                st.info(rec.get("rationale", ""))
                st.markdown("**Wording direction:**")
                st.markdown(f"> {rec.get('suggested_wording_direction', '')}")
                st.markdown("**Implementation steps:**")
                for step in rec.get("implementation_steps", []):
                    st.markdown(f"- {step}")
                with st.expander("Review questions and success criteria"):
                    st.markdown("**Review questions:**")
                    for q in rec.get("review_questions", []):
                        st.markdown(f"- {q}")
                    st.markdown("**Success criteria:**")
                    for c in rec.get("success_criteria", []):
                        st.markdown(f"- {c}")
                st.caption(rec.get("review_note", ""))
    else:
        st.success(
            "No policy improvement recommendations generated — all domains appear "
            "to have sufficient coverage."
        )

    # Download
    st.markdown("---")
    st.download_button(
        label="Download Recommendations Markdown",
        data=st.session_state["policy_recommendations_markdown"],
        file_name="brightpath-policy-improvement-recommendations.md",
        mime="text/markdown",
    )
    st.caption(
        "These recommendations are generated from synthetic/demo policy text only. "
        "Wording directions are not legally approved text. "
        "Human review required before any real-world use."
    )


def page_governance_maturity():
    render_page_header(
        "Governance Maturity",
        "Overall AI governance maturity score and domain-level maturity summary",
    )
    render_responsible_use_warning()

    if "coverage_results" not in st.session_state:
        st.error("**Coverage results not found.** Please complete the following steps first:")
        st.markdown(
            "1. Go to **Policy Library** and load the BrightPath synthetic policy pack.\n"
            "2. Go to **Governance Framework** and load the governance framework.\n"
            "3. Go to **Policy Checker** and run the policy coverage check.\n"
            "4. Return to **Governance Maturity**."
        )
        return

    if "gap_analysis" not in st.session_state or "policy_recommendations" not in st.session_state:
        st.info(
            "Run **Gap Analysis** and **Recommendations** first for a richer maturity summary. "
            "A basic maturity score can still be generated from coverage results only."
        )

    coverage_results = st.session_state["coverage_results"]
    gap_analysis = st.session_state.get("gap_analysis")
    recommendations = st.session_state.get("policy_recommendations")

    if "governance_maturity" not in st.session_state:
        with st.spinner("Calculating governance maturity scores across all domains..."):
            maturity_summary = generate_governance_maturity_summary(
                coverage_results, gap_analysis, recommendations
            )
            maturity_sum = summarise_governance_maturity(maturity_summary)
            maturity_markdown = format_governance_maturity_as_markdown(
                maturity_summary, maturity_sum
            )
            st.session_state["governance_maturity"] = maturity_summary
            st.session_state["governance_maturity_summary"] = maturity_sum
            st.session_state["governance_maturity_markdown"] = maturity_markdown
        st.success("Governance maturity summary generated.")

    maturity_summary = st.session_state["governance_maturity"]
    maturity_sum = st.session_state["governance_maturity_summary"]

    # Overall metrics
    st.markdown("---")
    st.markdown("### Overall Governance Score")
    render_metric_row([
        {"label": "Governance Score", "value": f"{maturity_summary['overall_governance_score']}/100"},
        {"label": "Maturity Level", "value": maturity_summary["overall_maturity_level"]},
        {"label": "Total Domains", "value": maturity_sum["total_domains"]},
        {"label": "Maturity Blockers", "value": maturity_sum["blocker_count"]},
    ])
    st.progress(int(maturity_summary["overall_governance_score"]) / 100)

    render_metric_row([
        {"label": "Managed/Optimised", "value": maturity_sum["managed_or_optimised_domains"]},
        {"label": "Defined", "value": maturity_sum["defined_domains"]},
        {"label": "Developing", "value": maturity_sum["developing_domains"]},
        {"label": "Initial", "value": maturity_sum["initial_domains"]},
    ])

    # Maturity level and description
    st.markdown("---")
    st.markdown("### Maturity Level")
    level = maturity_summary["overall_maturity_level"]
    score = maturity_summary["overall_governance_score"]
    if score >= 75:
        st.success(f"**{level}** — {maturity_summary['maturity_description']}")
    elif score >= 50:
        st.info(f"**{level}** — {maturity_summary['maturity_description']}")
    elif score >= 25:
        st.warning(f"**{level}** — {maturity_summary['maturity_description']}")
    else:
        st.error(f"**{level}** — {maturity_summary['maturity_description']}")

    # Adoption readiness
    st.markdown("---")
    st.markdown("### Adoption Readiness Position")
    blockers = maturity_summary.get("maturity_blockers", [])
    critical_blockers = [
        b for b in blockers if b.get("blocker_type") in ("Critical gap", "High gap")
    ]
    if critical_blockers:
        st.error(maturity_summary["adoption_readiness_position"])
    elif score >= 75:
        st.success(maturity_summary["adoption_readiness_position"])
    elif score >= 50:
        st.info(maturity_summary["adoption_readiness_position"])
    else:
        st.warning(maturity_summary["adoption_readiness_position"])

    # Recommended next step
    st.markdown("---")
    st.markdown("### Recommended Next Step")
    st.markdown(f"> {maturity_summary['recommended_next_step']}")

    # Strengths and weaknesses side by side
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Governance Strengths")
        strengths = maturity_summary.get("maturity_strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(
                    f"✅ **{s.get('domain_name', '')}** — "
                    f"{s.get('maturity_score', 0)}/100"
                )
        else:
            st.info("No domains currently meeting the strength threshold (75+).")
    with col2:
        st.markdown("### Governance Weaknesses")
        weaknesses = maturity_summary.get("maturity_weaknesses", [])
        if weaknesses:
            for w in weaknesses:
                st.markdown(
                    f"⚠️ **{w.get('domain_name', '')}** — "
                    f"{w.get('maturity_score', 0)}/100"
                )
        else:
            st.success("No domains below the weakness threshold (<50).")

    # Maturity blockers
    st.markdown("---")
    st.markdown("### Maturity Blockers")
    if blockers:
        for b in blockers:
            btype = b.get("blocker_type", "")
            if btype in ("Critical gap", "High gap"):
                icon = "🔴"
            else:
                icon = "🟠"
            with st.expander(
                f"{icon} {b.get('blocker_id', '')} — {b.get('domain_name', '')} ({btype})"
            ):
                st.markdown(f"**Reason:** {b.get('reason', '')}")
                st.markdown(f"**Recommended action:** {b.get('recommended_action', '')}")
    else:
        st.success("No maturity blockers identified from the current gap analysis.")

    # Improvement priorities
    st.markdown("---")
    st.markdown("### Improvement Priorities")
    priorities = maturity_summary.get("improvement_priorities", [])
    if priorities:
        for p in priorities:
            st.markdown(f"- {p}")
    else:
        st.info("No improvement priorities generated.")

    # Domain maturity table
    st.markdown("---")
    st.markdown("### Domain Maturity Scores")

    level_icons = {
        "Optimised governance": "✅",
        "Managed governance": "🟢",
        "Defined governance": "🔵",
        "Developing governance": "🟡",
        "Initial governance": "🔴",
    }
    priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    domain_scores = maturity_summary.get("domain_maturity_scores", [])
    for ds in sorted(domain_scores, key=lambda x: x.get("maturity_score", 0)):
        ml = ds.get("maturity_level", "")
        icon = level_icons.get(ml, "⬜")
        p_icon = priority_icons.get(ds.get("priority_level", ""), "⬜")
        ms = ds.get("maturity_score", 0)
        label = (
            f"{icon} {ds.get('domain_id', '')} — {ds.get('domain_name', '')} "
            f"({ms}/100 · {ml})"
        )
        with st.expander(label):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**Priority:** {p_icon} {ds.get('priority_level', '')}")
                st.markdown(f"**Coverage score:** {ds.get('coverage_score', 0)}/100")
                st.markdown(f"**Coverage level:** {ds.get('coverage_level', '')}")
                st.markdown(f"**Maturity score:** {ms}/100")
                st.markdown(f"**Maturity level:** {ml}")
            with col_b:
                gap_sev = ds.get("related_gap_severity", "")
                rec_pri = ds.get("related_recommendation_priority", "")
                if gap_sev:
                    st.markdown(f"**Related gap:** {gap_sev}")
                if rec_pri:
                    st.markdown(f"**Related recommendation:** {rec_pri}")
            st.info(ds.get("maturity_explanation", ""))
            st.markdown(f"**Recommended focus:** {ds.get('recommended_focus', '')}")

    # Download
    st.markdown("---")
    st.download_button(
        label="Download Governance Maturity Markdown",
        data=st.session_state["governance_maturity_markdown"],
        file_name="brightpath-governance-maturity-summary.md",
        mime="text/markdown",
    )
    st.caption(
        "This maturity summary is generated from synthetic/demo policy text only. "
        "Not a compliance certification, audit opinion, legal assessment, or professional "
        "governance judgement. Human review required before any real-world use."
    )


def page_governance_report():
    render_page_header(
        "Governance Report",
        "Assemble a complete client-facing AI governance policy review report",
    )
    render_responsible_use_warning()

    if "policy_pack" not in st.session_state:
        st.error("**Policy pack not found.** Please complete the following steps first:")
        st.markdown(
            "1. Go to **Policy Library** and load the BrightPath synthetic policy pack.\n"
            "2. Return to **Governance Report**."
        )
        return

    # Readiness check
    readiness = check_governance_report_readiness(st.session_state)
    st.markdown("---")
    st.markdown("### Report Readiness")

    _report_outputs = [
        ("policy_pack", "Synthetic policy pack loaded"),
        ("governance_framework", "Governance framework loaded"),
        ("coverage_results", "Policy coverage review complete"),
        ("gap_analysis", "Gap analysis complete"),
        ("policy_recommendations", "Recommendations generated"),
        ("governance_maturity", "Governance maturity calculated"),
    ]
    avail_col, miss_col = st.columns(2)
    with avail_col:
        st.markdown("**Available outputs:**")
        for key, label in _report_outputs:
            if key in st.session_state:
                st.markdown(f"✅ {label}")
    with miss_col:
        st.markdown("**Missing recommended outputs:**")
        any_missing = any(k not in st.session_state for k, _ in _report_outputs)
        if any_missing:
            for key, label in _report_outputs:
                if key not in st.session_state:
                    st.markdown(f"❌ {label}")
        else:
            st.markdown("All recommended outputs available.")

    _step_guidance = [
        ("policy_pack", "Go to **Policy Library** and load the BrightPath synthetic policy pack."),
        ("governance_framework", "Go to **Governance Framework** and load the governance framework."),
        ("coverage_results", "Go to **Policy Checker** and run the policy coverage check."),
        ("gap_analysis", "Go to **Gap Analysis** to generate the gap analysis."),
        ("policy_recommendations", "Go to **Recommendations** to generate policy improvement recommendations."),
        ("governance_maturity", "Go to **Governance Maturity** to generate the maturity summary."),
    ]
    missing_steps = [g for k, g in _step_guidance if k not in st.session_state]
    if missing_steps:
        st.markdown("---")
        st.markdown("### Recommended Steps to Complete the Report")
        for step in missing_steps:
            st.markdown(f"- {step}")
        st.info(
            "You can still generate a partial report now — missing sections will show "
            "placeholder notes explaining what to run first."
        )

    # Section selection
    st.markdown("---")
    st.markdown("### Select Report Sections")

    section_labels = {
        "executive_summary": "Executive Summary",
        "policy_pack": "Policy Pack Overview",
        "governance_framework": "Responsible AI Governance Framework",
        "coverage_review": "Policy Coverage Review",
        "gap_analysis": "Policy Gap Analysis",
        "recommendations": "Policy Improvement Recommendations",
        "maturity_summary": "Governance Score and Maturity Summary",
        "next_steps": "Recommended Next Steps",
        "responsible_use": "Responsible-Use Boundaries",
        "prototype_limitations": "Prototype Limitations",
        "appendices": "Appendices",
    }

    # Preselect sections whose underlying data is available
    data_available = {
        "executive_summary": True,
        "policy_pack": "policy_pack" in st.session_state,
        "governance_framework": "governance_framework" in st.session_state,
        "coverage_review": "coverage_results" in st.session_state,
        "gap_analysis": "gap_analysis" in st.session_state,
        "recommendations": "policy_recommendations" in st.session_state,
        "maturity_summary": "governance_maturity" in st.session_state,
        "next_steps": True,
        "responsible_use": True,
        "prototype_limitations": True,
        "appendices": True,
    }

    include_sections = {}
    col1, col2 = st.columns(2)
    section_keys = list(section_labels.keys())
    half = (len(section_keys) + 1) // 2
    for i, key in enumerate(section_keys):
        col = col1 if i < half else col2
        with col:
            include_sections[key] = st.checkbox(
                section_labels[key],
                value=data_available.get(key, True),
                key=f"report_section_{key}",
            )

    st.markdown("---")
    if st.button("Generate Governance Report", type="primary"):
        with st.spinner("Assembling governance report from all available outputs..."):
            report_data = build_governance_report_data_from_session_state(st.session_state)
            report_markdown = generate_markdown_governance_report(report_data, include_sections)
            report_summary = summarise_governance_report(report_data)
            org_name = report_data.get("organisation_name", "organisation")
            filename = create_governance_report_filename(org_name)
            st.session_state["governance_report_data"] = report_data
            st.session_state["governance_report_markdown"] = report_markdown
            st.session_state["governance_report_filename"] = filename
            st.session_state["governance_report_readiness"] = readiness
            st.session_state["governance_report_summary"] = report_summary
        st.success("Governance report generated.")

    if "governance_report_markdown" not in st.session_state:
        st.info("Select sections above and click **Generate Governance Report** to build the report.")
        return

    report_summary = st.session_state["governance_report_summary"]
    report_data = st.session_state["governance_report_data"]
    maturity = report_data.get("governance_maturity") or {}

    # Summary metrics
    st.markdown("---")
    st.markdown("### Report Summary")
    render_metric_row([
        {"label": "Organisation", "value": report_summary["organisation_name"]},
        {"label": "Sections Available", "value": report_summary["sections_available"]},
        {"label": "Sections Missing", "value": report_summary["sections_missing"]},
        {"label": "Domains Reviewed", "value": report_summary["domains_reviewed"]},
    ])
    render_metric_row([
        {"label": "Gaps Included", "value": report_summary["gaps_included"]},
        {"label": "Recommendations", "value": report_summary["recommendations_included"]},
        {"label": "Maturity Level", "value": report_summary["maturity_level"] or "—"},
        {"label": "Human Review Required", "value": "Yes"},
    ])

    # Report readiness position
    st.markdown("---")
    readiness_text = report_summary.get("report_readiness", "")
    if report_summary["sections_missing"] == 0:
        st.success(readiness_text)
    else:
        st.warning(readiness_text)

    # Markdown preview and download
    st.markdown("---")
    st.markdown("### Governance Report")
    st.download_button(
        label="Download Governance Report Markdown",
        data=st.session_state["governance_report_markdown"],
        file_name=st.session_state["governance_report_filename"],
        mime="text/markdown",
    )
    with st.expander("Preview Governance Report"):
        preview_md = st.session_state["governance_report_markdown"]
        st.markdown(preview_md[:10000])
        if len(preview_md) > 10000:
            st.caption("Preview truncated to 10,000 characters. Full report available via download.")

    st.markdown("---")
    st.caption(
        "This governance report is generated from synthetic/demo policy text only. "
        "Not a legal opinion, compliance certification, safeguarding assessment, "
        "HR assessment, or professional governance judgement. "
        "Human review required before any real-world use."
    )


def page_export_centre():
    render_page_header(
        "Export Centre",
        "Export the AI governance review report as Markdown and PDF",
    )
    render_responsible_use_warning()

    # Minimum requirements check
    if "policy_pack" not in st.session_state:
        st.error("**Policy pack not found.** Please complete the following steps first:")
        st.markdown(
            "1. Go to **Policy Library** and load the BrightPath synthetic policy pack.\n"
            "2. Work through Policy Checker, Gap Analysis, Recommendations, and Governance Maturity.\n"
            "3. Go to **Governance Report** and generate the report.\n"
            "4. Return to **Export Centre**."
        )
        return

    if "governance_report_markdown" not in st.session_state:
        st.error("**Governance report not found.** Please complete the following step:")
        st.markdown(
            "1. Go to **Governance Report**.\n"
            "2. Click **Generate Governance Report**.\n"
            "3. Return to **Export Centre**."
        )
        return

    # Build export data
    export_data = build_export_data_from_session_state(st.session_state)
    readiness = check_export_readiness(st.session_state)
    package_summary = summarise_export_package(export_data)
    checklist = generate_export_quality_checklist(export_data)

    st.session_state["export_data"] = export_data
    st.session_state["export_readiness"] = readiness

    # Readiness summary
    st.markdown("---")
    st.markdown("### Report Readiness")

    _report_outputs = [
        ("policy_pack", "Synthetic policy pack loaded"),
        ("governance_framework", "Governance framework loaded"),
        ("coverage_results", "Policy coverage review complete"),
        ("gap_analysis", "Gap analysis complete"),
        ("policy_recommendations", "Recommendations generated"),
        ("governance_maturity", "Governance maturity calculated"),
        ("governance_report_markdown", "Governance report generated"),
    ]
    avail_col, miss_col = st.columns(2)
    with avail_col:
        st.markdown("**Available outputs:**")
        for key, label in _report_outputs:
            if key in st.session_state:
                st.markdown(f"✅ {label}")
    with miss_col:
        st.markdown("**Missing recommended outputs:**")
        any_missing = any(k not in st.session_state for k, _ in _report_outputs)
        if any_missing:
            for key, label in _report_outputs:
                if key not in st.session_state:
                    st.markdown(f"❌ {label}")
        else:
            st.markdown("All recommended outputs available.")

    # Missing output guidance
    missing_steps = [
        g for k, g in [
            ("governance_framework", "Go to **Governance Framework** and load the governance framework."),
            ("coverage_results", "Go to **Policy Checker** and run the policy coverage check."),
            ("gap_analysis", "Go to **Gap Analysis** to generate the gap analysis."),
            ("policy_recommendations", "Go to **Recommendations** to generate policy improvement recommendations."),
            ("governance_maturity", "Go to **Governance Maturity** to generate the maturity summary."),
        ]
        if k not in st.session_state
    ]
    if missing_steps:
        with st.expander("Recommended steps to complete the report"):
            for step in missing_steps:
                st.markdown(f"- {step}")
            st.info(
                "You can still export now — missing sections will show placeholder notes."
            )

    # Package summary metrics
    st.markdown("---")
    st.markdown("### Export Summary")
    render_metric_row([
        {"label": "Organisation", "value": package_summary["organisation_name"]},
        {"label": "Domains Reviewed", "value": package_summary["domains_reviewed"]},
        {"label": "Gaps Included", "value": package_summary["gaps_included"]},
        {"label": "Recommendations", "value": package_summary["recommendations_included"]},
    ])
    render_metric_row([
        {"label": "Maturity Level", "value": package_summary["maturity_level"] or "—"},
        {"label": "Governance Score", "value": f"{package_summary['governance_score']}/100" if package_summary['governance_score'] else "—"},
        {"label": "Outputs Available", "value": f"{package_summary['outputs_available']}/{package_summary['total_outputs']}"},
        {"label": "Export Formats", "value": ", ".join(package_summary["export_formats"])},
    ])

    # Export quality checklist
    st.markdown("---")
    st.markdown("### Export Quality Checklist")
    req_items = [i for i in checklist if i["importance"] == "Required"]
    rec_items = [i for i in checklist if i["importance"] == "Recommended"]
    adv_items = [i for i in checklist if i["importance"] == "Advisory"]

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Required**")
        for item in req_items:
            icon = "✅" if item["is_complete"] else "❌"
            st.markdown(f"{icon} {item['label']}")
    with col_b:
        st.markdown("**Recommended**")
        for item in rec_items:
            icon = "✅" if item["is_complete"] else "⬜"
            st.markdown(f"{icon} {item['label']}")

    with st.expander("Advisory checks"):
        for item in adv_items:
            icon = "✅" if item["is_complete"] else "⬜"
            st.markdown(f"{icon} {item['label']} — {item['note']}")

    # Analytics
    st.markdown("---")
    st.markdown("### Governance Analytics")
    analytics = None
    with st.spinner("Calculating analytics..."):
        try:
            analytics = build_governance_report_analytics(export_data)
            st.session_state["governance_report_analytics"] = analytics
        except Exception as e:
            st.warning(f"Analytics could not be generated: {e}")

    if analytics:
        completion = analytics.get("export_completion", {})
        cov = analytics.get("coverage_levels", {})
        gaps = analytics.get("gap_severities", {})
        recs = analytics.get("recommendation_priorities", {})
        scores = analytics.get("governance_scores", {})
        quality = analytics.get("report_quality", {})

        pct = completion.get("completion_percentage", 0)
        quality_pct = quality.get("quality_percentage", 0)

        render_metric_row([
            {"label": "Export Completion", "value": f"{pct}%"},
            {"label": "Report Quality", "value": f"{quality_pct}%"},
            {"label": "Sections Present", "value": f"{quality.get('sections_present', 0)}/{quality.get('sections_total', 0)}"},
        ])

        col_left, col_right = st.columns(2)
        with col_left:
            if cov.get("total", 0) > 0:
                st.markdown("**Coverage levels**")
                for level, count in cov["counts"].items():
                    if count > 0:
                        st.markdown(f"- {level}: {count}")
            if gaps.get("total", 0) > 0:
                st.markdown("**Gap severities**")
                for sev, count in gaps["counts"].items():
                    if count > 0:
                        st.markdown(f"- {sev}: {count}")
        with col_right:
            if recs.get("total", 0) > 0:
                st.markdown("**Recommendation priorities**")
                for pri, count in recs["counts"].items():
                    if count > 0:
                        st.markdown(f"- {pri}: {count}")
            if scores.get("overall_governance_score"):
                st.markdown("**Governance scores**")
                st.markdown(f"- Coverage: {scores.get('overall_coverage_score', 0)}/100")
                st.markdown(f"- Governance: {scores.get('overall_governance_score', 0)}/100")
                st.markdown(f"- Maturity: {scores.get('overall_maturity_level', '—')}")

    # Charts
    st.markdown("---")
    st.markdown("### Analytics Charts")
    chart_paths: dict = {}
    if analytics:
        with st.spinner("Generating charts..."):
            try:
                chart_paths = generate_all_export_charts(analytics, output_dir="outputs/charts")
                st.session_state["governance_report_chart_paths"] = chart_paths
            except Exception as e:
                st.warning(f"Charts could not be generated: {e}")

    if chart_paths:
        chart_titles = {
            "completion_status": "Export Completion Status",
            "coverage_levels": "Policy Coverage Level Distribution",
            "gap_severities": "Policy Gap Severity Distribution",
            "recommendation_priorities": "Recommendation Priority Distribution",
            "maturity_levels": "Domain Maturity Level Distribution",
            "governance_scores": "Governance Scores by Domain",
        }
        chart_cols = list(chart_paths.items())
        for i in range(0, len(chart_cols), 2):
            cols = st.columns(2)
            for j, (key, path) in enumerate(chart_cols[i:i + 2]):
                with cols[j]:
                    st.image(path, caption=chart_titles.get(key, key), use_column_width=True)
    else:
        st.info("Charts will appear here after analytics are generated from the full workflow.")

    # Export buttons
    st.markdown("---")
    st.markdown("### Download Report")

    if readiness["can_export_markdown"]:
        try:
            md_text, md_filename = prepare_markdown_export(export_data)
            st.download_button(
                label="Download Markdown Governance Report",
                data=md_text,
                file_name=md_filename,
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"Markdown export failed: {e}")
    else:
        st.info("Markdown export will be available once the governance report is generated.")

    if readiness["can_export_pdf"]:
        with st.spinner("Preparing PDF..."):
            try:
                pdf_bytes, pdf_filename = prepare_pdf_export(export_data, analytics, chart_paths)
                st.session_state["governance_report_pdf_bytes"] = pdf_bytes
                st.session_state["governance_report_pdf_filename"] = pdf_filename
                st.download_button(
                    label="Download PDF Governance Report",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"PDF export failed: {e}")
    else:
        st.info("PDF export will be available once the governance report is generated.")

    st.markdown("---")
    st.caption(
        "Exports are generated from synthetic/demo policy text only. "
        "Not a legal opinion, compliance certification, safeguarding assessment, "
        "HR assessment, or professional governance judgement. "
        "Human review required before any real-world use."
    )


def page_completion_review():
    render_page_header(
        "Completion Review",
        "Build 6 completion status, portfolio value, and portfolio notes",
    )
    render_responsible_use_warning()

    # Generate completion review
    review = generate_build6_completion_review(st.session_state, base_path=".")
    portfolio_summary = generate_portfolio_summary()
    case_study = generate_case_study_summary()
    completion_markdown = format_completion_review_as_markdown(review)
    portfolio_markdown = format_portfolio_notes_as_markdown(portfolio_summary, case_study)

    st.session_state["completion_review"] = review
    st.session_state["completion_review_markdown"] = completion_markdown
    st.session_state["portfolio_notes"] = {"portfolio_summary": portfolio_summary, "case_study": case_study}
    st.session_state["portfolio_notes_markdown"] = portfolio_markdown

    status = review["completion_status"]

    # Completion score metrics
    st.markdown("---")
    st.markdown("### Build 6 Completion Status")
    render_metric_row([
        {"label": "Phase completion", "value": f"{status['phase_completion_percentage']}%"},
        {"label": "Output completion", "value": f"{status['output_completion_percentage']}%"},
        {"label": "Documentation", "value": f"{status['documentation_completion_percentage']}%"},
        {"label": "Overall status", "value": status["overall_status"]},
    ])
    overall_pct = status.get("overall_completion_percentage", 0)
    st.progress(overall_pct / 100)
    st.info(status["final_readiness_label"])

    # Phase completion checklist
    st.markdown("---")
    st.markdown("### Phase Completion Checklist")
    col1, col2 = st.columns(2)
    phases = review["phase_checklist"]
    half = (len(phases) + 1) // 2
    for i, phase in enumerate(phases):
        col = col1 if i < half else col2
        mark = "✅" if phase["status"] == "Complete" else "❌"
        with col:
            st.markdown(f"{mark} **{phase['phase']}:** {phase['name']}")

    # Output completion status
    st.markdown("---")
    st.markdown("### Output Completion")
    output_status = review["output_status"]
    render_metric_row([
        {"label": "Available", "value": output_status["available_count"]},
        {"label": "Missing", "value": output_status["missing_count"]},
        {"label": "Total expected", "value": output_status["total_outputs"]},
        {"label": "Completion", "value": f"{output_status['completion_percentage']}%"},
    ])
    st.progress(output_status["completion_percentage"] / 100)

    avail_col, miss_col = st.columns(2)
    with avail_col:
        st.markdown("**Available outputs:**")
        for item in output_status["available_outputs"]:
            st.markdown(f"✅ {item['label']}")
    with miss_col:
        st.markdown("**Missing outputs:**")
        if output_status["missing_outputs"]:
            for item in output_status["missing_outputs"]:
                st.markdown(f"❌ {item['label']}")
        else:
            st.markdown("All expected outputs are available.")

    if output_status["recommended_next_actions"]:
        with st.expander("Recommended steps to complete outputs"):
            for action in output_status["recommended_next_actions"]:
                st.markdown(f"- {action}")

    # Documentation checklist
    st.markdown("---")
    st.markdown("### Documentation Checklist")
    doc_status = review["documentation_status"]
    render_metric_row([
        {"label": "Files present", "value": doc_status["existing_count"]},
        {"label": "Files missing", "value": doc_status["missing_count"]},
        {"label": "Total expected", "value": doc_status["total_docs"]},
        {"label": "Completion", "value": f"{doc_status['documentation_completion_percentage']}%"},
    ])
    st.progress(doc_status["documentation_completion_percentage"] / 100)

    doc_col1, doc_col2 = st.columns(2)
    with doc_col1:
        st.markdown("**Present:**")
        for doc in doc_status["existing_files"]:
            st.markdown(f"✅ {doc['label']}")
    with doc_col2:
        st.markdown("**Missing:**")
        if doc_status["missing_files"]:
            for doc in doc_status["missing_files"]:
                st.markdown(f"❌ {doc['label']}")
        else:
            st.markdown("All documentation files are present.")

    # Portfolio and commercial value
    st.markdown("---")
    st.markdown("### Portfolio Value")
    st.markdown(review["portfolio_value"])

    st.markdown("---")
    st.markdown("### Commercial Value")
    st.markdown(review["commercial_value"])

    st.markdown("---")
    st.markdown("### Technical Value")
    st.markdown(review["technical_value"])

    st.markdown("---")
    st.markdown("### Responsible-Use Position")
    st.success(review["responsible_use_position"])

    # Recommended final actions
    st.markdown("---")
    st.markdown("### Recommended Final Actions")
    for action in review["recommended_final_actions"]:
        st.markdown(f"- {action}")

    # Downloads
    st.markdown("---")
    st.markdown("### Downloads")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Download Completion Review Markdown",
            data=completion_markdown,
            file_name="build6-completion-review.md",
            mime="text/markdown",
        )
    with col_dl2:
        st.download_button(
            label="Download Portfolio Notes Markdown",
            data=portfolio_markdown,
            file_name="build6-portfolio-notes.md",
            mime="text/markdown",
        )

    st.markdown("---")
    st.caption(
        "Build 6 — AI Governance Policy Checker — BrightPath ChatGPT Mastery Project. "
        "Synthetic scenarios only. Human review required before any real-world use."
    )


def main():
    page = render_sidebar()

    if page == "Home":
        page_home()
    elif page == "Policy Library":
        page_policy_library()
    elif page == "Governance Framework":
        page_governance_framework()
    elif page == "Policy Checker":
        page_policy_checker()
    elif page == "Gap Analysis":
        page_gap_analysis()
    elif page == "Recommendations":
        page_recommendations()
    elif page == "Governance Maturity":
        page_governance_maturity()
    elif page == "Governance Report":
        page_governance_report()
    elif page == "Export Centre":
        page_export_centre()
    elif page == "Completion Review":
        page_completion_review()


if __name__ == "__main__":
    main()
