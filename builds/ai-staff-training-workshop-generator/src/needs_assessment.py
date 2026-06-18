"""Training needs assessment for the AI Staff Training and Workshop Generator.

Phase 2: maps a synthetic organisation scenario to deterministic training needs,
priority topics, learning outcomes, and role-specific guidance.
No external AI API calls. Synthetic scenarios only.
"""

# ── Topic catalogue ────────────────────────────────────────────────────────────

def get_training_topic_catalogue() -> dict:
    """Return the full catalogue of responsible AI training topics.

    Each entry includes: title, description, risk_level, why_it_matters,
    example_staff_behaviour, recommended_training_angle.
    """
    return {
        "AI basics": {
            "title": "AI Basics and What AI Tools Actually Do",
            "description": (
                "A grounding overview of what AI language models are, how they work, "
                "and what they are and are not capable of."
            ),
            "risk_level": "low",
            "why_it_matters": (
                "Staff who don't understand how AI tools work are more likely to "
                "misuse them, over-trust outputs, or be unable to spot errors."
            ),
            "example_staff_behaviour": (
                "A tutor assumes ChatGPT has looked up the latest qualification "
                "requirements and acts on an outdated answer."
            ),
            "recommended_training_angle": (
                "Use a short demonstration of what AI can and cannot do. "
                "Emphasise that AI predicts plausible text, not verified fact."
            ),
        },
        "safe prompting": {
            "title": "Safe Prompting Techniques",
            "description": (
                "How to write prompts that achieve useful results without entering "
                "personal, sensitive, or confidential information."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "Poorly constructed prompts are the most common route for accidental "
                "data entry into AI tools. Staff need practical techniques they can "
                "use immediately."
            ),
            "example_staff_behaviour": (
                "An administrator copies a learner's name, address, and course status "
                "into a prompt to ask ChatGPT to write a progress letter."
            ),
            "recommended_training_angle": (
                "Rewrite practice: staff rewrite risky prompts into safe, anonymised "
                "or synthetic versions. Show before and after examples."
            ),
        },
        "learner data boundaries": {
            "title": "Learner Data Boundaries",
            "description": (
                "Understanding which types of learner information must never be "
                "entered into AI tools, and why."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "Learner data is personal data under UK GDPR. Entering it into "
                "external AI tools without a legal basis and appropriate controls "
                "is a data protection breach."
            ),
            "example_staff_behaviour": (
                "A tutor enters a learner's name, course, and attendance record into "
                "ChatGPT to get help writing a progress review."
            ),
            "recommended_training_angle": (
                "Clear 'never enter' list with concrete examples. "
                "Provide approved alternatives for common tasks."
            ),
        },
        "safeguarding boundaries": {
            "title": "Safeguarding Boundaries and AI",
            "description": (
                "Why safeguarding disclosures, welfare concerns, and case information "
                "must never be processed by AI tools."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "Safeguarding decisions require qualified human judgement and "
                "established procedures. AI tools can produce harmful, incorrect, "
                "or misleading responses to safeguarding scenarios."
            ),
            "example_staff_behaviour": (
                "A tutor describes a learner's disclosed concern to ChatGPT and asks "
                "what to do, instead of following the safeguarding procedure."
            ),
            "recommended_training_angle": (
                "Absolute rule: never share safeguarding information with AI tools. "
                "Reinforce the existing escalation procedure and key contacts."
            ),
        },
        "human review": {
            "title": "Human Review of AI Outputs",
            "description": (
                "Why all AI-generated content must be reviewed by a qualified human "
                "before use — and what to check for."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "AI tools produce plausible-sounding content that may be inaccurate, "
                "biased, incomplete, or inappropriate. Human review is the primary "
                "safeguard for responsible AI use."
            ),
            "example_staff_behaviour": (
                "A team leader copies an AI-generated staff briefing into an email "
                "without reading it carefully, including a factual error about a policy."
            ),
            "recommended_training_angle": (
                "Practical review checklist: fact-check, tone-check, appropriateness "
                "check, and source verification. Use example AI outputs for practice."
            ),
        },
        "approved tools": {
            "title": "Approved AI Tools and Unofficial Use",
            "description": (
                "Understanding which AI tools are approved for use, what the "
                "approval process looks like, and the risks of using unapproved tools."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "Unapproved tools may process and store data in ways that breach "
                "data protection law or organisational policy. Staff using personal "
                "accounts are creating data liability."
            ),
            "example_staff_behaviour": (
                "A staff member uses a personal free ChatGPT account with work data, "
                "unaware that the organisation's policy prohibits this."
            ),
            "recommended_training_angle": (
                "Present the approved tools list and the process for requesting a new "
                "tool. Explain the specific data risks of free consumer AI accounts."
            ),
        },
        "hallucination and accuracy": {
            "title": "Hallucination and Output Accuracy",
            "description": (
                "What AI hallucination is, why it happens, and how to verify "
                "AI-generated facts, citations, and recommendations."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "AI tools can confidently state incorrect facts, invent sources, "
                "and generate plausible-looking but wrong information. "
                "Acting on unverified AI output can cause harm to learners and "
                "reputational damage to the organisation."
            ),
            "example_staff_behaviour": (
                "A tutor includes an AI-generated citation in a learning resource "
                "without checking whether the source exists or is correctly quoted."
            ),
            "recommended_training_angle": (
                "Hallucination demonstration: show a live or recorded example. "
                "Teach a 3-step verification habit: check, source, confirm."
            ),
        },
        "bias and fairness": {
            "title": "Bias and Fairness in AI Outputs",
            "description": (
                "How AI tools can reflect or amplify bias in language, recommendations, "
                "and assessments — and what to watch for."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "Biased AI outputs can disadvantage learners from specific backgrounds, "
                "create unequal experiences, and conflict with the organisation's "
                "equality and diversity obligations."
            ),
            "example_staff_behaviour": (
                "A tutor uses an AI-generated assessment rubric without checking "
                "whether it contains culturally biased language or assumptions."
            ),
            "recommended_training_angle": (
                "Bias spotting exercise: review AI-generated examples and identify "
                "potential fairness issues. Link to equality and diversity policy."
            ),
        },
        "accountability": {
            "title": "Accountability and Professional Responsibility",
            "description": (
                "Understanding that AI does not remove professional accountability — "
                "staff remain responsible for AI-assisted outputs."
            ),
            "risk_level": "medium",
            "why_it_matters": (
                "Staff may assume that using an AI tool shifts responsibility for "
                "outputs. In regulated and professional contexts, the human producing "
                "or sharing the output remains accountable."
            ),
            "example_staff_behaviour": (
                "A staff member shares an AI-generated report claiming they checked it, "
                "but only skimmed it — and the report contains errors."
            ),
            "recommended_training_angle": (
                "Scenario discussion: who is responsible when an AI-assisted output "
                "causes a problem? Ground in real professional accountability principles."
            ),
        },
        "copyright and intellectual property": {
            "title": "Copyright and Intellectual Property",
            "description": (
                "The copyright implications of AI-generated text, images, and code — "
                "and the organisation's obligations."
            ),
            "risk_level": "medium",
            "why_it_matters": (
                "AI-generated content may reproduce copyrighted material or create "
                "ambiguous ownership. Using AI-generated content in learning materials "
                "without appropriate disclosure may create legal and reputational risk."
            ),
            "example_staff_behaviour": (
                "A staff member uses an AI-generated image in a learning resource "
                "without checking whether it is free for commercial use."
            ),
            "recommended_training_angle": (
                "Overview of copyright position on AI content. "
                "Practical guidance on when to disclose AI assistance and how."
            ),
        },
        "escalation routes": {
            "title": "Escalation Routes and Incident Reporting",
            "description": (
                "Who to contact when an AI tool produces something concerning — "
                "and how to report it."
            ),
            "risk_level": "high",
            "why_it_matters": (
                "Staff who encounter harmful, incorrect, or concerning AI outputs "
                "need clear escalation routes. Without them, problems go unreported "
                "and unresolved."
            ),
            "example_staff_behaviour": (
                "A staff member receives a deeply inappropriate AI-generated response "
                "and does not know who to report it to or whether they need to."
            ),
            "recommended_training_angle": (
                "Confirm key contacts and escalation steps. "
                "Cover data breach reporting, safeguarding escalation, and "
                "general AI incident reporting in three concrete scenarios."
            ),
        },
        "data minimisation": {
            "title": "Data Minimisation in AI Prompts",
            "description": (
                "Using the minimum amount of information necessary when writing "
                "prompts — and how to anonymise or generalise examples."
            ),
            "risk_level": "medium",
            "why_it_matters": (
                "Entering more data than necessary into AI tools increases data "
                "protection risk. Data minimisation is a UK GDPR principle that "
                "applies to AI tool use."
            ),
            "example_staff_behaviour": (
                "A staff member includes a full learner profile in a prompt when "
                "only a brief description of the task was needed."
            ),
            "recommended_training_angle": (
                "Prompt editing exercise: trim a sample prompt down to the minimum "
                "required information while preserving its usefulness."
            ),
        },
        "time-saving and workflow discipline": {
            "title": "Time-Saving and Workflow Discipline",
            "description": (
                "How to use AI tools productively for low-risk tasks without "
                "creating new burdens through poor workflow habits."
            ),
            "risk_level": "low",
            "why_it_matters": (
                "Staff adoption of AI tools without workflow discipline can create "
                "more work through over-reliance, excessive revision, or poor output "
                "quality. Setting good habits early prevents this."
            ),
            "example_staff_behaviour": (
                "A staff member spends 45 minutes revising an AI-generated email that "
                "would have taken 10 minutes to write from scratch."
            ),
            "recommended_training_angle": (
                "Practical guidance on which tasks AI genuinely saves time on vs "
                "tasks where it adds friction. Cover the 'good enough to useful' "
                "threshold and when to stop revising."
            ),
        },
    }


