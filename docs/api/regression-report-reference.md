---
title: "Regression Report Specification Reference"
description: "Current v3 schema and runtime semantics"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "promptops/schemas/regression-report.schema.json"
---

# Regression Report Specification Reference

model_results holds authoritative per-model regression decisions. Top-level evidence contains descriptive pooled deltas. Any blocking model failure fails the report; a candidate failing its own thresholds also fails. Warnings exit nonzero.

Schema identity: `apastra-regression-report-v3`. The [schema source](../../promptops/schemas/regression-report.schema.json) defines nested fields; [evaluation trust](../guides/evaluation-trust.md) defines admission checks beyond shape validation.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `cost_delta` | number | No | The difference in total cost between the candidate and the baseline |
| `status` | enum | Yes |  |
| `baseline_ref` | string | Yes | The reference digest or ID |
| `candidate_ref` | string | Yes | The digest or ID being tested |
| `evidence` | array | Yes | Descriptive pooled metric deltas; per-model results determine the policy outcome. |
| `source_revision` | string / null | Yes |  |
| `suite_id` | string | Yes |  |
| `policy_digest` | string | Yes |  |
| `schema_version` | constant | Yes |  |
| `model_results` | object | Yes | Authoritative regression policy results for every requested model. |
