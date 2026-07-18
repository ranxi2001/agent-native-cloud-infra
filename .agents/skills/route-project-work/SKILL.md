---
name: route-project-work
description: Route engineering work across the workstation's registered repositories and isolated contribution lanes. Use for any task that names, compares, or changes Karmada, AgentCube, OpenSandbox, another registered project, an issue or PR URL, a project task, or multiple open-source repositories at once; also use before delegating concurrent project work or choosing a target worktree.
---

# Route Project Work

Establish the target repository, task lane, instructions, and write boundary before doing project work.

## Start

1. Read root `PROGRESS.md` for cross-project state.
2. Run `./workstation list` and `./workstation status`.
3. Select the project from the explicit name, path, issue/PR URL, or registered domains.
4. Run `./workstation context <project>`.
5. Read the project lane's `PROJECT.md`, `BACKLOG.md`, and relevant task files.
6. Read every applicable target-repository instruction before editing. Follow the precedence in `references/routing-contract.md`.

If `context` reports an instruction or skill as a Git ref such as `origin/intern:AGENTS.md`, read it with `git -C <repo> show <ref>:<path>`. Do not switch the source worktree merely to load instructions.

## Route

- Keep discovery and portfolio state in this workstation.
- Keep source edits and project tests in the target repository or its task worktree.
- Keep one contribution per worktree and one machine-readable `task.toml` per task.
- Use project-local skills for project-specific behavior. Use workstation skills for routing, onboarding, contribution gates, and cross-project review.
- Treat `planned` projects as research/onboarding lanes until their repository, remotes, instructions, and validation commands are verified.

For a new task, create the lane first:

```bash
./workstation task-create <project> <slug> --title "<title>" --issue "<url>"
```

Add `--worktree --branch <kind/topic> [--base <ref>]` only when implementation is ready and the local repository exists.

## Coordinate Concurrent Work

- Parallelize read-only scans across projects.
- Assign different agents or processes different task directories and worktrees.
- Never allow two writers in the same worktree.
- Re-read `git status --short --branch` before and after edits because another agent or the user may have changed shared files.
- Keep upstream mutations serialized behind the approval gate in `manage-upstream-contribution`.

## Close

1. Record task facts in `task.toml`, reasoning in `brief.md`, raw-source links and commands in `evidence.md`, and proposed community text in `upstream-draft.md`.
2. Update the project `BACKLOG.md` only when priority or next action changed.
3. Keep root `PROGRESS.md` short: active tasks, blockers, next actions, and stop conditions only.
4. Run `./workstation status` and report the exact repository/worktree changed and verification completed.
