"""Matplotlib chart generation for training pack analytics.

Writes clean, professional PNG charts to disk for use in the app and PDF
exports. All chart data is deterministic and derived from generated content
only. Charts fail safely — an empty dataset returns "" instead of crashing.
"""

import os

NAVY = "#16243d"
BLUE = "#2563eb"
GREEN = "#27ae60"
GREY = "#94a3b8"
PURPLE = "#7c3aed"
AMBER = "#d97706"


def _save_figure(fig, output_path: str) -> str:
    """Save a figure to output_path and return the path."""
    import matplotlib.pyplot as plt

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fig.savefig(output_path, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return output_path


def _new_axes(figsize):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig, ax


def create_section_completion_chart(completion_status: dict, output_path: str) -> str:
    """Horizontal bar chart of section completion. Returns path or ""."""
    if not completion_status:
        return ""
    labels = list(completion_status.keys())
    values = [1 if v else 0 for v in completion_status.values()]
    colors = [GREEN if v else "#cbd5e1" for v in values]

    fig, ax = _new_axes((7, max(2.5, len(labels) * 0.45)))
    bars = ax.barh(labels, [1] * len(labels), color=colors, height=0.55)
    ax.set_xlim(0, 1.25)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_title("Section Completion", fontsize=12, fontweight="bold", color=NAVY, pad=10)
    for bar, val in zip(bars, values):
        ax.text(
            1.03, bar.get_y() + bar.get_height() / 2,
            "Complete" if val else "Pending",
            va="center", fontsize=9, color=GREEN if val else GREY,
        )
    ax.invert_yaxis()
    fig.tight_layout()
    return _save_figure(fig, output_path)


def create_activity_mix_chart(activity_counts: dict, output_path: str) -> str:
    """Horizontal bar chart of activity type counts. Returns path or ""."""
    if not activity_counts:
        return ""
    labels = [str(k).replace("_", " ").title()[:26] for k in activity_counts.keys()]
    values = list(activity_counts.values())

    fig, ax = _new_axes((7, max(2.5, len(labels) * 0.45)))
    ax.barh(labels, values, color=BLUE, height=0.55)
    ax.set_xlabel("Activities", fontsize=9, color=NAVY)
    ax.set_title("Activity Mix", fontsize=12, fontweight="bold", color=NAVY, pad=10)
    ax.invert_yaxis()
    fig.tight_layout()
    return _save_figure(fig, output_path)


def create_workshop_time_chart(time_allocation: list, output_path: str) -> str:
    """Horizontal bar chart of minutes per agenda section. Returns path or ""."""
    rows = [
        t for t in (time_allocation or [])
        if isinstance(t, dict) and int(t.get("minutes", 0)) > 0
    ]
    if not rows:
        return ""
    labels = [str(t.get("section", "Section"))[:28] for t in rows]
    values = [int(t.get("minutes", 0)) for t in rows]

    fig, ax = _new_axes((7, max(2.5, len(labels) * 0.45)))
    ax.barh(labels, values, color=PURPLE, height=0.55)
    ax.set_xlabel("Minutes", fontsize=9, color=NAVY)
    ax.set_title("Workshop Time Allocation", fontsize=12, fontweight="bold", color=NAVY, pad=10)
    ax.invert_yaxis()
    fig.tight_layout()
    return _save_figure(fig, output_path)


def create_knowledge_topic_chart(topic_counts: dict, output_path: str) -> str:
    """Horizontal bar chart of knowledge check topic coverage. Returns path or ""."""
    if not topic_counts:
        return ""
    labels = [str(k).replace("_", " ").title()[:26] for k in topic_counts.keys()]
    values = list(topic_counts.values())

    fig, ax = _new_axes((7, max(2.5, len(labels) * 0.45)))
    ax.barh(labels, values, color=AMBER, height=0.55)
    ax.set_xlabel("Questions", fontsize=9, color=NAVY)
    ax.set_title("Knowledge Check Topic Coverage", fontsize=12, fontweight="bold", color=NAVY, pad=10)
    ax.invert_yaxis()
    fig.tight_layout()
    return _save_figure(fig, output_path)


def generate_all_report_charts(analytics: dict, output_dir: str = "outputs/charts") -> dict:
    """Generate all available charts and return {chart_name: file_path}.

    Skips charts whose data is missing; a chart that fails to render is
    omitted rather than raising.
    """
    if not isinstance(analytics, dict):
        analytics = {}
    os.makedirs(output_dir, exist_ok=True)

    chart_specs = [
        ("section_completion", create_section_completion_chart,
         analytics.get("section_completion", {})),
        ("activity_mix", create_activity_mix_chart,
         analytics.get("activity_type_counts", {})),
        ("workshop_time", create_workshop_time_chart,
         analytics.get("workshop_time_allocation", [])),
        ("knowledge_topics", create_knowledge_topic_chart,
         analytics.get("knowledge_check_topic_counts", {})),
    ]

    charts: dict = {}
    for name, create_fn, data in chart_specs:
        try:
            path = create_fn(data, os.path.join(output_dir, f"{name}.png"))
            if path:
                charts[name] = path
        except Exception:
            continue
    return charts