# ── Priority logic ─────────────────────────────────────────────────────────────

_HIGH_RISK_TOPICS = {
    "safe prompting",
    "learner data boundaries",
    "safeguarding boundaries",
    "human review",
    "approved tools",
    "hallucination and accuracy",
    "bias and fairness",
    "escalation routes",
}


def assess_topic_priority(scenario: dict, topic: str) -> dict:
    """Return a priority assessment dict for a single topic against a scenario.

    Priority is high if:
    - the topic is in scenario["priority_topics"], OR
    - the topic is in the high-risk set and relates to a scenario concern.

    Otherwise medium if the topic appears in main_concerns (loosely matched).
    Otherwise low.
    """
    catalogue = get_training_topic_catalogue()
    topic_data = catalogue.get(topic, {})

    priority_topics = [t.lower() for t in scenario.get("priority_topics", [])]
    main_concerns = " ".join(scenario.get("main_concerns", [])).lower()

    in_priority_list = topic.lower() in priority_topics
    is_high_risk = topic.lower() in _HIGH_RISK_TOPICS
    concern_match = any(word in main_concerns for word in topic.lower().split())

    if in_priority_list or (is_high_risk and concern_match):
        priority_level = "high"
    elif concern_match:
        priority_level = "medium"
    else:
        priority_level = "low"

    return {
        "topic": topic,
        "title": topic_data.get("title", topic),
        "priority_level": priority_level,
        "risk_level": topic_data.get("risk_level", "medium"),
        "why_it_matters": topic_data.get("why_it_matters", ""),
        "training_need": (
            f"Staff need to understand and apply: {topic_data.get('description', topic)}"
        ),
        "example_staff_behaviour": topic_data.get("example_staff_behaviour", ""),
        "recommended_training_angle": topic_data.get("recommended_training_angle", ""),
    }


