"""Staff handout generator for the AI Staff Training and Workshop Generator.

Phase 6: generates a staff-facing responsible AI safe-use handout covering
safe-use principles, allowed/prohibited uses, prompt examples, human review
checklist, escalation guidance, and key takeaways.

All content is generated from synthetic organisation scenario data only.
No real learner data, safeguarding case details, or personal information.
"""

import re

_PROTOTYPE_NOTE = (
    "This staff handout is generated from a synthetic organisation scenario only. "
    "It must not be used with real learner data, safeguarding case details, "
    "confidential client records, staff HR data, personal data, or regulated "
    "information without appropriate governance, approvals, and responsible owners. "
    "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
    "financial, academic-integrity, or professional advice."
)

_RESPONSIBLE_USE_WARNING = (
    "Use synthetic or approved scenarios only. Do not enter real learner data, "
    "safeguarding case details, confidential client records, staff HR data, "
    "personal data, or regulated information into AI tools. Human review is "
    "required before using any AI output in real work."
)


def get_default_safe_use_principles() -> list:
    """Return a list of safe-use principles for staff."""
    return [
        "Use AI for low-risk drafting, planning, summarising, and idea generation.",
        "Use synthetic, anonymised, or generic examples — never real learner names, personal details, or case-specific facts.",
        "Keep learner data, safeguarding information, HR data, confidential records, personal data, and regulated information out of AI tools.",
        "Review AI outputs before using them. Check accuracy, tone, fairness, accessibility, and policy alignment.",
        "Use approved tools only. Do not use personal AI accounts for organisational tasks unless explicitly approved.",
        "Escalate uncertainty to the appropriate human owner — manager, safeguarding lead, data protection lead, or quality lead.",
        "Do not let AI make professional, safeguarding, assessment, disciplinary, legal, HR, or compliance decisions.",
        "Keep final responsibility with a human. AI supports your work — it does not replace your professional judgement.",
    ]


def generate_allowed_ai_uses(
    scenario: dict,
    assessment: dict | None = None,
) -> list:
    """Return a list of allowed AI uses based on the scenario."""
    org = scenario.get("organisation_name", "this organisation")
    sector = scenario.get("sector", "education and training").lower()

    base = [
        f"Drafting a generic lesson outline or session plan that will be reviewed before use at {org}.",
        "Creating discussion questions for a topic using only generic, non-identifiable content.",
        "Rewriting a generic email, letter, or notice for clarity or tone — without including personal details.",
        "Generating a checklist or template for a low-risk admin task.",
        "Producing ideas for classroom activities, learning materials, or group exercises.",
        "Simplifying generic learning materials or resources into plain English.",
        "Creating a neutral draft template that staff will review and adapt before any real use.",
        "Brainstorming topic ideas, agenda structures, or resource lists using generic examples.",
    ]

    if "education" in sector or "training" in sector:
        base.append(
            "Summarising generic research or publicly available guidance on a topic for staff awareness."
        )

    if assessment:
        priority_topics = [
            t.get("title", "")
            for t in assessment.get("topic_assessments", [])
            if t.get("priority_level") == "high"
        ]
        if "Safe Prompting" in str(priority_topics) or "Prompt Writing" in str(priority_topics):
            base.append(
                "Practising writing safe, generic prompts that do not include personal, learner, or regulated data."
            )

    return base


def generate_prohibited_ai_uses(
    scenario: dict,
    assessment: dict | None = None,
) -> list:
    """Return a list of prohibited AI uses based on the scenario."""
    base = [
        "Entering learner names, identifiable learner details, or personal learner records.",
        "Entering safeguarding case details, disclosures, or case-specific information.",
        "Entering confidential client records, organisation-specific contract data, or commercial-in-confidence information.",
        "Entering staff HR information, disciplinary records, or performance review content.",
        "Entering personal data or regulated information of any kind.",
        "Asking AI to decide safeguarding actions or assess safeguarding risk.",
        "Asking AI to make assessment decisions, exam judgements, or formal accreditation decisions.",
        "Asking AI to make disciplinary, legal, HR, compliance, or professional judgement decisions.",
        "Using unapproved personal AI accounts for work tasks where organisational policy requires approved systems.",
        "Using AI output without human review, especially for materials that will reach learners or external stakeholders.",
    ]

    if assessment:
        concerns = [
            t.get("title", "")
            for t in assessment.get("topic_assessments", [])
            if t.get("priority_level") == "high"
        ]
        if any("bias" in c.lower() for c in concerns):
            base.append(
                "Using AI-generated content about learner groups, demographics, or abilities without bias and fairness review."
            )
        if any("hallucination" in c.lower() or "accuracy" in c.lower() for c in concerns):
            base.append(
                "Treating AI output as factually reliable without verification — especially statistics, legal references, or policy claims."
            )

    return base


