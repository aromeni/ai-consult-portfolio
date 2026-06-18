"""Document loader for the Semantic RAG Policy Assistant.

Loads synthetic Markdown documents from a local directory.
No external APIs, embeddings, or database calls.
"""

import os
import re


def list_documents(directory: str) -> list:
    """Return sorted list of .md file paths in directory."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".md")
    )


def load_document(path: str) -> str:
    """Return full text content of a document file."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_all_documents(directory: str) -> dict:
    """Return dict mapping filename -> text for all .md files in directory."""
    documents = {}
    for path in list_documents(directory):
        filename = os.path.basename(path)
        documents[filename] = load_document(path)
    return documents


def get_document_metadata(path: str) -> dict:
    """Return metadata dict for a document file.

    Keys: filename, path, title, word_count, line_count, character_count.
    """
    text = load_document(path)
    lines = text.splitlines()
    words = text.split()

    title = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            break

    return {
        "filename": os.path.basename(path),
        "path": path,
        "title": title,
        "word_count": len(words),
        "line_count": len(lines),
        "character_count": len(text),
    }
