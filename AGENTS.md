# Agent-Native Cloud Infrastructure Workstation

## Purpose

This repository coordinates open-source engineering across independent source repositories. It owns project registration, contribution lanes, generic skills, and short portfolio state. It does not own Karmada, AgentCube, OpenSandbox, or their Git history.

## Core Principles

- Prefer exact refs and executable evidence over copied or remembered context.
- Load the smallest sufficient context: rules and current state first, indexes
  next, long reports and raw evidence only when the task requires them.
- Treat generated overlays, caches, and summaries as rebuildable views, not
  authoritative state.
- Evolve by promoting repeated, verified lessons into the narrowest durable
  owner; replace stale rules instead of accumulating contradictory guidance.
- Automate discovery, validation, indexing, and cleanup, but never infer
  authorization for upstream or external mutations.
- Measure context size, validation cost, and repeated failure patterns; prune
  machinery that does not improve correctness, restart speed, or review quality.

See `docs/architecture/core-principles.md` for the evolution and efficiency
model.

## Start Every Work Loop

1. Read root `PROGRESS.md`.
2. Run `./workstation status`.
3. Determine whether the work belongs to a registered source project or the independent `report/` domain.
4. For project work, use `.agents/skills/route-project-work/SKILL.md`, run `./workstation context <project>`, and read all applicable target-repository instructions. For report-only work, read `report/README.md` and load project context only when a claim depends on project source.
5. If a selected project has a knowledge ref, run `./workstation context-sync <project>`,
   then read the overlay's `AGENTS.md`, `PROGRESS.md`, and task-relevant report index.
6. For project work, read the project `PROJECT.md`, `BACKLOG.md`, and active task files before editing.

Run `./workstation doctor` when paths, remotes, refs, or onboarding state may have changed.

## Ownership Boundaries

- `projects/*.toml`: machine-readable project identity, local path, remotes, branches, domains, and command catalog.
- `lanes/<project>/PROJECT.md`: dated project snapshot and stable contribution contract.
- `lanes/<project>/BACKLOG.md`: current candidate priorities and next actions.
- `lanes/<project>/tasks/<task>/task.toml`: machine-readable task lifecycle state.
- Task `brief.md`: problem, design, scope, non-goals, and decisions.
- Task `evidence.md`: commands, source refs, observations, and supported claims.
- Task `upstream-draft.md`: exact proposed community-facing text; never proof of posting authorization.
- `PROGRESS.md`: short cross-project restart state only.
- `summaries/weekly/YYYY-Www.md`: compact reviewed cross-project outcomes,
  evidence links, blockers, and next actions for one ISO week.
- `report/README.md`: compact registry for workstation-owned technical reports.
- `report/*.md`: independent cross-project or topic reports; they do not carry
  repository, contribution-lane, or upstream-publication semantics.
- `.agents/skills/`: reusable cross-project procedures.
- `.context/projects/<project>/`: ignored, generated links to exact-ref project
  knowledge; never treat the link target as source ownership.
- Target repository/worktree: all product source edits and project tests.

Do not copy target-repository reports into `report/`. Keep project-specific investigation in its source repository or task lane; reserve `report/` for workstation-owned technical synthesis and link to the authoritative evidence.

## Instruction Precedence

Within a target repository, follow the user's current request, the nearest target `AGENTS.md`, root target instructions and native skills, the workstation project profile, then generic workstation rules. Use the stricter compatible safety rule. Surface irreconcilable conflicts before editing.

Project-local instructions are dynamic. A profile is a cached adapter, not authority over current manifests, CI, contribution guides, or nested `AGENTS.md` files.

## Contribution Isolation

- Use one task directory and one topic worktree per upstream contribution.
- Create topic branches from the latest canonical upstream default branch, not from `intern`, reporting, portfolio, or another feature branch.
- Keep source clones and `.worktrees/` out of this Git repository.
- Never let two agents write in the same worktree. Parallelize read-only scans or independent project/task work.
- Check `git status --short --branch` before and after edits. Preserve user and other-agent changes.
- Do not reset, clean, rebase, delete a worktree, force-push, or rewrite a branch unless the exact operation is in scope and its consequences have been checked.
- Prefer `--force-with-lease` over `--force` when rewriting an owned fork branch is explicitly required.
- Keep canonical upstream remotes read-only or with a disabled push URL. Push only to the personal fork after the relevant gate.

## Upstream Action Gate

Local research, code, commits, and drafts do not authorize upstream mutations. Before creating or updating an issue, PR, draft PR, comment, review, assignment, reviewer request, maintainer mention, or open-PR branch, present and obtain approval for:

- exact repository and target;
- exact action;
- exact title and full body/comment;
- diff and test summary;
- residual risks and skipped checks;
- why upstream attention is needed now.

Use English and the official template for upstream text unless the target project explicitly requires otherwise. Security findings must use the project's private reporting channel.

## Evidence And Review

- Ground current community claims in current official data; paginate issue, PR, review, and file queries.
- Pin code claims to an exact ref and time-sensitive observations to an `observed_at` timestamp.
- Separate local observations, code behavior, official contracts, maintainer direction, and inference.
- A green rerun supports nondeterminism, not root cause. Require a producer-to-impact causal chain before patching flakes or retry logic.
- Prove production reachability before presenting a synthetic fault as a confirmed bug.
- Distinguish released capability, main-only merged code, proposal, and local measurement.
- For three or more actors, branches, or state transitions, prefer a small Mermaid flow, sequence, or state diagram plus a prose conclusion.

## Knowledge Capture

- Put stable cross-project procedures in a workstation skill.
- Put stable project-specific rules in the project profile or target repository's own instructions.
- Put current task state in `task.toml`, not an improvised Markdown status vocabulary.
- Put investigation evidence in the task lane.
- Put independently maintained technical synthesis in `report/` and register it
  once in `report/README.md`; projects and summaries link to it.
- Keep `PROGRESS.md` below roughly one screen; archive details in tasks instead of growing a second report.
- Maintain at most one workstation summary per ISO week. Update it only for a
  durable cross-project outcome or decision; do not add daily or monthly views.
- Do not copy raw chats, volatile GitHub dumps, large generated images, build outputs, or secrets into Git.

## Security

Never commit credentials, tokens, kubeconfigs, cloud account identifiers, private cluster details, or unredacted secret-bearing logs. Keep ignored secret files permission-restricted. Do not print environment secrets while diagnosing tools. Treat sandbox execution, bind mounts, egress, credential injection, proxy trust, tenant identity, privileged containers, KVM, and service-account tokens as security boundaries.

## Validation

- `make test`: CLI contract tests, including temporary Git repositories and worktrees.
- `make validate-skills`: skill metadata and structure validation.
- `./workstation doctor`: registered path, Git, ref, and remote consistency.
- `./workstation doctor --context`: additionally require configured knowledge
  overlays to match their exact refs.
- `make check`: full workstation validation plus `git diff --check`.

Run target-project tests inside the target task worktree. Record exact commands and any unrun privileged, cluster, cloud, or release validation tier.
