"""
Chart Utilities — AI Governance Policy Checker
Build 6 · BrightPath ChatGPT Mastery Project

Generates deterministic matplotlib charts for the Export Centre.
No external AI, LLM, or API calls. Synthetic/demo data only.
"""

import os

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False


_NAVY = "#1a2744"
_TEAL = "#2d7d6e"
_STEEL = "#4a7cb8"
_AMBER = "#b87a2d"
_SLATE = "#6b7a8d"
_RED = "#c0392b"
_ORANGE = "#e67e22"
_YELLOW = "#d4ac0d"
_GREEN = "#27ae60"

_COVERAGE_COLORS = {
    "Strong coverage": _TEAL,
    "Partial coverage": _STEEL,
    "Weak coverage": _AMBER,
    "Not covered": _RED,
}

_SEVERITY_COLORS = {
    "Critical gap": _RED,
    "High gap": _ORANGE,
    "Medium gap": _YELLOW,
    "Low gap": _GREEN,
}

_PRIORITY_COLORS = {
    "Urgent": _RED,
    "High priority": _ORANGE,
    "Medium priority": _YELLOW,
    "Low priority": _GREEN,
}

_MATURITY_COLORS = {
    "Initial governance": _RED,
    "Developing governance": _ORANGE,
    "Defined governance": _YELLOW,
    "Managed governance": _GREEN,
    "Optimised governance": _TEAL,
}


def _ensure_output_dir(output_path: str) -> None:
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def _save_and_close(fig, output_path: str) -> str:
    fig.savefig(output_path, bbox_inches="tight", dpi=100)
    plt.close(fig)
    return output_path


