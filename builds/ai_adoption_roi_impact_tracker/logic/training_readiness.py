"""Training, Confidence, and Adoption Readiness engine for Build 7 Phase 4.

Analyses whether staff are becoming sufficiently trained, confident, and
adoption-ready to use AI-supported workflows safely and practically.

All figures are based on synthetic demo data only. No real client data.
"""

from logic.adoption_metrics import calculate_confidence_change

LOW_TRAINING_COMPLETION_THRESHOLD = 0.6
GOOD_TRAINING_COMPLETION_THRESHOLD = 0.75
STRONG_TRAINING_COMPLETION_THRESHOLD = 0.9

LOW_CONFIDENCE_SCORE_THRESHOLD = 3.0
GOOD_CONFIDENCE_SCORE_THRESHOLD = 3.5
STRONG_CONFIDENCE_SCORE_THRESHOLD = 4.0

MODERATE_CONFIDENCE_CHANGE_THRESHOLD = 0.5
STRONG_CONFIDENCE_CHANGE_THRESHOLD = 1.0

_READINESS_PRIORITY = {
    "Blocked": 0,
    "Needs support": 1,
    "Developing": 2,
    "Adoption ready": 3,
    "Scale ready": 4,
}


def classify_training_completion_band(training_completion_rate: float) -> str:
    """Classify a training completion rate into a descriptive band.

    Clamps values below 0.0 to 0.0 and above 1.0 to 1.0.
    Returns one of: 'Low completion', 'Moderate completion',
    'Good completion', 'Strong completion'.
    """
    rate = min(max(training_completion_rate, 0.0), 1.0)
    if rate < LOW_TRAINING_COMPLETION_THRESHOLD:
        return "Low completion"
    if rate < GOOD_TRAINING_COMPLETION_THRESHOLD:
        return "Moderate completion"
    if rate < STRONG_TRAINING_COMPLETION_THRESHOLD:
        return "Good completion"
    return "Strong completion"


def classify_confidence_level(confidence_score: float) -> str:
    """Classify a confidence score (1–5 scale) into a descriptive band.

    Clamps values to the 1.0 to 5.0 range.
    Returns one of: 'Low confidence', 'Developing confidence',
    'Good confidence', 'Strong confidence'.
    """
    score = min(max(confidence_score, 1.0), 5.0)
    if score < LOW_CONFIDENCE_SCORE_THRESHOLD:
        return "Low confidence"
    if score < GOOD_CONFIDENCE_SCORE_THRESHOLD:
        return "Developing confidence"
    if score < STRONG_CONFIDENCE_SCORE_THRESHOLD:
        return "Good confidence"
    return "Strong confidence"


def classify_confidence_growth(record: dict) -> str:
    """Classify the confidence change for a workflow record.

    Uses calculate_confidence_change() from logic.adoption_metrics.
    Returns one of: 'No growth', 'Small growth', 'Moderate growth', 'Strong growth'.
    """
    change = calculate_confidence_change(record)
    if change <= 0:
        return "No growth"
    if change < MODERATE_CONFIDENCE_CHANGE_THRESHOLD:
        return "Small growth"
    if change < STRONG_CONFIDENCE_CHANGE_THRESHOLD:
        return "Moderate growth"
    return "Strong growth"


def calculate_training_readiness_score(record: dict) -> float:
    """Return a synthetic training readiness score from 0 to 100.

    Scoring model (total 100 points):
    - Training completion: up to 40 points
    - Confidence after:    up to 35 points (normalised 1–5 scale)
    - Confidence growth:   up to 25 points (capped, no negative contribution)

    This is a synthetic consulting estimate, not an audited assessment.
    """
    training_rate = min(max(record.get("training_completion_rate", 0.0), 0.0), 1.0)
    confidence_after = min(max(record.get("confidence_after", 1.0), 1.0), 5.0)
    confidence_change = calculate_confidence_change(record)

    training_score = training_rate * 40
    confidence_after_score = ((confidence_after - 1.0) / 4.0) * 35
    confidence_growth_score = min(max(confidence_change, 0.0) / 2.0 * 25, 25)

    total = training_score + confidence_after_score + confidence_growth_score
    return round(min(max(total, 0.0), 100.0), 2)


