# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Completed with explicit user approval on 2026-07-24:

1. Pushed exact commit `25de486e295fe643347c6d4808091baff61972ae` to
   `ranxi2001/ai-agent-book:fix/multimodal-tools-toggle`.
2. Created non-draft [PR #377](https://github.com/bojieli/ai-agent-book/pull/377)
   from that branch to `bojieli/ai-agent-book:main` with the exact title and
   original body below.

GitHub verified one commit, the approved head SHA, and the approved 3-file
`+55/-8` diff. CodeRabbit subsequently appended its generated release notes to
the PR body. GitGuardian and CodeRabbit passed; the PR is clean and mergeable.
No follow-up branch update, comment, or reviewer request is authorized.

## Title

`fix(multimodal-agent): repair interactive tools toggle`

## Body

```markdown
## Summary

- centralize multimodal tool state changes in `MultimodalAgent`
- make the documented `/tools on` command initialize both tool execution and
  the OpenAI-compatible function definitions
- add offline regression tests for enabling and disabling tools interactively

The default interactive agent starts with tools disabled. `/tools on` currently
references `MultimodalTools` without importing it, so the command raises
`NameError`. Adding only that import would still leave `tool_definitions` empty,
and the OpenAI-compatible request path would omit tools after reporting that
they were enabled.

The new agent-owned transition keeps the enabled flag, execution object, and
tool definitions consistent. Disabling retains the existing schema cache while
the enabled flag prevents it from being sent.

## Validation

- focused Python 3.12 offline suite: 9 passed
- real credential-cleared stdin smoke for `/tools on` and `/quit`
- `python3 -m py_compile` for the changed source and test
- `git diff --check`

The complete component run is 15 passed and 4 failed. An exact-base run is 13
passed and the same 4 failed: two tests patch a Google SDK API that is no longer
present, and two do not mock the credential guards needed to reach their
provider clients.

No live provider request was run because credentials are not configured. The
direct Gemini streaming path already does not consume function tools even when
enabled at construction; adding Gemini tool calling is outside this fix.
```

## Posted Gate Summary

- Diff: 3 files, 55 insertions, 8 deletions.
- Focused tests: 9 passed on Python 3.12.
- Full comparison: patch 15 passed / 4 existing failures; exact base 13 passed /
  the same 4 failures.
- Other checks: CLI smoke, syntax compile, and whitespace check passed.
- Repository i18n check remains red on existing Japanese clone/project counts;
  this patch changes no documentation.
- Why upstream attention is appropriate now: the README documents the broken
  command, the failure reproduces on current main, and no issue, PR, or later
  commit overlaps it.
