"""
sample_data.py — shared constants and demo data for the Document Intelligence Demo.
"""

from pathlib import Path

# Absolute path to the synthetic documents folder
DOCS_DIR = Path(__file__).parent.parent / "data" / "synthetic_documents"

# Topics available for evidence extraction (matches TOPIC_KEYWORDS keys)
DEMO_TOPICS = [
    "learner data",
    "safeguarding",
    "human review",
    "approved tools",
    "accountability",
    "bias",
    "hallucination",
    "copyright",
    "escalation",
    "data minimisation",
    "anonymisation",
    "retention",
    "incident reporting",
]

# Example queries for the Document Viewer search bar
DEMO_QUERIES = [
    "learner data",
    "safeguarding",
    "human review",
    "approved tools",
    "hallucination",
    "copyright",
    "escalation",
    "accountability",
    "bias",
]

# Pre-filled demo data for the Mini Brief page
DEMO_BRIEF_DATA = {
    "title": "Policy Evidence Brief: Safeguarding and AI Use",
    "documents_reviewed": [
        "synthetic-safeguarding-and-ai-boundaries.md",
        "synthetic-ai-acceptable-use-policy.md",
    ],
    "question": "What safeguarding boundaries apply to AI use at BrightPath?",
    "evidence": [
        "Staff must never enter safeguarding information into any AI tool.",
        "All safeguarding matters must be escalated to the Designated Safeguarding Lead (DSL).",
        "AI tools must not be used to process, store, respond to, or record safeguarding information.",
        "AI cannot assess risk, judge the credibility of a disclosure, or make any safeguarding decision.",
        "All AI-generated content must be reviewed by a member of staff before it is shared or acted upon.",
    ],
    "key_risks": [
        "Accidental entry of safeguarding case details into an AI tool",
        "Over-reliance on AI outputs without human review",
        "Staff not understanding the boundary between safe admin use and prohibited use",
        "AI tool generating plausible-sounding but incorrect safeguarding guidance",
    ],
    "safeguards": [
        "Clear policy prohibiting AI use for any safeguarding information",
        "Staff training on safe and unsafe prompts (see staff training notes)",
        "Escalation pathway to DSL for all safeguarding concerns — not AI tools",
        "Human review required before any AI-generated content is acted upon",
        "Incident reporting pathway for suspected policy breaches",
    ],
    "limitations": [
        "This brief is generated from synthetic documents using keyword matching only.",
        "Real policy documents require review by qualified legal and safeguarding professionals.",
        "This prototype is for demonstration and planning purposes only.",
        "Evidence extraction does not guarantee completeness — full document review is required.",
    ],
}
