"""Tests for src/export_utils.py.

All tests use synthetic data. No external APIs. No real data.
Tests verify function contracts and output types — not visual perfection.
"""

import pytest
from src import export_utils as eu
from src import report_analytics as ra


# ── Fixtures ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def minimal_pack_data():
    return {
        "scenario": {
            "organisation_name": "BrightPath Skills Training",
            "organisation_type": "Training Provider",
            "sector": "Education",
            "staff_count": 8,
            "staff_roles": ["Tutors", "Administrators"],
            "priority_topics": ["learner data", "safeguarding"],
            "current_ai_use": "Informal ChatGPT use for lesson planning.",
            "training_goal": "Train staff to use AI responsibly.",
            "main_concerns": ["Learner data misuse", "Hallucination"],
        },
        "training_needs_assessment": {
            "topic_assessments": [
                {"title": "Learner Data", "priority_level": "high"},
                {"title": "Safeguarding", "priority_level": "high"},
            ],
            "recommended_learning_outcomes": [
                "Identify safe AI uses",
                "Recognise prohibited uses",
            ],
        },
        "workshop_plan": {
            "workshop_title": "Responsible AI for BrightPath Staff",
            "duration_minutes": 90,
            "delivery_mode": "In-person workshop",
            "audience": ["Tutors", "Administrators"],
            "learning_outcomes": ["Outcome 1"],
            "agenda": [
                {"section_title": "Welcome", "time_range": "0:00–0:10", "duration_minutes": 10,
                 "purpose": "Introduce session"},
                {"section_title": "Safe Prompting", "time_range": "0:10–0:30", "duration_minutes": 20,
                 "purpose": "Practice safe prompts"},
            ],
            "responsible_use_messages": ["Do not paste learner names into AI tools."],
        },
        "training_activities": [
            {"activity_title": "Sort Prompts", "activity_type": "sorting", "duration_minutes": 15,
             "learning_objective": "Identify safe and unsafe prompts."},
            {"activity_title": "Rewrite Prompt", "activity_type": "rewrite", "duration_minutes": 10,
             "learning_objective": "Rewrite a risky prompt safely."},
        ],
        "staff_handout": {
            "handout_title": "AI Safe Use — BrightPath Staff",
            "safe_use_principles": ["Use AI for generic tasks only."],
            "allowed_ai_uses": ["Generic lesson planning", "Rewriting correspondence"],
            "prohibited_ai_uses": ["Entering learner personal data", "Safeguarding decisions"],
            "human_review_checklist": ["Check for personal data before submitting."],
            "escalation_guidance": [
                {"issue": "Safeguarding", "what_to_do": "Contact DSL immediately."}
            ],
        },
        "knowledge_check": {
            "multiple_choice_questions": [
                {
                    "question_id": "mcq001", "topic": "learner data",
                    "question": "Which prompt is safest?",
                    "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
                    "correct_answer": "B", "explanation": "B avoids personal data.",
                }
            ],
            "scenario_questions": [],
            "reflection_questions": [],
            "answer_key": {"multiple_choice_answers": []},
            "pass_guidance": "Score 8 or more out of 10 to pass.",
        },
        "facilitator_guide": {"guide_title": "Facilitator Guide"},
    }


@pytest.fixture
def sample_analytics(minimal_pack_data):
    return ra.build_training_pack_analytics(minimal_pack_data)


@pytest.fixture
def minimal_markdown():
    return "# Training Pack\n\nSection 1\n\n## Organisation\n\nBrightPath Skills Training\n"


# ── create_safe_filename ──────────────────────────────────────────────────────────

