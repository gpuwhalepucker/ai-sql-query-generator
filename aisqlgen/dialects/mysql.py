from __future__ import annotations

from aisqlgen.dialects.base import Dialect

DIALECT = Dialect(
    name="mysql",
    display_name="MySQL 8.0",
    sqlglot_name="mysql",
    notes=(
        "Use backticks for identifiers. `LIMIT n OFFSET m` ordering matters — OFFSET requires LIMIT. "
        "Date arithmetic: `DATE_SUB(now(), INTERVAL 7 DAY)`."
    ),
    quote_ident="`",
    limit_style="limit",
)