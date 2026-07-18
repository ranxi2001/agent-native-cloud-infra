# OpenSandbox Backlog

Observed at: 2026-07-16. Re-check upstream immediately before acting.

| Priority | Candidate | Evidence | Status | Next action |
| --- | --- | --- | --- | --- |
| P0 | Select the first non-overlapping contribution | Current unassigned issue and open-PR scans completed; many apparently open issues already have active PRs | researching | Compare scope, ownership, overlap, review activity, and locally reachable validation before creating a task |
| P1 | Screen [#1265](https://github.com/opensandbox-group/OpenSandbox/issues/1265), container image provenance discoverability | Open, unassigned, no comments, and no matching open PR found on 2026-07-16; repository README/docs slice is separable from maintainer-only DockerHub account changes | screening | Verify docs ownership/build, decide whether a focused repository-only change is acceptable, and seek scope confirmation before implementation if needed |
| P2 | Screen [#1217](https://github.com/opensandbox-group/OpenSandbox/issues/1217), server Helm chart release/docs | Open, unassigned, no comments, and no matching open PR found; touches release governance and published artifacts | screening | Map release workflow ownership and avoid treating maintainer credentials as a contributor task |
| P2 | Parameterize Docker runtime smoke | Existing AgentCube smoke record uses historical fixed component versions | planned | Derive versions from the current OpenSandbox release train and keep cleanup checks explicit |
| - | [#1253](https://github.com/opensandbox-group/OpenSandbox/issues/1253), Helm docs CI | Open [PR #1259](https://github.com/opensandbox-group/OpenSandbox/pull/1259) already closes it | ruled-out | Monitor existing PR only; do not duplicate implementation |
| - | [#1262](https://github.com/opensandbox-group/OpenSandbox/issues/1262), Helm values schema | Open [PR #1263](https://github.com/opensandbox-group/OpenSandbox/pull/1263) already closes it and has collaborator approval | ruled-out | Monitor existing PR only; do not duplicate implementation |
| - | [#853](https://github.com/opensandbox-group/OpenSandbox/issues/853), ARM64 64K-page crash | Requires matching ARM64 64K-page hardware for credible validation | ruled-out | Reconsider only when that hardware is available |
