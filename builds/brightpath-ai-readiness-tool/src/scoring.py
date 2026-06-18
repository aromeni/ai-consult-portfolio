"""
Scoring logic for the BrightPath AI Readiness + Workflow Audit Tool.

Phase 1 — demo scoring (5 dimensions, 1–5 scale, total 5–25)
Phase 2 — full readiness assessment (10 dimensions, 0–10 scale, total 0–100)
"""

# ── Phase 1: demo scoring ─────────────────────────────────────────────────────

DIMENSION_LABELS = {
    "data_awareness": "Data Awareness",
    "prompt_skill": "Prompt Skill",
    "output_review": "Output Review",
    "governance": "Governance",
    "manager_oversight": "Manager Oversight",
}

SCORE_BANDS = [
    (21, 25, "Strong", "green",
     "The organisation has a good foundation for AI adoption. "
     "Recommend a structured pilot with one or two low-risk workflows."),
    (15, 20, "Developing", "orange",
     "Partial readiness. Training and a data protection briefing are needed "
     "before live workflow adoption. Recommend a 90-minute workshop first."),
    (10, 14, "Early", "red",
     "Significant gaps in awareness, governance, or review practice. "
     "Recommend a full half-day programme before any AI use in live workflows."),
    (5, 9, "Not ready", "red",
     "Critical gaps identified. Data protection and governance controls must be "
     "established before any AI tool use. Do not proceed to pilot without "
     "policy, approved tools, and a manager briefing in place."),
]

RISK_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


def total_readiness_score(responses: dict) -> int:
    return sum(responses.values())


def readiness_band(score: int) -> dict:
    for low, high, label, colour, recommendation in SCORE_BANDS:
        if low <= score <= high:
            return {
                "label": label,
                "colour": colour,
                "recommendation": recommendation,
                "score": score,
                "max": 25,
            }
    return {
        "label": "Unknown",
        "colour": "grey",
        "recommendation": "Score out of expected range.",
        "score": score,
        "max": 25,
    }


def workflow_summary(workflows: list) -> dict:
    suitable = [w for w in workflows if w["ai_suitable"] is True]
    borderline = [w for w in workflows if w["ai_suitable"] is None]
    unsuitable = [w for w in workflows if w["ai_suitable"] is False]
    high_risk = [
        w for w in workflows if w["risk_level"] in ("High", "Critical")
    ]
    return {
        "suitable_count": len(suitable),
        "borderline_count": len(borderline),
        "unsuitable_count": len(unsuitable),
        "high_risk_count": len(high_risk),
        "suitable": suitable,
        "borderline": borderline,
        "unsuitable": unsuitable,
        "high_risk": high_risk,
    }


def pilot_workflow_candidates(workflows: list) -> list:
    suitable = [w for w in workflows if w["ai_suitable"] is True]
    return sorted(suitable, key=lambda w: RISK_ORDER.get(w["risk_level"], 99))


# ── Phase 2: full readiness assessment (0–100) ────────────────────────────────

