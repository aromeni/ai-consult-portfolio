"""Deterministic export centre and completion review for Build 8 Phase 8."""

import csv
import io
import json
import re

from logic.action_tracker import build_all_action_tracker_summaries
from logic.blocker_review import build_all_blocker_review_summaries
from logic.client_checkin import build_all_client_checkin_summaries
from logic.governance_tracker import build_all_governance_summaries
from logic.progress_report import build_full_progress_report
from logic.training_followup import build_all_training_followup_summaries


def export_markdown_report(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
    organisation_id: str | None = None,
) -> str:
    """Return Markdown implementation progress report text."""
    return build_full_progress_report(
        organisations, actions, checkins, organisation_id=organisation_id
    )


def build_csv_export_rows(actions: list[dict]) -> list[dict]:
    """Return flat rows combining action, tracker, blocker, governance, and training fields."""
    tracker_by_id = {
        s["action_id"]: s for s in build_all_action_tracker_summaries(actions)
    }
    blocker_by_id = {
        s["action_id"]: s for s in build_all_blocker_review_summaries(actions)
    }
    governance_by_id = {
        s["action_id"]: s for s in build_all_governance_summaries(actions)
    }
    training_by_id = {
        s["action_id"]: s for s in build_all_training_followup_summaries(actions)
    }

    rows = []
    for action in actions:
        action_id = action.get("action_id", "")
        tracker = tracker_by_id.get(action_id, {})
        blocker = blocker_by_id.get(action_id, {})
        governance = governance_by_id.get(action_id, {})
        training = training_by_id.get(action_id, {})

        rows.append({
            "action_id": action_id,
            "organisation_id": action.get("organisation_id", ""),
            "organisation_name": action.get("organisation_name", ""),
            "workflow_id": action.get("workflow_id", ""),
            "workflow_name": action.get("workflow_name", ""),
            "related_build": action.get("related_build", ""),
            "action_title": action.get("action_title", ""),
            "owner_role": action.get("owner_role", ""),
            "priority": action.get("priority", ""),
            "status": action.get("status", ""),
            "due_in_days": action.get("due_in_days", 0),
            "delivery_state": tracker.get("delivery_state", ""),
            "attention_level": tracker.get("attention_level", ""),
            "action_score": tracker.get("action_score", 0),
            "blocker_type": blocker.get("blocker_type", ""),
            "blocker_severity": blocker.get("blocker_severity", ""),
            "delivery_risk_level": blocker.get("delivery_risk_level", ""),
            "requires_escalation": blocker.get("requires_escalation", False),
            "signoff_urgency": governance.get("signoff_urgency", ""),
            "control_area": governance.get("control_area", ""),
            "control_readiness": governance.get("control_readiness", ""),
            "governance_delivery_risk": governance.get("governance_delivery_risk", ""),
            "training_followup_urgency": training.get("training_followup_urgency", ""),
            "training_support_type": training.get("training_support_type", ""),
            "training_support_intensity": training.get("training_support_intensity", ""),
            "training_delivery_risk": training.get("training_delivery_risk", ""),
            "governance_signoff_required": action.get("governance_signoff_required", False),
            "training_followup_required": action.get("training_followup_required", False),
            "client_checkin_required": action.get("client_checkin_required", False),
        })

    return rows


