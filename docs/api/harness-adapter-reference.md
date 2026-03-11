---
title: "Harness Adapter Reference"
description: "API reference for Harness Adapter"
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/harness-adapter.schema.json"
---

# Harness Adapter Reference

API reference for Harness Adapter

## Properties

## `id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the harness adapter.

## `type`

- **Type:** string
- **Requirement:** Required
- **Description:** Must be 'harness_adapter'.

## `capabilities`

- **Type:** array of string
- **Requirement:** Required
- **Description:** List of capabilities (e.g., ['run_suite', 'trials', 'model_matrix']).

## `entrypoint`

- **Type:** string
- **Requirement:** Required
- **Description:** The CLI command or script to invoke the harness.

## `description`

- **Type:** string
- **Requirement:** Optional
- **Description:** Optional description of the harness adapter.

## `env_vars`

- **Type:** array of string
- **Requirement:** Optional
- **Description:** Required environment variables (e.g., 'OPENAI_API_KEY').

## `digest`

- **Type:** string
- **Requirement:** Optional
- **Description:** Content digest stored inline.
