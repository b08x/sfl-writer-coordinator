# sfl-writer — R.U.T.H. evidence review (0.3.0)

Primary agent: `sfl-writer-coordinator`. Includes 9 children: the original specialist roles, an evidence broker, and three metafunction judges. Only direct-executor edits document files. All models inherit the session model.

Requires an already configured codebase-memory MCP server. The plugin adds its own local review_packets MCP server using `python3` and `jsonschema`; ensure that interpreter has the dependency before installation, or change mcp_config.json's command to the absolute path of the appropriate Python environment. No endpoint, credentials, repository index, or dependencies are automatically installed.

Install this directory with `agy plugin install /absolute/path/to/sfl-writer`, or use the bundle's project installer. Use one route, not duplicate installations. Start a fresh CLI session, inspect /mcp, confirm `agy agents`, then run `agy --agent sfl-writer-coordinator`.

R.U.T.H. retrieves scoped evidence, delegates drafting, calls prepare_blind for a revision hash and restricted packet, runs three fresh blind judge sessions, obtains targeted broker evidence, calls prepare_cross, and delegates three fresh cross-examination sessions. Revisions repeat the affected cycle; two repair rounds maximum. check_final checks declared current judgments, evidence and five gates before acceptance. It checks consistency, not truth or conversation isolation.

Judges are tool-free; all draft/register/template/evidence inputs must be passed inline. Original advisors and authors disable MCP. R.U.T.H. and the broker inherit configured MCP/customizations, which can expose other servers; only broker graph use is routing policy, not enforced MCP tool isolation. No shell tools are configured. Host permissions remain authoritative. Missing graph or packet tools produce BLOCKED rather than invented verification.

The supplied codebase-memory and sfl-technical-writing skills are included, with original uploaded sources retained under references/originals/. The author uses the selected genre template; audit-only tasks do not edit documents. Optional boundary satire still requires an explicit request and a complete review of its candidate.

Use `agy plugin validate --strict /absolute/path/to/sfl-writer` on the target CLI. Packet schemas and helper implementation are self-contained in schemas/ and scripts/. See references/review-protocol.md for phase details. Native CLI discovery, MCP inheritance/enforcement, and model behavior remain untested here; actual offline and stdio fixture tests are reported in the parent bundle.
