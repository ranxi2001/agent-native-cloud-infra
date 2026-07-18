# Karmada Project Profile

Observed at: 2026-07-18 (local refs)

## Identity

- Canonical repository: `karmada-io/karmada`
- Default branch: `master`
- Local source: `/home/ranxi/projects/karmada`
- Personal fork: `ranxi2001/karmada` as `origin`
- Canonical remote: `upstream`, push URL `DISABLED`
- Canonical ref: `upstream/master` at `1f07b77c35ccac02501a4d0cd4f0bb525d26b887`
- Learning ref: `origin/intern` at `51f2c14cdbb5a28b40627c6e2db2067b674e3e2d`
- Current source worktree: clean `intern`, tracking `origin/intern`
- Local and fork `master`: 12 commits behind `upstream/master`

Use current `upstream/master` as the base for candidate analysis and topic worktrees. Do not use the stale local/fork `master` or the checked-out `intern` branch as a topic base; the learning ref has a long independent history.

## Architecture Surface

Karmada is a Go/Kubernetes multi-cluster control plane. Main review surfaces include API and generated clients, scheduler decisions, propagation/controllers, status reflection, failover/rescheduling, CLI/operator installation, certificates, Helm, and multi-cluster end-to-end behavior.

## Context Sources

Run `./workstation context karmada`. The current `master` worktree contains upstream `CONTRIBUTING.md` and the PR template. Workstation-specific `AGENTS.md` and native skills are discovered from `origin/intern` with `git show`, so loading them does not require a branch switch.

Source precedence for new work:

1. Current code, Go/module/tool version files, and CI.
2. Current upstream contribution guides and templates.
3. Karmada-specific instructions and skills from the learning ref.
4. This cached profile.

## Commands

- Build: `make all`
- Unit/race coverage: `make test`
- Repository verification: `make verify`
- Generated artifacts: `make update`
- Local environment: `hack/local-up-karmada.sh`

Choose focused component targets before the full build. API changes normally require generated artifacts. Installation, propagation, failover, scheduling, operator, and CLI system behavior may require e2e evidence.

## Contribution Contract

- Create one focused topic branch/worktree from current canonical upstream `master`.
- Keep learning reports and workstation state out of upstream diffs.
- Use DCO signoff and the official PR template as required by current project instructions.
- Prefer fork push CI where available; do not create disposable self-PRs.
- Obtain exact-action approval before any community-facing mutation.
