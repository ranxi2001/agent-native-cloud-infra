# Remove unsupported user-memory config options

## Problem

Two runnable user-memory demos and two provider examples pass
`update_threshold` to `MemoryProcessorConfig`, but that dataclass no longer
defines the field. Both demos fail during construction before any API call.

## Scope

- Remove the four stale `update_threshold` keyword arguments from
  `quickstart.py`, `demo_conversation_processing.py`, and `PROVIDERS.md`.

## Non-Goals

- Do not reintroduce an unused configuration field or change memory-update
  behavior, thresholds, providers, prompts, or storage.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| User-memory demos and provider examples | Match calls to the current dataclass contract | Accidentally changing another option | Constructor smoke test, existing focused tests, exact-reference scan |

## Plan

1. Delete only the unsupported keywords.
2. Prove no `update_threshold` reference remains in the experiment.
3. Run constructor smoke and existing offline regression tests.

## Decision Log

- Base: `upstream/main@fd254a3f0ff2baebd9108695f477b58808fa53aa`.
- Commit `697be969` removed the confidence/threshold path when memory updates
  moved to direct agent tool calls. Adding the field back would accept a
  configuration value that has no effect, so deletion is the compatible fix.
- No open issue, PR, comment claim, or canonical branch overlaps this change as
  observed on 2026-07-23.