READINESS_DIMENSIONS = [
    {
        "key": "workflow_clarity",
        "label": "Workflow Clarity",
        "question": (
            "How clearly has the organisation identified specific workflows "
            "it wants to improve with AI?"
        ),
        "hint": (
            "Think about whether target workflows are documented, understood by staff, "
            "and produce outputs that could be measured."
        ),
    },
    {
        "key": "ai_awareness",
        "label": "AI Awareness",
        "question": "How well do staff understand what AI tools can and cannot do?",
        "hint": (
            "Consider whether staff know about hallucination, AI limitations, "
            "and the difference between useful and risky use cases."
        ),
    },
    {
        "key": "data_sensitivity",
        "label": "Data Sensitivity and Control",
        "question": (
            "How well does the organisation control which data enters AI tools?"
        ),
        "hint": (
            "Consider whether prohibited data categories are defined and whether "
            "staff know not to enter learner, client, or confidential information."
        ),
    },
    {
        "key": "staff_capability",
        "label": "Staff Capability",
        "question": (
            "How confidently can staff use AI tools safely and effectively "
            "for their work tasks?"
        ),
        "hint": (
            "Think about whether staff can write a structured prompt, review an output "
            "critically, and recognise when not to use AI."
        ),
    },
    {
        "key": "leadership_support",
        "label": "Leadership Support",
        "question": (
            "How actively does senior leadership support responsible AI adoption?"
        ),
        "hint": (
            "Consider whether leadership has engaged with AI readiness and is willing "
            "to invest time in governance, training, and oversight."
        ),
    },
    {
        "key": "governance_maturity",
        "label": "Governance Maturity",
        "question": (
            "How mature is the organisation's AI governance — "
            "policies, approved tools, and escalation routes?"
        ),
        "hint": (
            "Think about whether an AI acceptable use policy exists, approved tools "
            "are defined, and staff know how to escalate concerns."
        ),
    },
    {
        "key": "technical_readiness",
        "label": "Technical Readiness",
        "question": (
            "How well-equipped is the organisation's technical setup "
            "to support AI tools safely?"
        ),
        "hint": (
            "Consider whether staff have access to approved tools, devices, "
            "and the connectivity needed to use AI at work."
        ),
    },
    {
        "key": "business_need",
        "label": "Measurable Business Need",
        "question": (
            "How clearly can the organisation articulate what it wants AI to improve "
            "and how success will be measured?"
        ),
        "hint": (
            "Think about whether specific, measurable outcomes exist — not just "
            "'save time' but which tasks, for which roles, and by how much."
        ),
    },
    {
        "key": "implementation_capacity",
        "label": "Implementation Capacity",
        "question": (
            "Does the organisation have the time, resource, and management bandwidth "
            "to run a structured AI pilot?"
        ),
        "hint": (
            "Consider whether a manager can oversee the pilot, staff have capacity "
            "to practise, and a review process can be put in place."
        ),
    },
    {
        "key": "risk_awareness",
        "label": "Risk Awareness",
        "question": (
            "How well does the organisation understand the risks of AI use — "
            "data, accuracy, governance, and accountability?"
        ),
        "hint": (
            "Think about whether risk has been discussed openly, concerns have been "
            "surfaced safely, and accountability for AI outputs is clear."
        ),
    },
]

# Each entry: (min_score, max_score, category, alert_type, explanation, next_action)
READINESS_LEVELS = [
    (
        0, 25,
        "Not ready",
        "error",
        "Critical gaps identified across multiple dimensions. The organisation needs "
        "foundational work on AI awareness, data boundaries, and governance before "
        "any AI tools are used in live workflows.",
        "Focus on basic AI awareness training, data boundaries, and governance "
        "controls before piloting AI. Start with a 60-minute awareness briefing.",
    ),
    (
        26, 50,
        "Early awareness",
        "warning",
        "Initial awareness exists but significant gaps remain in governance, "
        "data control, or staff capability. Some groundwork is in place but "
        "the organisation is not yet ready for a live AI pilot.",
        "Run a structured discovery session and identify 1–2 low-risk workflows. "
        "Deliver a 90-minute safe AI workshop before any live use.",
    ),
    (
        51, 70,
        "Pilot ready with safeguards",
        "info",
        "The organisation has enough foundations to attempt a carefully scoped pilot. "
        "Governance and data controls need to be confirmed before Week 3. "
        "Human review must be applied to all pilot outputs.",
        "Choose one low-risk workflow pilot with human review, clear data rules, "
        "and a manager oversight process. Limit scope until the first review.",
    ),
    (
        71, 85,
        "Implementation ready",
        "success",
        "Strong foundations across most dimensions. The organisation can run a "
        "structured pilot with confidence, provided governance and review processes "
        "are documented and followed.",
        "Build a controlled pilot with defined success metrics, staff guidance, "
        "and a documented review process. Expand to a second workflow after Week 4.",
    ),
    (
        86, 100,
        "Scaling ready",
        "success",
        "The organisation has mature AI readiness across all dimensions. "
        "Governance, capability, and oversight are well-established. "
        "The focus now shifts to consistency, monitoring, and controlled expansion.",
        "Standardise governance, monitor usage against agreed metrics, "
        "and expand only workflows that have been proven in the pilot.",
    ),
]


def calculate_readiness_score(scores: dict) -> int:
    return sum(scores.values())


def get_readiness_level(score: int) -> dict:
    for low, high, category, alert_type, explanation, next_action in READINESS_LEVELS:
        if low <= score <= high:
            return {
                "category": category,
                "alert_type": alert_type,
                "explanation": explanation,
                "next_action": next_action,
                "score": score,
            }
    return {
        "category": "Unknown",
        "alert_type": "info",
        "explanation": "Score out of expected range.",
        "next_action": "Review inputs and recalculate.",
        "score": score,
    }