def export_csv_text(actions: list[dict]) -> str:
    """Return CSV text from export rows."""
    rows = build_csv_export_rows(actions)

    if not rows:
        return ""

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def export_json_text(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> str:
    """Return pretty JSON evidence pack."""
    payload = {
        "organisations": organisations,
        "implementation_actions": actions,
        "client_checkins": checkins,
        "action_tracker_summaries": build_all_action_tracker_summaries(actions),
        "blocker_review_summaries": build_all_blocker_review_summaries(actions),
        "governance_summaries": build_all_governance_summaries(actions),
        "training_followup_summaries": build_all_training_followup_summaries(actions),
        "completion_summary": build_completion_summary(organisations, actions, checkins),
    }
    return json.dumps(payload, indent=2)


def build_export_filename(base_name: str, extension: str) -> str:
    """Return safe lowercase filename with extension."""
    ext = extension.lstrip(".")
    safe_name = base_name.lower().replace(" ", "_")
    safe_name = re.sub(r"[^a-z0-9_\-]", "", safe_name)
    if safe_name.endswith(f".{ext}"):
        return safe_name
    return f"{safe_name}.{ext}"


def build_completion_summary(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> dict:
    """Return final Build 8 completion metrics."""
    blocker_summaries = build_all_blocker_review_summaries(actions)
    governance_summaries = build_all_governance_summaries(actions)
    training_summaries = build_all_training_followup_summaries(actions)

    return {
        "total_organisations": len(organisations),
        "total_actions": len(actions),
        "total_checkins": len(checkins),
        "completed_actions": sum(
            a.get("status") == "Completed" for a in actions
        ),
        "blocked_actions": sum(
            a.get("status") == "Blocked" for a in actions
        ),
        "in_progress_actions": sum(
            a.get("status") == "In progress" for a in actions
        ),
        "critical_or_high_priority_actions": sum(
            a.get("priority") in {"Critical", "High"} for a in actions
        ),
        "governance_signoff_required_actions": sum(
            bool(a.get("governance_signoff_required")) for a in actions
        ),
        "training_followup_required_actions": sum(
            bool(a.get("training_followup_required")) for a in actions
        ),
        "client_checkin_required_actions": sum(
            bool(a.get("client_checkin_required")) for a in actions
        ),
        "escalation_required_actions": sum(
            s["requires_escalation"] for s in blocker_summaries
        ),
        "high_governance_risk_actions": sum(
            s["governance_delivery_risk"] == "High governance delivery risk"
            for s in governance_summaries
        ),
        "high_training_delivery_risk_actions": sum(
            s["training_delivery_risk"] == "High training delivery risk"
            for s in training_summaries
        ),
    }


def build_completion_review_text(
    organisations: list[dict],
    actions: list[dict],
    checkins: list[dict],
) -> str:
    """Return concise Markdown completion review for Build 8."""
    summary = build_completion_summary(organisations, actions, checkins)

    lines = [
        "# Build 8 — AI Adoption Delivery and Implementation Tracker",
        "## Completion Review",
        "",
        "### What Build 8 Does",
        "",
        "Build 8 helps an AI consultant manage the work that follows an audit, governance "
        "review, training programme, consulting report, and adoption impact review. It turns "
        "findings and decisions into implementation actions with owners, priorities, deadlines, "
        "blockers, and follow-up requirements.",
        "",
        "### Completed Phases",
        "",
        "- Phase 1 — Scaffold and Synthetic Implementation Action Data",
        "- Phase 2 — Action Tracker and Status Engine",
        "- Phase 3 — Blocker, Risk, and Dependency Review",
        "- Phase 4 — Governance Sign-off and Control Tracker",
        "- Phase 5 — Training Follow-up and Support Plan",
        "- Phase 6 — Client Check-in Summary Builder",
        "- Phase 7 — Implementation Progress Report Builder",
        "- Phase 8 — Export Centre, Completion Review, and Final Sweep",
        "",
        "### Completion Summary",
        "",
        f"- Total organisations: **{summary['total_organisations']}**",
        f"- Total implementation actions: **{summary['total_actions']}**",
        f"- Total client check-ins: **{summary['total_checkins']}**",
        f"- Completed actions: **{summary['completed_actions']}**",
        f"- Blocked actions: **{summary['blocked_actions']}**",
        f"- In-progress actions: **{summary['in_progress_actions']}**",
        f"- Critical or high priority: **{summary['critical_or_high_priority_actions']}**",
        f"- Governance sign-off required: **{summary['governance_signoff_required_actions']}**",
        f"- Training follow-up required: **{summary['training_followup_required_actions']}**",
        f"- Client check-in required: **{summary['client_checkin_required_actions']}**",
        f"- Escalation required: **{summary['escalation_required_actions']}**",
        "",
        "### Consulting Use Case",
        "",
        "Build 8 is designed for an AI adoption consultant managing post-audit implementation "
        "work with small and medium organisations. It tracks delivery actions, blockers, "
        "governance sign-offs, training follow-up, and client check-ins across synthetic delivery "
        "organisations, and packages the evidence into structured progress reports and export formats.",
        "",
        "### Portfolio Connections",
        "",
        "- **Build 1** — Readiness findings feed into delivery and blocker sections.",
        "- **Build 4** — Training needs feed into the training follow-up plan.",
        "- **Build 5** — Consulting recommendations feed into owned follow-up actions.",
        "- **Build 6** — Governance gaps feed into sign-off and control tracking.",
        "- **Build 7** — Adoption decisions feed into implementation deadlines.",
        "",
        "### Limitations",
        "",
        "- Uses synthetic data only. Does not connect to real client systems, data sources, or APIs.",
        "- Deterministic logic only. Does not use predictive modelling, machine learning, or LLMs.",
        "- No persistence. Data is not stored between sessions.",
        "- No authentication. Not suitable for multi-user environments without additional security.",
        "- No real-time data. Action progress is based on synthetic static records.",
        "",
        "### Recommended Future Extensions",
        "",
        "- Connect to a live action register or project management tool.",
        "- Add role-based access for consultant and client views.",
        "- Add a timeline or Gantt view for delivery scheduling.",
        "- Enable progress updates directly in the app.",
        "- Extend the export centre to include branded PDF reporting or PowerPoint slides.",
        "",
        "### Synthetic Data Disclaimer",
        "",
        "> This build uses synthetic portfolio data only. It does not contain real client, staff, "
        "learner, safeguarding, HR, personal, confidential, or regulated data. Human review is "
        "required before any real-world use.",
        "",
    ]
    return "\n".join(lines)


def export_pdf_bytes(markdown_text: str) -> bytes:
    """Return basic PDF bytes from Markdown-like text."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as error:
        raise ImportError(
            "reportlab is required for PDF export. Install with: pip install reportlab"
        ) from error

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    story = []

    for line in markdown_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
        elif stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], styles["Heading1"]))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], styles["Heading2"]))
        elif stripped.startswith("### "):
            story.append(Paragraph(stripped[4:], styles["Heading3"]))
        else:
            clean = stripped.replace("**", "").replace("*", "").replace("`", "")
            clean = clean.replace(">", "").strip()
            story.append(Paragraph(clean, styles["BodyText"]))

    doc.build(story)
    return buffer.getvalue()


def export_summary_chart_png_bytes(actions: list[dict]) -> bytes:
    """Return simple PNG bytes for action delivery state counts."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError(
            "matplotlib is required for chart export. Install with: pip install matplotlib"
        ) from error

    summaries = build_all_action_tracker_summaries(actions)
    state_order = ["Completed", "Active", "Waiting", "Blocked", "Deferred"]
    state_counts = {state: 0 for state in state_order}
    for summary in summaries:
        state = summary["delivery_state"]
        if state in state_counts:
            state_counts[state] += 1

    states = list(state_counts.keys())
    counts = list(state_counts.values())

    fig, ax = plt.subplots(figsize=(8, 4))
    colours = ["#357654", "#0f6b64", "#9a651b", "#c95d44", "#5d6a70"]
    ax.bar(states, counts, color=colours)
    ax.set_title("Build 8 — Implementation Action Delivery State Summary")
    ax.set_xlabel("Delivery State")
    ax.set_ylabel("Action Count")
    ax.set_ylim(0, max(counts) + 1 if any(counts) else 1)
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    return buffer.getvalue()
