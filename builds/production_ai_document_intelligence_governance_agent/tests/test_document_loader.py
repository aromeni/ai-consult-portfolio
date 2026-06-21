"""Tests for logic/document_loader.py — Phase 2."""

from pathlib import Path

import pytest

from logic.document_loader import (
    SAMPLE_DOCS_DIR,
    document_summary,
    list_document_paths,
    load_all_documents,
    load_document,
)

# ---------------------------------------------------------------------------
# list_document_paths
# ---------------------------------------------------------------------------


def test_list_document_paths_returns_list():
    paths = list_document_paths()
    assert isinstance(paths, list)


def test_list_document_paths_returns_paths():
    paths = list_document_paths()
    assert all(isinstance(p, Path) for p in paths)


def test_list_document_paths_returns_eight_sample_docs():
    paths = list_document_paths()
    assert len(paths) == 8


def test_list_document_paths_only_md_and_txt(tmp_path):
    (tmp_path / "doc.md").write_text("hello")
    (tmp_path / "doc.txt").write_text("world")
    (tmp_path / "doc.pdf").write_bytes(b"%PDF")
    (tmp_path / "doc.py").write_text("pass")
    paths = list_document_paths(tmp_path)
    assert all(p.suffix in {".md", ".txt"} for p in paths)
    assert len(paths) == 2


def test_list_document_paths_is_sorted():
    paths = list_document_paths()
    assert paths == sorted(paths)


def test_list_document_paths_empty_dir(tmp_path):
    paths = list_document_paths(tmp_path)
    assert paths == []


def test_list_document_paths_custom_directory(tmp_path):
    (tmp_path / "a.md").write_text("content")
    paths = list_document_paths(tmp_path)
    assert len(paths) == 1
    assert paths[0].name == "a.md"


# ---------------------------------------------------------------------------
# load_document
# ---------------------------------------------------------------------------


def test_load_document_returns_dict(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("Hello world")
    doc = load_document(f)
    assert isinstance(doc, dict)


def test_load_document_required_keys(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("Hello world")
    doc = load_document(f)
    for key in ("document_id", "source_name", "file_path", "text", "word_count", "char_count", "metadata"):
        assert key in doc, f"Missing key: {key}"


def test_load_document_document_id_is_stem(tmp_path):
    f = tmp_path / "my-policy.md"
    f.write_text("content")
    doc = load_document(f)
    assert doc["document_id"] == "my-policy"


def test_load_document_source_name_is_filename(tmp_path):
    f = tmp_path / "my-policy.md"
    f.write_text("content")
    doc = load_document(f)
    assert doc["source_name"] == "my-policy.md"


def test_load_document_word_count(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("one two three four five")
    doc = load_document(f)
    assert doc["word_count"] == 5


def test_load_document_char_count(tmp_path):
    f = tmp_path / "test.md"
    content = "Hello world"
    f.write_text(content)
    doc = load_document(f)
    assert doc["char_count"] == len(content)


def test_load_document_text_matches_file(tmp_path):
    f = tmp_path / "test.md"
    content = "This is the document text.\n\nSecond paragraph."
    f.write_text(content)
    doc = load_document(f)
    assert doc["text"] == content


def test_load_document_metadata_has_extension(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("text")
    doc = load_document(f)
    assert doc["metadata"]["extension"] == ".md"


def test_load_document_txt_file(tmp_path):
    f = tmp_path / "guide.txt"
    f.write_text("Plain text document content here.")
    doc = load_document(f)
    assert doc["source_name"] == "guide.txt"
    assert doc["word_count"] == 5


def test_load_document_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_document(tmp_path / "nonexistent.md")


# ---------------------------------------------------------------------------
# load_all_documents
# ---------------------------------------------------------------------------


def test_load_all_documents_returns_list():
    docs = load_all_documents()
    assert isinstance(docs, list)


def test_load_all_documents_returns_eight_docs():
    docs = load_all_documents()
    assert len(docs) == 8


def test_load_all_documents_each_has_required_keys():
    docs = load_all_documents()
    for doc in docs:
        assert "document_id" in doc
        assert "text" in doc
        assert "word_count" in doc


def test_load_all_documents_word_counts_positive():
    docs = load_all_documents()
    assert all(doc["word_count"] > 0 for doc in docs)


def test_load_all_documents_empty_dir(tmp_path):
    docs = load_all_documents(tmp_path)
    assert docs == []


# ---------------------------------------------------------------------------
# document_summary
# ---------------------------------------------------------------------------


def test_document_summary_returns_dict():
    docs = load_all_documents()
    summary = document_summary(docs)
    assert isinstance(summary, dict)


def test_document_summary_total_documents():
    docs = load_all_documents()
    summary = document_summary(docs)
    assert summary["total_documents"] == 8


def test_document_summary_total_word_count_positive():
    docs = load_all_documents()
    summary = document_summary(docs)
    assert summary["total_word_count"] > 0


def test_document_summary_source_names_is_list():
    docs = load_all_documents()
    summary = document_summary(docs)
    assert isinstance(summary["source_names"], list)
    assert len(summary["source_names"]) == 8


def test_document_summary_empty_list():
    summary = document_summary([])
    assert summary["total_documents"] == 0
    assert summary["total_word_count"] == 0
    assert summary["source_names"] == []
