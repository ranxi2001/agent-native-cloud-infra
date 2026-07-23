# Workstation Progress

Last updated: 2026-07-23

## Goal

Operate a reusable, skills-based workstation for concurrent open-source contributions across agent-native cloud infrastructure projects.

## Active Lanes

| Project | State | Current focus | Next action |
| --- | --- | --- | --- |
| Karmada | active | Source worktree is on `feature/cert-mode-rotate`, 17 commits behind `upstream/master`; canonical push is currently enabled | Disable canonical push before new contribution work and base new tasks on refreshed `upstream/master` |
| AgentCube | active | Existing intern workflow remains project-native; upstream push is disabled | Route the next new contribution through a workstation task/worktree |
| AI Agent Book | active | PRs #288/#322/#323/#325/#326/#327 merged; PR #339 is open, clean, mergeable, and green | Wait for maintainer review of #339; do not update it without a new gate |
| OpenSandbox | active | Registered path `/Users/onefly/Desktop/project/opensandbox` is currently absent | Restore or re-onboard the checkout before resuming contribution selection |
| Work API | active | PR #72 merged as `9710f2f9d7c6`; the registered checkout is currently absent | Restore the checkout before any new work; otherwise monitor only |

## Current State

- Independent workstation repository, project registry, task lanes, and isolated worktree support are implemented.
- Four generic skills cover routing, onboarding, upstream contribution management, and agent-native infrastructure review.
- Exact-ref context overlays are implemented for Karmada and AgentCube: both currently resolve to clean `origin/intern` worktrees, with allowlisted snapshot fallback, strict doctor checks, and a 256 KiB always-load budget.
- Cross-project outcomes are indexed once per ISO week under `summaries/weekly/`; daily and monthly rollups are intentionally omitted.
- Full validation covers CLI behavior, safety-critical remote checks, skill metadata/checksums, and tracked, staged, or untracked whitespace on an unborn repository.
- `review-agent-native-infra` revision 2 passed a fresh-context static forward test against OpenSandbox `main@18eaee779685`, with pinned evidence, loaded instructions, a lifecycle diagram, explicit validation gaps, and clean-state confirmation.
- Karmada instructions and native skills remain available from `origin/intern` without using that learning branch as a contribution base.
- The previously verified OpenSandbox checkout is currently absent from its registered path; its cached profile remains but must not substitute for live instructions.
- The Work API checkout is also absent from its registered path; PR #72 remains
  complete, but future source work requires restoring or re-onboarding it.
- OpenSandbox root/Kubernetes instructions, PR template, CODEOWNERS, CI baseline, and six CLI-bundled runtime skills remain documented in the cached profile but require live revalidation after the checkout is restored.
- `./scripts/verify-license.sh` passed on OpenSandbox without changing its worktree.
- Issues #1253 and #1262 are not viable new contributions because open PRs #1259 and #1263 already implement them.
- AI Agent Book PRs #288, #322, and #323 merged into `main` as `e9d1fe79`, `1912079f`, and `2e8aed79`; no follow-up mutation is pending.
- AI Agent Book PRs #325, #326, and #327 merged as `37c39dde`, `c83810cf`, and
  `4e6f2125`; PR #339 is based on the later canonical
  `main@cb7564c98427e339794e28a101efdca8c40e0a27`.
- AI Agent Book PR #339 removes unnecessary expression evaluation from two
  bundled MCP client examples. It is open at `9ae0c0c1`, clean and mergeable,
  with GitGuardian and CodeRabbit passing.
- No OpenSandbox personal fork, global skill installation, issue claim, comment, branch push, or other upstream action has been performed.
- Karmada is currently on `feature/cert-mode-rotate` and 17 commits behind its tracked `upstream/master`; the canonical push URL is enabled and must be disabled before upstream work.
- AgentCube canonical `upstream` push is disabled.
- `./workstation doctor` reports Karmada's enabled canonical push URL and the absent OpenSandbox path. Work API's fork is registered; no `AGENTS.md` exists in that repository.

## Blockers

- OpenSandbox personal fork is not registered; this does not block read-only scouting.
- OpenSandbox candidate issues must be refreshed immediately before selection because community state changes quickly.
- Workstation-wide doctor is red on Karmada's enabled canonical push and the
  absent OpenSandbox and Work API checkouts described above.

## Next

1. Monitor AI Agent Book PR #339 for maintainer review; require a new exact gate before any branch update or comment.
2. Extend context discovery with path-scoped nested `AGENTS.md` and compact report indexes.
3. Disable Karmada's canonical push URL before starting new contribution work.
4. Restore or re-onboard OpenSandbox before continuing candidate selection.

## Stop Conditions

- Stop before creating a fork, claim, issue, PR, review, comment, reviewer request, maintainer mention, or open-PR branch update without exact user approval.
- Stop before privileged/Kubernetes/cloud smoke tests if cleanup, credentials, or host impact is not controlled.