def get_readiness_category(score: int) -> str:
    return get_readiness_level(score)["category"]


def get_readiness_explanation(score: int) -> str:
    return get_readiness_level(score)["explanation"]


def get_next_action(score: int) -> str:
    return get_readiness_level(score)["next_action"]


# ── Phase 3: workflow suitability scoring (10 dimensions, 0–5 each, total 0–50) ─

WORKFLOW_SCORING_DIMENSIONS = [
    {
        "key": "repetition",
        "label": "Repetition",
        "question": "How repetitive is this workflow?",
        "hint": (
            "A workflow that follows the same steps every time is more suitable "
            "for AI support than one that varies widely between instances."
        ),
    },
    {
        "key": "rule_clarity",
        "label": "Rule Clarity",
        "question": "How clearly defined are the rules and steps in this workflow?",
        "hint": (
            "Well-documented steps with clear inputs, outputs, and decision points "
            "are easier to support with AI than ad hoc or judgement-heavy processes."
        ),
    },
    {
        "key": "document_intensity",
        "label": "Document Intensity",
        "question": "How document or text-intensive is this workflow?",
        "hint": (
            "AI tools work best on text-based tasks: drafting, summarising, "
            "structuring, and reviewing documents. Manual or physical tasks score lower."
        ),
    },
    {
        "key": "time_burden",
        "label": "Time Burden",
        "question": "How significant is the time burden of this workflow?",
        "hint": (
            "Higher time cost for a repetitive task means greater potential value "
            "from AI support. Quick tasks may not justify the review overhead."
        ),
    },
    {
        "key": "risk_manageability",
        "label": "Risk Manageability",
        "question": "How manageable is the risk if AI produces an incorrect output?",
        "hint": (
            "Score high if errors are easy to catch before they cause harm. "
            "Score low if an AI error in this workflow could cause serious consequences."
        ),
    },
    {
        "key": "human_review_feasibility",
        "label": "Human Review Feasibility",
        "question": "How easy is it to add a human review step before the AI output is used?",
        "hint": (
            "AI support is safest when a human can review the output before it is "
            "acted on. Score high if review is straightforward and fast."
        ),
    },
    {
        "key": "business_value",
        "label": "Business Value",
        "question": "How much business value would AI support deliver for this workflow?",
        "hint": (
            "Consider time saved, consistency improved, staff effort released, "
            "or quality gains — relative to the effort of implementing AI support."
        ),
    },
    {
        "key": "staff_readiness",
        "label": "Staff Readiness",
        "question": "How ready and willing are staff to use AI support for this workflow?",
        "hint": (
            "Staff who are curious and capable will use AI support effectively. "
            "Resistance or low capability reduces practical suitability."
        ),
    },
    {
        "key": "data_sensitivity_control",
        "label": "Data Sensitivity Control",
        "question": (
            "How well is data sensitivity managed for this workflow? "
            "(High score = low sensitivity data or strong controls in place)"
        ),
        "hint": (
            "Score high if no personal, learner, client, or confidential data is "
            "involved — or if strong controls prevent prohibited data from entering AI tools. "
            "Score low if sensitive data is regularly part of this workflow."
        ),
    },
    {
        "key": "implementation_simplicity",
        "label": "Implementation Simplicity",
        "question": "How simple would it be to implement AI support for this workflow?",
        "hint": (
            "A prompt-based task with no system integration needed scores high. "
            "A workflow requiring API connections, custom tools, or major process changes scores lower."
        ),
    },
]

