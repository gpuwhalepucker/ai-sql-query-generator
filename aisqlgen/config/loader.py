"""Load config.yaml, merge with defaults, validate."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from aisqlgen.config.models import AppConfig
from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)

_DEFAULT_PATHS = (
    Path("config/config.yaml"),
    Path.home() / ".aisqlgen" / "config.yaml",
)


def load_config(explicit: Path | None = None) -> AppConfig:
    if explicit is not None:
        return _load_one(explicit)

    for candidate in _DEFAULT_PATHS:
        if candidate.is_file():
            return _load_one(candidate)

    log.debug("no config file found; using defaults")
    return AppConfig()


def _load_one(path: Path) -> AppConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    try:
        return AppConfig.model_validate(raw)
    except ValidationError as exc:
        raise SystemExit(f"invalid config at {path}:\n{exc}") from exc