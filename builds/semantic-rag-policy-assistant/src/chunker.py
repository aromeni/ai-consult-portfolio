"""Text chunker for the Semantic RAG Policy Assistant.

Phase 2: word-based chunking with validation, summary, and an experimental
section-based strategy that splits on Markdown headings.
"""

import re


# ── Helpers ───────────────────────────────────────────────────────────────────

def split_text_into_words(text: str) -> list:
    """Return a list of whitespace-separated words from text."""
    if not text or not text.strip():
        return []
    return text.split()


def validate_chunk_settings(chunk_size: int, overlap: int) -> tuple:
    """Return (is_valid: bool, message: str) for the given settings.

    Rules:
    - chunk_size > 0
    - overlap >= 0
    - overlap < chunk_size
    """
    if chunk_size <= 0:
        return False, "Chunk size must be greater than 0."
    if overlap < 0:
        return False, "Overlap must be 0 or greater."
    if overlap >= chunk_size:
        return (
            False,
            f"Overlap ({overlap}) must be smaller than chunk size ({chunk_size}). "
            "Reduce the overlap or increase the chunk size.",
        )
    return True, "Settings are valid."


def estimate_chunk_count(word_count: int, chunk_size: int, overlap: int) -> int:
    """Estimate the number of chunks produced by the given settings.

    Uses the same sliding-window logic as chunk_text so the estimate is exact.
    Returns 0 for invalid inputs.
    """
    if word_count <= 0 or chunk_size <= 0:
        return 0
    if overlap < 0 or overlap >= chunk_size:
        return 0
    step = chunk_size - overlap
    count = 0
    idx = 0
    while idx < word_count:
        count += 1
        idx += step
    return count


# ── Internal chunking implementations ────────────────────────────────────────

def _doc_slug(document_name: str) -> str:
    """Return a safe slug for use in chunk IDs."""
    if not document_name:
        return "doc"
    return document_name.replace(".md", "").replace(" ", "-")


def _word_chunks(words: list, chunk_size: int, overlap: int, document_name: str) -> list:
    """Core sliding-window word chunker. Returns chunk dicts."""
    if not words:
        return []
    slug = _doc_slug(document_name)
    step = chunk_size - overlap
    chunks = []
    idx = 0
    local_index = 0

    while idx < len(words):
        chunk_words = words[idx : idx + chunk_size]
        chunk_str = " ".join(chunk_words)
        chunks.append(
            {
                "chunk_id": f"{slug}__chunk_{local_index:03d}",
                "document_name": document_name,
                "chunk_index": local_index,
                "text": chunk_str,
                "word_count": len(chunk_words),
                "character_count": len(chunk_str),
                "start_word": idx,
                "end_word": idx + len(chunk_words) - 1,
                "chunk_size": chunk_size,
                "overlap": overlap,
                "strategy": "word",
            }
        )
        idx += step
        local_index += 1

    return chunks


def _section_chunks(text: str, chunk_size: int, overlap: int, document_name: str) -> list:
    """Experimental: split on Markdown level-2 headings, then word-chunk each section.

    Falls back to word chunking when fewer than 2 headings are found.
    Word positions (start_word, end_word) are relative to each section, not the full document.
    """
    parts = re.split(r"\n(?=## )", text.strip())
    parts = [p.strip() for p in parts if p.strip()]

    if len(parts) < 2:
        chunks = _word_chunks(split_text_into_words(text), chunk_size, overlap, document_name)
        for c in chunks:
            c["strategy"] = "section"
        return chunks

    slug = _doc_slug(document_name)
    all_chunks = []
    global_index = 0

    for part in parts:
        section_words = split_text_into_words(part)
        section_chunks = _word_chunks(section_words, chunk_size, overlap, document_name)
        for chunk in section_chunks:
            chunk["chunk_id"] = f"{slug}__chunk_{global_index:03d}"
            chunk["chunk_index"] = global_index
            chunk["strategy"] = "section"
            all_chunks.append(chunk)
            global_index += 1

    return all_chunks


# ── Public API ────────────────────────────────────────────────────────────────

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
    document_name: str = "",
    strategy: str = "word",
) -> list:
    """Split text into overlapping chunks.

    Args:
        text: document text to split
        chunk_size: maximum words per chunk (default 500)
        overlap: words shared between adjacent chunks (default 100)
        document_name: used in chunk_id generation (e.g. 'policy.md')
        strategy: 'word' (default) or 'section' (experimental — splits on ## headings)

    Returns a list of chunk dicts, each containing:
        chunk_id, document_name, chunk_index, text,
        word_count, character_count, start_word, end_word,
        chunk_size, overlap, strategy.

    Raises ValueError for invalid chunk settings.
    """
    if not text or not text.strip():
        return []

    valid, msg = validate_chunk_settings(chunk_size, overlap)
    if not valid:
        raise ValueError(msg)

    if strategy == "section":
        return _section_chunks(text, chunk_size, overlap, document_name)

    words = split_text_into_words(text)
    return _word_chunks(words, chunk_size, overlap, document_name)


def chunk_documents(
    documents: dict,
    chunk_size: int = 500,
    overlap: int = 100,
    strategy: str = "word",
) -> list:
    """Chunk all documents in a {filename: text} dict.

    Returns a flat list of chunk dicts. chunk_ids are globally unique because
    each document's slug is derived from its unique filename.
    """
    all_chunks = []
    for filename, text in documents.items():
        doc_chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap,
            document_name=filename,
            strategy=strategy,
        )
        all_chunks.extend(doc_chunks)
    return all_chunks


def get_chunking_summary(chunks: list) -> dict:
    """Return summary statistics for a list of chunk dicts.

    Returns dict with:
        total_chunks, total_documents, total_words,
        average_chunk_words, min_chunk_words, max_chunk_words,
        average_chunk_characters.
    """
    if not chunks:
        return {
            "total_chunks": 0,
            "total_documents": 0,
            "total_words": 0,
            "average_chunk_words": 0,
            "min_chunk_words": 0,
            "max_chunk_words": 0,
            "average_chunk_characters": 0,
        }

    word_counts = [c["word_count"] for c in chunks]
    char_counts = [c["character_count"] for c in chunks]
    doc_names = {c["document_name"] for c in chunks}

    return {
        "total_chunks": len(chunks),
        "total_documents": len(doc_names),
        "total_words": sum(word_counts),
        "average_chunk_words": round(sum(word_counts) / len(word_counts), 1),
        "min_chunk_words": min(word_counts),
        "max_chunk_words": max(word_counts),
        "average_chunk_characters": round(sum(char_counts) / len(char_counts), 1),
    }
