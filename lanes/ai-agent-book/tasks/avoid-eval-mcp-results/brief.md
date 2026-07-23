# Avoid eval when parsing MCP results

## Problem

`chapter4/collaboration-tools/client_example.py` and `quickstart.py` use
`eval()` to parse text returned by MCP tools. The bundled server serializes
tool dictionaries with `str(result)`, so the examples need Python-literal
compatibility, but they do not need arbitrary expression execution.

## Scope

- Add a small shared parser based on `ast.literal_eval()`.
- Require parsed MCP results to be dictionaries, matching both callers.
- Replace both `eval()` calls and add focused standard-library tests.

## Non-Goals

- Changing the server response format from Python literals to JSON.
- Claiming that the repository's local stdio setup is remotely exploitable.
- Refactoring unrelated MCP result handling or demo behavior.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `chapter4/collaboration-tools/result_parsing.py` | Parse server dictionary text without expression execution | Rejecting unexpected legacy response shapes | Focused unit tests |
| `chapter4/collaboration-tools/client_example.py` | Remove direct `eval()` from the reusable client wrapper | Import/path compatibility | Unit test import and `py_compile` |
| `chapter4/collaboration-tools/quickstart.py` | Remove direct `eval()` from the timer demo | Timer result parsing regression | Unit tests and `py_compile` |
| `chapter4/collaboration-tools/test_result_parsing.py` | Cover accepted and rejected inputs | Test-only | `python3 -m unittest -v test_result_parsing.py` |

## Plan

1. Implement `parse_mapping()` with `ast.literal_eval()` and a dictionary type check.
2. Route both example call sites through the helper.
3. Test representative server output, nested values, inert suspicious strings,
   executable expressions, and non-dictionary literals.
4. Recheck latest upstream state, duplicate PRs, syntax, focused tests, i18n,
   and whitespace before proposing the upstream action.

## Decision Log

- 2026-07-23: Use `ast.literal_eval()` rather than `json.loads()` because the
  bundled server currently returns `str(dict)` with single quotes and Python
  values such as `True` and `None`.
- 2026-07-23: Validate the top-level type as `dict` because both call sites use
  mapping operations and silently accepting other literals would defer errors.
