# Kubernetes SIGs Work API

Status: `active`

## Sources

- Canonical repository: `https://github.com/kubernetes-sigs/work-api.git`
- Default branch: `master`
- Default-branch ref: `9710f2f9d7c6359c76d501104df86e1278942772`
- Observed at: `2026-07-21`
- License: Apache License 2.0 (`LICENSE`)
- Local source: `/home/work-api`
- Canonical remote: `upstream`, with push URL `DISABLED`
- Personal fork: `https://github.com/ranxi2001/work-api.git` (`origin`)

## Architecture

- The repository defines the SIG Multicluster Work API and a controller that
  delivers resources described by `Work` objects from a hub to a spoke cluster.
- API types and generated artifacts live under `pkg/apis` and `config`; the
  controller entry point is `cmd/workcontroller/workcontroller.go`.
- Unit tests use controller-runtime envtest; end-to-end tests require Docker,
  kind, kubectl, and temporary hub/spoke cluster state.

## Contribution Contract

- No `AGENTS.md` or repository-native agent skill was present at the observed
  ref. Root `CONTRIBUTING.md` and the Kubernetes contributor guide govern work.
- Kubernetes CLA compliance is required. Root `OWNERS` lists approvers and SIG
  Multicluster ownership. No repository-local pull request template was found.
- Security reports follow `SECURITY.md` and the Kubernetes private disclosure
  process; do not file public issues for vulnerabilities.
- CI is defined in `.github/workflows/ci.yml` with lint, verify, unit, and kind
  end-to-end jobs. Current organization policy requires every action reference
  to use a full 40-character commit SHA.
- Build: `make controller`. Unit/envtest: `make test`. Verification:
  `make verify`. Generation: `make generate` and `make manifests`.
- Make targets may generate, format, download tools, create binaries, or build
  clusters/images. Check worktree state before and after running them.
