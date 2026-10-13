"""Dialect contract every backend must satisfy."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Dialect:
    name: str
    display_name: str
    sqlglot_name: str
    notes: str
    quote_ident: str = '"'
    limit_style: str = "limit"  # "limit" | "top" | "fetch"

    def quote(self, identifier: str) -> str:
        q = self.quote_ident
        escaped = identifier.replace(q, q * 2)
        return f"{q}{escaped}{q}"