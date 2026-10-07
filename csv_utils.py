"""CSV reading, writing, and cleaning utilities.

All functions work with lists of dicts where keys are column names.
"""

import csv
from pathlib import Path
from typing import Any


def read_csv(
    path: str | Path,
    delimiter: str = ",",
    skip_header: bool = False,
    encoding: str = "utf-8",
) -> list[dict[str, Any]]:
    """Read CSV file into list of dicts.

    Args:
        path: Path to CSV file
        delimiter: Column delimiter
        skip_header: If True, skip first row
        encoding: File encoding

    Returns:
        List of dicts, one per row
    """
    with open(path, encoding=encoding, newline="") as f:
        if skip_header:
            next(f)
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)


def write_csv(
    path: str | Path,
    data: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> None:
    """Write list of dicts to CSV file.

    Args:
        path: Output path
        data: List of dicts to write
        fieldnames: Column names (auto-detect if None)
        delimiter: Column delimiter
        encoding: File encoding
    """
    if not data:
        return

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(path, "w", encoding=encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)


def clean_csv(
    data: list[dict[str, Any]],
    strip_whitespace: bool = True,
    remove_empty_rows: bool = True,
    lowercase_keys: bool = False,
) -> list[dict[str, Any]]:
    """Clean CSV data.

    Args:
        data: List of dicts
        strip_whitespace: Strip whitespace from string values
        remove_empty_rows: Remove rows where all values are empty
        lowercase_keys: Convert keys to lowercase

    Returns:
        Cleaned data
    """
    result = []
    for row in data:
        new_row = {}
        for key, value in row.items():
            new_key = key.lower() if lowercase_keys else key
            if isinstance(value, str) and strip_whitespace:
                value = value.strip()
            new_row[new_key] = value

        if remove_empty_rows:
            if any(v for v in new_row.values()):
                result.append(new_row)
        else:
            result.append(new_row)

    return result


def filter_columns(data: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    """Keep only specified columns from data."""
    return [{k: row.get(k) for k in columns} for row in data]


def rename_columns(data: list[dict[str, Any]], mapping: dict[str, str]) -> list[dict[str, Any]]:
    """Rename columns using a mapping dict."""
    return [{mapping.get(k, k): v for k, v in row.items()} for row in data]
