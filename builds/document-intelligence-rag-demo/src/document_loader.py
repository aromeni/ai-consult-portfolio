"""
document_loader.py — simple file-based document loading.

Functions:
    list_documents(directory)   → list of .md file paths
    load_document(path)         → file content as string
    get_document_metadata(path) → dict of basic metadata
"""

from pathlib import Path
from datetime import datetime


def list_documents(directory: str) -> list:
    """Return sorted list of absolute paths to all .md files in directory."""
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    return sorted(str(p) for p in dir_path.glob("*.md"))


def load_document(path: str) -> str:
    """Return text content of a document. Returns empty string if not found."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return ""


def get_document_metadata(path: str) -> dict:
    """Return basic metadata for a document file."""
    p = Path(path)
    if not p.exists():
        return {
            "name": p.stem,
            "filename": p.name,
            "path": str(path),
            "exists": False,
        }
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    words = text.split()
    stat = p.stat()
    return {
        "name": p.stem,
        "filename": p.name,
        "path": str(path),
        "exists": True,
        "size_bytes": stat.st_size,
        "line_count": len(lines),
        "word_count": len(words),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%d %B %Y"),
    }
