# Runtime binding contract

This is a portable definition repository with executable packet helpers. It does not include an agent scheduler or a file-permission sandbox. OpenGAP 0.5.0 schema validation and an export do not establish those controls.

## Host requirements

1. Load the coordinator and all nine declared child roots. Each child has its own identity, rules, prompt contract, schemas embedded inline, and local skill/tool declarations. No tools, MCP, credentials, or conversation are inherited implicitly.
2. Bind document-read to supplied paths for advisors, author, and broker; bind document-write only for direct-executor, to explicit output paths. These YAML files are interfaces without an implementation; do not claim file operations work until the host binds them. They do not request shell access. On audit-only tasks deny all document writes.
3. Configure codebase-memory MCP on evidence-broker only. No endpoint or credential is shipped. Permit its listed read-only operations; deny graph administration and unrelated MCP. The root has only the local packet MCP service. Judges have neither MCP nor file tools.
4. Launch review-packets with the repository as working directory, or use an absolute scripts/review_mcp.py argument. Python must have requirements.txt dependencies. The MCP server keeps prepare_blind/prepare_cross/check_final names. OpenGAP script tools expose prepare-blind/prepare-cross/check-final with identical JSON argument shapes. Use one execution binding, not duplicate calls merely to obtain a second hash.
5. Schedule workflows/review-cycle.yaml in dependency order; the root model supplies gates. Resolve workflow expressions without eval. Tool steps wrap their raw JSON into outputs.packet, except check-final into outputs.result; judges map raw JSON to outputs.judgment; broker maps to outputs.packet; gates maps gate JSON to outputs.gates. The DAG declares these output names; the host supplies those envelopes. Map final acceptance.outputs.result to workflow result. Revisions restart the DAG, with at most two repair rounds outside it.
6. Every blind and cross judge invocation gets a NEW isolated conversation and only its inline packet. Tool-free judges cannot read schema paths, so their SOUL.md embeds the full judgment schema. Freeze all blind judgments before cross material is visible. Shared packet content is immutable for a cycle.
7. Parse one JSON object per response, validate its schema, and reject identity/role mismatches. Tools returning accepted=false must block acceptance even though transport succeeded. Missing capabilities return BLOCKED. Host configuration must not silently collapse roles into the coordinator.

## Models

Premium: claude-opus-4-6 for coordinator, with Sonnet fallback. Standard: claude-sonnet-4-6 for author, broker, judges, validator, and synthesizer, with Opus fallback. Fast: claude-haiku-4-5-20251001 for scoping and pragmatic advice, with Sonnet fallback. Each manifest declares its own tier; no model API requests were made. A host may need provider-specific IDs and may ignore fallback routing; verify the effective model in deployment.

These are explicit defaults, not claimed quality scores. Model IDs and lifecycle were checked against Anthropic model documentation on 2026-11-11: https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions and https://platform.claude.com/docs/en/about-claude/model-deprecations . No temperature is forced on models whose sampling support varies.

## Export limits

The pinned upstream system-prompt exporter loads SOUL.md, RULES.md, DUTIES.md, all local skills, always-load knowledge, and memory. It does not load PROMPT.md or recursively serialize all child instructions. Therefore operational output contracts are mirrored in each SOUL.md, and the protocol is always-load knowledge. Export each child separately or use an adapter with inspected recursive behavior. A single exported parent prompt cannot establish nine-agent execution or blind-session isolation.
