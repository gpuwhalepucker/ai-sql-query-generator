"""Handler for schema introspection + summarization."""
from __future__ import annotations

from pathlib import Path

from aisqlgen.services.schema_reader import SchemaReader


class SchemaHandler:
    def __init__(self, reader: SchemaReader) -> None:
        self._reader = reader

    def from_file(self, path: Path) -> str:
        return self._reader.summarize_ddl(path.read_text(encoding="utf-8"))

    def from_dsn(self, dsn: str) -> str:
        return self._reader.summarize_live(dsn)