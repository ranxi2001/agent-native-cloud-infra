# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Completed with explicit user approval on 2026-07-23:

1. Pushed `d69742a1c005792c01f5a72bf3aa40dec3c2d2de` by exact SHA to
   `ranxi2001/ai-agent-book:fix/event-trigger-exec-namespace`.
2. Opened a PR from that branch to `bojieli/ai-agent-book:main` with the exact
   approved title and body below.

Created: `https://github.com/bojieli/ai-agent-book/pull/325`

GitHub verification shows the PR is open and clean with exact head
`d69742a1c005792c01f5a72bf3aa40dec3c2d2de`; GitGuardian passed. Any later
branch push, comment, reviewer request, or other upstream mutation remains
separately gated.

## Title

fix(chapter4): give code interpreter an explicit namespace

## Body

## Summary

- execute event-trigger agent snippets in one explicit namespace
- add an offline regression test for functions that reference earlier snippet
  assignments

`_tool_code_interpreter()` calls bare `exec(code)` inside a method. Top-level
assignments then use the method's local namespace, while functions defined by
the snippet resolve names through module globals. A snippet that assigns
`value = 5` and reads it inside `double()` therefore raises `NameError`. One
explicit namespace restores module-like name resolution and mirrors the
chapter 2 fix merged in #199.

## Validation

- `python3 chapter4/agent-with-event-trigger/test_code_interpreter.py -v`
  (`1 test passed`)
- `python3 -m py_compile` for the changed source and test
- `python3 scripts/check_i18n_consistency.py`
- `git diff --check`

This is a namespace correctness fix, not a Python sandbox: snippets retain
normal builtins and can import modules. Code that relied on accidental access
to `self` or modules imported by `agent.py` must import or define its own
dependencies.
