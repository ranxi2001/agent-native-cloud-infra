# Routing Contract

## Instruction Precedence

Apply instructions in this order:

1. The user's current, explicit request.
2. The nearest `AGENTS.md` governing the target file in the source worktree.
3. Root repository instructions, contribution guides, templates, and project-local skills.
4. The workstation project profile and task lane.
5. Root workstation rules and generic skills.

Use the stricter safety rule when two compatible layers differ. Surface a true conflict before editing.

## Project Selection

| Signal | Route |
| --- | --- |
| Explicit project id or repository path | Use that registered project. |
| GitHub URL | Match `OWNER/REPO` to `upstream_repo` or fork URL. |
| Existing task slug | Use the project named in `task.toml`. |
| Domain-only request | Compare registered domains and profiles; ask only if multiple targets would materially change the result. |
| Cross-project comparison | Create no source worktree unless implementation is selected. Keep evidence separated by project. |
| Workstation technical report | Use `report/README.md`; do not register it as a project. Load a project context only for project-source evidence or changes. |

## State Boundaries

| State | Source of truth |
| --- | --- |
| Project identity, remotes, path, commands | `projects/<id>.toml` |
| Stable project snapshot and contribution contract | `lanes/<id>/PROJECT.md` |
| Candidate priorities | `lanes/<id>/BACKLOG.md` |
| Task status | `lanes/<id>/tasks/<slug>/task.toml` |
| Design and decisions | Task `brief.md` |
| Observations and source links | Task `evidence.md` |
| Exact proposed upstream text | Task `upstream-draft.md` |
| Short portfolio restart state | Root `PROGRESS.md` |
| Independent technical-report catalog and content | `report/README.md` and `report/*.md` |
| Source code | Target repository task worktree |

Do not copy long project-local reports into the workstation. Link stable local paths or upstream URLs and capture only the decision-relevant conclusion.
