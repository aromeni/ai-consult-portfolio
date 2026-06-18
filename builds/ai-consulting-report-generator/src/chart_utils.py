"""Chart utilities — Build 5 Phase 8.

Generates matplotlib bar charts for the Export Centre.
All content is deterministic. No external AI calls. No invented data.
Charts fail gracefully — PDF/PPTX exports work without them.
"""

import os

_NAVY = "#1a2744"
_BLUE = "#2563eb"
_AMBER = "#d97706"
_GREEN = "#166534"
_RED = "#b91c1c"
_SLATE = "#94a3b8"
_LIGHT = "#e2e8f0"


def _ensure_dir(path: str) -> None:
    if path:
        os.makedirs(path, exist_ok=True)


def _setup_matplotlib():
    """Import matplotlib with Agg backend (no display required)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def create_completion_status_chart(
    completion_status: dict,
    output_path: str,
) -> str:
    """Horizontal bar chart showing output completion. Returns path or empty string."""
    if not completion_status or not output_path:
        return ""
    try:
        plt = _setup_matplotlib()

        labels = list(completion_status.keys())
        colours = [_GREEN if v else _LIGHT for v in completion_status.values()]
        values = [1 if v else 0.2 for v in completion_status.values()]

        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.barh(labels, values, color=colours, height=0.55)
        for i, (label, done) in enumerate(completion_status.items()):
            ax.text(
                0.05, i,
                "✓ Generated" if done else "Not yet generated",
                va="center", fontsize=9,
                color="#ffffff" if done else _SLATE,
                fontweight="bold" if done else "normal",
            )
        ax.set_xlim(0, 1.5)
        ax.set_xticks([])
        ax.set_title(
            "Report Output Completion",
            fontsize=12, color=_NAVY, fontweight="bold", pad=10,
        )
        ax.tick_params(axis="y", labelsize=9, colors=_NAVY)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_color(_LIGHT)
        plt.tight_layout()
        _ensure_dir(os.path.dirname(os.path.abspath(output_path)))
        plt.savefig(output_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return output_path
    except Exception:
        return ""


def create_readiness_score_chart(
    score_breakdown: dict,
    output_path: str,
) -> str:
    """Horizontal bar chart of readiness scores by category. Returns path or empty string."""
    if not score_breakdown or not output_path:
        return ""
    try:
        plt = _setup_matplotlib()

        # Place Overall at the bottom
        items = [(k, v) for k, v in score_breakdown.items() if k != "Overall"]
        if "Overall" in score_breakdown:
            items.append(("Overall", score_breakdown["Overall"]))

        labels = [k for k, _ in items]
        values = [v for _, v in items]
        colours = []
        for v in values:
            if v >= 70:
                colours.append(_GREEN)
            elif v >= 40:
                colours.append(_AMBER)
            else:
                colours.append(_RED)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.barh(labels, values, color=colours, height=0.55)
        for i, v in enumerate(values):
            ax.text(
                v + 1.5, i, f"{v}/100",
                va="center", fontsize=9, color=_NAVY,
            )
        ax.set_xlim(0, 115)
        ax.axvline(40, color=_AMBER, linestyle="--", linewidth=1, alpha=0.5, label="Developing (40)")
        ax.axvline(70, color=_GREEN, linestyle="--", linewidth=1, alpha=0.5, label="Moderate (70)")
        ax.legend(fontsize=8, loc="lower right")
        ax.set_title(
            "AI Readiness Score by Category",
            fontsize=12, color=_NAVY, fontweight="bold", pad=10,
        )
        ax.tick_params(axis="y", labelsize=9, colors=_NAVY)
        ax.set_xlabel("Score / 100", fontsize=9, color=_SLATE)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", linestyle="--", alpha=0.25)
        plt.tight_layout()
        _ensure_dir(os.path.dirname(os.path.abspath(output_path)))
        plt.savefig(output_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return output_path
    except Exception:
        return ""


def create_risk_level_chart(
    risk_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of risk counts by level. Returns path or empty string."""
    if not risk_counts or not output_path:
        return ""
    if all(v == 0 for v in risk_counts.values()):
        return ""
    try:
        plt = _setup_matplotlib()

        level_colours = {
            "Critical": "#b91c1c",
            "High": "#d97706",
            "Medium": "#2563eb",
            "Low": "#166534",
        }
        labels = list(risk_counts.keys())
        values = list(risk_counts.values())
        colours = [level_colours.get(l, _SLATE) for l in labels]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=colours, width=0.5)
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, val + 0.1,
                    str(val), ha="center", va="bottom",
                    fontsize=11, color=_NAVY, fontweight="bold",
                )
        ax.set_ylabel("Number of Risks", fontsize=10, color=_NAVY)
        ax.set_title(
            "AI Risk Distribution by Level",
            fontsize=12, color=_NAVY, fontweight="bold", pad=10,
        )
        ax.tick_params(axis="x", labelsize=10, colors=_NAVY)
        ax.set_ylim(0, max(values or [0]) + 2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        plt.tight_layout()
        _ensure_dir(os.path.dirname(os.path.abspath(output_path)))
        plt.savefig(output_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return output_path
    except Exception:
        return ""


def create_opportunity_priority_chart(
    opportunity_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of opportunity counts by priority. Returns path or empty string."""
    if not opportunity_counts or not output_path:
        return ""
    if all(v == 0 for v in opportunity_counts.values()):
        return ""
    try:
        plt = _setup_matplotlib()

        priority_colours = {
            "Strategic": _NAVY,
            "High": _BLUE,
            "Medium": _AMBER,
            "Low": _SLATE,
        }
        labels = list(opportunity_counts.keys())
        values = list(opportunity_counts.values())
        colours = [priority_colours.get(l, _SLATE) for l in labels]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=colours, width=0.5)
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, val + 0.1,
                    str(val), ha="center", va="bottom",
                    fontsize=11, color=_NAVY, fontweight="bold",
                )
        ax.set_ylabel("Number of Opportunities", fontsize=10, color=_NAVY)
        ax.set_title(
            "AI Opportunity Priority Distribution",
            fontsize=12, color=_NAVY, fontweight="bold", pad=10,
        )
        ax.tick_params(axis="x", labelsize=10, colors=_NAVY)
        ax.set_ylim(0, max(values or [0]) + 2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        plt.tight_layout()
        _ensure_dir(os.path.dirname(os.path.abspath(output_path)))
        plt.savefig(output_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return output_path
    except Exception:
        return ""


def create_roadmap_action_chart(
    roadmap_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of roadmap actions by phase. Returns path or empty string."""
    if not roadmap_counts or not output_path:
        return ""
    if all(v == 0 for v in roadmap_counts.values()):
        return ""
    try:
        plt = _setup_matplotlib()

        phase_colours = [_NAVY, _BLUE, _AMBER]
        labels = list(roadmap_counts.keys())
        values = list(roadmap_counts.values())
        colours = phase_colours[: len(labels)]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=colours, width=0.5)
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, val + 0.1,
                    str(val), ha="center", va="bottom",
                    fontsize=11, color=_NAVY, fontweight="bold",
                )
        ax.set_ylabel("Number of Actions", fontsize=10, color=_NAVY)
        ax.set_title(
            "Roadmap Actions by Phase",
            fontsize=12, color=_NAVY, fontweight="bold", pad=10,
        )
        ax.tick_params(axis="x", labelsize=9, colors=_NAVY)
        ax.set_ylim(0, max(values or [0]) + 3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        plt.tight_layout()
        _ensure_dir(os.path.dirname(os.path.abspath(output_path)))
        plt.savefig(output_path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return output_path
    except Exception:
        return ""


def generate_all_export_charts(
    analytics: dict,
    output_dir: str = "outputs/charts",
) -> dict:
    """Generate all export charts. Returns dict of name -> file path."""
    an = analytics or {}
    chart_paths = {}
    _ensure_dir(output_dir)

    completion = an.get("completion_status") or {}
    if completion:
        path = create_completion_status_chart(
            completion, os.path.join(output_dir, "completion_status.png")
        )
        if path:
            chart_paths["completion_status"] = path

    readiness = an.get("readiness_score_breakdown") or {}
    if readiness:
        path = create_readiness_score_chart(
            readiness, os.path.join(output_dir, "readiness_scores.png")
        )
        if path:
            chart_paths["readiness_scores"] = path

    risks = an.get("risk_level_counts") or {}
    if risks:
        path = create_risk_level_chart(
            risks, os.path.join(output_dir, "risk_levels.png")
        )
        if path:
            chart_paths["risk_levels"] = path

    opps = an.get("opportunity_priority_counts") or {}
    if opps:
        path = create_opportunity_priority_chart(
            opps, os.path.join(output_dir, "opportunity_priorities.png")
        )
        if path:
            chart_paths["opportunity_priorities"] = path

    roadmap = an.get("roadmap_action_counts") or {}
    if roadmap:
        path = create_roadmap_action_chart(
            roadmap, os.path.join(output_dir, "roadmap_actions.png")
        )
        if path:
            chart_paths["roadmap_actions"] = path

    return chart_paths