# Each entry: (min_score, max_score, category, alert_type, explanation, next_action)
WORKFLOW_SUITABILITY_LEVELS = [
    (
        0, 15,
        "Not suitable",
        "error",
        "This workflow has fundamental barriers to safe AI use — high data sensitivity, "
        "low rule clarity, unmanageable risk, or poor review feasibility. "
        "Introducing AI without resolving these would create more risk than value.",
        "Do not use AI for this workflow. Keep it human-led or redesign "
        "the process first before reconsidering AI support.",
    ),
    (
        16, 25,
        "Needs governance first",
        "warning",
        "Some potential for AI support exists but governance gaps — data boundaries, "
        "approved tools, human review processes, or escalation routes — must be "
        "established before any pilot can safely proceed.",
        "Define data boundaries, approved tools, human review steps, and escalation "
        "rules before piloting AI for this workflow.",
    ),
    (
        26, 35,
        "Needs process redesign first",
        "warning",
        "The workflow has potential but its steps, ownership, inputs, or outputs "
        "are not sufficiently clear to support reliable AI use. Attempting a pilot "
        "now would produce inconsistent results.",
        "Clarify the workflow steps, ownership, inputs, outputs, and success criteria "
        "before adding AI. Document the process first.",
    ),
    (
        36, 42,
        "Good pilot candidate",
        "info",
        "This workflow has good foundations for a structured AI pilot. Data sensitivity "
        "is manageable, human review is feasible, and the potential value is clear. "
        "A controlled pilot with defined success metrics is the right next step.",
        "Pilot AI support with safe inputs, human review at the agreed stage, "
        "and clear success metrics. Review after four weeks before expanding.",
    ),
    (
        43, 50,
        "Quick win",
        "success",
        "This workflow is a strong candidate for immediate, low-risk AI support. "
        "It is text-intensive, repetitive, well-understood, and data-safe. "
        "The main requirement is confirming that data boundaries and review "
        "controls are documented before staff begin.",
        "Consider this a strong low-risk pilot candidate. Confirm data boundaries "
        "and review controls are in place, then begin with a supported trial.",
    ),
]


def calculate_workflow_suitability_score(scores: dict) -> int:
    return sum(scores.values())


def get_workflow_suitability_level(score: int) -> dict:
    for low, high, category, alert_type, explanation, next_action in WORKFLOW_SUITABILITY_LEVELS:
        if low <= score <= high:
            return {
                "category": category,
                "alert_type": alert_type,
                "explanation": explanation,
                "next_action": next_action,
                "score": score,
            }
    return {
        "category": "Unknown",
        "alert_type": "info",
        "explanation": "Score out of expected range.",
        "next_action": "Review inputs and recalculate.",
        "score": score,
    }


def get_workflow_suitability_category(score: int) -> str:
    return get_workflow_suitability_level(score)["category"]


def get_workflow_suitability_explanation(score: int) -> str:
    return get_workflow_suitability_level(score)["explanation"]


def get_workflow_next_action(score: int) -> str:
    return get_workflow_suitability_level(score)["next_action"]


# ── Phase 4: risk assessment (10 categories, likelihood × impact, 1–25) ───────

RISK_CATEGORIES = [
    {
        "key": "data_privacy",
        "label": "Data Privacy",
        "description": (
            "Risk that personal or confidential data enters an AI tool "
            "without appropriate controls."
        ),
    },
    {
        "key": "learner_data",
        "label": "Learner / Client / Staff Data",
        "description": (
            "Risk that identifiable learner, client, or staff data is "
            "processed by an AI tool."
        ),
    },
    {
        "key": "safeguarding",
        "label": "Safeguarding",
        "description": (
            "Risk that safeguarding case details, disclosures, or "
            "vulnerable person information enters an AI tool."
        ),
    },
    {
        "key": "confidentiality",
        "label": "Confidentiality",
        "description": (
            "Risk that confidential organisational, commercial, or "
            "contractual information is disclosed to an AI tool."
        ),
    },
    {
        "key": "accuracy_hallucination",
        "label": "Accuracy and Hallucination",
        "description": (
            "Risk that AI outputs contain errors, invented facts, or "
            "misleading content that is acted on without verification."
        ),
    },
    {
        "key": "bias_fairness",
        "label": "Bias and Fairness",
        "description": (
            "Risk that AI outputs contain unfair assumptions, "
            "discriminatory language, or biased recommendations."
        ),
    },
    {
        "key": "copyright_ip",
        "label": "Copyright and IP",
        "description": (
            "Risk that AI use infringes copyright, intellectual property, "
            "or reuse rights on source material."
        ),
    },
    {
        "key": "security",
        "label": "Security",
        "description": (
            "Risk that credentials, API keys, system details, or sensitive "
            "configurations are exposed through AI tool use."
        ),
    },
    {
        "key": "over_reliance",
        "label": "Over-Reliance",
        "description": (
            "Risk that staff use AI outputs without adequate review, "
            "reducing human judgement and accountability."
        ),
    },
    {
        "key": "accountability",
        "label": "Accountability",
        "description": (
            "Risk that AI-assisted decisions lack a clear responsible owner, "
            "audit trail, or escalation route."
        ),
    },
]

