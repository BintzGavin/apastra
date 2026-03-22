---
title: "Run Request Specification"
description: "Schema for a minimal BYO harness run request."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/run-request.schema.json"
---

# Run Request Specification

Schema for a minimal BYO harness run request.

## Properties

### `suite_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The benchmark suite ID

### `revision_ref`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The revision ref (SHA/tag/digest)

### `model_matrix`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Model matrix
- **Items Type:** `string`

### `evaluator_refs`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Evaluator references
- **Items Type:** `string`

### `trials`

- **Type:** `integer`
- **Requirement:** Optional
- **Description:** Number of trials

### `budgets`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Budgets

### `timeouts`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Timeouts

### `artifact_backend_config`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Artifact backend config
