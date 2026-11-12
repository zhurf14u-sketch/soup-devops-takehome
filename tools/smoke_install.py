"""Install the built wheel into an empty venv and test its installed entry point."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile


def main(directory: str) -> int:
    wheel = next(pathlib.Path(directory).glob("*.whl"), None)
    if wheel is None:
        raise SystemExit("no wheel to smoke test")
    with tempfile.TemporaryDirectory() as temporary:
        venv = pathlib.Path(temporary) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        scripts = venv / ("Scripts" if sys.platform == "win32" else "bin")
        python = scripts / ("python.exe" if sys.platform == "win32" else "python")
        command = scripts / ("soupc.exe" if sys.platform == "win32" else "soupc")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", str(wheel)], check=True)
        subprocess.run([str(command), "--json"], check=True)
    print("clean-install smoke test: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
