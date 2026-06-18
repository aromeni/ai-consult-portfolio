"""Workshop planner for the AI Staff Training and Workshop Generator.

Phase 3: generates a structured responsible AI staff workshop plan from a
synthetic organisation scenario and optional training needs assessment.
All generation is deterministic and template-based. No external AI API calls.
"""

import re


# ── Duration helpers ───────────────────────────────────────────────────────────

def normalise_duration_to_minutes(duration) -> int:
    """Convert a duration value to integer minutes.

    Handles:
    - int or float: returned directly as int
    - "90 minutes", "90 mins", "90min"
    - "1 hour", "1.5 hours", "2 hours"
    - "1 hour 30 minutes", "1h 30m"
    - Defaults to 90 if unparseable.
    """
    if duration is None:
        return 90
    if isinstance(duration, (int, float)):
        minutes = int(duration)
        return minutes if minutes > 0 else 90

    text = str(duration).strip().lower()

    # Pure digit
    if re.fullmatch(r"\d+", text):
        return int(text)

    # "90 minutes" / "90 mins" / "90min"
    m = re.search(r"(\d+)\s*(?:minutes?|mins?|min)", text)
    if m:
        minutes = int(m.group(1))
        h = re.search(r"(\d+)\s*(?:hours?|hrs?|h)\b", text)
        if h:
            minutes += int(h.group(1)) * 60
        return minutes if minutes > 0 else 90

    # "1 hour" / "1.5 hours"
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)\b", text)
    if m:
        minutes = int(float(m.group(1)) * 60)
        return minutes if minutes > 0 else 90

    return 90


# ── Utility helpers ────────────────────────────────────────────────────────────

def _fmt_time(start_minute: int, end_minute: int) -> str:
    """Return a HH:MM-HH:MM time range string from minute offsets."""
    def m2s(m):
        return f"{m // 60:02d}:{m % 60:02d}"
    return f"{m2s(start_minute)}-{m2s(end_minute)}"


def create_workshop_title(scenario: dict, assessment: dict = None) -> str:
    """Return a workshop title based on the scenario's training goal and sector."""
    goal = scenario.get("training_goal", "").lower()
    sector = scenario.get("sector", "").lower()
    org = scenario.get("organisation_name", "")

    if "lesson" in goal or "education" in sector or "training" in sector:
        return "Using AI Safely for Lesson Planning and Admin"
    if "health" in sector or "clinical" in sector:
        return "Responsible AI Use for Healthcare Staff"
    if "legal" in sector or "compliance" in sector:
        return "Responsible AI Use in a Regulated Professional Context"
    if "customer" in goal or "retail" in sector or "service" in sector:
        return "Responsible AI Use for Customer-Facing Staff"
    return f"Responsible AI Use at {org}" if org else "Responsible AI Staff Training Workshop"


