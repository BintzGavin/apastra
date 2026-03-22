---
title: "Harness Adapter"
description: ""
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/harness-adapter.schema.json"
---

# Harness Adapter



## Properties

### `id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Stable identifier for the harness adapter.

### `type`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Must be 'harness_adapter'.

### `capabilities`

- **Type:** `array`
- **Requirement:** Required
- **Description:** List of capabilities (e.g., ['run_suite', 'trials', 'model_matrix']).
- **Items Type:** `string`

### `entrypoint`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The CLI command or script to invoke the harness.

### `description`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Optional description of the harness adapter.

### `env_vars`

- **Type:** `array`
- **Requirement:** Optional
- **Description:** Required environment variables (e.g., 'OPENAI_API_KEY').
- **Items Type:** `string`

### `digest`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Content digest stored inline.
