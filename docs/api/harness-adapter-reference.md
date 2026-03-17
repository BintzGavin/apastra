---
title: "Harness Adapter Reference"
description: "API reference for harness-adapter schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/harness-adapter.schema.json"
---

# Harness Adapter Reference

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the harness adapter.

### `type`
- **Type**: const (`harness_adapter`)
- **Presence**: **Required**
- **Description**: Must be 'harness_adapter'.

### `capabilities`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: List of capabilities (e.g., ['run_suite', 'trials', 'model_matrix']).

### `entrypoint`
- **Type**: string
- **Presence**: **Required**
- **Description**: The CLI command or script to invoke the harness.

### `description`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Optional description of the harness adapter.

### `env_vars`
- **Type**: array of string
- **Presence**: *Optional*
- **Description**: Required environment variables (e.g., 'OPENAI_API_KEY').

### `digest`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Content digest stored inline.
