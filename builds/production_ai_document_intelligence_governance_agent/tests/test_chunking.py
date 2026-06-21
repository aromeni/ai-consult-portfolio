"""Tests for logic/chunking.py — Phase 2."""

import pytest

from logic.chunking import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_OVERLAP,
    chunk_all_documents,
    chunk_document,
    chunk_text,
    chunking_summary,
)

# ---------------------------------------------------------------------------
# chunk_text
# ---------------------------------------------------------------------------


def test_chunk_text_returns_list():
    assert isinstance(chunk_text("one two three"), list)


def test_chunk_text_empty_text_returns_empty():
    assert chunk_text("") == []


def test_chunk_text_whitespace_only_returns_empty():
    assert chunk_text("   \n\n  ") == []


def test_chunk_text_short_text_single_chunk():
    chunks = chunk_text("one two three", chunk_size=200, overlap=40)
    assert len(chunks) == 1


def test_chunk_text_chunk_index_starts_at_zero():
    chunks = chunk_text("one two three")
    assert chunks[0]["chunk_index"] == 0


def test_chunk_text_chunk_indices_are_sequential():
    words = " ".join(f"word{i}" for i in range(500))
    chunks = chunk_text(words, chunk_size=100, overlap=20)
    indices = [c["chunk_index"] for c in chunks]
    assert indices == list(range(len(chunks)))


def test_chunk_text_word_count_matches_text():
    words = " ".join(f"word{i}" for i in range(500))
    chunks = chunk_text(words, chunk_size=100, overlap=20)
    for c in chunks:
        assert c["word_count"] == len(c["text"].split())


def test_chunk_text_start_word_of_first_chunk_is_zero():
    words = " ".join(f"w{i}" for i in range(300))
    chunks = chunk_text(words, chunk_size=100, overlap=20)
    assert chunks[0]["start_word"] == 0


def test_chunk_text_end_word_consistent_with_word_count():
    words = " ".join(f"w{i}" for i in range(300))
    chunks = chunk_text(words, chunk_size=100, overlap=20)
    for c in chunks:
        assert c["end_word"] == c["start_word"] + c["word_count"] - 1


def test_chunk_text_step_creates_overlap():
    words = " ".join(f"w{i}" for i in range(300))
    chunk_size, overlap = 100, 20
    chunks = chunk_text(words, chunk_size=chunk_size, overlap=overlap)
    step = chunk_size - overlap
    assert chunks[1]["start_word"] == chunks[0]["start_word"] + step


def test_chunk_text_last_chunk_not_empty():
    words = " ".join(f"w{i}" for i in range(250))
    chunks = chunk_text(words, chunk_size=100, overlap=20)
    assert chunks[-1]["word_count"] > 0
    assert chunks[-1]["text"].strip() != ""


def test_chunk_text_overlap_must_be_less_than_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("some text", chunk_size=50, overlap=50)


def test_chunk_text_required_keys():
    chunks = chunk_text("one two three four five")
    for key in ("chunk_index", "text", "word_count", "start_word", "end_word"):
        assert key in chunks[0], f"Missing key: {key}"


# ---------------------------------------------------------------------------
# chunk_document
# ---------------------------------------------------------------------------

SAMPLE_DOC = {
    "document_id": "test-policy",
    "source_name": "test-policy.md",
    "text": " ".join(f"word{i}" for i in range(300)),
    "word_count": 300,
    "char_count": 2000,
    "metadata": {"extension": ".md"},
}


def test_chunk_document_returns_list():
    assert isinstance(chunk_document(SAMPLE_DOC), list)


def test_chunk_document_required_keys():
    chunks = chunk_document(SAMPLE_DOC)
    for key in ("chunk_id", "document_id", "source_name", "chunk_index", "text", "word_count", "metadata"):
        assert key in chunks[0], f"Missing key: {key}"


def test_chunk_document_chunk_id_contains_document_id():
    chunks = chunk_document(SAMPLE_DOC)
    for c in chunks:
        assert SAMPLE_DOC["document_id"] in c["chunk_id"]


def test_chunk_document_chunk_id_contains_index():
    chunks = chunk_document(SAMPLE_DOC)
    assert "000" in chunks[0]["chunk_id"]


def test_chunk_document_document_id_propagated():
    chunks = chunk_document(SAMPLE_DOC)
    assert all(c["document_id"] == "test-policy" for c in chunks)


def test_chunk_document_source_name_propagated():
    chunks = chunk_document(SAMPLE_DOC)
    assert all(c["source_name"] == "test-policy.md" for c in chunks)


def test_chunk_document_metadata_propagated():
    chunks = chunk_document(SAMPLE_DOC)
    assert all(c["metadata"] == SAMPLE_DOC["metadata"] for c in chunks)


def test_chunk_document_empty_text_returns_empty():
    doc = {**SAMPLE_DOC, "text": ""}
    assert chunk_document(doc) == []


# ---------------------------------------------------------------------------
# chunk_all_documents
# ---------------------------------------------------------------------------


def test_chunk_all_documents_returns_list():
    assert isinstance(chunk_all_documents([SAMPLE_DOC]), list)


def test_chunk_all_documents_empty_input():
    assert chunk_all_documents([]) == []


def test_chunk_all_documents_multiple_docs_flat():
    doc2 = {**SAMPLE_DOC, "document_id": "second-doc", "source_name": "second-doc.md"}
    chunks = chunk_all_documents([SAMPLE_DOC, doc2])
    sources = {c["source_name"] for c in chunks}
    assert "test-policy.md" in sources
    assert "second-doc.md" in sources


def test_chunk_all_documents_total_is_sum_of_individual():
    doc2 = {**SAMPLE_DOC, "document_id": "second-doc", "source_name": "second-doc.md"}
    total = chunk_all_documents([SAMPLE_DOC, doc2])
    from_one = chunk_document(SAMPLE_DOC)
    from_two = chunk_document(doc2)
    assert len(total) == len(from_one) + len(from_two)


# ---------------------------------------------------------------------------
# chunking_summary
# ---------------------------------------------------------------------------


def test_chunking_summary_returns_dict():
    chunks = chunk_document(SAMPLE_DOC)
    assert isinstance(chunking_summary(chunks), dict)


def test_chunking_summary_total_chunks():
    chunks = chunk_document(SAMPLE_DOC)
    summary = chunking_summary(chunks)
    assert summary["total_chunks"] == len(chunks)


def test_chunking_summary_unique_sources():
    doc2 = {**SAMPLE_DOC, "document_id": "second-doc", "source_name": "second-doc.md"}
    chunks = chunk_all_documents([SAMPLE_DOC, doc2])
    summary = chunking_summary(chunks)
    assert summary["unique_sources"] == 2


def test_chunking_summary_empty_input():
    summary = chunking_summary([])
    assert summary["total_chunks"] == 0
    assert summary["unique_sources"] == 0


def test_chunking_summary_avg_word_count_positive():
    chunks = chunk_document(SAMPLE_DOC)
    summary = chunking_summary(chunks)
    assert summary["avg_word_count"] > 0


def test_chunking_summary_min_lte_max():
    chunks = chunk_document(SAMPLE_DOC)
    summary = chunking_summary(chunks)
    assert summary["min_word_count"] <= summary["max_word_count"]
