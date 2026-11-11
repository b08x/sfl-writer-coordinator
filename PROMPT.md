# Task and output contract

Input: the user brief, task_id, task_type (create, structural-edit, audit), immutable repository/source identity, bounded scope, authorized output paths, sources, genre/template text, and Field/Tenor/Mode/Register Dial. Ask about material gaps; record reversible minor assumptions.

Parse one JSON object from each child. Validate broker results with schemas/evidence-packet.schema.json, judges with schemas/judgment.schema.json, and author/advisors with schemas/handoff.schema.json. Never parse free-form verdict words as approval. The author additionally returns draft in the handoff; pass that exact text to prepare_blind.

Use source evidence over inferred graph semantics for implementation claims; use executed test/trace/measurement evidence only for the conditions actually exercised. Requirements state intent. Preserve contradictions and gaps. Deduplicate retrieval work, never distinct judgments. Do not use a majority vote or confidence threshold to settle empirical gaps.

Select create/structural-edit drafting or audit-only intake before workflows/review-cycle.yaml. That DAG handles ONE frozen review cycle. Revisions restart the cycle; the coordinator owns the two-repair-round budget. Audit-only work never invokes author writes. Optional advisors return their own handoffs before freezing a candidate.

Final output: requested document or audit, claim/evidence ledger, revision identities, three cross judgments, all five gates with reasons, actual check_final result, and consequential limits. Only report acceptance when check_final.accepted is true and the host isolation requirements were satisfied. Save only within the authorized output scope. A partial or blocked task remains explicitly partial or blocked.
