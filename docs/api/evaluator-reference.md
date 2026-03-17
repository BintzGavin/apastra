---
title: "Evaluator Reference"
description: "API reference for evaluator schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/evaluator.schema.json"
---

# Evaluator Reference

Scoring definition (deterministic checks, schema validation, rubric/judge config)

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the evaluator.

### `type`
- **Type**: enum (`deterministic`, `schema`, `judge`, `human`)
- **Presence**: **Required**
- **Description**: The type of the evaluator.

### `metrics`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Array of metrics produced by this evaluator.

### `description`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Optional human-readable description of the evaluator.

### `config`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Configuration specific to the evaluator type, such as model details or target values.

### `metric_versions`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Mapping of metric names to their semantic versions.

### `digest`
- **Type**: string
- **Presence**: *Optional*
- **Description**: SHA-256 hash of the evaluator content.