def generate_safe_prompt_examples(
    scenario: dict,
    activities: list | None = None,
) -> list:
    """Return a list of safe prompt example dicts."""
    org = scenario.get("organisation_name", "this organisation")

    examples = [
        {
            "title": "Generic lesson planning",
            "prompt": (
                f"Create a 30-minute introductory lesson outline on workplace communication "
                f"for adult learners. Do not include learner names, personal details, or "
                f"case-specific information."
            ),
            "why_it_is_safe": (
                "Uses a generic topic and includes an explicit instruction to exclude "
                "identifiable learner data."
            ),
        },
        {
            "title": "Rewriting generic correspondence",
            "prompt": (
                "Rewrite this generic attendance reminder in a polite and professional tone. "
                "Do not include any learner names or personal details."
            ),
            "why_it_is_safe": (
                "Improves wording of a generic template without exposing personal data."
            ),
        },
        {
            "title": "Generating discussion questions",
            "prompt": (
                "Generate five discussion questions for an adult learning group about "
                "using AI tools safely at work. Keep questions generic — do not reference "
                "any specific learners or cases."
            ),
            "why_it_is_safe": (
                "Creates generic facilitation content without including personal or "
                "case-specific details."
            ),
        },
        {
            "title": "Producing a checklist template",
            "prompt": (
                f"Create a generic checklist for reviewing a lesson plan before delivery "
                f"at {org}. Include checks for clarity, accessibility, and policy alignment. "
                f"Do not include any learner names or personal information."
            ),
            "why_it_is_safe": (
                "Generates a reusable template for internal quality review with no "
                "personal data involved."
            ),
        },
    ]

    if activities:
        for activity in activities:
            if activity.get("activity_type") == "safe_unsafe_prompt_sorting":
                cards = activity.get("scenario_cards", [])
                for card in cards:
                    if card.get("classification") == "SAFE":
                        examples.append({
                            "title": f"Activity example: {card.get('card_id', 'Card')}",
                            "prompt": card.get("prompt", ""),
                            "why_it_is_safe": card.get("reason", "No personal or sensitive data included."),
                        })
                        break

    return examples


def generate_unsafe_prompt_examples(
    scenario: dict,
    activities: list | None = None,
) -> list:
    """Return a list of unsafe prompt example dicts."""
    examples = [
        {
            "title": "Learner personal data risk",
            "prompt": (
                "Rewrite this support note for learner Sarah Ahmed, who disclosed anxiety "
                "and family problems during class."
            ),
            "why_it_is_risky": (
                "Contains identifiable learner information and sensitive personal context. "
                "Sharing this data with an external AI tool likely breaches data protection obligations."
            ),
        },
        {
            "title": "Safeguarding decision risk",
            "prompt": (
                "Decide whether this safeguarding concern about a named learner should be reported."
            ),
            "why_it_is_risky": (
                "Attempts to use AI for safeguarding judgement. Safeguarding decisions must "
                "always be made by a qualified designated safeguarding lead — never AI."
            ),
        },
        {
            "title": "HR and disciplinary information",
            "prompt": (
                "Write a disciplinary letter for a staff member based on these performance notes from their HR file."
            ),
            "why_it_is_risky": (
                "Involves confidential HR and disciplinary data. Entering staff HR records "
                "into AI tools is prohibited."
            ),
        },
        {
            "title": "Assessment decision",
            "prompt": (
                "Based on this learner's work sample, decide whether they should pass or fail the unit."
            ),
            "why_it_is_risky": (
                "AI must not make assessment or accreditation decisions. Professional judgement "
                "by a qualified assessor is required."
            ),
        },
    ]

    if activities:
        for activity in activities:
            if activity.get("activity_type") == "safe_unsafe_prompt_sorting":
                cards = activity.get("scenario_cards", [])
                for card in cards:
                    if card.get("classification") == "PROHIBITED":
                        examples.append({
                            "title": f"Activity example: {card.get('card_id', 'Card')}",
                            "prompt": card.get("prompt", ""),
                            "why_it_is_risky": card.get("reason", "Contains prohibited data or requests a prohibited decision."),
                        })
                        break

    return examples


