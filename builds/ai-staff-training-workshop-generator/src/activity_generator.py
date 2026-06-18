"""Activity generator for the AI Staff Training and Workshop Generator.

Phase 4: generates practical responsible AI workshop activities from a synthetic
organisation scenario. All content is deterministic and template-based — no
external AI API calls.
"""

import re

# ── Responsible-use note ────────────────────────────────────────────────────────

_RESPONSIBLE_USE_NOTE = (
    "These activities must only be used with synthetic or approved scenarios. "
    "Do not use real learner names, identifiable learner details, safeguarding "
    "case information, confidential client records, staff HR data, personal data, "
    "or regulated information. Human review is required before use in a real training "
    "session. This prototype does not provide legal, safeguarding, HR, compliance, "
    "medical, financial, or professional advice."
)

_RISK_WARNINGS = [
    "Do not use real learner names or identifiable learner details.",
    "Do not include safeguarding case information in prompts or activity materials.",
    "Do not include confidential client records or staff HR data.",
    "Do not treat AI output as final authority — human review remains required.",
    "Escalate safeguarding, data protection, accuracy, or policy concerns to the appropriate human owner.",
    "All scenario cards in this activity use synthetic, fictional examples only.",
]

# ── Activity type catalogue ─────────────────────────────────────────────────────

def get_activity_type_catalogue() -> dict:
    """Return a catalogue of available activity types with metadata."""
    return {
        "safe_unsafe_prompt_sorting": {
            "title": "Safe vs Unsafe Prompt Sorting",
            "type": "sorting",
            "recommended_duration": 10,
            "description": "Staff classify prompts as safe, risky, or prohibited.",
        },
        "risky_prompt_rewrite": {
            "title": "Rewrite a Risky Prompt Safely",
            "type": "rewrite",
            "recommended_duration": 15,
            "description": (
                "Staff practise removing identifiers and converting risky prompts "
                "into safer synthetic prompts."
            ),
        },
        "hallucination_review": {
            "title": "Spot the Hallucination",
            "type": "review",
            "recommended_duration": 10,
            "description": (
                "Staff review an AI output for invented, unsupported, or inaccurate claims."
            ),
        },
        "learner_data_boundary": {
            "title": "Learner Data Boundary Scenario",
            "type": "scenario",
            "recommended_duration": 10,
            "description": (
                "Staff decide what learner information must not be entered into AI tools."
            ),
        },
        "safeguarding_escalation": {
            "title": "Safeguarding Escalation Scenario",
            "type": "scenario",
            "recommended_duration": 10,
            "description": (
                "Staff practise keeping safeguarding concerns human-led and escalating appropriately."
            ),
        },
        "human_review_checklist": {
            "title": "Human Review Checklist",
            "type": "checklist",
            "recommended_duration": 10,
            "description": (
                "Staff build or apply a review checklist before using AI-assisted outputs."
            ),
        },
        "approved_tools_decision": {
            "title": "Approved Tools Decision Activity",
            "type": "decision",
            "recommended_duration": 10,
            "description": (
                "Staff decide whether a proposed AI use should use approved systems, "
                "be escalated, or be stopped."
            ),
        },
        "bias_fairness_review": {
            "title": "Bias and Fairness Review",
            "type": "review",
            "recommended_duration": 10,
            "description": (
                "Staff examine AI output for unfair assumptions, accessibility issues, "
                "or biased wording."
            ),
        },
    }


def get_default_activity_types() -> list:
    """Return the default set of activity types for the BrightPath demo."""
    return [
        "safe_unsafe_prompt_sorting",
        "risky_prompt_rewrite",
        "hallucination_review",
        "learner_data_boundary",
        "safeguarding_escalation",
        "human_review_checklist",
    ]


# ── Internal helpers ────────────────────────────────────────────────────────────

def _get_org(scenario: dict) -> str:
    return scenario.get("organisation_name") or "Unnamed organisation"


def _get_sector(scenario: dict) -> str:
    return scenario.get("sector") or "education and training"


def _get_roles(scenario: dict) -> list:
    roles = scenario.get("staff_roles") or []
    return roles if roles else ["staff"]


# ── Individual activity creators ────────────────────────────────────────────────

