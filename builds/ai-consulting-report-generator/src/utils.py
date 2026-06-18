"""General utility functions for Build 5 — AI Consulting Report Generator."""

import re
from datetime import date


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def create_safe_filename(title: str, extension: str = "md") -> str:
    """Return a safe filename for a report output."""
    today = date.today().strftime("%Y-%m-%d")
    slug = slugify(title)[:60]
    ext = extension.lstrip(".")
    return f"{today}-{slug}.{ext}"


def truncate_text(text: str, max_chars: int = 500, suffix: str = "...") -> str:
    """Truncate text to max_chars, appending suffix if truncated."""
    if not isinstance(text, str):
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + suffix


def risk_level_sort_key(level: str) -> int:
    """Return a sort key for risk levels so Critical sorts first."""
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return order.get(str(level).lower(), 99)


def format_score_bar(score: float, max_score: float = 100, bar_width: int = 20) -> str:
    """Return a simple ASCII progress bar for a score."""
    filled = int((score / max_score) * bar_width)
    filled = max(0, min(bar_width, filled))
    return "█" * filled + "░" * (bar_width - filled)