# ── Role-specific needs ────────────────────────────────────────────────────────

_ROLE_NEEDS = {
    "tutors": {
        "role": "Tutors",
        "key_risks": [
            "Using learner names or records in prompts",
            "Acting on unverified AI-generated lesson content",
            "Using AI for safeguarding decisions",
            "Over-trusting AI accuracy for qualification or policy information",
        ],
        "training_focus": (
            "Safe lesson planning prompts, avoiding learner identifiers, verifying "
            "factual accuracy, and understanding that AI must never be used for "
            "safeguarding decisions or welfare judgements."
        ),
        "practical_guidance": [
            "Write lesson planning prompts without learner names or personal details.",
            "Always check AI-generated content for factual accuracy before use.",
            "Never describe a learner's welfare concern to an AI tool.",
            "Use approved tools only — not personal AI accounts.",
        ],
    },
    "administrators": {
        "role": "Administrators",
        "key_risks": [
            "Entering personal data into AI tools when drafting letters or emails",
            "Using AI to process enrolment, attendance, or progress records",
            "Sharing AI-generated communications without reviewing them",
            "Using unapproved tools for routine admin tasks",
        ],
        "training_focus": (
            "Data-minimised prompts for email and document drafts, understanding "
            "which admin data must never be entered into AI tools, and reviewing "
            "AI-generated communications before sending."
        ),
        "practical_guidance": [
            "Never enter learner names, addresses, or course details into AI prompts.",
            "Use placeholder names or anonymised descriptions in draft prompts.",
            "Read AI-generated emails fully before sending — check tone and accuracy.",
            "If unsure whether a task involves personal data, ask your manager.",
        ],
    },
    "team leaders": {
        "role": "Team Leaders",
        "key_risks": [
            "Setting poor expectations around AI use for their team",
            "Not knowing how to handle staff AI incidents or concerns",
            "Using AI to inform HR or performance decisions without appropriate review",
            "Sharing AI-generated staff-facing content without sufficient review",
        ],
        "training_focus": (
            "Policy enforcement, escalation procedures, supporting staff to use AI "
            "safely, and understanding the accountability implications of AI-assisted "
            "management tasks."
        ),
        "practical_guidance": [
            "Know the escalation route for AI-related data or safeguarding incidents.",
            "Do not use AI to draft HR, performance, or disciplinary communications.",
            "Model good AI use habits — review and verify before sharing.",
            "Create space for staff to ask questions about appropriate AI use.",
        ],
    },
    "quality lead": {
        "role": "Quality Lead",
        "key_risks": [
            "AI-assisted quality reports containing unverified data or inaccurate analysis",
            "AI-generated compliance or self-assessment language that overstates evidence",
            "AI tools being used by staff without audit trail or oversight",
            "Quality documents referencing AI-generated content without disclosure",
        ],
        "training_focus": (
            "Quality assurance of AI-assisted outputs, maintaining audit trails, "
            "disclosure of AI tool use in quality documents, and reviewing AI tools "
            "for organisational risk."
        ),
        "practical_guidance": [
            "Establish a review process for AI-assisted quality documents.",
            "Require staff to label AI-assisted content in internal submissions.",
            "Include AI tool use in the organisation's risk register review.",
            "Verify AI-generated data summaries against source records.",
        ],
    },
    "curriculum leads": {
        "role": "Curriculum Leads",
        "key_risks": [
            "AI-generated curriculum content containing inaccuracies or outdated information",
            "Copyright issues in AI-generated learning materials",
            "Bias in AI-generated assessment criteria or rubrics",
            "Over-reliance on AI for curriculum design without expert review",
        ],
        "training_focus": (
            "Safe use of AI for curriculum drafting, copyright and IP obligations, "
            "bias checking in assessment content, and maintaining expert curriculum "
            "ownership."
        ),
        "practical_guidance": [
            "Treat AI-generated curriculum content as a first draft requiring expert review.",
            "Check for copyright before using AI-generated images or written passages.",
            "Review assessment rubrics for culturally biased language.",
            "Document where AI tools have been used in curriculum development.",
        ],
    },
    "assessors": {
        "role": "Assessors",
        "key_risks": [
            "Using AI to make or support assessment decisions",
            "Entering learner work or performance details into AI tools",
            "AI-generated feedback that lacks specificity or contains errors",
            "Learner data protection breaches via AI-assisted assessment notes",
        ],
        "training_focus": (
            "The boundaries of AI in assessment, data protection in assessment "
            "contexts, and maintaining professional judgement as the assessor."
        ),
        "practical_guidance": [
            "Never enter learner work, portfolios, or assessment decisions into AI.",
            "AI-generated feedback must be fully reviewed and personalised before use.",
            "Assessment decisions must be made by qualified human assessors.",
            "Do not use AI to summarise or process learner achievement data.",
        ],
    },
}


