---
title: "Run Request Specification Reference"
description: "Schema for a minimal BYO harness run request."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/run-request.schema.json"
---

# Run Request Specification Reference

Schema for a minimal BYO harness run request.

## Properties

## `suite_id`

- **Type:** string
- **Requirement:** Required
- **Description:** The benchmark suite ID

## `revision_ref`

- **Type:** string
- **Requirement:** Required
- **Description:** The revision ref (SHA/tag/digest)

## `model_matrix`

- **Type:** array of string
- **Requirement:** Required
- **Description:** Model matrix

## `evaluator_refs`

- **Type:** array of string
- **Requirement:** Required
- **Description:** Evaluator references

## `trials`

- **Type:** integer
- **Requirement:** Optional
- **Description:** Number of trials

## `budgets`

- **Type:** object
- **Requirement:** Optional
- **Description:** Budgets

## `timeouts`

- **Type:** object
- **Requirement:** Optional
- **Description:** Timeouts

## `artifact_backend_config`

- **Type:** object
- **Requirement:** Optional
- **Description:** Artifact backend config

