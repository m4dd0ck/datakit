"""JSON reading, writing, and manipulation utilities."""

import json
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Any


class ExtendedEncoder(json.JSONEncoder):
    """JSON encoder that handles common Python types.

    Converts: datetime/date -> ISO string, Decimal -> float,
    set -> list, Path -> string.
    """

    def default(self, obj):
        """Serialize non-standard types to JSON-compatible values."""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


def read_json(path: str | Path, encoding: str = "utf-8") -> Any:
    """Read and parse a JSON file.

    Args:
        path: Path to JSON file
        encoding: File encoding

    Returns:
        Parsed JSON data (dict, list, or primitive)
    """
    with open(path, encoding=encoding) as f:
        return json.load(f)


def write_json(
    path: str | Path,
    data: Any,
    indent: int = 2,
    encoding: str = "utf-8",
    ensure_ascii: bool = False,
) -> None:
    """Write data to JSON file.

    Args:
        path: Output path
        data: Data to serialize
        indent: Indentation level
        encoding: File encoding
        ensure_ascii: Escape non-ASCII characters
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, cls=ExtendedEncoder)


def read_jsonl(path: str | Path, encoding: str = "utf-8") -> list[Any]:
    """Read JSON Lines file (one JSON object per line)."""
    result = []
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(json.loads(line))
    return result


def write_jsonl(path: str | Path, data: list[Any], encoding: str = "utf-8") -> None:
    """Write data to JSON Lines file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        for item in data:
            f.write(json.dumps(item, cls=ExtendedEncoder) + "\n")


def flatten_json(data: dict, separator: str = ".") -> dict:
    """Flatten nested JSON into flat dict with dotted keys.

    Example:
        {"a": {"b": 1}} -> {"a.b": 1}
    """
    result = {}

    def _flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}{separator}{key}" if prefix else key
                _flatten(value, new_key)
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                new_key = f"{prefix}{separator}{i}" if prefix else str(i)
                _flatten(value, new_key)
        else:
            result[prefix] = obj

    _flatten(data)
    return result


def get_nested(data: dict, path: str, default: Any = None, separator: str = ".") -> Any:
    """Get value from nested dict using dot notation.

    Example:
        get_nested({"a": {"b": 1}}, "a.b") -> 1
    """
    keys = path.split(separator)
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
