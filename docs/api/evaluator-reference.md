---
title: "Evaluator Specification"
description: "Scoring definition (deterministic checks, schema validation, rubric/judge config)"
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/evaluator.schema.json"
---

# Evaluator Specification

Scoring definition (deterministic checks, schema validation, rubric/judge config)

## Properties

### `id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Stable identifier for the evaluator.

### `type`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The type of the evaluator.
- **Allowed Values:** `deterministic`, `schema`, `judge`, `human`

### `metrics`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Array of metrics produced by this evaluator.
- **Items Type:** `string`

### `description`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Optional human-readable description of the evaluator.

### `config`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Configuration specific to the evaluator type, such as model details or target values.

### `metric_versions`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Mapping of metric names to their semantic versions.

### `digest`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** SHA-256 hash of the evaluator content.
