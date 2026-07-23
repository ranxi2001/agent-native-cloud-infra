# Fix event-trigger code interpreter namespace

## Problem

`EventTriggeredAgent._tool_code_interpreter()` executes snippets with bare
`exec(code)` inside a method. Top-level assignments then land in the method's
local namespace while functions defined by the snippet resolve names through
module globals. A valid generated snippet such as `x = 5; def f(): return x`
therefore raises `NameError`.

## Scope

- Execute snippets with one explicit namespace dictionary.
- Add an offline regression test for a function reading a variable assigned by
  the same snippet.

## Non-Goals

- Do not claim or implement a Python security sandbox. An empty globals dict
  still receives normal builtins from Python.
- Do not change shell execution, file tools, prompts, provider behavior, or
  exception contracts.
- Do not reopen or claim to fix issue #191, which covered the chapter 2 copy.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `chapter4/agent-with-event-trigger/agent.py` | Give one snippet module-like name resolution | Assignment visibility or output capture changes | Focused offline execution test |
| Focused test | Preserve the reproduced LLM-generated code shape | Importing optional experiment dependencies | Isolated requirements environment |

## Plan

1. Reproduce the `NameError` at the exact base.
2. Apply the explicit shared-namespace pattern already merged for chapter 2.
3. Prove stdout capture and nested name resolution with an offline test.

## Decision Log

- Base: `upstream/main@ef2d0cc12df979a3897ff7c09b1fbf1a8eb01794`.
- Merged PR #199 fixed the same correctness defect in
  `chapter2/system-hint/agent.py` with `exec(code, exec_ns)`.
- `exec(code, {})` is not a security boundary because Python injects builtins;
  this contribution is intentionally framed only as namespace correctness.
- Open PRs #82 and #84 and open issues #63, #70, and #89 do not overlap this
  chapter 4 path as observed on 2026-07-23.
