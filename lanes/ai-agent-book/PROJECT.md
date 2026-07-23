# AI Agent Book

Status: `active`

## Sources

- Canonical: `https://github.com/bojieli/ai-agent-book.git`, default branch
  `main@fd254a3f0ff2baebd9108695f477b58808fa53aa`, observed 2026-07-23.
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

## Current Contributions

- [PR #288](https://github.com/bojieli/ai-agent-book/pull/288) merged into
  `main` as `e9d1fe79fc1dbf1a950d1eab30721f5fe5ee8b91` on 2026-07-22.
- [PR #322](https://github.com/bojieli/ai-agent-book/pull/322) fixes the stale
  user-memory config option; [PR #323](https://github.com/bojieli/ai-agent-book/pull/323)
  restores recurring timers. Both are open at their approved exact heads.
