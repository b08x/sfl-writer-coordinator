# SFL Writer Coordinator

R.U.T.H. — Records Uncertainty, Traces History — coordinates evidence-backed technical writing with nine leaf specialists. A sole author drafts; an evidence broker retrieves bounded source/graph evidence; three independent judges audit ideational, interpersonal, and textual concerns, then cross-examine a shared revision-bound evidence packet. Four domain advisors support scoping, validation, integration, and practical constraints.

This repository is the canonical portable OpenGAP definition. The manifest and DAG describe the workflow; the host supplies scheduling, scoped tools, and fresh isolated judge sessions. Packet scripts check consistency and declared gate state. They cannot prove truth or runtime isolation.

## Start

```bash
git clone https://github.com/b08x/sfl-writer-coordinator.git
cd sfl-writer-coordinator
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

Optional upstream CLI (Node 18+):

```bash
npm install -g @open-gitagent/opengap@0.5.0
opengap validate --dir . --compliance
opengap export --dir . --format system-prompt --output coordinator-prompt.md
```

The local validator checks every child, tool, skill, DAG reference, and SOD assignment against vendored upstream schemas. Upstream CLI validation alone does not cover all those relationships. See [validation](docs/validation.md) for checks actually executed in this migration.

## Repository

- Root agent.yaml, SOUL.md, RULES.md, PROMPT.md, DUTIES.md: coordinator identity, constraints, contracts, and single SOD policy.
- agents/<name>/: nine self-contained leaf roots, each with agent.yaml/SOUL.md/RULES.md/PROMPT.md and only its local skills/tools.
- workflows/review-cycle.yaml: one frozen candidate review DAG; authoring and the two-repair budget belong to the coordinator outside this cycle.
- tools/: three executable JSON packet wrappers; scripts/: retained CLI and stdio MCP implementations.
- schemas/: review contracts and pinned upstream OpenGAP schemas.
- knowledge/docs/review-protocol.md and skills/: protocol, writing templates, calibration references, and broker-only graph guidance.
- references/antigravity/: original source bytes, kept outside active discovery.

## Delegation and model tiers

| Agent | Duty | Preferred model | Declared tools |
|---|---|---|---|
| sfl-writer-coordinator | orchestrator | claude-opus-4-6 | prepare-blind, prepare-cross, check-final |
| sfl-writer-analytical-validator | advisor | claude-sonnet-4-6 | document-read |
| sfl-writer-collaborative-synthesizer | advisor | claude-sonnet-4-6 | document-read |
| sfl-writer-direct-executor | maker | claude-sonnet-4-6 | document-read, document-write |
| sfl-writer-docs-ideational-judge | ideational | claude-sonnet-4-6 | None |
| sfl-writer-docs-interpersonal-judge | interpersonal | claude-sonnet-4-6 | None |
| sfl-writer-docs-textual-judge | textual | claude-sonnet-4-6 | None |
| sfl-writer-evidence-broker | broker | claude-sonnet-4-6 | document-read |
| sfl-writer-pragmatic-realist | advisor | claude-haiku-4-5-20251001 | document-read |
| sfl-writer-socratic-inquirer | advisor | claude-haiku-4-5-20251001 | document-read |

All delegations are explicit. Only direct-executor edits document deliverables; no shell capability is declared. Author and advisors return handoff.schema.json; broker returns evidence-packet.schema.json; judges return judgment.schema.json. Every role receives explicit context. Full contracts are mirrored in SOUL.md for exporters that omit PROMPT.md.

## Host setup

Bind document-read/document-write interfaces to your host with explicit path scopes. Configure an existing codebase-memory MCP server on evidence-broker. Root review-packets uses python3 scripts/review_mcp.py from the repository root. Tool-free judges must receive inline packets in new sessions. Missing tools, graph freshness, or session isolation produces BLOCKED.

Read [runtime contract](docs/runtime-contract.md) before launching or exporting. Exports are format conversions; inspect the adapter before claiming it retains the nine-agent graph or enforces permissions. This package makes no Antigravity CLI dependency and requires no particular framework export.

See [migration mapping](docs/migration.md) for source provenance and schema differences. No document review, live model inference, graph retrieval, or external publication was performed by converting this repository.
