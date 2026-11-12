# Release verdict

**Verdict: do not enable completely unattended real-PyPI publication yet.** The
pipeline can safely publish a tested artifact to TestPyPI after the one-time Trusted
Publisher setup, but production release automation needs independent human review
until branch protection, CODEOWNERS for workflow/release files, a production PyPI
Trusted Publisher, a rehearsed yank/supersede runbook, and at least one proven
red-to-green evidence cycle are in place. Immutable package versions make a mistaken
upload a public support and security event rather than a reversible deploy.

Fix first: replace `REPLACE_WITH_GITHUB_OWNER` with the real owner, configure the
TestPyPI Trusted Publisher and protected environment, push the repository, and save
the four expected-red plus one fixed-green Actions URLs. Then enable TestPyPI only.
After a reviewed test release and incident drill, an organization may choose to
remove the environment approval for low-risk production releases - that is a policy
decision, not a conclusion drawn from a green CI badge.

One thing that surprised me: the most valuable test here is not the source test but
installing the actual wheel in an empty environment and calling its generated entry
point. What still concerns me is the trust boundary after CI: a correct artifact can
still be published under the wrong policy, from a compromised maintainer account, or
into an ecosystem with a compromised future dependency.

## AI-use disclosure

I used an AI coding assistant to scaffold the repository layout, write the first
draft of the standard-library build/audit scripts and workflow YAML, and challenge
the threat model. I accepted the separation between source, artifact, and publish
jobs; I manually reviewed every workflow permission/condition, each intentional
failure, wheel metadata/`RECORD` logic, platform assumptions, and the verdict. I
would re-run the commands and inspect every GitHub Actions result in the target
account before representing the evidence as completed.
