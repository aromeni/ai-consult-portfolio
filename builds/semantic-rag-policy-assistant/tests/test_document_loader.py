"""Tests for src/document_loader.py."""

import os
import tempfile
import pytest
from src.document_loader import (
    list_documents,
    load_document,
    load_all_documents,
    get_document_metadata,
)

SYNTHETIC_DOCS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "synthetic_documents"
)


# ── list_documents ────────────────────────────────────────────────────────────

def test_list_documents_returns_md_files():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    assert len(docs) >= 4


def test_list_documents_all_md():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    assert all(f.endswith(".md") for f in docs)


def test_list_documents_expected_filenames():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    names = [os.path.basename(d) for d in docs]
    assert "synthetic-ai-acceptable-use-policy.md" in names
    assert "synthetic-data-protection-guidance.md" in names
    assert "synthetic-safeguarding-and-ai-boundaries.md" in names
    assert "synthetic-staff-ai-training-notes.md" in names


def test_list_documents_missing_dir_returns_empty():
    assert list_documents("/nonexistent/path/xyz") == []


def test_list_documents_empty_dir_returns_empty():
    with tempfile.TemporaryDirectory() as tmp:
        assert list_documents(tmp) == []


def test_list_documents_ignores_non_md():
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "notes.txt"), "w").close()
        open(os.path.join(tmp, "data.csv"), "w").close()
        assert list_documents(tmp) == []


# ── load_document ─────────────────────────────────────────────────────────────

def test_load_document_returns_string():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    text = load_document(docs[0])
    assert isinstance(text, str)


def test_load_document_non_empty():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    text = load_document(docs[0])
    assert len(text) > 100


def test_load_document_contains_synthetic_marker():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    text = load_document(docs[0])
    assert "Synthetic" in text or "synthetic" in text


# ── load_all_documents ────────────────────────────────────────────────────────

def test_load_all_documents_returns_dict():
    result = load_all_documents(SYNTHETIC_DOCS_DIR)
    assert isinstance(result, dict)


def test_load_all_documents_keys_are_filenames():
    result = load_all_documents(SYNTHETIC_DOCS_DIR)
    for key in result:
        assert key.endswith(".md")


def test_load_all_documents_values_non_empty():
    result = load_all_documents(SYNTHETIC_DOCS_DIR)
    for text in result.values():
        assert len(text) > 0


def test_load_all_documents_count():
    result = load_all_documents(SYNTHETIC_DOCS_DIR)
    assert len(result) >= 4


def test_load_all_documents_missing_dir_returns_empty():
    result = load_all_documents("/nonexistent/path/xyz")
    assert result == {}


# ── get_document_metadata ─────────────────────────────────────────────────────

def test_metadata_has_required_keys():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    meta = get_document_metadata(docs[0])
    for key in ("filename", "path", "title", "word_count", "line_count", "character_count"):
        assert key in meta


def test_metadata_filename_is_basename():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    meta = get_document_metadata(docs[0])
    assert meta["filename"] == os.path.basename(docs[0])


def test_metadata_word_count_positive():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    meta = get_document_metadata(docs[0])
    assert meta["word_count"] > 0


def test_metadata_line_count_positive():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    meta = get_document_metadata(docs[0])
    assert meta["line_count"] > 0


def test_metadata_character_count_positive():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    meta = get_document_metadata(docs[0])
    assert meta["character_count"] > 0


def test_metadata_title_extracted():
    docs = list_documents(SYNTHETIC_DOCS_DIR)
    meta = get_document_metadata(docs[0])
    assert isinstance(meta["title"], str)
    assert len(meta["title"]) > 0
