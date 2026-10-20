# Runbook

Procedures for datakit. `README.md` says what each module is; this file says what to run.

## On open

```bash
git status --short
git log -3 --oneline
```

## On close

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

## Use a module in another project

Copy the file across (the SQL helpers also need `sql_identifiers.py`), or put this folder on the
path and import the flat module name. Nothing here imports anything else in the folder apart
from that one pair, so a copied file works on its own once its third-party package is installed.

## Release

Follows `~/developer/hq/CONVENTIONS.md` §Versioning (portfolio repos):

1. On close checks green.
2. Bump `version` in `pyproject.toml`, `uv lock`, one `chore: Release vX.Y.Z` commit.
3. Annotated tag `vX.Y.Z`, push with `--tags`; tags only, no GitHub release, for this repo.
4. Commits in real time; never backdated.

## Restore on a new machine

Clone and `uv sync`. There is no data and no key.

## Validate

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
python3 ~/.claude/scripts/doc-check.py --repo .
```
