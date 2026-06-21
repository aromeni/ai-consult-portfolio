"""Tests for logic/text_cleaning.py — Phase 2."""

import pytest

from logic.text_cleaning import (
    clean_document,
    clean_text,
    normalise_whitespace,
    remove_markdown_syntax,
)

# ---------------------------------------------------------------------------
# clean_text
# ---------------------------------------------------------------------------


def test_clean_text_returns_string():
    assert isinstance(clean_text("hello"), str)


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_clean_text_strips_leading_trailing_whitespace():
    assert clean_text("  hello  ") == "hello"


def test_clean_text_collapses_multiple_blank_lines():
    text = "line one\n\n\n\nline two"
    result = clean_text(text)
    assert "\n\n\n" not in result


def test_clean_text_preserves_single_blank_line():
    text = "line one\n\nline two"
    result = clean_text(text)
    assert "line one" in result
    assert "line two" in result


def test_clean_text_strips_trailing_whitespace_per_line():
    text = "line one   \nline two   "
    result = clean_text(text)
    for line in result.split("\n"):
        assert line == line.rstrip()


def test_clean_text_normalises_crlf():
    text = "line one\r\nline two\r\n"
    result = clean_text(text)
    assert "\r" not in result


def test_clean_text_does_not_mutate_input():
    original = "  hello  \n\n\nworld  "
    original_copy = original
    clean_text(original)
    assert original == original_copy


def test_clean_text_preserves_headings():
    text = "# Section One\n\nSome content here."
    result = clean_text(text)
    assert "# Section One" in result


def test_clean_text_preserves_meaningful_content():
    text = "Do not enter learner names into AI tools."
    result = clean_text(text)
    assert "learner names" in result


# ---------------------------------------------------------------------------
# remove_markdown_syntax
# ---------------------------------------------------------------------------


def test_remove_markdown_syntax_removes_heading_markers():
    result = remove_markdown_syntax("## Section Title")
    assert "##" not in result
    assert "Section Title" in result


def test_remove_markdown_syntax_removes_bold_markers():
    result = remove_markdown_syntax("This is **important** text.")
    assert "**" not in result
    assert "important" in result


def test_remove_markdown_syntax_removes_inline_code():
    result = remove_markdown_syntax("Use `pytest` to run tests.")
    assert "`" not in result
    assert "pytest" in result


def test_remove_markdown_syntax_preserves_words():
    result = remove_markdown_syntax("# Hello **world** with `code`")
    assert "Hello" in result
    assert "world" in result
    assert "code" in result


def test_remove_markdown_syntax_empty_string():
    assert remove_markdown_syntax("") == ""


# ---------------------------------------------------------------------------
# normalise_whitespace
# ---------------------------------------------------------------------------


def test_normalise_whitespace_collapses_multiple_spaces():
    result = normalise_whitespace("hello   world")
    assert "   " not in result
    assert "hello world" == result


def test_normalise_whitespace_single_space_unchanged():
    text = "hello world"
    assert normalise_whitespace(text) == text


def test_normalise_whitespace_empty_string():
    assert normalise_whitespace("") == ""


def test_normalise_whitespace_does_not_affect_newlines():
    text = "line one\n  indented"
    result = normalise_whitespace(text)
    assert "\n" in result


# ---------------------------------------------------------------------------
# clean_document
# ---------------------------------------------------------------------------


def test_clean_document_returns_dict():
    doc = {"document_id": "test", "source_name": "test.md", "text": "  hello  ", "word_count": 1, "char_count": 7}
    result = clean_document(doc)
    assert isinstance(result, dict)


def test_clean_document_preserves_document_id():
    doc = {"document_id": "my-doc", "source_name": "my-doc.md", "text": "hello", "word_count": 1, "char_count": 5}
    result = clean_document(doc)
    assert result["document_id"] == "my-doc"


def test_clean_document_preserves_source_name():
    doc = {"document_id": "my-doc", "source_name": "my-doc.md", "text": "hello", "word_count": 1, "char_count": 5}
    result = clean_document(doc)
    assert result["source_name"] == "my-doc.md"


def test_clean_document_does_not_mutate_input():
    original_text = "  hello   \n\n\nworld  "
    doc = {"document_id": "d", "source_name": "d.md", "text": original_text, "word_count": 2, "char_count": 20}
    clean_document(doc)
    assert doc["text"] == original_text


def test_clean_document_updates_word_count():
    doc = {
        "document_id": "d",
        "source_name": "d.md",
        "text": "  one two   three  ",
        "word_count": 999,
        "char_count": 999,
    }
    result = clean_document(doc)
    assert result["word_count"] == 3


def test_clean_document_updates_char_count():
    doc = {
        "document_id": "d",
        "source_name": "d.md",
        "text": "  hello  ",
        "word_count": 1,
        "char_count": 9,
    }
    result = clean_document(doc)
    assert result["char_count"] == len(result["text"])
