"""Tests for src/chunker.py — Phase 2."""

import os
import pytest
from src.chunker import (
    split_text_into_words,
    validate_chunk_settings,
    estimate_chunk_count,
    chunk_text,
    chunk_documents,
    get_chunking_summary,
)
from src.document_loader import load_all_documents

SYNTHETIC_DOCS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "synthetic_documents"
)

SAMPLE_TEXT = (
    "This is a synthetic policy document used for testing. "
    "Staff must not enter personal data into AI tools. "
    "Human review is required before acting on any output. "
    "Safeguarding decisions must always be made by a qualified professional. "
    "Data minimisation principles apply to all AI tool usage at this organisation. "
    "Approved tools have been reviewed for data processing terms and conditions. "
    "Staff must escalate safeguarding concerns to the Designated Safeguarding Lead. "
    "AI tools cannot assess risk or make decisions about learner welfare or safety. "
    "All prompts must use anonymised synthetic or general information only."
)

SECTION_TEXT = (
    "## Introduction\n"
    "This section covers the introduction to AI policy.\n"
    "Staff must read this document carefully before using any AI tools.\n\n"
    "## Approved Use\n"
    "Staff may use approved AI tools for drafting correspondence and lesson plans.\n"
    "All outputs must be reviewed by a human before use.\n\n"
    "## Prohibited Use\n"
    "Staff must not enter personal data or safeguarding information into AI tools.\n"
    "Violations will be investigated and may lead to disciplinary action.\n"
)


# ── split_text_into_words ─────────────────────────────────────────────────────

def test_split_words_returns_list():
    assert isinstance(split_text_into_words("hello world"), list)


def test_split_words_basic():
    result = split_text_into_words("hello world foo")
    assert result == ["hello", "world", "foo"]


def test_split_words_empty_returns_empty():
    assert split_text_into_words("") == []


def test_split_words_whitespace_returns_empty():
    assert split_text_into_words("   \n\t  ") == []


def test_split_words_strips_extra_spaces():
    result = split_text_into_words("hello   world")
    assert result == ["hello", "world"]


def test_split_words_count_matches():
    result = split_text_into_words(SAMPLE_TEXT)
    assert len(result) == len(SAMPLE_TEXT.split())


# ── validate_chunk_settings ───────────────────────────────────────────────────

def test_validate_valid_settings():
    ok, msg = validate_chunk_settings(120, 30)
    assert ok is True


def test_validate_message_on_valid():
    ok, msg = validate_chunk_settings(120, 30)
    assert isinstance(msg, str) and len(msg) > 0


def test_validate_overlap_zero_is_valid():
    ok, _ = validate_chunk_settings(100, 0)
    assert ok is True


def test_validate_chunk_size_zero_is_invalid():
    ok, msg = validate_chunk_settings(0, 0)
    assert ok is False
    assert "chunk size" in msg.lower() or "0" in msg


def test_validate_negative_chunk_size_is_invalid():
    ok, _ = validate_chunk_settings(-10, 0)
    assert ok is False


def test_validate_negative_overlap_is_invalid():
    ok, _ = validate_chunk_settings(100, -1)
    assert ok is False


def test_validate_overlap_equals_chunk_size_is_invalid():
    ok, msg = validate_chunk_settings(100, 100)
    assert ok is False
    assert "overlap" in msg.lower()


def test_validate_overlap_greater_than_chunk_size_is_invalid():
    ok, _ = validate_chunk_settings(50, 75)
    assert ok is False


def test_validate_large_valid_settings():
    ok, _ = validate_chunk_settings(1000, 200)
    assert ok is True


# ── estimate_chunk_count ──────────────────────────────────────────────────────

def test_estimate_returns_int():
    assert isinstance(estimate_chunk_count(100, 20, 5), int)


def test_estimate_single_chunk_when_text_fits():
    assert estimate_chunk_count(50, 100, 0) == 1


def test_estimate_exact_no_overlap():
    # 100 words, size 25, no overlap → 4 chunks
    assert estimate_chunk_count(100, 25, 0) == 4


def test_estimate_with_overlap_produces_more_chunks():
    without = estimate_chunk_count(100, 25, 0)
    with_overlap = estimate_chunk_count(100, 25, 10)
    assert with_overlap >= without


def test_estimate_zero_word_count_returns_zero():
    assert estimate_chunk_count(0, 25, 5) == 0


def test_estimate_invalid_overlap_returns_zero():
    assert estimate_chunk_count(100, 25, 25) == 0


def test_estimate_matches_actual_chunk_count():
    words = split_text_into_words(SAMPLE_TEXT)
    estimated = estimate_chunk_count(len(words), 20, 5)
    actual = len(chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5))
    assert estimated == actual


# ── chunk_text ────────────────────────────────────────────────────────────────

def test_chunk_text_returns_list():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    assert isinstance(result, list)


def test_chunk_text_non_empty():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    assert len(result) > 0


def test_chunk_text_empty_string_returns_empty():
    assert chunk_text("") == []


def test_chunk_text_whitespace_returns_empty():
    assert chunk_text("   \n\t  ") == []


def test_chunk_text_has_all_required_keys():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    required = (
        "chunk_id", "document_name", "chunk_index", "text",
        "word_count", "character_count", "start_word", "end_word",
        "chunk_size", "overlap", "strategy",
    )
    for key in required:
        assert key in result[0], f"Missing key: {key}"


