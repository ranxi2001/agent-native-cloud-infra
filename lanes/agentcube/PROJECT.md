# AgentCube Project Profile

Observed at: 2026-07-21 (local refs)

## Identity

- Canonical repository: `volcano-sh/agentcube`
- Default branch: `main`
- Local source: `/home/agentcube`
- Personal fork: `ranxi2001/agentcube` as `origin`
- Canonical remote: `upstream`
- Canonical ref: `upstream/main@58422c02b673daf1cb7991f22e4e1476e97ea1f3`
- Current source worktree: clean
  `intern@d2ff20430821b6c0a865f102c619efd562a86778`, tracking `origin/intern`

The long-lived `intern` branch contains project learning records and many project-native skills. Do not use it as the base of an upstream topic branch. Create a separate worktree from current `upstream/main`.

The canonical remote push URL is `DISABLED`, so an accidental `git push upstream` fails locally.

## Architecture Surface

AgentCube is a Go-first Kubernetes agent runtime platform with Python CLI/SDK surfaces. Main review areas include workload/session lifecycle, routing, sandbox/runtime integration, warm pools, storage, auth, generated APIs/clients, Kubernetes deployment, and end-to-end cleanup.

## Native Context

Run `./workstation context-sync agentcube`, then run the project context
command and read the generated overlay's root `AGENTS.md`, `PROGRESS.md`, and
task-relevant report index. Reuse project-specific issue, PR, review, runtime
smoke, Mermaid, and visualization skills where applicable. Keep the workstation
generic layer responsible for multi-project routing and task isolation.

## Commands

- Build: `make build-all`
- Unit tests: `make test`
- Lint/format: `make lint`, `make fmt`
- Generated artifacts: `make gen-all`
- End-to-end: `make e2e`
- Python tests: component-specific suites under `sdk-python/tests/` and `cmd/cli/tests/`

## Contribution Contract

- Keep fork `main` as a mirror of canonical `upstream/main`.
- Keep learning records and local skills on `intern` or in this workstation.
- Use signed-off, focused topic commits from `upstream/main` for upstream PRs.
- Refresh issue/PR state before selecting work and verify exact commit checks after fork pushes.
- Obtain exact-action approval before community-facing mutations or open-PR branch pushes.
