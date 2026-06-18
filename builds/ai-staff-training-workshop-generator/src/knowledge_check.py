"""Knowledge check generator for the AI Staff Training and Workshop Generator.

Phase 7: generates responsible AI staff knowledge checks — multiple-choice questions,
scenario-based questions, short reflection prompts, and answer guidance.

All content is generated from synthetic organisation scenario data only.
No real learner data, safeguarding case details, or personal information.
"""

import re

_PROTOTYPE_NOTE = (
    "This knowledge check is generated from a synthetic organisation scenario only. "
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

_MARKING_NOTE = (
    "This knowledge check is designed for learning and discussion, not formal "
    "certification. Human review remains required before staff use AI for work tasks."
)

# Complete bank of 15 multiple-choice questions — generate_multiple_choice_questions
# selects up to question_count from the beginning of this list.
_MCQ_BANK = [
    {
        "question_id": "mcq_001",
        "topic": "safe prompting",
        "question": "Which prompt is safest to use in an AI tool?",
        "options": {
            "A": "Rewrite this support note for learner Sarah Ahmed who disclosed anxiety.",
            "B": "Create a generic lesson outline on workplace communication for adult learners.",
            "C": "Decide whether this safeguarding concern should be reported.",
            "D": "Summarise this staff disciplinary record.",
        },
        "correct_answer": "B",
        "explanation": (
            "Option B uses a generic topic and does not include identifiable learner data, "
            "safeguarding details, HR data, or confidential information. "
            "Options A, C, and D all involve prohibited data types or decisions."
        ),
    },
    {
        "question_id": "mcq_002",
        "topic": "human review",
        "question": "What should staff do before using an AI-generated lesson plan?",
        "options": {
            "A": "Use it immediately if it sounds professional.",
            "B": "Ask AI whether it is accurate.",
            "C": "Review it for accuracy, bias, accessibility, tone, and policy alignment.",
            "D": "Share it with learners without checking it.",
        },
        "correct_answer": "C",
        "explanation": (
            "AI-generated content must be reviewed by a human before use. "
            "Staff should check accuracy, fairness, accessibility, tone, and policy alignment. "
            "AI cannot reliably verify its own output."
        ),
    },
    {
        "question_id": "mcq_003",
        "topic": "learner data boundaries",
        "question": "Which of the following must NOT be entered into an AI tool?",
        "options": {
            "A": "A generic discussion question about workplace safety.",
            "B": "A list of learner names and attendance records.",
            "C": "A template agenda for a team meeting.",
            "D": "A reworded version of a public policy summary.",
        },
        "correct_answer": "B",
        "explanation": (
            "Learner names and attendance records are personal data. "
            "Entering identifiable learner data into AI tools likely breaches data protection obligations. "
            "Generic, non-identifiable content is acceptable."
        ),
    },
    {
        "question_id": "mcq_004",
        "topic": "safeguarding boundaries",
        "question": "A safeguarding concern about a named learner has been raised. What should staff do?",
        "options": {
            "A": "Ask ChatGPT for advice on how to handle the concern.",
            "B": "Use AI to draft a safeguarding referral.",
            "C": "Follow the organisation's safeguarding procedure and contact the safeguarding lead.",
            "D": "Record the concern in AI and forward the output to the manager.",
        },
        "correct_answer": "C",
        "explanation": (
            "Safeguarding decisions must always be made by a qualified designated safeguarding lead, "
            "following the organisation's procedure. AI must never be used for safeguarding judgement, "
            "referrals, or case handling."
        ),
    },
    {
        "question_id": "mcq_005",
        "topic": "approved tools",
        "question": "A staff member is unsure whether a free AI tool they found online is approved for work use. What should they do?",
        "options": {
            "A": "Use it for work tasks if it gives good results.",
            "B": "Check with a manager or AI/policy owner before using it for work data.",
            "C": "Use it only for personal tasks and then use the output at work.",
            "D": "Ask the AI tool whether it is approved.",
        },
        "correct_answer": "B",
        "explanation": (
            "Staff must only use approved tools for organisational data. "
            "If unsure, the correct action is to ask the manager or AI/policy owner before using. "
            "Using unapproved tools with work data may breach policy."
        ),
    },
    {
        "question_id": "mcq_006",
        "topic": "hallucination and accuracy",
        "question": "An AI tool produces a lesson resource that includes a statistic claiming that 85% of learners fail due to poor attendance. What should a tutor do?",
        "options": {
            "A": "Use the statistic if it seems plausible.",
            "B": "Include the statistic since AI is usually reliable.",
            "C": "Verify the statistic independently before including it in any materials.",
            "D": "Remove the statistic only if a learner questions it.",
        },
        "correct_answer": "C",
        "explanation": (
            "AI tools can produce hallucinations — plausible-sounding but fabricated facts, "
            "statistics, or references. Staff must independently verify any factual claims "
            "before using AI-generated content."
        ),
    },
    {
        "question_id": "mcq_007",
        "topic": "bias and fairness",
        "question": "An AI tool generates a description of a 'typical learner' that only describes a young, male, English-speaking person. What should staff do?",
        "options": {
            "A": "Use it as-is — AI is neutral.",
            "B": "Recognise this as a potential bias issue and revise to be inclusive.",
            "C": "Replace 'male' with 'person' and use the rest unchanged.",
            "D": "Ask the AI to fix it and use whatever it produces next.",
        },
        "correct_answer": "B",
        "explanation": (
            "AI tools can reproduce and amplify biases in their training data. "
            "Staff should review AI output for bias and unfair representation, "
            "and revise to ensure learning materials are inclusive and accessible."
        ),
    },
    {
        "question_id": "mcq_008",
        "topic": "accountability",
        "question": "An AI tool produces a formal report about a learner's progress. Who is responsible for the content of that report?",
        "options": {
            "A": "The AI tool that produced it.",
            "B": "The organisation that built the AI tool.",
            "C": "The staff member who reviewed and used the report.",
            "D": "No one — AI output is not anyone's responsibility.",
        },
        "correct_answer": "C",
        "explanation": (
            "Professional responsibility remains with the human who reviewed and used the output. "
            "AI is a tool that supports work — it does not hold or transfer accountability. "
            "Staff must review all AI output before using it."
        ),
    },
    {
        "question_id": "mcq_009",
        "topic": "escalation routes",
        "question": "A staff member realises they may have accidentally entered learner personal data into an unapproved AI tool. What should they do?",
        "options": {
            "A": "Delete the conversation history and say nothing.",
            "B": "Report the potential data breach to the data protection lead or manager immediately.",
            "C": "Wait to see if any problems occur before reporting.",
            "D": "Ask the AI tool to delete the data.",
        },
        "correct_answer": "B",
        "explanation": (
            "A potential data breach must be reported to the data protection lead or manager immediately. "
            "Organisations have a legal obligation to report certain data breaches within 72 hours. "
            "Delaying or concealing a breach may worsen the situation."
        ),
    },
    {
        "question_id": "mcq_010",
        "topic": "prohibited AI uses",
        "question": "Which of the following is a prohibited use of AI in a training organisation?",
        "options": {
            "A": "Drafting a generic email template for a low-risk admin task.",
            "B": "Creating discussion questions for a topic without using any personal data.",
            "C": "Making an assessment decision about whether a learner should pass or fail.",
            "D": "Simplifying publicly available guidance into plain English.",
        },
        "correct_answer": "C",
        "explanation": (
            "AI must not make assessment, accreditation, or formal qualification decisions. "
            "These decisions require professional judgement by a qualified assessor. "
            "Options A, B, and D are acceptable low-risk uses."
        ),
    },
    {
        "question_id": "mcq_011",
        "topic": "learner data boundaries",
        "question": "A tutor wants to use AI to personalise feedback for a specific learner. What is the safest approach?",
        "options": {
            "A": "Enter the learner's name, grades, and attendance into the AI tool.",
            "B": "Create a generic feedback template using AI, then personalise it manually without AI.",
            "C": "Ask AI to write individual feedback for each learner by name.",
            "D": "Upload the learner's assessment portfolio to the AI tool.",
        },
        "correct_answer": "B",
        "explanation": (
            "The safest approach is to use AI for the generic template only, "
            "then personalise manually without entering identifiable learner data into AI. "
            "Entering names, grades, and portfolios into AI tools is likely a data protection breach."
        ),
    },
    {
        "question_id": "mcq_012",
        "topic": "safe prompting",
        "question": "What should a well-written safe AI prompt include?",
        "options": {
            "A": "As much specific context as possible, including learner names.",
            "B": "An explicit instruction not to include personal data, and a generic task description.",
            "C": "A request for the AI to use real examples from your organisation.",
            "D": "Personal context about individual staff members to get a more relevant result.",
        },
        "correct_answer": "B",
        "explanation": (
            "Safe prompts use generic task descriptions and explicitly instruct the AI "
            "not to include personal data. The more specific and personal the prompt, "
            "the higher the risk of a data protection or safeguarding issue."
        ),
    },
    {
        "question_id": "mcq_013",
        "topic": "human review",
        "question": "Which of the following checks should staff complete before using AI-generated content with learners?",
        "options": {
            "A": "Check it once quickly for obvious errors.",
            "B": "Check accuracy, tone, fairness, accessibility, and policy alignment.",
            "C": "Ask another AI tool to review it.",
            "D": "Use it if the AI gave a confident answer.",
        },
        "correct_answer": "B",
        "explanation": (
            "AI output must be reviewed across multiple dimensions: "
            "accuracy (facts are correct), tone (appropriate for the audience), "
            "fairness (no bias or stereotyping), accessibility (inclusive language), "
            "and policy alignment (consistent with organisational policy)."
        ),
    },
    {
        "question_id": "mcq_014",
        "topic": "hallucination and accuracy",
        "question": "An AI tool cites a specific piece of legislation in a training resource. What should staff do?",
        "options": {
            "A": "Trust the citation — AI tools are trained on legal documents.",
            "B": "Verify the legislation exists and the reference is accurate before using it.",
            "C": "Remove all legal references from the resource just in case.",
            "D": "Forward the resource to the legal team and wait indefinitely.",
        },
        "correct_answer": "B",
        "explanation": (
            "AI tools frequently hallucinate legal references — citing laws, clauses, or "
            "cases that do not exist or are incorrectly described. Staff must independently "
            "verify any legal or regulatory references before using them."
        ),
    },
    {
        "question_id": "mcq_015",
        "topic": "accountability",
        "question": "A manager decides to use AI to draft a staff performance review. Who holds professional responsibility for the review?",
        "options": {
            "A": "The AI tool.",
            "B": "The manager who reviewed and approved the draft.",
            "C": "The HR department that stores the review.",
            "D": "The organisation that licensed the AI tool.",
        },
        "correct_answer": "B",
        "explanation": (
            "The manager who reviewed, approved, and signed off the review holds professional "
            "responsibility. AI drafts a document — the human who uses it is accountable for its content. "
            "AI tools should not be used for formal HR documentation without significant caution and review."
        ),
    },
]

# Complete bank of scenario questions
_SCENARIO_BANK = [
    {
        "question_id": "scenario_001",
        "topic": "safeguarding boundaries",
        "scenario": (
            "A tutor has just had a concerning conversation with a learner. "
            "They want to paste the details of what the learner said into ChatGPT "
            "to ask what action to take."
        ),
        "question": "What should the tutor do instead?",
        "expected_answer_points": [
            "Do not enter safeguarding case details into AI tools.",
            "Follow the organisation's safeguarding procedure.",
            "Escalate to the designated safeguarding lead (DSL) immediately.",
            "Keep decisions human-led — do not rely on AI for safeguarding judgement.",
            "Record the concern in the designated safeguarding system, not an AI tool.",
        ],
        "risk_flags": [
            "Safeguarding data breach risk.",
            "Incorrect or delayed safeguarding response if AI is used.",
            "Potential harm to learner if correct procedure is not followed.",
        ],
        "model_answer": (
            "The tutor should immediately follow the organisation's safeguarding procedure. "
            "They should not enter any details of the concern into AI tools. "
            "They should contact the designated safeguarding lead (DSL) and record the concern "
            "in the appropriate safeguarding system. Safeguarding decisions must always be "
            "made by a qualified human lead — never by AI."
        ),
    },
    {
        "question_id": "scenario_002",
        "topic": "learner data boundaries",
        "scenario": (
            "An administrator wants to use a free personal AI account to rewrite emails "
            "about learner attendance. The emails contain learner names, dates, and attendance figures."
        ),
        "question": "What are the risks and what should the administrator do instead?",
        "expected_answer_points": [
            "Do not enter identifiable learner data into unapproved AI tools.",
            "Personal AI accounts are not approved for organisational or learner data.",
            "Use approved systems only — check with manager or AI/policy owner.",
            "Remove identifiers (names, dates, specific figures) before using AI, if approved.",
            "Seek manager or data protection lead guidance before proceeding.",
        ],
        "risk_flags": [
            "Data protection breach risk.",
            "Learner personal data sent to unapproved third-party system.",
            "Organisation likely has no data processing agreement with the AI tool provider.",
        ],
        "model_answer": (
            "The administrator should not enter learner names or attendance data into any "
            "unapproved AI tool, including personal accounts. They should check with their "
            "manager or data protection lead to understand which tools are approved. "
            "If a task is acceptable with AI, they should use an approved tool and ensure "
            "no identifiable learner data is included in the prompt."
        ),
    },
    {
        "question_id": "scenario_003",
        "topic": "hallucination and accuracy",
        "scenario": (
            "A team leader uses AI to write a training resource. The resource includes "
            "a statistic: 'According to the Department for Education 2023 report, "
            "72% of learners improve when taught with AI tools.' "
            "The team leader cannot find this report."
        ),
        "question": "What should the team leader do and why?",
        "expected_answer_points": [
            "Remove or replace the statistic until it can be independently verified.",
            "Do not publish or use resources containing unverified claims.",
            "AI tools frequently hallucinate statistics, reports, and citations.",
            "Search for the cited report and confirm it exists before using the statistic.",
            "If the report cannot be found, do not use the statistic.",
        ],
        "risk_flags": [
            "Hallucinated statistic from AI tool.",
            "Potential reputational and credibility risk if published.",
            "Possible regulatory risk if materials are submitted for accreditation.",
        ],
        "model_answer": (
            "The team leader should remove the statistic immediately and not publish the resource "
            "until the claim is verified. AI tools frequently produce hallucinated statistics "
            "that sound plausible but do not exist. The team leader should search for the "
            "cited report independently. If it cannot be found, the statistic must be removed "
            "or replaced with a verified source."
        ),
    },
    {
        "question_id": "scenario_004",
        "topic": "bias and fairness",
        "scenario": (
            "A quality lead uses AI to generate learner profiles for a training exercise. "
            "All of the generated profiles describe learners as young, male, English-speaking, "
            "and with no additional learning needs."
        ),
        "question": "What issue does this raise and what should the quality lead do?",
        "expected_answer_points": [
            "Identify this as a bias issue in the AI-generated content.",
            "AI tools can reproduce and amplify biases from training data.",
            "Do not use biased content in learner-facing materials.",
            "Revise the profiles to represent a diverse range of learners.",
            "Check all AI-generated materials for bias before use.",
        ],
        "risk_flags": [
            "Bias and fairness risk.",
            "Potential impact on learner inclusion and engagement.",
            "Could disadvantage or exclude learners with protected characteristics.",
        ],
        "model_answer": (
            "The quality lead should recognise this as a potential AI bias issue. "
            "AI tools can reflect and amplify biases in their training data. "
            "The profiles should not be used as-is. The quality lead should revise them "
            "to represent a diverse range of learners, including different ages, genders, "
            "languages, and learning needs. All AI-generated content used with learners "
            "should be reviewed for inclusivity and fairness."
        ),
    },
]

_REFLECTION_BANK = [
    {
        "question_id": "reflection_001",
        "topic": "safe prompting",
        "question": (
            "What is one AI task you can safely carry out for low-risk work — "
            "and what would you include in a safe prompt for that task?"
        ),
        "guidance_points": [
            "Low-risk tasks: drafting generic templates, generating discussion questions, rewriting generic correspondence.",
            "Safe prompts use generic, non-identifiable content.",
            "Good prompts include an explicit instruction: 'Do not include names, personal details, or case-specific information.'",
            "Safe tasks do not involve learner data, safeguarding, HR, or professional decisions.",
        ],
    },
    {
        "question_id": "reflection_002",
        "topic": "learner data boundaries",
        "question": (
            "What is one type of information you must never enter into an AI tool — "
            "and what would you do instead if you needed help with that task?"
        ),
        "guidance_points": [
            "Prohibited information includes: learner names, attendance data, assessment records, safeguarding details, HR records, personal data.",
            "Instead: convert the task to a generic template using AI, then personalise manually.",
            "Or: check with manager or data protection lead whether an approved tool exists.",
            "Or: carry out the task without AI if no safe option is available.",
        ],
    },
    {
        "question_id": "reflection_003",
        "topic": "human review",
        "question": (
            "What checks should you complete before using AI-generated content "
            "in a lesson or sharing it with learners?"
        ),
        "guidance_points": [
            "Check factual accuracy — verify statistics, citations, and legal references independently.",
            "Check tone — is it appropriate for the audience?",
            "Check fairness — does it include bias, stereotyping, or exclusionary language?",
            "Check accessibility — is it inclusive for all learners?",
            "Check policy alignment — is it consistent with organisational and sector policy?",
            "Final responsibility remains with the staff member who uses the content.",
        ],
    },
    {
        "question_id": "reflection_004",
        "topic": "escalation routes",
        "question": (
            "Who should you escalate to if you are unsure whether an AI use is safe — "
            "and what would prompt you to escalate?"
        ),
        "guidance_points": [
            "Escalate to: manager, safeguarding lead (for safeguarding concerns), data protection lead (for data concerns), quality lead (for content concerns).",
            "Escalate if: unsure whether a tool is approved, unsure whether data is safe to use, unsure whether an output is accurate or fair.",
            "Escalate if: a safeguarding concern arises during AI use.",
            "Escalate if: you may have accidentally entered personal or regulated data into an unapproved tool.",
            "Do not proceed if you are unsure — stop and ask.",
        ],
    },
    {
        "question_id": "reflection_005",
        "topic": "accountability",
        "question": (
            "If an AI tool makes a mistake in a document you used with learners, "
            "who is responsible — and how would you prevent this situation?"
        ),
        "guidance_points": [
            "The staff member who reviewed and used the document is professionally responsible.",
            "AI tools do not hold accountability — they produce outputs that humans must review.",
            "Prevention: review all AI output before use for accuracy, fairness, tone, and policy alignment.",
            "Prevention: do not use AI output for formal, accredited, safeguarding, HR, or legal documents without significant caution.",
        ],
    },
]


def get_default_question_topics() -> list:
    """Return the list of question topics covered in the knowledge check."""
    return [
        "safe prompting",
        "learner data boundaries",
        "safeguarding boundaries",
        "approved tools",
        "human review",
        "hallucination and accuracy",
        "bias and fairness",
        "accountability",
        "escalation routes",
        "prohibited AI uses",
    ]


def generate_multiple_choice_questions(
    scenario: dict,
    assessment: dict | None = None,
    handout: dict | None = None,
    question_count: int = 10,
) -> list:
    """Return a list of multiple-choice question dicts.

    Draws from _MCQ_BANK. If question_count exceeds the bank size, returns
    the full bank. Defaults to 10 if question_count is invalid.
    """
    if not isinstance(question_count, int) or question_count < 1:
        question_count = 10

    return _MCQ_BANK[:min(question_count, len(_MCQ_BANK))]


def generate_scenario_questions(
    scenario: dict,
    assessment: dict | None = None,
    activities: list | None = None,
) -> list:
    """Return a list of scenario question dicts."""
    return list(_SCENARIO_BANK)


def generate_short_reflection_questions(
    scenario: dict,
    assessment: dict | None = None,
) -> list:
    """Return a list of short reflection question dicts."""
    questions = list(_REFLECTION_BANK)

    if assessment:
        high_priority = [
            t.get("title", "").lower()
            for t in assessment.get("topic_assessments", [])
            if t.get("priority_level") == "high"
        ]
        if any("bias" in t or "fairness" in t for t in high_priority):
            questions.append({
                "question_id": "reflection_006",
                "topic": "bias and fairness",
                "question": (
                    "Describe a situation where AI output might be biased or unfair "
                    "when used in a training context — and how you would identify and correct it."
                ),
                "guidance_points": [
                    "AI tools can reproduce stereotypes or exclude groups not well represented in training data.",
                    "Watch for: homogeneous examples, exclusionary language, assumptions about ability or background.",
                    "Review: does the content represent diverse learners fairly?",
                    "Correct by: revising content to be inclusive, seeking quality lead review.",
                ],
            })

    return questions


def generate_answer_key(
    multiple_choice_questions: list,
    scenario_questions: list,
    reflection_questions: list,
) -> dict:
    """Return an answer key dict covering all question types."""
    mcq_answers = [
        {
            "question_id": q["question_id"],
            "question": q["question"],
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"],
        }
        for q in multiple_choice_questions
    ]

    scenario_guidance = [
        {
            "question_id": q["question_id"],
            "topic": q["topic"],
            "scenario": q["scenario"],
            "model_answer": q["model_answer"],
            "expected_answer_points": q["expected_answer_points"],
        }
        for q in scenario_questions
    ]

    reflection_guidance = [
        {
            "question_id": q["question_id"],
            "topic": q["topic"],
            "question": q["question"],
            "guidance_points": q["guidance_points"],
        }
        for q in reflection_questions
    ]

    return {
        "multiple_choice_answers": mcq_answers,
        "scenario_answer_guidance": scenario_guidance,
        "reflection_guidance": reflection_guidance,
        "marking_note": _MARKING_NOTE,
    }


def generate_knowledge_check(
    scenario: dict,
    assessment: dict | None = None,
    workshop_plan: dict | None = None,
    activities: list | None = None,
    facilitator_guide: dict | None = None,
    handout: dict | None = None,
    question_count: int = 10,
) -> dict:
    """Generate and return a complete knowledge check dict."""
    if scenario is None:
        scenario = {}

    if not isinstance(question_count, int) or question_count < 1:
        question_count = 10

    org = scenario.get("organisation_name", "Unnamed organisation")
    audience = scenario.get("staff_roles", ["All staff"])
    if not audience:
        audience = ["All staff"]

    purpose_lines = [
        f"This knowledge check helps staff at {org} confirm their understanding of "
        "responsible AI use before or after the workshop.",
        "It covers safe prompting, learner data boundaries, safeguarding boundaries, "
        "approved tools, human review, hallucination and accuracy risks, bias and fairness, "
        "escalation routes, accountability, and prohibited AI uses.",
        "All scenarios in this knowledge check are synthetic — they do not contain real "
        "learner, safeguarding, or personal data.",
    ]
    if workshop_plan:
        purpose_lines.append(
            f"This check supports the '{workshop_plan.get('workshop_title', 'Responsible AI Workshop')}'."
        )

    purpose = " ".join(purpose_lines)

    instructions = (
        "Answer all multiple-choice questions by selecting one option (A, B, C, or D). "
        "For scenario questions, write your response in your own words. "
        "For reflection questions, consider your own practice and note your answers. "
        "There are no trick questions — the goal is to confirm safe and responsible AI use. "
        "All scenarios are synthetic examples — do not use real learner or case information in your answers."
    )

    pass_guidance = (
        f"Suggested pass threshold: {max(question_count - 2, int(question_count * 0.8))} "
        f"out of {question_count} multiple-choice questions. "
        "If staff miss questions on learner data, safeguarding, approved tools, or escalation routes, "
        "the trainer should review those topics before staff use AI for work tasks."
    )

    review_guidance = (
        "Scenario and reflection answers should be reviewed qualitatively by a facilitator or manager. "
        "There is no single correct answer — look for key points: "
        "no AI for safeguarding decisions, no real data in prompts, human review required, "
        "use approved tools, escalate uncertainty."
    )

    mcqs = generate_multiple_choice_questions(scenario, assessment, handout, question_count)
    scenario_qs = generate_scenario_questions(scenario, assessment, activities)
    reflection_qs = generate_short_reflection_questions(scenario, assessment)
    answer_key = generate_answer_key(mcqs, scenario_qs, reflection_qs)

    return {
        "knowledge_check_title": "Responsible AI Staff Knowledge Check",
        "organisation_name": org,
        "audience": audience,
        "purpose": purpose,
        "instructions": instructions,
        "multiple_choice_questions": mcqs,
        "scenario_questions": scenario_qs,
        "reflection_questions": reflection_qs,
        "answer_key": answer_key,
        "pass_guidance": pass_guidance,
        "review_guidance": review_guidance,
        "responsible_use_warning": _RESPONSIBLE_USE_WARNING,
        "prototype_note": _PROTOTYPE_NOTE,
    }


def summarise_knowledge_check(knowledge_check: dict) -> dict:
    """Return a compact summary dict for the knowledge check."""
    answer_key = knowledge_check.get("answer_key", {})
    return {
        "organisation_name": knowledge_check.get("organisation_name", ""),
        "audience_roles": knowledge_check.get("audience", []),
        "mcq_count": len(knowledge_check.get("multiple_choice_questions", [])),
        "scenario_question_count": len(knowledge_check.get("scenario_questions", [])),
        "reflection_question_count": len(knowledge_check.get("reflection_questions", [])),
        "answer_key_included": bool(answer_key),
        "total_question_count": (
            len(knowledge_check.get("multiple_choice_questions", []))
            + len(knowledge_check.get("scenario_questions", []))
            + len(knowledge_check.get("reflection_questions", []))
        ),
    }


def format_knowledge_check_as_markdown(
    knowledge_check: dict,
    include_answer_key: bool = True,
) -> str:
    """Return the knowledge check formatted as a Markdown string."""
    lines = []

    lines.append("# Responsible AI Staff Knowledge Check")
    lines.append("")

    # Organisation
    lines.append("## Organisation")
    lines.append("")
    lines.append(f"**{knowledge_check.get('organisation_name', 'Unnamed organisation')}**")
    audience = knowledge_check.get("audience", [])
    if audience:
        lines.append(f"**Audience:** {', '.join(audience)}")
    lines.append("")

    # Purpose
    lines.append("## Purpose")
    lines.append("")
    lines.append(knowledge_check.get("purpose", ""))
    lines.append("")

    # Instructions
    lines.append("## Instructions")
    lines.append("")
    lines.append(knowledge_check.get("instructions", ""))
    lines.append("")

    # Multiple-choice questions
    lines.append("## Multiple-Choice Questions")
    lines.append("")
    for q in knowledge_check.get("multiple_choice_questions", []):
        lines.append(f"**{q['question_id'].upper()}. {q['question']}**")
        lines.append("")
        for letter, text in q.get("options", {}).items():
            lines.append(f"{letter}. {text}")
        lines.append("")

    # Scenario questions
    lines.append("## Scenario Questions")
    lines.append("")
    for q in knowledge_check.get("scenario_questions", []):
        lines.append(f"**{q['question_id'].upper()}. Scenario: {q['topic'].title()}**")
        lines.append("")
        lines.append(f"*{q['scenario']}*")
        lines.append("")
        lines.append(f"**Question:** {q['question']}")
        lines.append("")
        lines.append("*Your answer:*")
        lines.append("")

    # Reflection questions
    lines.append("## Reflection Questions")
    lines.append("")
    lines.append("Answer these questions in your own words:")
    lines.append("")
    for q in knowledge_check.get("reflection_questions", []):
        lines.append(f"**{q['question_id'].upper()}.** {q['question']}")
        lines.append("")
        lines.append("*Your answer:*")
        lines.append("")

    # Answer key
    if include_answer_key:
        lines.append("## Answer Key")
        lines.append("")
        lines.append(f"*{knowledge_check.get('answer_key', {}).get('marking_note', '')}*")
        lines.append("")

        lines.append("### Multiple-Choice Answers")
        lines.append("")
        for answer in knowledge_check.get("answer_key", {}).get("multiple_choice_answers", []):
            lines.append(f"**{answer['question_id'].upper()}:** Correct answer: **{answer['correct_answer']}**")
            lines.append("")
            lines.append(f"*{answer['explanation']}*")
            lines.append("")

        lines.append("### Scenario Answer Guidance")
        lines.append("")
        for guidance in knowledge_check.get("answer_key", {}).get("scenario_answer_guidance", []):
            lines.append(f"**{guidance['question_id'].upper()} — {guidance['topic'].title()}**")
            lines.append("")
            lines.append(f"**Model answer:** {guidance['model_answer']}")
            lines.append("")
            lines.append("**Key points to look for:**")
            for point in guidance.get("expected_answer_points", []):
                lines.append(f"- {point}")
            lines.append("")

        lines.append("### Reflection Guidance")
        lines.append("")
        for guidance in knowledge_check.get("answer_key", {}).get("reflection_guidance", []):
            lines.append(f"**{guidance['question_id'].upper()} — {guidance['topic'].title()}**")
            lines.append("")
            for point in guidance.get("guidance_points", []):
                lines.append(f"- {point}")
            lines.append("")

    # Pass and review guidance
    lines.append("## Pass and Review Guidance")
    lines.append("")
    lines.append(knowledge_check.get("pass_guidance", ""))
    lines.append("")
    lines.append(knowledge_check.get("review_guidance", ""))
    lines.append("")

    # Responsible-use boundaries
    lines.append("## Prototype and Responsible-Use Boundaries")
    lines.append("")
    lines.append(f"> {knowledge_check.get('responsible_use_warning', '')}")
    lines.append("")
    lines.append(knowledge_check.get("prototype_note", ""))
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "*Build 4 · AI Staff Training and Workshop Generator · BrightPath ChatGPT Mastery Project*"
    )
    lines.append("*All scenarios are synthetic. Outputs require human review before use.*")

    return "\n".join(lines)


def create_knowledge_check_filename(organisation_name: str) -> str:
    """Return a safe kebab-case filename for the knowledge check."""
    if not organisation_name:
        organisation_name = "organisation"
    slug = organisation_name.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return f"knowledge-check-{slug}.md"
