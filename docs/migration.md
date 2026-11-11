# Antigravity to OpenGAP

Source: uploaded sfl-writer.zip, plugin 0.3.0; SHA-256 866e4019a6d2a1100389d5bce7e1a816443435f7b8b5f27c12c2f1207cd7e17e.
Destination baseline: b08x/sfl-writer-coordinator commit bb8c99b818801c0f863cb3e858f2f3fdf898e332 (starter scaffolding).
OpenGAP source/schema pin: d7a8e2edb54b942d6b4635cdd8b919ebd23e5da5, package version 0.5.0, spec_version 0.1.0.

| Antigravity | OpenGAP |
|---|---|
| plugin.json | Root agent.yaml and README.md |
| agents/sfl-writer-coordinator.md | Root SOUL.md, RULES.md, PROMPT.md, DUTIES.md |
| Nine agents/*.md frontmatter | agents/<original-name>/agent.yaml |
| Role system prompts | Each child SOUL.md; explicit PROMPT.md output contract |
| invoke_subagent / lifecycle tool names | Host-bound delegation, mode explicit |
| mcp_config.json review_packets | Root mcp_servers.review-packets plus OpenGAP script tool wrappers |
| inheritMcp/inheritCustomizations flags | Explicit host isolation requirements; no invented manifest equivalents |
| Author write_to_file/replace_file_content | Host-bound document-write interface, author only |
| view_file | Host-bound document-read interface |
| Scripts and packet schemas | Preserved implementation and schemas; regression tests added |
| Session-inherited models | Explicit premium/standard/fast tiers selected by user |
| Boundary-only role references | Removed from active writer protocol; original remains archived |
| user-invocable skill metadata | Removed from active Agent Skills frontmatter; original remains archived |

All original source files are byte-preserved under references/antigravity/ for provenance, outside active agent and skill discovery. They are historical data, not active runtime instructions. The nine specialist names, SFL lenses, judgment classes, five gates, hash binding, and two-repair limit are retained. Template-only compliance claims, no-op hooks, example skill, and empty memory configuration were removed. No license is inferred from uploaded content; upstream schemas retain their upstream MIT license separately.

The schema is authoritative over the README examples: delegation is explicit (not manual); workflow steps are arrays with id/action; failures use on_step_failure; compliance tier is standard (not medium). SOD role permissions use the upstream enum. The SOD policy lives once in agent.yaml; DUTIES.md explains its operational boundary.
