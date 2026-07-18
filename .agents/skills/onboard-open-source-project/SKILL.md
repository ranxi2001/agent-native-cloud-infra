---
name: onboard-open-source-project
description: Onboard an open-source repository into this multi-project workstation using current official sources, nested agent instructions, manifests, CI, governance, contribution templates, local validation, and a first-contribution lane. Use when adding a new project, preparing to contribute to an unfamiliar repository, refreshing a stale project profile, configuring canonical upstream and fork remotes, or promoting a project from planned to active.
---

# Onboard Open Source Project

Build a current, evidence-backed adapter around the upstream project without copying its source or rules into this workstation.

## Workflow

1. Read `references/onboarding-checklist.md`.
2. Confirm the canonical repository, default branch, license, current HEAD, and official documentation from primary sources.
3. Register a `planned` lane if none exists:

   ```bash
   ./workstation project-add <id> \
     --name "<display name>" \
     --path <local-path> \
     --upstream-repo <owner/repo> \
     --upstream-url <clone-url>
   ```

4. Inspect root and nearest directory-level `AGENTS.md`, manifests, CI workflows, build files, contribution guide, issue/PR templates, code ownership, proposals, security policy, and release model.
5. Treat executable truth as fresher than prose when they disagree: manifests and lockfiles, nearest `AGENTS.md`, CI, then general contribution docs. Record every verified drift instead of silently choosing.
6. Configure the local clone with canonical `upstream` and the personal fork as `origin` when a fork already exists. Do not create an external fork or push anything without user authorization. Disable or avoid upstream pushes.
7. Fill `projects/<id>.toml`, `lanes/<id>/PROJECT.md`, and `BACKLOG.md` with exact refs and an `observed_at` date.
8. Run the narrowest non-mutating preflight. Check `git status` before and after because some build targets format, vendor, tidy, generate, or fix files.
9. Perform a current community scan: open issues, assignees, claim comments, overlapping PRs, maintainer blockers, recent releases, and active proposals.
10. Create one onboarding task with evidence and a concrete next action. Promote the project to `active` only after the clone, remotes, instructions, and at least one validation path are known.

## Preserve Native Skills

- Discover repository-provided skills at runtime and list them in `./workstation context <id>`.
- Keep project-native operational skills in the project or its supported install mechanism.
- Keep contribution orchestration in this workstation.
- Record source ref, version, license, and local modifications before vendoring any external skill. Prefer references over copies.

## Deliverable

Leave a project profile that another agent can use without chat history, a prioritized backlog grounded in current community state, and an onboarding task that states what is verified, what remains unknown, and what action requires user approval.
