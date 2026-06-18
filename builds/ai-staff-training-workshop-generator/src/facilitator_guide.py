"""Facilitator guide generator for the AI Staff Training and Workshop Generator.

Phase 5: generates trainer-facing delivery notes, scripts, activity guidance,
misconceptions, debrief notes, and risk warnings from a synthetic organisation
scenario. All content is deterministic and template-based — no external AI API calls.
"""

import re

# ── Responsible-use note ────────────────────────────────────────────────────────

_PROTOTYPE_NOTE = (
    "This facilitator guide is generated from a synthetic organisation scenario only. "
    "It must not be used with real learner data, safeguarding case details, confidential "
    "client records, staff HR data, personal data, or regulated information without "
    "appropriate governance, approvals, and responsible owners. "
    "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
    "financial, academic-integrity, or professional advice."
)

_RESPONSIBLE_USE_MESSAGES = [
    "AI supports drafting and thinking — it does not make final decisions.",
    "Safeguarding, data protection, compliance, and HR decisions must always be human-led.",
    "Use only organisation-approved AI tools for work tasks.",
    "Remove all identifying details before using AI tools.",
    "Human review is required before sharing any AI-generated output.",
    "When in doubt, escalate to the appropriate human owner — do not ask AI.",
]

# ── Internal helpers ────────────────────────────────────────────────────────────

def _get_org(scenario: dict) -> str:
    return scenario.get("organisation_name") or "Unnamed organisation"


def _get_sector(scenario: dict) -> str:
    return scenario.get("sector") or "education and training"


def _get_roles(scenario: dict) -> list:
    roles = scenario.get("staff_roles") or []
    return roles if roles else ["staff"]


def _get_duration(scenario: dict, workshop_plan: dict = None) -> int:
    if workshop_plan and workshop_plan.get("duration_minutes"):
        return int(workshop_plan["duration_minutes"])
    raw = scenario.get("training_duration", "90 minutes")
    if isinstance(raw, int):
        return raw
    match = re.search(r"(\d+)", str(raw))
    return int(match.group(1)) if match else 90


def _get_delivery_mode(scenario: dict, workshop_plan: dict = None) -> str:
    if workshop_plan and workshop_plan.get("delivery_mode"):
        return workshop_plan["delivery_mode"]
    return scenario.get("delivery_mode") or "In-person workshop"


def _get_high_priority_topics(assessment: dict = None) -> list:
    if not assessment:
        return []
    return [
        t["title"]
        for t in assessment.get("topic_assessments", [])
        if t.get("priority_level") == "high"
    ]


# ── Principles and checklist ────────────────────────────────────────────────────

def get_default_facilitator_principles() -> list:
    """Return the core principles for responsible AI workshop facilitation."""
    return [
        "Keep the session practical and scenario-based.",
        "Use synthetic examples only — do not ask participants to share real cases.",
        "Do not ask participants to share real learner, safeguarding, HR, client, personal, or regulated information.",
        "Reinforce that AI supports drafting and thinking, not final decisions.",
        "Keep safeguarding, disciplinary, assessment, compliance, and data-protection decisions human-led.",
        "Encourage staff to ask for help when unsure — escalation is a strength, not a failure.",
        "Focus on safe everyday behaviour rather than abstract AI theory.",
        "Acknowledge that policies may still be developing — the session is about safe practice now.",
    ]


def get_facilitator_preparation_checklist() -> list:
    """Return a preparation checklist for the workshop facilitator."""
    return [
        "Confirm the workshop uses synthetic examples only — no real learner, safeguarding, or HR data.",
        "Confirm the organisation's approved AI tools and current policy position.",
        "Confirm who owns safeguarding, data protection, quality, and escalation decisions in this organisation.",
        "Prepare the workshop plan, agenda, and any printed materials.",
        "Prepare the activity cards if using printed sorting or scenario activities.",
        "Prepare the staff handout if available.",
        "Test any technology or AI tools you plan to demonstrate.",
        "Avoid displaying real client, learner, HR, or safeguarding information on screen or in materials.",
        "Prepare a parking-lot process for questions that need manager, DPO, safeguarding lead, or policy-owner review.",
        "Know your own escalation contacts: DPO, safeguarding lead, line manager.",
        "Review the session plan and timing — know which sections can be shortened if running over.",
    ]


