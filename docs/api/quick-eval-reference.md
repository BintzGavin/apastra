---
title: "Quick Eval"
description: "Schema defining a combined quick evaluation file containing prompt, cases, and assertions."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/quick-eval.schema.json"
---

# Quick Eval

Schema defining a combined quick evaluation file containing prompt, cases, and assertions.

## Properties

### `id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Stable identifier for the quick eval.

### `prompt`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The prompt template.

### `cases`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Array of dataset cases with inputs and inline asserts.
- **Items Type:** `any`

### `thresholds`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Optional thresholds for the evaluation.
