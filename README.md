# Trustworthy Python releases - Soup DevOps take-home

This repository is a deliberately small Python CLI and a release pipeline designed
around a simple claim: **a green source checkout is not evidence that the published
artifact works for users.**

The intentionally unsafe implementation is preserved in
[`reproductions/naive`](reproductions/naive). It is not imported or published by the
fixed package. The red/green evidence plan, exact commands, and the remaining gaps
are in [`docs/INCIDENT.md`](docs/INCIDENT.md). The concise decision note is
[`docs/RELEASE-NOTE.md`](docs/RELEASE-NOTE.md).

## What the protected release path proves

On every pull request and tag, GitHub Actions:

1. runs a stdlib lint/import guard;
2. tests Python 3.10, 3.11, and 3.12 on Ubuntu, Windows, and macOS;
3. creates a wheel and source distribution without a build-time network dependency;
4. audits the wheel contents and `RECORD` file;
5. creates a fresh virtual environment, installs only the wheel, and invokes the
   installed `soupc` console command; and
6. builds and smoke-tests the non-root Docker image on Ubuntu.

Only a signed `vX.Y.Z` tag whose version agrees with `pyproject.toml`, after all
checks succeed, reaches the isolated TestPyPI publish job. It uses PyPI Trusted
Publishing (OIDC), never a token stored as a GitHub secret.

## Local verification

Requires Python 3.10+ only; no package downloads are needed.

```powershell
$env:PYTHONPATH = "src"
python tools/lint.py
python -m unittest discover -s tests -v
python tools/build.py
python tools/audit_wheel.py dist
python tools/smoke_install.py dist
```

The release workflow needs a one-time repository setting in TestPyPI: add a Trusted
Publisher for this repository, workflow file `release.yml`, and environment
`testpypi`. Protect that environment with required reviewers while this is an
internship exercise; see the verdict for why fully unattended publication is not
recommended yet.
