"""Legacy-compatible sdist installer; normal releases use the audited wheel."""

from pathlib import Path
import re

from setuptools import find_packages, setup


text = Path("pyproject.toml").read_text(encoding="utf-8")
version = re.search(r'^version = "([^"]+)"$', text, re.M).group(1)

setup(
    name="soup-devops-takehome-danial-2026",
    version=version,
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["soupc=soup_cli.cli:main"]},
)
