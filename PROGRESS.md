# Workstation Progress

Last updated: 2026-07-24

## Goal

Operate a reusable, skills-based workstation for concurrent open-source contributions across agent-native cloud infrastructure projects.

## Active Lanes

| Project | State | Current focus | Next action |
| --- | --- | --- | --- |
| Karmada | active | Learning checkout `intern` has five reporting changes and is `+72/-44` against `upstream/master`; canonical push is disabled | Preserve the dirty learning checkout and base any contribution worktree on refreshed `upstream/master` |
| AgentCube | active | Existing intern workflow remains project-native; upstream push is disabled | Route the next new contribution through a workstation task/worktree |
| AI Agent Book | active | PR #339 merged; interactive multimodal tools toggle fix is ready locally at `25de486e` | Obtain exact approval before pushing the fork branch and opening the drafted PR |
| OpenSandbox | active | Checkout is restored and clean at `main@18eaee77`; canonical push is disabled and no personal fork is registered | Refresh live project context before scouting; register a fork only with explicit authority |
| Work API | active | PR #72 merged as `9710f2f9d7c6`; the registered checkout is currently absent | Restore the checkout before any new work; otherwise monitor only |

## Current State

- Independent workstation repository, project registry, task lanes, and isolated worktree support are implemented.
- Four generic skills cover routing, onboarding, upstream contribution management, and agent-native infrastructure review.
- Exact-ref context overlays are implemented for Karmada and AgentCube: both currently resolve to clean `origin/intern` worktrees, with allowlisted snapshot fallback, strict doctor checks, and a 256 KiB always-load budget.
- Cross-project outcomes are indexed once per ISO week under `summaries/weekly/`; daily and monthly rollups are intentionally omitted.
- Full validation covers CLI behavior, safety-critical remote checks, skill metadata/checksums, and tracked, staged, or untracked whitespace on an unborn repository.
- `review-agent-native-infra` revision 2 passed a fresh-context static forward test against OpenSandbox `main@18eaee779685`, with pinned evidence, loaded instructions, a lifecycle diagram, explicit validation gaps, and clean-state confirmation.
- Karmada instructions and native skills remain available from `origin/intern` without using that learning branch as a contribution base.
- The OpenSandbox checkout is restored and clean at `main@18eaee77`; live
  project context still needs refreshing before new source work.
- The Work API checkout is also absent from its registered path; PR #72 remains
  complete, but future source work requires restoring or re-onboarding it.
- OpenSandbox root/Kubernetes instructions, PR template, CODEOWNERS, CI baseline, and six CLI-bundled runtime skills remain documented in the cached profile and require live revalidation before source work.
- `./scripts/verify-license.sh` passed on OpenSandbox without changing its worktree.
- Issues #1253 and #1262 are not viable new contributions because open PRs #1259 and #1263 already implement them.
- AI Agent Book PRs #288, #322, and #323 merged into `main` as `e9d1fe79`, `1912079f`, and `2e8aed79`; no follow-up mutation is pending.
- AI Agent Book PRs #325, #326, #327, and #339 merged as `37c39dde`,
  `c83810cf`, `4e6f2125`, and `cdb4bffc`.
- AI Agent Book source is restored at its registered path with canonical push
  disabled. A current-main fix for the documented interactive `/tools on`
  failure is committed locally as `25de486e`; no fork push or PR is authorized.
- No OpenSandbox personal fork, global skill installation, issue claim, comment, branch push, or other upstream action has been performed.
- Karmada's `intern` checkout has five user reporting changes and is `+72/-44`
  against `upstream/master`; canonical push is disabled. Do not use or clean
  that checkout for a contribution branch.
- AgentCube canonical `upstream` push is disabled.
- `./workstation doctor` is red only because the registered Work API path is
  absent. It also reports unmaterialized AgentCube/Karmada context overlays and
  the missing OpenSandbox personal fork as informational conditions.

## Blockers

- OpenSandbox personal fork is not registered; this does not block read-only scouting.
- OpenSandbox candidate issues must be refreshed immediately before selection because community state changes quickly.
- Workstation-wide doctor is red on the absent Work API checkout described
  above.

## Next

1. Present the exact AI Agent Book multimodal toggle push and PR gate; perform no upstream action before approval.
2. Extend context discovery with path-scoped nested `AGENTS.md` and compact report indexes.
3. Preserve Karmada's dirty `intern` checkout and create any contribution lane from refreshed `upstream/master`.
4. Refresh live OpenSandbox context before continuing candidate selection.

## Stop Conditions

- Stop before creating a fork, claim, issue, PR, review, comment, reviewer request, maintainer mention, or open-PR branch update without exact user approval.
- Stop before privileged/Kubernetes/cloud smoke tests if cleanup, credentials, or host impact is not controlled.
