# Contribution Gates

## Evidence Levels

| Level | Meaning | Allowed conclusion |
| --- | --- | --- |
| E0 | Symptom, report, or failing check | A problem was observed or reported. |
| E1 | Same-SHA repeat or independent observation | Nondeterminism or recurrence is supported. |
| E2 | Source-backed hypothesis or focused experiment | A candidate cause is plausible. |
| E3 | Producer-to-impact causal chain | Root cause and patch design are supportable. |
| E4 | Baseline/patch counterfactual or regression test | The patch cuts the proven causal edge. |

Label facts as local observation, code behavior at an exact ref, official contract, maintainer direction, or inference. Do not present inference as shipped behavior.

## Candidate Gate

- Current issue state and last material update checked
- Assignee and claim comments checked
- Same-topic open PRs checked
- Required proposal or design process checked
- Local validation feasibility checked
- Security reports routed privately

## Design Gate

Record before editing:

| Area | Required question |
| --- | --- |
| Problem | What user-visible or invariant-level behavior is wrong? |
| Existing flow | Which entry point, state, side effect, and cleanup path own it? |
| Scope | Which files must change and why? |
| Non-goals | Which adjacent components must not change? |
| Compatibility | Which API, schema, generated client, version, or upgrade path is affected? |
| Validation | Which positive, negative, boundary, lifecycle, and cleanup cases prove it? |

For three or more actors or state transitions, add a compact Mermaid flow or sequence diagram.

## Readiness Gate

- Diff contains one focused change from current upstream main
- Tests cover changed behavior and failure/cleanup paths
- Required generated files, license headers, formatting, and DCO/CLA rules checked
- `git status`, `git diff --check`, and unexpected mutation check clean
- Official PR template filled
- Breaking changes and skipped validation stated explicitly
- Commit identity and exact SHA recorded

## Upstream Posting Gate

Present all of the following and wait for explicit approval:

- Repository and target branch/thread
- Upstream-facing or fork-only classification
- Exact action
- Exact title and complete body/comment
- Diff summary and tests run
- Residual risk and skipped checks
- Why community attention is needed now

Approval for analysis or local code does not authorize posting. Approval for one exact action does not authorize follow-up comments, reviewer requests, or later branch pushes.
