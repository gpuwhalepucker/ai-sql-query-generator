# Contributing to ai-sql-query-generator

Thanks for wanting to poke at the tuber. This repo is a Windows desktop tool that turns natural-language prompts into dialect-aware SQL, and it is maintained by people who actually use it.

## Ground rules

- One feature per PR. If it touches the planner *and* the dialect layer, split it.
- Every new dialect goes in `aisqlgen/dialects/` with a matching test in `tests/`.
- Prompt templates live in `aisqlgen/prompts/` — no prompt strings hardcoded inside handlers.
- If you touch the schema introspection code, run the integration tests against both SQLite and Postgres before opening the PR.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pre-commit install
pytest -q
```

## Style

- `ruff` for lint, `black` for format, `mypy --strict` on `aisqlgen/core` and `aisqlgen/services`.
- Type hints on every public function. No `Any` unless you're wrapping a third-party boundary and you comment why.
- Logging via the `aisqlgen.utils.logging` helper, never bare `print`.

## Reporting bugs

Open an issue with: OS build, Python version, the prompt you typed, the dialect you selected, and the generated SQL. Redact connection strings.

## Code of conduct

Be a decent spud. Not negotiable.