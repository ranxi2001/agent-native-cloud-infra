# Workstation Progress

Last updated: 2026-07-24

## Goal

Operate a reusable, skills-based workstation for concurrent open-source contributions across agent-native cloud infrastructure projects.

## Active Lanes

| Project | State | Current focus | Next action |
| --- | --- | --- | --- |
| Karmada | active | Dedicated `intern` worktree is dirty and `+54/-81` against `upstream/master`; canonical push is disabled | Preserve the dirty learning worktree and base any contribution worktree on refreshed `upstream/master` |
| AgentCube | active | Existing intern workflow remains project-native; upstream push is disabled | Route the next new contribution through a workstation task/worktree |
| AI Agent Book | active | Source checkout is absent; PR #377 remains open at `25de486e` with initial checks green | Wait for maintainer review; restore source before any branch work and require a new gate before updates or replies |
| OpenSandbox | active | Source checkout is absent; cached profile remains available and no personal fork is registered | Restore and refresh live context before scouting; register a fork only with explicit authority |
| Work API | active | PR #72 merged as `9710f2f9d7c6`; checkout is restored and clean at `master@7263f56` | Monitor only unless new work is selected |

## Current State

- Independent workstation repository, project registry, task lanes, and isolated worktree support are implemented.
- Four generic skills cover routing, onboarding, upstream contribution management, and agent-native infrastructure review.
- Exact-ref context overlays are implemented for Karmada and AgentCube with clean-worktree preference, allowlisted snapshot fallback, strict doctor checks, and a 256 KiB always-load budget; both generated overlays currently need refreshing.
- Cross-project outcomes are indexed once per ISO week under `summaries/weekly/`; daily and monthly rollups are intentionally omitted.
- Workstation-owned technical reports are independently indexed under `report/`;
  they may reference registered projects but do not become project registrations
  or contribution lanes.
- `humanizer-cs` v0.2.0 is formally released at
  `https://github.com/ranxi2001/humanizer-cs/releases/tag/v0.2.0`; `main` and the
  peeled tag point to `6b02919`. The release includes 687 de-identified records
  from 88 pre-2026 public threads, corpus validation, two behavior fixtures, and
  two passing fresh-context manual forward tests. Its Python 3.11/3.12 CI passed.
  The repository remains outside project registration until owner-maintained
  repository semantics are designed explicitly.
- Full validation covers CLI behavior, safety-critical remote checks, skill metadata/checksums, and tracked, staged, or untracked whitespace on an unborn repository.
- `review-agent-native-infra` revision 2 passed a fresh-context static forward test against OpenSandbox `main@18eaee779685`, with pinned evidence, loaded instructions, a lifecycle diagram, explicit validation gaps, and clean-state confirmation.
- Karmada instructions and native skills remain available from `origin/intern` without using that learning branch as a contribution base.
- The OpenSandbox checkout is absent; its cached profile must be revalidated
  against live source before new work.
- The Work API checkout is restored and clean at `master@7263f56`; PR #72
  remains complete.
- OpenSandbox root/Kubernetes instructions, PR template, CODEOWNERS, CI baseline, and six CLI-bundled runtime skills remain documented in the cached profile and require live revalidation before source work.
- `./scripts/verify-license.sh` passed on OpenSandbox without changing its worktree.
- Issues #1253 and #1262 are not viable new contributions because open PRs #1259 and #1263 already implement them.
- AI Agent Book PRs #288, #322, and #323 merged into `main` as `e9d1fe79`, `1912079f`, and `2e8aed79`; no follow-up mutation is pending.
- AI Agent Book PRs #325, #326, #327, and #339 merged as `37c39dde`,
  `c83810cf`, `4e6f2125`, and `cdb4bffc`.
- AI Agent Book source is absent from its registered path. PR #377 fixes the
  documented interactive `/tools on` failure from approved head `25de486e`; its
  last observed state was clean and mergeable with initial checks green.
- No OpenSandbox personal fork, global skill installation, issue claim, comment, branch push, or other upstream action has been performed.
- Karmada's dedicated `intern` worktree has nine user-owned changed paths and is
  `+54/-81` against `upstream/master`; canonical push is disabled. Do not use or
  clean that worktree for a contribution branch.
- AgentCube canonical `upstream` push is disabled.
- `./workstation doctor` is red because the AI Agent Book and OpenSandbox source
  paths are absent. It also reports stale AgentCube/Karmada context overlays;
  Karmada canonical push is disabled.

## Blockers

- OpenSandbox personal fork is not registered; this does not block read-only scouting.
- OpenSandbox candidate issues must be refreshed immediately before selection because community state changes quickly.
- Workstation-wide doctor is red on the absent AI Agent Book and OpenSandbox
  checkouts described above.
- `humanizer-cs` still lacks an automated model evaluation runner; marketplace
  submission and announcement remain unauthorized.

## Next

1. Design an automated model evaluation runner for `humanizer-cs`; require a new gate before marketplace submission or announcement.
2. Monitor AI Agent Book PR #377 for maintainer review; perform no branch update, reply, or reviewer request without a new exact gate.
3. Extend context discovery with path-scoped nested `AGENTS.md`.
4. Preserve Karmada's dirty `intern` checkout and create any contribution lane from refreshed `upstream/master`.
5. Refresh live OpenSandbox context before continuing candidate selection.

## Stop Conditions

- Stop before creating a fork, claim, issue, PR, review, comment, reviewer request, maintainer mention, or open-PR branch update without exact user approval.
- Stop before privileged/Kubernetes/cloud smoke tests if cleanup, credentials, or host impact is not controlled.
