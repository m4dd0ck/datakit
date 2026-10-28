import csv_utils


def test_write_then_read_round_trips_rows(tmp_path):
    path = tmp_path / "out.csv"
    rows = [{"name": "a", "qty": "1"}, {"name": "b", "qty": "2"}]
    csv_utils.write_csv(path, rows)
    assert csv_utils.read_csv(path) == rows


def test_read_csv_uses_given_delimiter(tmp_path):
    path = tmp_path / "semi.csv"
    path.write_text("name;qty\na;1\n", encoding="utf-8")
    assert csv_utils.read_csv(path, delimiter=";") == [{"name": "a", "qty": "1"}]


def test_read_csv_keeps_quoted_commas_in_one_field(tmp_path):
    path = tmp_path / "quoted.csv"
    path.write_text('name,note\na,"x, y"\n', encoding="utf-8")
    assert csv_utils.read_csv(path) == [{"name": "a", "note": "x, y"}]


def test_write_csv_with_no_rows_creates_no_file(tmp_path):
    path = tmp_path / "empty.csv"
    csv_utils.write_csv(path, [])
    assert not path.exists()


def test_write_csv_uses_given_fieldnames_order(tmp_path):
    path = tmp_path / "ordered.csv"
    csv_utils.write_csv(path, [{"a": 1, "b": 2}], fieldnames=["b", "a"])
    assert path.read_text(encoding="utf-8").splitlines()[0] == "b,a"


def test_clean_csv_strips_whitespace_from_strings():
    assert csv_utils.clean_csv([{"name": "  a  ", "qty": 1}]) == [{"name": "a", "qty": 1}]


def test_clean_csv_drops_rows_whose_values_are_all_empty():
    data = [{"name": " ", "qty": ""}, {"name": "a", "qty": ""}]
    assert csv_utils.clean_csv(data) == [{"name": "a", "qty": ""}]


def test_clean_csv_keeps_empty_rows_when_asked():
    data = [{"name": "", "qty": ""}]
    assert csv_utils.clean_csv(data, remove_empty_rows=False) == data


def test_clean_csv_lowercases_keys_when_asked():
    assert csv_utils.clean_csv([{"Name": "a"}], lowercase_keys=True) == [{"name": "a"}]


def test_filter_columns_keeps_listed_columns_and_fills_missing_with_none():
    data = [{"a": 1, "b": 2, "c": 3}]
    assert csv_utils.filter_columns(data, ["a", "z"]) == [{"a": 1, "z": None}]


def test_rename_columns_renames_mapped_keys_only():
    data = [{"a": 1, "b": 2}]
    assert csv_utils.rename_columns(data, {"a": "x"}) == [{"x": 1, "b": 2}]