class TestCreateSafeFilename:
    def test_returns_string(self):
        result = eu.create_safe_filename("BrightPath Skills Training", "pdf")
        assert isinstance(result, str)

    def test_contains_extension(self):
        result = eu.create_safe_filename("My Org", "pdf")
        assert result.endswith(".pdf")

    def test_lowercase_kebab(self):
        result = eu.create_safe_filename("BrightPath Skills Training", "pdf")
        assert " " not in result
        assert result == result.lower()

    def test_strips_special_characters(self):
        result = eu.create_safe_filename("Org & Partners (2024)!", "pdf")
        assert "&" not in result
        assert "!" not in result
        assert "(" not in result

    def test_pptx_extension(self):
        result = eu.create_safe_filename("My Pack", "pptx")
        assert result.endswith(".pptx")

    def test_md_extension(self):
        result = eu.create_safe_filename("My Pack", "md")
        assert result.endswith(".md")

    def test_handles_empty_title(self):
        result = eu.create_safe_filename("", "pdf")
        assert result.endswith(".pdf")
        assert len(result) > 4

    def test_handles_non_string_title(self):
        result = eu.create_safe_filename(None, "pdf")
        assert result.endswith(".pdf")

    def test_max_length_not_exceeded(self):
        long_title = "A" * 200
        result = eu.create_safe_filename(long_title, "pdf")
        assert len(result) <= 70  # slug (60) + dot + ext (3)


# ── format_text_for_pdf ───────────────────────────────────────────────────────────

class TestFormatTextForPdf:
    def test_returns_string(self):
        result = eu.format_text_for_pdf("Hello **world**")
        assert isinstance(result, str)

    def test_strips_bold_markers(self):
        result = eu.format_text_for_pdf("**Bold text**")
        assert "**" not in result
        assert "Bold text" in result

    def test_strips_italic_markers(self):
        result = eu.format_text_for_pdf("*italic text*")
        assert "*" not in result

    def test_strips_heading_markers(self):
        result = eu.format_text_for_pdf("## My Heading")
        assert "##" not in result
        assert "My Heading" in result

    def test_strips_inline_code(self):
        result = eu.format_text_for_pdf("`code here`")
        assert "`" not in result
        assert "code here" in result

    def test_handles_empty_string(self):
        result = eu.format_text_for_pdf("")
        assert result == ""

    def test_handles_none(self):
        result = eu.format_text_for_pdf(None)
        assert result == ""

    def test_plain_text_unchanged(self):
        result = eu.format_text_for_pdf("Plain text here")
        assert "Plain text here" in result


# ── format_slide_text ─────────────────────────────────────────────────────────────

class TestFormatSlideText:
    def test_returns_string(self):
        result = eu.format_slide_text("Some text")
        assert isinstance(result, str)

    def test_truncates_at_max_chars(self):
        long_text = "x " * 600
        result = eu.format_slide_text(long_text, max_chars=100)
        assert len(result) <= 104  # max_chars + ellipsis + word boundary slack

    def test_adds_ellipsis_when_truncated(self):
        long_text = "word " * 300
        result = eu.format_slide_text(long_text, max_chars=50)
        assert result.endswith("…")

    def test_short_text_unchanged(self):
        result = eu.format_slide_text("Short text", max_chars=900)
        assert "Short text" in result

    def test_handles_empty_string(self):
        result = eu.format_slide_text("")
        assert result == ""

    def test_handles_none(self):
        result = eu.format_slide_text(None)
        assert result == ""

    def test_strips_markdown(self):
        result = eu.format_slide_text("**Bold** and *italic*")
        assert "**" not in result


# ── export_training_pack_to_pdf ───────────────────────────────────────────────────

class TestExportTrainingPackToPdf:
    def test_returns_bytes(self, minimal_pack_data, sample_analytics, minimal_markdown):
        result = eu.export_training_pack_to_pdf(
            minimal_pack_data, minimal_markdown, analytics=sample_analytics
        )
        assert isinstance(result, bytes)

    def test_returns_non_empty_bytes(self, minimal_pack_data, sample_analytics, minimal_markdown):
        result = eu.export_training_pack_to_pdf(
            minimal_pack_data, minimal_markdown, analytics=sample_analytics
        )
        assert len(result) > 1000  # PDF has non-trivial size

    def test_pdf_magic_bytes(self, minimal_pack_data, sample_analytics, minimal_markdown):
        result = eu.export_training_pack_to_pdf(
            minimal_pack_data, minimal_markdown, analytics=sample_analytics
        )
        assert result[:4] == b"%PDF"

    def test_handles_empty_pack_data(self, minimal_markdown):
        result = eu.export_training_pack_to_pdf({}, minimal_markdown)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_handles_none_analytics(self, minimal_pack_data, minimal_markdown):
        result = eu.export_training_pack_to_pdf(minimal_pack_data, minimal_markdown, analytics=None)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_handles_empty_markdown(self, minimal_pack_data, sample_analytics):
        result = eu.export_training_pack_to_pdf(minimal_pack_data, "", analytics=sample_analytics)
        assert isinstance(result, bytes)

    def test_handles_none_pack_data(self, minimal_markdown):
        result = eu.export_training_pack_to_pdf(None, minimal_markdown)
        assert isinstance(result, bytes)

    def test_pdf_without_activities(self, sample_analytics, minimal_markdown):
        pack_data = {"scenario": {"organisation_name": "Test Org"}}
        result = eu.export_training_pack_to_pdf(pack_data, minimal_markdown, analytics=sample_analytics)
        assert isinstance(result, bytes)
        assert len(result) > 0


