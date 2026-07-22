# Fix citation punctuation and JSON code fences

## Problem

Chinese citation footnotes contain a space between a quoted title and the
following comma or period. The chapter 4 structured-event example is valid
JSON but is fenced as JavaScript in every maintained language edition.

## Scope

- Remove the punctuation-leading space from every matching citation footnote
  in the Chinese book source.
- Mark the shared chapter 4 structured-event example as `json` in all six
  maintained language editions.

## Non-Goals

- No prose, citation source, URL, experiment-count, framework-name, or language
  label changes.
- No generated PDF, EPUB, `_web`, or `site` artifacts.
- No upstream issue, branch push, or pull request without explicit approval.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `book/chapter{2,3,7,8,9}.md` | Normalize citation punctuation | Accidental prose changes | Exact-pattern scan, Pandoc parse, diff review |
| Six chapter 4 language files | Correct JSON syntax highlighting consistently | Editing a non-equivalent block | Parse each fenced payload as JSON, diff review |

## Plan

1. Apply the mechanical punctuation and fence-label changes.
2. Prove no matching citation footnotes or mislabeled shared examples remain.
3. Run Pandoc parsing and whitespace checks, then prepare the PR draft.

## Decision Log

- Base is current canonical `main` at
  `6421668b39536c8b75a6a86bce9bb81ee6be098e`.
- PR #197 already fixed the Bitter Lesson URL, PR #228 superseded the proposed
  project counts, and PR #271 corrected the missing-directory wording; those
  stale candidates are excluded.
- Open PRs #82 and #84 are unrelated translation work. No open or historical
  issue/PR/comment matches this punctuation or code-fence fix as observed on
  2026-07-22.