def _apply_clean_spines(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def create_completion_status_chart(
    completion_status: dict,
    output_path: str,
) -> str:
    """Horizontal bar chart showing which outputs are available."""
    if not _MATPLOTLIB_AVAILABLE:
        return ""
    try:
        _ensure_output_dir(output_path)
        items = completion_status.get("items", {})
        if not items:
            return ""

        labels = list(items.keys())
        values = [1 if v else 0 for v in items.values()]
        colors = [_TEAL if v else "#cccccc" for v in items.values()]

        fig, ax = plt.subplots(figsize=(8, max(3, len(labels) * 0.55)))
        bars = ax.barh(labels, values, color=colors, height=0.55)
        ax.set_xlim(0, 1.3)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Not available", "Available"], fontsize=9)
        ax.set_title("Export Completion Status", fontsize=12, color=_NAVY, pad=10)

        for bar, val in zip(bars, values):
            label = "Available" if val else "—"
            ax.text(
                bar.get_width() + 0.04,
                bar.get_y() + bar.get_height() / 2,
                label,
                va="center",
                fontsize=8,
                color=_NAVY,
            )

        _apply_clean_spines(ax)
        plt.yticks(fontsize=9)
        fig.tight_layout()
        return _save_and_close(fig, output_path)
    except Exception:
        return ""


def create_coverage_level_chart(
    coverage_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of policy coverage level distribution."""
    if not _MATPLOTLIB_AVAILABLE:
        return ""
    try:
        _ensure_output_dir(output_path)
        counts = coverage_counts.get("counts", {})
        if not counts or sum(counts.values()) == 0:
            return ""

        labels = list(counts.keys())
        values = [counts[l] for l in labels]
        bar_colors = [_COVERAGE_COLORS.get(l, _SLATE) for l in labels]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(labels, values, color=bar_colors, width=0.5)
        ax.set_ylabel("Number of domains", fontsize=10)
        ax.set_title("Policy Coverage Level Distribution", fontsize=12, color=_NAVY, pad=10)
        ax.set_ylim(0, max(values) + 1.5)

        for i, v in enumerate(values):
            if v > 0:
                ax.text(i, v + 0.1, str(v), ha="center", fontsize=10, color=_NAVY)

        _apply_clean_spines(ax)
        plt.xticks(fontsize=9)
        fig.tight_layout()
        return _save_and_close(fig, output_path)
    except Exception:
        return ""


def create_gap_severity_chart(
    gap_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of gap severity distribution."""
    if not _MATPLOTLIB_AVAILABLE:
        return ""
    try:
        _ensure_output_dir(output_path)
        counts = gap_counts.get("counts", {})
        if not counts or sum(counts.values()) == 0:
            return ""

        labels = list(counts.keys())
        values = [counts[l] for l in labels]
        bar_colors = [_SEVERITY_COLORS.get(l, _SLATE) for l in labels]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(labels, values, color=bar_colors, width=0.5)
        ax.set_ylabel("Number of gaps", fontsize=10)
        ax.set_title("Policy Gap Severity Distribution", fontsize=12, color=_NAVY, pad=10)
        ax.set_ylim(0, max(values) + 1.5)

        for i, v in enumerate(values):
            if v > 0:
                ax.text(i, v + 0.1, str(v), ha="center", fontsize=10, color=_NAVY)

        _apply_clean_spines(ax)
        plt.xticks(fontsize=9)
        fig.tight_layout()
        return _save_and_close(fig, output_path)
    except Exception:
        return ""


def create_recommendation_priority_chart(
    recommendation_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of recommendation priority distribution."""
    if not _MATPLOTLIB_AVAILABLE:
        return ""
    try:
        _ensure_output_dir(output_path)
        counts = recommendation_counts.get("counts", {})
        if not counts or sum(counts.values()) == 0:
            return ""

        labels = list(counts.keys())
        values = [counts[l] for l in labels]
        bar_colors = [_PRIORITY_COLORS.get(l, _SLATE) for l in labels]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(labels, values, color=bar_colors, width=0.5)
        ax.set_ylabel("Number of recommendations", fontsize=10)
        ax.set_title("Recommendation Priority Distribution", fontsize=12, color=_NAVY, pad=10)
        ax.set_ylim(0, max(values) + 1.5)

        for i, v in enumerate(values):
            if v > 0:
                ax.text(i, v + 0.1, str(v), ha="center", fontsize=10, color=_NAVY)

        _apply_clean_spines(ax)
        plt.xticks(fontsize=9)
        fig.tight_layout()
        return _save_and_close(fig, output_path)
    except Exception:
        return ""


def create_maturity_level_chart(
    maturity_counts: dict,
    output_path: str,
) -> str:
    """Bar chart of domain maturity level distribution."""
    if not _MATPLOTLIB_AVAILABLE:
        return ""
    try:
        _ensure_output_dir(output_path)
        counts = maturity_counts.get("counts", {})
        if not counts or sum(counts.values()) == 0:
            return ""

        # Only include levels with non-zero counts
        non_zero = [(l, v) for l, v in counts.items() if v > 0]
        if not non_zero:
            return ""

        labels = [l for l, _ in non_zero]
        values = [v for _, v in non_zero]
        bar_colors = [_MATURITY_COLORS.get(l, _SLATE) for l in labels]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, values, color=bar_colors, width=0.5)
        ax.set_ylabel("Number of domains", fontsize=10)
        ax.set_title("Domain Maturity Level Distribution", fontsize=12, color=_NAVY, pad=10)
        ax.set_ylim(0, max(values) + 1.5)

        for i, v in enumerate(values):
            if v > 0:
                ax.text(i, v + 0.1, str(v), ha="center", fontsize=10, color=_NAVY)

        _apply_clean_spines(ax)
        plt.xticks(fontsize=8, rotation=15, ha="right")
        fig.tight_layout()
        return _save_and_close(fig, output_path)
    except Exception:
        return ""


def create_governance_score_chart(
    score_breakdown: dict,
    output_path: str,
) -> str:
    """Horizontal bar chart of governance scores by domain."""
    if not _MATPLOTLIB_AVAILABLE:
        return ""
    try:
        _ensure_output_dir(output_path)
        domain_scores = score_breakdown.get("domain_maturity_scores", {})

        if domain_scores:
            sorted_items = sorted(domain_scores.items(), key=lambda x: x[1])
            labels = [k for k, _ in sorted_items]
            values = [v for _, v in sorted_items]
        else:
            overall_gov = score_breakdown.get("overall_governance_score", 0)
            overall_cov = score_breakdown.get("overall_coverage_score", 0)
            if not overall_gov and not overall_cov:
                return ""
            labels = ["Coverage Score", "Governance Score"]
            values = [overall_cov, overall_gov]

        colors = [
            _TEAL if v >= 75 else _STEEL if v >= 50 else _AMBER if v >= 25 else _RED
            for v in values
        ]

        fig, ax = plt.subplots(figsize=(9, max(3, len(labels) * 0.55)))
        ax.barh(labels, values, color=colors, height=0.55)
        ax.set_xlim(0, 120)
        ax.set_xlabel("Score (out of 100)", fontsize=10)
        ax.set_title("Governance Scores by Domain", fontsize=12, color=_NAVY, pad=10)

        for i, v in enumerate(values):
            ax.text(v + 1.5, i, str(v), va="center", fontsize=8, color=_NAVY)

        # Reference lines at 50 and 75
        ax.axvline(x=75, color=_TEAL, linestyle="--", alpha=0.4, linewidth=1)
        ax.axvline(x=50, color=_AMBER, linestyle="--", alpha=0.4, linewidth=1)
        _apply_clean_spines(ax)
        plt.yticks(fontsize=8)
        fig.tight_layout()
        return _save_and_close(fig, output_path)
    except Exception:
        return ""


def generate_all_export_charts(
    analytics: dict,
    output_dir: str = "outputs/charts",
) -> dict:
    """
    Generate all export charts from analytics dict.
    Returns dict of chart_key -> file_path for successfully generated charts.
    Skips charts gracefully where data is missing or generation fails.
    """
    if not _MATPLOTLIB_AVAILABLE:
        return {}

    os.makedirs(output_dir, exist_ok=True)

    chart_specs = [
        (
            "completion_status",
            create_completion_status_chart,
            analytics.get("export_completion", {}),
            os.path.join(output_dir, "completion_status.png"),
        ),
        (
            "coverage_levels",
            create_coverage_level_chart,
            analytics.get("coverage_levels", {}),
            os.path.join(output_dir, "coverage_levels.png"),
        ),
        (
            "gap_severities",
            create_gap_severity_chart,
            analytics.get("gap_severities", {}),
            os.path.join(output_dir, "gap_severities.png"),
        ),
        (
            "recommendation_priorities",
            create_recommendation_priority_chart,
            analytics.get("recommendation_priorities", {}),
            os.path.join(output_dir, "recommendation_priorities.png"),
        ),
        (
            "maturity_levels",
            create_maturity_level_chart,
            analytics.get("maturity_levels", {}),
            os.path.join(output_dir, "maturity_levels.png"),
        ),
        (
            "governance_scores",
            create_governance_score_chart,
            analytics.get("governance_scores", {}),
            os.path.join(output_dir, "governance_scores.png"),
        ),
    ]

    chart_paths: dict[str, str] = {}
    for key, fn, data, path in chart_specs:
        try:
            result = fn(data, path)
            if result and os.path.exists(result):
                chart_paths[key] = result
        except Exception:
            pass

    return chart_paths
