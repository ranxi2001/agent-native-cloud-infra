# Upgrade And Pin GitHub Actions

## Problem

PR #70 changes four `actions/checkout` references from `@v6` to `@v7`, and PR
#71 independently changes four `actions/setup-go` references from `@v6` to
`@v7`.
GitHub rejects every job during setup because the Kubernetes organization now
requires all action references to be pinned to full 40-character commit SHAs.
The same workflow also contains tag references for setup-go, golangci-lint, and
setup-kind, so changing checkout alone cannot make the workflow schedulable.

## Scope

- Update every `uses:` reference in `.github/workflows/ci.yml` to a verified
  full commit SHA.
- Preserve a human-readable release comment after each SHA, following Karmada's
  convention.
- Upgrade every action reference to its latest stable release observed on
  2026-07-21: checkout v7.0.1, setup-go v7.0.0, golangci-lint-action v9.3.0,
  and helm/kind-action v1.14.0.
- Replace `engineerd/setup-kind` because the v0.6.2 tag commit does not contain
  the action's `dist/main/index.js`; the first fork CI proved that exact-SHA
  execution fails before cluster creation.
- Upgrade kind from v0.11.1 to the latest v0.32.0 because the maintained Helm
  action cannot validate the legacy release's checksum format. Pin the official
  Kubernetes v1.35.5 node image digest to match this repository's v0.35.x
  client dependencies, while preserving the `kind` cluster name and
  300-second readiness wait.
- Configure setup-go cache dependency paths explicitly for both root and
  GOPATH-style checkout locations.
- Produce one contribution that supersedes both PR #70 and PR #71.

## Non-Goals

- No controller, API, dependency, generated-code, or test behavior changes.
- No CI job, runner, permission, trigger, or tool-version redesign.
- No Go toolchain or golangci-lint binary upgrade.
- Do not move the e2e cluster beyond the repository's Kubernetes v1.35
  dependency minor even though kind v0.32.0 defaults to Kubernetes v1.36.1.
- No upstream push, PR replacement, comment, or closure without approval.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `.github/workflows/ci.yml` | Upgrade and pin every action; replace the non-runnable setup-kind tag commit | A wrong SHA or mismatched replacement input could prevent job setup or cluster creation | Resolve exact release tags, parse with actionlint, scan all `uses:` refs, run repository verification, then require full fork CI including e2e |

## Plan

1. Replace all action references with latest release commit SHAs and version
   comments; preserve setup-kind behavior through helm/kind-action inputs.
2. Validate YAML structure and immutable reference format.
3. Run repository verification that is feasible without Docker/kind state.
4. Inspect the focused diff, commit locally, and prepare exact upstream text.

## Decision Log

- Following user review, the contribution now intentionally combines PR #70
  and PR #71 instead of preserving separate major-upgrade lanes.
- `actions/checkout` is upgraded to the latest v7.0.1 release
  (`3d3c42e...`).
- `actions/setup-go` is upgraded to the latest v7.0.0 release
  (`b7ad1da...`), matching current Karmada practice.
- `golangci/golangci-lint-action` pins the commit beneath the annotated v9.3.0
  tag (`ba0d7d2...`), not the annotated tag object's SHA.
- `engineerd/setup-kind@v0.6.2` ambiguously resolves a release branch containing
  built assets while its same-named tag points to `71e45b9...`, which lacks
  those assets and failed under full-SHA execution. Replace it with the latest
  maintained `helm/kind-action` v1.14.0 (`ef37e7f...`), already used by other
  kubernetes-sigs projects under full-SHA pinning.
- Fork CI proved helm/kind-action cannot install kind v0.11.1 because its old
  checksum format is incompatible. Upgrade to the latest kind v0.32.0 and use
  the release-published Kubernetes v1.35.5 image digest, matching Work API's
  Kubernetes v0.35.x dependencies rather than kind's v1.36.1 default.
- setup-go v7 reports cache warnings for checkout steps that place the module
  under `go/src/sigs.k8s.io/work-api`; set the dependency path explicitly so
  caching is effective and warning-free.
- The local branch starts from `upstream/master`. This produces a coherent
  replacement contribution because the authenticated account cannot write to
  Dependabot's upstream PR branch.
