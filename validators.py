"""Validation utilities for common data types.

All validators return bool - True if valid, False otherwise.
None and empty strings are considered invalid.
"""

import re
from urllib.parse import urlparse


def is_valid_email(email: str) -> bool:
    """Check if string is a valid email address."""
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def is_valid_url(url: str, require_scheme: bool = True) -> bool:
    """Check if string is a valid URL.

    Args:
        url: URL to validate
        require_scheme: Require http/https prefix

    Returns:
        True if valid URL
    """
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url.strip())
        if require_scheme:
            return bool(result.scheme in ("http", "https") and result.netloc)
        return bool(result.netloc)
    except Exception:
        return False


def is_valid_phone(phone: str, country: str = "US") -> bool:
    """Check if string is a valid phone number.

    Args:
        phone: Phone number string
        country: Country code for format validation

    Returns:
        True if valid phone number
    """
    if not phone or not isinstance(phone, str):
        return False

    # Strip common formatting chars
    digits = re.sub(r"[\s\-\.\(\)\+]", "", phone)

    if country == "US":
        # US: 10 digits, optionally with leading 1
        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]
        return len(digits) == 10 and digits.isdigit()

    # Generic: 7-15 digits
    return 7 <= len(digits) <= 15 and digits.isdigit()


def is_valid_zip(zipcode: str, country: str = "US") -> bool:
    """Check if string is a valid postal/ZIP code.

    Args:
        zipcode: ZIP code string
        country: Country code

    Returns:
        True if valid ZIP code
    """
    if not zipcode or not isinstance(zipcode, str):
        return False

    zipcode = zipcode.strip()

    patterns = {
        "US": r"^\d{5}(-\d{4})?$",
        "CA": r"^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$",
        "UK": r"^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$",
    }

    pattern = patterns.get(country, r"^[\w\s-]{3,10}$")
    return bool(re.match(pattern, zipcode, re.IGNORECASE))


def is_valid_ssn(ssn: str) -> bool:
    """Check if string is a valid US Social Security Number format."""
    if not ssn or not isinstance(ssn, str):
        return False

    # Remove dashes
    digits = ssn.replace("-", "")

    if len(digits) != 9 or not digits.isdigit():
        return False

    # SSN cannot start with 000, 666, or 900-999
    area = int(digits[:3])
    if area == 0 or area == 666 or area >= 900:
        return False

    # Group and serial cannot be 0000
    if digits[3:5] == "00" or digits[5:] == "0000":
        return False

    return True


def is_valid_credit_card(number: str) -> bool:
    """Check if string passes Luhn algorithm (credit card checksum)."""
    if not number or not isinstance(number, str):
        return False

    # Remove spaces and dashes
    digits = re.sub(r"[\s-]", "", number)

    if not digits.isdigit() or len(digits) < 13 or len(digits) > 19:
        return False

    # Luhn algorithm
    total = 0
    for i, digit in enumerate(reversed(digits)):
        d = int(digit)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    return total % 10 == 0


def is_not_empty(value: str | None) -> bool:
    """Check if string is not None and not empty after stripping."""
    if value is None:
        return False
    return bool(str(value).strip())


def is_in_range(value: float | int, min_val: float | None = None, max_val: float | None = None) -> bool:
    """Check if number is within range (inclusive)."""
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True
