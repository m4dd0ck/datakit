# DataKit

Collection of various tools universalized for cross-project use. DRY and KISS.

## Install

```bash
pip install -r requirements.txt
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

Most functions have docstrings.

## TODO

- [ ] Add proper tests
- [ ] Package this properly
- [ ] Better error handling in some places
