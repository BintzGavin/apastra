---
title: "Quick Eval Reference"
description: "API reference for quick-eval schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/quick-eval.schema.json"
---

# Quick Eval Reference

Schema defining a combined quick evaluation file containing prompt, cases, and assertions.

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the quick eval.

### `prompt`
- **Type**: string
- **Presence**: **Required**
- **Description**: The prompt template.

### `cases`
- **Type**: array of reference ([dataset-case](./dataset-case-reference.md))
- **Presence**: **Required**
- **Description**: Array of dataset cases with inputs and inline asserts.

### `thresholds`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Optional thresholds for the evaluation.
