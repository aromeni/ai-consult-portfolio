"""
Document chunking for Build 11.

Splits cleaned document text into overlapping word-window chunks.
Each chunk carries full metadata for retrieval and citation.
"""

from __future__ import annotations

DEFAULT_CHUNK_SIZE = 200
DEFAULT_OVERLAP = 40


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[dict]:
    """
    Split text into overlapping word-window chunks.

    Returns list of dicts with keys:
        chunk_index (int), text (str), word_count (int),
        start_word (int), end_word (int).
    """
    if overlap >= chunk_size:
        raise ValueError(f"overlap ({overlap}) must be less than chunk_size ({chunk_size})")

    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    chunks: list[dict] = []
    chunk_index = 0
    i = 0

    while i < len(words):
        chunk_words = words[i : i + chunk_size]
        chunks.append(
            {
                "chunk_index": chunk_index,
                "text": " ".join(chunk_words),
                "word_count": len(chunk_words),
                "start_word": i,
                "end_word": i + len(chunk_words) - 1,
            }
        )
        chunk_index += 1
        i += step

    return chunks


def chunk_document(
    document: dict,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[dict]:
    """
    Chunk a single document dict.

    Returns list of chunk dicts with keys:
        chunk_id (str), document_id (str), source_name (str),
        chunk_index (int), text (str), word_count (int),
        start_word (int), end_word (int), metadata (dict).
    """
    text_chunks = chunk_text(document["text"], chunk_size, overlap)
    doc_id = document["document_id"]
    return [
        {
            "chunk_id": f"{doc_id}_chunk_{tc['chunk_index']:03d}",
            "document_id": doc_id,
            "source_name": document["source_name"],
            **tc,
            "metadata": document.get("metadata", {}),
        }
        for tc in text_chunks
    ]


def chunk_all_documents(
    documents: list[dict],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[dict]:
    """Chunk all documents and return a flat list of chunk dicts."""
    result: list[dict] = []
    for doc in documents:
        result.extend(chunk_document(doc, chunk_size, overlap))
    return result


def chunking_summary(chunks: list[dict]) -> dict:
    """Return summary statistics for a list of chunks."""
    if not chunks:
        return {
            "total_chunks": 0,
            "avg_word_count": 0,
            "min_word_count": 0,
            "max_word_count": 0,
            "unique_sources": 0,
        }
    word_counts = [c["word_count"] for c in chunks]
    return {
        "total_chunks": len(chunks),
        "avg_word_count": round(sum(word_counts) / len(word_counts), 1),
        "min_word_count": min(word_counts),
        "max_word_count": max(word_counts),
        "unique_sources": len({c["source_name"] for c in chunks}),
    }
