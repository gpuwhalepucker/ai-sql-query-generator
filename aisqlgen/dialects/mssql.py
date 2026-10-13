from __future__ import annotations

from aisqlgen.dialects.base import Dialect

DIALECT = Dialect(
    name="mssql",
    display_name="Microsoft SQL Server 2022",
    sqlglot_name="tsql",
    notes=(
        "Use `TOP (n)` or `OFFSET ... FETCH NEXT`. Identifiers in [brackets]. "
        "String concat with `+`. `GETDATE()` for current time."
    ),
    quote_ident="[",
    limit_style="top",
)