def generate_safer_rewritten_prompt_examples(
    scenario: dict,
    activities: list | None = None,
) -> list:
    """Return a list of safer rewritten prompt example dicts."""
    examples = [
        {
            "unsafe_prompt": (
                "Rewrite this support note for learner Sarah Ahmed, who disclosed anxiety "
                "and family problems during class."
            ),
            "safer_prompt": (
                "Create a generic wellbeing signposting email template for an adult learner "
                "who may need support. Do not include names, personal details, or case-specific facts."
            ),
            "what_changed": [
                "Removed learner name.",
                "Removed sensitive personal details.",
                "Converted case-specific request into a generic reusable template.",
                "Kept the task low-risk and suitable for human review before use.",
            ],
        },
        {
            "unsafe_prompt": (
                "Decide whether this safeguarding concern about a named learner should be reported."
            ),
            "safer_prompt": (
                "Explain the general safeguarding reporting procedure for a training provider in the UK. "
                "Do not include any names, case details, or personal information."
            ),
            "what_changed": [
                "Removed named learner and case-specific details.",
                "Changed from a decision request to a general information request.",
                "Safeguarding decisions remain with the designated safeguarding lead.",
                "Output is informational only — not a substitute for professional judgement.",
            ],
        },
        {
            "unsafe_prompt": (
                "Write a disciplinary letter for a staff member based on these performance notes from their HR file."
            ),
            "safer_prompt": (
                "Create a generic template for a formal performance conversation agenda. "
                "Do not include names, personal details, or any HR case information."
            ),
            "what_changed": [
                "Removed staff name and HR case content.",
                "Converted specific disciplinary request into a generic template.",
                "HR and disciplinary decisions remain with the appropriate manager and HR lead.",
            ],
        },
    ]

    if activities:
        for activity in activities:
            if activity.get("activity_type") == "risky_prompt_rewrite":
                cards = activity.get("scenario_cards", [])
                for card in cards:
                    what_changed = card.get("what_changed", [])
                    if isinstance(what_changed, str):
                        what_changed = [what_changed]
                    examples.append({
                        "unsafe_prompt": card.get("original_prompt", ""),
                        "safer_prompt": card.get("safe_rewrite", ""),
                        "what_changed": what_changed,
                    })
                break

    return examples


def generate_human_review_checklist(
    scenario: dict,
    assessment: dict | None = None,
) -> list:
    """Return a list of human review checklist items."""
    checklist = [
        "Have I removed learner names and identifiers from anything I used as input?",
        "Have I avoided safeguarding, HR, confidential, personal, or regulated information?",
        "Is the AI output factually accurate? Have I checked key claims and statistics?",
        "Is the output fair, inclusive, and accessible for all learners and staff?",
        "Is the tone appropriate for the intended audience?",
        "Does the output align with organisational policy and sector-specific requirements?",
        "Could this output cause harm if it contains an error or misrepresentation?",
        "Does this require review by a manager, safeguarding lead, data protection lead, quality lead, HR lead, or policy owner?",
        "Am I using an approved tool for this task?",
        "Have I kept final responsibility with a human — not delegated the decision to AI?",
    ]

    if assessment:
        high_priority = [
            t.get("title", "")
            for t in assessment.get("topic_assessments", [])
            if t.get("priority_level") == "high"
        ]
        if any("hallucination" in t.lower() or "accuracy" in t.lower() for t in high_priority):
            checklist.append(
                "For any facts, statistics, or legal references: have I independently verified these — not just trusted the AI output?"
            )
        if any("bias" in t.lower() or "fairness" in t.lower() for t in high_priority):
            checklist.append(
                "Have I checked the output for bias, stereotyping, or unfair representation of any learner group?"
            )

    return checklist


def generate_escalation_guidance(
    scenario: dict,
    assessment: dict | None = None,
) -> list:
    """Return a list of escalation guidance dicts."""
    org = scenario.get("organisation_name", "your organisation")

    guidance = [
        {
            "issue": "Safeguarding concern",
            "what_to_do": (
                "Do not enter any details into an AI tool. "
                "Follow your organisation's safeguarding procedure immediately."
            ),
            "who_to_contact": f"Designated Safeguarding Lead (DSL) at {org}.",
        },
        {
            "issue": "Data protection concern",
            "what_to_do": (
                "Stop and seek advice before using AI with any personal, learner, or regulated data. "
                "Do not proceed until you have confirmed it is appropriate."
            ),
            "who_to_contact": f"Data Protection Lead, DPO, or your manager at {org}.",
        },
        {
            "issue": "AI output seems inaccurate, biased, or harmful",
            "what_to_do": (
                "Do not use the output as-is. "
                "Check key claims independently. "
                "Ask a manager or quality lead to review before it is used."
            ),
            "who_to_contact": f"Your manager or Quality Lead at {org}.",
        },
        {
            "issue": "Unsure whether an AI tool is approved for use",
            "what_to_do": (
                "Do not use the tool for work data until you have confirmed it is approved. "
                "Using unapproved tools with organisational or learner data may breach policy."
            ),
            "who_to_contact": f"Your manager or AI/policy owner at {org}.",
        },
        {
            "issue": "AI output used for a decision that affects a learner or staff member",
            "what_to_do": (
                "Ensure a qualified human has reviewed and made the final decision. "
                "AI output must not be the sole basis for professional, assessment, "
                "safeguarding, disciplinary, HR, or compliance decisions."
            ),
            "who_to_contact": f"The relevant professional lead or manager at {org}.",
        },
    ]

    return guidance


