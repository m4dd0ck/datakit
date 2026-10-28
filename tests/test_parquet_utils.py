import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

import parquet_utils

ROWS = [
    {"id": 1, "region": "east", "amount": 10.0},
    {"id": 2, "region": "west", "amount": 20.0},
    {"id": 3, "region": "east", "amount": 30.0},
]


@pytest.fixture
def parquet_path(tmp_path):
    path = tmp_path / "rows.parquet"
    parquet_utils.write_parquet(ROWS, path)
    return path


def test_write_then_read_round_trips_rows(parquet_path):
    assert parquet_utils.read_parquet(parquet_path) == ROWS


def test_read_parquet_returns_only_requested_columns(parquet_path):
    assert parquet_utils.read_parquet(parquet_path, columns=["id"]) == [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]


def test_write_parquet_with_no_rows_creates_no_file(tmp_path):
    path = tmp_path / "empty.parquet"
    parquet_utils.write_parquet([], path)
    assert not path.exists()


def test_dataframe_write_then_read_round_trips(tmp_path):
    path = tmp_path / "df.parquet"
    parquet_utils.write_parquet_df(pd.DataFrame(ROWS), path)
    assert parquet_utils.read_parquet_df(path).to_dict("records") == ROWS


def test_get_schema_lists_column_names_and_types(parquet_path):
    assert parquet_utils.get_schema(parquet_path) == [
        {"name": "id", "type": "int64"},
        {"name": "region", "type": "string"},
        {"name": "amount", "type": "double"},
    ]


def test_get_metadata_reports_rows_columns_and_size(parquet_path):
    metadata = parquet_utils.get_metadata(parquet_path)
    assert metadata["num_rows"] == 3
    assert metadata["num_columns"] == 3
    assert metadata["num_row_groups"] == 1
    assert metadata["size_bytes"] == parquet_path.stat().st_size


def test_get_row_count_matches_rows_written(parquet_path):
    assert parquet_utils.get_row_count(parquet_path) == 3


@pytest.fixture
def two_group_path(tmp_path):
    path = tmp_path / "groups.parquet"
    pq.write_table(pa.Table.from_pylist(ROWS), path, row_group_size=2)
    return path


def test_read_row_group_returns_only_that_group(two_group_path):
    assert parquet_utils.read_row_group(two_group_path, 1) == [ROWS[2]]


def test_iter_row_groups_yields_each_group_in_order(two_group_path):
    assert list(parquet_utils.iter_row_groups(two_group_path, columns=["id"])) == [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}],
    ]


def test_merge_parquet_files_concatenates_rows(tmp_path):
    first = tmp_path / "a.parquet"
    second = tmp_path / "b.parquet"
    parquet_utils.write_parquet(ROWS[:1], first)
    parquet_utils.write_parquet(ROWS[1:], second)
    output = tmp_path / "out" / "merged.parquet"
    assert parquet_utils.merge_parquet_files([first, second], output) == 3
    assert parquet_utils.read_parquet(output) == ROWS


def test_partition_by_writes_one_directory_per_value(parquet_path, tmp_path):
    output_dir = tmp_path / "parts"
    parquet_utils.partition_by(parquet_path, output_dir, ["region"])
    assert sorted(p.name for p in output_dir.iterdir()) == ["region=east", "region=west"]
    east = pq.read_table(output_dir / "region=east").to_pylist()
    assert sorted(row["id"] for row in east) == [1, 3]


def test_filter_parquet_writes_only_matching_rows(parquet_path, tmp_path):
    output = tmp_path / "filtered.parquet"
    count = parquet_utils.filter_parquet(parquet_path, output, [("amount", ">", 15.0)])
    assert count == 2
    assert [row["id"] for row in parquet_utils.read_parquet(output)] == [2, 3]
