"""Handler for a single generate request. Keeps the service layer unaware of CLI."""
from __future__ import annotations

from dataclasses import dataclass

from aisqlgen.core.planner import classify
from aisqlgen.services.generator import QueryGenerator


@dataclass(frozen=True, slots=True)
class GenerateRequest:
    prompt: str
    schema_ddl: str | None = None


@dataclass(frozen=True, slots=True)
class GenerateResponse:
    sql: str
    intent: str


class GenerateHandler:
    def __init__(self, generator: QueryGenerator) -> None:
        self._generator = generator

    def handle(self, req: GenerateRequest) -> GenerateResponse:
        plan = classify(req.prompt)
        sql = self._generator.generate(prompt=req.prompt, schema_ddl=req.schema_ddl)
        return GenerateResponse(sql=sql, intent=plan.intent)