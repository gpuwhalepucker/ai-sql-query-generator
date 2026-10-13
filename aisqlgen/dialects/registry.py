"""Resolve dialect name -> Dialect instance."""
from __future__ import annotations

from aisqlgen.dialects import mssql, mysql, postgres, sqlite
from aisqlgen.dialects.base import Dialect

_REGISTRY: dict[str, Dialect] = {
    d.name: d
    for d in (postgres.DIALECT, mysql.DIALECT, sqlite.DIALECT, mssql.DIALECT)
}


def get_dialect(name: str) -> Dialect:
    key = name.strip().lower()
    if key not in _REGISTRY:
        raise KeyError(f"unknown dialect: {name!r}. known: {sorted(_REGISTRY)}")
    return _REGISTRY[key]


def all_dialects() -> list[Dialect]:
    return list(_REGISTRY.values())