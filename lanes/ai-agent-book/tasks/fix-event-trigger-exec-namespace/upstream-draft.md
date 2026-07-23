# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Proposed gated actions:

1. Push `d69742a1c005792c01f5a72bf3aa40dec3c2d2de` by exact SHA to
   `ranxi2001/ai-agent-book:fix/event-trigger-exec-namespace`.
2. Open a PR from that branch to `bojieli/ai-agent-book:main` with the exact
   title and body below.

No upstream action is authorized by this file. Obtain approval for the exact
commit, target, title, and body before posting.

## Title

fix(chapter4): give code interpreter an explicit namespace

## Body

## Summary

- execute event-trigger agent snippets in one explicit namespace
- add an offline regression test for functions that reference variables
  assigned earlier in the same snippet

`_tool_code_interpreter()` currently calls bare `exec(code)` inside a method.
Top-level assignments then land in the method's local namespace, while
functions defined by the snippet resolve names through module globals. A
common generated snippet such as:

```python
value = 5

def double():
    return value * 2

print(double())
```

therefore raises `NameError: name 'value' is not defined`.

Using one explicit namespace gives the snippet normal module-like name
resolution. This mirrors the equivalent chapter 2 fix merged in #199.

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
