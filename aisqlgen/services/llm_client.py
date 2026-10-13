"""Thin async HTTP client for OpenAI-compatible endpoints (Ollama, Azure, OpenAI).

Uses httpx.AsyncClient. One client per process; connection pooling is on.
"""
from __future__ import annotations

import os
from typing import Any

import httpx

from aisqlgen.config.models import LLMConfig
from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, config: LLMConfig) -> None:
        self._cfg = config
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "LLMClient":
        self._client = httpx.AsyncClient(
            base_url=self._cfg.base_url.rstrip("/"),
            timeout=self._cfg.timeout_s,
            headers=self._headers(),
        )
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _headers(self) -> dict[str, str]:
        key = os.environ.get(self._cfg.api_key_env, "")
        headers = {"Content-Type": "application/json"}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        return headers

    async def chat(self, messages: list[dict[str, str]]) -> str:
        if self._client is None:
            raise LLMError("LLMClient used outside of async context manager")
        payload: dict[str, Any] = {
            "model": self._cfg.model,
            "messages": messages,
            "temperature": self._cfg.temperature,
            "max_tokens": self._cfg.max_tokens,
        }
        try:
            resp = await self._client.post("/chat/completions", json=payload)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc

        body = resp.json()
        try:
            return body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"unexpected LLM response shape: {body!r}") from exc