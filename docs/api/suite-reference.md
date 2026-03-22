---
title: "Benchmark Suite Specification"
description: "Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/suite.schema.json"
---

# Benchmark Suite Specification

Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.

## Properties

### `id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Stable identifier for the suite.

### `name`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Human-readable name of the suite.

### `description`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Optional detailed description of the suite's purpose.

### `datasets`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Array of dataset references.
- **Items Type:** `string`

### `evaluators`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Array of evaluator references.
- **Items Type:** `string`

### `model_matrix`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Array of model/provider identifiers to run the suite against.
- **Items Type:** `string`

### `trials`

- **Type:** `integer`
- **Requirement:** Optional
- **Description:** Number of times to run the evaluation.

### `budgets`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Cost or time limits for the execution.

### `thresholds`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Pass/fail criteria mapped to specific metrics.
