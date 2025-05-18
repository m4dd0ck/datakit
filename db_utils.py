"""SQLite database utilities."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator


@contextmanager
def get_connection(
    db_path: str | Path,
    row_factory: bool = True,
) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite connection.

    Args:
        db_path: Path to database file
        row_factory: If True, return rows as dicts

    Yields:
        Database connection
    """
    conn = sqlite3.connect(db_path)
    if row_factory:
        conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def execute_query(
    db_path: str | Path,
    query: str,
    params: tuple | dict | None = None,
) -> list[dict[str, Any]]:
    """Execute a SELECT query and return results as dicts.

    Args:
        db_path: Path to database
        query: SQL query string
        params: Query parameters

    Returns:
        List of dicts, one per row
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return [dict(row) for row in cursor.fetchall()]


def execute_write(
    db_path: str | Path,
    query: str,
    params: tuple | dict | None = None,
    many: list | None = None,
) -> int:
    """Execute an INSERT/UPDATE/DELETE query.

    Args:
        db_path: Path to database
        query: SQL query string
        params: Query parameters (for single insert)
        many: List of parameter tuples (for bulk insert)

    Returns:
        Number of rows affected
    """
    with get_connection(db_path, row_factory=False) as conn:
        cursor = conn.cursor()
        if many:
            cursor.executemany(query, many)
        elif params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.rowcount


def table_exists(db_path: str | Path, table_name: str) -> bool:
    """Check if a table exists in the database."""
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    result = execute_query(db_path, query, (table_name,))
    return len(result) > 0


def get_tables(db_path: str | Path) -> list[str]:
    """Get list of all tables in database."""
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    result = execute_query(db_path, query)
    return [row["name"] for row in result]


def get_columns(db_path: str | Path, table_name: str) -> list[dict[str, Any]]:
    """Get column info for a table."""
    query = f"PRAGMA table_info({table_name})"
    return execute_query(db_path, query)


def insert_dict(db_path: str | Path, table_name: str, data: dict[str, Any]) -> int:
    """Insert a dict as a row into a table.

    Args:
        db_path: Path to database
        table_name: Table to insert into
        data: Dict of column->value pairs

    Returns:
        Inserted row ID
    """
    columns = ", ".join(data.keys())
    placeholders = ", ".join("?" * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    with get_connection(db_path, row_factory=False) as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return cursor.lastrowid


def insert_many(
    db_path: str | Path,
    table_name: str,
    data: list[dict[str, Any]],
) -> int:
    """Insert multiple dicts as rows.

    Args:
        db_path: Path to database
        table_name: Table to insert into
        data: List of dicts to insert

    Returns:
        Number of rows inserted
    """
    if not data:
        return 0

    columns = list(data[0].keys())
    col_str = ", ".join(columns)
    placeholders = ", ".join("?" * len(columns))
    query = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})"

    rows = [tuple(d.get(c) for c in columns) for d in data]
    return execute_write(db_path, query, many=rows)
