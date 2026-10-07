"""DuckDB utilities for analytics queries."""

from pathlib import Path
from typing import Any

import duckdb

from sql_identifiers import quote_identifier, quote_literal


def connect(
    db_path: str | Path | None = None, read_only: bool = False
) -> duckdb.DuckDBPyConnection:
    """Connect to DuckDB database.

    Args:
        db_path: Path to database file, or None for in-memory
        read_only: Open in read-only mode

    Returns:
        DuckDB connection
    """
    if db_path is None:
        return duckdb.connect(":memory:")
    return duckdb.connect(str(db_path), read_only=read_only)


def query(
    sql: str,
    db_path: str | Path | None = None,
    params: list | dict | None = None,
) -> list[dict[str, Any]]:
    """Execute a query and return results as list of dicts.

    Args:
        sql: SQL query string
        db_path: Database path (None for in-memory)
        params: Query parameters

    Returns:
        List of dicts, one per row
    """
    con = connect(db_path, read_only=True)
    try:
        if params:
            result = con.execute(sql, params)
        else:
            result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        return [dict(zip(columns, row, strict=True)) for row in result.fetchall()]
    finally:
        con.close()


def query_df(
    sql: str,
    db_path: str | Path | None = None,
    params: list | dict | None = None,
):
    """Execute a query and return results as DataFrame.

    Args:
        sql: SQL query string
        db_path: Database path (None for in-memory)
        params: Query parameters

    Returns:
        pandas DataFrame
    """
    con = connect(db_path, read_only=True)
    try:
        if params:
            return con.execute(sql, params).df()
        return con.execute(sql).df()
    finally:
        con.close()


def execute(
    sql: str,
    db_path: str | Path,
    params: list | dict | None = None,
) -> int:
    """Execute a write query (INSERT, UPDATE, DELETE, CREATE, etc).

    Args:
        sql: SQL statement
        db_path: Database path
        params: Query parameters

    Returns:
        Number of rows affected (for INSERT/UPDATE/DELETE)
    """
    con = connect(db_path)
    try:
        if params:
            result = con.execute(sql, params)
        else:
            result = con.execute(sql)
        con.commit()
        return result.fetchone()[0] if result.description else 0
    finally:
        con.close()


def load_parquet(
    parquet_path: str | Path,
    table_name: str,
    db_path: str | Path,
) -> int:
    """Load a Parquet file into a DuckDB table.

    Args:
        parquet_path: Path to Parquet file
        table_name: Name for the table
        db_path: Database path

    Returns:
        Number of rows loaded
    """
    con = connect(db_path)
    try:
        table = quote_identifier(table_name)
        con.execute(
            f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_parquet(?)",
            [str(parquet_path)],
        )
        result = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        return result[0]
    finally:
        con.close()


def load_csv(
    csv_path: str | Path,
    table_name: str,
    db_path: str | Path,
    header: bool = True,
    delimiter: str = ",",
) -> int:
    """Load a CSV file into a DuckDB table.

    Args:
        csv_path: Path to CSV file
        table_name: Name for the table
        db_path: Database path
        header: CSV has header row
        delimiter: Column delimiter

    Returns:
        Number of rows loaded
    """
    con = connect(db_path)
    try:
        table = quote_identifier(table_name)
        con.execute(
            f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv(?, header=?, delim=?)",
            [str(csv_path), bool(header), delimiter],
        )
        result = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        return result[0]
    finally:
        con.close()


def export_parquet(
    sql: str,
    output_path: str | Path,
    db_path: str | Path | None = None,
) -> None:
    """Export query results to Parquet file.

    Args:
        sql: SQL query
        output_path: Output Parquet file path
        db_path: Database path
    """
    con = connect(db_path, read_only=True)
    try:
        con.execute(f"COPY ({sql}) TO {quote_literal(str(output_path))} (FORMAT PARQUET)")
    finally:
        con.close()


def export_csv(
    sql: str,
    output_path: str | Path,
    db_path: str | Path | None = None,
    header: bool = True,
) -> None:
    """Export query results to CSV file.

    Args:
        sql: SQL query
        output_path: Output CSV file path
        db_path: Database path
        header: Include header row
    """
    con = connect(db_path, read_only=True)
    try:
        header_flag = "true" if header else "false"
        con.execute(
            f"COPY ({sql}) TO {quote_literal(str(output_path))} (FORMAT CSV, HEADER {header_flag})"
        )
    finally:
        con.close()


def table_exists(db_path: str | Path, table_name: str) -> bool:
    """Check if a table exists in the database.

    Args:
        db_path: Path to DuckDB database
        table_name: Name of table to check
    """
    result = query(
        "SELECT COUNT(*) as cnt FROM information_schema.tables WHERE table_name = ?",
        db_path,
        [table_name],
    )
    return result[0]["cnt"] > 0


def get_tables(db_path: str | Path) -> list[str]:
    """Get list of all table names in database."""
    result = query(
        "SELECT table_name FROM information_schema.tables\n"
        "WHERE table_schema = 'main' ORDER BY table_name",
        db_path,
    )
    return [row["table_name"] for row in result]


def get_columns(db_path: str | Path, table_name: str) -> list[dict[str, str]]:
    """Get column info for a table.

    Returns:
        List of dicts with 'name' and 'type' keys
    """
    result = query(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = ?
        ORDER BY ordinal_position
        """,
        db_path,
        [table_name],
    )
    return [{"name": row["column_name"], "type": row["data_type"]} for row in result]


def row_count(db_path: str | Path, table_name: str) -> int:
    """Get row count for a table.

    Args:
        db_path: Path to DuckDB database
        table_name: Name of table to count
    """
    result = query(f"SELECT COUNT(*) as cnt FROM {quote_identifier(table_name)}", db_path)
    return result[0]["cnt"]
