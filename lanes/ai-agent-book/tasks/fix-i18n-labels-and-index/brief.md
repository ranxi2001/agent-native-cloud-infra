# Fix Tamil labels and English experiment index

## Problem

The compact language lists in the Simplified and Traditional Chinese READMEs
abbreviate Tamil as `泰`, which normally denotes Thai, even though the download
lists correctly say Tamil. The English chapter 3 project index also contains
one untranslated Chinese structured-index description.

## Scope

- Spell out Tamil as `泰米尔` in the root README and `泰米爾` in the zh-TW
  README.
- Translate the one structured-index row using terminology supported by the
  experiment's README.

## Non-Goals

- No book-body translation, experiment-README translation, language-count
  change, new locale, AutoGen/AG2 wording, or generated book artifacts.
- Do not expand into issue #89's experiment-level bilingual README proposal.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| Root and zh-TW READMEs | Remove Thai/Tamil ambiguity consistently | Translation drift or count change | Exact cross-locale scan, i18n consistency check |
| `chapter3/README.en.md` | Remove the sole Chinese project description | Inaccurate RAPTOR terminology | Compare project README, Markdown/table parse |

## Plan

1. Change only the two ambiguous labels and one untranslated table cell.
2. Scan maintained indexes for the stale strings.
3. Run i18n structure and Markdown parsing checks.

## Decision Log

- Base: `upstream/main@ef2d0cc12df979a3897ff7c09b1fbf1a8eb01794`.
- Use “hierarchical trees with recursive summarization” for RAPTOR, matching
  `chapter3/structured-index/README.md`; do not use the inaccurate expansion
  “recursive abstract tree.”
- Draft PR #84 also edits the root language list to add Japanese but retains
  the ambiguous Tamil abbreviation. It is a possible line-level conflict, not
  an implementation of this fix.
- Issue #89 concerns per-experiment README translation and does not claim this
  chapter-level index correction.
