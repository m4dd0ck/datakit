# Tasks

Single-repo status. Hand-kept; dates are absolute. Last reviewed **2026-10-20**. Cross-repo
items are in `~/developer/hq/OPEN_ITEMS.md`.

Tests cover the SQLite, DuckDB and identifier helpers; the other sixteen modules are exercised
by use, not tests. Nothing in `~/developer` imports this repo.

## Needs the owner

| Item | Why it is stuck | Added |
|---|---|---|
| **Move the clone under `~/developer/portfolio/`, or archive it** | The hq repo map's verdict is keep and move, while its consolidation note says archive; nothing uses the repo either way. The move is in hq OPEN_ITEMS §Codebase review and waits on the owner's sign-off | 2026-10-16 |

## Queue

From the 2026-10-07 inventory, still true on 2026-10-20.

| Item | Note |
|---|---|
| Tests for the untested modules | Start with the ones that hold logic: `csv_utils.py`, `json_utils.py`, `parquet_utils.py`, `dt_utils.py`, `validators.py` |
| `csv_utils.read_csv(skip_header=True)` | Drops the first line and then lets `DictReader` take the second as the header; the name suggests the opposite |
| `cache.cached` | Uses `None` as the miss marker, so a `None` result is never cached; and it does not apply `functools.wraps` |
| `api_utils.APIClient` | Retries on every `RequestException`, including 4xx responses raised by `raise_for_status`, and reimplements the module's own `retry` decorator |
| `zip_utils.create_zip` | Includes the output zip in itself when the output path sits inside the directory being zipped |
| `excel_utils.read_excel` | Leaves the workbook open when the sheet is empty |
| Duplicated helpers | Byte-size formatting in `converters.py` and `file_utils.py`; `table_exists`, `get_tables`, `get_columns` in both SQL modules with different return shapes; the email regex in `text_utils.py` and `validators.py` |
| Flat module names | `cache`, `validators`, `converters`, `scraper` can shadow other packages when the folder is on `sys.path`; a documented limitation until the repo is packaged, which the flat-copy design argues against |