def classify_training_readiness_band(score: float) -> str:
    """Classify a training readiness score into a readiness band.

    Returns one of: 'Not ready', 'Partly ready',
    'Ready with support', 'Ready to scale'.
    """
    if score < 40:
        return "Not ready"
    if score < 60:
        return "Partly ready"
    if score < 80:
        return "Ready with support"
    return "Ready to scale"


def identify_training_support_need(record: dict) -> str:
    """Identify the primary training support need for a workflow record.

    Priority order: Foundation training > Workflow-specific coaching >
    Confidence reinforcement > Scale enablement > Light-touch support.

    Returns one of: 'Foundation training', 'Workflow-specific coaching',
    'Confidence reinforcement', 'Light-touch support', 'Scale enablement'.
    """
    training_rate = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)
    confidence_change = calculate_confidence_change(record)

    if training_rate < LOW_TRAINING_COMPLETION_THRESHOLD:
        return "Foundation training"

    if training_rate >= LOW_TRAINING_COMPLETION_THRESHOLD and confidence_after < GOOD_CONFIDENCE_SCORE_THRESHOLD:
        return "Workflow-specific coaching"

    if confidence_after >= GOOD_CONFIDENCE_SCORE_THRESHOLD and confidence_change < MODERATE_CONFIDENCE_CHANGE_THRESHOLD:
        return "Confidence reinforcement"

    if (
        training_rate >= STRONG_TRAINING_COMPLETION_THRESHOLD
        and confidence_after >= STRONG_CONFIDENCE_SCORE_THRESHOLD
        and confidence_change >= STRONG_CONFIDENCE_CHANGE_THRESHOLD
    ):
        return "Scale enablement"

    return "Light-touch support"


def classify_staff_adoption_readiness(record: dict) -> str:
    """Classify the staff adoption readiness status for a workflow record.

    Priority order: Blocked > Needs support > Scale ready >
    Adoption ready > Developing.

    Returns one of: 'Blocked', 'Needs support', 'Developing',
    'Adoption ready', 'Scale ready'.
    """
    adoption_status = record.get("adoption_status", "")
    pilot_status = record.get("pilot_status", "")
    training_rate = record.get("training_completion_rate", 0.0)
    confidence_after = record.get("confidence_after", 0.0)
    confidence_change = calculate_confidence_change(record)
    score = calculate_training_readiness_score(record)

    if adoption_status == "Stop" or pilot_status == "Paused":
        return "Blocked"

    if training_rate < LOW_TRAINING_COMPLETION_THRESHOLD or confidence_after < LOW_CONFIDENCE_SCORE_THRESHOLD:
        return "Needs support"

    if (
        score >= 80
        and training_rate >= STRONG_TRAINING_COMPLETION_THRESHOLD
        and confidence_after >= STRONG_CONFIDENCE_SCORE_THRESHOLD
        and confidence_change >= STRONG_CONFIDENCE_CHANGE_THRESHOLD
        and adoption_status == "Scale"
    ):
        return "Scale ready"

    if (
        score >= 70
        and training_rate >= GOOD_TRAINING_COMPLETION_THRESHOLD
        and confidence_after >= GOOD_CONFIDENCE_SCORE_THRESHOLD
    ):
        return "Adoption ready"

    return "Developing"


