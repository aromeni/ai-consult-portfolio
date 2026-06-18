"""
Synthetic sample data for the BrightPath AI Readiness + Workflow Audit Tool.

All data is fictional and anonymised. No real learner, client, staff,
safeguarding, or personal data is represented here.
"""

BRIGHTPATH_PROFILE = {
    "org_name": "BrightPath Skills Training",
    "org_type": "Private skills training provider (funded provision)",
    "sector": "Education and training",
    "staff_count": "11–50",
    "current_ai_tools": ["ChatGPT (personal accounts)", "Grammarly"],
    "has_ai_policy": False,
    "has_approved_tools": False,
    "has_dpo_or_lead": True,
    "manager_ai_awareness": "Low",
    "notes": (
        "Staff are using personal ChatGPT accounts for lesson planning and "
        "email drafting. No formal AI policy or approved tool list exists. "
        "Some staff may be entering learner-related context into ChatGPT."
    ),
}

BRIGHTPATH_READINESS_RESPONSES = {
    "data_awareness": 2,       # Staff awareness of data boundaries
    "prompt_skill": 2,         # Ability to write structured prompts
    "output_review": 2,        # Habit of reviewing AI outputs before use
    "governance": 1,           # Existence of policy, approved tools, escalation
    "manager_oversight": 2,    # Manager ability to oversee AI-assisted work
}

# Phase 2: full readiness assessment scores (0–10 per dimension, total 0–100)
# BrightPath total: 35 → "Early awareness" band
BRIGHTPATH_READINESS_SCORES = {
    "workflow_clarity": 5,        # Some workflows identified, but not documented
    "ai_awareness": 3,            # Low — staff unaware of hallucination risks
    "data_sensitivity": 2,        # Critical gap — learner data being entered into ChatGPT
    "staff_capability": 3,        # Informal use only; no structured prompting
    "leadership_support": 4,      # Interested but not yet committed
    "governance_maturity": 1,     # No policy, no approved tools, no escalation route
    "technical_readiness": 6,     # Staff have device access and internet connectivity
    "business_need": 5,           # Want to save time but no measurable targets set
    "implementation_capacity": 4, # Small team; limited management bandwidth
    "risk_awareness": 2,          # Low — staff do not recognise data risk they are creating
}

BRIGHTPATH_WORKFLOWS = [
    {
        "workflow": "Generic lesson plan structure",
        "role": "Tutor",
        "current_time_min": 45,
        "ai_suitable": True,
        "risk_level": "Low",
        "notes": "No learner identifiers needed. Safe with constraints clause.",
    },
    {
        "workflow": "Staff email drafting (non-sensitive)",
        "role": "Administrator",
        "current_time_min": 20,
        "ai_suitable": True,
        "risk_level": "Low",
        "notes": "Suitable for non-personnel, non-learner correspondence.",
    },
    {
        "workflow": "Meeting agenda templates",
        "role": "Manager / Administrator",
        "current_time_min": 15,
        "ai_suitable": True,
        "risk_level": "Low",
        "notes": "Standard structure only. No confidential agenda items.",
    },
    {
        "workflow": "Learner progress report writing",
        "role": "Tutor",
        "current_time_min": 30,
        "ai_suitable": False,
        "risk_level": "High",
        "notes": (
            "Contains identifiable learner data. Must not be entered into "
            "unapproved AI tools. Requires governance approval before any AI use."
        ),
    },
    {
        "workflow": "Safeguarding case notes",
        "role": "Designated Safeguarding Lead",
        "current_time_min": 40,
        "ai_suitable": False,
        "risk_level": "Critical",
        "notes": (
            "Safeguarding data is special category under UK GDPR. "
            "AI tools must never be used for safeguarding records."
        ),
    },
    {
        "workflow": "Funding application narrative drafting",
        "role": "Manager",
        "current_time_min": 120,
        "ai_suitable": None,  # Borderline
        "risk_level": "Medium",
        "notes": (
            "Public-facing narrative sections may be AI-assisted with human review. "
            "Learner outcome data and cohort figures must not be entered. "
            "Governance review recommended before use."
        ),
    },
    {
        "workflow": "IQA / EQA report preparation",
        "role": "IQA Lead",
        "current_time_min": 90,
        "ai_suitable": False,
        "risk_level": "High",
        "notes": (
            "Contains learner outcome data and assessment judgements. "
            "Not suitable for AI tools without governance approval."
        ),
    },
    {
        "workflow": "Staff newsletter drafts",
        "role": "Administrator / Manager",
        "current_time_min": 30,
        "ai_suitable": True,
        "risk_level": "Low",
        "notes": "Public-facing, non-sensitive content. Safe with human review.",
    },
]

# Phase 3: sample workflow for the Workflow Audit page
BRIGHTPATH_SAMPLE_WORKFLOW = {
    "name": "Generic lesson planning support",
    "owner": "Tutor team",
    "description": (
        "Tutors create first-draft lesson plans for standard curriculum topics. "
        "Each plan follows a consistent structure: learning aims, activities, "
        "resources needed, and assessment approach. No learner names or individual "
        "data are included — plans are topic-based, not cohort-specific."
    ),
    "tools": "Word processor, curriculum guidelines, awarding body unit specifications",
    "frequency": "Weekly",
    "time_spent": "~45 minutes per lesson plan",
    "pain_points": (
        "Tutors spend most of their time on formatting and structure rather than "
        "content. The first draft is nearly always restructured before use. "
        "Newer tutors find the structure difficult to get right consistently."
    ),
    "data_sensitivity": "Low — no learner names, outcomes, or identifiable data involved",
    "ai_support_idea": (
        "Generate a first-draft lesson plan structure from an approved curriculum topic "
        "and unit specification. Tutor reviews, edits, and approves before use. "
        "No learner data or personal information is entered into the AI tool."
    ),
}