def generate_role_specific_needs(scenario: dict) -> list:
    """Return a list of role-specific training need dicts for the scenario's staff roles.

    Uses the _ROLE_NEEDS library. Falls back to a generic entry for unknown roles.
    """
    roles = scenario.get("staff_roles", [])
    if not roles:
        roles = ["staff"]

    result = []
    for role in roles:
        role_lower = role.lower()
        if role_lower in _ROLE_NEEDS:
            result.append(dict(_ROLE_NEEDS[role_lower]))
        else:
            result.append({
                "role": role.title(),
                "key_risks": [
                    "Potential data entry errors when using AI tools",
                    "Over-reliance on AI outputs without sufficient human review",
                ],
                "training_focus": (
                    f"{role.title()} staff should focus on safe prompting, "
                    "human review of AI outputs, and knowing when not to use AI."
                ),
                "practical_guidance": [
                    "Use AI only for low-risk, non-personal tasks.",
                    "Always review AI outputs before acting on them.",
                    "Escalate concerns to your manager or the quality lead.",
                ],
            })
    return result


# ── Learning outcomes ──────────────────────────────────────────────────────────

_OUTCOME_TEMPLATES = {
    "safe prompting": (
        "Write data-minimised, anonymised prompts for common tasks such as "
        "lesson planning and email drafting without entering personal or sensitive information."
    ),
    "learner data boundaries": (
        "Explain which types of learner information must never be entered into AI tools "
        "and identify three approved alternatives for common tasks."
    ),
    "safeguarding boundaries": (
        "Describe why safeguarding disclosures and welfare concerns must never be "
        "shared with AI tools and state the correct escalation procedure."
    ),
    "human review": (
        "Apply a consistent review process to AI-generated content before sharing or "
        "acting on it — checking for accuracy, tone, and appropriateness."
    ),
    "approved tools": (
        "Identify which AI tools are approved for use in the organisation and explain "
        "why using unapproved personal accounts creates data protection risk."
    ),
    "hallucination and accuracy": (
        "Recognise common signs of AI hallucination and apply a three-step "
        "verification habit: check, source, confirm."
    ),
    "bias and fairness": (
        "Identify potential bias in AI-generated assessment, feedback, and "
        "communication content and apply the organisation's equality and diversity principles."
    ),
    "escalation routes": (
        "State the escalation route for three types of AI-related incident: "
        "data concern, safeguarding concern, and general AI output concern."
    ),
    "accountability": (
        "Explain why professional accountability for AI-assisted outputs remains with "
        "the staff member who produces or shares them."
    ),
    "data minimisation": (
        "Rewrite a detailed prompt into a data-minimised version that achieves the "
        "same task without entering unnecessary personal or sensitive information."
    ),
    "copyright and intellectual property": (
        "Describe the organisation's position on using AI-generated content in "
        "learning materials and when to disclose AI assistance."
    ),
    "time-saving and workflow discipline": (
        "Identify three tasks where AI genuinely saves time and two tasks where "
        "it is likely to add friction — and explain why."
    ),
    "AI basics": (
        "Explain in plain language what AI language models do, "
        "why they can produce incorrect outputs, and why human oversight matters."
    ),
}

