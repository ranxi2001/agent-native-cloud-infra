# Onboard OpenSandbox For First Contribution

## Problem

OpenSandbox needed an exact local source baseline, safe remote topology, live component instructions, validation evidence, and a current contribution scan before it could join the workstation as an active project.

## Current State

- Canonical `main` is cloned with blob filtering at `18eaee779685774ba97b8a5b4c3a06030a978722`.
- The canonical remote is named `upstream`; its push URL is `DISABLED`.
- Root and Kubernetes `AGENTS.md`, current CI, PR template, CODEOWNERS, proposal path, and six CLI-bundled runtime skills were inspected locally.
- The license verification preflight passed and did not modify the source worktree.
- The project is active for source reading and contribution preparation.
- No personal fork, `origin`, global skill install, issue claim, comment, push, or upstream action exists.
- Issues #1253 and #1262 were removed as candidates after the freshness scan found open implementation PRs #1259 and #1263.

## Scope And Result

| Area | Result | Validation |
| --- | --- | --- |
| Local clone and remotes | Complete | Clean `main...upstream/main`; canonical fetch URL; push URL disabled |
| Native instructions | Complete for root and Kubernetes onboarding | `workstation context` plus local root/Kubernetes instructions |
| Native Skills | Complete | Six CLI-bundled skill sources discovered through project registration |
| Non-privileged preflight | Complete | `./scripts/verify-license.sh` passed; before/after Git status clean |
| Community freshness | Complete for initial leads | #1253/#1262 cross-checked against #1259/#1263 and ruled out |
| Project activation | Complete | Registry moved from `planned` to `active`; doctor has no error/warning for OpenSandbox |
| First implementation task | Pending | Select and re-check a non-overlapping candidate first |

## Non-Goals

- Do not create a GitHub fork or contact maintainers without exact approval.
- Do not claim #1253, #1262, or another issue during onboarding.
- Do not install built-in skills globally without approval.
- Do not run privileged Linux, Kind, KVM, bwrap, gVisor, or cloud tests in the onboarding preflight.
- Do not rewrite Alibaba-era module/package coordinates because the GitHub organization moved.

## Next

1. Screen issue #1265's repository-owned documentation portion against current docs, CODEOWNERS, and docs build.
2. Compare it with other unassigned, non-overlapping candidates.
3. Ask before creating/registering the personal fork or sending a scope-confirmation comment.
4. Create a separate implementation task/worktree from `upstream/main` only after selection.

## Decision Log

- Keep OpenSandbox runtime-operation skills native to OpenSandbox; expose their source paths through the project adapter.
- Keep task status machine-readable in `task.toml` and detailed evidence in this lane.
- Treat shipped component releases, main-only merged changes, proposals, and local measurements as separate evidence classes.
- Treat an open issue without an assignee as unavailable when an active PR already implements it.
