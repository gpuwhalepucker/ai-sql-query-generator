from __future__ import annotations

from aisqlgen.dialects.base import Dialect

DIALECT = Dialect(
    name="sqlite",
    display_name="SQLite 3.45",
    sqlglot_name="sqlite",
    notes=(
        "No native boolean type — use 0/1. `datetime('now')` for timestamps. "
        "No RIGHT JOIN before 3.39. Prefer `WITH` CTEs over nested subqueries."
    ),
    quote_ident='"',
    limit_style="limit",
)