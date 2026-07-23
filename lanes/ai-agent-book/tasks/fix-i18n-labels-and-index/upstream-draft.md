# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Proposed gated actions:

1. Push `05035b5d191267f5452107236bfb57efed07fcf2` by exact SHA to
   `ranxi2001/ai-agent-book:docs/fix-i18n-labels-and-index`.
2. Open a PR from that branch to `bojieli/ai-agent-book:main` with the exact
   title and body below.

No upstream action is authorized by this file. Obtain approval for the exact
commit, target, title, and body before posting.

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
