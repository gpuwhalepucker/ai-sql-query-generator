"""Wire config, services, and the CLI together. Returns a process exit code."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aisqlgen.app.session import Session
from aisqlgen.config.loader import load_config
from aisqlgen.services.generator import QueryGenerator
from aisqlgen.services.llm_client import LLMClient
from aisqlgen.utils.logging import get_logger

log = get_logger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="aisqlgen",
        description="Turn natural-language prompts into dialect-aware SQL.",
    )
    p.add_argument("-p", "--prompt", help="natural-language prompt to translate")
    p.add_argument("-d", "--dialect", default=None, help="target SQL dialect (postgres, mysql, sqlite, mssql)")
    p.add_argument("-s", "--schema", type=Path, default=None, help="path to a .sql schema dump for grounding")
    p.add_argument("--config", type=Path, default=None, help="path to config.yaml")
    p.add_argument("--allow-write", action="store_true", help="permit non-read-only statements (off by default)")
    p.add_argument("--repl", action="store_true", help="start an interactive session")
    return p


def bootstrap(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)
    cfg = load_config(args.config)

    if args.dialect:
        cfg = cfg.with_dialect(args.dialect)

    llm = LLMClient(cfg.llm)
    generator = QueryGenerator(cfg=cfg, llm=llm)

    session = Session(generator=generator, config=cfg, allow_write=args.allow_write)

    if args.schema:
        session.load_schema(args.schema)

    if args.repl or not args.prompt:
        session.run_repl()
        return 0

    sql = session.generate(args.prompt)
    sys.stdout.write(sql + "\n")
    return 0