# Migration validation

Validated on 2026-11-11 against OpenGAP source commit d7a8e2edb54b942d6b4635cdd8b919ebd23e5da5 (package 0.5.0, manifest spec 0.1.0).

## Executed locally

- Python jsonschema Draft202012Validator against vendored upstream schemas: ten manifests, ten tool definitions, five skill frontmatters, one workflow, and one knowledge index entry.
- Cross-file checks: child roster, local skill/tool resolution, tool implementation paths, inline judge schema fidelity, exportable output contracts, SOD assignments/conflicts/handoffs, and tool-free judge declarations.
- DAG checks: unique IDs, known dependencies, acyclicity, all expression inputs/output references, and dependency ancestry.
- Fourteen offline regression tests: successful synthetic packet cycle; blind input stripping; blind PASS rejection; duplicate judge rejection; changed draft/evidence identity rejection; stale judgments; unsupported assertions; negative-claim evidence tier; missing coverage; unresolved gates; working-directory independent script wrapper; MCP initialization boundary; and stdio MCP success/error responses.
- Byte comparison of all 43 source files in the uploaded ZIP against references/antigravity/. Retained packet scripts and five packet schemas are unchanged from that source.

Commands:

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

## Deployment checks still required

The OpenGAP Node CLI and its dependencies were unavailable in the conversion environment; the CLI was not executed locally. The GitHub workflow installs the pinned CLI and validates the coordinator plus every child. Its outcome must be read from the actual workflow run.

No live LLM run, codebase-memory connection, host document-write binding, deterministic scheduler, provider fallback, framework export, or actual fresh-session isolation was exercised. Passing schema and synthetic packet tests supports portable definition consistency and helper behavior. It does not certify a real document or deployed permission boundary. Follow docs/runtime-contract.md for those bindings before running a real review.