def build_training_readiness_summary(record: dict) -> dict:
    """Build a full training readiness summary dict for one adoption record."""
    training_rate = record.get("training_completion_rate", 0.0)
    confidence_before = record.get("confidence_before", 0.0)
    confidence_after = record.get("confidence_after", 0.0)
    confidence_change = calculate_confidence_change(record)
    score = calculate_training_readiness_score(record)

    return {
        "organisation_id": record.get("organisation_id", ""),
        "organisation_name": record.get("organisation_name", ""),
        "workflow_id": record.get("workflow_id", ""),
        "workflow_name": record.get("workflow_name", ""),
        "related_build": record.get("related_build", ""),
        "staff_group": record.get("staff_group", ""),
        "training_completion_rate": training_rate,
        "training_completion_band": classify_training_completion_band(training_rate),
        "confidence_before": confidence_before,
        "confidence_after": confidence_after,
        "confidence_before_band": classify_confidence_level(confidence_before),
        "confidence_after_band": classify_confidence_level(confidence_after),
        "confidence_change": confidence_change,
        "confidence_growth_band": classify_confidence_growth(record),
        "training_readiness_score": score,
        "training_readiness_band": classify_training_readiness_band(score),
        "training_support_need": identify_training_support_need(record),
        "staff_adoption_readiness": classify_staff_adoption_readiness(record),
        "adoption_status": record.get("adoption_status", ""),
        "pilot_status": record.get("pilot_status", ""),
        "review_decision": record.get("review_decision", ""),
    }


def build_all_training_readiness_summaries(records: list[dict]) -> list[dict]:
    """Return one training readiness summary per adoption record."""
    return [build_training_readiness_summary(record) for record in records]


def summarise_training_readiness_by_staff_group(tr_summaries: list[dict]) -> list[dict]:
    """Group training readiness summaries by staff group.

    Accepts the output of build_all_training_readiness_summaries.
    Returns one summary dict per staff group.
    """
    group_map: dict[str, dict] = {}

    for summary in tr_summaries:
        group = summary["staff_group"]
        if group not in group_map:
            group_map[group] = {
                "staff_group": group,
                "workflow_count": 0,
                "_sum_training_rate": 0.0,
                "_sum_confidence_before": 0.0,
                "_sum_confidence_after": 0.0,
                "_sum_confidence_change": 0.0,
                "_sum_score": 0.0,
                "blocked_count": 0,
                "needs_support_count": 0,
                "developing_count": 0,
                "adoption_ready_count": 0,
                "scale_ready_count": 0,
                "_support_needs": [],
            }

        entry = group_map[group]
        entry["workflow_count"] += 1
        entry["_sum_training_rate"] += summary["training_completion_rate"]
        entry["_sum_confidence_before"] += summary["confidence_before"]
        entry["_sum_confidence_after"] += summary["confidence_after"]
        entry["_sum_confidence_change"] += summary["confidence_change"]
        entry["_sum_score"] += summary["training_readiness_score"]
        entry["_support_needs"].append(summary["training_support_need"])

        readiness = summary["staff_adoption_readiness"]
        if readiness == "Blocked":
            entry["blocked_count"] += 1
        elif readiness == "Needs support":
            entry["needs_support_count"] += 1
        elif readiness == "Developing":
            entry["developing_count"] += 1
        elif readiness == "Adoption ready":
            entry["adoption_ready_count"] += 1
        elif readiness == "Scale ready":
            entry["scale_ready_count"] += 1

    result = []
    for entry in group_map.values():
        count = entry["workflow_count"]
        result.append(
            {
                "staff_group": entry["staff_group"],
                "workflow_count": count,
                "average_training_completion_rate": round(entry["_sum_training_rate"] / count, 2)
                if count
                else 0.0,
                "average_confidence_before": round(entry["_sum_confidence_before"] / count, 2)
                if count
                else 0.0,
                "average_confidence_after": round(entry["_sum_confidence_after"] / count, 2)
                if count
                else 0.0,
                "average_confidence_change": round(entry["_sum_confidence_change"] / count, 2)
                if count
                else 0.0,
                "average_training_readiness_score": round(entry["_sum_score"] / count, 2)
                if count
                else 0.0,
                "blocked_count": entry["blocked_count"],
                "needs_support_count": entry["needs_support_count"],
                "developing_count": entry["developing_count"],
                "adoption_ready_count": entry["adoption_ready_count"],
                "scale_ready_count": entry["scale_ready_count"],
                "dominant_support_need": _dominant_support_need(entry["_support_needs"]),
            }
        )

    return result


