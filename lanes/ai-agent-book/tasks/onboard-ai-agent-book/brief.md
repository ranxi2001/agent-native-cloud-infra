# Onboard AI Agent Book

## Problem

Register current repository identity, contribution rules, validation paths,
community state, and safe remotes before the first contribution.

## Scope

- Verify canonical repository, default branch, license, fork, instructions,
  governance, CI, and the first isolated task.

## Non-Goals

- No external fork creation, push, issue, PR, or comment.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| Project profile | Make future work restartable | Stale refs or unsafe push target | GitHub API, Git refs, doctor |

## Plan

1. Register and clone the repository.
2. Configure the canonical remote as read-only and the existing fork as origin.
3. Record contribution rules, checks, and refreshed candidates.

## Decision Log

- Activated at `main@6421668b39536c8b75a6a86bce9bb81ee6be098e`.
- No repository-local agent instructions or formal contribution templates were
  found; root README and CI workflows are the applicable contract.
