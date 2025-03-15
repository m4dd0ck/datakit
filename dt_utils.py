"""Datetime parsing and manipulation utilities."""

from datetime import datetime, date, timedelta
from typing import Any

from dateutil import parser as date_parser


def parse_date(
    value: str | datetime | date | None,
    default: datetime | None = None,
) -> datetime | None:
    """Parse various date formats into datetime.

    Handles ISO format, common US/EU formats, relative dates.

    Args:
        value: Date string or datetime object
        default: Default value if parsing fails

    Returns:
        Parsed datetime or default
    """
    if value is None:
        return default

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    try:
        return date_parser.parse(str(value))
    except (ValueError, TypeError):
        return default


def format_date(
    dt: datetime | date | None,
    fmt: str = "%Y-%m-%d",
    default: str = "",
) -> str:
    """Format datetime to string.

    Args:
        dt: Datetime to format
        fmt: strftime format string
        default: Return value if dt is None

    Returns:
        Formatted date string
    """
    if dt is None:
        return default
    return dt.strftime(fmt)


def date_range(
    start: datetime | date,
    end: datetime | date,
    step_days: int = 1,
) -> list[date]:
    """Generate list of dates between start and end (inclusive).

    Args:
        start: Start date
        end: End date
        step_days: Days between each date

    Returns:
        List of dates
    """
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()

    result = []
    current = start
    while current <= end:
        result.append(current)
        current += timedelta(days=step_days)
    return result


def start_of_day(dt: datetime) -> datetime:
    """Return datetime at start of day (00:00:00)."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime) -> datetime:
    """Return datetime at end of day (23:59:59)."""
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def is_weekend(dt: datetime | date) -> bool:
    """Check if date falls on Saturday or Sunday."""
    return dt.weekday() >= 5


def business_days_between(start: date, end: date) -> int:
    """Count business days (Mon-Fri) between two dates."""
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count


def add_business_days(start: date, days: int) -> date:
    """Add N business days to a date."""
    current = start
    added = 0
    direction = 1 if days >= 0 else -1
    days = abs(days)

    while added < days:
        current += timedelta(days=direction)
        if current.weekday() < 5:
            added += 1
    return current