_DEFAULT_OUTCOMES = [
    "Identify safe and unsafe AI use cases relevant to your role.",
    "Apply human review to any AI-generated content before sharing or acting on it.",
    "Know who to contact if an AI tool produces something concerning or harmful.",
]


def generate_learning_outcomes(scenario: dict, priority_topics: list) -> list:
    """Return 5–8 practical learning outcomes for the given scenario and topics.

    Outcomes are selected from templates keyed to priority topics.
    Up to 5 topic-specific outcomes are returned, plus a default closing outcome.
    """
    outcomes = []
    for topic in priority_topics:
        if topic in _OUTCOME_TEMPLATES and len(outcomes) < 6:
            outcomes.append(_OUTCOME_TEMPLATES[topic])

    for default in _DEFAULT_OUTCOMES:
        if default not in outcomes and len(outcomes) < 8:
            outcomes.append(default)

    return outcomes


# ── Risk and session type helpers ──────────────────────────────────────────────

def _derive_risk_summary(scenario: dict, topic_assessments: list) -> str:
    high_priority = [t for t in topic_assessments if t["priority_level"] == "high"]
    high_count = len(high_priority)
    org = scenario.get("organisation_name", "This organisation")
    concerns = scenario.get("main_concerns", [])

    if high_count >= 6:
        level = "high"
        framing = (
            f"{org} has {high_count} high-priority training topics, indicating "
            "significant staff exposure to AI risk through informal tool use. "
            "Training should prioritise data protection, safeguarding boundaries, "
            "and human review before covering productivity topics."
        )
    elif high_count >= 3:
        level = "medium-high"
        framing = (
            f"{org} has {high_count} high-priority training topics. "
            "The core risk areas are "
            + ", ".join(t["topic"] for t in high_priority[:3])
            + ". Training should address these explicitly before broadening to workflow topics."
        )
    else:
        level = "medium"
        framing = (
            f"{org} has {high_count} high-priority training topics. "
            "Staff awareness is the primary need — training should build confidence "
            "in safe AI use rather than focus heavily on prohibitions."
        )

    if concerns:
        framing += (
            f" Staff have expressed concern about: "
            + ", ".join(concerns[:4])
            + (". These concerns should be addressed directly in the session." if len(concerns) <= 4
               else f" and {len(concerns) - 4} further areas.")
        )

    return framing


