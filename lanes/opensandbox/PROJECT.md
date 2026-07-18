# OpenSandbox Project Profile

Observed at: 2026-07-16

## Identity

- Canonical repository: [opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)
- Official documentation: [open-sandbox.ai](https://open-sandbox.ai/)
- Default branch: `main`
- Remote HEAD observed with `git ls-remote`: `18eaee779685774ba97b8a5b4c3a06030a978722`
- License: Apache-2.0
- Local source: clean partial clone at `/home/ranxi/projects/opensandbox`
- Local branch: `main`, tracking `upstream/main`
- Canonical remote: `upstream` with push URL `DISABLED`
- Personal fork and `origin` remote: not registered

The former `alibaba/OpenSandbox` URL redirects to the new organization. Go modules, imports, Java coordinates, and JavaScript package names still use Alibaba-era namespaces in current source; never rewrite them solely because the GitHub organization changed.

The live checkout, root/Kubernetes instructions, PR template, CODEOWNERS, CI baseline, and repository-native runtime skills were verified at the observed HEAD. `./scripts/verify-license.sh` passed and left the worktree clean. The project is active for source reading and contribution preparation; fork creation and candidate selection remain separate gates.

## Repository Model

OpenSandbox is a polyglot monorepo spanning:

- Python FastAPI server and Python CLI;
- Go execd, ingress, egress, Kubernetes controllers, and Go SDK;
- JavaScript/TypeScript, Kotlin/Java, C#, Go, and Python SDKs;
- OpenAPI specifications and generated clients;
- Docker and Kubernetes providers, Helm/Kustomize, runtime isolation, ingress/egress, pools, credentials, and observability.

Root `AGENTS.md` routes work to directory-level `AGENTS.md` files. For any component, read the nearest `AGENTS.md` before relying on root prose. Current executable-source precedence is:

1. Component manifest/module and lock/tool-version files.
2. Nearest `AGENTS.md`.
3. Current CI workflow.
4. General `CONTRIBUTING.md`.

This matters because the general contribution guide contains stale Go and framework details while current modules/CI use Go 1.25 for components and Kubernetes. The Go SDK separately preserves a Go 1.20 compatibility floor.

## Toolchain And Validation Tiers

| Area | Current baseline | Narrow validation |
| --- | --- | --- |
| Server | Python >=3.10, uv, FastAPI | `cd server && uv sync --all-groups && uv run ruff check && uv run pyright && uv run pytest` |
| CLI | Python >=3.10; CI Python 3.11 | `cd cli && uv run --frozen ruff check && uv run --frozen pyright && uv run --frozen pytest tests/ -q` |
| execd/ingress | Go 1.25 | component `make golint`, `make build`, `make test` |
| egress | Go 1.25 | `go vet ./...`, `go build .`, `go test ./...` |
| Kubernetes | Go 1.25, controller-runtime, Kind | `make setup-envtest`, `make lint`, `make build`, `make task-executor-build`, `make test` |
| JS/TS SDK | Node >=20, pnpm 9.15.0 | install, lint, typecheck, build, and test from `sdks/` |
| Docs | Node 22, pnpm 9.15.0 | `cd docs && pnpm install --frozen-lockfile && pnpm docs:build` |
| Kotlin/Java | JDK 17, Gradle | nearest Gradle/AGENTS tasks |
| C# | .NET SDK 10 | nearest solution/AGENTS tasks |

Global checks include `pre-commit run --all-files` and `./scripts/verify-license.sh`.

Some component Make targets run `go mod tidy`, vendor dependencies, or lint with `--fix`. Always compare Git state before and after validation. Distinguish static/unit, Docker/component, Kind/cluster, privileged Linux, and cloud validation; report every unrun tier. Do not attempt privileged, KVM, bwrap, gVisor, mount, or cluster tests without controlled cleanup.

## Contribution Contract

- Use Conventional Commits and current branch naming conventions such as `feature/*`, `fix/*`, or `docs/*`.
- Apply the required Alibaba Apache-2.0 source header to new source files.
- No CLA/DCO or signoff workflow was found in the 2026-07-16 inspection; re-check current governance before the first PR.
- Use OSEP for major features or core API/runtime/security changes.
- Use `kubernetes/docs/proposals/` for major Kubernetes changes.
- Fill `.github/pull_request_template.md`: summary, testing, breaking changes, and issue/docs/tests/security/backward-compatibility checklist.
- Route security reports only through GitHub Private Vulnerability Reporting.
- Check `.github/CODEOWNERS` and path-based CI/label rules for the changed component.

## Native Runtime Skills

The OpenSandbox CLI currently exposes six built-in operational skills: sandbox lifecycle, command execution, file operations, network egress, troubleshooting, and credential vault. Discover the live list rather than relying on docs:

```bash
uv tool install opensandbox-cli
osb skills list -o json
```

Installing all built-ins globally changes the user's Codex skill environment and is not part of onboarding by default. Ask before running a global install command. These operational skills complement, rather than replace, this workstation's contribution skills.

## Contribution Readiness

Completed:

- Canonical partial clone at the exact observed HEAD.
- Read-only upstream topology and clean worktree.
- Root and Kubernetes instruction, CI, template, CODEOWNERS, and proposal-path inspection.
- Live discovery of six CLI-bundled runtime skills.
- Non-privileged license preflight with clean before/after Git state.
- Freshness correction that ruled out issues #1253 and #1262 due to open implementation PRs.

Remaining before implementation:

1. Select a current issue or self-contained improvement after assignee, claim, overlap, owner, and validation checks.
2. Obtain approval before creating a personal fork or contacting the community.
3. Register the fork as `origin`, keep canonical `upstream` push-disabled, and create a dedicated task/worktree from `upstream/main`.
4. Read the nearest component `AGENTS.md` and run a component-specific preflight for the selected surface.
