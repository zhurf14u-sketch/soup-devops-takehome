"""CLI entry point. Keep imports and behavior portable across supported Pythons."""

from __future__ import annotations

import argparse
import json
import platform
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="soupc", description="Print release-demo diagnostics")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = {"package": "soup-devops-takehome-danial-2026", "python": platform.python_version(), "version": __version__}
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print("soup-devops-takehome-danial-2026 " + __version__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
