---
title: "Suite Reference"
description: "API reference for suite schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/suite.schema.json"
---

# Suite Reference

Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the suite.

### `name`
- **Type**: string
- **Presence**: **Required**
- **Description**: Human-readable name of the suite.

### `description`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Optional detailed description of the suite's purpose.

### `datasets`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Array of dataset references.

### `evaluators`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Array of evaluator references.

### `model_matrix`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Array of model/provider identifiers to run the suite against.

### `trials`
- **Type**: integer
- **Presence**: *Optional*
- **Description**: Number of times to run the evaluation.

### `budgets`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Cost or time limits for the execution.

### `budgets.cost`
- **Type**: number
- **Presence**: *Optional*
- **Description**: Maximum allowed cost in dollars.

### `budgets.time`
- **Type**: integer
- **Presence**: *Optional*
- **Description**: Maximum allowed execution time in seconds.

### `thresholds`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Pass/fail criteria mapped to specific metrics.
