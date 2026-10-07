import pytest

from sql_identifiers import (
    InvalidIdentifierError,
    quote_identifier,
    quote_literal,
    validate_identifier,
)


@pytest.mark.parametrize("name", ["users", "_tmp", "Order2", "snake_case_name"])
def test_plain_identifiers_pass(name):
    assert validate_identifier(name) == name
    assert quote_identifier(name) == f'"{name}"'


@pytest.mark.parametrize(
    "name",
    ["", "1abc", "users; DROP TABLE x", "a b", "schema.table", 'a"b', "x--", None, 42],
)
def test_anything_else_is_rejected(name):
    with pytest.raises(InvalidIdentifierError):
        validate_identifier(name)


def test_quote_literal_doubles_embedded_quotes():
    assert quote_literal("plain") == "'plain'"
    assert quote_literal("it's") == "'it''s'"
    assert quote_literal("/tmp/o'neil/out.csv") == "'/tmp/o''neil/out.csv'"