def summarise_training_readiness_by_organisation(tr_summaries: list[dict]) -> list[dict]:
    """Group training readiness summaries by organisation.

    Accepts the output of build_all_training_readiness_summaries.
    Returns one summary dict per organisation.
    """
    org_map: dict[str, dict] = {}

    for summary in tr_summaries:
        org_id = summary["organisation_id"]
        if org_id not in org_map:
            org_map[org_id] = {
                "organisation_id": org_id,
                "organisation_name": summary["organisation_name"],
                "workflow_count": 0,
                "_sum_training_rate": 0.0,
                "_sum_confidence_before": 0.0,
                "_sum_confidence_after": 0.0,
                "_sum_confidence_change": 0.0,
                "_sum_score": 0.0,
                "blocked_count": 0,
                "needs_support_count": 0,
                "developing_count": 0,
                "adoption_ready_count": 0,
                "scale_ready_count": 0,
                "_support_needs": [],
            }

        entry = org_map[org_id]
        entry["workflow_count"] += 1
        entry["_sum_training_rate"] += summary["training_completion_rate"]
        entry["_sum_confidence_before"] += summary["confidence_before"]
        entry["_sum_confidence_after"] += summary["confidence_after"]
        entry["_sum_confidence_change"] += summary["confidence_change"]
        entry["_sum_score"] += summary["training_readiness_score"]
        entry["_support_needs"].append(summary["training_support_need"])

        readiness = summary["staff_adoption_readiness"]
        if readiness == "Blocked":
            entry["blocked_count"] += 1
        elif readiness == "Needs support":
            entry["needs_support_count"] += 1
        elif readiness == "Developing":
            entry["developing_count"] += 1
        elif readiness == "Adoption ready":
            entry["adoption_ready_count"] += 1
        elif readiness == "Scale ready":
            entry["scale_ready_count"] += 1

    result = []
    for entry in org_map.values():
        count = entry["workflow_count"]
        result.append(
            {
                "organisation_id": entry["organisation_id"],
                "organisation_name": entry["organisation_name"],
                "workflow_count": count,
                "average_training_completion_rate": round(entry["_sum_training_rate"] / count, 2)
                if count
                else 0.0,
                "average_confidence_before": round(entry["_sum_confidence_before"] / count, 2)
                if count
                else 0.0,
                "average_confidence_after": round(entry["_sum_confidence_after"] / count, 2)
                if count
                else 0.0,
                "average_confidence_change": round(entry["_sum_confidence_change"] / count, 2)
                if count
                else 0.0,
                "average_training_readiness_score": round(entry["_sum_score"] / count, 2)
                if count
                else 0.0,
                "blocked_count": entry["blocked_count"],
                "needs_support_count": entry["needs_support_count"],
                "developing_count": entry["developing_count"],
                "adoption_ready_count": entry["adoption_ready_count"],
                "scale_ready_count": entry["scale_ready_count"],
                "dominant_support_need": _dominant_support_need(entry["_support_needs"]),
            }
        )

    return result