# Phase 3: workflow suitability scores for the lesson plan sample (total = 42 → Good pilot candidate)
BRIGHTPATH_SAMPLE_WORKFLOW_SCORES = {
    "repetition": 4,              # Same structure every week
    "rule_clarity": 4,            # Curriculum and awarding body specs provide clear structure
    "document_intensity": 4,      # Entirely text-based task
    "time_burden": 4,             # 45 min per plan is significant at weekly frequency
    "risk_manageability": 5,      # Tutor reviews before use; errors are easy to spot
    "human_review_feasibility": 5,  # Straightforward for a tutor to review a draft
    "business_value": 4,          # Frees tutor time for teaching and learner support
    "staff_readiness": 3,         # Mixed — some tutors keen, some cautious
    "data_sensitivity_control": 5,  # No learner data needed; topic-based only
    "implementation_simplicity": 4,  # Prompt-based task; no system integration needed
}

# Phase 4: risk profile for the lesson plan support use case
# Scores are likelihood (1–5) × impact (1–5) per category.
# Use case: BrightPath tutors using AI to draft generic lesson plan structures.
BRIGHTPATH_RISK_PROFILE = {
    "use_case": "Generic lesson planning support",
    "scores": {
        # Low — only curriculum topics entered; no personal data needed
        "data_privacy":           {"likelihood": 1, "impact": 2},
        # Low — lesson plans are topic-based; no learner identifiers needed
        "learner_data":           {"likelihood": 1, "impact": 4},
        # High — small risk a tutor inadvertently adds case context to the prompt
        "safeguarding":           {"likelihood": 2, "impact": 5},
        # Low — curriculum topics are not confidential
        "confidentiality":        {"likelihood": 1, "impact": 2},
        # Moderate — AI may generate plausible but inaccurate curriculum content
        "accuracy_hallucination": {"likelihood": 3, "impact": 3},
        # Low — lesson plan structure has limited bias risk at content level
        "bias_fairness":          {"likelihood": 2, "impact": 2},
        # Moderate — awarding body unit specs and materials may be copyrighted
        "copyright_ip":           {"likelihood": 2, "impact": 3},
        # Low — no credentials or system details involved
        "security":               {"likelihood": 1, "impact": 2},
        # Moderate — tutors may adopt AI drafts without checking curriculum accuracy
        "over_reliance":          {"likelihood": 3, "impact": 3},
        # Moderate — no formal AI output ownership or review process yet in place
        "accountability":         {"likelihood": 2, "impact": 3},
    },
}

# Phase 5: worked pilot recommendation example (values chosen to illustrate Low-risk pilot candidate)
# Note: these are illustrative, not the same as BRIGHTPATH_READINESS_SCORES / BRIGHTPATH_RISK_PROFILE totals.
# Phase 6: sample values for the Mini Report page load-sample button
BRIGHTPATH_MINI_REPORT_SAMPLE = {
    "org_name": "BrightPath Skills Training",
    "org_type": "Small UK training provider",
    "staff_count": "8",
    "ai_use_summary": (
        "Staff are beginning to use ChatGPT informally for lesson planning, "
        "emails, and report drafting."
    ),
    "main_concerns": (
        "Learner data, safeguarding, staff misuse, output accuracy, "
        "and whether AI will genuinely save time."
    ),
    "readiness_score": 62,
    "workflow_name": "Generic lesson planning support",
    "workflow_owner": "Tutor team",
    "ai_support_idea": (
        "Generate first-draft lesson plans from approved curriculum topics, "
        "reviewed by tutors before use."
    ),
    "workflow_score": 40,
    "highest_risk": "Moderate",
    "has_critical": False,
    "has_high": False,
    "key_risk_notes": (
        "AI may produce inaccurate or unsuitable lesson content if not reviewed. "
        "Staff must not enter learner data or safeguarding information."
    ),
    "safeguards_text": (
        "- Use approved curriculum topics only.\n"
        "- Do not enter identifiable learner data.\n"
        "- Do not enter safeguarding information.\n"
        "- Tutor reviews all lesson plans before use.\n"
        "- Track time saved and quality issues.\n"
        "- Review pilot after 4 weeks."
    ),
    "next_actions_text": (
        "1. Confirm approved AI tool and account settings.\n"
        "2. Train tutor team on safe prompting and data boundaries.\n"
        "3. Run a 2–4 week pilot with generic lesson planning only.\n"
        "4. Collect staff feedback and examples of time saved.\n"
        "5. Review risks before expanding to other workflows."
    ),
    "consultant_notes": (
        "This is a safe first pilot candidate if data boundaries "
        "and human review are enforced."
    ),
}

BRIGHTPATH_PILOT_EXAMPLE = {
    "workflow_name": "Generic lesson planning support",
    "ai_support_idea": (
        "Generate first-draft lesson plans from approved curriculum topics, "
        "reviewed by tutors before use."
    ),
    "readiness_score": 62,
    "readiness_category": "Pilot ready with safeguards",
    "workflow_score": 40,
    "workflow_category": "Good pilot candidate",
    "highest_risk_level": "Moderate",
    "has_critical_risk": False,
    "has_high_risk": False,
    "recommendation": "Low-risk pilot candidate",
}
