"""Training scenario management for the AI Staff Training and Workshop Generator.

Phase 1: validates, summarises, and formats synthetic training scenarios.
No real organisational data is processed.
"""

_REQUIRED_FIELDS = [
    "organisation_name",
    "organisation_type",
    "staff_count",
    "current_ai_use",
    "training_goal",
    "priority_topics",
]


def validate_training_scenario(scenario: dict) -> tuple:
    """Return (is_valid: bool, message: str) for a training scenario dict.

    Checks:
    - organisation_name is present and non-empty
    - organisation_type is present and non-empty
    - staff_count is present and a positive integer
    - current_ai_use is present and non-empty
    - training_goal is present and non-empty
    - priority_topics is a non-empty list
    """
    if not scenario:
        return False, "Scenario is empty."

    if not str(scenario.get("organisation_name", "")).strip():
        return False, "Organisation name is required."

    if not str(scenario.get("organisation_type", "")).strip():
        return False, "Organisation type is required."

    staff_count = scenario.get("staff_count")
    if staff_count is None:
        return False, "Staff count is required."
    try:
        if int(staff_count) <= 0:
            return False, "Staff count must be a positive number."
    except (TypeError, ValueError):
        return False, "Staff count must be a valid number."

    if not str(scenario.get("current_ai_use", "")).strip():
        return False, "Current AI use description is required."

    if not str(scenario.get("training_goal", "")).strip():
        return False, "Training goal is required."

    topics = scenario.get("priority_topics", [])
    if not topics or len(topics) == 0:
        return False, "At least one priority topic is required."

    return True, f"Scenario for '{scenario['organisation_name']}' is valid."


def summarise_training_scenario(scenario: dict) -> dict:
    """Return a summary dict with key statistics and display values.

    Returns:
        {
            organisation_name: str,
            organisation_type: str,
            staff_count: int,
            sector: str,
            country_context: str,
            topic_count: int,
            role_count: int,
            training_duration: str,
            delivery_mode: str,
            concern_count: int,
        }
    """
    return {
        "organisation_name": scenario.get("organisation_name", ""),
        "organisation_type": scenario.get("organisation_type", ""),
        "staff_count": scenario.get("staff_count", 0),
        "sector": scenario.get("sector", ""),
        "country_context": scenario.get("country_context", ""),
        "topic_count": len(scenario.get("priority_topics", [])),
        "role_count": len(scenario.get("staff_roles", [])),
        "training_duration": scenario.get("training_duration", ""),
        "delivery_mode": scenario.get("delivery_mode", ""),
        "concern_count": len(scenario.get("main_concerns", [])),
    }


def format_scenario_as_markdown(scenario: dict) -> str:
    """Return a Markdown-formatted representation of a training scenario dict."""
    lines = []

    org = scenario.get("organisation_name", "Unknown organisation")
    lines.append(f"# Training Scenario: {org}")
    lines.append("")

    lines.append("## Organisation")
    lines.append(f"- **Name:** {scenario.get('organisation_name', '')}")
    lines.append(f"- **Type:** {scenario.get('organisation_type', '')}")
    lines.append(f"- **Staff count:** {scenario.get('staff_count', '')}")
    lines.append(f"- **Sector:** {scenario.get('sector', '')}")
    lines.append(f"- **Country context:** {scenario.get('country_context', '')}")
    lines.append("")

    lines.append("## AI Use and Concerns")
    lines.append(f"**Current AI use:**")
    lines.append(scenario.get("current_ai_use", ""))
    lines.append("")

    concerns = scenario.get("main_concerns", [])
    if concerns:
        lines.append("**Main concerns:**")
        for c in concerns:
            lines.append(f"- {c}")
        lines.append("")

    lines.append("## Training Setup")
    lines.append(f"- **Goal:** {scenario.get('training_goal', '')}")
    lines.append(f"- **Duration:** {scenario.get('training_duration', '')}")
    lines.append(f"- **Delivery mode:** {scenario.get('delivery_mode', '')}")
    lines.append("")

    roles = scenario.get("staff_roles", [])
    if roles:
        lines.append("**Staff roles attending:**")
        for r in roles:
            lines.append(f"- {r}")
        lines.append("")

    topics = scenario.get("priority_topics", [])
    if topics:
        lines.append("## Priority Topics")
        for t in topics:
            lines.append(f"- {t}")
        lines.append("")

    lines.append("---")
    lines.append(
        "*Synthetic scenario — for demonstration purposes only. "
        "Does not contain real organisational, learner, or personal data.*"
    )

    return "\n".join(lines)


def create_scenario_from_form_data(form_data: dict) -> dict:
    """Build a normalised scenario dict from raw Streamlit form data.

    Handles string-to-int conversion for staff_count.
    Splits newline-separated strings for list fields if needed.
    """
    scenario = dict(form_data)

    try:
        scenario["staff_count"] = int(form_data.get("staff_count", 0))
    except (TypeError, ValueError):
        scenario["staff_count"] = 0

    for list_field in ("main_concerns", "staff_roles", "priority_topics"):
        value = form_data.get(list_field, [])
        if isinstance(value, str):
            scenario[list_field] = [
                item.strip() for item in value.splitlines() if item.strip()
            ]
        else:
            scenario[list_field] = list(value)

    return scenario
