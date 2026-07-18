---
name: manage-upstream-contribution
description: Manage an open-source contribution from current issue and repository evidence through isolated design, implementation, validation, reviewer-ready drafting, CI follow-up, and knowledge capture. Use when scouting or claiming issues, implementing fixes or features, preparing or updating PRs, responding to review, diagnosing CI, drafting issue/PR/review text, requesting reviewers, or taking any upstream-facing GitHub action in a registered project.
---

# Manage Upstream Contribution

Drive one focused change while separating local engineering work from community-facing mutations.

## Required Gates

Read `references/contribution-gates.md` before changing code or drafting upstream text.

1. Route the project with `route-project-work` and load repository-local instructions.
2. Refresh the issue/PR thread and repository state. Check assignees, claims, overlapping work, dependencies, and maintainer direction using paginated queries.
3. Create or resume one structured task. Keep one contribution in one worktree.
4. Create the topic branch from the latest canonical upstream default branch, never from a learning, reporting, or portfolio branch.
5. Write the problem, current behavior, file scope, non-goals, risk, and test matrix in `brief.md` before a non-trivial implementation.
6. Implement the smallest coherent change. Expand scope only after updating the task design.
7. Run focused tests first, then required repository checks. Record commands, exact commit, results, skipped tiers, and environment limitations in `evidence.md`.
8. Inspect generated/vendor/formatting changes and `git diff --check`. Do not assume a target named `test`, `lint`, or `build` is non-mutating.
9. Prepare concise reviewer-facing text in `upstream-draft.md` using the official template and project language. Make it an index to problem, behavior, risk, validation, and stable evidence.
10. Stop before any upstream-facing mutation and obtain approval for the exact target, action, title, and full body/comment. This includes issues, PRs, draft PRs, comments, reviews, assignments, mentions, reviewer requests, and pushes that update an open PR.

## Review And CI Follow-Up

- Classify feedback as in-scope correctness, independent prerequisite, repository-wide problem, or follow-up work before changing an open PR branch.
- Reproduce or source-prove a CI failure before patching. A green rerun proves nondeterminism, not root cause.
- Validate fixes on an isolated branch when reviewer notification would otherwise happen prematurely.
- Keep independent prerequisites in separate branches from current upstream main.
- Never use a self-PR or upstream PR merely as a disposable CI runner.

## Close

- Update task status and evidence.
- Preserve reusable project rules in the project profile or target repository instructions, not in chat.
- Improve this generic skill only for cross-project patterns; keep component-specific workflows in project-native skills.
- Report local branches, worktrees, commits, tests, residual risks, and the next gated action.
