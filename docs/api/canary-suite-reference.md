---
title: "Canary Suite Specification Reference"
description: "Canary benchmark suite declaring schedule, alerts, datasets, evaluators, model/provider matrix, trials, budgets, and thresholds."
audience: "developers | platform-teams | agents"
last_verified: "2024-05-24"
source_files:
  - "promptops/schemas/canary-suite.schema.json"
---

# Canary Suite Specification Reference

Canary benchmark suite declaring schedule, alerts, datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.

## Schema Details

### `id`

- **Type**: string
- **Required**: Yes
- **Description**: Stable identifier for the canary suite.

### `name`

- **Type**: string
- **Required**: Yes
- **Description**: Human-readable name of the canary suite.

### `description`

- **Type**: string
- **Required**: No
- **Description**: Optional detailed description of the canary suite's purpose.

### `schedule`

- **Type**: string
- **Required**: Yes
- **Description**: Cron string defining the schedule for execution.

### `alert`

- **Type**: object
- **Required**: No
- **Description**: Notification routing for alerts upon threshold failure or drift detection.

### `datasets`

- **Type**: array of string
- **Required**: Yes
- **Description**: Array of dataset references.

### `evaluators`

- **Type**: array of string
- **Required**: Yes
- **Description**: Array of evaluator references.

### `model_matrix`

- **Type**: array of string
- **Required**: Yes
- **Description**: Array of model/provider identifiers to run the canary suite against.

### `trials`

- **Type**: integer
- **Required**: No
- **Description**: Number of times to run the evaluation.

### `budgets`

- **Type**: object
- **Required**: No
- **Description**: Cost or time limits for the execution.

### `thresholds`

- **Type**: object
- **Required**: No
- **Description**: Pass/fail criteria mapped to specific metrics.