# ── Scripts ─────────────────────────────────────────────────────────────────────

def generate_opening_script(
    scenario: dict,
    workshop_plan: dict = None,
) -> str:
    """Return a short opening script tailored to the scenario."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    goal = scenario.get("training_goal") or "use AI tools safely and responsibly"
    duration = _get_duration(scenario, workshop_plan)

    return (
        f"Welcome, everyone. Today's {duration}-minute session is about using AI safely and "
        f"practically in {sector}. My name is [facilitator name] and I'm here to work through "
        f"this with you — not to lecture you on technology.\n\n"
        f"We are focusing on {goal.lower().rstrip('.')}. "
        f"We will look at where AI can help with everyday tasks, where it must not be used, "
        f"and how human review and escalation should work in practice.\n\n"
        f"A few ground rules for today:\n"
        f"- We are using synthetic, fictional examples only. "
        f"Please do not share real learner names, safeguarding concerns, client details, "
        f"HR information, or personal data during the session.\n"
        f"- There are no wrong questions. If something is unclear or feels relevant to "
        f"your work, please raise it — we have a parking lot for anything that needs "
        f"a follow-up from your manager or policy lead.\n"
        f"- This session is not about banning AI. It is about using it well.\n\n"
        f"Let's start with a quick question: who here has used an AI tool — "
        f"like ChatGPT — for a work task in the last month? [pause for show of hands]"
    )


def generate_closing_script(
    scenario: dict,
    workshop_plan: dict = None,
) -> str:
    """Return a short closing script tailored to the scenario."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)

    return (
        f"Thank you all for your engagement today. Let's recap the key points:\n\n"
        f"- AI tools can help with low-risk drafting, summarising, and planning tasks "
        f"when used with the right safeguards.\n"
        f"- Some tasks must never go to AI: safeguarding decisions, learner data processing "
        f"without anonymisation, compliance judgements, and HR decisions.\n"
        f"- Always use your organisation's approved tools, anonymise before prompting, "
        f"and review all AI output before use.\n"
        f"- When in doubt, escalate to your line manager, DPO, or safeguarding lead. "
        f"That is the right action — not a last resort.\n\n"
        f"You should each have the workshop materials to take away. "
        f"[If available: the staff handout covers the key dos and don'ts for everyday use.]\n\n"
        f"Any final questions before we close? [pause]\n\n"
        f"Thank you. Please complete the follow-up actions we discussed, and do not "
        f"hesitate to reach out if anything comes up. "
        f"The parking-lot items will be followed up by [responsible person] by [date]."
    )


# ── Section delivery notes ───────────────────────────────────────────────────────

