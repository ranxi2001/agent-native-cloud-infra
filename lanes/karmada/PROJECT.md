# Karmada Project Profile

Observed at: 2026-07-21 (local refs)

## Identity

- Canonical repository: `karmada-io/karmada`
- Default branch: `master`
- Local source: `/home/karmada`
- Personal fork: `ranxi2001/karmada` as `origin`
- Canonical remote: `upstream`; its push URL is currently enabled and must be
  disabled before contribution work
- Canonical ref: `upstream/master` at `e4417e3862918be6e64daeba88ad643d549201b4`
- Learning ref: `origin/intern` at `838bc82e008155c1fbbb8192d2c986eb5dfe60b1`
- Current source worktree: clean `feature/cert-mode-rotate`, tracking
  `upstream/master`, one commit ahead and 17 behind
- Separate clean intern worktree: `/tmp/karmada-intern-worktree`, matching
  `origin/intern`

Use current `upstream/master` as the base for candidate analysis and topic worktrees. Do not use the stale local/fork `master` or the checked-out `intern` branch as a topic base; the learning ref has a long independent history.

## Architecture Surface

Karmada is a Go/Kubernetes multi-cluster control plane. Main review surfaces include API and generated clients, scheduler decisions, propagation/controllers, status reflection, failover/rescheduling, CLI/operator installation, certificates, Helm, and multi-cluster end-to-end behavior.

## Context Sources

Run `./workstation context-sync karmada`, then `./workstation context karmada`.
The generated overlay exposes `AGENTS.md`, `PROGRESS.md`, reports, and native
skills from exact `origin/intern` without switching the source worktree. If the
temporary intern worktree disappears or becomes dirty, the overlay falls back
to an exact-ref snapshot.

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
