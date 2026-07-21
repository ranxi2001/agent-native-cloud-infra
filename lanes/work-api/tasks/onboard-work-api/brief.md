# Onboard Kubernetes SIGs Work API

## Problem

The existing `/home/work-api` checkout was not registered in the workstation,
its canonical repository was configured as a push-enabled `origin`, and no
current project adapter captured its contribution or validation rules.

## Scope

- Verify repository identity, default branch, license, governance, instructions,
  CI, manifests, and validation entry points.
- Register the source and lane, make the canonical remote read-only, and record
  the current PR #70/#71 contribution surface.
- Establish one narrow local validation path and a concrete first task.

## Non-Goals

- No personal fork creation or upstream mutation.
- No product-source change in the onboarding task.
- No deep architecture or release audit beyond what the selected workflow fix
  requires.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `projects/work-api.toml` | Machine-readable identity and commands | Stale path or remote could misroute later work | `./workstation context work-api`; doctor result |
| `lanes/work-api/PROJECT.md` | Stable contribution contract | Cached guidance could overrule live repository truth | Pin observed ref/date and list live instructions |
| `lanes/work-api/BACKLOG.md` | Current first-contribution candidates | Duplicate or stale candidate selection | Refresh PR #70 and #71 state through GitHub APIs |

## Plan

1. Verify canonical GitHub and local Git state.
2. Read repository-owned instructions, CI, governance, security, and commands.
3. Register and activate the project with canonical push disabled.
4. Create the isolated PR #70 implementation task.

## Decision Log

- The project is active because the clone, remotes, instructions, command paths,
  current candidates, and a non-cluster validation tier are all verified.
- No fork is registered because `ranxi2001/work-api` does not exist and creating
  it is an upstream-facing mutation requiring approval.
- `CONTRIBUTING.md` is the only discovered repository-local instruction file;
  no `AGENTS.md`, native skill, or local PR template exists at the observed ref.
