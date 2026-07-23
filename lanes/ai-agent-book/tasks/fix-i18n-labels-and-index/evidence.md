# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-23T10:55:00+08:00 | Canonical ref | `git fetch upstream main`; `git rev-parse HEAD upstream/main`; `git rev-list --left-right --count upstream/main...HEAD` | Worktree HEAD and canonical main are `ef2d0cc12df979a3897ff7c09b1fbf1a8eb01794`; ahead/behind is `0/0` | Patch is based on current canonical main |
| 2026-07-23T10:55:00+08:00 | Community scan | Current open issues and PRs plus open-PR target-file scan | PRs #324 and #82 do not overlap; draft PR #84 edits the same two language-summary lines but retains the ambiguous `泰` label | No current PR implements this fix; #84 creates a disclosed line-level conflict |
| 2026-07-23 | Locale evidence | Repository locale paths and full labels in the same READMEs | Locale `ta` is called `泰米尔语` in the root README and `泰米爾語` in zh-TW; `泰` is only the compact summary label | Spelling out the existing name removes ambiguity without changing locale identity or count |
| 2026-07-23 | Terminology evidence | `chapter3/structured-index/README.md` and implementation | RAPTOR builds hierarchical trees with recursive summarization; GraphRAG builds knowledge graphs | The English replacement describes implemented behavior and avoids the inaccurate “recursive abstract tree” expansion |
| 2026-07-23 | Exact scans | Stale label/Chinese-row scans and Han-character scan of `chapter3/README.en.md` | The three targeted stale strings are absent; the corrected chapter 3 English index contains no Han characters | Requested entries are fully corrected |
| 2026-07-23 | Markdown validation | Pandoc 3.6.1 GFM-to-JSON parse of all three changed files | Passed | Tables and Markdown remain parseable |
| 2026-07-23 | Repository checks | `python3 scripts/check_i18n_consistency.py`; `git diff --check` | Passed; 92 projects remain aligned across six languages | No locale structure or project-count drift was introduced |
| 2026-07-23 | Local commit | `05035b5d191267f5452107236bfb57efed07fcf2` | 3 files, 3 insertions, 3 deletions; clean worktree one commit ahead of `ef2d0cc` | Reviewer-ready local patch identity |
| 2026-07-23 | Approved fork push | Exact-SHA refspec to `ranxi2001/ai-agent-book:docs/fix-i18n-labels-and-index` | Remote branch is exactly `05035b5d191267f5452107236bfb57efed07fcf2` | Approved patch is available without rewriting an existing branch |
| 2026-07-23 | Approved PR creation | `gh pr create`; exact body/head/file verification; `gh pr checks 327` | PR #327 is open and clean at the approved head; repository check and GitGuardian passed | Exact approved contribution is upstream for review |
| 2026-07-23 | Upstream outcome | `gh pr view 327`; canonical `upstream/main` history | Maintainer merged PR #327 as `4e6f21253c8826f3675d1517384d7b37e1a4fc76` | Contribution is complete and must not be duplicated |

## Residual Risk And Skipped Tiers

- `泰米爾` follows the terminology already used elsewhere in this repository's
  zh-TW README. This contribution does not claim it is the official Taiwan
  CLDR display name.
- Draft PR #84 changes the same root and zh-TW summary lines while adding
  Japanese. If it advances, it will need to absorb this wording during rebase.
- Full MkDocs, PDF, and EPUB builds were not run for three one-line README
  edits. The maintained i18n check and Pandoc parsing cover the affected
  structure.
- This patch translates the named chapter 3 entry only; it does not claim that
  every English experiment index in the repository is fully translated.
