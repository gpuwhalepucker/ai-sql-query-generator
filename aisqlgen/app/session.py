"""Interactive + one-shot session. Owns schema context and the safety gate."""
from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from aisqlgen.config.models import AppConfig
from aisqlgen.core.guard import SqlGuard, UnsafeStatementError
from aisqlgen.services.generator import QueryGenerator
from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)
console = Console()


class Session:
    def __init__(self, *, generator: QueryGenerator, config: AppConfig, allow_write: bool = False) -> None:
        self._generator = generator
        self._config = config
        self._allow_write = allow_write
        self._guard = SqlGuard(allow_write=allow_write)
        self._schema_ddl: str | None = None

    def load_schema(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        # Cap to ~32k chars; longer dumps blow the prompt budget on small models.
        self._schema_ddl = text[:32_000]
        log.info("schema loaded: %d chars from %s", len(self._schema_ddl), path)

    def generate(self, prompt: str) -> str:
        sql = self._generator.generate(prompt=prompt, schema_ddl=self._schema_ddl)
        try:
            self._guard.assert_safe(sql)
        except UnsafeStatementError as exc:
            console.print(f"[red]guard rejected generated SQL:[/red] {exc}")
            raise
        return sql

    def run_repl(self) -> None:
        console.print("[bold green]aisqlgen[/bold green] — type a prompt, `:q` to quit, `:schema <path>` to load DDL.")
        while True:
            try:
                raw = Prompt.ask("[cyan]prompt[/cyan]").strip()
            except (EOFError, KeyboardInterrupt):
                console.print()
                return
            if not raw:
                continue
            if raw in {":q", ":quit", ":exit"}:
                return
            if raw.startswith(":schema "):
                self.load_schema(Path(raw.split(" ", 1)[1]))
                continue
            try:
                console.print(self.generate(raw))
            except Exception as exc:  # noqa: BLE001 — REPL must not die on one bad prompt
                log.exception("generation failed")
                console.print(f"[red]{exc}[/red]")