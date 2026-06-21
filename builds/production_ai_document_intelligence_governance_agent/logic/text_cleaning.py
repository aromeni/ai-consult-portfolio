"""
Text cleaning utilities for Build 11.

Cleans raw document text while preserving headings and meaningful content.
Does not mutate input strings.
"""

from __future__ import annotations

import re


def clean_text(text: str) -> str:
    """
    Clean whitespace, remove repeated blank lines, and normalise line endings.
    Does not remove headings, punctuation, or meaningful content.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    result: list[str] = []
    prev_blank = False
    for line in lines:
        is_blank = line == ""
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return "\n".join(result).strip()


def remove_markdown_syntax(text: str) -> str:
    """
    Remove Markdown syntax markers (e.g. #, *, **, `) from text.
    Preserves the underlying words and structure.
    """
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}([^*\n]+)\*{1,3}", r"\1", text)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    return text


def normalise_whitespace(text: str) -> str:
    """Replace multiple consecutive spaces with a single space."""
    return re.sub(r" {2,}", " ", text)


def clean_document(document: dict) -> dict:
    """
    Return a new document dict with cleaned text.
    Does not modify the input dict.
    """
    cleaned = clean_text(document["text"])
    return {
        **document,
        "text": cleaned,
        "word_count": len(cleaned.split()),
        "char_count": len(cleaned),
    }
