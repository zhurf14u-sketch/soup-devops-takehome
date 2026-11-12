"""Produce a deterministic, minimal wheel and sdist with only the standard library."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import pathlib
import re
import tarfile
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PROJECT = "soup_release_demo"


def version() -> str:
    match = re.search(r'^version = "([^"]+)"$', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.M)
    if not match:
        raise RuntimeError("version not found in pyproject.toml")
    return match.group(1)


def record_hash(data: bytes) -> str:
    encoded = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
    return "sha256=" + encoded


def metadata(release: str) -> bytes:
    return ("Metadata-Version: 2.1\nName: soup-release-demo\nVersion: " + release + "\n"
            "Summary: Small CLI used to demonstrate a trustworthy Python release pipeline\n"
            "Requires-Python: >=3.10\nLicense: MIT\n").encode()


def wheel(release: str) -> pathlib.Path:
    DIST.mkdir(exist_ok=True)
    filename = f"{PROJECT}-{release}-py3-none-any.whl"
    target = DIST / filename
    contents: dict[str, bytes] = {}
    for source in sorted((ROOT / "src" / "soup_cli").glob("*.py")):
        contents[f"soup_cli/{source.name}"] = source.read_bytes()
    info = f"{PROJECT}-{release}.dist-info"
    contents[f"{info}/METADATA"] = metadata(release)
    contents[f"{info}/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: soup-release-demo\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    contents[f"{info}/entry_points.txt"] = b"[console_scripts]\nsoupc = soup_cli.cli:main\n"
    record_rows = [[name, record_hash(data), str(len(data))] for name, data in sorted(contents.items())]
    record_rows.append([f"{info}/RECORD", "", ""])
    buffer = io.StringIO(newline="")
    csv.writer(buffer, lineterminator="\n").writerows(record_rows)
    contents[f"{info}/RECORD"] = buffer.getvalue().encode()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(contents.items()):
            archive.writestr(name, data)
    return target


def sdist(release: str) -> pathlib.Path:
    target = DIST / f"soup-release-demo-{release}.tar.gz"
    with tarfile.open(target, "w:gz") as archive:
        for name in ["pyproject.toml", "README.md", "LICENSE"]:
            archive.add(ROOT / name, arcname=f"soup-release-demo-{release}/{name}")
        for source in sorted((ROOT / "src" / "soup_cli").glob("*.py")):
            archive.add(source, arcname=f"soup-release-demo-{release}/src/soup_cli/{source.name}")
    return target


if __name__ == "__main__":
    release = version()
    print(wheel(release))
    print(sdist(release))
