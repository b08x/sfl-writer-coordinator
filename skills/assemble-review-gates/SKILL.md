---
name: assemble-review-gates
description: Assemble the five revision-bound linguistic gates from current cross-examination judgments and evidence without drafting or restarting the review.
---

# Assemble review gates

This is the coordinator's bounded gates step, not the full writing workflow. Accept the current cross packet and all three current cross judgments. Validate schema, roster, document/repository/draft identities, and evidence digest first. Do not retrieve, delegate, edit the candidate, or start a new cycle from this step.

Return one JSON object conforming to schemas/gates.schema.json: task_id, document_revision, repository_revision, draft_sha256, evidence_sha256, and gates. The five keys are process_coverage, modality, cohesion, connectives, and negative_capability. Each value has status (PASS, REVISE, BLOCKED, or NOT_APPLICABLE) and a nonempty reason with the relevant finding/evidence references in that reason.

Map sustained/deadlocked ideational concerns to process_coverage; interpersonal concerns to modality or negative_capability; textual concerns to cohesion or connectives according to the actual finding. Do not mechanically pass a gate from a missing finding. Explain each assessment from current judgments, draft, and evidence. A material unresolved evidence requirement blocks the relevant gate; an applicable writing defect requires revision. NOT_APPLICABLE needs a scope-based reason and cannot conceal a retained unsupported claim. Missing inputs require BLOCKED. No source count or measurement may be invented to satisfy a template.

Echo all supplied identities and the evidence digest; do not compute replacement values. Return the JSON to the host as outputs.gates. The separate check-final step determines packet consistency and declared acceptance.
