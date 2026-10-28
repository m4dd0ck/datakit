import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pytest

import json_utils


def test_write_then_read_json_round_trips(tmp_path):
    path = tmp_path / "data.json"
    data = {"name": "café", "items": [1, 2]}
    json_utils.write_json(path, data)
    assert json_utils.read_json(path) == data


def test_write_json_keeps_non_ascii_unescaped_by_default(tmp_path):
    path = tmp_path / "data.json"
    json_utils.write_json(path, {"name": "café"})
    assert "café" in path.read_text(encoding="utf-8")


def test_write_json_creates_missing_parent_directories(tmp_path):
    path = tmp_path / "nested" / "dir" / "data.json"
    json_utils.write_json(path, [1])
    assert json_utils.read_json(path) == [1]


def test_encoder_serialises_dates_decimals_sets_and_paths():
    data = {
        "when": datetime(2026, 1, 2, 3, 4, 5),
        "day": date(2026, 1, 2),
        "amount": Decimal("1.5"),
        "tags": {"x"},
        "path": Path("a/b"),
    }
    assert json.loads(json.dumps(data, cls=json_utils.ExtendedEncoder)) == {
        "when": "2026-01-02T03:04:05",
        "day": "2026-01-02",
        "amount": 1.5,
        "tags": ["x"],
        "path": "a/b",
    }


def test_encoder_rejects_unknown_types():
    with pytest.raises(TypeError):
        json.dumps({"x": object()}, cls=json_utils.ExtendedEncoder)


def test_write_then_read_jsonl_round_trips(tmp_path):
    path = tmp_path / "data.jsonl"
    rows = [{"a": 1}, {"a": 2}]
    json_utils.write_jsonl(path, rows)
    assert json_utils.read_jsonl(path) == rows


def test_read_jsonl_skips_blank_lines(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text('{"a": 1}\n\n   \n{"a": 2}\n', encoding="utf-8")
    assert json_utils.read_jsonl(path) == [{"a": 1}, {"a": 2}]


def test_flatten_json_joins_nested_keys_and_list_indexes():
    data = {"a": {"b": 1, "c": [10, {"d": 2}]}}
    assert json_utils.flatten_json(data) == {"a.b": 1, "a.c.0": 10, "a.c.1.d": 2}


def test_flatten_json_uses_given_separator():
    assert json_utils.flatten_json({"a": {"b": 1}}, separator="/") == {"a/b": 1}


def test_get_nested_returns_value_at_path():
    assert json_utils.get_nested({"a": {"b": {"c": 3}}}, "a.b.c") == 3


def test_get_nested_returns_default_for_missing_path():
    assert json_utils.get_nested({"a": {"b": 1}}, "a.x", default="none") == "none"


def test_get_nested_returns_default_when_path_goes_through_a_non_dict():
    assert json_utils.get_nested({"a": 1}, "a.b") is None
