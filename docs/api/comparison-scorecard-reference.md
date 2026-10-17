---
title: "Comparison Scorecard Specification Reference"
description: "Current v3 schema and runtime semantics"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "promptops/schemas/comparison-scorecard.schema.json"
---

# Comparison Scorecard Specification Reference

Complete comparisons retain pass, fail and not_evaluated measurements. model_results holds authoritative per-model threshold decisions; execution_status is completed only when every requested model produced valid evidence. Missing or invalid evidence is an error, not a completed comparison.

Schema identity: `apastra-comparison-scorecard-v3`. The [schema source](../../promptops/schemas/comparison-scorecard.schema.json) defines nested fields; [evaluation trust](../guides/evaluation-trust.md) defines admission checks beyond shape validation.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `suite_id` | string | Yes | Reference to the evaluation suite |
| `models` | array | Yes | List of candidate models evaluated |
| `metrics` | object | Yes | Per-model metric breakdown |
| `comparison_tradeoffs` | object | Yes | Tradeoff comparisons between models |
| `status` | enum | Yes |  |
| `runs` | object | Yes |  |
| `total_cost` | number | No |  |
| `schema_version` | constant | Yes |  |
| `execution_status` | constant | Yes |  |
| `model_results` | object | Yes | Authoritative per-model threshold policy results. |
