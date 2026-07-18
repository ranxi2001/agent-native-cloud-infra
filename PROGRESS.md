# Workstation Progress

Last updated: 2026-07-18

## Goal

Operate a reusable, skills-based workstation for concurrent open-source contributions across agent-native cloud infrastructure projects.

## Active Lanes

| Project | State | Current focus | Next action |
| --- | --- | --- | --- |
| Karmada | active | Canonical remote is read-only; clean worktree is on `intern`, while local/fork `master` is 12 commits behind | Base any new task on `upstream/master`, not the learning branch or stale mirror |
| AgentCube | active | Existing intern workflow remains project-native; upstream push is disabled | Route the next new contribution through a workstation task/worktree |
| OpenSandbox | active | Canonical clone, native instructions/skills, and license preflight verified | Screen a non-overlapping contribution, then decide personal-fork setup |

## Current State

- Independent workstation repository, project registry, task lanes, and isolated worktree support are implemented.
- Four generic skills cover routing, onboarding, upstream contribution management, and agent-native infrastructure review.
- Full validation covers CLI behavior, safety-critical remote checks, skill metadata/checksums, and tracked, staged, or untracked whitespace on an unborn repository.
- `review-agent-native-infra` revision 2 passed a fresh-context static forward test against OpenSandbox `main@18eaee779685`, with pinned evidence, loaded instructions, a lifecycle diagram, explicit validation gaps, and clean-state confirmation.
- Karmada instructions and native skills remain available from `origin/intern` without using that learning branch as a contribution base.
- OpenSandbox is a clean partial clone at `18eaee779685774ba97b8a5b4c3a06030a978722`; it tracks canonical `upstream/main` and the upstream push URL is disabled.
- OpenSandbox root/Kubernetes instructions, PR template, CODEOWNERS, CI baseline, and six CLI-bundled runtime skills are discoverable from the live checkout.
- `./scripts/verify-license.sh` passed on OpenSandbox without changing its worktree.
- Issues #1253 and #1262 are not viable new contributions because open PRs #1259 and #1263 already implement them.
- No OpenSandbox personal fork, global skill installation, issue claim, comment, branch push, or other upstream action has been performed.
- Karmada has canonical `upstream/master@1f07b77c35cc` with push disabled; the clean worktree is `intern@51f2c14cdbb5`, and local/fork `master` is 12 commits behind canonical.
- AgentCube canonical `upstream` push is disabled.
- `./workstation doctor` reports all registered repositories consistent and only the intentionally absent OpenSandbox personal fork as informational.

## Blockers

- OpenSandbox personal fork is not registered; this does not block read-only scouting.
- OpenSandbox candidate issues must be refreshed immediately before selection because community state changes quickly.

## Next

1. Continue the structured OpenSandbox `select-first-contribution` task, starting with issue #1265's repository-owned documentation slice.
2. Create a personal fork only after a contribution is selected and the exact external action is approved.
3. Create a dedicated OpenSandbox task/worktree from `upstream/main` for the selected contribution.

## Stop Conditions

- Stop before creating a fork, claim, issue, PR, review, comment, reviewer request, maintainer mention, or open-PR branch update without exact user approval.
- Stop before privileged/Kubernetes/cloud smoke tests if cleanup, credentials, or host impact is not controlled.
