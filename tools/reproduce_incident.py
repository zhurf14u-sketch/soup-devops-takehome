"""Intentionally fail one check against reproductions/naive for recorded red evidence."""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
NAIVE = ROOT / "reproductions" / "naive"


def fail(message: str) -> None:
    raise SystemExit("EXPECTED RED: " + message)


def main(name: str) -> None:
    source = (NAIVE / "src" / "soup_cli" / "cli.py").read_text(encoding="utf-8")
    if name == "py310-import" and "tomllib" in source:
        fail("tomllib is imported but Python 3.10 does not provide it")
    if name == "windows-startup" and "os.fork" in source:
        fail("os.fork is unavailable on Windows")
    if name == "missing-wheel-data" and not (NAIVE / "src" / "soup_cli" / "defaults.json").exists():
        fail("the runtime defaults file is absent from the artifact source")
    if name == "tag-version":
        declared = "0.9.2"
        tag = "0.9.3"
        if declared != tag:
            fail(f"tag {tag} does not equal package version {declared}")
    raise SystemExit("reproduction did not fail; the fixture was altered")


if __name__ == "__main__":
    main(sys.argv[1])
