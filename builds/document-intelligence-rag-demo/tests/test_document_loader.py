"""
Tests for src/document_loader.py

Run from the project root:  pytest
"""

from pathlib import Path
from src.document_loader import list_documents, load_document, get_document_metadata

DOCS_DIR = Path(__file__).parent.parent / "data" / "synthetic_documents"


# ── list_documents ────────────────────────────────────────────────────────────

def test_list_documents_returns_list():
    assert isinstance(list_documents(str(DOCS_DIR)), list)


def test_list_documents_finds_four_synthetic_docs():
    result = list_documents(str(DOCS_DIR))
    assert len(result) == 4


def test_list_documents_returns_only_md_files():
    for path in list_documents(str(DOCS_DIR)):
        assert path.endswith(".md")


def test_list_documents_missing_directory_returns_empty():
    assert list_documents("/nonexistent/path/xyz") == []


def test_list_documents_results_are_sorted():
    result = list_documents(str(DOCS_DIR))
    assert result == sorted(result)


# ── load_document ─────────────────────────────────────────────────────────────

def test_load_document_returns_string():
    paths = list_documents(str(DOCS_DIR))
    assert isinstance(load_document(paths[0]), str)


def test_load_document_is_not_empty():
    paths = list_documents(str(DOCS_DIR))
    assert len(load_document(paths[0])) > 0


def test_load_document_contains_expected_content():
    policy_path = str(DOCS_DIR / "synthetic-ai-acceptable-use-policy.md")
    content = load_document(policy_path)
    assert "safeguarding" in content.lower()


def test_load_document_missing_file_returns_empty_string():
    assert load_document("/nonexistent/file.md") == ""


def test_load_document_all_four_docs_are_loadable():
    for path in list_documents(str(DOCS_DIR)):
        assert len(load_document(path)) > 100


# ── get_document_metadata ─────────────────────────────────────────────────────

def test_get_document_metadata_returns_dict():
    paths = list_documents(str(DOCS_DIR))
    assert isinstance(get_document_metadata(paths[0]), dict)


def test_get_document_metadata_has_required_keys():
    paths = list_documents(str(DOCS_DIR))
    meta = get_document_metadata(paths[0])
    for key in ("name", "filename", "path", "exists", "word_count", "line_count"):
        assert key in meta, f"Missing key: {key}"


def test_get_document_metadata_exists_is_true_for_real_file():
    paths = list_documents(str(DOCS_DIR))
    assert get_document_metadata(paths[0])["exists"] is True


def test_get_document_metadata_word_count_is_positive():
    paths = list_documents(str(DOCS_DIR))
    assert get_document_metadata(paths[0])["word_count"] > 0


def test_get_document_metadata_missing_file_returns_exists_false():
    meta = get_document_metadata("/nonexistent/file.md")
    assert meta["exists"] is False
