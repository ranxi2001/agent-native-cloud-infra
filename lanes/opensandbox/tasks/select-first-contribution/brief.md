# Select The First OpenSandbox Contribution

## Problem

OpenSandbox is locally active, but an open issue is not automatically available work. The first contribution must have no active implementation, a component boundary that can be validated locally, current owner/reviewer activity, and scope appropriate for an initial upstream change.

## Selection Criteria

| Criterion | Required evidence |
| --- | --- |
| Availability | Current issue, assignee, claim comments, and same-topic open PR scan |
| Scope | One reviewable behavior or documentation boundary with explicit non-goals |
| Ownership | CODEOWNERS and recent component review activity |
| Validation | A locally reachable focused check plus stated CI/privileged gaps |
| Upstream fit | Current docs/proposal/template rules and no maintainer-only operation disguised as contributor work |
| Learning value | Agent-native runtime, Kubernetes, lifecycle, security, or operational judgment that transfers across projects |

## Current Leads

| Lead | Initial assessment | Main uncertainty |
| --- | --- | --- |
| #1265 container image provenance discoverability | A focused README/docs pointer may be locally implementable; DockerHub account changes are maintainer-only | Whether maintainers want the repository-only slice separately and where the single source of truth belongs |
| #1217 server Helm chart release/docs | High operational value but spans publishing workflow, release artifact ownership, and documentation | Contributor-accessible scope versus maintainer release credentials |

Issues #1253 and #1262 are excluded because open PRs #1259 and #1263 already implement them. Issue #853 is excluded because credible validation needs ARM64 64K-page hardware unavailable in this workspace.

## Non-Goals

- Do not claim an issue or post a scope question without exact approval.
- Do not create a personal fork until a contribution is selected.
- Do not create a source worktree or draft a patch during screening.
- Do not use issue labels or absent assignees as the only availability signal.

## Plan

1. Trace #1265 against root README, release verification docs, docs ownership, docs build, and CODEOWNERS.
2. Trace #1217 against current chart publishing workflows, release tags/assets, docs, and ownership.
3. Compare at least one code/runtime candidate if a locally reproducible, non-overlapping issue is found.
4. Rank candidates by reviewability, validation reachability, maintainer dependency, and learning value.
5. Prepare any required scope-confirmation text locally and obtain exact approval before posting.
6. Create a dedicated implementation task/worktree only after selection.

## Decision Log

- Freshness scanning must join issue and open-PR evidence; issue state alone produced two false candidates in the first pass.
- Prefer a repository-owned change over an external account/release operation that only maintainers can complete.