RISK_SAFEGUARDS = {
    "data_privacy": (
        "Use anonymised or synthetic data, minimise inputs, use approved tools, "
        "and avoid sensitive data."
    ),
    "learner_data": (
        "Do not use identifiable learner, client, or staff data in casual AI tools. "
        "Use anonymised examples and human review."
    ),
    "safeguarding": (
        "Do not enter safeguarding case information into AI tools. "
        "Escalate to safeguarding lead and keep process human-led."
    ),
    "confidentiality": (
        "Do not upload confidential documents to unapproved tools. "
        "Use approved systems and access controls."
    ),
    "accuracy_hallucination": (
        "Verify outputs against source material, request evidence, "
        "and require human review before use."
    ),
    "bias_fairness": (
        "Check outputs for unfair assumptions, accessibility issues, "
        "and possible discriminatory effects."
    ),
    "copyright_ip": (
        "Avoid uploading copyrighted or proprietary material without permission. "
        "Check ownership and reuse rights."
    ),
    "security": (
        "Do not expose API keys, passwords, credentials, or system details. "
        "Use secure configuration."
    ),
    "over_reliance": (
        "Use AI as support only. Keep human judgement and accountability "
        "for final decisions."
    ),
    "accountability": (
        "Assign a responsible owner, document decisions, and define review "
        "and escalation routes."
    ),
}

# Risk level thresholds: score = likelihood × impact (1–25)
_RISK_LEVEL_MAP = [
    (1,  4,  "Low",      "Risk appears manageable with standard safeguards and normal human review."),
    (5,  9,  "Moderate", "Risk needs clear safeguards, staff guidance, and review before piloting."),
    (10, 15, "High",     "Risk should not proceed without stronger controls, specialist review, and clear accountability."),
    (16, 25, "Critical", "Do not proceed without formal escalation, governance controls, and senior/specialist review."),
]

_RISK_LEVEL_ORDER = ["Critical", "High", "Moderate", "Low"]


def calculate_risk_score(likelihood: int, impact: int) -> int:
    return likelihood * impact


def get_risk_level(score: int) -> str:
    for low, high, level, _ in _RISK_LEVEL_MAP:
        if low <= score <= high:
            return level
    return "Unknown"


def get_risk_level_explanation(score: int) -> str:
    for low, high, _, explanation in _RISK_LEVEL_MAP:
        if low <= score <= high:
            return explanation
    return "Score out of expected range."


def get_risk_safeguard(risk_category: str, risk_level: str) -> str:
    return RISK_SAFEGUARDS.get(
        risk_category, "Apply appropriate safeguards and human review before use."
    )


def calculate_overall_risk_summary(risk_rows: list) -> dict:
    counts = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}
    for row in risk_rows:
        level = row.get("level", "")
        if level in counts:
            counts[level] += 1

    highest = "Low"
    for level in _RISK_LEVEL_ORDER:
        if counts[level] > 0:
            highest = level
            break

    if counts["Critical"] > 0:
        recommendation = (
            "Do not proceed. Escalate and create governance controls before using AI."
        )
    elif counts["High"] > 0:
        recommendation = (
            "Proceed only after stronger safeguards, specialist review, "
            "and clear accountability."
        )
    elif counts["Moderate"] > 0:
        recommendation = (
            "Pilot only with safeguards, staff guidance, and human review."
        )
    else:
        recommendation = (
            "Suitable for low-risk pilot, assuming data boundaries "
            "and human review are in place."
        )

    return {
        "counts": counts,
        "highest_level": highest,
        "recommendation": recommendation,
    }


# ── Phase 5: pilot recommendation ─────────────────────────────────────────────

_PILOT_ALERT_TYPES = {
    "Not ready for AI pilot": "error",
    "Governance-first before pilot": "warning",
    "Process redesign before AI": "warning",
    "Low-risk pilot candidate": "info",
    "Strong pilot candidate": "success",
    "Ready for controlled implementation": "success",
}