def generate_key_takeaways(
    scenario: dict,
    assessment: dict | None = None,
) -> list:
    """Return a list of key takeaway strings for the handout."""
    org = scenario.get("organisation_name", "your organisation")

    takeaways = [
        "AI is a drafting and support tool — not a decision-maker.",
        "Keep learner data, safeguarding details, HR records, and personal information out of AI tools.",
        "Review everything AI produces before you use it.",
        "Use approved tools only. If you're unsure, ask before using.",
        "Escalate safeguarding and data protection concerns to the right human — do not involve AI.",
        f"Keep final responsibility with a human at {org} — not with the AI system.",
        "Safe AI use protects learners, staff, and the organisation.",
    ]

    if assessment:
        high_priority = [
            t.get("title", "")
            for t in assessment.get("topic_assessments", [])
            if t.get("priority_level") == "high"
        ]
        if any("hallucination" in t.lower() or "accuracy" in t.lower() for t in high_priority):
            takeaways.append(
                "Check AI output for hallucinations — invented facts, statistics, or legal references that sound plausible but are wrong."
            )
        if any("bias" in t.lower() or "fairness" in t.lower() for t in high_priority):
            takeaways.append(
                "Check AI output for bias and unfair representation before using it with or about learners."
            )

    return takeaways


def generate_staff_handout(
    scenario: dict,
    assessment: dict | None = None,
    workshop_plan: dict | None = None,
    activities: list | None = None,
    facilitator_guide: dict | None = None,
) -> dict:
    """Generate and return a complete staff handout dict."""
    if scenario is None:
        scenario = {}

    org = scenario.get("organisation_name", "Unnamed organisation")
    audience = scenario.get("staff_roles", ["All staff"])
    if not audience:
        audience = ["All staff"]

    purpose_lines = [
        f"This handout is a quick reference guide for staff at {org} on using AI tools safely and responsibly.",
        "It covers what you can and cannot do with AI at work, how to write safe prompts, "
        "what to check before using AI output, and who to contact if you are unsure.",
        "All examples in this handout are synthetic — they do not contain real learner, safeguarding, or personal data.",
    ]
    if workshop_plan:
        purpose_lines.append(
            f"This handout supports the '{workshop_plan.get('workshop_title', 'Responsible AI Workshop')}'."
        )

    purpose = " ".join(purpose_lines)

    return {
        "handout_title": f"Staff Handout: Using AI Safely at {org}",
        "organisation_name": org,
        "audience": audience,
        "purpose": purpose,
        "safe_use_principles": get_default_safe_use_principles(),
        "allowed_ai_uses": generate_allowed_ai_uses(scenario, assessment),
        "prohibited_ai_uses": generate_prohibited_ai_uses(scenario, assessment),
        "safe_prompt_examples": generate_safe_prompt_examples(scenario, activities),
        "unsafe_prompt_examples": generate_unsafe_prompt_examples(scenario, activities),
        "safer_rewritten_prompt_examples": generate_safer_rewritten_prompt_examples(scenario, activities),
        "human_review_checklist": generate_human_review_checklist(scenario, assessment),
        "escalation_guidance": generate_escalation_guidance(scenario, assessment),
        "key_takeaways": generate_key_takeaways(scenario, assessment),
        "responsible_use_warning": _RESPONSIBLE_USE_WARNING,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def summarise_staff_handout(handout: dict) -> dict:
    """Return a compact summary dict for the staff handout."""
    return {
        "organisation_name": handout.get("organisation_name", ""),
        "audience_roles": handout.get("audience", []),
        "safe_prompt_count": len(handout.get("safe_prompt_examples", [])),
        "unsafe_prompt_count": len(handout.get("unsafe_prompt_examples", [])),
        "safer_rewrite_count": len(handout.get("safer_rewritten_prompt_examples", [])),
        "checklist_item_count": len(handout.get("human_review_checklist", [])),
        "escalation_item_count": len(handout.get("escalation_guidance", [])),
        "key_takeaway_count": len(handout.get("key_takeaways", [])),
    }


def format_staff_handout_as_markdown(handout: dict) -> str:
    """Return the staff handout formatted as a Markdown string."""
    lines = []

    lines.append("# Responsible AI Staff Handout")
    lines.append("")

    # Organisation
    lines.append("## Organisation")
    lines.append("")
    lines.append(f"**{handout.get('organisation_name', 'Unnamed organisation')}**")
    audience = handout.get("audience", [])
    if audience:
        lines.append(f"**Audience:** {', '.join(audience)}")
    lines.append("")

    # Purpose
    lines.append("## Purpose")
    lines.append("")
    lines.append(handout.get("purpose", ""))
    lines.append("")

    # Safe-use principles
    lines.append("## Safe-Use Principles")
    lines.append("")
    for principle in handout.get("safe_use_principles", []):
        lines.append(f"- {principle}")
    lines.append("")

    # Allowed uses
    lines.append("## What Staff Can Use AI For")
    lines.append("")
    for use in handout.get("allowed_ai_uses", []):
        lines.append(f"- {use}")
    lines.append("")

    # Prohibited uses
    lines.append("## What Staff Must Not Use AI For")
    lines.append("")
    for use in handout.get("prohibited_ai_uses", []):
        lines.append(f"- {use}")
    lines.append("")

    # Safe prompts
    lines.append("## Safe Prompt Examples")
    lines.append("")
    for ex in handout.get("safe_prompt_examples", []):
        lines.append(f"### {ex.get('title', 'Example')}")
        lines.append("")
        lines.append(f"**Prompt:** {ex.get('prompt', '')}")
        lines.append("")
        lines.append(f"**Why it is safe:** {ex.get('why_it_is_safe', '')}")
        lines.append("")

    # Unsafe prompts
    lines.append("## Unsafe Prompt Examples")
    lines.append("")
    for ex in handout.get("unsafe_prompt_examples", []):
        lines.append(f"### {ex.get('title', 'Example')}")
        lines.append("")
        lines.append(f"**Prompt:** {ex.get('prompt', '')}")
        lines.append("")
        lines.append(f"**Why it is risky:** {ex.get('why_it_is_risky', '')}")
        lines.append("")

    # Safer rewrites
    lines.append("## Safer Rewritten Prompt Examples")
    lines.append("")
    for i, ex in enumerate(handout.get("safer_rewritten_prompt_examples", []), 1):
        lines.append(f"### Example {i}")
        lines.append("")
        lines.append(f"**Unsafe prompt:** {ex.get('unsafe_prompt', '')}")
        lines.append("")
        lines.append(f"**Safer prompt:** {ex.get('safer_prompt', '')}")
        lines.append("")
        what_changed = ex.get("what_changed", [])
        if what_changed:
            lines.append("**What changed:**")
            for change in what_changed:
                lines.append(f"- {change}")
        lines.append("")

    # Human review checklist
    lines.append("## Human Review Checklist")
    lines.append("")
    lines.append("Before using any AI output, check:")
    lines.append("")
    for item in handout.get("human_review_checklist", []):
        lines.append(f"- [ ] {item}")
    lines.append("")

    # Escalation guidance
    lines.append("## Escalation Guidance")
    lines.append("")
    for item in handout.get("escalation_guidance", []):
        lines.append(f"### {item.get('issue', 'Issue')}")
        lines.append("")
        lines.append(f"**What to do:** {item.get('what_to_do', '')}")
        lines.append("")
        lines.append(f"**Who to contact:** {item.get('who_to_contact', '')}")
        lines.append("")

    # Key takeaways
    lines.append("## Key Takeaways")
    lines.append("")
    for takeaway in handout.get("key_takeaways", []):
        lines.append(f"- {takeaway}")
    lines.append("")

    # Prototype and responsible-use boundaries
    lines.append("## Prototype and Responsible-Use Boundaries")
    lines.append("")
    lines.append(f"> {handout.get('responsible_use_warning', '')}")
    lines.append("")
    lines.append(handout.get("prototype_note", ""))
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)


def create_staff_handout_filename(organisation_name: str) -> str:
    """Return a safe kebab-case filename for the staff handout."""
    if not organisation_name:
        organisation_name = "organisation"
    slug = organisation_name.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return f"staff-handout-{slug}.md"
