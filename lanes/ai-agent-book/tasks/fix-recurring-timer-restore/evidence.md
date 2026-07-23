# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-23 | Canonical ref | Final `git fetch upstream main`; local rebase | `fd254a3f0ff2baebd9108695f477b58808fa53aa` | Branch starts from current canonical main |
| 2026-07-23 | Community scan | Fully paginated issues, PRs, comments, reviews, and canonical branches; final open-PR query | Open PRs #82/#84 are unrelated; no matching issue, PR, branch, or claim | Candidate is current and unclaimed |
| 2026-07-23 | Baseline counterfactual | Inline async harness against `upstream/main@f4680c0` | Recurring reload aborts on missing `expiry_time`, status fails, resumed count restarts at zero, and the terminal disk record remains `active` | The reported lifecycle failures are reproduced at the exact base |
| 2026-07-23 | Focused regression | `python3 -m unittest -v test_timer_tools.py` | 4 tests passed | Patch restores mixed timer records, status, occurrence counts, terminal persistence, and legacy records |
| 2026-07-23 | Pytest compatibility | Isolated venv: `python -m pytest -q test_timer_tools.py` | 4 passed in 0.03s | New standard-library tests also run under the repository's common pytest discovery path |
| 2026-07-23 | Stability and compatibility | Async debug with warnings as errors; 10 repeated focused runs; existing one-shot smoke with temporary config | All passed; cancelled one-shot storage was `{}` | No observed async leak/flakiness or one-shot persistence regression |
| 2026-07-23 | Repository checks | `python3 scripts/check_i18n_consistency.py`; `py_compile`; tracked/untracked whitespace checks | All passed | Repository indexes remain aligned and changed Python sources parse cleanly |
| 2026-07-23 | Post-rebase validation | `unittest`, pytest, `py_compile`, repository i18n check, whitespace check | 4 tests passed under each runner; all other checks passed | Patch remains valid on latest canonical main |
| 2026-07-23 | Local commit | `7eae95e31bf289a0720e0d3acbd1c05b342c32fc` | 2 files, 220 insertions, 21 deletions | Reviewer-ready local patch identity |
| 2026-07-23 | Approved fork push | Exact-SHA refspec to `ranxi2001/ai-agent-book:fix/recurring-timer-restore` | Remote branch is exactly `7eae95e31bf289a0720e0d3acbd1c05b342c32fc` | Approved patch is available without rewriting an existing branch |
| 2026-07-23 | Approved PR creation | `gh pr create`; `gh pr view 323`; `gh pr checks 323` | PR #323 is open and mergeable with the approved title/body, head SHA, and +220/-21 diff; GitGuardian passed | Exact approved contribution is upstream for review |
| 2026-07-23 | Upstream outcome | `gh pr view 323`; canonical `upstream/main` history | Maintainer merged PR #323 as `2e8aed7983d803c619bd6729ab35bd4be2a6bbba` | Contribution is complete and must not be duplicated |

## Residual Risk And Skipped Tiers

- Persisted records do not contain a next-fire timestamp. A restored recurring
  timer therefore waits one complete interval after restart. This patch keeps
  the existing storage schema and does not attempt a scheduling migration.
- The complete MCP experiment suite was not run because its browser, service,
  and notification dependencies are not installed. Changed timer behavior is
  covered by focused offline tests; the repository i18n check also passed.
