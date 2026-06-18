"""
Tests for src/brief_generator.py

Run from the project root:  pytest
"""

from src.brief_generator import (
    generate_short_answer,
    deduplicate_list,
    generate_next_actions,
    generate_markdown_brief,
    create_brief_filename,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_EVIDENCE = [
    {
        "topic": "safeguarding",
        "document_name": "doc_a.md",
        "line_number": 2,
        "evidence_text": "Staff must not enter safeguarding case details into any AI tool.",
        "matched_keywords": ["safeguarding"],
        "relevance_count": 1,
    },
    {
        "topic": "learner data",
        "document_name": "doc_a.md",
        "line_number": 1,
        "evidence_text": "Staff must not enter learner data into AI tools.",
        "matched_keywords": ["learner data"],
        "relevance_count": 1,
    },
]

SAMPLE_RISK_ITEMS = [
    {
        "topic": "safeguarding",
        "risk_title": "Safeguarding information mishandled through AI tools",
        "risk_description": "Staff may enter safeguarding case details into AI tools.",
        "why_it_matters": "Safeguarding decisions require trained human judgement.",
        "recommended_safeguards": [
            "Do not enter safeguarding case details into AI tools.",
            "Escalate concerns to the safeguarding lead.",
        ],
        "suggested_owner": "Safeguarding lead",
        "evidence_items": SAMPLE_EVIDENCE[:1],
        "evidence_count": 1,
        "coverage_note": "Limited evidence found.",
    },
]

SAMPLE_BRIEF_DATA = {
    "title": "Safeguarding and AI Boundaries",
    "question": "What does the policy say about safeguarding and AI?",
    "topics": ["safeguarding"],
    "documents_reviewed": ["synthetic-safeguarding-and-ai-boundaries.md"],
    "generated_date": "10 June 2026",
    "short_answer": "Safeguarding case details should not be entered into AI tools.",
    "evidence_results": SAMPLE_EVIDENCE[:1],
    "risk_summary_items": SAMPLE_RISK_ITEMS,
    "next_actions": ["Review the relevant source policy sections."],
}


# ── generate_short_answer ─────────────────────────────────────────────────────

def test_generate_short_answer_returns_string():
    result = generate_short_answer("What about safeguarding?", ["safeguarding"], SAMPLE_EVIDENCE)
    assert isinstance(result, str)


def test_generate_short_answer_safeguarding_produces_relevant_text():
    result = generate_short_answer("", ["safeguarding"], SAMPLE_EVIDENCE)
    assert "safeguarding" in result.lower()


def test_generate_short_answer_learner_data_produces_relevant_text():
    result = generate_short_answer("", ["learner data"], SAMPLE_EVIDENCE)
    assert "learner" in result.lower()


def test_generate_short_answer_empty_topics_returns_cautious_answer():
    result = generate_short_answer("Any question?", [], [])
    assert "review" in result.lower() or "evidence" in result.lower()


def test_generate_short_answer_multiple_topics_combines_answers():
    single = generate_short_answer("", ["safeguarding"], SAMPLE_EVIDENCE)
    multi = generate_short_answer("", ["safeguarding", "learner data"], SAMPLE_EVIDENCE)
    assert len(multi) >= len(single)


def test_generate_short_answer_unknown_topic_returns_cautious_answer():
    result = generate_short_answer("question", ["xyz_unknown_topic"], [])
    assert isinstance(result, str) and len(result) > 0


def test_generate_short_answer_empty_evidence_still_returns_template_if_known_topic():
    result = generate_short_answer("", ["safeguarding"], [])
    assert "safeguarding" in result.lower()


# ── deduplicate_list ──────────────────────────────────────────────────────────

def test_deduplicate_list_returns_list():
    assert isinstance(deduplicate_list(["a", "b"]), list)


def test_deduplicate_list_removes_duplicates():
    result = deduplicate_list(["a", "b", "a", "c"])
    assert result.count("a") == 1


def test_deduplicate_list_preserves_order():
    result = deduplicate_list(["c", "a", "b", "a", "c"])
    assert result == ["c", "a", "b"]


def test_deduplicate_list_empty_returns_empty():
    assert deduplicate_list([]) == []


def test_deduplicate_list_no_duplicates_unchanged():
    items = ["x", "y", "z"]
    assert deduplicate_list(items) == items


# ── generate_next_actions ─────────────────────────────────────────────────────

def test_generate_next_actions_returns_list():
    assert isinstance(generate_next_actions(["safeguarding"], SAMPLE_EVIDENCE), list)


def test_generate_next_actions_contains_review_action():
    result = generate_next_actions(["safeguarding"], SAMPLE_EVIDENCE)
    assert any("Review" in a for a in result)


def test_generate_next_actions_contains_responsible_owner_action():
    result = generate_next_actions(["safeguarding"], SAMPLE_EVIDENCE)
    assert any("responsible owner" in a.lower() or "Confirm" in a for a in result)


def test_generate_next_actions_learner_data_adds_topic_specific_action():
    result = generate_next_actions(["learner data"], SAMPLE_EVIDENCE)
    assert any("learner" in a.lower() for a in result)


def test_generate_next_actions_result_has_no_duplicates():
    result = generate_next_actions(["safeguarding", "learner data"], SAMPLE_EVIDENCE)
    assert len(result) == len(set(result))


def test_generate_next_actions_empty_topics_returns_universal_actions():
    result = generate_next_actions([], [])
    assert len(result) >= 1


# ── generate_markdown_brief ───────────────────────────────────────────────────

def test_generate_markdown_brief_returns_string():
    assert isinstance(generate_markdown_brief(SAMPLE_BRIEF_DATA), str)


def test_generate_markdown_brief_contains_title():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Safeguarding and AI Boundaries" in md


def test_generate_markdown_brief_contains_question_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Question / Topic" in md


def test_generate_markdown_brief_contains_documents_reviewed_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Documents Reviewed" in md


def test_generate_markdown_brief_contains_short_answer_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Short Answer" in md


def test_generate_markdown_brief_contains_evidence_found_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Evidence Found" in md


def test_generate_markdown_brief_contains_key_risks_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Key Risks" in md


def test_generate_markdown_brief_contains_safeguards_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Recommended Safeguards" in md


def test_generate_markdown_brief_contains_next_actions_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Suggested Next Actions" in md


def test_generate_markdown_brief_contains_limitations_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Limitations and Responsible Use" in md


def test_generate_markdown_brief_contains_reviewer_notes_section():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "Notes for Reviewer" in md


def test_generate_markdown_brief_limitations_contains_required_text():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "deterministic keyword" in md


def test_generate_markdown_brief_limitations_contains_real_data_warning():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "real learner data" in md or "real" in md.lower()


def test_generate_markdown_brief_includes_document_name_in_evidence():
    md = generate_markdown_brief(SAMPLE_BRIEF_DATA)
    assert "doc_a.md" in md


def test_generate_markdown_brief_empty_brief_data_still_returns_string():
    md = generate_markdown_brief({})
    assert isinstance(md, str)
    assert "Evidence Found" in md


def test_generate_markdown_brief_generates_short_answer_if_absent():
    data = {**SAMPLE_BRIEF_DATA, "short_answer": ""}
    md = generate_markdown_brief(data)
    assert "Short Answer" in md


# ── create_brief_filename ─────────────────────────────────────────────────────

def test_create_brief_filename_returns_string():
    assert isinstance(create_brief_filename("My Brief"), str)


def test_create_brief_filename_returns_md_extension():
    assert create_brief_filename("My Brief").endswith(".md")


def test_create_brief_filename_creates_lowercase_slug():
    result = create_brief_filename("Learner Data Policy")
    assert result == "learner-data-policy.md"


def test_create_brief_filename_strips_special_characters():
    result = create_brief_filename("Safeguarding & AI: Boundaries!")
    assert "&" not in result
    assert ":" not in result
    assert "!" not in result


def test_create_brief_filename_empty_title_returns_default():
    assert create_brief_filename("") == "document-intelligence-mini-brief.md"


def test_create_brief_filename_whitespace_title_returns_default():
    assert create_brief_filename("   ") == "document-intelligence-mini-brief.md"


def test_create_brief_filename_hyphens_separate_words():
    result = create_brief_filename("AI Output Quality")
    assert result == "ai-output-quality.md"
