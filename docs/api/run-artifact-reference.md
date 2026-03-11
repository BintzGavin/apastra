---
title: "Run Artifact Specification Reference"
description: "Schema for a minimal BYO harness run artifact output."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/run-artifact.schema.json"
---

# Run Artifact Specification Reference

Schema for a minimal BYO harness run artifact output.

## Properties

## `manifest`

- **Type:** object
- **Requirement:** Required
- **Description:** Run manifest

### `input_refs`

- **Type:** object
- **Requirement:** Required

### `resolved_digests`

- **Type:** object
- **Requirement:** Required

### `timestamps`

- **Type:** object
- **Requirement:** Required

### `harness_version`

- **Type:** string
- **Requirement:** Required

### `model_ids`

- **Type:** array of string
- **Requirement:** Required

### `environment`

- **Type:** object
- **Requirement:** Required

### `status`

- **Type:** string
- **Requirement:** Required

## `scorecard`

- **Type:** object
- **Requirement:** Required
- **Description:** Run scorecard

### `normalized_metrics`

- **Type:** object
- **Requirement:** Required

### `metric_definitions`

- **Type:** object
- **Requirement:** Required

## `cases`

- **Type:** array of object
- **Requirement:** Required
- **Description:** Run cases

### `case_id`

- **Type:** string
- **Requirement:** Required

### `per_trial_outputs`

- **Type:** array of any
- **Requirement:** Required

### `evaluator_outputs`

- **Type:** array of any
- **Requirement:** Required

## `failures`

- **Type:** array of object
- **Requirement:** Required
- **Description:** Run failures
