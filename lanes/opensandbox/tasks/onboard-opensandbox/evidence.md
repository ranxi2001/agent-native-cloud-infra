# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-16 | DOC | [Canonical repository](https://github.com/opensandbox-group/OpenSandbox) | Repository is under `opensandbox-group`; old organization redirects | Canonical identity |
| 2026-07-16 | OBS | `git ls-remote --symref https://github.com/opensandbox-group/OpenSandbox.git HEAD` | `main`, `18eaee779685774ba97b8a5b4c3a06030a978722` | Default branch and observed remote HEAD |
| 2026-07-16 | OBS | Partial `git clone` with remote name `upstream` and disabled push URL | Clean `main...upstream/main` at the observed HEAD | Local source and safe canonical remote topology |
| 2026-07-16 | CODE | Root and `kubernetes/AGENTS.md` at `18eaee779685` | Root routes work to nearest component instructions; Kubernetes contracts and commands verified | Live instruction precedence and Kubernetes adapter |
| 2026-07-16 | CODE | `cli/src/opensandbox_cli/skill_registry.py` and `cli/src/opensandbox_cli/skills/*.md` | Six bundled skills, including credential vault | Native skill inventory comes from executable source |
| 2026-07-16 | CODE/CI | Component manifests and [workflows](https://github.com/opensandbox-group/OpenSandbox/tree/main/.github/workflows) | Component/Kubernetes Go baseline is 1.25; Go SDK keeps older compatibility | General contribution prose is not the sole toolchain source |
| 2026-07-16 | DOC | [Contribution guide](https://github.com/opensandbox-group/OpenSandbox/blob/main/CONTRIBUTING.md), [PR template](https://github.com/opensandbox-group/OpenSandbox/blob/main/.github/pull_request_template.md), and [OSEP guide](https://github.com/opensandbox-group/OpenSandbox/blob/main/oseps/CONTRIBUTING.md) | Conventional commits, template fields, and proposal gates identified | Initial contribution contract |
| 2026-07-16 | OBS | `./scripts/verify-license.sh` | Passed; subsequent `git status --short --branch` remained clean | One non-privileged preflight is locally runnable and non-mutating |
| 2026-07-16 | OBS | Initial `gh issue/pr view --json` used unsupported relationship field names | CLI returned available-field guidance; commands were rerun with supported fields | Failed evidence query was corrected rather than ignored |
| 2026-07-16 | OBS | Issue #1253 plus PR #1259 | PR is open and states `Closes #1253` | Helm docs CI is already being implemented |
| 2026-07-16 | OBS | Issue #1262 plus PR #1263 | PR is open, states `Closes #1262`, and has collaborator approval | Helm values schema is already being implemented |
| 2026-07-16 | OBS | Open issue/open PR search, then issue-specific searches | #1265 and #1217 have no matching open PR in the inspected search; both remain unassigned | Leads for further screening, not implementation authorization |
| 2026-07-16 | OBS | `./workstation doctor opensandbox` | No errors or warnings; personal fork absence remains informational | Project adapter is active and internally consistent |

No source change, personal fork, global skill installation, issue claim, comment, branch push, runtime smoke, or upstream mutation was performed.
