from __future__ import annotations

from aisqlgen.dialects.base import Dialect

DIALECT = Dialect(
    name="postgres",
    display_name="PostgreSQL 16",
    sqlglot_name="postgres",
    notes=(
        "Use ILIKE for case-insensitive matches. Prefer `now()` over `CURRENT_TIMESTAMP` "
        "for consistency. Interval literals: `INTERVAL '7 days'`. JSONB operators: `->`, `->>`, `@>`."
    ),
    quote_ident='"',
    limit_style="limit",
)