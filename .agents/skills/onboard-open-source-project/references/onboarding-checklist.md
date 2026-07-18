# Onboarding Checklist

## Identity And Governance

- Canonical repository and redirects
- Default branch and exact observed HEAD
- License and contribution license requirements
- Security reporting channel
- CLA, DCO, signoff, conventional commit, or release-note requirements
- CODEOWNERS/OWNERS and proposal process
- Exact issue and PR template paths

## Instruction Discovery

- Root `AGENTS.md`
- Nearest directory-level `AGENTS.md` for every likely component
- `CONTRIBUTING*`, `README*`, `SECURITY*`
- Manifests, lockfiles, tool-version files, Makefiles, task runners
- CI workflows and path-based change detection
- Repository-native skills and installation scope

Record disagreements with the exact files and refs. Do not "fix" imports, module paths, package coordinates, or branding solely because repository ownership changed.

## Architecture Fingerprint

- User entry points and public contracts
- Control-plane and data-plane components
- Persistent and cached state
- Runtime/isolation boundary
- SDKs, generated clients, schemas, and compatibility matrix
- Unit, integration, end-to-end, privileged, and cloud-only validation tiers
- Cleanup and rollback commands

## Community Scan

For every candidate, capture:

- Issue state, labels, author, assignee, and last material update
- Claim or `/assign` comments
- Same-topic open PRs and dependent proposals
- Component activity and recent maintainer review
- Reproduction or acceptance criteria
- Required hardware, cloud account, privilege, or secret
- Smallest credible validation available locally

Do not rank by `good first issue` alone. Prefer a clear problem, reachable local validation, active ownership, and a contribution surface that can be reviewed independently.

## Activation Gate

Mark the project `active` only when all are true:

- Local source path is a valid Git worktree.
- Canonical upstream and default branch are verified.
- Fork state is known, even if no fork exists yet.
- Instruction precedence is documented.
- Build/test commands are sourced from current code or CI.
- At least one narrow preflight has a recorded result or an explicit environment blocker.
- First contribution candidates were refreshed against current upstream state.