_SECTION_TEMPLATES = [
    {
        "section_title": "Welcome and Responsible-Use Boundaries",
        "facilitator_goal": "Set the tone: practical, safe, and human-led. Establish the boundary rules before any AI discussion.",
        "what_to_say": (
            "Open with the ground rules: synthetic examples only, no real data, "
            "no wrong questions, and a parking lot for follow-ups. "
            "Acknowledge that AI use may already be happening informally — this session is about doing it safely."
        ),
        "what_to_ask": [
            "Who has used an AI tool for a work task in the last month?",
            "What was the task? [if comfortable sharing a synthetic example]",
        ],
        "expected_responses": [
            "Lesson planning, email drafting, report writing.",
            "Looking things up or summarising documents.",
        ],
        "watch_out_for": [
            "Participants mentioning real learner names or case details — redirect immediately to synthetic examples.",
            "Defensive reactions from staff who feel they are being told off — emphasise the session is supportive, not punitive.",
        ],
        "transition_note": "Move into AI use cases once the ground rules feel settled.",
    },
    {
        "section_title": "Where AI Helps: Use Cases for This Organisation",
        "facilitator_goal": "Ground the session in realistic, low-risk everyday tasks — make AI feel accessible, not threatening.",
        "what_to_say": (
            "Walk through examples of safe AI use: drafting lesson outlines, "
            "summarising anonymised policy documents, generating generic communication templates. "
            "Emphasise that these tasks are synthetic and low-risk."
        ),
        "what_to_ask": [
            "Can you think of a low-risk task in your role where AI might save you time?",
            "What would make you confident enough to try it?",
        ],
        "expected_responses": [
            "Writing first drafts of emails or letters.",
            "Creating lesson plan templates.",
            "Summarising meeting notes.",
        ],
        "watch_out_for": [
            "Participants suggesting tasks that would involve personal data or case-specific content — explore the boundary.",
            "Over-enthusiasm about AI replacing existing processes without governance review.",
        ],
        "transition_note": "Use this section to set up the data boundaries section naturally — 'So now we know what AI can help with, let's look at the line it must not cross.'",
    },
    {
        "section_title": "Data and Safeguarding Boundaries",
        "facilitator_goal": "Make the boundary between safe and prohibited use concrete and memorable.",
        "what_to_say": (
            "The core rule: personal data, safeguarding case information, HR data, and "
            "confidential client records must never go into AI tools. "
            "Introduce the template approach: use AI to generate a generic template, "
            "then fill in the specific details manually."
        ),
        "what_to_ask": [
            "What kind of information do you handle daily that could identify a specific learner or colleague?",
            "If you wanted to use AI to help draft a support letter, what would you need to remove first?",
        ],
        "expected_responses": [
            "Names, IDs, attendance records, ILP details.",
            "Safeguarding disclosures, personal circumstances.",
        ],
        "watch_out_for": [
            "Participants assuming 'removing the name' is always enough — explore aggregation and context risks.",
            "Confusion between organisational approved tools and personal AI accounts.",
        ],
        "transition_note": "Move into safe prompting to show what good practice looks like in practice.",
    },
    {
        "section_title": "Safe Prompting Practice",
        "facilitator_goal": "Give staff a practical, repeatable technique for safe prompt writing.",
        "what_to_say": (
            "Walk through the safe prompting checklist: "
            "remove names and IDs, generalise specific details, "
            "add explicit instructions to exclude personal information, "
            "and always review the output before use."
        ),
        "what_to_ask": [
            "Look at this prompt: [show a risky example from the activity cards]. What would you change?",
            "What is the safest way to phrase a prompt when you are not sure?",
        ],
        "expected_responses": [
            "Replace the name with 'a learner' or 'a staff member'.",
            "Add 'Do not include names or personal details' to the prompt.",
        ],
        "watch_out_for": [
            "Participants skipping the output review step — emphasise AI output is always a draft.",
            "Assumptions that a well-worded prompt means the output will be accurate.",
        ],
        "transition_note": "Lead into human review and hallucination — 'Even a well-structured prompt does not guarantee accurate output.'",
    },
    {
        "section_title": "Human Review, Hallucination, and Bias",
        "facilitator_goal": "Establish that AI output always requires human review — especially in regulated or high-stakes contexts.",
        "what_to_say": (
            "AI can generate confident-sounding output that is factually wrong, biased, or invented. "
            "Show a hallucination example and a bias example. "
            "Introduce the human review checklist: facts, personal data, safeguarding content, "
            "legal or compliance claims, audience appropriateness, bias."
        ),
        "what_to_ask": [
            "What would happen if this AI-generated compliance statement went out without a review?",
            "What types of bias might appear in AI output about learners or staff?",
        ],
        "expected_responses": [
            "Incorrect regulatory information could create a compliance risk.",
            "Assumptions based on age, ethnicity, disability, or language background.",
        ],
        "watch_out_for": [
            "Participants dismissing hallucination as rare — use the activity cards to show it happens in ordinary outputs.",
            "Over-reaction that leads to 'we should never use AI' — reframe as 'review before use'.",
        ],
        "transition_note": "Move into escalation routes — 'Now we know when to review — let's cover when to escalate.'",
    },
    {
        "section_title": "Escalation Routes and Closing Commitments",
        "facilitator_goal": "Ensure every participant leaves knowing who to contact when they are unsure.",
        "what_to_say": (
            "Confirm the escalation contacts: data protection officer, safeguarding lead, "
            "line manager, quality lead. "
            "Reinforce: escalating is the right action, not a failure. "
            "Close with three personal commitments staff can make today."
        ),
        "what_to_ask": [
            "Who is your first point of contact if you discover you have entered personal data into an AI tool?",
            "What is one change you will make to how you use AI tools after today's session?",
        ],
        "expected_responses": [
            "Contact the DPO or line manager immediately.",
            "Always anonymise before prompting; always review the output.",
        ],
        "watch_out_for": [
            "Participants not knowing their safeguarding lead or DPO — note it in the parking lot for follow-up.",
            "Vague commitments — encourage specific, behavioural commitments.",
        ],
        "transition_note": "Close the session with the closing script.",
    },
]


