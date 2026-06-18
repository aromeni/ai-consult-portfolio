"""Synthetic scenario data for the AI Staff Training and Workshop Generator.

Phase 1: all data is synthetic and clearly labelled. No real organisations,
learner records, safeguarding information, or personal data.
"""


def get_brightpath_training_scenario() -> dict:
    """Return the BrightPath synthetic training scenario.

    BrightPath Skills Training is a fictional small UK training provider used
    as the demo scenario throughout this prototype. It is entirely synthetic.
    """
    return {
        "organisation_name": "BrightPath Skills Training",
        "organisation_type": "Small UK training provider",
        "staff_count": 8,
        "sector": "Education and training",
        "country_context": "United Kingdom",
        "current_ai_use": (
            "Staff are beginning to use ChatGPT informally for lesson planning, "
            "emails, and reports. No formal policy or approved tooling is in place."
        ),
        "main_concerns": [
            "learner data",
            "safeguarding boundaries",
            "staff misuse",
            "output accuracy",
            "hallucination",
            "bias",
            "approved tools",
            "accountability",
            "time saving",
        ],
        "staff_roles": [
            "tutors",
            "administrators",
            "team leaders",
            "quality lead",
        ],
        "training_goal": (
            "Help staff use AI safely and practically for low-risk lesson planning "
            "and admin support."
        ),
        "training_duration": "90 minutes",
        "delivery_mode": "In-person workshop",
        "priority_topics": [
            "safe prompting",
            "learner data boundaries",
            "safeguarding boundaries",
            "human review",
            "approved tools",
            "hallucination and accuracy",
            "bias and fairness",
            "escalation routes",
        ],
    }


def get_default_priority_topics() -> list:
    """Return the full list of responsible AI training topics available for selection."""
    return [
        "safe prompting",
        "learner data boundaries",
        "safeguarding boundaries",
        "human review",
        "approved tools",
        "hallucination and accuracy",
        "bias and fairness",
        "escalation routes",
        "data minimisation",
        "output verification",
        "copyright and intellectual property",
        "consent and transparency",
        "accountability and responsibility",
        "AI limitations",
        "when not to use AI",
    ]


def get_default_staff_roles() -> list:
    """Return a common set of staff roles in a small training organisation."""
    return [
        "tutors",
        "administrators",
        "team leaders",
        "quality lead",
        "curriculum leads",
        "assessors",
        "pastoral support staff",
        "IT staff",
    ]


def get_responsible_ai_topic_descriptions() -> dict:
    """Return a description for each responsible AI training topic.

    These descriptions are used in workshop materials to give context to each topic.
    All content is generic responsible-AI guidance — not legal or compliance advice.
    """
    return {
        "safe prompting": (
            "How to write prompts that avoid entering sensitive, personal, or "
            "confidential information into AI tools. Includes data-minimised prompt "
            "techniques and approved phrasing examples."
        ),
        "learner data boundaries": (
            "Understanding which types of learner information must never be entered "
            "into AI tools. Covers names, contact details, grades, attendance, "
            "safeguarding records, and any identifiable data."
        ),
        "safeguarding boundaries": (
            "Why safeguarding disclosures, welfare concerns, and case information must "
            "never be processed by AI tools. Covers the risk of AI handling sensitive "
            "disclosures incorrectly and the need for human escalation."
        ),
        "human review": (
            "Why all AI outputs — answers, drafts, summaries — must be reviewed by a "
            "qualified human before use. AI tools can produce plausible but incorrect, "
            "biased, or inappropriate content."
        ),
        "approved tools": (
            "Understanding which AI tools are approved for use in the organisation, "
            "how to access them, and why unapproved tools carry data protection "
            "and reputational risk."
        ),
        "hallucination and accuracy": (
            "What AI hallucination is, why it happens, and how to spot it. Practical "
            "guidance for verifying AI-generated facts, figures, citations, and "
            "recommendations before acting on them."
        ),
        "bias and fairness": (
            "How AI tools can reflect or amplify bias in language, imagery, and "
            "recommendations. Covers the risk to learners, staff, and organisational "
            "equality and diversity obligations."
        ),
        "escalation routes": (
            "Who to contact when an AI tool produces something concerning, harmful, "
            "or unexpected. Covers incident reporting, data breach procedures, and "
            "safeguarding escalation pathways."
        ),
        "data minimisation": (
            "The principle of using the minimum amount of information necessary when "
            "writing prompts. Practical techniques for anonymising and generalising "
            "examples before entering them into AI tools."
        ),
        "output verification": (
            "Practical steps for checking AI outputs before sharing or acting on them. "
            "Includes source checking, factual verification, tone review, and applying "
            "professional judgement."
        ),
        "copyright and intellectual property": (
            "Understanding the copyright implications of AI-generated text, images, "
            "and code. Covers organisational policy on AI-generated content and "
            "disclosure obligations."
        ),
        "consent and transparency": (
            "When and how to disclose AI tool use to learners, clients, and "
            "colleagues. Covers consent requirements and transparency obligations "
            "in an educational context."
        ),
        "accountability and responsibility": (
            "Who is responsible for AI outputs used in professional contexts. Covers "
            "the principle that AI does not remove professional accountability, and "
            "practical guidance on maintaining a clear chain of responsibility."
        ),
        "AI limitations": (
            "Understanding what AI tools cannot reliably do: legal advice, medical "
            "advice, safeguarding decisions, HR decisions, compliance assessments, "
            "and other high-stakes judgements that require qualified human expertise."
        ),
        "when not to use AI": (
            "Practical guidance on situations where AI tools should not be used at "
            "all: safeguarding disclosures, personal data processing, high-stakes "
            "decisions, regulated advice, and situations requiring empathy and "
            "professional judgement."
        ),
    }
