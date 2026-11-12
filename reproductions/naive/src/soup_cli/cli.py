"""Intentionally broken: do not copy into production."""

import importlib.resources
import os
from tomllib import loads  # Python 3.11+, but metadata claims >=3.10.


def main() -> int:
    os.fork()  # AttributeError on Windows.
    defaults = importlib.resources.files("soup_cli").joinpath("defaults.json").read_text()
    print(loads(defaults))  # defaults.json was omitted from the release artifact.
    return 0
