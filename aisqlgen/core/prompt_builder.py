"""Assemble the system + user prompt sent to the LLM."""
from __future__ import annotations

from aisqlgen.dialects.registry import get_dialect
from aisqlgen.prompts.system import SYSTEM_PROMPT
from aisqlgen.prompts.templates import USER_TEMPLATE


class PromptBuilder:
    def __init__(self, *, dialect: str, schema_ddl: str | None, schema_char_budget: int = 32_000) -> None:
        self._dialect = get_dialect(dialect)
        self._schema = (schema_ddl or "")[:schema_char_budget]

    def build(self, prompt: str) -> list[dict[str, str]]:
        system = SYSTEM_PROMPT.format(dialect_name=self._dialect.display_name)
        user = USER_TEMPLATE.format(
            dialect_name=self._dialect.display_name,
            dialect_notes=self._dialect.notes,
            schema_ddl=self._schema or "-- (no schema provided)",
            prompt=prompt.strip(),
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]