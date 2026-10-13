"""Orchestrates prompt building + LLM call + SQL extraction."""
from __future__ import annotations

import asyncio
import re

from aisqlgen.config.models import AppConfig
from aisqlgen.core.prompt_builder import PromptBuilder
from aisqlgen.services.llm_client import LLMClient
from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)

_FENCE = re.compile(r"```(?:sql)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


class QueryGenerator:
    def __init__(self, *, cfg: AppConfig, llm: LLMClient) -> None:
        self._cfg = cfg
        self._llm = llm

    def generate(self, *, prompt: str, schema_ddl: str | None) -> str:
        builder = PromptBuilder(
            dialect=self._cfg.dialect,
            schema_ddl=schema_ddl,
            schema_char_budget=self._cfg.schema_char_budget,
        )
        messages = builder.build(prompt)
        raw = asyncio.run(self._call(messages))
        return self._extract_sql(raw)

    async def _call(self, messages: list[dict[str, str]]) -> str:
        async with self._llm as client:
            return await client.chat(messages)

    @staticmethod
    def _extract_sql(raw: str) -> str:
        fenced = _FENCE.search(raw)
        if fenced:
            return fenced.group(1).strip()
        # No fence: strip a leading "SQL:" label if present.
        stripped = re.sub(r"^\s*sql\s*:\s*", "", raw, flags=re.IGNORECASE)
        return stripped.strip()