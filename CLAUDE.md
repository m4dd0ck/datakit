# datakit: agent rules

Instructions for coding agents working in this repo; a human reader wants `README.md`. Read
`README.md` for how it works, `RUNBOOK.md` for procedures, `TASK.md` for what is open. The
owner's global agent rules apply on top of these.

- Public repo: no personal data in code, tests or examples; no keys.
- Real-time commits only, never backdated; no AI attribution lines.
- Release steps: `RUNBOOK.md` §Release.
- Traps: never splice a table name, path or delimiter into SQL; go through `sql_identifiers.py`
  (the 2026-10-06 fix). Keep modules flat and independent so a single file can be copied out;
  do not add a package init file or cross-imports.
