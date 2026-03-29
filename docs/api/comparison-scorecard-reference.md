---
title: "Comparison Scorecard Specification Reference"
description: "Schema for multi-model evaluation scorecards with cost/quality/latency tradeoffs."
audience: "developers | platform-teams | agents"
last_verified: "2024-05-24"
source_files:
  - "promptops/schemas/comparison-scorecard.schema.json"
---

# Comparison Scorecard Specification Reference

Schema for multi-model evaluation scorecards with cost/quality/latency tradeoffs.

## Schema Details

### `id`

- **Type**: string
- **Required**: Yes
- **Description**: Unique identifier for this comparison scorecard

### `suite_id`

- **Type**: string
- **Required**: Yes
- **Description**: Reference to the evaluation suite

### `baselines`

- **Type**: array of string
- **Required**: Yes
- **Description**: List of baseline models

### `models`

- **Type**: array of string
- **Required**: Yes
- **Description**: List of candidate models evaluated

### `metrics`

- **Type**: object
- **Required**: Yes
- **Description**: Per-model metric breakdown

### `comparison_tradeoffs`

- **Type**: object
- **Required**: Yes
- **Description**: Tradeoff comparisons between models
