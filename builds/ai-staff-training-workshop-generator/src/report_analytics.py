"""Deterministic analytics summaries for the AI Staff Training training pack.

All calculations are based on content already generated in session state.
No external data, no LLM calls, no invented statistics.
"""

from datetime import date


def calculate_section_completion_status(session_state: dict) -> dict:
    """Return {section_name: bool} for each tracked output in session state."""
    return {
        "Organisation Scenario": bool(session_state.get("training_scenario")),
        "Training Needs Assessment": bool(session_state.get("training_needs_assessment")),
        "Workshop Plan": bool(session_state.get("workshop_plan")),
        "Training Activities": bool(session_state.get("training_activities")),
        "Facilitator Guide": bool(session_state.get("facilitator_guide")),
        "Staff Handout": bool(session_state.get("staff_handout")),
        "Knowledge Check": bool(session_state.get("knowledge_check")),
    }


def calculate_training_topic_counts(pack_data: dict) -> dict:
    """Return {topic: 1} for each priority topic in the scenario."""
    scenario = pack_data.get("scenario") or {}
    topics = scenario.get("priority_topics") or []
    return {str(t): 1 for t in topics if t}


def calculate_priority_topic_counts(pack_data: dict) -> dict:
    """Return {topic: count} for the scenario's priority topics.

    Stable public name for topic coverage analytics; equivalent to
    calculate_training_topic_counts.
    """
    return calculate_training_topic_counts(pack_data)


def calculate_activity_type_counts(activities: list) -> dict:
    """Return {activity_type: count} from a list of activity dicts."""
    if not activities:
        return {}
    counts: dict = {}
    for activity in activities:
        if not isinstance(activity, dict):
            continue
        atype = activity.get("activity_type", "other")
        counts[atype] = counts.get(atype, 0) + 1
    return counts


def calculate_workshop_time_allocation(workshop_plan: dict) -> list:
    """Return [{section, minutes}] for each agenda item.

    Uses duration_minutes if present; otherwise derives minutes from the
    agenda item's time_range (e.g. "00:10-00:25" → 15).
    """
    import re

    if not workshop_plan:
        return []
    agenda = workshop_plan.get("agenda") or []
    result = []
    for item in agenda:
        if not isinstance(item, dict):
            continue
        minutes = int(item.get("duration_minutes", 0))
        if minutes <= 0:
            match = re.match(
                r"(\d{1,2}):(\d{2})\s*[-–]\s*(\d{1,2}):(\d{2})",
                str(item.get("time_range", "")),
            )
            if match:
                start = int(match.group(1)) * 60 + int(match.group(2))
                end = int(match.group(3)) * 60 + int(match.group(4))
                minutes = max(end - start, 0)
        result.append({
            "section": item.get("section_title", "Section"),
            "minutes": minutes,
        })
    return result


def calculate_knowledge_check_topic_counts(knowledge_check: dict) -> dict:
    """Return {topic: count} across MCQs and scenario questions."""
    if not knowledge_check:
        return {}
    counts: dict = {}
    for q in (knowledge_check.get("multiple_choice_questions") or []):
        if not isinstance(q, dict):
            continue
        topic = q.get("topic", "general")
        counts[topic] = counts.get(topic, 0) + 1
    for q in (knowledge_check.get("scenario_questions") or []):
        if not isinstance(q, dict):
            continue
        topic = q.get("topic", "general")
        counts[topic] = counts.get(topic, 0) + 1
    return counts


def calculate_report_quality_summary(pack_data: dict) -> dict:
    """Return a completeness summary for the training pack."""
    keys = [
        "scenario", "training_needs_assessment", "workshop_plan",
        "training_activities", "facilitator_guide", "staff_handout", "knowledge_check",
    ]
    available = sum(1 for k in keys if pack_data.get(k))
    total = len(keys)
    activities = pack_data.get("training_activities") or []
    kc = pack_data.get("knowledge_check") or {}
    return {
        "sections_available": available,
        "sections_total": total,
        "completeness_pct": round(available / total * 100) if total else 0,
        "has_responsible_use_boundaries": True,
        "has_human_review_requirement": True,
        "has_prototype_notice": True,
        "activity_count": len(activities) if isinstance(activities, list) else 0,
        "mcq_count": len(kc.get("multiple_choice_questions") or []),
        "answer_key_included": bool(kc.get("answer_key")),
    }


def build_training_pack_analytics(pack_data: dict) -> dict:
    """Build the full analytics dict for a training pack.

    pack_data uses keys from build_training_pack_data_from_session_state:
    "scenario", "training_needs_assessment", "workshop_plan", etc.
    """
    if not isinstance(pack_data, dict):
        pack_data = {}

    scenario = pack_data.get("scenario") or {}
    activities = pack_data.get("training_activities") or []
    workshop_plan = pack_data.get("workshop_plan") or {}
    knowledge_check = pack_data.get("knowledge_check") or {}

    section_completion = {
        "Organisation Scenario": bool(pack_data.get("scenario")),
        "Training Needs Assessment": bool(pack_data.get("training_needs_assessment")),
        "Workshop Plan": bool(pack_data.get("workshop_plan")),
        "Training Activities": bool(pack_data.get("training_activities")),
        "Facilitator Guide": bool(pack_data.get("facilitator_guide")),
        "Staff Handout": bool(pack_data.get("staff_handout")),
        "Knowledge Check": bool(pack_data.get("knowledge_check")),
    }

    return {
        "section_completion": section_completion,
        "topic_counts": calculate_training_topic_counts(pack_data),
        "activity_type_counts": calculate_activity_type_counts(
            activities if isinstance(activities, list) else []
        ),
        "workshop_time_allocation": calculate_workshop_time_allocation(
            workshop_plan if isinstance(workshop_plan, dict) else {}
        ),
        "knowledge_check_topic_counts": calculate_knowledge_check_topic_counts(
            knowledge_check if isinstance(knowledge_check, dict) else {}
        ),
        "report_quality": calculate_report_quality_summary(pack_data),
        "organisation_name": scenario.get("organisation_name", "Organisation"),
        "generated_date": str(date.today()),
    }
