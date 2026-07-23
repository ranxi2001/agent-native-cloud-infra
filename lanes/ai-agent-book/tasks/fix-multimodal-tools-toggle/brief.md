# Fix interactive multimodal tools toggle

## Problem

The documented `/tools on` command raises `NameError` in a default interactive
session because `main.py` references `MultimodalTools` without importing it.
Even adding that import would leave `tool_definitions` empty: the default agent
is constructed with tools disabled, while the command only updates the flag and
execution object. OpenAI-compatible requests would therefore still omit the
tool schemas after reporting that tools were enabled.

## Scope

- Give `MultimodalAgent` one method that keeps the enabled flag, execution
  object, and OpenAI-compatible tool definitions in a valid state.
- Route both interactive `/tools on` and `/tools off` through that method.
- Add offline interaction tests for enabling from the default state and
  disabling an enabled agent.

## Non-Goals

- Do not add tool calling to the direct Gemini streaming path; tools are already
  limited to the OpenAI-compatible path even when enabled at construction.
- Do not change tool schemas, execution behavior, provider selection, prompts,
  or command output.
- Do not fold in unrelated documentation, localization, or license cleanup.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `chapter3/multimodal-agent/agent.py` | Centralize the three related tool states | Constructor behavior or repeated toggles regress | Existing initialization tests plus focused toggle tests |
| `chapter3/multimodal-agent/main.py` | Use the agent-owned transition for both commands | Interactive command behavior changes | Scripted stdin smoke test |
| `chapter3/multimodal-agent/test_interactive_tools_toggle.py` | Reproduce the documented default workflow without API calls | Input loop could hide an exception | Assert final flag, execution object, and schemas |

## Plan

1. Record the exact upstream base, duplicate scan, and two-part baseline failure.
2. Move existing schema initialization behind an idempotent agent method and
   call it from the constructor and interactive command.
3. Run the focused regression, existing component tests, real stdin smoke test,
   parse checks, and whitespace checks without API credentials.

## Decision Log

- Base: `upstream/main@0c8aa91525ae4fe9bcb9894f7d7392bbf9cc119e`.
- No issue, PR, or later commit overlaps this command as observed at
  `2026-07-24T01:15:00+08:00`; the sole open PR is unrelated translation work.
- Disabling keeps the already-built schemas, matching current behavior. The
  request path is gated by the enabled flag, while retaining schemas makes a
  later enable operation complete without rebuilding or discarding custom
  definitions.
- The command delegates to the agent instead of importing `MultimodalTools`
  into `main.py`, so state construction has one owner.
