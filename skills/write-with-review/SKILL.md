---
name: write-with-review
description: Coordinate evidence-backed SFL writing with a sole author, evidence broker, three independent blind metafunction audits, and revision-bound cross-examination.
---

# Write with review

Use the root sfl-writer-coordinator identity and declared child roster. Load SOUL.md, RULES.md, DUTIES.md, PROMPT.md, knowledge/docs/review-protocol.md, and workflows/review-cycle.yaml from the agent repository root. This module grants no tools, role identity, file access, or isolation.

1. Establish brief, scope, task type, repository revision, register, template, output paths, and acceptance criteria.
2. Obtain an actual planning hash with prepare_blind, route evidence retrieval to evidence-broker, and route authorized drafting only to direct-executor. Audit-only tasks retain the supplied draft without writes. Optional advisors return structured handoffs.
3. Freeze the candidate with prepare_blind. Send the same inline restricted packet to three fresh tool-free judge sessions. Freeze all blind responses before sharing peer findings.
4. Request candidate-bound evidence from the broker, call prepare_cross, and send the shared packet to three fresh cross-examination sessions.
5. Adjudicate; use the author for revisions and restart the cycle for changed candidates. Maximum two repair rounds across the whole task.
6. Assemble five current gates and call check_final. Deliver actual acceptance or PARTIAL/BLOCKED with reasons, ledger, identities, and limits.

Never substitute yourself for a missing role. Evidence agreement is not factual verification; helper checks establish declared packet consistency. Missing tools, source/index access, or fresh isolated sessions block the affected transition. The portable DAG needs a host scheduler; this skill is not one.
