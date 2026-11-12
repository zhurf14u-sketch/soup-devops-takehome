# Known-bad 0.9.3 fixture

This directory is evidence, not a release candidate. The root `naive-ci.yml` checks only
syntax on Ubuntu/Python 3.12, so it stays green while all four user-visible defects
remain. Use the root `incident-red.yml` dispatch workflow to make each defect red
on demand. The fixed root package is the matching green run.
