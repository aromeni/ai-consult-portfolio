"""
Rule-based governance and risk checks for Build 11.

Scans text (query or document chunks) for governance risk signals.
Returns structured risk flags with category, level, and recommended action.
Does not claim to be a complete or infallible classifier.
"""

from __future__ import annotations

RISK_CATEGORIES = {
    "learner_data": {
        "terms": [
            "learner name", "learner id", "learner record", "attendance", "assessment result",
            "progress review", "ilp", "individual learning plan", "learner reference",
        ],
        "level": "High",
        "action": "Do not process identifiable learner data in any AI tool. Anonymise or use synthetic examples only.",
    },
    "safeguarding": {
        "terms": [
            "safeguarding", "disclosure", "referral", "child protection", "vulnerable adult",
            "abuse", "neglect", "exploitation", "welfare concern", "prevent", "radicalisation",
        ],
        "level": "High",
        "action": "Safeguarding matters must be handled exclusively through approved safeguarding procedures. AI tools must not be used.",
    },
    "assessment_decisions": {
        "terms": [
            "grade", "pass", "fail", "mark", "assessment decision", "grade appeal",
            "grading", "exam result", "qualification outcome",
        ],
        "level": "High",
        "action": "Assessment and grading decisions require professional human judgement. AI must not be used to determine or recommend grades.",
    },
    "disciplinary_complaints": {
        "terms": [
            "disciplinary", "complaint", "grievance", "misconduct", "investigation",
            "formal warning", "dismissal", "tribunal",
        ],
        "level": "High",
        "action": "Disciplinary and complaints matters require expert HR and legal judgement. AI must not be used in these processes.",
    },
    "personal_data": {
        "terms": [
            "personal data", "name and address", "date of birth", "national insurance",
            "passport", "bank details", "email address", "phone number", "home address",
            "staff record", "hr record",
        ],
        "level": "Medium",
        "action": "Personal data must not be entered into AI tools without a lawful basis and appropriate data processing agreement.",
    },
    "confidential_data": {
        "terms": [
            "confidential", "commercially sensitive", "client contract", "partner agreement",
            "financial data", "budget", "undisclosed",
        ],
        "level": "Medium",
        "action": "Confidential and commercially sensitive information must not be shared with AI tools without explicit approval.",
    },
    "funding_eligibility": {
        "terms": [
            "funding eligibility", "esfa", "ofsted", "funding claim", "eligibility decision",
            "contract compliance", "audit", "subcontractor",
        ],
        "level": "Medium",
        "action": "Funding eligibility and compliance determinations require qualified human review and must not rely on AI outputs.",
    },
    "human_approval_missing": {
        "terms": [
            "without review", "no approval", "skip review", "not been checked",
            "automatically approved", "ai decided",
        ],
        "level": "Medium",
        "action": "All AI outputs must be reviewed and approved by a qualified member of staff before use or distribution.",
    },
}

_RISK_LEVEL_ORDER = {"High": 3, "Medium": 2, "Low": 1}


def check_text(text: str) -> list[dict]:
    """
    Scan text for governance risk signals.

    Returns a list of risk flag dicts, each with:
        category (str), risk_level (str), matched_terms (list[str]),
        recommended_action (str).
    Returns an empty list if no risks detected.
    """
    lowered = text.lower()
    flags = []
    for category, config in RISK_CATEGORIES.items():
        matched = [term for term in config["terms"] if term in lowered]
        if matched:
            flags.append({
                "category": category,
                "risk_level": config["level"],
                "matched_terms": matched,
                "recommended_action": config["action"],
            })
    return flags


def check_query(query: str) -> list[dict]:
    """Check a user query for governance risks. Wrapper around check_text."""
    return check_text(query)


def check_chunks(chunks: list[dict]) -> list[dict]:
    """Check a list of retrieved chunks for governance risks. Returns deduplicated flags."""
    category_flags: dict[str, dict] = {}
    for chunk in chunks:
        for flag in check_text(chunk.get("text", "")):
            cat = flag["category"]
            if cat not in category_flags:
                category_flags[cat] = {
                    "category": cat,
                    "risk_level": flag["risk_level"],
                    "matched_terms": list(flag["matched_terms"]),
                    "recommended_action": flag["recommended_action"],
                }
            else:
                existing_terms = category_flags[cat]["matched_terms"]
                for term in flag["matched_terms"]:
                    if term not in existing_terms:
                        existing_terms.append(term)
    return list(category_flags.values())


def summarise_risk_flags(flags: list[dict]) -> dict:
    """
    Return a summary of risk flags.

    Includes: total_flags (int), high_count (int), medium_count (int),
    low_count (int), categories (list[str]).
    """
    return {
        "total_flags": len(flags),
        "high_count": sum(1 for f in flags if f["risk_level"] == "High"),
        "medium_count": sum(1 for f in flags if f["risk_level"] == "Medium"),
        "low_count": sum(1 for f in flags if f["risk_level"] == "Low"),
        "categories": [f["category"] for f in flags],
    }


def highest_risk_level(flags: list[dict]) -> str:
    """Return the highest risk level present in a list of flags, or 'None' if empty."""
    if not flags:
        return "None"
    return max(flags, key=lambda f: _RISK_LEVEL_ORDER.get(f["risk_level"], 0))["risk_level"]
