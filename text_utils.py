"""String cleaning and text processing utilities."""

import re
import unicodedata
from typing import Any


def clean_string(
    s: str | None,
    strip: bool = True,
    lower: bool = False,
    upper: bool = False,
    remove_extra_whitespace: bool = True,
) -> str:
    """Clean a string with various options.

    Args:
        s: Input string
        strip: Strip leading/trailing whitespace
        lower: Convert to lowercase
        upper: Convert to uppercase
        remove_extra_whitespace: Collapse multiple spaces to one

    Returns:
        Cleaned string
    """
    if s is None:
        return ""

    s = str(s)

    if strip:
        s = s.strip()

    if remove_extra_whitespace:
        s = re.sub(r"\s+", " ", s)

    if lower:
        s = s.lower()
    elif upper:
        s = s.upper()

    return s


def normalize_unicode(s: str, form: str = "NFC") -> str:
    """Normalize unicode string.

    Args:
        s: Input string
        form: Normalization form (NFC, NFD, NFKC, NFKD)

    Returns:
        Normalized string
    """
    return unicodedata.normalize(form, s)


def remove_accents(s: str) -> str:
    """Remove accents from characters (é -> e)."""
    normalized = unicodedata.normalize("NFD", s)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def slugify(s: str, separator: str = "-") -> str:
    """Convert string to URL-safe slug.

    Example:
        "Hello World!" -> "hello-world"
    """
    s = remove_accents(s.lower())
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", separator, s)
    return s.strip(separator)


def truncate(s: str, length: int, suffix: str = "...") -> str:
    """Truncate string to max length, adding suffix if truncated.

    The suffix is included in the length limit.
    Example: truncate("hello world", 8) -> "hello..."
    """
    if len(s) <= length:
        return s
    return s[: length - len(suffix)] + suffix


def extract_numbers(s: str) -> list[float]:
    """Extract all numbers from a string."""
    pattern = r"-?\d+\.?\d*"
    return [float(n) for n in re.findall(pattern, s)]


def extract_emails(s: str) -> list[str]:
    """Extract email addresses from text."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, s)


def extract_urls(s: str) -> list[str]:
    """Extract URLs from text."""
    pattern = r"https?://[^\s<>\"{}|\\^`\[\]]+"
    return re.findall(pattern, s)


def mask_string(s: str, visible_start: int = 2, visible_end: int = 2, mask_char: str = "*") -> str:
    """Mask middle portion of string.

    Example:
        "1234567890" -> "12******90"
    """
    if len(s) <= visible_start + visible_end:
        return s
    masked_len = len(s) - visible_start - visible_end
    return s[:visible_start] + (mask_char * masked_len) + s[-visible_end:]


def to_snake_case(s: str) -> str:
    """Convert string to snake_case.

    Example: "myVariableName" -> "my_variable_name"
    """
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.replace("-", "_").lower()


def to_camel_case(s: str) -> str:
    """Convert string to camelCase.

    Example: "my_variable_name" -> "myVariableName"
    """
    parts = re.split(r"[_\-\s]+", s)
    return parts[0].lower() + "".join(p.title() for p in parts[1:])
