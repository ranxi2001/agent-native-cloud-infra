# AI Agent Book

Status: `active`

## Sources

- Canonical: `https://github.com/bojieli/ai-agent-book.git`, default branch
  `main@6421668b39536c8b75a6a86bce9bb81ee6be098e`, observed 2026-07-22.
- License: Apache-2.0. Local source: `/Users/onefly/Desktop/project/ai-agent-book`.
- `upstream` push is disabled; `origin` is `ranxi2001/ai-agent-book`.

## Architecture

- Chinese source is in `book/`; translations are in `book-{en,ru,ta,vi,zhtw}/`.
- `scripts/build_site.sh` assembles `_web/`; MkDocs builds the online site.

## Contribution Contract

- No `AGENTS.md`, CONTRIBUTING, SECURITY, CODEOWNERS, PR template, CLA, DCO,
  or signoff rule was found at the observed ref. Root README welcomes PRs.
- Run `python3 scripts/check_i18n_consistency.py` for i18n indexes. Site builds
  use `bash scripts/build_site.sh` and `mkdocs build -d site`.
- Fork pushes and upstream actions require explicit approval.