def _derive_session_type(scenario: dict, high_count: int) -> str:
    duration = scenario.get("training_duration", "").lower()
    mode = scenario.get("delivery_mode", "").lower()
    staff_count = scenario.get("staff_count", 0)

    if high_count >= 6:
        focus = "focused responsible-use workshop with scenario-based activities"
    elif high_count >= 3:
        focus = "mixed workshop covering policy, practice, and scenario activities"
    else:
        focus = "awareness session with practical workflow guidance"

    delivery = "in-person" if "in-person" in mode or "face" in mode else "online or hybrid"
    size = "small group" if staff_count <= 12 else "larger group"

    return f"{duration} {delivery} {size} — {focus}".strip().lstrip("—").strip()


# ── Main assessment function ───────────────────────────────────────────────────

def generate_training_needs_assessment(scenario: dict) -> dict:
    """Generate a full training needs assessment from a synthetic organisation scenario.

    Returns a structured dict covering priority topics, role-specific needs,
    learning outcomes, risk summary, and responsible-use framing.
    """
    org = scenario.get("organisation_name", "Unnamed organisation")
    training_goal = scenario.get("training_goal", "Help staff use AI responsibly.")
    staff_roles = scenario.get("staff_roles", [])
    priority_topics = scenario.get("priority_topics", [])

    # Assess each priority topic
    topic_assessments = [
        assess_topic_priority(scenario, topic)
        for topic in priority_topics
    ]

    # Also surface any catalogue topics not in priority_topics that scored high
    catalogue = get_training_topic_catalogue()
    covered = {t.lower() for t in priority_topics}
    for topic in catalogue:
        if topic.lower() not in covered:
            assessment = assess_topic_priority(scenario, topic)
            if assessment["priority_level"] == "high":
                topic_assessments.append(assessment)

    # Sort: high first, then medium, then low
    _order = {"high": 0, "medium": 1, "low": 2}
    topic_assessments.sort(key=lambda t: _order.get(t["priority_level"], 3))

    high_priority_topics = [
        t["topic"] for t in topic_assessments if t["priority_level"] == "high"
    ]
    high_count = len(high_priority_topics)

    role_specific_needs = generate_role_specific_needs(scenario)
    learning_outcomes = generate_learning_outcomes(scenario, high_priority_topics)
    risk_summary = _derive_risk_summary(scenario, topic_assessments)
    session_type = _derive_session_type(scenario, high_count)

    overall_focus = (
        f"Build practical responsible AI habits for {org} staff. "
        f"Prioritise the {high_count} high-risk topic{'s' if high_count != 1 else ''} "
        f"before covering workflow and productivity topics."
    ) if high_count > 0 else (
        f"Build AI awareness and safe working habits for {org} staff."
    )

    return {
        "organisation_name": org,
        "training_goal": training_goal,
        "staff_roles": staff_roles,
        "priority_topics": priority_topics,
        "topic_assessments": topic_assessments,
        "role_specific_needs": role_specific_needs,
        "recommended_learning_outcomes": learning_outcomes,
        "overall_training_focus": overall_focus,
        "risk_summary": risk_summary,
        "recommended_session_type": session_type,
        "responsible_use_note": (
            "This assessment uses a synthetic organisation scenario only. "
            "It must not be used with real learner data, safeguarding case details, "
            "confidential client records, staff HR data, personal data, or regulated "
            "information without appropriate governance, approvals, and responsible owners. "
            "This prototype does not provide legal, safeguarding, HR, compliance, "
            "medical, financial, academic-integrity, or professional advice."
        ),
    }


