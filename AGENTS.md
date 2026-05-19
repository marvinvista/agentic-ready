# AGENTS.md

## Product Standard

Keep `agentic-ready` small, deterministic, and public-safe.

- The public promise is: find the five reasons agents will skip your B2B product.
- Do not add private source references, paid-source excerpts, or strategy-framework bloat.
- Prefer exact artifacts over broad claims: `llms.txt`, OpenAPI, MCP manifests, schemas, pricing, sandbox docs, status/security pages.
- Keep runtime dependencies at zero unless a dependency materially improves the smoke test.
- Make CLI output blunt and useful before making it exhaustive.

## Verify

```bash
PYTHONPATH=src python3 -B -m unittest discover -s tests
PYTHONPATH=src python3 -B -m agentic_ready tests/fixtures/ready --fail-under ready
PYTHONPATH=src python3 -B -m agentic_ready tests/fixtures/not-ready --json
python3 scripts/verify-public-surface
```
