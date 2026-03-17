---
title: "Run Request Reference"
description: "API reference for run-request schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/run-request.schema.json"
---

# Run Request Reference

Schema for a minimal BYO harness run request.

## Properties

### `suite_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: The benchmark suite ID

### `revision_ref`
- **Type**: string
- **Presence**: **Required**
- **Description**: The revision ref (SHA/tag/digest)

### `model_matrix`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Model matrix

### `evaluator_refs`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Evaluator references

### `trials`
- **Type**: integer
- **Presence**: *Optional*
- **Description**: Number of trials

### `budgets`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Budgets

### `timeouts`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Timeouts

### `artifact_backend_config`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Artifact backend config
