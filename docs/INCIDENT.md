# Incident reproduction and proof plan

## The four defects that a green naive CI misses

| ID | Deliberate defect in `reproductions/naive` | Why naive CI is green | User symptom | Red evidence | Fixed green evidence |
|---|---|---|---|---|---|
| B1 | `from tomllib import loads` while metadata says `>=3.10` | `compileall` on Python 3.12 does not execute the import | `ImportError` on Python 3.10 | Dispatch `incident-red.yml`, `py310-import` | `release.yml` matrix tests 3.10 |
| B2 | `os.fork()` in CLI startup | Ubuntu-only syntax checking never invokes the command | CLI cannot start on Windows | Dispatch `windows-startup` | Windows matrix plus installed-wheel smoke |
| B3 | runtime `defaults.json` exists in source but is excluded from the wheel | no wheel is made or installed | package imports, then fails at runtime for every installed user | Dispatch `missing-wheel-data` | wheel contents, `RECORD`, and clean-venv command are audited |
| B4 | package is `0.9.2` but the hypothetical tag is `v0.9.3` | CI never reads tags or artifact metadata | immutable index receives a misleading release | Dispatch `tag-version` | tag job rejects unequal values before build/publish |

The deliberately red workflow exits non-zero by design. It is separate from the
protected green workflow so ordinary contributors are not trained to ignore failing
checks. When this is pushed to GitHub, record each run URL in the table below; the
repository is intentionally not presented as having evidence that has not run.

| Evidence | GitHub Actions URL |
|---|---|
| B1 expected-red | Run after repository push |
| B2 expected-red | Run after repository push |
| B3 expected-red | Run after repository push |
| B4 expected-red | Run after repository push |
| fixed 0.9.4 green | Run after repository push |

## Why the fixed pipeline is materially stronger

The release path has separate source-test, artifact, container, verification, and publisher jobs.
The verification job consumes only the artifact uploaded by this exact commit and
retests the downloaded wheel. The publisher has no checkout, shell, or stored package
credential; it receives only that verified artifact. Its OIDC
identity is restricted by TestPyPI to this repository, `release.yml`, and the
`testpypi` environment. A fork pull request receives only read permissions and never
meets the publish condition.

The checks are still not a proof of every property: they do not test Linux
distributions outside the runner image, alternate CPU architectures, a broken PyPI
mirror, user configuration, malicious maintainer changes, or a dependency added
after this take-home. They also cannot reverse an already published immutable
version. The mitigation is a fast superseding patch, yanking the bad release where
appropriate, clear advisory notes, and revoking/rotating any affected credential.

## Silent supply-chain failures closed

1. **Swapped or compromised CI action:** every action invocation is pinned to an
   immutable commit SHA; Dependabot opens the reviewable update rather than silently
   changing a tag.
2. **Secret from a fork PR:** the default workflow token is read-only, no `pull_request_target`
   event exists, and publishing uses short-lived OIDC rather than a repository secret.
3. **Stale or substituted artifact:** the artifact name includes `github.sha`; publish downloads
   that exact artifact, re-audits it, and smoke-installs it before transfer.
4. **Tag/version mismatch:** the tag gate compares `vX.Y.Z` to `pyproject.toml` before upload.
5. **Cache masking resolver issues:** this project has no dependency cache or runtime third-party
   dependencies. Any future dependency must be exact-pinned, hash-locked, tested from an empty
   environment, and receive a dependency-review/SBOM check before cache is enabled.

## GPU CI design and monthly cost

I would rent ephemeral, single-tenant NVIDIA L4 (or equivalent 24 GB) runners from
a provider integrated with GitHub Actions, with a disposable image and a provider
budget cap. The release tag runs the 10-minute acceptance test once; a nightly run
uses the same cap and stops at 30 minutes. Fork PRs never get GPU capacity. The
workflow labels (`self-hosted`, `gpu`, `ephemeral`) make this an explicit deployment
contract, not an accidental ordinary runner.

Illustrative conservative model: 1 L4 runner at $0.80/hour, 10 minutes per release,
20 releases/month, plus 30 minutes for each of 30 nightlies. That is
`(20 * 10 / 60 + 30 * 30 / 60) * $0.80 = $14.67/month`; add a 30% retry/boot reserve
for **$19.07/month**. I would set a $25/month provider budget alert. Exact price must
be replaced by the chosen vendor's current quote before approval. `timeout-minutes`,
concurrency cancellation, a small data fixture, GPU-shape assertion, and automatic
ephemeral teardown prevent failed runs and stuck machines from spending the budget.
