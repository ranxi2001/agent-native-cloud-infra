# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-23 | Canonical ref | Final `git fetch upstream main`; local rebase | `fd254a3f0ff2baebd9108695f477b58808fa53aa` | Branch starts from current canonical main |
| 2026-07-23 | Community scan | Fully paginated issues, PRs, comments, and canonical branches | Open PRs #82/#84 are unrelated; no matching issue, PR, branch, or claim | Candidate is current and unclaimed |
| 2026-07-23 | Baseline | Exact-ref construction in both runnable demos | Both fail before API use with `unexpected keyword argument 'update_threshold'` | Stale examples are user-reachable |
| 2026-07-23 | Source history | Commit `697be969` and current processor flow | Confidence/threshold processing was removed in favor of direct agent tool calls | Re-adding an unused field would be incorrect |
| 2026-07-23 | Constructor smoke | Real module `MemoryProcessorConfig(...)` with the remaining demo options | Passed in an isolated requirements venv | Patched option sets match the runtime dataclass |
| 2026-07-23 | Existing tests | `python -m pytest -q` in `chapter3/user-memory` | 5 passed in 1.19s | Existing offline behavior is preserved |
| 2026-07-23 | Focused validation | AST keyword contract scan; `py_compile`; zero-reference `rg`; `git diff --check` | All passed | No unsupported option remains and changed sources parse cleanly |
| 2026-07-23 | Repository check | `python3 scripts/check_i18n_consistency.py` | Passed; 92 projects aligned across all six languages | Repository indexes remain consistent |
| 2026-07-23 | Post-rebase validation | Focused pytest, `py_compile`, repository i18n check, whitespace check | 5 passed; all other checks passed | Patch remains valid on latest canonical main |
| 2026-07-23 | Local commit | `c09e43e5f0b256188f687c0d4657f4c68c6f428f` | 3 files, 3 insertions, 7 deletions | Reviewer-ready local patch identity |
| 2026-07-23 | Approved fork push | Exact-SHA refspec to `ranxi2001/ai-agent-book:fix/user-memory-config` | Remote branch is exactly `c09e43e5f0b256188f687c0d4657f4c68c6f428f` | Approved patch is available without rewriting an existing branch |
| 2026-07-23 | Approved PR creation | `gh pr create`; `gh pr view 322`; `gh pr checks 322` | PR #322 is open and mergeable with the approved title/body, head SHA, and +3/-7 diff; GitGuardian passed | Exact approved contribution is upstream for review |
| 2026-07-23 | Upstream outcome | `gh pr view 322`; canonical `upstream/main` history | Maintainer merged PR #322 as `1912079f0bfc58be74bc077ece0e9fd188be7dbb` | Contribution is complete and must not be duplicated |

## Skipped Tiers

- Live conversational demos were not run because they require external LLM API
  credentials. The failure and fix occur during local dataclass construction,
  before any provider call.
