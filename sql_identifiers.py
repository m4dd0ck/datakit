"""Safe handling of SQL identifiers and literals that cannot be bound as parameters.

Table and column names cannot be passed as query parameters in SQLite or DuckDB,
so every helper that splices a name into SQL goes through ``quote_identifier``.
File paths inside ``read_csv('...')`` / ``COPY ... TO '...'`` cannot be bound in
every statement either, so they go through ``quote_literal``.
"""

import re

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class InvalidIdentifierError(ValueError):
    """Raised when a table or column name is not a plain SQL identifier."""


def validate_identifier(name: str) -> str:
    """Return ``name`` unchanged if it is a plain identifier, else raise.

    Accepts letters, digits and underscores, not starting with a digit.
    Dotted names (``schema.table``) are rejected on purpose: pass the schema
    separately or quote each part yourself.

    Raises:
        InvalidIdentifierError: if the name contains anything else.
    """
    if not isinstance(name, str) or not _IDENTIFIER.match(name):
        raise InvalidIdentifierError(f"Not a valid SQL identifier: {name!r}")
    return name


def quote_identifier(name: str) -> str:
    """Validate ``name`` and wrap it in double quotes for use in SQL.

    Double-quoting also keeps reserved words (``order``, ``group``) usable
    as table or column names.
    """
    return f'"{validate_identifier(name)}"'


def quote_literal(value: str) -> str:
    """Wrap a string in single quotes, doubling any embedded single quotes."""
    return "'" + str(value).replace("'", "''") + "'"
