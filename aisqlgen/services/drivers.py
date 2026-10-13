"""Live DSN introspection. Imported lazily — optional drivers not required."""
from __future__ import annotations


def introspect(dsn: str) -> str:
    if dsn.startswith("postgres"):
        return _postgres(dsn)
    if dsn.startswith("mysql"):
        return _mysql(dsn)
    if dsn.startswith("mssql"):
        return _mssql(dsn)
    if dsn.startswith("sqlite"):
        return _sqlite(dsn)
    raise ValueError(f"unsupported DSN scheme: {dsn.split(':', 1)[0]}")


def _postgres(dsn: str) -> str:
    import psycopg  # type: ignore[import-not-found]

    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT table_name, column_name, data_type FROM information_schema.columns "
            "WHERE table_schema = 'public' ORDER BY table_name, ordinal_position"
        )
        return _rows_to_summary(cur.fetchall())


def _mysql(dsn: str) -> str:
    import pymysql  # type: ignore[import-not-found]

    conn = pymysql.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_name, column_name, data_type FROM information_schema.columns "
                "WHERE table_schema = DATABASE() ORDER BY table_name, ordinal_position"
            )
            return _rows_to_summary(cur.fetchall())
    finally:
        conn.close()


def _mssql(dsn: str) -> str:
    import pyodbc  # type: ignore[import-not-found]

    with pyodbc.connect(dsn) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT table_name, column_name, data_type FROM information_schema.columns "
            "ORDER BY table_name, ordinal_position"
        )
        return _rows_to_summary(cur.fetchall())


def _sqlite(dsn: str) -> str:
    import sqlite3

    path = dsn.split("///", 1)[-1]
    with sqlite3.connect(path) as conn:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        lines: list[str] = []
        for (table,) in cur.fetchall():
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            rendered = ", ".join(f"{c[1]} {c[2]}" for c in cols)
            lines.append(f"{table}({rendered})")
        return "\n".join(lines)


def _rows_to_summary(rows: list[tuple[str, str, str]]) -> str:
    grouped: dict[str, list[str]] = {}
    for table, column, dtype in rows:
        grouped.setdefault(table, []).append(f"{column} {dtype}")
    return "\n".join(f"{t}({', '.join(cols)})" for t, cols in grouped.items())