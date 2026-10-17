---
title: "Harness Adapter Reference"
description: "Current v3 schema and runtime semantics"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "promptops/schemas/harness-adapter.schema.json"
---

# Harness Adapter Reference

implementation.files optionally pins raw SHA-256 file bytes relative to this config directory. Runtime admission rejects absolute paths, traversal, symlinks, missing files and changed hashes. Files are checked before/after execution and on admission. This is not dependency closure or authentication; without pins the invocation explicitly records configuration_only.

Schema identity: `apastra-harness-adapter-v3`. The [schema source](../../promptops/schemas/harness-adapter.schema.json) defines nested fields; [evaluation trust](../guides/evaluation-trust.md) defines admission checks beyond shape validation.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | string | Yes | Stable identifier for the harness adapter. |
| `type` | string | Yes | Must be 'harness_adapter'. |
| `capabilities` | array | Yes | List of capabilities (e.g., ['run_suite', 'trials', 'model_matrix']). |
| `entrypoint` | string | Yes | The CLI command or script to invoke the harness. |
| `description` | string | No | Optional description of the harness adapter. |
| `env_vars` | array | No | Required environment variables (e.g., 'OPENAI_API_KEY'). |
| `digest` | string | No | Content digest stored inline. |
| `extensions` | object | No |  |
| `execution_mode` | enum | Yes |  |
| `version` | string | No |  |
| `implementation` | object | No | Optional raw content pins for explicitly declared local files; does not describe dependency closure or authenticity. |
