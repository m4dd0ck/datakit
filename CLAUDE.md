# datakit: agent rules

Read `README.md` for how it works, `RUNBOOK.md` for procedures, `TASK.md` for what is open.
Global rules in `~/.claude/CLAUDE.md` still apply.

- Public repo: no personal data in code, tests or examples; no keys.
- Real-time commits only, never backdated; no AI attribution lines.
- Release steps: `~/developer/hq/CONVENTIONS.md` §Versioning.
- Traps: never splice a table name, path or delimiter into SQL; go through `sql_identifiers.py`
  (the 2026-10-06 fix). Keep modules flat and independent so a single file can be copied out;
  do not add a package init file or cross-imports.
