# Upstream Draft

Target: `kubernetes-sigs/work-api:master`

Classification: upstream-facing replacement contribution for PR #70

Completed with explicit approval on 2026-07-21:

1. Created the public fork `ranxi2001/work-api`.
2. Pushed local branch `ci/pin-actions-pr70`, then updated it with the user's
   explicit approval to final signed commit
   `1ab1c5ee6303aa06766073076d89612fa989b662`. The remote branch was verified
   at the same SHA.

3. With explicit user approval, opened
   `https://github.com/kubernetes-sigs/work-api/pull/72` against
   `kubernetes-sigs/work-api:master` with the exact title and body below.

## Title

ci: upgrade and pin GitHub Actions

## Body

#### What type of PR is this?

/kind cleanup

#### What this PR does / why we need it:

The Kubernetes GitHub Actions policy requires actions to be pinned to full
40-character commit SHAs. The current tag-based references, including the
changes proposed by #70 and #71, are rejected before the workflow steps can
run.

This PR upgrades every action in the CI workflow to its latest stable release
and pins the exact release commit, while retaining `# vX.Y.Z` comments for
Dependabot and reviewers:

- actions/checkout v7.0.1
- actions/setup-go v7.0.0
- golangci/golangci-lint-action v9.3.0
- helm/kind-action v1.14.0

`engineerd/setup-kind` is replaced rather than pinned in place because its
`v0.6.2` tag and same-named branch point to different commits. The tag commit
does not contain the action's built `dist/main/index.js`; pinning that official
tag commit by SHA was tested in [fork CI run 29794417222] and failed before
kind cluster creation. The branch commit contains the built files, but pinning
a different, non-tag commit behind the same version name would leave the action
provenance ambiguous. `helm/kind-action` provides a maintained, release-tagged
replacement with its built action entry points committed.

The replacement action cannot install the previous kind v0.11.1 release
because that legacy release uses a checksum asset format it cannot validate,
as shown by [fork CI run 29795085094]. Kind is therefore upgraded to v0.32.0.
Since kind v0.32.0 defaults to Kubernetes v1.36.1, the workflow explicitly
pins the official Kubernetes v1.35.5 node image digest and kubectl v1.35.0 to
stay aligned with this repository's Kubernetes v0.35.x dependencies.

Setup-go cache dependency paths are also explicit for both the root and
GOPATH-style checkout locations, avoiding cache warnings and ensuring the
module cache is used.

#### Which issue(s) this PR fixes:

None.

#### Special notes for your reviewer:

This supersedes the dependency changes in #70 and #71. The action SHAs were
resolved from exact release tags, including the commit beneath
golangci-lint-action's annotated tag. This follows the same
`uses: owner/action@<full-sha> # vX.Y.Z` convention used by Karmada.

Validation:

- `actionlint v1.7.12`
- full-SHA scan of all 10 `uses:` references
- `./hack/verify-all.sh -v`
- [fork CI run 29795409249]: lint, verify, unit test, image build, kind setup,
  image load, and e2e all passed at commit
  `1ab1c5ee6303aa06766073076d89612fa989b662`

#### Does this PR introduce a user-facing change?

```release-note
NONE
```

[fork CI run 29794417222]: https://github.com/ranxi2001/work-api/actions/runs/29794417222
[fork CI run 29795085094]: https://github.com/ranxi2001/work-api/actions/runs/29795085094
[fork CI run 29795409249]: https://github.com/ranxi2001/work-api/actions/runs/29795409249

## Diff And Validation

- `.github/workflows/ci.yml`: one file changed, with 19 insertions and 11
  deletions. All 10 action references are upgraded or pinned; setup-kind moves
  to helm/kind-action v1.14.0 with kind v0.32.0 and Kubernetes v1.35.5.
- `actionlint v1.7.12`: passed.
- Full-SHA scan: passed for 10 of 10 action references.
- `./hack/verify-all.sh -v`: passed with a temporary host-only Python shim.
- `git diff --check`: passed.
- Fork CI run `29795409249` passed lint, verify, unit, image build, kind setup,
  image load, and e2e at the exact proposed commit.

## Residual Risk

- PRs #70 and #71 overlap this combined contribution and will need maintainers
  to close or supersede them if it lands.
- The e2e cluster moves from the legacy kind default to Kubernetes v1.35.5;
  this matches the repository's Kubernetes v0.35.x Go dependencies but is a
  broader test-environment update than SHA pinning alone.

The PR is open. Comments, reviewer requests, branch updates, and other
follow-up mutations remain separately gated.
