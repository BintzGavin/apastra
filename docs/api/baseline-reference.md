---
title: "Baseline Specification Reference"
description: "Current v3 schema and runtime semantics"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "promptops/schemas/baseline.schema.json"
---

# Baseline Specification Reference

run_path is resolved relative to the baseline record file, with parent segments permitted. Move record and evidence together preserving relative layout. Legacy absolute references remain readable. CI additionally requires the resolved run directory inside its checkout. Admission verifies suite_id and run_digest; names are immutable.

Schema identity: `apastra-baseline-v3`. The [schema source](../../promptops/schemas/baseline.schema.json) defines nested fields; [evaluation trust](../guides/evaluation-trust.md) defines admission checks beyond shape validation.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `baseline_id` | string | Yes | The baseline ID |
| `run_digest` | string | Yes | The run digest |
| `created_at` | string | Yes | The creation time |
| `metadata` | object | No | The metadata |
| `description` | string | No | The description |
| `run_path` | string | Yes | Run directory relative to this baseline record file; parent segments are permitted. Legacy absolute references remain readable. |
| `suite_id` | string | Yes |  |
