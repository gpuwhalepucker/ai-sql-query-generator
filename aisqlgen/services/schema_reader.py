"""Summarize a schema so it fits the prompt budget without losing table names."""
from __future__ import annotations

import re

from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)

_CREATE = re.compile(r"CREATE\s+TABLE\s+([`\"\[]?[\w.]+[`\"\]]?)\s*\((.*?)\)\s*;", re.I | re.S)
_COL = re.compile(r"^\s*([`\"\[]?[\w]+[`\"\]]?)\s+([A-Za-z][\w()]*)", re.M)


class SchemaReader:
    def summarize_ddl(self, ddl: str) -> str:
        tables = _CREATE.findall(ddl)
        if not tables:
            return ddl[:8_000]

        lines: list[str] = []
        for name, body in tables:
            cols = [f"{c[0]} {c[1]}" for c in _COL.findall(body)]
            lines.append(f"{name}({', '.join(cols)})")
        return "\n".join(lines)

    def summarize_live(self, dsn: str) -> str:
        # Live introspection is dialect-specific; delegate to the driver module.
        from aisqlgen.services.drivers import introspect

        return introspect(dsn)