# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-21 | Canonical identity | `gh repo view kubernetes-sigs/work-api`; local `git rev-parse` | Apache-2.0 repository, default `master` at `7263f5630a715438393bc0a129d4b29eb88c0222` | Exact project identity and activation ref |
| 2026-07-21 | Local source | `git status`; `git remote -v`; `git worktree list` | Clean checkout at `/home/work-api`; canonical remote renamed to `upstream` with push URL `DISABLED` | Safe local routing and remote boundary |
| 2026-07-21 | Fork state | `gh repo view ranxi2001/work-api` | Repository does not exist; authenticated upstream permission is `READ` | Personal fork is absent and must not be assumed |
| 2026-07-21 | Instructions | `rg --files` plus reads of `CONTRIBUTING.md`, `SECURITY.md`, `OWNERS`, `README.md`, Makefile, go.mod, and `.github/workflows/ci.yml` | Kubernetes CLA/security process, approvers, Go 1.25.8 toolchain, make commands, and CI tiers recorded; no AGENTS/native skill/local PR template found | Live contribution and validation contract |
| 2026-07-21 | Community scan | Paginated PR #70 comments/reviews plus open PR list and PR #71 | PR #70 and #71 are the only open PRs; both fail the new full-SHA Actions policy | Current first-contribution lane and overlap |
| 2026-07-21 | Narrow preflight | `actionlint v1.7.12`; `./hack/verify-all.sh -v` with temporary Python shim | Passed; no generated drift | At least one local workflow and repository validation path is usable |
| 2026-07-21 | Activation | `./workstation context work-api`; `./workstation doctor` | Context resolves active project and commands; doctor reports only informational Work API notices | Work API registration is internally consistent |

## Next Action

Continue `pin-actions-pr70` from its isolated worktree. Obtain explicit approval
before creating a fork, pushing the branch, or opening the drafted pull request.
