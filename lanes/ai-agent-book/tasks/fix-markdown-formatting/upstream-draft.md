# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Completed with explicit user approval on 2026-07-22:

1. Push `e5aa013ddfaac633811f209cf119cdcaea10eca1` to
   `ranxi2001/ai-agent-book:docs/fix-markdown-formatting`.
2. Open a PR from that branch to `bojieli/ai-agent-book:main`.

Created: `https://github.com/bojieli/ai-agent-book/pull/288`

GitHub verification shows the PR is open and mergeable with head
`e5aa013ddfaac633811f209cf119cdcaea10eca1`. Any later branch push, comment,
reviewer request, or other upstream mutation remains separately gated.

## Title

docs: fix citation punctuation and JSON code fences

## Body

## Summary

- remove spaces between quoted titles and punctuation in all 18 matching
  Chinese citation footnotes
- label the shared structured-event example as JSON across all six maintained
  language editions

## Validation

- `git diff --check`
- Pandoc parsing of all 11 changed Markdown files
- `jq` parsing of each relabeled JSON payload
- `python3 scripts/check_i18n_consistency.py`

Pandoc emitted only pre-existing duplicate-note warnings in the translated
chapter 4 files. Full MkDocs, PDF, and EPUB builds were not run because the
changes are limited to punctuation whitespace and syntax-highlighting labels.