def create_safe_unsafe_prompt_sorting_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a safe vs unsafe prompt sorting activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "A",
            "prompt": (
                "Create a 30-minute introductory lesson outline on workplace communication "
                "for adult learners. Do not include learner names or personal details."
            ),
            "classification": "SAFE",
            "reason": (
                "Generic, synthetic task with no personal data and an explicit instruction "
                "to exclude identifying details."
            ),
        },
        {
            "card_id": "B",
            "prompt": (
                "Summarise the key points from this policy document for a staff briefing. "
                "[paste anonymised policy text]"
            ),
            "classification": "SAFE",
            "reason": (
                "Policy summarisation using anonymised, non-personal content is "
                "generally acceptable with an approved tool."
            ),
        },
        {
            "card_id": "C",
            "prompt": (
                f"Rewrite this support note for learner Sarah Ahmed, who disclosed anxiety "
                f"and family problems during class."
            ),
            "classification": "RISKY",
            "reason": (
                "Contains a real learner name and sensitive personal disclosure. "
                "Must be anonymised before using any AI tool."
            ),
        },
        {
            "card_id": "D",
            "prompt": (
                "Write a personalised assessment feedback letter for Learner ID #4721 "
                "who achieved 62% and has attendance concerns."
            ),
            "classification": "RISKY",
            "reason": (
                "Learner ID and performance data are personal data. "
                "This requires anonymisation and DPO guidance before AI use."
            ),
        },
        {
            "card_id": "E",
            "prompt": (
                "Decide whether this safeguarding concern about a named learner "
                "should be reported to the local authority."
            ),
            "classification": "PROHIBITED",
            "reason": (
                "Safeguarding decisions must never be delegated to AI tools. "
                "Follow the organisation's safeguarding procedure and escalate "
                "to the safeguarding lead."
            ),
        },
        {
            "card_id": "F",
            "prompt": (
                "Generate a report on which staff members had poor punctuality "
                "last quarter and suggest performance improvement actions."
            ),
            "classification": "PROHIBITED",
            "reason": (
                "HR and performance data about named staff is confidential. "
                "AI tools must not be used for staff performance decisions."
            ),
        },
    ]

    return {
        "activity_id": "safe_unsafe_prompt_sorting",
        "activity_title": "Safe vs Unsafe Prompt Sorting",
        "activity_type": "sorting",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can distinguish safe AI prompts from risky or prohibited "
            f"ones in a {sector} context and explain their reasoning."
        ),
        "materials_needed": [
            "Printed or digital prompt cards (A–F)",
            "Three sorting labels: SAFE / RISKY / PROHIBITED",
            "Flipchart or whiteboard for group discussion",
        ],
        "instructions_for_trainer": [
            "Distribute prompt cards A–F to pairs or small groups.",
            "Ask participants to sort each card into SAFE, RISKY, or PROHIBITED.",
            "Give groups 5 minutes to sort and discuss their reasoning.",
            "Debrief by revealing the expected classifications and reasons.",
            "Emphasise that 'risky' prompts can often be made safe through anonymisation — but some decisions must never go to AI.",
        ],
        "instructions_for_participants": [
            "Read each prompt card carefully.",
            "Decide: is this prompt SAFE to use with an AI tool, RISKY (needs changes), or PROHIBITED (must not be used)?",
            "Note your reasoning — be ready to explain your classification.",
            "Discuss your choices with your partner or group.",
        ],
        "activity_steps": [
            "Step 1 (2 min): Trainer hands out prompt cards.",
            "Step 2 (5 min): Pairs or groups classify each card as SAFE, RISKY, or PROHIBITED.",
            "Step 3 (3 min): Trainer reveals classifications and leads brief discussion on cards C–F.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "A — SAFE: Generic, anonymised, no personal data.",
            "B — SAFE: Anonymised policy content, appropriate use.",
            "C — RISKY: Contains learner name and sensitive personal disclosure.",
            "D — RISKY: Learner ID and performance data require DPO guidance.",
            "E — PROHIBITED: Safeguarding decisions must be human-led.",
            "F — PROHIBITED: Staff HR data must not go into AI tools.",
        ],
        "debrief_questions": [
            f"Which card surprised you most? Why?",
            "What is the difference between 'risky' and 'prohibited'?",
            f"How would you rewrite card C so it could be used safely with an approved tool?",
            f"What should a {sector.split()[0]} staff member do if they're unsure whether a prompt is safe?",
        ],
        "key_takeaways": [
            "Some AI prompts are safe as written. Others need anonymisation before use.",
            "Safeguarding and HR decisions must never be delegated to AI.",
            "When in doubt, ask your line manager or data protection contact before using AI.",
            "Anonymisation means removing names, IDs, and any details that could identify a real person.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_risky_prompt_rewrite_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a risky prompt rewrite activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "R1",
            "original_prompt": (
                "Write a progress report for learner James Osei (learner ID 8834) "
                "who scored 58% in his last assessment and has been flagged for "
                "additional support due to personal circumstances."
            ),
            "problem": "Contains a real-sounding name, learner ID, performance data, and reference to personal circumstances.",
            "safe_rewrite": (
                "Write a progress report template for an adult learner who achieved "
                "below 65% in their most recent assessment and has been identified as "
                "benefiting from additional support. Do not include names, IDs, or "
                "personal details."
            ),
            "what_changed": [
                "Removed learner name.",
                "Removed learner ID.",
                "Replaced specific score with a generalised band.",
                "Replaced 'personal circumstances' with a generic support need.",
                "Added explicit instruction to exclude personal details.",
            ],
        },
        {
            "card_id": "R2",
            "original_prompt": (
                "Help me write a class observation report about tutor Priya Sharma "
                "whose delivery was poor and who was observed using her phone during class."
            ),
            "problem": "Contains a staff member's name and performance judgement — this is HR data.",
            "safe_rewrite": (
                "Generate a class observation report template for a situation where "
                "a trainer's delivery did not meet expected standards and professional "
                "conduct concerns were noted. Do not include any staff names or "
                "identifying details."
            ),
            "what_changed": [
                "Removed staff member's name.",
                "Generalised the performance observation.",
                "Removed the specific behaviour detail that could identify the individual.",
                "Added instruction to exclude identifying details.",
            ],
        },
    ]

    return {
        "activity_id": "risky_prompt_rewrite",
        "activity_title": "Rewrite a Risky Prompt Safely",
        "activity_type": "rewrite",
        "duration_minutes": 15,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can identify identifying or sensitive details in a "
            f"prompt and rewrite it so it can be used safely with an approved AI tool."
        ),
        "materials_needed": [
            "Printed or digital scenario cards R1 and R2",
            "Pen/paper or digital notes",
            "Approved AI tool (optional — for live practice if time allows)",
        ],
        "instructions_for_trainer": [
            "Distribute scenario cards R1 and R2.",
            "Ask participants to identify what makes each prompt risky.",
            "Ask them to write a safer version of each prompt.",
            "After 8 minutes, share the suggested safe rewrites.",
            "Emphasise the key technique: generalise, anonymise, and add explicit no-personal-data instructions.",
            "Optional: if an approved AI tool is available, try the rewritten prompts live.",
        ],
        "instructions_for_participants": [
            "Read the original prompt on each card.",
            "Identify what makes it risky: names? IDs? personal circumstances? HR data?",
            "Rewrite the prompt so it removes all identifying details and could safely be used with an approved tool.",
            "Compare your rewrite to the suggested safe version.",
        ],
        "activity_steps": [
            "Step 1 (2 min): Trainer explains the task.",
            "Step 2 (8 min): Participants rewrite both prompts.",
            "Step 3 (5 min): Trainer shares suggested rewrites and leads discussion on what changed.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "R1 — Remove name, ID, specific score, and personal circumstances reference. Generalise to a template.",
            "R2 — Remove staff name. Generalise the performance concern. Add explicit no-identifying-details instruction.",
        ],
        "debrief_questions": [
            "What is the first thing you check before using a prompt with an AI tool?",
            "Is it ever acceptable to include a learner's name in a prompt? In what circumstances?",
            "What would you do if you received an AI-generated output that contained a real person's name?",
            f"What is your organisation's approved AI tool for tasks like these?",
        ],
        "key_takeaways": [
            "Remove names, IDs, and personal details before using AI — every time.",
            "Generalise specific situations into templates. The AI output is then a starting point, not a final document.",
            "Always add: 'Do not include names, personal details, or identifying information' to prompts that touch sensitive topics.",
            "If you cannot anonymise a prompt sufficiently, do not use AI for that task.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_hallucination_review_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a hallucination review activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "H1",
            "ai_output": (
                "This lesson plan is guaranteed to meet all Ofsted requirements and will "
                "improve learner achievement by 40%. Research from the Department for "
                "Education (2024) confirms that AI-assisted lesson planning consistently "
                "outperforms traditional methods in FE settings. The plan includes all "
                "mandatory safeguarding indicators as required by the 2023 Education Act."
            ),
            "hallucination_flags": [
                "'Guaranteed to meet all Ofsted requirements' — AI cannot guarantee regulatory compliance.",
                "'Will improve learner achievement by 40%' — invented statistic with no evidence.",
                "'Department for Education (2024) research' — this citation may not exist; verify before using.",
                "'2023 Education Act' — check whether this Act exists and whether it contains what is claimed.",
            ],
            "what_to_do": [
                "Remove all guarantee language — replace with 'designed to support' or 'may assist with'.",
                "Remove the 40% improvement claim entirely — it is unsupported.",
                "Verify any research citations before including them in materials.",
                "Verify any legal references with the relevant policy owner.",
                "Ask a responsible human to review before using the output.",
            ],
        },
        {
            "card_id": "H2",
            "ai_output": (
                "Under the UK GDPR, organisations are required to seek learner consent "
                "before any data processing. Failure to do so carries a mandatory fine "
                "of £500 per learner record. Your DPO must countersign all AI-generated "
                "communications before they are sent."
            ),
            "hallucination_flags": [
                "UK GDPR does not require consent for all data processing — there are six lawful bases.",
                "There is no mandatory £500 per-learner-record fine — fine structures are complex and context-dependent.",
                "DPO countersigning all AI communications is not a universal legal requirement.",
            ],
            "what_to_do": [
                "Do not share AI-generated legal or compliance information without verification.",
                "Refer to your DPO or legal team for UK GDPR obligations.",
                "Remove or flag all compliance claims before using the output.",
            ],
        },
    ]

    return {
        "activity_id": "hallucination_review",
        "activity_title": "Spot the Hallucination",
        "activity_type": "review",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can identify invented, unsupported, or inaccurate claims "
            f"in an AI output and understand why human review is always required before "
            f"using AI-generated content."
        ),
        "materials_needed": [
            "Printed or digital scenario cards H1 and H2",
            "Highlighter pens or digital annotation",
        ],
        "instructions_for_trainer": [
            "Distribute scenario cards H1 and H2.",
            "Ask participants to highlight any claims that seem invented, unsupported, or unverifiable.",
            "After 5 minutes, reveal the hallucination flags for each output.",
            "Emphasise: AI can produce confident-sounding output that is factually wrong.",
            "Remind participants: all AI output must be reviewed by a responsible human before use.",
        ],
        "instructions_for_participants": [
            "Read the AI output on each card.",
            "Highlight any claims that seem invented, guaranteed, or would need independent verification.",
            "Write down what you would do before using this output.",
        ],
        "activity_steps": [
            "Step 1 (1 min): Trainer introduces the task.",
            "Step 2 (5 min): Participants review and highlight both cards.",
            "Step 3 (4 min): Trainer reveals flags and leads discussion.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "H1 — Flag: guarantee of Ofsted compliance, 40% improvement statistic, unverified DfE citation, unverified Education Act reference.",
            "H2 — Flag: incorrect description of UK GDPR consent, invented fine amount, unverified DPO requirement.",
        ],
        "debrief_questions": [
            "Why does AI produce confident-sounding incorrect information?",
            "What is the cost of using unchecked AI output in a regulatory context?",
            "What would your review process look like before sharing AI-generated content with learners?",
            "Who in your organisation is the responsible owner for policy and compliance claims?",
        ],
        "key_takeaways": [
            "AI generates plausible-sounding text — it does not check facts.",
            "Regulatory, legal, and statistical claims must always be independently verified.",
            "Never share AI output with learners or external stakeholders without human review.",
            "The cost of a hallucination in a safeguarding, compliance, or legal context can be serious.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_learner_data_boundary_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a learner data boundary scenario activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "L1",
            "situation": (
                "A tutor wants to ask an AI tool to summarise a learner's ILP "
                "(Individual Learning Plan) so they can write a quick progress note."
            ),
            "what_not_to_do": "Paste the actual ILP into an AI tool — it contains personal data.",
            "what_to_do": (
                "Write a summary note manually using your knowledge of the learner, "
                "or create a template using anonymised, fictional details."
            ),
            "boundary_rule": "Individual learning plans contain personal data and must not be entered into AI tools.",
        },
        {
            "card_id": "L2",
            "situation": (
                "An administrator needs to draft a letter to parents about a group of "
                "learners who have low attendance. She has a spreadsheet with learner "
                "names and attendance percentages."
            ),
            "what_not_to_do": "Upload the spreadsheet or paste learner names and percentages into an AI tool.",
            "what_to_do": (
                "Ask AI to generate a template attendance letter for parents. "
                "Then fill in the learner details manually."
            ),
            "boundary_rule": "Learner names and attendance data are personal data. Use AI to generate templates only.",
        },
        {
            "card_id": "L3",
            "situation": (
                "A team leader wants to use AI to analyse which learner groups are "
                "underperforming by pasting a results table into a prompt."
            ),
            "what_not_to_do": "Paste identifiable learner results into an AI tool.",
            "what_to_do": (
                "Aggregate and anonymise data before analysis. "
                "For example: 'Group A: 12 learners, average 58%, lowest 34%.' "
                "No individual names or IDs."
            ),
            "boundary_rule": "Aggregate and anonymise before AI analysis. Never include individual learner identifiers.",
        },
    ]

    return {
        "activity_id": "learner_data_boundary",
        "activity_title": "Learner Data Boundary Scenario",
        "activity_type": "scenario",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can identify which types of learner information must not "
            f"be entered into AI tools and know what to do instead."
        ),
        "materials_needed": [
            "Printed or digital scenario cards L1, L2, L3",
            "Organisation's data protection or AI use policy (if available)",
        ],
        "instructions_for_trainer": [
            "Distribute scenario cards L1–L3.",
            "Ask participants to identify: what is the boundary being crossed and what should the staff member do instead?",
            "After 5 minutes, discuss each card.",
            "Connect to the organisation's data protection policy and DPO contact.",
            "Remind participants: if in doubt, do not paste it in — ask your DPO.",
        ],
        "instructions_for_participants": [
            "Read each scenario.",
            "Identify: what personal data is at risk?",
            "Decide: what should the staff member do instead?",
            "Be ready to explain the boundary rule for each scenario.",
        ],
        "activity_steps": [
            "Step 1 (1 min): Trainer introduces the boundary principle.",
            "Step 2 (5 min): Participants work through all three scenarios.",
            "Step 3 (4 min): Trainer debriefs each card and shares the boundary rules.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "L1 — Do not paste ILP into AI. Write the note manually or use an anonymised template.",
            "L2 — Do not paste names and attendance data. Use AI for the template; fill in details manually.",
            "L3 — Do not paste identifiable results. Aggregate and anonymise first.",
        ],
        "debrief_questions": [
            "What types of learner information are you currently recording digitally?",
            "Which of those would be personal data under UK GDPR?",
            "What is the 'template approach' and why is it safer?",
            "Who is your organisation's data protection contact or DPO?",
        ],
        "key_takeaways": [
            "Learner names, IDs, results, ILPs, and attendance data are personal data.",
            "The template approach: use AI to generate a generic template, then fill in the real details manually.",
            "Aggregate data before AI analysis — remove individual identifiers.",
            "When in doubt, check with your DPO before using AI for any learner-data task.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_safeguarding_escalation_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a safeguarding escalation scenario activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "S1",
            "situation": (
                "A tutor is concerned about a learner's wellbeing after a difficult "
                "conversation. The tutor is unsure what to do and thinks they could "
                "use ChatGPT to help decide whether this counts as a safeguarding concern."
            ),
            "wrong_action": "Paste the concern into ChatGPT and ask it to advise on next steps.",
            "correct_action": (
                "Follow the organisation's safeguarding procedure. "
                "Contact the Designated Safeguarding Lead (DSL) immediately. "
                "Do not enter case details, learner details, or your concerns into any AI tool."
            ),
            "why": (
                "Safeguarding decisions are human judgements with legal accountability. "
                "AI cannot hold that accountability. Safeguarding case information is "
                "highly sensitive personal data that must never go into AI tools."
            ),
        },
        {
            "card_id": "S2",
            "situation": (
                "An administrator receives a concerning message from a learner by email "
                "and thinks it might relate to a safeguarding issue. They copy the email "
                "into an AI tool to ask whether they need to report it."
            ),
            "wrong_action": "Copy the email into an AI tool.",
            "correct_action": (
                "Do not enter the email content into any AI tool. "
                "Contact the DSL directly. Report your concern using the organisation's "
                "safeguarding referral process."
            ),
            "why": (
                "Even if the concern turns out to be minor, safeguarding case information "
                "must always be handled by trained, accountable humans — never by AI."
            ),
        },
    ]

    return {
        "activity_id": "safeguarding_escalation",
        "activity_title": "Safeguarding Escalation Scenario",
        "activity_type": "scenario",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can recognise when a safeguarding concern arises, "
            f"understand why AI must not be used in safeguarding decisions, "
            f"and know the correct escalation path."
        ),
        "materials_needed": [
            "Printed or digital scenario cards S1 and S2",
            "Organisation's safeguarding policy and DSL contact details",
        ],
        "instructions_for_trainer": [
            "Distribute scenario cards S1 and S2.",
            "Ask participants: what should the staff member do, and what must they not do?",
            "After 5 minutes, reveal the correct actions.",
            "Confirm the DSL name and escalation route for your organisation.",
            "Emphasise: safeguarding decisions must always be human-led. There are no exceptions.",
        ],
        "instructions_for_participants": [
            "Read each scenario.",
            "Decide: what should the staff member do? What must they not do?",
            "Be ready to name the correct escalation route.",
        ],
        "activity_steps": [
            "Step 1 (1 min): Trainer introduces the safeguarding principle.",
            "Step 2 (5 min): Pairs work through both scenarios.",
            "Step 3 (4 min): Trainer reveals answers and confirms DSL escalation route.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "S1 — Do not use AI. Follow safeguarding procedure. Contact DSL immediately.",
            "S2 — Do not copy email into AI. Contact DSL. Use the safeguarding referral process.",
        ],
        "debrief_questions": [
            "Why can AI never be used to make safeguarding decisions?",
            "Who is your Designated Safeguarding Lead?",
            "What is the first thing you would do if a learner disclosed something concerning?",
            "What happens if you are unsure whether something is a safeguarding concern?",
        ],
        "key_takeaways": [
            "Safeguarding decisions must always be human-led. No exceptions.",
            "Never enter safeguarding case information, learner disclosures, or concern details into any AI tool.",
            "The correct action is always: contact your Designated Safeguarding Lead.",
            "If unsure whether something is a safeguarding concern, escalate anyway — the DSL will decide.",
        ],
        "risk_warnings": _RISK_WARNINGS + [
            "This activity uses synthetic scenarios only. Do not use real safeguarding case details.",
        ],
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_human_review_checklist_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a human review checklist activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    checklist_items = [
        {
            "item_id": "1",
            "check": "Is this output factually accurate?",
            "guidance": "Verify any claims, statistics, citations, or policy references against authoritative sources.",
        },
        {
            "item_id": "2",
            "check": "Does this output contain any personal data?",
            "guidance": "Check for names, IDs, contact details, or any information that could identify a real person.",
        },
        {
            "item_id": "3",
            "check": "Does this output contain any safeguarding-related content?",
            "guidance": "If yes, do not use this output. Refer to your safeguarding lead.",
        },
        {
            "item_id": "4",
            "check": "Does this output contain legal, compliance, or regulatory claims?",
            "guidance": "If yes, verify with your DPO, legal team, or relevant policy owner before sharing.",
        },
        {
            "item_id": "5",
            "check": "Is this output appropriate for the audience?",
            "guidance": "Review tone, reading level, and cultural appropriateness for your learner group.",
        },
        {
            "item_id": "6",
            "check": "Does this output contain any bias or unfair assumptions?",
            "guidance": "Check for assumptions about gender, age, ethnicity, disability, or other protected characteristics.",
        },
        {
            "item_id": "7",
            "check": "Was this output generated by an approved AI tool?",
            "guidance": "Check your organisation's approved tool list before using any AI output in a work context.",
        },
        {
            "item_id": "8",
            "check": "Have I added my own professional judgement?",
            "guidance": "AI output is a draft starting point. You are the responsible human. Apply your expertise.",
        },
    ]

    scenario_cards = [
        {
            "card_id": "C1",
            "task": (
                "A tutor has used an AI tool to draft a letter to a learner explaining "
                "why they have been withdrawn from their programme due to attendance. "
                "Apply the human review checklist before sharing the letter."
            ),
            "key_checks": [
                "Check 1: Are the facts about the learner's attendance correct?",
                "Check 2: Does the letter contain the learner's name or personal details?",
                "Check 3: Is the tone appropriate and respectful?",
                "Check 4: Does the letter reference any policies or regulations that need verification?",
                "Check 8: Have you reviewed and personalised the letter yourself?",
            ],
        }
    ]

    return {
        "activity_id": "human_review_checklist",
        "activity_title": "Human Review Checklist",
        "activity_type": "checklist",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can apply a structured human review checklist to any "
            f"AI-generated output before using it in a work context."
        ),
        "materials_needed": [
            "Printed or digital human review checklist (8 items)",
            "Scenario card C1",
        ],
        "instructions_for_trainer": [
            "Share the human review checklist with participants.",
            "Walk through each item briefly (2 min).",
            "Distribute scenario card C1.",
            "Ask participants to apply the checklist to the scenario — which checks would they fail?",
            "Debrief: which checks are most critical in a training and education context?",
        ],
        "instructions_for_participants": [
            "Read the 8-item human review checklist.",
            "Read scenario card C1.",
            "Apply the checklist: which checks would the letter likely fail?",
            "What would you do before sending the letter?",
        ],
        "activity_steps": [
            "Step 1 (2 min): Trainer walks through the checklist.",
            "Step 2 (5 min): Participants apply the checklist to scenario C1.",
            "Step 3 (3 min): Trainer debriefs.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "C1 — Check 1: Verify attendance facts against records.",
            "C1 — Check 2: Confirm the letter contains the correct learner name (personal data — handled by staff, not AI).",
            "C1 — Check 3: Review tone — is it respectful and appropriate?",
            "C1 — Check 4: Verify any policy or regulatory references.",
            "C1 — Check 8: Personalise and apply professional judgement before sending.",
        ],
        "debrief_questions": [
            "Which checklist item do you think staff are most likely to skip?",
            "What is the risk of sending an AI-generated letter without any human review?",
            "How would you embed this checklist into your team's normal workflow?",
            "What should a staff member do if they fail multiple checks?",
        ],
        "key_takeaways": [
            "Human review is not optional — it is the final step before any AI output is used.",
            "The checklist is a practical tool, not a bureaucratic box-tick.",
            "AI output is a draft starting point. You are the responsible human.",
            "When in doubt, do not send. Ask a colleague or line manager to review.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_approved_tools_decision_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return an approved tools decision activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "T1",
            "proposed_use": "Use a free online AI tool to summarise a funding application.",
            "decision": "ESCALATE",
            "reason": (
                "Funding applications may contain commercially sensitive or confidential "
                "organisational information. Use approved tools only; escalate if unsure."
            ),
        },
        {
            "card_id": "T2",
            "proposed_use": "Use the organisation's approved AI writing tool to draft a generic welcome email for new learners.",
            "decision": "APPROVED",
            "reason": (
                "Generic, non-personal communication using an approved tool is "
                "acceptable. Review the output before sending."
            ),
        },
        {
            "card_id": "T3",
            "proposed_use": "Use an AI tool found online to analyse learner feedback survey responses.",
            "decision": "STOP",
            "reason": (
                "Survey responses may contain personal data or sensitive learner comments. "
                "Do not use unapproved tools for learner data. Escalate to your DPO."
            ),
        },
        {
            "card_id": "T4",
            "proposed_use": "Use an AI image generator to create a decorative banner for a course brochure.",
            "decision": "ESCALATE",
            "reason": (
                "Image generation has copyright and intellectual property implications. "
                "Check with your manager and review the organisation's AI policy before use."
            ),
        },
    ]

    return {
        "activity_id": "approved_tools_decision",
        "activity_title": "Approved Tools Decision Activity",
        "activity_type": "decision",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can apply a consistent decision process to determine "
            f"whether a proposed AI use should be approved, escalated, or stopped."
        ),
        "materials_needed": [
            "Printed or digital scenario cards T1–T4",
            "Organisation's approved AI tools list (if available)",
            "Three decision cards: APPROVED / ESCALATE / STOP",
        ],
        "instructions_for_trainer": [
            "Distribute scenario cards T1–T4.",
            "Ask participants to classify each proposed use as APPROVED, ESCALATE, or STOP.",
            "After 5 minutes, reveal the expected decisions and reasoning.",
            "Share the organisation's actual approved tools list if available.",
            "Remind participants: using an unapproved tool is a policy breach, not just a mistake.",
        ],
        "instructions_for_participants": [
            "Read each proposed AI use.",
            "Decide: APPROVED (safe to proceed with approved tool), ESCALATE (need guidance), or STOP (must not proceed)?",
            "Note your reasoning for each decision.",
        ],
        "activity_steps": [
            "Step 1 (1 min): Trainer explains the three decisions.",
            "Step 2 (5 min): Participants classify all four scenarios.",
            "Step 3 (4 min): Trainer reveals decisions and discusses the approved tools list.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "T1 — ESCALATE: Confidential information, unapproved tool. Check before proceeding.",
            "T2 — APPROVED: Approved tool, generic non-personal content.",
            "T3 — STOP: Learner data, unapproved tool.",
            "T4 — ESCALATE: Copyright and IP concerns. Check policy first.",
        ],
        "debrief_questions": [
            "What AI tools are currently approved by your organisation?",
            "What should you do if you want to use an AI tool that is not on the approved list?",
            "What is the risk of using a free AI tool for work tasks?",
            "Who do you escalate to when you are unsure about an approved tools decision?",
        ],
        "key_takeaways": [
            "Only use AI tools approved by your organisation for work tasks.",
            "Free online AI tools are not automatically approved — their data handling may not meet your obligations.",
            "When unsure: ESCALATE to your line manager or DPO, not STOP entirely.",
            "The approved tools list exists to protect the organisation, learners, and you.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


def create_bias_fairness_review_activity(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
) -> dict:
    """Return a bias and fairness review activity dict."""
    org = _get_org(scenario)
    sector = _get_sector(scenario)
    roles = _get_roles(scenario)

    scenario_cards = [
        {
            "card_id": "B1",
            "ai_output": (
                "This programme is best suited to motivated, independent learners who are "
                "confident with technology. It is not recommended for learners who need "
                "additional support or who have English as a second language."
            ),
            "bias_flags": [
                "'Not recommended for learners who need additional support' — potentially discriminatory; assumes AI can make eligibility decisions.",
                "'English as a second language' framed as a barrier — could exclude protected groups without justification.",
                "Programme descriptions should not pre-screen learners based on assumed capability.",
            ],
            "fair_rewrite": (
                "This programme includes self-paced elements and is designed for adult "
                "learners in a range of contexts. Additional learning support and English "
                "language support are available — please contact the team to discuss your needs."
            ),
        },
        {
            "card_id": "B2",
            "ai_output": (
                "Younger staff members will adapt to AI tools more quickly and will need "
                "less training. Focus your training resources on older staff who are less "
                "comfortable with technology."
            ),
            "bias_flags": [
                "Age-based assumption about digital capability — this is a protected characteristic.",
                "Not supported by evidence — technology comfort varies across all age groups.",
                "May discourage investment in training for younger staff who also need responsible AI guidance.",
            ],
            "fair_rewrite": (
                "Staff members have varied experience with AI tools regardless of age. "
                "Training should be accessible to all staff at all career stages and should "
                "not assume capability based on age or seniority."
            ),
        },
    ]

    return {
        "activity_id": "bias_fairness_review",
        "activity_title": "Bias and Fairness Review",
        "activity_type": "review",
        "duration_minutes": 10,
        "target_roles": roles,
        "learning_objective": (
            f"Staff at {org} can identify unfair assumptions, accessibility issues, "
            f"or biased wording in AI output and suggest fairer alternatives."
        ),
        "materials_needed": [
            "Printed or digital scenario cards B1 and B2",
            "Equality Act 2010 protected characteristics list (optional reference)",
        ],
        "instructions_for_trainer": [
            "Distribute scenario cards B1 and B2.",
            "Ask participants to identify any language that could be unfair, discriminatory, or biased.",
            "After 5 minutes, reveal the bias flags and fair rewrites.",
            "Connect to the Equality Act 2010 protected characteristics if relevant.",
            "Remind participants: AI can reproduce and amplify societal biases. Human review is essential.",
        ],
        "instructions_for_participants": [
            "Read each AI output.",
            "Highlight language that seems unfair, biased, or that makes assumptions about people.",
            "Write a fairer version of the problematic sentence or section.",
        ],
        "activity_steps": [
            "Step 1 (1 min): Trainer introduces the bias concept.",
            "Step 2 (5 min): Participants review and annotate both cards.",
            "Step 3 (4 min): Trainer reveals flags, fair rewrites, and leads discussion.",
        ],
        "scenario_cards": scenario_cards,
        "expected_answers": [
            "B1 — Flag: pre-screening language against support needs and language background. Rewrite to inclusive framing.",
            "B2 — Flag: age-based assumption about digital capability. Rewrite to equal-access framing.",
        ],
        "debrief_questions": [
            "Where do you think AI bias comes from?",
            "What protected characteristics under the Equality Act 2010 are most relevant to your work context?",
            "What would you do if you noticed bias in AI output before it was sent to learners?",
            "Who in your organisation is responsible for equality, diversity, and inclusion?",
        ],
        "key_takeaways": [
            "AI can reproduce and amplify biases that exist in its training data.",
            "Bias is not always obvious — it can appear in tone, assumptions, and who is excluded.",
            "The Equality Act 2010 protects nine characteristics. AI output touching any of them requires careful review.",
            "Fairer language is not just ethical — it protects the organisation from discrimination complaints.",
        ],
        "risk_warnings": _RISK_WARNINGS,
        "responsible_use_note": _RESPONSIBLE_USE_NOTE,
    }


# ── Main generation function ────────────────────────────────────────────────────

def generate_training_activities(
    scenario: dict,
    assessment: dict = None,
    workshop_plan: dict = None,
    selected_activity_types: list = None,
) -> list:
    """Generate a list of training activity dicts for the given scenario.

    Uses selected_activity_types if provided; falls back to default activity types.
    """
    if not scenario:
        scenario = {}

    if not selected_activity_types:
        selected_activity_types = get_default_activity_types()

    catalogue = get_activity_type_catalogue()
    creators = {
        "safe_unsafe_prompt_sorting": create_safe_unsafe_prompt_sorting_activity,
        "risky_prompt_rewrite": create_risky_prompt_rewrite_activity,
        "hallucination_review": create_hallucination_review_activity,
        "learner_data_boundary": create_learner_data_boundary_activity,
        "safeguarding_escalation": create_safeguarding_escalation_activity,
        "human_review_checklist": create_human_review_checklist_activity,
        "approved_tools_decision": create_approved_tools_decision_activity,
        "bias_fairness_review": create_bias_fairness_review_activity,
    }

    activities = []
    for activity_type in selected_activity_types:
        if activity_type in creators:
            activity = creators[activity_type](scenario, assessment, workshop_plan)
            activities.append(activity)

    return activities


# ── Summary and export ──────────────────────────────────────────────────────────

def summarise_training_activities(activities: list) -> dict:
    """Return a compact summary dict for metric cards."""
    if not activities:
        return {
            "activity_count": 0,
            "estimated_total_minutes": 0,
            "activity_types": [],
            "target_roles": [],
        }

    total_minutes = sum(a.get("duration_minutes", 0) for a in activities)
    activity_types = list({a.get("activity_type", "") for a in activities if a.get("activity_type")})

    all_roles = []
    for a in activities:
        all_roles.extend(a.get("target_roles", []))
    unique_roles = list(dict.fromkeys(all_roles))

    return {
        "activity_count": len(activities),
        "estimated_total_minutes": total_minutes,
        "activity_types": sorted(activity_types),
        "target_roles": unique_roles,
    }


def format_activity_as_markdown(activity: dict) -> str:
    """Return a single activity formatted as Markdown."""
    lines = []

    lines.append(f"### {activity.get('activity_title', 'Activity')}")
    lines.append("")
    lines.append(f"**Type:** {activity.get('activity_type', '').capitalize()}")
    lines.append(f"**Duration:** {activity.get('duration_minutes', '')} minutes")

    roles = activity.get("target_roles", [])
    if roles:
        lines.append(f"**Target roles:** {', '.join(roles)}")

    lines.append("")
    lines.append(f"**Learning objective:** {activity.get('learning_objective', '')}")

    materials = activity.get("materials_needed", [])
    if materials:
        lines.append("")
        lines.append("**Materials needed:**")
        for m in materials:
            lines.append(f"- {m}")

    trainer_instrs = activity.get("instructions_for_trainer", [])
    if trainer_instrs:
        lines.append("")
        lines.append("**Trainer instructions:**")
        for i, instr in enumerate(trainer_instrs, 1):
            lines.append(f"{i}. {instr}")

    participant_instrs = activity.get("instructions_for_participants", [])
    if participant_instrs:
        lines.append("")
        lines.append("**Participant instructions:**")
        for instr in participant_instrs:
            lines.append(f"- {instr}")

    steps = activity.get("activity_steps", [])
    if steps:
        lines.append("")
        lines.append("**Activity steps:**")
        for step in steps:
            lines.append(f"- {step}")

    scenario_cards = activity.get("scenario_cards", [])
    if scenario_cards:
        lines.append("")
        lines.append("**Scenario cards / examples:**")
        for card in scenario_cards:
            card_id = card.get("card_id", "")
            if "prompt" in card:
                lines.append(f"")
                lines.append(f"*Card {card_id} — Prompt:* \"{card['prompt']}\"")
                lines.append(f"*Classification:* {card.get('classification', '')}")
                lines.append(f"*Reason:* {card.get('reason', '')}")
            elif "original_prompt" in card:
                lines.append(f"")
                lines.append(f"*Card {card_id} — Original prompt:* \"{card['original_prompt']}\"")
                lines.append(f"*Problem:* {card.get('problem', '')}")
                lines.append(f"*Safe rewrite:* \"{card.get('safe_rewrite', '')}\"")
            elif "ai_output" in card:
                lines.append(f"")
                lines.append(f"*Card {card_id} — AI output:* \"{card['ai_output']}\"")
                flags = card.get("hallucination_flags", card.get("bias_flags", []))
                if flags:
                    lines.append(f"*Issues identified:*")
                    for flag in flags:
                        lines.append(f"  - {flag}")
            elif "situation" in card:
                lines.append(f"")
                lines.append(f"*Card {card_id} — Situation:* {card['situation']}")
                if card.get("wrong_action"):
                    lines.append(f"*Wrong action:* {card['wrong_action']}")
                if card.get("correct_action"):
                    lines.append(f"*Correct action:* {card['correct_action']}")
                if card.get("boundary_rule"):
                    lines.append(f"*Boundary rule:* {card['boundary_rule']}")
                if card.get("why"):
                    lines.append(f"*Why:* {card['why']}")
            elif "proposed_use" in card:
                lines.append(f"")
                lines.append(f"*Card {card_id} — Proposed use:* {card['proposed_use']}")
                lines.append(f"*Decision:* {card.get('decision', '')}")
                lines.append(f"*Reason:* {card.get('reason', '')}")
            elif "task" in card:
                lines.append(f"")
                lines.append(f"*Card {card_id} — Task:* {card['task']}")
                key_checks = card.get("key_checks", [])
                if key_checks:
                    lines.append(f"*Key checks to apply:*")
                    for check in key_checks:
                        lines.append(f"  - {check}")

    expected = activity.get("expected_answers", [])
    if expected:
        lines.append("")
        lines.append("**Expected answers:**")
        for ans in expected:
            lines.append(f"- {ans}")

    debrief = activity.get("debrief_questions", [])
    if debrief:
        lines.append("")
        lines.append("**Debrief questions:**")
        for i, q in enumerate(debrief, 1):
            lines.append(f"{i}. {q}")

    takeaways = activity.get("key_takeaways", [])
    if takeaways:
        lines.append("")
        lines.append("**Key takeaways:**")
        for t in takeaways:
            lines.append(f"- {t}")

    warnings = activity.get("risk_warnings", [])
    if warnings:
        lines.append("")
        lines.append("**Risk warnings:**")
        for w in warnings:
            lines.append(f"- {w}")

    note = activity.get("responsible_use_note", "")
    if note:
        lines.append("")
        lines.append(f"**Responsible use note:** {note}")

    return "\n".join(lines)


def format_activities_as_markdown(activities: list) -> str:
    """Return all activities formatted as a complete Markdown document."""
    if not activities:
        return "# Responsible AI Staff Training Activities\n\nNo activities generated.\n"

    org = activities[0].get("responsible_use_note", "")
    first = activities[0]
    org_name = ""
    for a in activities:
        roles = a.get("target_roles", [])
        if roles:
            break

    lines = []
    lines.append("# Responsible AI Staff Training Activities")
    lines.append("")

    summary = summarise_training_activities(activities)
    lines.append("## Activity Summary")
    lines.append("")
    lines.append(f"- **Total activities:** {summary['activity_count']}")
    lines.append(f"- **Estimated total time:** {summary['estimated_total_minutes']} minutes")
    lines.append(f"- **Activity types:** {', '.join(summary['activity_types'])}")
    if summary["target_roles"]:
        lines.append(f"- **Target roles:** {', '.join(summary['target_roles'])}")
    lines.append("")

    for i, activity in enumerate(activities, 1):
        lines.append(f"## Activity {i}: {activity.get('activity_title', 'Activity')}")
        lines.append("")
        lines.append(format_activity_as_markdown(activity))
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Prototype and Responsible-Use Boundaries")
    lines.append("")
    lines.append(
        "These activities are generated from a synthetic organisation scenario only. "
        "They must not be used with real learner data, safeguarding case details, "
        "confidential client records, staff HR data, personal data, or regulated "
        "information without appropriate governance, approvals, and responsible owners."
    )
    lines.append("")
    lines.append(
        "This prototype does not provide legal, safeguarding, HR, compliance, medical, "
        "financial, academic-integrity, or professional advice."
    )
    lines.append("")
    lines.append(
        "All scenario cards, example prompts, and AI outputs in these activities are "
        "synthetic and fictional. Human review is required before using any output in "
        "a real training session."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)


def create_activities_filename(organisation_name: str) -> str:
    """Return a safe kebab-case filename for the activities Markdown file."""
    org = organisation_name or "organisation"
    slug = org.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return f"training-activities-{slug}.md"
