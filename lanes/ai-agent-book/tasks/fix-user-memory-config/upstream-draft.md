# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Completed with explicit user approval on 2026-07-23:

1. Push `c09e43e5f0b256188f687c0d4657f4c68c6f428f` to
   `ranxi2001/ai-agent-book:fix/user-memory-config`.
2. Open a PR from that branch to `bojieli/ai-agent-book:main`.

Created: `https://github.com/bojieli/ai-agent-book/pull/322`

The maintainer merged the approved head on 2026-07-23 as
`1912079f0bfc58be74bc077ece0e9fd188be7dbb`; GitGuardian passed. No follow-up
upstream action is pending.

## Title

fix(user-memory): remove unsupported config option

## Body

## Summary

- remove the obsolete `update_threshold` option from the quickstart and
  conversation-processing demos
- update both provider examples to use the current `MemoryProcessorConfig` API

`update_threshold` was removed when memory updates moved to direct agent tool
calls, but these examples still passed it to the dataclass and failed during
construction before any provider request.

## Validation

- `python -m pytest -q` (`5 passed`)
- real `MemoryProcessorConfig` constructor smoke test
- AST scan confirming demo keywords match supported dataclass fields
- `python -m py_compile` for the changed Python entry points
- `python3 scripts/check_i18n_consistency.py`
- `git diff --check`

Live LLM-backed demos were not run because they require external API
credentials. This patch changes example configuration only; it does not alter
memory-processing behavior.
