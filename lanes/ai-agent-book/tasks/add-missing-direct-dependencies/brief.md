# Add missing direct experiment dependencies

## Problem

Two experiments directly import packages that their own `requirements.txt`
files do not declare: attention visualization imports `requests`, while the
structured-index document and API paths import `aiofiles` and its sample
downloader imports `requests`. Installation can therefore depend accidentally
on unrelated packages bringing them transitively.

## Scope

- Add `requests>=2.31.0` to the attention-visualization requirements.
- Add `aiofiles>=24.1.0` and `requests>=2.31.0` to the structured-index
  requirements.

## Non-Goals

- No dependency upgrades, lockfiles, code changes, or broad repository audit.
- Do not claim `requests` always fails to import today; large transitive
  dependencies may happen to install it.
- Do not change optional versus required feature boundaries.

## File Matrix

| Area | Why | Risk | Validation |
| --- | --- | --- | --- |
| `chapter2/attention_visualization/requirements.txt` | Declare direct HTTP-client import | Version conflicts | Parse manifest, install/import added requirement |
| `chapter3/structured-index/requirements.txt` | Declare direct async-file imports and sample-downloader HTTP import | Version conflicts | Parse manifest, install/import added requirements |

## Plan

1. Prove each direct import and absence from its local manifest at the base.
2. Add only the missing declarations in these two manifests using versions
   already accepted in this repository.
3. Validate requirement syntax and added-package installation/import in an
   isolated environment.

## Decision Log

- Base: `upstream/main@ef2d0cc12df979a3897ff7c09b1fbf1a8eb01794`.
- `requests>=2.31.0` is used by many adjacent experiments;
  `aiofiles>=24.1.0` is already used by `chapter3/multimodal-agent`.
- No matching issue, PR, canonical branch, or claim was found as observed on
  2026-07-23; open PRs #82 and #84 are unrelated translations.
