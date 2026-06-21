"""
Document loader for Build 11.

Loads .md and .txt documents from the sample_documents folder.
Returns a list of document dicts with standardised metadata.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

SAMPLE_DOCS_DIR = Path(__file__).parent.parent / "data" / "sample_documents"
SUPPORTED_EXTENSIONS = {".md", ".txt"}


def list_document_paths(directory: Optional[Path] = None) -> list[Path]:
    """Return sorted paths to all .md and .txt files in directory."""
    directory = Path(directory) if directory else SAMPLE_DOCS_DIR
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix in SUPPORTED_EXTENSIONS
    )


def load_document(path: Path) -> dict:
    """
    Load a single document from path.

    Returns a dict with keys:
        document_id (str), source_name (str), file_path (str),
        text (str), word_count (int), char_count (int), metadata (dict).
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return {
        "document_id": path.stem,
        "source_name": path.name,
        "file_path": str(path),
        "text": text,
        "word_count": len(text.split()),
        "char_count": len(text),
        "metadata": {
            "extension": path.suffix,
            "size_bytes": path.stat().st_size,
        },
    }


def load_all_documents(directory: Optional[Path] = None) -> list[dict]:
    """Load all .md and .txt documents from directory. Returns list of document dicts."""
    return [load_document(p) for p in list_document_paths(directory)]


def document_summary(documents: list[dict]) -> dict:
    """Return summary statistics for a list of loaded documents."""
    if not documents:
        return {
            "total_documents": 0,
            "total_word_count": 0,
            "total_char_count": 0,
            "source_names": [],
        }
    return {
        "total_documents": len(documents),
        "total_word_count": sum(d["word_count"] for d in documents),
        "total_char_count": sum(d["char_count"] for d in documents),
        "source_names": [d["source_name"] for d in documents],
    }
