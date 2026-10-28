# Tasks

Single-repo status, kept by hand. Last reviewed **2026-10-28**.

Tests cover the SQLite, DuckDB, identifier, CSV, JSON, Parquet, date and validator helpers, plus
regression tests for the fixes in `cache.py`, `api_utils.py`, `zip_utils.py` and
`excel_utils.py`; the remaining modules are exercised by use, not tests. No other repo imports
this one.

## Needs the owner

Nothing.

## Queue

From the 2026-10-07 inventory, still true on 2026-10-28.

| Item | Note |
|---|---|
| Duplicated helpers | Byte-size formatting in `converters.py` and `file_utils.py`; `table_exists`, `get_tables`, `get_columns` in both SQL modules with different return shapes; the email regex in `text_utils.py` and `validators.py` |
| Flat module names | `cache`, `validators`, `converters`, `scraper` can shadow other packages when the folder is on `sys.path`; a documented limitation until the repo is packaged, which the flat-copy design argues against |