def summarise_training_readiness_by_related_build(tr_summaries: list[dict]) -> list[dict]:
    """Group training readiness summaries by related build.

    Accepts the output of build_all_training_readiness_summaries.
    Returns one summary dict per related build.
    """
    build_map: dict[str, dict] = {}

    for summary in tr_summaries:
        build = summary["related_build"]
        if build not in build_map:
            build_map[build] = {
                "related_build": build,
                "workflow_count": 0,
                "_sum_training_rate": 0.0,
                "_sum_confidence_change": 0.0,
                "_sum_score": 0.0,
                "blocked_count": 0,
                "needs_support_count": 0,
                "developing_count": 0,
                "adoption_ready_count": 0,
                "scale_ready_count": 0,
                "_support_needs": [],
            }

        entry = build_map[build]
        entry["workflow_count"] += 1
        entry["_sum_training_rate"] += summary["training_completion_rate"]
        entry["_sum_confidence_change"] += summary["confidence_change"]
        entry["_sum_score"] += summary["training_readiness_score"]
        entry["_support_needs"].append(summary["training_support_need"])

        readiness = summary["staff_adoption_readiness"]
        if readiness == "Blocked":
            entry["blocked_count"] += 1
        elif readiness == "Needs support":
            entry["needs_support_count"] += 1
        elif readiness == "Developing":
            entry["developing_count"] += 1
        elif readiness == "Adoption ready":
            entry["adoption_ready_count"] += 1
        elif readiness == "Scale ready":
            entry["scale_ready_count"] += 1

    result = []
    for entry in build_map.values():
        count = entry["workflow_count"]
        result.append(
            {
                "related_build": entry["related_build"],
                "workflow_count": count,
                "average_training_completion_rate": round(entry["_sum_training_rate"] / count, 2)
                if count
                else 0.0,
                "average_confidence_change": round(entry["_sum_confidence_change"] / count, 2)
                if count
                else 0.0,
                "average_training_readiness_score": round(entry["_sum_score"] / count, 2)
                if count
                else 0.0,
                "blocked_count": entry["blocked_count"],
                "needs_support_count": entry["needs_support_count"],
                "developing_count": entry["developing_count"],
                "adoption_ready_count": entry["adoption_ready_count"],
                "scale_ready_count": entry["scale_ready_count"],
                "dominant_support_need": _dominant_support_need(entry["_support_needs"]),
            }
        )

    return result


def _dominant_support_need(support_needs: list[str]) -> str:
    """Return the most common training support need from a list."""
    counts: dict[str, int] = {}
    for need in support_needs:
        counts[need] = counts.get(need, 0) + 1
    if not counts:
        return ""
    return max(counts, key=lambda k: counts[k])


def prioritise_training_support_actions(tr_summaries: list[dict]) -> list[dict]:
    """Return training readiness summaries sorted by support priority.

    Priority order: Blocked > Needs support > Developing >
    Adoption ready > Scale ready.

    Within the same readiness status, sorts by: training_readiness_score
    ascending, training_completion_rate ascending, confidence_after ascending.
    This puts the workflows most in need of support at the top.
    """

    def sort_key(summary: dict) -> tuple:
        readiness = summary.get("staff_adoption_readiness", "Developing")
        priority = _READINESS_PRIORITY.get(readiness, 2)
        score = summary.get("training_readiness_score", 0.0)
        training = summary.get("training_completion_rate", 0.0)
        confidence = summary.get("confidence_after", 0.0)
        return (priority, score, training, confidence)

    return sorted(tr_summaries, key=sort_key)


def generate_training_support_recommendation(summary: dict) -> str:
    """Return deterministic consulting recommendation text for a training readiness summary."""
    readiness = summary.get("staff_adoption_readiness", "")
    support_need = summary.get("training_support_need", "")

    if readiness == "Blocked":
        return (
            "Do not scale this workflow yet. Resolve the paused or stopped adoption status "
            "before investing in further training."
        )
    if support_need == "Foundation training":
        return (
            "Run a foundation AI use session before expecting staff to adopt this workflow. "
            "Focus on safe prompting, review habits, and when not to use AI."
        )
    if support_need == "Workflow-specific coaching":
        return (
            "Provide workflow-specific coaching with examples from this task. "
            "Staff have some training exposure but need practical confidence using AI in context."
        )
    if support_need == "Confidence reinforcement":
        return (
            "Use confidence reinforcement activities such as paired practice, worked examples, "
            "and short review checklists to consolidate adoption."
        )
    if support_need == "Scale enablement":
        return (
            "Prepare scale enablement materials such as quick-reference guides, peer champions, "
            "and sample outputs for wider rollout."
        )
    if support_need == "Light-touch support":
        return (
            "Continue with light-touch support. Staff appear to be developing confidence, "
            "but adoption should still be monitored through quality and risk evidence."
        )
    return (
        "Review training completion, confidence, and workflow evidence before deciding "
        "the next support action."
    )


def add_training_recommendations_to_summaries(summaries: list[dict]) -> list[dict]:
    """Return summaries with an additional 'training_recommendation' field.

    Does not mutate the original summaries.
    """
    return [
        {**summary, "training_recommendation": generate_training_support_recommendation(summary)}
        for summary in summaries
    ]