def create_workshop_plan_filename(title: str) -> str:
    """Return a safe lowercase kebab-case filename from a workshop title."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return f"workshop-plan-{slug}.md"


# ── Static content libraries ───────────────────────────────────────────────────

def get_default_workshop_resources(delivery_mode: str = "In-person workshop") -> list:
    """Return a list of recommended resources for the given delivery mode."""
    mode = delivery_mode.lower() if delivery_mode else ""
    base = [
        "Printed or digital participant handout (one per staff member)",
        "Facilitator guide (trainer copy only)",
        "Printed or shared knowledge check / quiz sheet",
        "Flip chart or whiteboard for group activities",
        "Pens and sticky notes for prompt-sorting activity",
    ]
    if "online" in mode or "virtual" in mode:
        return [
            "Video conferencing platform (e.g. Teams, Zoom) with screen sharing",
            "Shared digital whiteboard (e.g. Miro, Jamboard) for activities",
            "Digital participant handout (shared link or PDF)",
            "Facilitator guide (trainer copy)",
            "Digital poll or quiz tool for knowledge check",
            "Breakout room capability for small group activities",
        ]
    if "hybrid" in mode:
        return base + [
            "Video conferencing platform for remote participants",
            "Camera and microphone setup for the room",
            "Shared digital workspace accessible to all participants",
        ]
    return base


def get_default_workshop_ground_rules() -> list:
    """Return a standard set of ground rules for a responsible AI workshop."""
    return [
        "Confidentiality: what is discussed in the room stays in the room.",
        "No judgement: there are no silly questions — everyone is learning.",
        "Phones and devices: please keep notifications off during activities.",
        "Participation: everyone's experience is valuable — please contribute.",
        "Honesty: if you are already using AI tools, that is fine — this session helps you use them more safely.",
        "Human review: we will practise checking AI outputs, not just trusting them.",
    ]


_RESPONSIBLE_USE_MESSAGES = [
    (
        "Do not enter learner names, identifiable learner data, safeguarding case details, "
        "confidential client records, staff HR data, personal data, or regulated information "
        "into AI tools."
    ),
    "AI outputs must be reviewed by a responsible human before use.",
    "AI should support low-risk drafting and planning, not replace professional judgement.",
    (
        "Safeguarding, disciplinary, assessment, legal, or compliance decisions "
        "must remain human-led."
    ),
    "Staff should use only approved tools and follow organisational policy.",
    "If an AI output seems wrong, harmful, or unexpected — stop, do not use it, and escalate.",
]


# ── Agenda generation ──────────────────────────────────────────────────────────

_AGENDA_BLOCKS = [
    # (weight, section_title, purpose, trainer_activity, participant_activity, key_message, materials)
    (
        0.10,
        "Welcome, Purpose, and Responsible-Use Boundaries",
        "Set the scene, establish ground rules, and introduce the core responsible-use message.",
        (
            "Welcome participants. Introduce yourself and the session purpose. "
            "Share the ground rules. Briefly explain what AI tools are and are not."
        ),
        "Listen, ask questions, share current AI use experience (show of hands).",
        "AI tools can be useful — and they carry real risks for learner data, safeguarding, and accuracy. Today we learn to use them responsibly.",
        ["Facilitator guide", "Ground rules slide or flip chart"],
    ),
    (
        0.17,
        "AI Use Cases: Safe, Low-Risk, and Prohibited",
        "Help staff distinguish safe AI tasks from risky or prohibited ones.",
        (
            "Present 3–4 example tasks: lesson plan drafting, email drafting, "
            "writing a safeguarding referral, processing learner records. "
            "Ask which are safe, low-risk, or prohibited."
        ),
        "In pairs or small groups: sort example tasks into safe / low-risk / prohibited.",
        "Not all AI tasks are equal. Draft writing is low risk. Personal data and safeguarding are always prohibited.",
        ["Task sorting cards or slide", "Participant handout"],
    ),
    (
        0.17,
        "Learner Data, Safeguarding, and Confidential Information Boundaries",
        "Establish firm, clear boundaries for data protection and safeguarding.",
        (
            "Walk through the 'never enter' list: learner names, records, "
            "safeguarding disclosures, client records, staff HR data. "
            "Explain why each carries specific data protection and safeguarding risk."
        ),
        "Discuss: what types of information are you currently tempted to use AI with? Which should you stop?",
        "Some information must never go into an AI tool. These are absolute rules — not guidelines.",
        ["Never-enter list in handout", "Escalation contacts card"],
    ),
    (
        0.17,
        "Safe Prompting and Anonymisation Practice",
        "Build practical safe prompting skills through active practice.",
        (
            "Demonstrate a risky prompt (with learner name) and a safe version (anonymised). "
            "Explain data minimisation. Facilitate the rewrite exercise."
        ),
        "Individually: rewrite two provided risky prompts into safer, anonymised versions. Share with the group.",
        "You can usually achieve the same result with much less information. Less data in = less risk.",
        ["Prompt rewrite worksheet", "Before/after prompt examples in handout"],
    ),
    (
        0.17,
        "Human Review, Hallucination, Bias, and Accountability",
        "Teach staff to critically review AI outputs and understand their accountability.",
        (
            "Show an example AI output containing a hallucinated fact. "
            "Demonstrate the 3-step review habit: check, source, confirm. "
            "Discuss accountability: who is responsible when an AI output causes a problem?"
        ),
        "Review a sample AI-generated lesson plan or email. Identify at least one thing to verify. Discuss.",
        "You are always accountable for what you share or act on — AI does not remove your professional responsibility.",
        ["Sample AI output for review activity", "Review checklist in handout"],
    ),
    (
        0.17,
        "Escalation Routes and Team Workflow Rules",
        "Ensure all staff know what to do when something goes wrong with AI.",
        (
            "Present the escalation route for three scenarios: a data concern, "
            "a safeguarding concern, and a general AI output concern. "
            "Confirm the team's agreed workflow rules for AI use."
        ),
        "In pairs: role-play one escalation scenario. What would you say? Who would you contact?",
        "Knowing when to stop and who to contact is as important as knowing how to use AI safely.",
        ["Escalation route card or slide", "Contact list in handout"],
    ),
    (
        0.05,
        "Commitments, Next Steps, and Questions",
        "Close the session with individual commitments and confirmed next steps.",
        (
            "Ask each participant to name one thing they will do differently. "
            "Confirm the approved tools list and who to contact with future questions. "
            "Distribute the take-away handout."
        ),
        "Write or share one commitment: 'After today I will...'",
        "Responsible AI use is a team habit, not a one-day event. Today is the start.",
        ["Commitment card or slip", "Take-away handout", "Next steps summary"],
    ),
]


def generate_timed_agenda(
    scenario: dict,
    assessment: dict = None,
    duration_minutes: int = 90,
) -> list:
    """Return a list of timed agenda item dicts scaled to duration_minutes.

    The 7 standard blocks are weighted proportionally to the total duration.
    Each item includes time_range, section_title, purpose, trainer_activity,
    participant_activity, key_message, and materials.
    """
    if duration_minutes <= 0:
        duration_minutes = 90

    total_weight = sum(b[0] for b in _AGENDA_BLOCKS)
    cursor = 0
    items = []

    for i, (weight, title, purpose, trainer_act, part_act, key_msg, mats) in enumerate(_AGENDA_BLOCKS):
        raw_mins = (weight / total_weight) * duration_minutes
        block_mins = max(5, round(raw_mins / 5) * 5)

        # Last block absorbs any leftover
        if i == len(_AGENDA_BLOCKS) - 1:
            block_mins = duration_minutes - cursor

        block_mins = max(5, block_mins)
        items.append({
            "time_range": _fmt_time(cursor, cursor + block_mins),
            "section_title": title,
            "purpose": purpose,
            "trainer_activity": trainer_act,
            "participant_activity": part_act,
            "key_message": key_msg,
            "materials": list(mats),
        })
        cursor += block_mins

    return items


# ── Learning outcomes ──────────────────────────────────────────────────────────

_DEFAULT_OUTCOMES = [
    "Explain what information staff must not enter into AI tools.",
    "Identify safe and unsafe AI use cases for lesson planning and admin support.",
    "Rewrite risky prompts into safer synthetic or anonymised prompts.",
    "Apply human review to AI-generated lesson plans, emails, and reports.",
    "Escalate safeguarding, data protection, or accuracy concerns to the appropriate human owner.",
]


def generate_learning_outcome_section(scenario: dict, assessment: dict = None) -> list:
    """Return a list of learning outcome strings for the workshop.

    Uses outcomes from the training needs assessment if available,
    otherwise falls back to role-sensitive defaults.
    """
    if assessment:
        outcomes = assessment.get("recommended_learning_outcomes", [])
        if outcomes:
            return outcomes

    # Role-sensitive defaults
    roles = [r.lower() for r in scenario.get("staff_roles", [])]
    outcomes = list(_DEFAULT_OUTCOMES)

    if "assessors" in roles:
        outcomes.append(
            "Describe why AI must not be used to make or support assessment decisions."
        )
    if "quality lead" in roles or "quality" in roles:
        outcomes.append(
            "Apply a review process for AI-assisted quality documents and confirm "
            "disclosure requirements."
        )
    if "team leaders" in roles or "team leader" in roles:
        outcomes.append(
            "Support team members to use AI safely and know the escalation route "
            "for AI-related incidents."
        )

    return outcomes[:8]


# ── Trainer notes ──────────────────────────────────────────────────────────────

def generate_trainer_notes(scenario: dict, assessment: dict = None) -> list:
    """Return a list of practical trainer notes for the workshop."""
    org = scenario.get("organisation_name", "the organisation")
    roles = scenario.get("staff_roles", [])
    concerns = scenario.get("main_concerns", [])
    staff_count = scenario.get("staff_count", 0)

    notes = [
        f"This workshop is tailored to {org}. Read the scenario summary before the session.",
        (
            f"Expected audience: {', '.join(roles) if roles else 'general staff'} "
            f"({staff_count} staff). Allow participation from all roles."
        ),
        "Start with the responsible-use message clearly — it sets the tone for everything that follows.",
        "The prompt-sorting and rewrite activities generate the most discussion. Allow extra time if needed.",
        "Do not present AI as either all-good or all-bad — frame it as a powerful tool that requires discipline.",
        "Participants may be nervous about admitting current AI use. Create psychological safety early.",
        "If safeguarding is mentioned in the context of AI tools — stop and redirect to the established procedure.",
        "Close with individual commitments — this increases follow-through after the session.",
    ]

    if concerns:
        flagged = concerns[:3]
        notes.append(
            f"Staff have flagged concerns about: {', '.join(flagged)}. "
            "Address these explicitly — don't skip over them."
        )

    if assessment:
        high = [t["topic"] for t in assessment.get("topic_assessments", [])
                if t.get("priority_level") == "high"]
        if high:
            notes.append(
                f"High-priority topics from the Training Needs Assessment: "
                f"{', '.join(high[:5])}. Ensure these receive sufficient time."
            )

    return notes


# ── Discussion prompts ─────────────────────────────────────────────────────────

def generate_discussion_prompts(scenario: dict, assessment: dict = None) -> list:
    """Return a list of facilitated discussion prompts for the workshop."""
    sector = scenario.get("sector", "").lower()

    prompts = [
        "What AI tools are you currently using — even informally? What do you use them for?",
        "Can you think of a task where using AI might accidentally involve personal or sensitive information?",
        "If you received an AI-generated email draft that contained a factual error, what would you do?",
        "What would you do if a learner or colleague disclosed something sensitive in a conversation and you had been using an AI tool?",
        "How would you check whether an AI-generated piece of information is accurate before acting on it?",
        "Who in this organisation would you contact if an AI tool produced something harmful, unexpected, or concerning?",
        "What is one task you currently do manually that AI could genuinely help with — safely?",
        "What is one task you should never use AI for in your role?",
    ]

    if "education" in sector or "training" in sector:
        prompts.insert(2,
            "Can you describe a lesson planning task where AI could help — "
            "and one where it would be risky or inappropriate?"
        )

    return prompts[:8]


# ── Follow-up actions ──────────────────────────────────────────────────────────

def generate_follow_up_actions(scenario: dict, assessment: dict = None) -> list:
    """Return a list of post-workshop follow-up actions for the organisation."""
    org = scenario.get("organisation_name", "the organisation")
    return [
        f"Share the take-away handout with all staff at {org} — including those not present.",
        "Circulate the approved AI tools list and confirm who to contact with questions.",
        "Confirm escalation contacts for data concerns, safeguarding concerns, and general AI incidents.",
        "Set a date for a 30-day check-in: what has changed? What questions have emerged?",
        "Review the AI acceptable-use policy in light of today's discussion and update if needed.",
        "Consider a short follow-up quiz or knowledge check 2–4 weeks after the session.",
        "Capture any staff-identified gaps or use cases for future training sessions.",
        "Record staff attendance and commitments for training records.",
    ]


# ── Main plan generator ────────────────────────────────────────────────────────

def generate_workshop_plan(
    scenario: dict,
    assessment: dict = None,
    duration_minutes: int = None,
    delivery_mode: str = None,
) -> dict:
    """Generate a complete workshop plan dict from a synthetic scenario.

    duration_minutes overrides scenario["training_duration"] if supplied.
    delivery_mode overrides scenario["delivery_mode"] if supplied.
    """
    org = scenario.get("organisation_name", "Unnamed organisation")
    training_goal = scenario.get("training_goal", "Help staff use AI responsibly.")
    staff_roles = scenario.get("staff_roles", [])

    # Resolve duration
    if duration_minutes is None or duration_minutes <= 0:
        raw_duration = scenario.get("training_duration", "90 minutes")
        duration_minutes = normalise_duration_to_minutes(raw_duration)

    # Resolve delivery mode
    if not delivery_mode:
        delivery_mode = scenario.get("delivery_mode", "In-person workshop")

    title = create_workshop_title(scenario, assessment)
    learning_outcomes = generate_learning_outcome_section(scenario, assessment)
    agenda = generate_timed_agenda(scenario, assessment, duration_minutes)
    resources = get_default_workshop_resources(delivery_mode)
    ground_rules = get_default_workshop_ground_rules()
    trainer_notes = generate_trainer_notes(scenario, assessment)
    discussion_prompts = generate_discussion_prompts(scenario, assessment)
    follow_up = generate_follow_up_actions(scenario, assessment)

    expected_outputs = [
        "All staff understand the absolute data and safeguarding boundaries for AI use.",
        "All staff can write a data-minimised prompt for a common task.",
        "All staff know who to contact when an AI tool produces something concerning.",
        "Each staff member has named one personal commitment to change their AI practice.",
        "The facilitator has a record of attendance and staff commitments.",
    ]

    return {
        "workshop_title": title,
        "organisation_name": org,
        "audience": staff_roles if staff_roles else ["All staff"],
        "duration_minutes": duration_minutes,
        "delivery_mode": delivery_mode,
        "training_goal": training_goal,
        "learning_outcomes": learning_outcomes,
        "agenda": agenda,
        "resources_needed": resources,
        "ground_rules": ground_rules,
        "trainer_notes": trainer_notes,
        "discussion_prompts": discussion_prompts,
        "responsible_use_messages": list(_RESPONSIBLE_USE_MESSAGES),
        "expected_outputs": expected_outputs,
        "follow_up_actions": follow_up,
        "prototype_note": (
            "This workshop plan is generated from a synthetic organisation scenario only. "
            "It must not be used with real learner data, safeguarding case details, "
            "confidential client records, staff HR data, personal data, or regulated "
            "information without appropriate governance, approvals, and responsible owners. "
            "This prototype does not provide legal, safeguarding, HR, compliance, "
            "medical, financial, academic-integrity, or professional advice."
        ),
    }


# ── Summary ────────────────────────────────────────────────────────────────────

def summarise_workshop_plan(workshop_plan: dict) -> dict:
    """Return a compact summary dict for display in metric cards."""
    return {
        "workshop_title": workshop_plan.get("workshop_title", ""),
        "organisation_name": workshop_plan.get("organisation_name", ""),
        "duration_minutes": workshop_plan.get("duration_minutes", 0),
        "delivery_mode": workshop_plan.get("delivery_mode", ""),
        "audience_count": len(workshop_plan.get("audience", [])),
        "agenda_section_count": len(workshop_plan.get("agenda", [])),
        "learning_outcome_count": len(workshop_plan.get("learning_outcomes", [])),
        "follow_up_action_count": len(workshop_plan.get("follow_up_actions", [])),
    }


# ── Markdown export ────────────────────────────────────────────────────────────

def format_workshop_plan_as_markdown(workshop_plan: dict) -> str:
    """Return a Markdown-formatted workshop plan."""
    lines = []
    org = workshop_plan.get("organisation_name", "Unknown organisation")
    title = workshop_plan.get("workshop_title", "AI Staff Training Workshop")
    duration = workshop_plan.get("duration_minutes", 90)
    mode = workshop_plan.get("delivery_mode", "In-person workshop")

    lines.append("# AI Staff Training Workshop Plan")
    lines.append("")

    lines.append("## Organisation")
    lines.append(f"- **Organisation:** {org}")
    audience = workshop_plan.get("audience", [])
    if audience:
        lines.append(f"- **Audience:** {', '.join(audience)}")
    lines.append("")

    lines.append("## Workshop Title")
    lines.append(f"**{title}**")
    lines.append("")

    lines.append("## Audience")
    for role in audience:
        lines.append(f"- {role}")
    lines.append("")

    lines.append("## Duration and Delivery Mode")
    lines.append(f"- **Duration:** {duration} minutes")
    lines.append(f"- **Delivery mode:** {mode}")
    lines.append("")

    lines.append("## Training Goal")
    lines.append(workshop_plan.get("training_goal", ""))
    lines.append("")

    lines.append("## Learning Outcomes")
    lines.append("")
    lines.append("By the end of this session, staff will be able to:")
    lines.append("")
    for outcome in workshop_plan.get("learning_outcomes", []):
        lines.append(f"- {outcome}")
    lines.append("")

    lines.append("## Timed Agenda")
    lines.append("")
    lines.append("| Time | Section | Purpose |")
    lines.append("|---|---|---|")
    for item in workshop_plan.get("agenda", []):
        purpose = item.get("purpose", "").replace("\n", " ")[:100]
        lines.append(
            f"| {item.get('time_range', '')} "
            f"| {item.get('section_title', '')} "
            f"| {purpose} |"
        )
    lines.append("")

    lines.append("### Agenda Detail")
    lines.append("")
    for item in workshop_plan.get("agenda", []):
        lines.append(f"#### {item.get('time_range', '')} — {item.get('section_title', '')}")
        lines.append("")
        lines.append(f"**Purpose:** {item.get('purpose', '')}")
        lines.append("")
        lines.append(f"**Trainer activity:** {item.get('trainer_activity', '')}")
        lines.append("")
        lines.append(f"**Participant activity:** {item.get('participant_activity', '')}")
        lines.append("")
        lines.append(f"**Key message:** *{item.get('key_message', '')}*")
        lines.append("")
        mats = item.get("materials", [])
        if mats:
            lines.append("**Materials:**")
            for m in mats:
                lines.append(f"- {m}")
        lines.append("")

    lines.append("## Resources Needed")
    for resource in workshop_plan.get("resources_needed", []):
        lines.append(f"- {resource}")
    lines.append("")

    lines.append("## Ground Rules")
    for rule in workshop_plan.get("ground_rules", []):
        lines.append(f"- {rule}")
    lines.append("")

    lines.append("## Trainer Notes")
    for note in workshop_plan.get("trainer_notes", []):
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## Discussion Prompts")
    for i, prompt in enumerate(workshop_plan.get("discussion_prompts", []), 1):
        lines.append(f"{i}. {prompt}")
    lines.append("")

    lines.append("## Responsible Use Messages")
    lines.append("")
    lines.append(
        "These messages must be shared clearly at the start and end of the session:"
    )
    lines.append("")
    for msg in workshop_plan.get("responsible_use_messages", []):
        lines.append(f"- {msg}")
    lines.append("")

    lines.append("## Expected Outputs")
    for output in workshop_plan.get("expected_outputs", []):
        lines.append(f"- {output}")
    lines.append("")

    lines.append("## Follow-Up Actions")
    for action in workshop_plan.get("follow_up_actions", []):
        lines.append(f"- {action}")
    lines.append("")

    lines.append("## Prototype and Responsible-Use Boundaries")
    lines.append("")
    lines.append(workshop_plan.get("prototype_note", ""))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*Workshop Plan · {title} · {org} · "
        "AI Staff Training and Workshop Generator · Build 4*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)
