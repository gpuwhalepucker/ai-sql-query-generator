"""Entry point for `aisqlgen`. Boots the desktop app or the CLI."""
from __future__ import annotations

import sys

from aisqlgen.app.bootstrap import bootstrap
from aisqlgen.utils.logging import configure_logging


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    configure_logging(level="INFO")
    return bootstrap(argv)


if __name__ == "__main__":
    raise SystemExit(main())