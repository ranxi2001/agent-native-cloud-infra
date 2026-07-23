# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Proposed gated actions:

1. Push `b1471929f4e29a2bbcd7cea662c0e89c72d72502` by exact SHA to
   `ranxi2001/ai-agent-book:fix/missing-direct-dependencies`.
2. Open a PR from that branch to `bojieli/ai-agent-book:main` with the exact
   title and body below.

No upstream action is authorized by this file. Obtain approval for the exact
commit, target, title, and body before posting.

## Title

fix: declare missing direct experiment dependencies

## Body

## Summary

- declare `requests` for the attention-visualization experiment
- declare `requests` and `aiofiles` for the structured-index experiment

Both experiments directly import packages that their local
`requirements.txt` files do not declare, so installation depends on unrelated
packages providing them transitively. The version floors match versions
already used by other experiments in this repository.

## Validation

- parsed all 41 entries in the two changed requirement files
- AST audit confirming all required direct third-party imports are declared
- fresh venv installation and import of `requests==2.31.0` and
  `aiofiles==24.1.0`
- `pip check`
- `python3 scripts/check_i18n_consistency.py`
- `git diff --check`

The complete ML-heavy requirement sets and live model/API workflows were not
run. `igraph` and `leidenalg` remain optional because structured index catches
their import failure and falls back to NetworkX Louvain.
