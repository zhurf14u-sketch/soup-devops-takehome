"""Dependency-free policy checks that run identically on all CI runners."""

from __future__ import annotations

import ast
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN = {"os.fork", "tomllib"}


def dotted_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def main() -> int:
    failures: list[str] = []
    for path in (ROOT / "src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = {alias.name for alias in node.names}
                if "tomllib" in names:
                    failures.append(f"{path}: tomllib is unavailable on Python 3.10")
            if isinstance(node, ast.ImportFrom) and node.module == "tomllib":
                failures.append(f"{path}: tomllib is unavailable on Python 3.10")
            if isinstance(node, ast.Call) and dotted_name(node.func) in FORBIDDEN:
                failures.append(f"{path}: {dotted_name(node.func)} is not portable")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("lint policy: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