_PILOT_EXPLANATIONS = {
    "Not ready for AI pilot": (
        "Critical or unmanageable risks, low organisational readiness, or serious governance gaps "
        "mean this workflow should not proceed to an AI pilot. "
        "The organisation needs foundational work before any live AI use."
    ),
    "Governance-first before pilot": (
        "High-level risks have been identified that require stronger controls before piloting. "
        "Data boundaries, human review processes, and accountability structures must be confirmed "
        "before any AI tool is used in live work."
    ),
    "Process redesign before AI": (
        "The workflow lacks the clarity, stability, or structure needed to support reliable AI use. "
        "Attempting a pilot now would produce inconsistent results. "
        "Document and simplify the process first, then re-score."
    ),
    "Low-risk pilot candidate": (
        "The organisation, workflow, and risk profile have enough foundations for a carefully scoped pilot. "
        "Safe inputs, human review at a defined stage, and measurable success criteria are the key requirements. "
        "Keep the scope small and review results before expanding."
    ),
    "Strong pilot candidate": (
        "Strong foundations across readiness, workflow clarity, and risk management. "
        "A structured, controlled pilot is appropriate. "
        "Expand to a second workflow only after the first pilot review confirms results."
    ),
    "Ready for controlled implementation": (
        "The organisation appears ready to move beyond a small pilot. "
        "Governance, capability, and oversight are well-established. "
        "Standardise the workflow, document controls, and expand carefully and incrementally."
    ),
}

_PILOT_NEXT_ACTIONS = {
    "Not ready for AI pilot": [
        "Run AI awareness training.",
        "Define data boundaries.",
        "Identify approved tools.",
        "Create basic acceptable-use rules.",
        "Reassess readiness after governance basics are in place.",
    ],
    "Governance-first before pilot": [
        "Complete AI risk assessment.",
        "Define human review process.",
        "Confirm approved tools and data rules.",
        "Escalate high-risk areas to responsible owners.",
        "Select only low-risk workflows for initial testing.",
    ],
    "Process redesign before AI": [
        "Map the workflow steps clearly.",
        "Define inputs, outputs, owners, and success metrics.",
        "Remove unnecessary complexity.",
        "Identify whether AI support is actually needed.",
        "Re-score the workflow after redesign.",
    ],
    "Low-risk pilot candidate": [
        "Start with a 2–4 week limited pilot.",
        "Use safe or anonymised inputs.",
        "Assign a human reviewer.",
        "Track time saved and quality issues.",
        "Review results before wider rollout.",
    ],
    "Strong pilot candidate": [
        "Define a controlled pilot plan.",
        "Train staff on safe use.",
        "Set success metrics.",
        "Monitor risks and output quality.",
        "Prepare an implementation roadmap if the pilot succeeds.",
    ],
    "Ready for controlled implementation": [
        "Standardise the workflow.",
        "Document governance controls.",
        "Train all relevant staff.",
        "Monitor usage and quality.",
        "Expand only after evidence of value and safety.",
    ],
}

# Universal safeguards — applicable regardless of recommendation category.
PILOT_SAFEGUARDS = [
    "Use synthetic or anonymised examples where possible.",
    "Avoid identifiable learner data.",
    "Avoid safeguarding case details.",
    "Avoid confidential client data unless approved and controlled.",
    "Use approved tools only.",
    "Require human review before any external use.",
    "Document assumptions and limitations of AI outputs.",
    "Verify important outputs against source material.",
    "Track issues and apply escalation routes.",
    "Review pilot outcomes before scaling.",
]


def get_pilot_recommendation(
    readiness_score: int,
    workflow_score: int,
    highest_risk_level: str,
    has_critical_risk: bool,
    has_high_risk: bool,
) -> str:
    if has_critical_risk:
        return "Not ready for AI pilot"
    if has_high_risk:
        return "Governance-first before pilot"
    if readiness_score < 51:
        return "Not ready for AI pilot"
    if workflow_score < 26:
        return "Process redesign before AI"
    if readiness_score >= 86 and workflow_score >= 43 and highest_risk_level == "Low":
        return "Ready for controlled implementation"
    if readiness_score >= 71 and workflow_score >= 43 and highest_risk_level in ("Low", "Moderate"):
        return "Strong pilot candidate"
    if readiness_score >= 51 and workflow_score >= 36 and highest_risk_level in ("Low", "Moderate"):
        return "Low-risk pilot candidate"
    return "Not ready for AI pilot"


def get_pilot_recommendation_explanation(
    recommendation: str,
    readiness_score: int,
    workflow_score: int,
    highest_risk_level: str,
) -> str:
    return _PILOT_EXPLANATIONS.get(recommendation, "Review scores and re-assess.")


def get_pilot_next_actions(recommendation: str) -> list:
    return _PILOT_NEXT_ACTIONS.get(recommendation, [])


def get_pilot_safeguards(recommendation: str) -> list:
    return PILOT_SAFEGUARDS
