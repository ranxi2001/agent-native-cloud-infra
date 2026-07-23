# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Completed with explicit user approval on 2026-07-23:

1. Push `7eae95e31bf289a0720e0d3acbd1c05b342c32fc` to
   `ranxi2001/ai-agent-book:fix/recurring-timer-restore`.
2. Open a PR from that branch to `bojieli/ai-agent-book:main`.

Created: `https://github.com/bojieli/ai-agent-book/pull/323`

The maintainer merged the approved head on 2026-07-23 as
`2e8aed7983d803c619bd6729ab35bd4be2a6bbba`; GitGuardian passed. No follow-up
upstream action is pending.

## Title

fix(collaboration-tools): restore recurring timers

## Body

## Summary

- restore persisted recurring timers without requiring the one-shot-only
  `expiry_time` field
- resume persisted occurrence counts and save the terminal `completed` state
- add offline async regression coverage for reload, status, mixed timer types,
  and legacy terminal records

Recurring records store an interval rather than an expiry timestamp. The
existing reload and status paths treated every active timer as one-shot, so a
persisted recurring timer raised `KeyError` and could prevent later timers from
being restored. Restarted runners also reset their occurrence count, while the
terminal state was saved as `active` before being changed in memory.

Completed recurring records now remain queryable after restart, matching their
existing in-memory visibility and the persistence of expired one-shot timers.

## Validation

- `python3 -m unittest -v test_timer_tools.py` (`4 passed`)
- `python -m pytest -q test_timer_tools.py` (`4 passed`)
- async debug/warnings-as-errors run and 10 repeated focused runs
- existing one-shot timer smoke test
- `python3 scripts/check_i18n_consistency.py`
- `python -m py_compile` and whitespace checks

The full MCP experiment suite was not run because its optional browser and
service dependencies are not installed. Persisted records do not include a
next-fire timestamp, so a restored recurring timer still waits one complete
interval after restart; this patch intentionally keeps the existing storage
schema.