# ── Summary ────────────────────────────────────────────────────────────────────

def summarise_training_needs(assessment: dict) -> dict:
    """Return a compact summary dict for display in metric cards."""
    topic_assessments = assessment.get("topic_assessments", [])
    return {
        "organisation_name": assessment.get("organisation_name", ""),
        "staff_role_count": len(assessment.get("staff_roles", [])),
        "priority_topic_count": len(assessment.get("priority_topics", [])),
        "high_priority_count": sum(
            1 for t in topic_assessments if t.get("priority_level") == "high"
        ),
        "medium_priority_count": sum(
            1 for t in topic_assessments if t.get("priority_level") == "medium"
        ),
        "learning_outcome_count": len(assessment.get("recommended_learning_outcomes", [])),
        "recommended_session_type": assessment.get("recommended_session_type", ""),
        "overall_training_focus": assessment.get("overall_training_focus", ""),
    }


# ── Markdown export ────────────────────────────────────────────────────────────

def format_needs_assessment_as_markdown(assessment: dict) -> str:
    """Return a Markdown-formatted training needs assessment."""
    lines = []
    org = assessment.get("organisation_name", "Unknown organisation")

    lines.append("# Training Needs Assessment")
    lines.append("")
    lines.append(f"**Organisation:** {org}")
    lines.append("")

    lines.append("## Organisation")
    lines.append(f"- **Organisation:** {org}")
    roles = assessment.get("staff_roles", [])
    if roles:
        lines.append(f"- **Staff roles:** {', '.join(roles)}")
    lines.append("")

    lines.append("## Training Goal")
    lines.append(assessment.get("training_goal", ""))
    lines.append("")

    lines.append("## Priority Topics")
    for topic in assessment.get("priority_topics", []):
        lines.append(f"- {topic}")
    lines.append("")

    lines.append("## Topic Assessment")
    lines.append("")
    lines.append("| Topic | Priority | Risk | Why It Matters |")
    lines.append("|---|---|---|---|")
    for t in assessment.get("topic_assessments", []):
        why = t.get("why_it_matters", "").replace("\n", " ")[:120]
        lines.append(
            f"| {t.get('title', t.get('topic', ''))} "
            f"| {t.get('priority_level', '').upper()} "
            f"| {t.get('risk_level', '').upper()} "
            f"| {why} |"
        )
    lines.append("")

    lines.append("## Recommended Learning Outcomes")
    lines.append("")
    lines.append("By the end of the training session, staff will be able to:")
    lines.append("")
    for outcome in assessment.get("recommended_learning_outcomes", []):
        lines.append(f"- {outcome}")
    lines.append("")

    lines.append("## Role-Specific Training Needs")
    lines.append("")
    for role_need in assessment.get("role_specific_needs", []):
        lines.append(f"### {role_need.get('role', 'Staff')}")
        lines.append("")
        lines.append(f"**Training focus:** {role_need.get('training_focus', '')}")
        lines.append("")
        risks = role_need.get("key_risks", [])
        if risks:
            lines.append("**Key risks:**")
            for risk in risks:
                lines.append(f"- {risk}")
        guidance = role_need.get("practical_guidance", [])
        if guidance:
            lines.append("")
            lines.append("**Practical guidance:**")
            for g in guidance:
                lines.append(f"- {g}")
        lines.append("")

    lines.append("## Risk Summary")
    lines.append("")
    lines.append(assessment.get("risk_summary", ""))
    lines.append("")

    lines.append("## Recommended Session Type")
    lines.append("")
    lines.append(assessment.get("recommended_session_type", ""))
    lines.append("")

    lines.append("## Overall Training Focus")
    lines.append("")
    lines.append(assessment.get("overall_training_focus", ""))
    lines.append("")

    lines.append("## Responsible Use Boundaries")
    lines.append("")
    lines.append(assessment.get("responsible_use_note", ""))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*Training Needs Assessment · {org} · "
        "AI Staff Training and Workshop Generator · Build 4*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)
