# Input and output contract

Receive task_id, role, input_revision, assigned output_revision, document_revision, repository_revision, brief, sources/evidence, register, template, authorized output paths, and candidate text inline. Return exactly one JSON object under the schema below. Use your full declared agent name for role. Echo assigned revisions; never self-increment them. Advisors return draft=null; the author returns the complete candidate in draft, even when changes were written to authorized files. For audit-only tasks do not write. A SUCCEEDED handoff is not document acceptance. Host-bound file capabilities are narrow contracts, not installed permissions. No shell, network, MCP, delegation, or peer messaging is authorized.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string",
      "minLength": 1
    },
    "role": {
      "enum": [
        "sfl-writer-analytical-validator",
        "sfl-writer-collaborative-synthesizer",
        "sfl-writer-direct-executor",
        "sfl-writer-pragmatic-realist",
        "sfl-writer-socratic-inquirer"
      ]
    },
    "status": {
      "enum": [
        "SUCCEEDED",
        "NEEDS_REVISION",
        "BLOCKED",
        "FAILED"
      ]
    },
    "input_revision": {
      "type": "string"
    },
    "output_revision": {
      "type": "string"
    },
    "document_revision": {
      "type": "string"
    },
    "repository_revision": {
      "type": "string"
    },
    "summary": {
      "type": "string"
    },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "path",
          "purpose"
        ],
        "additionalProperties": false,
        "properties": {
          "path": {
            "type": "string"
          },
          "purpose": {
            "type": "string"
          }
        }
      }
    },
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "claim",
          "source_location"
        ],
        "additionalProperties": false,
        "properties": {
          "claim": {
            "type": "string"
          },
          "source_location": {
            "type": "string"
          }
        }
      }
    },
    "assumptions": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "required_actions": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "verdict": {
      "enum": [
        "PASS",
        "REVISE",
        "BLOCKED"
      ]
    },
    "draft": {
      "type": [
        "string",
        "null"
      ]
    }
  },
  "required": [
    "task_id",
    "role",
    "status",
    "input_revision",
    "output_revision",
    "document_revision",
    "repository_revision",
    "summary",
    "artifacts",
    "evidence",
    "assumptions",
    "blockers",
    "required_actions",
    "verdict",
    "draft"
  ]
}
```
