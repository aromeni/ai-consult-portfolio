import re
from datetime import date


def safe_get(dictionary: dict, key: str, default=None):
    if not isinstance(dictionary, dict):
        return default
    return dictionary.get(key, default)


def safe_list(value) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def create_safe_filename(title: str, extension: str = "md") -> str:
    safe = re.sub(r"[^\w\s-]", "", str(title))
    safe = re.sub(r"[\s]+", "-", safe).strip("-").lower()
    ext = extension.lstrip(".")
    return f"{safe}.{ext}"


def get_current_date_label() -> str:
    return date.today().isoformat()
