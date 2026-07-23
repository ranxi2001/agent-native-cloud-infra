# Upstream Draft

Target: `bojieli/ai-agent-book:main`

Action: push `fix/collaboration-tools-safe-parsing` to `ranxi2001/ai-agent-book`
and create a non-draft pull request.

Posted exactly as approved: https://github.com/bojieli/ai-agent-book/pull/339

The maintainer merged the approved contribution on 2026-07-23 as
`cdb4bffc066b1b10f182a587fe1583723c222ac5`. No follow-up upstream action is
pending.

Title: `fix(collaboration-tools): avoid eval when parsing MCP results`

Body:

```markdown
## Summary

- replace two `eval()` calls used for MCP text results with a shared
  `ast.literal_eval()` parser
- validate that decoded results are dictionaries before callers use mapping
  operations
- cover Python repr values, expression-like string data, executable
  expressions, and non-dictionary literals

The bundled MCP server returns `str(result)`, so responses use Python-literal
syntax (`'...'`, `True`, and `None`) rather than JSON. `json.loads()` would not
preserve compatibility. `ast.literal_eval()` accepts the existing format
without evaluating call expressions in response text.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_result_parsing.py`
  (`4 passed`)
- `python3 -m py_compile` for the two examples, parser, and test
- import smoke test in a temporary venv with `mcp==1.28.1`
- `python3 scripts/check_i18n_consistency.py`
- `git diff --check`

The full MCP demo was not run because browser, notification, and external
service integrations are not configured. This change removes arbitrary Python
expression evaluation from the local stdio examples; it does not change the
server serialization format or add a response-size limit.
```

No upstream action is authorized by this file. Obtain approval for the exact target and text before posting.
