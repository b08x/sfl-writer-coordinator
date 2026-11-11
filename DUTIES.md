# Duties

The manifest contains the single machine-readable SOD policy. This file explains that policy.

Only direct-executor authors document deliverables. Only evidence-broker retrieves graph evidence. Each metafunction has a distinct judge; the coordinator adjudicates and delivers but cannot substitute for an author, broker, or judge. Advisors cannot approve the document. Acceptance requires all three current cross judgments plus evidence and packet-gate acceptance.

`enforcement: advisory` describes this portable package honestly: no scheduler, permission sandbox, or credential provisioning is installed by a manifest. For deployment, require fresh isolated judge sessions, inline-only judge inputs, no judge tools/MCP, scoped author writes, and broker-only graph transport. If the host cannot satisfy these requirements, the affected review is BLOCKED. Merely changing enforcement to strict does not create those controls.

Host credentials must remain separate from tool-free judge contexts. Shared evidence is supplied only at cross-examination. The sole-author role cannot receive checker authority. Code changes, publication, external messaging, graph mutation, and dependency installation are outside a documentation task unless separately authorized.
