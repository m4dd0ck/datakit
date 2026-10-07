import pytest

import db_utils
from sql_identifiers import InvalidIdentifierError


@pytest.fixture
def db(tmp_path):
    path = tmp_path / "t.sqlite"
    db_utils.execute_write(
        path, 'CREATE TABLE "order" (id INTEGER PRIMARY KEY, name TEXT, qty INTEGER)'
    )
    return path


def test_insert_dict_and_read_back(db):
    row_id = db_utils.insert_dict(db, "order", {"name": "a", "qty": 1})
    assert row_id == 1
    rows = db_utils.execute_query(db, 'SELECT name, qty FROM "order"')
    assert rows == [{"name": "a", "qty": 1}]


def test_insert_many_returns_count(db):
    n = db_utils.insert_many(db, "order", [{"name": "a", "qty": 1}, {"name": "b", "qty": 2}])
    assert n == 2
    assert db_utils.get_tables(db) == ["order"]
    assert [c["name"] for c in db_utils.get_columns(db, "order")] == ["id", "name", "qty"]


def test_values_are_bound_not_interpolated(db):
    hostile = 'x\'); DROP TABLE "order"; --'
    db_utils.insert_dict(db, "order", {"name": hostile, "qty": 0})
    assert db_utils.table_exists(db, "order")
    assert db_utils.execute_query(db, 'SELECT name FROM "order"')[0]["name"] == hostile


def test_hostile_table_or_column_name_is_rejected(db):
    with pytest.raises(InvalidIdentifierError):
        db_utils.insert_dict(db, 'order"; DROP TABLE "order', {"name": "a"})
    with pytest.raises(InvalidIdentifierError):
        db_utils.insert_dict(db, "order", {"name) VALUES ('x'); --": "a"})
    with pytest.raises(InvalidIdentifierError):
        db_utils.get_columns(db, "order) ; DROP TABLE x; --")
    assert db_utils.table_exists(db, "order")
