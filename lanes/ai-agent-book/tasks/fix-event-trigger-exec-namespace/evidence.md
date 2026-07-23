# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-23T10:52:20+08:00 | Canonical ref | `git fetch upstream main`; `git rev-parse HEAD upstream/main`; `git ls-remote upstream refs/heads/main` | Worktree HEAD and canonical main are `ef2d0cc12df979a3897ff7c09b1fbf1a8eb01794`; ahead/behind is `0/0` | Patch is based on current canonical main |
| 2026-07-23T10:52:20+08:00 | Community scan | Fully paginated all-state PR file scan; current open issue and PR queries | Open PRs #324, #84, and #82 do not touch the target; no open, closed, or merged PR duplicates this chapter 4 fix | Candidate is current and not already claimed |
| 2026-07-23 | Prior art | Merged PR #199 and `chapter2/system-hint/agent.py` | Chapter 2's equivalent interpreter already uses `exec(code, exec_ns)` | The patch follows an accepted repository pattern rather than inventing a new contract |
| 2026-07-23 | Baseline counterfactual | In-memory load of the real `EventTriggeredAgent` from the exact base with its original bare `exec(code)` | A snippet assigning `value = 5` and reading it inside `double()` raises `NameError: name 'value' is not defined` | The namespace failure is reproduced in the actual entry point |
| 2026-07-23 | Focused regression | `PYTHONDONTWRITEBYTECODE=1 python3 chapter4/agent-with-event-trigger/test_code_interpreter.py -v` | 1 test passed; stdout is exactly `10\n` | One explicit namespace restores module-like name resolution and preserves output capture |
| 2026-07-23 | Source checks | `python3 -m py_compile` for the changed source and test; `git diff --check` | Passed | Changed Python parses and the patch has no whitespace errors |
| 2026-07-23 | Repository check | `python3 scripts/check_i18n_consistency.py` | Passed; 92 projects aligned across all six languages | Repository indexes remain consistent |
| 2026-07-23 | Local commit | `d69742a1c005792c01f5a72bf3aa40dec3c2d2de` | 2 files, 77 insertions, 1 deletion; clean worktree one commit ahead of `ef2d0cc` | Reviewer-ready local patch identity |

## Residual Risk And Skipped Tiers

- `exec(code, {})` is not a security sandbox. Python supplies normal builtins,
  and snippets can still import modules. This change is only a namespace
  correctness fix.
- Snippets no longer receive accidental access to method locals such as
  `self` or modules imported by `agent.py`; they must import their own
  dependencies. This matches the chapter 2 precedent and the standalone code
  interpreter contract.
- The repository does not provide CI for this experiment. The focused test was
  run with the standard library's `unittest`; pytest compatibility was not run
  because pytest is not installed in the current host Python.
