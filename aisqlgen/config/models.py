"""Pydantic config models. Everything the app reads is validated here."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Dialect = Literal["postgres", "mysql", "sqlite", "mssql"]


class LLMConfig(BaseModel):
    provider: Literal["openai", "ollama", "azure", "openai_compat"] = "ollama"
    model: str = "qwen2.5-coder:7b"
    base_url: str = "http://127.0.0.1:11434/v1"
    api_key_env: str = "AISQLGEN_API_KEY"
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=64, le=8192)
    timeout_s: float = Field(default=60.0, gt=0)


class GuardConfig(BaseModel):
    allow_write: bool = False
    max_statements: int = 1
    deny_keywords: list[str] = Field(
        default_factory=lambda: ["attach", "detach", "pragma", "copy", "load_file", "xp_cmdshell"]
    )


class AppConfig(BaseModel):
    dialect: Dialect = "postgres"
    llm: LLMConfig = Field(default_factory=LLMConfig)
    guard: GuardConfig = Field(default_factory=GuardConfig)
    schema_char_budget: int = Field(default=32_000, ge=2_000, le=200_000)

    def with_dialect(self, dialect: str) -> "AppConfig":
        return self.model_copy(update={"dialect": dialect})  # type: ignore[arg-type]