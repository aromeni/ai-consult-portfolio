"""Training pack assembly and export for the AI Staff Training and Workshop Generator.

Phase 8: combines all generated outputs into a downloadable Markdown training pack.
All content is assembled from synthetic organisation scenario data only.
No real learner data, safeguarding case details, or personal information.
"""

import re
from datetime import date

_RESPONSIBLE_USE_NOTE = (
    "This training pack is generated from a synthetic organisation scenario only. "
    "It must not be used with real learner data, safeguarding case details, "
    "confidential client records, staff HR data, personal data, or regulated "
    "information without appropriate governance, approvals, and responsible owners. "
    "AI-generated or template-generated training materials must be reviewed by a "
    "responsible human before use. This prototype does not provide legal, "
    "safeguarding, HR, compliance, medical, financial, academic-integrity, or "
    "professional advice."
)

_PROTOTYPE_NOTE = (
    "Production-style responsible AI training prototype, not a production "
    "compliance or legal training system."
)

_ALL_SECTIONS = [
    "scenario",
    "training_needs_assessment",
    "workshop_plan",
    "training_activities",
    "facilitator_guide",
    "staff_handout",
    "knowledge_check",
    "answer_key",
    "facilitator_review_checklist",
    "responsible_use_boundaries",
    "prototype_limitations",
    "recommended_next_steps",
]

_SECTION_LABELS = {
    "scenario": "Organisation Scenario Summary",
    "training_needs_assessment": "Training Needs Assessment",
    "workshop_plan": "Workshop Plan",
    "training_activities": "Training Activities",
    "facilitator_guide": "Facilitator Guide",
    "staff_handout": "Staff Handout",
    "knowledge_check": "Knowledge Check",
    "answer_key": "Answer Key",
    "facilitator_review_checklist": "Facilitator Review Checklist",
    "responsible_use_boundaries": "Responsible-Use Boundaries",
    "prototype_limitations": "Prototype Limitations",
    "recommended_next_steps": "Recommended Next Steps",
}


def get_training_pack_required_sections() -> list:
    """Return the list of required section keys for the training pack."""
    return ["scenario"]


def get_training_pack_optional_sections() -> list:
    """Return the list of optional/recommended section keys."""
    return [
        "training_needs_assessment",
        "workshop_plan",
        "training_activities",
        "facilitator_guide",
        "staff_handout",
        "knowledge_check",
        "answer_key",
        "facilitator_review_checklist",
        "responsible_use_boundaries",
        "prototype_limitations",
        "recommended_next_steps",
    ]


def check_training_pack_readiness(session_state: dict) -> dict:
    """Inspect session state and return a readiness dict."""
    available = []
    missing = []

    recommended_keys = [
        "training_scenario",
        "training_needs_assessment",
        "workshop_plan",
        "training_activities",
        "facilitator_guide",
        "staff_handout",
        "knowledge_check",
    ]

    label_map = {
        "training_scenario": "Organisation Scenario",
        "training_needs_assessment": "Training Needs Assessment",
        "workshop_plan": "Workshop Plan",
        "training_activities": "Training Activities",
        "facilitator_guide": "Facilitator Guide",
        "staff_handout": "Staff Handout",
        "knowledge_check": "Knowledge Check",
    }

    for key in recommended_keys:
        label = label_map[key]
        if session_state.get(key):
            available.append(label)
        else:
            missing.append(label)

    has_scenario = bool(session_state.get("training_scenario"))
    is_ready = has_scenario

    next_steps = []
    if not has_scenario:
        next_steps.append("Go to Organisation Scenario and load or create the demo scenario.")
    else:
        for key in recommended_keys[1:]:
            if not session_state.get(key):
                page_map = {
                    "training_needs_assessment": "Training Needs Assessment",
                    "workshop_plan": "Workshop Planner",
                    "training_activities": "Activity Generator",
                    "facilitator_guide": "Facilitator Guide",
                    "staff_handout": "Staff Handout",
                    "knowledge_check": "Knowledge Check",
                }
                next_steps.append(
                    f"Go to {page_map[key]} and generate the output before exporting."
                )

    return {
        "is_ready": is_ready,
        "available_sections": available,
        "missing_sections": missing,
        "recommended_next_steps": next_steps,
    }