# ── export_training_pack_to_pptx ─────────────────────────────────────────────────

class TestExportTrainingPackToPptx:
    def test_returns_bytes(self, minimal_pack_data, sample_analytics):
        result = eu.export_training_pack_to_pptx(minimal_pack_data, analytics=sample_analytics)
        assert isinstance(result, bytes)

    def test_returns_non_empty_bytes(self, minimal_pack_data, sample_analytics):
        result = eu.export_training_pack_to_pptx(minimal_pack_data, analytics=sample_analytics)
        assert len(result) > 5000  # PPTX has non-trivial size

    def test_pptx_magic_bytes(self, minimal_pack_data, sample_analytics):
        result = eu.export_training_pack_to_pptx(minimal_pack_data, analytics=sample_analytics)
        # PPTX is a ZIP file
        assert result[:2] == b"PK"

    def test_handles_empty_pack_data(self):
        result = eu.export_training_pack_to_pptx({})
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_handles_none_analytics(self, minimal_pack_data):
        result = eu.export_training_pack_to_pptx(minimal_pack_data, analytics=None)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_handles_none_pack_data(self):
        result = eu.export_training_pack_to_pptx(None)
        assert isinstance(result, bytes)

    def test_pptx_has_slides(self, minimal_pack_data, sample_analytics):
        from pptx import Presentation
        import io
        result = eu.export_training_pack_to_pptx(minimal_pack_data, analytics=sample_analytics)
        prs = Presentation(io.BytesIO(result))
        assert len(prs.slides) >= 11

    def test_pptx_without_knowledge_check(self, sample_analytics):
        pack_data = {
            "scenario": {"organisation_name": "Test", "priority_topics": []},
        }
        result = eu.export_training_pack_to_pptx(pack_data, analytics=sample_analytics)
        assert isinstance(result, bytes)
        assert len(result) > 0


# ── generate_chart_images_for_training_pack ──────────────────────────────────────

class TestGenerateChartImages:
    def test_returns_dict(self, minimal_pack_data, sample_analytics):
        result = eu.generate_chart_images_for_training_pack(minimal_pack_data, sample_analytics)
        assert isinstance(result, dict)

    def test_section_completion_chart_present(self, minimal_pack_data, sample_analytics):
        result = eu.generate_chart_images_for_training_pack(minimal_pack_data, sample_analytics)
        assert "section_completion" in result

    def test_chart_values_are_bytes(self, minimal_pack_data, sample_analytics):
        result = eu.generate_chart_images_for_training_pack(minimal_pack_data, sample_analytics)
        for v in result.values():
            assert isinstance(v, bytes)

    def test_chart_bytes_are_png(self, minimal_pack_data, sample_analytics):
        result = eu.generate_chart_images_for_training_pack(minimal_pack_data, sample_analytics)
        for v in result.values():
            assert v[:4] == b"\x89PNG"

    def test_handles_empty_analytics(self, minimal_pack_data):
        result = eu.generate_chart_images_for_training_pack(minimal_pack_data, {})
        assert isinstance(result, dict)

    def test_handles_empty_pack_data(self, sample_analytics):
        result = eu.generate_chart_images_for_training_pack({}, sample_analytics)
        assert isinstance(result, dict)
