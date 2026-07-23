# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Completed with explicit user approval on 2026-07-23:

1. Pushed `05035b5d191267f5452107236bfb57efed07fcf2` by exact SHA to
   `ranxi2001/ai-agent-book:docs/fix-i18n-labels-and-index`.
2. Opened a PR from that branch to `bojieli/ai-agent-book:main` with the exact
   approved title and body below.

Created: `https://github.com/bojieli/ai-agent-book/pull/327`

The maintainer merged the approved head on 2026-07-23 as
`4e6f21253c8826f3675d1517384d7b37e1a4fc76`; the repository check and
GitGuardian passed. No follow-up upstream action is pending.

## Title

docs(i18n): clarify Tamil labels and translate chapter 3 index

## Body

## Summary

- spell out Tamil in the Simplified and Traditional Chinese language summaries
  to avoid confusion with Thai
- translate the `structured-index` entry in the English chapter 3 project
  index

The expanded Tamil labels follow the full names already used elsewhere in the
same READMEs. The English entry describes RAPTOR as hierarchical trees with
recursive summarization and GraphRAG as knowledge graphs, matching the
experiment README and implementation.

## Validation

- `python3 scripts/check_i18n_consistency.py`
- Pandoc 3.6.1 parsing of all three changed Markdown files
- exact scans for the old labels and untranslated row
- `git diff --check`

Full site, PDF, and EPUB builds were not run because the changes are limited
to three README table cells. Draft PR #84 also edits the two language-summary
lines while adding Japanese, so it may need to absorb this wording when
rebased.
