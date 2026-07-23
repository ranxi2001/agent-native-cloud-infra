# Evidence

| Time | Kind | Source / command | Result | Claim supported |
| --- | --- | --- | --- | --- |
| 2026-07-23T10:50:15+08:00 | Canonical ref | `git fetch upstream main`; `git rev-parse HEAD upstream/main`; `git rev-list --left-right --count upstream/main...HEAD` | Worktree HEAD and canonical main are `ef2d0cc12df979a3897ff7c09b1fbf1a8eb01794`; ahead/behind is `0/0` | Patch is based on current canonical main |
| 2026-07-23T10:50:15+08:00 | Community scan | Paginated current PRs and issues; keyword and target-file history scans | Open PRs #324, #84, and #82 are unrelated; no open or merged dependency fix overlaps these manifests | Candidate is current and not duplicated |
| 2026-07-23 | Direct-import audit | AST scan of both experiment directories | `attention_visualization` directly imports `requests`; `structured-index` directly imports `requests` and `aiofiles`; all required third-party roots are declared after the patch | Each added requirement is reachable production or sample code, not speculative |
| 2026-07-23 | Optional-boundary audit | `structured-index` Leiden imports and fallback flow | `igraph` and `leidenalg` are guarded by `ImportError` with a NetworkX Louvain fallback | Optional enhancements should not be promoted to mandatory dependencies |
| 2026-07-23 | Version evidence | Repository-wide requirements scan | `requests>=2.31.0` already appears in 17 experiment manifests; `chapter3/multimodal-agent` uses `aiofiles>=24.1.0` | Added floors follow versions already accepted by this repository |
| 2026-07-23 | Manifest validation | PEP 508 parse of both changed files | 41 non-comment requirement entries parsed | Both manifests remain syntactically valid |
| 2026-07-23 | Lower-bound install | Fresh venv install of exact `requests==2.31.0` and `aiofiles==24.1.0`; import smoke; `pip check` | Both exact versions imported and `pip check` reported no broken requirements | Added packages and selected floors install together |
| 2026-07-23 | Repository checks | `python3 scripts/check_i18n_consistency.py`; `git diff --check` | Passed | Repository indexes and whitespace remain clean |
| 2026-07-23 | Local commit | `b1471929f4e29a2bbcd7cea662c0e89c72d72502` | 2 files, 4 insertions, 1 deletion; clean worktree one commit ahead of `ef2d0cc` | Reviewer-ready local patch identity |

## Residual Risk And Skipped Tiers

- The two complete experiment requirement sets were not installed because they
  include large ML and GraphRAG dependencies. Live model/API workflows were
  also not run. Validation proves the missing direct declarations and their
  exact lower-bound installation, not the compatibility of every permitted
  transitive version.
- The chosen lower bounds come from repository consistency rather than a claim
  that they are the oldest versions capable of every used API.
