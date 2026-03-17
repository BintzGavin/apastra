---
title: "Run Artifact Reference"
description: "API reference for run-artifact schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/run-artifact.schema.json"
---

# Run Artifact Reference

Schema for a minimal BYO harness run artifact output.

## Properties

### `manifest`
- **Type**: object
- **Presence**: **Required**
- **Description**: Run manifest

### `manifest.input_refs`
- **Type**: object
- **Presence**: **Required**

### `manifest.resolved_digests`
- **Type**: object
- **Presence**: **Required**

### `manifest.timestamps`
- **Type**: object
- **Presence**: **Required**

### `manifest.harness_identifier`
- **Type**: string
- **Presence**: **Required**

### `manifest.harness_version`
- **Type**: string
- **Presence**: **Required**

### `manifest.model_ids`
- **Type**: array of string
- **Presence**: **Required**

### `manifest.sampling_config`
- **Type**: object
- **Presence**: **Required**

### `manifest.environment`
- **Type**: object
- **Presence**: **Required**

### `manifest.status`
- **Type**: string
- **Presence**: **Required**

### `scorecard`
- **Type**: object
- **Presence**: **Required**
- **Description**: Run scorecard

### `scorecard.normalized_metrics`
- **Type**: object
- **Presence**: **Required**

### `scorecard.metric_definitions`
- **Type**: object
- **Presence**: **Required**

### `cases`
- **Type**: array of object
- **Presence**: **Required**
- **Description**: Run cases

### `cases[].case_id`
- **Type**: string
- **Presence**: **Required**

### `cases[].per_trial_outputs`
- **Type**: array
- **Presence**: **Required**

### `cases[].evaluator_outputs`
- **Type**: array
- **Presence**: **Required**

### `failures`
- **Type**: array of object
- **Presence**: **Required**
- **Description**: Run failures
