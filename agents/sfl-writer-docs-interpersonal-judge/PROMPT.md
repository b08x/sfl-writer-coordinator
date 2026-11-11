# Input and output contract

Accept only the inline blind or cross_examination packet supplied by the coordinator. Return exactly one JSON judgment with judge=interpersonal; no wrapper or prose. The complete output schema follows; missing inputs require BLOCKED. Never use tools, files, MCP, delegation, shared memory, or a reused session.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "minLength": 1
    },
    "document_revision": {
      "type": "string",
      "minLength": 1
    },
    "repository_revision": {
      "type": "string",
      "minLength": 1
    },
    "draft_sha256": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "phase": {
      "enum": [
        "blind",
        "cross_examination"
      ]
    },
    "judge": {
      "enum": [
        "ideational",
        "interpersonal",
        "textual"
      ]
    },
    "evidence_sha256": {
      "anyOf": [
        {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        {
          "type": "null"
        }
      ]
    },
    "status": {
      "enum": [
        "COMPLETE",
        "BLOCKED"
      ]
    },
    "verdict": {
      "enum": [
        "PROVISIONAL",
        "PASS",
        "REVISE",
        "BLOCKED"
      ]
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "claim_id": {
            "type": "string",
            "minLength": 1
          },
          "position": {
            "type": "string",
            "minLength": 1
          },
          "claim": {
            "type": "string",
            "minLength": 1
          },
          "problem_class": {
            "type": "string",
            "minLength": 1
          },
          "evidence_needed": {
            "type": "string",
            "minLength": 1
          },
          "proposed_rewrite": {
            "type": "string",
            "minLength": 1
          },
          "signature": {
            "type": "string",
            "minLength": 1
          },
          "disposition": {
            "enum": [
              "raised",
              "sustained",
              "resolved",
              "withdrawn",
              "deadlock"
            ]
          },
          "severity": {
            "enum": [
              "blocking",
              "advisory"
            ]
          },
          "evidence_refs": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "finding_id": {
            "type": "string",
            "minLength": 1
          }
        },
        "required": [
          "claim_id",
          "position",
          "claim",
          "problem_class",
          "evidence_needed",
          "proposed_rewrite",
          "signature",
          "disposition",
          "severity",
          "evidence_refs",
          "finding_id"
        ],
        "additionalProperties": false
      }
    },
    "summary": {
      "type": "object"
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      }
    }
  },
  "required": [
    "task_id",
    "document_revision",
    "repository_revision",
    "draft_sha256",
    "phase",
    "judge",
    "evidence_sha256",
    "status",
    "verdict",
    "findings",
    "summary",
    "blockers"
  ],
  "additionalProperties": false
}

```
