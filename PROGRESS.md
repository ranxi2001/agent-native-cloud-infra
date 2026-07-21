# Workstation Progress

Last updated: 2026-07-21

## Goal

Operate a reusable, skills-based workstation for concurrent open-source contributions across agent-native cloud infrastructure projects.

## Active Lanes

| Project | State | Current focus | Next action |
| --- | --- | --- | --- |
| Karmada | active | Source worktree is on `feature/cert-mode-rotate`, 17 commits behind `upstream/master`; canonical push is currently enabled | Disable canonical push before new contribution work and base new tasks on refreshed `upstream/master` |
| AgentCube | active | Existing intern workflow remains project-native; upstream push is disabled | Route the next new contribution through a workstation task/worktree |
| OpenSandbox | active | Registered path `/home/opensandbox` is currently absent | Restore or re-onboard the checkout before resuming contribution selection |
| Work API | active | PR #72 is open from `ranxi2001/work-api:ci/pin-actions-pr70` at `1ab1c5ee6303`; fork CI is fully green | Complete EasyCLA authorization, then await upstream workflow approval and review |

## Current State

- Independent workstation repository, project registry, task lanes, and isolated worktree support are implemented.
- Four generic skills cover routing, onboarding, upstream contribution management, and agent-native infrastructure review.
- Full validation covers CLI behavior, safety-critical remote checks, skill metadata/checksums, and tracked, staged, or untracked whitespace on an unborn repository.
- `review-agent-native-infra` revision 2 passed a fresh-context static forward test against OpenSandbox `main@18eaee779685`, with pinned evidence, loaded instructions, a lifecycle diagram, explicit validation gaps, and clean-state confirmation.
- Karmada instructions and native skills remain available from `origin/intern` without using that learning branch as a contribution base.
- The previously verified OpenSandbox checkout is currently absent from its registered path; its cached profile remains but must not substitute for live instructions.
- OpenSandbox root/Kubernetes instructions, PR template, CODEOWNERS, CI baseline, and six CLI-bundled runtime skills are discoverable from the live checkout.
- `./scripts/verify-license.sh` passed on OpenSandbox without changing its worktree.
- Issues #1253 and #1262 are not viable new contributions because open PRs #1259 and #1263 already implement them.
- No OpenSandbox personal fork, global skill installation, issue claim, comment, branch push, or other upstream action has been performed.
- Karmada is currently on `feature/cert-mode-rotate` and 17 commits behind its tracked `upstream/master`; the canonical push URL is enabled and must be disabled before upstream work.
- AgentCube canonical `upstream` push is disabled.
- `./workstation doctor` reports pre-existing errors for missing AgentCube/Karmada task directories, Karmada's enabled canonical push URL, and the absent OpenSandbox path. Work API's fork is now registered; no `AGENTS.md` exists in that repository.

## Blockers

- OpenSandbox personal fork is not registered; this does not block read-only scouting.
- OpenSandbox candidate issues must be refreshed immediately before selection because community state changes quickly.
- Workstation-wide doctor is red on the pre-existing AgentCube, Karmada, and OpenSandbox state described above.
- Work API PR #72 is open; EasyCLA reports the commit is not yet authorized and the upstream workflow is waiting for approval.

## Next

1. Complete EasyCLA authorization for Work API PR #72, then monitor the approval-gated upstream workflow and review state.
2. Continue the structured OpenSandbox `select-first-contribution` task, starting with issue #1265's repository-owned documentation slice.
3. Create a personal OpenSandbox fork only after a contribution is selected and the exact external action is approved.

## Stop Conditions

- Stop before creating a fork, claim, issue, PR, review, comment, reviewer request, maintainer mention, or open-PR branch update without exact user approval.
- Stop before privileged/Kubernetes/cloud smoke tests if cleanup, credentials, or host impact is not controlled.