def build_training_pack_data_from_session_state(session_state: dict) -> dict:
    """Build and return the training pack data dict from session state."""
    scenario = session_state.get("training_scenario") or {}
    org = scenario.get("organisation_name", "Unnamed organisation")

    return {
        "pack_title": "Responsible AI Staff Training Pack",
        "organisation_name": org,
        "generated_date": str(date.today()),
        "scenario": scenario,
        "training_needs_assessment": session_state.get("training_needs_assessment"),
        "workshop_plan": session_state.get("workshop_plan"),
        "training_activities": session_state.get("training_activities"),
        "facilitator_guide": session_state.get("facilitator_guide"),
        "staff_handout": session_state.get("staff_handout"),
        "knowledge_check": session_state.get("knowledge_check"),
        "training_needs_markdown": session_state.get("training_needs_markdown"),
        "workshop_plan_markdown": session_state.get("workshop_plan_markdown"),
        "training_activities_markdown": session_state.get("training_activities_markdown"),
        "facilitator_guide_markdown": session_state.get("facilitator_guide_markdown"),
        "staff_handout_markdown": session_state.get("staff_handout_markdown"),
        "knowledge_check_markdown": session_state.get("knowledge_check_markdown"),
        "source_outputs_available": {
            "scenario": bool(session_state.get("training_scenario")),
            "training_needs_assessment": bool(session_state.get("training_needs_assessment")),
            "workshop_plan": bool(session_state.get("workshop_plan")),
            "training_activities": bool(session_state.get("training_activities")),
            "facilitator_guide": bool(session_state.get("facilitator_guide")),
            "staff_handout": bool(session_state.get("staff_handout")),
            "knowledge_check": bool(session_state.get("knowledge_check")),
        },
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def generate_training_pack_cover_section(pack_data: dict) -> str:
    """Return Markdown for the training pack cover section."""
    scenario = pack_data.get("scenario") or {}
    lines = [
        f"**Pack title:** {pack_data.get('pack_title', 'Responsible AI Staff Training Pack')}",
        "",
        f"**Organisation:** {pack_data.get('organisation_name', 'Unnamed organisation')}",
        f"**Organisation type:** {scenario.get('organisation_type', 'Not specified')}",
        f"**Sector:** {scenario.get('sector', 'Not specified')}",
        f"**Staff roles:** {', '.join(scenario.get('staff_roles', ['All staff']))}",
        f"**Training duration:** {scenario.get('training_duration', 'Not specified')}",
        f"**Delivery mode:** {scenario.get('delivery_mode', 'Not specified')}",
        f"**Generated date:** {pack_data.get('generated_date', str(date.today()))}",
        "",
        f"**Prototype status:** {pack_data.get('prototype_note', _PROTOTYPE_NOTE)}",
        "",
        "> All scenarios in this training pack are synthetic. "
        "Outputs require human review before use in a real training session.",
    ]
    return "\n".join(lines)


def generate_training_pack_table_of_contents(include_sections: dict) -> str:
    """Return Markdown for the table of contents."""
    lines = []
    counter = 1
    for key in _ALL_SECTIONS:
        if key in ("responsible_use_boundaries", "prototype_limitations", "recommended_next_steps",
                   "answer_key", "facilitator_review_checklist"):
            if include_sections.get(key, True):
                lines.append(f"{counter}. {_SECTION_LABELS[key]}")
                counter += 1
        else:
            if include_sections.get(key, True):
                lines.append(f"{counter}. {_SECTION_LABELS[key]}")
                counter += 1
    return "\n".join(lines)


def generate_training_pack_responsible_use_section() -> str:
    """Return Markdown for the responsible-use boundaries section."""
    lines = [
        "This training pack is generated from a synthetic organisation scenario only. "
        "It must not be used with real learner data, safeguarding case details, "
        "confidential client records, staff HR data, personal data, or regulated "
        "information without appropriate governance, approvals, and responsible owners.",
        "",
        "Do not paste real learner data, safeguarding information, staff HR data, "
        "confidential records, personal data, or regulated information into this prototype.",
        "",
        "AI-generated or template-generated training materials must be reviewed by a "
        "responsible human before use.",
        "",
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice.",
    ]
    return "\n".join(lines)


def generate_training_pack_limitations_section() -> str:
    """Return Markdown for the prototype limitations section."""
    items = [
        "This is a production-style prototype, not a production training compliance system.",
        "The pack is generated from synthetic scenario data — the BrightPath scenario is fictional.",
        "Outputs are deterministic and template-based; no external AI or LLM APIs are used.",
        "The pack has not been validated against a real organisation's policy, legal obligations, "
        "safeguarding procedures, HR process, or compliance framework.",
        "The materials require human review before any real-world use.",
        "Local policy owners, safeguarding leads, data protection leads, HR leads, quality leads, "
        "and managers should review the content before delivery.",
    ]
    return "\n".join(f"- {item}" for item in items)


def generate_facilitator_review_checklist() -> list:
    """Return a list of facilitator review checklist items."""
    return [
        "Check that all examples and scenarios in the pack are synthetic — no real learner, client, or staff data.",
        "Confirm no real learner, safeguarding, HR, client, personal, or regulated information is included.",
        "Confirm the organisation's approved AI tools and current AI policy position before delivery.",
        "Confirm safeguarding escalation route (designated safeguarding lead and contact) before the session.",
        "Confirm data protection escalation route (DPO, data protection lead, or manager) before the session.",
        "Confirm that staff understand human review responsibilities — AI is a support tool, not a decision-maker.",
        "Confirm activities are appropriate for the audience's roles, experience level, and AI familiarity.",
        "Confirm the staff handout reflects local organisational policy before it is distributed.",
        "Confirm the knowledge check is reviewed by a responsible human before use.",
        "Confirm this pack is treated as training support material, not legal, safeguarding, or compliance advice.",
    ]


def generate_training_pack_next_steps(pack_data: dict) -> list:
    """Return a list of recommended next steps for the organisation."""
    org = pack_data.get("organisation_name", "the organisation")
    return [
        f"Review the training pack with {org}'s manager or responsible owner before delivery.",
        "Align examples and scenario cards with the organisation's approved AI tools and policy.",
        "Confirm the escalation routes (safeguarding lead, DPO, manager) listed in the staff handout.",
        "Run a pilot workshop with a small group before full delivery — collect facilitator notes.",
        "Collect staff feedback after the session and update the handout and knowledge check accordingly.",
        "Keep a record of training completion if required by organisational policy or sector regulations.",
        "Schedule a review of the training materials as AI tools, sector guidance, and organisational policy evolve.",
        "Share the knowledge check answer key only with facilitators and managers — not with staff before the session.",
        "Revisit the Training Needs Assessment if the organisation's AI use or staff concerns change significantly.",
    ]


def _section_header(number: int, title: str) -> str:
    return f"## {number}. {title}"


def _missing_section_note(section_title: str, page_name: str) -> str:
    return (
        f"*No {section_title} is available yet. "
        f"Run the {page_name} page to include this section.*"
    )


def _format_scenario_section(scenario: dict) -> str:
    if not scenario:
        return _missing_section_note("Organisation Scenario", "Organisation Scenario")
    lines = [
        f"**Organisation:** {scenario.get('organisation_name', 'Not specified')}",
        f"**Organisation type:** {scenario.get('organisation_type', 'Not specified')}",
        f"**Staff count:** {scenario.get('staff_count', 'Not specified')}",
        f"**Sector:** {scenario.get('sector', 'Not specified')}",
        f"**Country context:** {scenario.get('country_context', 'Not specified')}",
        f"**Training goal:** {scenario.get('training_goal', 'Not specified')}",
        f"**Delivery mode:** {scenario.get('delivery_mode', 'Not specified')}",
        f"**Training duration:** {scenario.get('training_duration', 'Not specified')}",
        "",
    ]
    if scenario.get("current_ai_use"):
        lines.append(f"**Current AI use:** {scenario['current_ai_use']}")
        lines.append("")
    staff_roles = scenario.get("staff_roles", [])
    if staff_roles:
        lines.append(f"**Staff roles:** {', '.join(staff_roles)}")
        lines.append("")
    priority_topics = scenario.get("priority_topics", [])
    if priority_topics:
        lines.append("**Priority training topics:**")
        for topic in priority_topics:
            lines.append(f"- {topic}")
        lines.append("")
    main_concerns = scenario.get("main_concerns", [])
    if main_concerns:
        concerns_list = (
            main_concerns
            if isinstance(main_concerns, list)
            else [c.strip() for c in main_concerns.split("\n") if c.strip()]
        )
        lines.append("**Main concerns:**")
        for concern in concerns_list:
            lines.append(f"- {concern}")
    return "\n".join(lines)


def _format_needs_assessment_section(assessment: dict, markdown: str | None) -> str:
    if not assessment:
        return _missing_section_note("Training Needs Assessment", "Training Needs Assessment")
    if markdown:
        return _strip_top_heading(markdown)
    lines = [
        f"**Training focus:** {assessment.get('overall_training_focus', 'Responsible AI use')}",
        f"**Recommended session:** {assessment.get('recommended_session_type', 'Workshop')}",
        "",
        f"**Risk summary:** {assessment.get('risk_summary', '')}",
        "",
    ]
    outcomes = assessment.get("recommended_learning_outcomes", [])
    if outcomes:
        lines.append("**Recommended learning outcomes:**")
        for o in outcomes:
            lines.append(f"- {o}")
        lines.append("")
    topics = assessment.get("topic_assessments", [])
    if topics:
        lines.append("**Topic priorities:**")
        for t in topics:
            lines.append(
                f"- **{t.get('title', '')}** — {t.get('priority_level', '').upper()} priority"
            )
    return "\n".join(lines)


def _format_workshop_plan_section(plan: dict, markdown: str | None) -> str:
    if not plan:
        return _missing_section_note("Workshop Plan", "Workshop Planner")
    if markdown:
        return _strip_top_heading(markdown)
    lines = [
        f"**Workshop title:** {plan.get('workshop_title', '')}",
        f"**Duration:** {plan.get('duration_minutes', '')} minutes",
        f"**Delivery mode:** {plan.get('delivery_mode', '')}",
        f"**Audience:** {', '.join(plan.get('audience', []))}",
        "",
    ]
    outcomes = plan.get("learning_outcomes", [])
    if outcomes:
        lines.append("**Learning outcomes:**")
        for o in outcomes:
            lines.append(f"- {o}")
        lines.append("")
    agenda = plan.get("agenda", [])
    if agenda:
        lines.append("**Timed agenda:**")
        for item in agenda:
            lines.append(
                f"- {item.get('time_range', '')} — {item.get('section_title', '')}: "
                f"{item.get('purpose', '')}"
            )
    return "\n".join(lines)


def _format_activities_section(activities: list, markdown: str | None) -> str:
    if not activities:
        return _missing_section_note("Training Activities", "Activity Generator")
    if markdown:
        return _strip_top_heading(markdown)
    lines = []
    for i, activity in enumerate(activities, 1):
        lines.append(
            f"### Activity {i}: {activity.get('activity_title', '')} "
            f"({activity.get('duration_minutes', '')} min)"
        )
        lines.append("")
        lines.append(f"**Learning objective:** {activity.get('learning_objective', '')}")
        lines.append(f"**Target roles:** {', '.join(activity.get('target_roles', []))}")
        takeaways = activity.get("key_takeaways", [])
        if takeaways:
            lines.append("**Key takeaways:**")
            for t in takeaways:
                lines.append(f"- {t}")
        lines.append("")
    return "\n".join(lines)


def _format_facilitator_guide_section(guide: dict, markdown: str | None) -> str:
    if not guide:
        return _missing_section_note("Facilitator Guide", "Facilitator Guide")
    if markdown:
        return _strip_top_heading(markdown)
    lines = [
        f"**Guide title:** {guide.get('guide_title', '')}",
        f"**Session purpose:** {guide.get('session_purpose', '')}",
        "",
    ]
    principles = guide.get("facilitator_principles", [])
    if principles:
        lines.append("**Facilitator principles:**")
        for p in principles:
            lines.append(f"- {p}")
    return "\n".join(lines)


def _format_staff_handout_section(handout: dict, markdown: str | None) -> str:
    if not handout:
        return _missing_section_note("Staff Handout", "Staff Handout")
    if markdown:
        return _strip_top_heading(markdown)
    lines = [
        f"**Title:** {handout.get('handout_title', '')}",
        f"**Purpose:** {handout.get('purpose', '')}",
        "",
    ]
    principles = handout.get("safe_use_principles", [])
    if principles:
        lines.append("**Safe-use principles:**")
        for p in principles:
            lines.append(f"- {p}")
    return "\n".join(lines)


def _format_knowledge_check_section(check: dict, markdown: str | None) -> str:
    if not check:
        return _missing_section_note("Knowledge Check", "Knowledge Check")
    if markdown:
        # Strip top heading and also strip the Answer Key section (it gets its own section)
        stripped = _strip_top_heading(markdown)
        # Remove the Answer Key sub-section and everything after it in the check section
        answer_key_marker = "## Answer Key"
        if answer_key_marker in stripped:
            stripped = stripped[:stripped.index(answer_key_marker)].rstrip()
        return stripped
    mcqs = check.get("multiple_choice_questions", [])
    reflections = check.get("reflection_questions", [])
    lines = [
        f"**{check.get('knowledge_check_title', 'Responsible AI Staff Knowledge Check')}**",
        "",
        f"**MCQs:** {len(mcqs)}  |  "
        f"**Scenario questions:** {len(check.get('scenario_questions', []))}  |  "
        f"**Reflection questions:** {len(reflections)}",
    ]
    return "\n".join(lines)


def _format_answer_key_section(check: dict) -> str:
    if not check:
        return "*No answer key is available yet.*"
    answer_key = check.get("answer_key")
    if not answer_key:
        return "*No answer key is available yet.*"
    lines = [
        f"*{answer_key.get('marking_note', '')}*",
        "",
        "### Multiple-Choice Answers",
        "",
    ]
    for answer in answer_key.get("multiple_choice_answers", []):
        lines.append(
            f"**{answer['question_id'].upper()}:** Correct answer: **{answer['correct_answer']}**"
        )
        lines.append(f"*{answer.get('explanation', '')}*")
        lines.append("")
    lines.append("### Scenario Answer Guidance")
    lines.append("")
    for guidance in answer_key.get("scenario_answer_guidance", []):
        lines.append(f"**{guidance['question_id'].upper()} — {guidance['topic'].title()}**")
        lines.append(f"*Model answer:* {guidance.get('model_answer', '')}")
        lines.append("Key points:")
        for point in guidance.get("expected_answer_points", []):
            lines.append(f"- {point}")
        lines.append("")
    lines.append("### Reflection Guidance")
    lines.append("")
    for guidance in answer_key.get("reflection_guidance", []):
        lines.append(f"**{guidance['question_id'].upper()} — {guidance['topic'].title()}**")
        for point in guidance.get("guidance_points", []):
            lines.append(f"- {point}")
        lines.append("")
    return "\n".join(lines)


def _strip_top_heading(markdown: str) -> str:
    """Remove the first `# Heading` line from a Markdown string."""
    lines = markdown.split("\n")
    # Find and remove the first h1 line
    for i, line in enumerate(lines):
        if line.startswith("# "):
            remaining = lines[i + 1:]
            # Skip blank lines immediately after the heading
            while remaining and not remaining[0].strip():
                remaining = remaining[1:]
            return "\n".join(remaining)
    return markdown


def generate_markdown_training_pack(
    pack_data: dict,
    include_sections: dict | None = None,
) -> str:
    """Return the full training pack as a Markdown string."""
    if include_sections is None:
        include_sections = {key: True for key in _ALL_SECTIONS}

    lines = []

    # Title
    lines.append("# Responsible AI Staff Training Pack")
    lines.append("")
    lines.append(
        f"**{pack_data.get('organisation_name', 'Unnamed organisation')}** · "
        f"Generated: {pack_data.get('generated_date', str(date.today()))}"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Cover page
    lines.append("## Cover Page")
    lines.append("")
    lines.append(generate_training_pack_cover_section(pack_data))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    lines.append(generate_training_pack_table_of_contents(include_sections))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Numbered section counter
    n = 1

    # Organisation Scenario Summary
    if include_sections.get("scenario", True):
        lines.append(_section_header(n, "Organisation Scenario Summary"))
        lines.append("")
        lines.append(_format_scenario_section(pack_data.get("scenario") or {}))
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Training Needs Assessment
    if include_sections.get("training_needs_assessment", True):
        lines.append(_section_header(n, "Training Needs Assessment"))
        lines.append("")
        lines.append(
            _format_needs_assessment_section(
                pack_data.get("training_needs_assessment"),
                pack_data.get("training_needs_markdown"),
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Workshop Plan
    if include_sections.get("workshop_plan", True):
        lines.append(_section_header(n, "Workshop Plan"))
        lines.append("")
        lines.append(
            _format_workshop_plan_section(
                pack_data.get("workshop_plan"),
                pack_data.get("workshop_plan_markdown"),
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Training Activities
    if include_sections.get("training_activities", True):
        lines.append(_section_header(n, "Training Activities"))
        lines.append("")
        lines.append(
            _format_activities_section(
                pack_data.get("training_activities"),
                pack_data.get("training_activities_markdown"),
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Facilitator Guide
    if include_sections.get("facilitator_guide", True):
        lines.append(_section_header(n, "Facilitator Guide"))
        lines.append("")
        lines.append(
            _format_facilitator_guide_section(
                pack_data.get("facilitator_guide"),
                pack_data.get("facilitator_guide_markdown"),
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Staff Handout
    if include_sections.get("staff_handout", True):
        lines.append(_section_header(n, "Staff Handout"))
        lines.append("")
        lines.append(
            _format_staff_handout_section(
                pack_data.get("staff_handout"),
                pack_data.get("staff_handout_markdown"),
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Knowledge Check
    if include_sections.get("knowledge_check", True):
        lines.append(_section_header(n, "Knowledge Check"))
        lines.append("")
        lines.append(
            _format_knowledge_check_section(
                pack_data.get("knowledge_check"),
                pack_data.get("knowledge_check_markdown"),
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Answer Key
    if include_sections.get("answer_key", True):
        lines.append(_section_header(n, "Answer Key"))
        lines.append("")
        lines.append(_format_answer_key_section(pack_data.get("knowledge_check")))
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Facilitator Review Checklist
    if include_sections.get("facilitator_review_checklist", True):
        lines.append(_section_header(n, "Facilitator Review Checklist"))
        lines.append("")
        lines.append("Before delivering this training pack, confirm:")
        lines.append("")
        for item in generate_facilitator_review_checklist():
            lines.append(f"- [ ] {item}")
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Responsible-Use Boundaries
    if include_sections.get("responsible_use_boundaries", True):
        lines.append(_section_header(n, "Responsible-Use Boundaries"))
        lines.append("")
        lines.append(generate_training_pack_responsible_use_section())
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Prototype Limitations
    if include_sections.get("prototype_limitations", True):
        lines.append(_section_header(n, "Prototype Limitations"))
        lines.append("")
        lines.append(generate_training_pack_limitations_section())
        lines.append("")
        lines.append("---")
        lines.append("")
        n += 1

    # Recommended Next Steps
    if include_sections.get("recommended_next_steps", True):
        lines.append(_section_header(n, "Recommended Next Steps"))
        lines.append("")
        for step in generate_training_pack_next_steps(pack_data):
            lines.append(f"- {step}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(
        "*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)


def summarise_training_pack(pack_data: dict) -> dict:
    """Return a compact summary dict for the training pack."""
    available = pack_data.get("source_outputs_available", {})
    activities = pack_data.get("training_activities") or []
    check = pack_data.get("knowledge_check") or {}
    return {
        "organisation_name": pack_data.get("organisation_name", ""),
        "generated_date": pack_data.get("generated_date", ""),
        "sections_available": sum(1 for v in available.values() if v),
        "sections_total": len(available),
        "activity_count": len(activities),
        "mcq_count": len(check.get("multiple_choice_questions", [])),
        "knowledge_check_included": bool(check),
        "answer_key_included": bool(check.get("answer_key")),
    }


def create_training_pack_filename(organisation_name: str) -> str:
    """Return a safe kebab-case filename for the training pack."""
    if not organisation_name:
        organisation_name = "organisation"
    slug = organisation_name.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return f"training-pack-{slug}.md"


# ── Backwards-compatible shims for Phase 1 tests ─────────────────────────────
# The test_training_pack.py file is replaced in Phase 8, but keep these
# so any external code that imported them does not crash.

def get_placeholder_message() -> str:
    return "Training pack export is implemented in Phase 8."


def assemble_training_pack(
    scenario: dict,
    needs: dict = None,
    workshop_plan: dict = None,
    activities: list = None,
    facilitator_guide: dict = None,
    staff_handout: dict = None,
    knowledge_check: dict = None,
) -> dict:
    session = {
        "training_scenario": scenario,
        "training_needs_assessment": needs,
        "workshop_plan": workshop_plan,
        "training_activities": activities,
        "facilitator_guide": facilitator_guide,
        "staff_handout": staff_handout,
        "knowledge_check": knowledge_check,
    }
    return build_training_pack_data_from_session_state(session)


def generate_pack_markdown(pack: dict) -> str:
    return generate_markdown_training_pack(pack)
