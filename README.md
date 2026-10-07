# DataKit

Flat folder of standalone Python helpers for everyday data work: CSV, Excel, Parquet, SQLite, DuckDB, dates, text, HTTP. Copy a module into a project or import the folder.

## Install

```bash
uv sync            # or: pip install -r requirements.txt
uv run pytest      # tests for the SQL helpers
```

## What's Here

- `csv_utils` - CSV reading/writing/cleaning
- `excel_utils` - XLSX operations
- `file_utils` - File operations
- `json_utils` - JSON helpers
- `dt_utils` - Datetime parsing
- `text_utils` - String cleaning
- `validators` - Validate emails, URLs, etc.
- `scraper` - Web scraping helpers
- `db_utils` - SQLite helpers
- `duckdb_utils` - DuckDB queries and imports
- `sql_identifiers` - validates and quotes table/column names for the two modules above
- `parquet_utils` - Parquet file operations
- `config_loader` - Load configs from various formats
- `log_setup` - Logging configuration
- `cache` - Simple file cache
- `api_utils` - API client with retry
- `cli_helpers` - Progress bars, colors
- `converters` - Unit conversions
- `zip_utils` - Zip file operations

## Usage

Import what you need:

```python
from csv_utils import read_csv, clean_csv
from dt_utils import parse_date
from file_utils import find_files
```

Most functions have docstrings. Table and column names passed to `db_utils` / `duckdb_utils` must be plain identifiers (`[A-Za-z_][A-Za-z0-9_]*`); anything else raises `InvalidIdentifierError` instead of being spliced into SQL. Values are always bound as parameters.

## Status

Tests cover the SQLite and DuckDB helpers. The rest is exercised by use, not tests.
