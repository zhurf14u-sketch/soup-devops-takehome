"""Fail if the release artifact is malformed or lacks what an end user needs."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import pathlib
import sys
import zipfile


def digest(data: bytes) -> str:
    return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")


def main(directory: str) -> int:
    wheels = list(pathlib.Path(directory).glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one wheel, found {len(wheels)}")
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
        required = {"soup_cli/__init__.py", "soup_cli/cli.py"}
        if missing := required - names:
            raise SystemExit("wheel misses runtime files: " + ", ".join(sorted(missing)))
        record = next((name for name in names if name.endswith(".dist-info/RECORD")), None)
        entry_points = next((name for name in names if name.endswith(".dist-info/entry_points.txt")), None)
        if not record or not entry_points or b"soupc = soup_cli.cli:main" not in archive.read(entry_points):
            raise SystemExit("wheel misses console-script metadata")
        for row in csv.reader(io.StringIO(archive.read(record).decode())):
            if row[0] == record:
                continue
            if row[0] not in names or row[1] != digest(archive.read(row[0])):
                raise SystemExit("wheel RECORD integrity check failed: " + row[0])
    print("wheel audit: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