def test_chunk_text_word_count_matches():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    for chunk in result:
        assert chunk["word_count"] == len(chunk["text"].split())


def test_chunk_text_character_count_matches():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    for chunk in result:
        assert chunk["character_count"] == len(chunk["text"])


def test_chunk_text_chunk_index_sequential():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    for i, chunk in enumerate(result):
        assert chunk["chunk_index"] == i


def test_chunk_text_start_word_zero_for_first_chunk():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    assert result[0]["start_word"] == 0


def test_chunk_text_end_word_gt_start_word():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    for chunk in result:
        assert chunk["end_word"] >= chunk["start_word"]


def test_chunk_text_start_word_advances_with_step():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    step = 20 - 5  # chunk_size - overlap
    assert result[1]["start_word"] == step


def test_chunk_text_stores_chunk_size():
    result = chunk_text(SAMPLE_TEXT, chunk_size=25, overlap=5)
    for chunk in result:
        assert chunk["chunk_size"] == 25


def test_chunk_text_stores_overlap():
    result = chunk_text(SAMPLE_TEXT, chunk_size=25, overlap=5)
    for chunk in result:
        assert chunk["overlap"] == 5


def test_chunk_text_word_strategy_stored():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5, strategy="word")
    for chunk in result:
        assert chunk["strategy"] == "word"


def test_chunk_text_document_name_stored():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5, document_name="my-policy.md")
    for chunk in result:
        assert chunk["document_name"] == "my-policy.md"


def test_chunk_text_chunk_id_includes_doc_slug():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5, document_name="my-policy.md")
    assert "my-policy" in result[0]["chunk_id"]


def test_chunk_text_no_overlap_produces_fewer_chunks():
    with_overlap = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=10)
    without_overlap = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=0)
    assert len(with_overlap) >= len(without_overlap)


def test_chunk_text_large_chunk_size_gives_one_chunk():
    result = chunk_text(SAMPLE_TEXT, chunk_size=10000, overlap=0)
    assert len(result) == 1


def test_chunk_text_text_is_non_empty():
    result = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    for chunk in result:
        assert len(chunk["text"]) > 0


def test_chunk_text_invalid_overlap_raises():
    with pytest.raises(ValueError):
        chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=20)


def test_chunk_text_section_strategy_returns_list():
    result = chunk_text(SECTION_TEXT, chunk_size=20, overlap=5, strategy="section")
    assert isinstance(result, list)


def test_chunk_text_section_strategy_non_empty():
    result = chunk_text(SECTION_TEXT, chunk_size=20, overlap=5, strategy="section")
    assert len(result) > 0


def test_chunk_text_section_strategy_stored():
    result = chunk_text(SECTION_TEXT, chunk_size=20, overlap=5, strategy="section")
    for chunk in result:
        assert chunk["strategy"] == "section"


# ── chunk_documents ───────────────────────────────────────────────────────────

def test_chunk_documents_returns_list():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    assert isinstance(result, list)


def test_chunk_documents_non_empty():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    assert len(result) > 0


def test_chunk_documents_sets_document_name():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    for chunk in result:
        assert chunk["document_name"] != ""


def test_chunk_documents_document_names_are_filenames():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    filenames = set(docs.keys())
    for chunk in result:
        assert chunk["document_name"] in filenames


def test_chunk_documents_chunk_ids_unique():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    ids = [c["chunk_id"] for c in result]
    assert len(ids) == len(set(ids))


def test_chunk_documents_covers_all_documents():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    doc_names_in_chunks = {c["document_name"] for c in result}
    assert doc_names_in_chunks == set(docs.keys())


def test_chunk_documents_empty_dict_returns_empty():
    assert chunk_documents({}) == []


def test_chunk_documents_has_new_keys():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    result = chunk_documents(docs, chunk_size=120, overlap=30)
    for key in ("start_word", "end_word", "chunk_size", "overlap", "strategy"):
        assert key in result[0]


# ── get_chunking_summary ──────────────────────────────────────────────────────

def test_summary_returns_dict():
    chunks = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    assert isinstance(get_chunking_summary(chunks), dict)


def test_summary_has_required_keys():
    chunks = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    summary = get_chunking_summary(chunks)
    for key in (
        "total_chunks", "total_documents", "total_words",
        "average_chunk_words", "min_chunk_words", "max_chunk_words",
        "average_chunk_characters",
    ):
        assert key in summary


def test_summary_total_chunks_correct():
    chunks = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    summary = get_chunking_summary(chunks)
    assert summary["total_chunks"] == len(chunks)


def test_summary_total_words_positive():
    chunks = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    summary = get_chunking_summary(chunks)
    assert summary["total_words"] > 0


def test_summary_min_le_average_le_max():
    chunks = chunk_text(SAMPLE_TEXT, chunk_size=20, overlap=5)
    summary = get_chunking_summary(chunks)
    assert summary["min_chunk_words"] <= summary["average_chunk_words"]
    assert summary["average_chunk_words"] <= summary["max_chunk_words"]


def test_summary_empty_chunks_returns_zeros():
    summary = get_chunking_summary([])
    assert summary["total_chunks"] == 0
    assert summary["total_words"] == 0
    assert summary["min_chunk_words"] == 0


def test_summary_document_count_from_documents():
    docs = load_all_documents(SYNTHETIC_DOCS_DIR)
    chunks = chunk_documents(docs, chunk_size=120, overlap=30)
    summary = get_chunking_summary(chunks)
    assert summary["total_documents"] == len(docs)
