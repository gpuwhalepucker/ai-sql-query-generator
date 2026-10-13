"""Reject unsafe statements before they ever reach a connection.

This is the last line of defense, not the first. The prompt layer already
asks for read-only SQL; this module assumes the model may ignore that.
"""
from __future__ import annotations

import re

import sqlglot
from sqlglot import exp

from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)


class UnsafeStatementError(ValueError):
    """Raised when generated SQL fails a guard check."""


_WRITE_ROOTS: tuple[type[exp.Expression], ...] = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
    exp.TruncateTable,
)


class SqlGuard:
    def __init__(self, *, allow_write: bool = False, max_statements: int = 1, deny_keywords: list[str] | None = None) -> None:
        self._allow_write = allow_write
        self._max_statements = max_statements
        self._deny = [k.lower() for k in (deny_keywords or [])]

    def assert_safe(self, sql: str) -> None:
        stripped = sql.strip().rstrip(";")
        if not stripped:
            raise UnsafeStatementError("empty statement")

        lowered = stripped.lower()
        for kw in self._deny:
            if re.search(rf"\b{re.escape(kw)}\b", lowered):
                raise UnsafeStatementError(f"denied keyword: {kw}")

        try:
            parsed = sqlglot.parse(stripped)
        except Exception as exc:  # noqa: BLE001 — sqlglot throws bare Exception on some dialects
            raise UnsafeStatementError(f"unparseable SQL: {exc}") from exc

        statements = [s for s in parsed if s is not None]
        if len(statements) > self._max_statements:
            raise UnsafeStatementError(f"stacked statements not allowed ({len(statements)} found)")

        if self._allow_write:
            return

        for stmt in statements:
            for node in stmt.walk():
                if isinstance(node, _WRITE_ROOTS):
                    raise UnsafeStatementError(f"write statement rejected: {type(node).__name__}")