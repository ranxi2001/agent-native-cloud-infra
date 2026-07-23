# AI Agent Book

Status: `active`

## Sources

- Canonical: `https://github.com/bojieli/ai-agent-book.git`, default branch
  `main@cb7564c98427e339794e28a101efdca8c40e0a27`, observed 2026-07-23.
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
- [PR #322](https://github.com/bojieli/ai-agent-book/pull/322) merged as
  `1912079f0bfc58be74bc077ece0e9fd188be7dbb`; [PR #323](https://github.com/bojieli/ai-agent-book/pull/323)
  merged as `2e8aed7983d803c619bd6729ab35bd4be2a6bbba` on 2026-07-23.
- [PR #325](https://github.com/bojieli/ai-agent-book/pull/325),
  [PR #326](https://github.com/bojieli/ai-agent-book/pull/326), and
  [PR #327](https://github.com/bojieli/ai-agent-book/pull/327) merged as
  `37c39dde1a4c24474e54e0f2210871da9f141e06`,
  `c83810cfa525bb8bd6a94c6c08305dc8f2bdf8cb`, and
  `4e6f21253c8826f3675d1517384d7b37e1a4fc76` on 2026-07-23.
- [PR #339](https://github.com/bojieli/ai-agent-book/pull/339) is open from
  `9ae0c0c1f875a5062edc53b5ff748cfd4ac6eafc`; it is clean and mergeable, and
  GitGuardian and CodeRabbit passed on 2026-07-23.
