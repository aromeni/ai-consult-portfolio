"""Phase 1 capstone overview logic for Build 9."""

_REQUIRED_CLIENT_FIELDS = {
    "client_id",
    "organisation_name",
    "sector",
    "staff_count",
    "capstone_stage",
    "primary_ai_goal",
    "consulting_priority",
}

_REQUIRED_STAGE_FIELDS = {
    "stage_id",
    "client_id",
    "organisation_name",
    "build_number",
    "build_name",
    "journey_stage",
    "stage_status",
    "stage_summary",
    "evidence_strength",
    "consulting_value",
}

_REQUIRED_INDICATOR_FIELDS = {
    "client_id",
    "organisation_name",
    "readiness_position",
    "governance_position",
    "training_position",
    "roi_position",
    "delivery_position",
    "commercial_position",
    "overall_capstone_status",
    "recommended_next_step",
}

_ALLOWED_STAGE_STATUSES = {"Not started", "In progress", "Completed", "Needs review"}
_ALLOWED_EVIDENCE_STRENGTHS = {"Weak", "Moderate", "Strong", "Very strong"}
_ALLOWED_CAPSTONE_STATUSES = {
    "Needs more evidence",
    "Developing demo",
    "Portfolio-ready demo",
    "Strong portfolio asset",
}


def validate_capstone_client(client: dict) -> list[str]:
    warnings = []
    missing = _REQUIRED_CLIENT_FIELDS - set(client.keys())
    for field in sorted(missing):
        warnings.append(f"Missing required field: {field}")
    if not missing:
        if not str(client.get("organisation_name", "")).strip():
            warnings.append("organisation_name must not be empty")
        if not isinstance(client.get("staff_count"), int) or client["staff_count"] < 1:
            warnings.append("staff_count must be an integer of 1 or more")
        if not str(client.get("primary_ai_goal", "")).strip():
            warnings.append("primary_ai_goal must not be empty")
        if not str(client.get("consulting_priority", "")).strip():
            warnings.append("consulting_priority must not be empty")
    return warnings


def validate_cross_build_stage(stage: dict) -> list[str]:
    warnings = []
    missing = _REQUIRED_STAGE_FIELDS - set(stage.keys())
    for field in sorted(missing):
        warnings.append(f"Missing required field: {field}")
    if not missing:
        status = stage.get("stage_status", "")
        if status not in _ALLOWED_STAGE_STATUSES:
            warnings.append(f"Invalid stage_status: '{status}'")
        strength = stage.get("evidence_strength", "")
        if strength not in _ALLOWED_EVIDENCE_STRENGTHS:
            warnings.append(f"Invalid evidence_strength: '{strength}'")
        if not str(stage.get("build_name", "")).strip():
            warnings.append("build_name must not be empty")
        if not str(stage.get("journey_stage", "")).strip():
            warnings.append("journey_stage must not be empty")
        if not str(stage.get("stage_summary", "")).strip():
            warnings.append("stage_summary must not be empty")
        if not str(stage.get("consulting_value", "")).strip():
            warnings.append("consulting_value must not be empty")
    return warnings


def validate_capstone_indicator(indicator: dict) -> list[str]:
    warnings = []
    missing = _REQUIRED_INDICATOR_FIELDS - set(indicator.keys())
    for field in sorted(missing):
        warnings.append(f"Missing required field: {field}")
    if not missing:
        status = indicator.get("overall_capstone_status", "")
        if status not in _ALLOWED_CAPSTONE_STATUSES:
            warnings.append(f"Invalid overall_capstone_status: '{status}'")
        if not str(indicator.get("recommended_next_step", "")).strip():
            warnings.append("recommended_next_step must not be empty")
    return warnings


def validate_all_capstone_data(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> dict:
    warnings = []

    valid_clients = 0
    for client in clients:
        issues = validate_capstone_client(client)
        if issues:
            cid = client.get("client_id", "unknown")
            for issue in issues:
                warnings.append(f"Client {cid}: {issue}")
        else:
            valid_clients += 1

    valid_stages = 0
    client_ids = {c["client_id"] for c in clients if "client_id" in c}
    for stage in stages:
        issues = validate_cross_build_stage(stage)
        sid = stage.get("stage_id", "unknown")
        if stage.get("client_id") not in client_ids:
            issues.append(f"client_id '{stage.get('client_id')}' does not match any known client")
        if issues:
            for issue in issues:
                warnings.append(f"Stage {sid}: {issue}")
        else:
            valid_stages += 1

    valid_indicators = 0
    for indicator in indicators:
        issues = validate_capstone_indicator(indicator)
        if issues:
            iid = indicator.get("client_id", "unknown")
            for issue in issues:
                warnings.append(f"Indicator {iid}: {issue}")
        else:
            valid_indicators += 1

    return {
        "total_clients": len(clients),
        "total_stages": len(stages),
        "total_indicators": len(indicators),
        "valid_clients": valid_clients,
        "valid_stages": valid_stages,
        "valid_indicators": valid_indicators,
        "warnings": warnings,
    }


def get_stages_for_client(stages: list[dict], client_id: str) -> list[dict]:
    return [s for s in stages if s.get("client_id") == client_id]


def get_indicator_for_client(indicators: list[dict], client_id: str) -> dict | None:
    for indicator in indicators:
        if indicator.get("client_id") == client_id:
            return indicator
    return None


def calculate_stage_counts_by_status(stages: list[dict]) -> dict:
    counts = {status: 0 for status in sorted(_ALLOWED_STAGE_STATUSES)}
    for stage in stages:
        status = stage.get("stage_status", "")
        if status in counts:
            counts[status] += 1
    return counts


def calculate_evidence_counts_by_strength(stages: list[dict]) -> dict:
    counts = {strength: 0 for strength in sorted(_ALLOWED_EVIDENCE_STRENGTHS)}
    for stage in stages:
        strength = stage.get("evidence_strength", "")
        if strength in counts:
            counts[strength] += 1
    return counts


def summarise_phase_1_capstone(
    clients: list[dict],
    stages: list[dict],
    indicators: list[dict],
) -> dict:
    status_counts = calculate_stage_counts_by_status(stages)
    evidence_counts = calculate_evidence_counts_by_strength(stages)
    portfolio_ready_statuses = {"Portfolio-ready demo", "Strong portfolio asset"}
    portfolio_ready_count = sum(
        1 for i in indicators
        if i.get("overall_capstone_status") in portfolio_ready_statuses
    )
    return {
        "total_clients": len(clients),
        "total_cross_build_stages": len(stages),
        "total_indicators": len(indicators),
        "completed_stage_count": status_counts.get("Completed", 0),
        "in_progress_stage_count": status_counts.get("In progress", 0),
        "needs_review_stage_count": status_counts.get("Needs review", 0),
        "strong_or_very_strong_evidence_count": (
            evidence_counts.get("Strong", 0) + evidence_counts.get("Very strong", 0)
        ),
        "portfolio_ready_or_strong_asset_count": portfolio_ready_count,
    }
