"""Parquet file utilities."""

from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq


def read_parquet(
    path: str | Path,
    columns: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Read Parquet file into list of dicts.

    Args:
        path: Path to Parquet file
        columns: Specific columns to read (None for all)

    Returns:
        List of dicts, one per row
    """
    table = pq.read_table(path, columns=columns)
    return table.to_pylist()


def read_parquet_df(
    path: str | Path,
    columns: list[str] | None = None,
):
    """Read Parquet file into pandas DataFrame.

    Args:
        path: Path to Parquet file
        columns: Specific columns to read (None for all)

    Returns:
        pandas DataFrame
    """
    table = pq.read_table(path, columns=columns)
    return table.to_pandas()


def write_parquet(
    data: list[dict[str, Any]],
    path: str | Path,
    compression: str = "snappy",
) -> None:
    """Write list of dicts to Parquet file.

    Args:
        data: List of dicts to write
        path: Output path
        compression: Compression codec (snappy, gzip, zstd, none)
    """
    if not data:
        return

    table = pa.Table.from_pylist(data)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path, compression=compression)


def write_parquet_df(
    df,
    path: str | Path,
    compression: str = "snappy",
) -> None:
    """Write pandas DataFrame to Parquet file.

    Args:
        df: pandas DataFrame
        path: Output path
        compression: Compression codec (snappy, gzip, zstd, none)
    """
    table = pa.Table.from_pandas(df)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path, compression=compression)


def get_schema(path: str | Path) -> list[dict[str, str]]:
    """Get schema of a Parquet file.

    Args:
        path: Path to Parquet file

    Returns:
        List of dicts with 'name' and 'type' keys
    """
    schema = pq.read_schema(path)
    return [{"name": field.name, "type": str(field.type)} for field in schema]


def get_metadata(path: str | Path) -> dict[str, Any]:
    """Get metadata from Parquet file.

    Args:
        path: Path to Parquet file

    Returns:
        Dict with num_rows, num_columns, num_row_groups, size_bytes
    """
    metadata = pq.read_metadata(path)
    return {
        "num_rows": metadata.num_rows,
        "num_columns": metadata.num_columns,
        "num_row_groups": metadata.num_row_groups,
        "size_bytes": Path(path).stat().st_size,
        "created_by": metadata.created_by,
    }


def get_row_count(path: str | Path) -> int:
    """Get row count without reading full file."""
    metadata = pq.read_metadata(path)
    return metadata.num_rows


def read_row_group(
    path: str | Path,
    row_group: int,
    columns: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Read a specific row group from Parquet file.

    Useful for processing large files in chunks.

    Args:
        path: Path to Parquet file
        row_group: Row group index (0-based)
        columns: Specific columns to read

    Returns:
        List of dicts for that row group
    """
    parquet_file = pq.ParquetFile(path)
    table = parquet_file.read_row_group(row_group, columns=columns)
    return table.to_pylist()


def iter_row_groups(
    path: str | Path,
    columns: list[str] | None = None,
):
    """Iterate over row groups in a Parquet file.

    Yields list of dicts for each row group. Memory-efficient
    for large files.

    Args:
        path: Path to Parquet file
        columns: Specific columns to read

    Yields:
        List of dicts for each row group
    """
    parquet_file = pq.ParquetFile(path)
    for i in range(parquet_file.metadata.num_row_groups):
        table = parquet_file.read_row_group(i, columns=columns)
        yield table.to_pylist()


def merge_parquet_files(
    input_paths: list[str | Path],
    output_path: str | Path,
    compression: str = "snappy",
) -> int:
    """Merge multiple Parquet files into one.

    Args:
        input_paths: List of input Parquet files
        output_path: Output file path
        compression: Compression codec

    Returns:
        Total number of rows in merged file
    """
    tables = [pq.read_table(p) for p in input_paths]
    merged = pa.concat_tables(tables)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(merged, output_path, compression=compression)
    return merged.num_rows


def partition_by(
    path: str | Path,
    output_dir: str | Path,
    partition_cols: list[str],
    compression: str = "snappy",
) -> None:
    """Write Parquet file partitioned by columns.

    Creates directory structure like:
    output_dir/col1=val1/col2=val2/data.parquet

    Args:
        path: Input Parquet file
        output_dir: Output directory
        partition_cols: Columns to partition by
        compression: Compression codec
    """
    table = pq.read_table(path)
    pq.write_to_dataset(
        table,
        root_path=str(output_dir),
        partition_cols=partition_cols,
        compression=compression,
    )


def filter_parquet(
    path: str | Path,
    output_path: str | Path,
    filters: list[tuple],
    compression: str = "snappy",
) -> int:
    """Filter Parquet file using predicate pushdown.

    Args:
        path: Input Parquet file
        output_path: Output file path
        filters: List of filter tuples, e.g. [("col", ">", 5), ("col2", "==", "value")]
        compression: Compression codec

    Returns:
        Number of rows in filtered output
    """
    table = pq.read_table(path, filters=filters)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, output_path, compression=compression)
    return table.num_rows