def generate_section_delivery_notes(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> list:
    """Return section-by-section delivery notes tailored to the scenario."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    high_topics = _get_high_priority_topics(assessment)

    notes = []
    for template in _SECTION_TEMPLATES:
        note = dict(template)
        note["section_title"] = note["section_title"]
        note["suggested_timing"] = "See workshop plan for timed agenda."
        if workshop_plan and workshop_plan.get("agenda"):
            for item in workshop_plan["agenda"]:
                if item.get("section_title", "").lower() in note["section_title"].lower() or \
                   note["section_title"].lower() in item.get("section_title", "").lower():
                    note["suggested_timing"] = item.get("time_range", note["suggested_timing"])
                    break
        notes.append(note)

    return notes


# ── Activity facilitation notes ──────────────────────────────────────────────────

def generate_activity_facilitation_notes(
    activities: list = None,
) -> list:
    """Return facilitation notes for each activity, or generic notes if no activities provided."""
    if not activities:
        return [
            {
                "activity_title": "Safe vs Unsafe Prompt Sorting",
                "duration_minutes": 10,
                "facilitator_goal": "Help staff distinguish safe, risky, and prohibited prompts through hands-on sorting.",
                "setup_instructions": [
                    "Distribute prompt cards A–F.",
                    "Explain the three categories: SAFE, RISKY, PROHIBITED.",
                ],
                "how_to_run": [
                    "Give groups 5 minutes to sort and discuss.",
                    "Reveal classifications one by one, starting with A and B (safe).",
                    "Spend the most time on E and F (prohibited) — these prompt the most discussion.",
                ],
                "expected_answers": [
                    "A — SAFE, B — SAFE, C — RISKY, D — RISKY, E — PROHIBITED, F — PROHIBITED.",
                ],
                "debrief_questions": [
                    "Which card surprised you most?",
                    "What is the difference between risky and prohibited?",
                ],
                "key_takeaways": [
                    "Risky prompts can often be made safe. Prohibited ones cannot.",
                    "Safeguarding and HR decisions must never go to AI.",
                ],
                "risk_warnings": [
                    "Do not use real prompts containing learner or staff names during this activity.",
                ],
            }
        ]

    notes = []
    for activity in activities:
        note = {
            "activity_title": activity.get("activity_title", "Activity"),
            "duration_minutes": activity.get("duration_minutes", 10),
            "facilitator_goal": activity.get("learning_objective", ""),
            "setup_instructions": activity.get("materials_needed", []),
            "how_to_run": activity.get("instructions_for_trainer", []),
            "expected_answers": activity.get("expected_answers", []),
            "debrief_questions": activity.get("debrief_questions", []),
            "key_takeaways": activity.get("key_takeaways", []),
            "risk_warnings": activity.get("risk_warnings", []),
        }
        notes.append(note)

    return notes


# ── Common misconceptions ────────────────────────────────────────────────────────

def generate_common_misconceptions(
    scenario: dict,
    assessment: dict = None,
) -> list:
    """Return common AI misconceptions with facilitator responses."""
    sector = _get_sector(scenario)

    return [
        {
            "misconception": "If AI sounds confident, it must be correct.",
            "why_it_is_risky": (
                "AI generates plausible-sounding text regardless of accuracy. "
                "Confident language is a feature of the output style, not an indicator of truth."
            ),
            "facilitator_response": (
                "Show the hallucination activity cards. Point to the invented 40% statistic "
                "and unverified policy reference. Emphasise: always verify facts, citations, "
                "and regulatory claims before using AI output."
            ),
        },
        {
            "misconception": "Removing a name is always enough to anonymise a case.",
            "why_it_is_risky": (
                "Combination of role, subject matter, and context can still identify an individual. "
                "For example: 'the only male tutors-only learner with anxiety who joined in September' "
                "could be identifiable even without a name."
            ),
            "facilitator_response": (
                "Use the learner data boundary activity. Explain that genuine anonymisation "
                "removes or generalises all identifying context — not just the name."
            ),
        },
        {
            "misconception": "AI can decide safeguarding actions.",
            "why_it_is_risky": (
                "Safeguarding decisions carry legal accountability that AI cannot hold. "
                "Using AI for safeguarding decisions could result in harm, liability, "
                "and regulatory breach."
            ),
            "facilitator_response": (
                "Use the safeguarding escalation cards. Confirm the DSL name and escalation route. "
                "Reinforce: there are no exceptions to the rule that safeguarding must be human-led."
            ),
        },
        {
            "misconception": f"AI-generated {sector} materials do not need human review.",
            "why_it_is_risky": (
                "AI-generated lesson plans, policies, assessments, and communications "
                "can contain incorrect information, biased assumptions, or unsuitable content. "
                "They always require professional review before use."
            ),
            "facilitator_response": (
                "Walk through the human review checklist. Ask: what would happen if this "
                "AI-generated policy statement was shared without review?"
            ),
        },
        {
            "misconception": "Using a personal AI account is the same as using an approved organisational tool.",
            "why_it_is_risky": (
                "Personal AI accounts are not covered by organisational data processing agreements. "
                "Content entered may be used for AI training. This could breach UK GDPR "
                "and organisational policy."
            ),
            "facilitator_response": (
                "Use the approved tools decision activity. Confirm which tools are approved "
                "and explain why unapproved tools are a data-handling risk, not just a policy technicality."
            ),
        },
        {
            "misconception": "AI can replace professional judgement.",
            "why_it_is_risky": (
                "Professional judgement includes contextual knowledge, ethical accountability, "
                "relationship awareness, and regulatory responsibility that AI cannot replicate."
            ),
            "facilitator_response": (
                "Reinforce the principle: AI supports drafting and thinking, not final decisions. "
                "You remain the responsible human. Your professional judgement is the final check."
            ),
        },
        {
            "misconception": "If no policy exists yet, staff can use any tool they like.",
            "why_it_is_risky": (
                "UK GDPR and sector-specific regulations apply regardless of whether an internal "
                "AI policy has been written. Absence of a policy does not create permission."
            ),
            "facilitator_response": (
                "Explain that the legal obligation exists independently of internal policy. "
                "Until a formal policy is in place, the safe default is: do not enter personal, "
                "sensitive, or regulated information into any AI tool."
            ),
        },
    ]


# ── Debrief guidance ─────────────────────────────────────────────────────────────

def generate_debrief_guidance(
    scenario: dict,
    activities: list = None,
) -> list:
    """Return debrief guidance notes for the close of session."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)

    guidance = [
        f"Open the debrief by asking: 'What is the one thing from today you will do differently when using AI tools?'",
        "Allow 3–4 participants to share. Note answers on the flipchart or whiteboard.",
        "Summarise the three core responsible-use principles: anonymise, review, escalate.",
        "Confirm the escalation contacts for this organisation: DPO, safeguarding lead, line manager.",
        "Address any parking-lot questions that can be answered in the session.",
        "Flag which parking-lot items require follow-up from a manager, policy owner, DPO, or safeguarding lead.",
        "Close with the three commitments: (1) use approved tools only, (2) anonymise before prompting, (3) always review before use.",
        f"Remind participants that the staff handout [if available] summarises the key dos and don'ts for {sector} contexts.",
    ]

    if activities:
        activity_titles = [a.get("activity_title", "") for a in activities]
        if activity_titles:
            guidance.append(
                f"If time allows, revisit the activity that generated the most discussion: "
                f"ask what would have happened in a real scenario."
            )

    return guidance


# ── Risk warnings ────────────────────────────────────────────────────────────────

def generate_facilitator_risk_warnings(
    scenario: dict,
    assessment: dict = None,
) -> list:
    """Return facilitator-specific risk warnings for the session."""
    warnings = [
        "Do not enter learner names or identifiable learner details into AI tools during the session.",
        "Do not enter safeguarding case details — even as a 'demonstration' — into AI tools.",
        "Do not enter confidential client records, staff HR data, personal data, or regulated information.",
        "Do not allow AI to make safeguarding, disciplinary, assessment, legal, compliance, or HR decisions.",
        "AI outputs demonstrated during the session can be inaccurate, biased, incomplete, or invented — make this explicit.",
        "Human review remains required for all AI output — model this behaviour during the session.",
        "Staff should use organisation-approved tools and follow organisational policy.",
        "Escalate uncertainty to the appropriate human owner — demonstrate this principle in the session.",
        "If a participant raises a real safeguarding concern during the session, follow the organisation's safeguarding procedure immediately.",
        "If a participant shares real personal data, stop and redirect — do not continue using that data in the session.",
    ]

    high_topics = _get_high_priority_topics(assessment)
    if "safeguarding boundaries" in high_topics or "learner data boundaries" in high_topics:
        warnings.append(
            "This organisation's Training Needs Assessment identified safeguarding and learner data "
            "as high-priority topics — pay particular attention to reinforcing these boundaries."
        )

    return warnings


# ── Discussion prompts ───────────────────────────────────────────────────────────

def generate_facilitator_discussion_prompts(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> list:
    """Return facilitated discussion prompts for the session."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    prompts = [
        f"What AI tools are you currently using for work tasks — either approved or informally?",
        f"What is the most common task in your role where AI could help you draft or plan?",
        f"What would need to be true before you felt confident using an AI tool for that task?",
        f"Where do you think AI use could go wrong in a {sector} context?",
        f"What would you do if a colleague asked you to paste a safeguarding concern into ChatGPT?",
        f"What does 'human review' look like in practice for your role?",
        f"Who in this organisation should own the decision about which AI tools are approved?",
        f"What should happen if a staff member discovers they have entered personal data into an unapproved AI tool?",
    ]

    if workshop_plan and workshop_plan.get("discussion_prompts"):
        extra = workshop_plan["discussion_prompts"]
        for p in extra:
            if p not in prompts:
                prompts.append(p)

    return prompts[:10]


# ── Follow-up guidance ───────────────────────────────────────────────────────────

def _generate_follow_up_guidance(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> list:
    org = _get_org(scenario)
    sector = _get_sector(scenario)

    guidance = [
        f"Share the workshop materials with all participants within 2 working days.",
        f"Follow up on parking-lot questions with the relevant policy owner, DPO, or safeguarding lead.",
        f"Confirm the organisation's approved AI tools list and share it with all staff.",
        f"Agree a date for the next AI responsible-use review — recommended within 6 months.",
        f"Ensure all staff have the escalation contacts: DPO, safeguarding lead, line manager.",
        f"Review and update the organisation's AI policy or acceptable use statement if one does not yet exist.",
        f"Consider a short follow-up check-in (15 min) in 4–6 weeks to review how staff are applying what they learned.",
    ]

    if workshop_plan and workshop_plan.get("follow_up_actions"):
        for action in workshop_plan["follow_up_actions"]:
            if action not in guidance:
                guidance.append(action)

    return guidance[:10]


# ── Guide title ──────────────────────────────────────────────────────────────────

def _create_guide_title(
    scenario: dict,
    workshop_plan: dict = None,
) -> str:
    if workshop_plan and workshop_plan.get("workshop_title"):
        return f"Facilitator Guide: {workshop_plan['workshop_title']}"
    sector = _get_sector(scenario)
    goal = scenario.get("training_goal") or "Responsible AI Use"
    short_goal = goal[:60].rstrip(".")
    return f"Facilitator Guide: Responsible AI Use in {sector.title()}"


# ── Main generation function ─────────────────────────────────────────────────────

def generate_facilitator_guide(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
    activities: list = None,
) -> dict:
    """Generate a complete facilitator guide dict from the given inputs."""
    if not scenario:
        scenario = {}

    org = _get_org(scenario)
    roles = _get_roles(scenario)
    duration = _get_duration(scenario, workshop_plan)
    delivery_mode = _get_delivery_mode(scenario, workshop_plan)

    session_purpose = (
        f"To equip {org} staff with practical knowledge and confidence to use AI tools "
        f"safely and responsibly — understanding where AI can help, where it must not be "
        f"used, and how human review and escalation work in practice."
    )

    return {
        "guide_title": _create_guide_title(scenario, workshop_plan),
        "organisation_name": org,
        "audience": roles,
        "duration_minutes": duration,
        "delivery_mode": delivery_mode,
        "session_purpose": session_purpose,
        "facilitator_principles": get_default_facilitator_principles(),
        "preparation_checklist": get_facilitator_preparation_checklist(),
        "opening_script": generate_opening_script(scenario, workshop_plan),
        "section_delivery_notes": generate_section_delivery_notes(
            scenario, assessment, workshop_plan
        ),
        "activity_facilitation_notes": generate_activity_facilitation_notes(activities),
        "discussion_prompts": generate_facilitator_discussion_prompts(
            scenario, assessment, workshop_plan
        ),
        "common_misconceptions": generate_common_misconceptions(scenario, assessment),
        "debrief_guidance": generate_debrief_guidance(scenario, activities),
        "risk_warnings": generate_facilitator_risk_warnings(scenario, assessment),
        "responsible_use_messages": _RESPONSIBLE_USE_MESSAGES,
        "closing_script": generate_closing_script(scenario, workshop_plan),
        "follow_up_guidance": _generate_follow_up_guidance(
            scenario, assessment, workshop_plan
        ),
        "prototype_note": _PROTOTYPE_NOTE,
    }


# ── Summary and export ────────────────────────────────────────────────────────────

def summarise_facilitator_guide(facilitator_guide: dict) -> dict:
    """Return a compact summary dict for metric cards."""
    activities_covered = len(facilitator_guide.get("activity_facilitation_notes", []))
    return {
        "organisation_name": facilitator_guide.get("organisation_name", ""),
        "audience_roles": facilitator_guide.get("audience", []),
        "duration_minutes": facilitator_guide.get("duration_minutes", 90),
        "delivery_mode": facilitator_guide.get("delivery_mode", ""),
        "activities_covered": activities_covered,
        "section_count": len(facilitator_guide.get("section_delivery_notes", [])),
        "misconception_count": len(facilitator_guide.get("common_misconceptions", [])),
        "discussion_prompt_count": len(facilitator_guide.get("discussion_prompts", [])),
    }


def format_facilitator_guide_as_markdown(facilitator_guide: dict) -> str:
    """Return the facilitator guide as a complete Markdown document."""
    lines = []

    lines.append("# Responsible AI Workshop Facilitator Guide")
    lines.append("")

    lines.append("## Organisation")
    lines.append("")
    lines.append(f"**Organisation:** {facilitator_guide.get('organisation_name', '')}")
    lines.append(f"**Audience:** {', '.join(facilitator_guide.get('audience', []))}")
    lines.append(f"**Duration:** {facilitator_guide.get('duration_minutes', 90)} minutes")
    lines.append(f"**Delivery mode:** {facilitator_guide.get('delivery_mode', '')}")
    lines.append("")

    lines.append("## Session Purpose")
    lines.append("")
    lines.append(facilitator_guide.get("session_purpose", ""))
    lines.append("")

    lines.append("## Audience and Delivery Mode")
    lines.append("")
    roles = facilitator_guide.get("audience", [])
    if roles:
        for role in roles:
            lines.append(f"- {role}")
    lines.append(f"- **Delivery:** {facilitator_guide.get('delivery_mode', '')}")
    lines.append(f"- **Duration:** {facilitator_guide.get('duration_minutes', 90)} minutes")
    lines.append("")

    lines.append("## Facilitator Principles")
    lines.append("")
    for principle in facilitator_guide.get("facilitator_principles", []):
        lines.append(f"- {principle}")
    lines.append("")

    lines.append("## Preparation Checklist")
    lines.append("")
    for i, item in enumerate(facilitator_guide.get("preparation_checklist", []), 1):
        lines.append(f"{i}. {item}")
    lines.append("")

    lines.append("## Opening Script")
    lines.append("")
    lines.append(facilitator_guide.get("opening_script", ""))
    lines.append("")

    lines.append("## Section-by-Section Delivery Notes")
    lines.append("")
    for note in facilitator_guide.get("section_delivery_notes", []):
        lines.append(f"### {note.get('section_title', '')}")
        lines.append("")
        if note.get("suggested_timing"):
            lines.append(f"**Suggested timing:** {note['suggested_timing']}")
        lines.append(f"**Facilitator goal:** {note.get('facilitator_goal', '')}")
        lines.append("")
        lines.append(f"**What to say:** {note.get('what_to_say', '')}")
        lines.append("")
        asks = note.get("what_to_ask", [])
        if asks:
            lines.append("**What to ask:**")
            for q in asks:
                lines.append(f"- {q}")
            lines.append("")
        responses = note.get("expected_responses", [])
        if responses:
            lines.append("**Expected responses:**")
            for r in responses:
                lines.append(f"- {r}")
            lines.append("")
        watch = note.get("watch_out_for", [])
        if watch:
            lines.append("**Watch out for:**")
            for w in watch:
                lines.append(f"- {w}")
            lines.append("")
        if note.get("transition_note"):
            lines.append(f"**Transition:** {note['transition_note']}")
        lines.append("")

    lines.append("## Activity Facilitation Notes")
    lines.append("")
    for note in facilitator_guide.get("activity_facilitation_notes", []):
        lines.append(f"### {note.get('activity_title', 'Activity')} ({note.get('duration_minutes', 10)} min)")
        lines.append("")
        lines.append(f"**Facilitator goal:** {note.get('facilitator_goal', '')}")
        lines.append("")
        setup = note.get("setup_instructions", [])
        if setup:
            lines.append("**Setup:**")
            for s in setup:
                lines.append(f"- {s}")
            lines.append("")
        how = note.get("how_to_run", [])
        if how:
            lines.append("**How to run:**")
            for i, step in enumerate(how, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        expected = note.get("expected_answers", [])
        if expected:
            lines.append("**Expected answers:**")
            for ans in expected:
                lines.append(f"- {ans}")
            lines.append("")
        debrief = note.get("debrief_questions", [])
        if debrief:
            lines.append("**Debrief questions:**")
            for q in debrief:
                lines.append(f"- {q}")
            lines.append("")
        takeaways = note.get("key_takeaways", [])
        if takeaways:
            lines.append("**Key takeaways:**")
            for t in takeaways:
                lines.append(f"- {t}")
            lines.append("")

    lines.append("## Discussion Prompts")
    lines.append("")
    for i, prompt in enumerate(facilitator_guide.get("discussion_prompts", []), 1):
        lines.append(f"{i}. {prompt}")
    lines.append("")

    lines.append("## Common Misconceptions and Suggested Responses")
    lines.append("")
    for misconception in facilitator_guide.get("common_misconceptions", []):
        lines.append(f"### Misconception: \"{misconception.get('misconception', '')}\"")
        lines.append("")
        lines.append(f"**Why it is risky:** {misconception.get('why_it_is_risky', '')}")
        lines.append("")
        lines.append(f"**Facilitator response:** {misconception.get('facilitator_response', '')}")
        lines.append("")

    lines.append("## Debrief Guidance")
    lines.append("")
    for i, item in enumerate(facilitator_guide.get("debrief_guidance", []), 1):
        lines.append(f"{i}. {item}")
    lines.append("")

    lines.append("## Risk Warnings")
    lines.append("")
    for warning in facilitator_guide.get("risk_warnings", []):
        lines.append(f"- {warning}")
    lines.append("")

    lines.append("## Responsible Use Messages")
    lines.append("")
    for msg in facilitator_guide.get("responsible_use_messages", []):
        lines.append(f"- {msg}")
    lines.append("")

    lines.append("## Closing Script")
    lines.append("")
    lines.append(facilitator_guide.get("closing_script", ""))
    lines.append("")

    lines.append("## Follow-Up Guidance")
    lines.append("")
    for i, item in enumerate(facilitator_guide.get("follow_up_guidance", []), 1):
        lines.append(f"{i}. {item}")
    lines.append("")

    lines.append("## Prototype and Responsible-Use Boundaries")
    lines.append("")
    lines.append(facilitator_guide.get("prototype_note", _PROTOTYPE_NOTE))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)


def create_facilitator_guide_filename(organisation_name: str) -> str:
    """Return a safe kebab-case filename for the facilitator guide Markdown file."""
    org = organisation_name or "organisation"
    slug = org.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return f"facilitator-guide-{slug}.md"
