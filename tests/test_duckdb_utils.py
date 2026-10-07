import csv

import pytest

import duckdb_utils
from sql_identifiers import InvalidIdentifierError


@pytest.fixture
def csv_file(tmp_path):
    path = tmp_path / "in.csv"
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name"])
        w.writerows([[1, "a"], [2, "b"], [3, "c"]])
    return path


def test_load_csv_then_query_and_count(tmp_path, csv_file):
    db = tmp_path / "t.duckdb"
    assert duckdb_utils.load_csv(csv_file, "people", db) == 3
    assert duckdb_utils.row_count(db, "people") == 3
    assert duckdb_utils.table_exists(db, "people")
    assert duckdb_utils.get_tables(db) == ["people"]
    assert [c["name"] for c in duckdb_utils.get_columns(db, "people")] == ["id", "name"]


def test_export_and_reload_parquet_with_quote_in_path(tmp_path, csv_file):
    db = tmp_path / "t.duckdb"
    duckdb_utils.load_csv(csv_file, "people", db)
    out = tmp_path / "o'neil.parquet"
    duckdb_utils.export_parquet("SELECT * FROM people WHERE id > 1", out, db)
    assert duckdb_utils.load_parquet(out, "people2", db) == 2


def test_export_csv_header_flag(tmp_path, csv_file):
    db = tmp_path / "t.duckdb"
    duckdb_utils.load_csv(csv_file, "people", db)
    out = tmp_path / "out.csv"
    duckdb_utils.export_csv("SELECT id FROM people ORDER BY id", out, db, header=False)
    assert out.read_text().split() == ["1", "2", "3"]


def test_hostile_table_name_is_rejected(tmp_path, csv_file):
    db = tmp_path / "t.duckdb"
    duckdb_utils.load_csv(csv_file, "people", db)
    with pytest.raises(InvalidIdentifierError):
        duckdb_utils.row_count(db, "people; DROP TABLE people; --")
    with pytest.raises(InvalidIdentifierError):
        duckdb_utils.load_csv(csv_file, "x; DROP TABLE people", db)
    assert duckdb_utils.table_exists(db, "people")
