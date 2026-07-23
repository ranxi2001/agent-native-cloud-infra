# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-22 | Canonical ref | Final `git fetch upstream main`; local rebase | `6421668b39536c8b75a6a86bce9bb81ee6be098e` | Topic worktree starts from current upstream main |
| 2026-07-22 | Community scan | Paginated GitHub REST queries for open/all issues, PRs, and issue comments | Only open PRs #82 and #84; no overlap or claim for this change | Candidate is current and unclaimed |
| 2026-07-22 | Stale candidates | Merged PRs #197, #228, and #271 | URL, experiment-count, and external-directory items are already fixed | Previously reported items must not be repeated |
| 2026-07-22 | Focused validation | `git diff --check`; Pandoc parse of 11 changed files; six extracted payloads through `jq -e`; `python3 scripts/check_i18n_consistency.py` | Passed; Pandoc only reported pre-existing translated chapter 4 duplicate-note warnings | Patch is parseable, JSON labels are correct, and i18n indexes remain aligned |
| 2026-07-22 | Local commit | `e5aa013ddfaac633811f209cf119cdcaea10eca1` | 11 files, 24 insertions and 24 deletions; branch one commit ahead of latest main | Reviewer-ready patch identity |
| 2026-07-22 | Approved fork push | `git push origin e5aa013...:refs/heads/docs/fix-markdown-formatting` | Fork branch created at the exact approved commit | Reviewed patch is available without rewriting any remote branch |
| 2026-07-22 | Approved PR creation | `gh pr create` followed by `gh pr view 288` | PR #288 is open and mergeable; head is exactly `e5aa013`; 11 files, +24/-24 | Exact approved contribution is upstream for review |
| 2026-07-23 | Upstream outcome | `gh pr view 288` | Maintainer merged the PR as `e9d1fe79fc1dbf1a950d1eab30721f5fe5ee8b91`; GitGuardian passed | Contribution is complete and must not be duplicated |

## Skipped Tiers

- Full MkDocs, PDF, and EPUB builds were not run. The changes are punctuation
  whitespace and syntax-highlighting labels; all changed Markdown parsed and
  all six relabeled payloads are valid JSON.
