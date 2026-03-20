---
title: "Regression Policy Specification Reference"
description: "Schema for regression policy definition."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/regression-policy.schema.json"
---

# Regression Policy Specification Reference

Schema for regression policy definition.

## Properties

## `baseline`

- **Type:** string
- **Requirement:** Required
- **Description:** Baseline reference rules, e.g., 'prod current'

## `rules`

- **Type:** array of object
- **Requirement:** Required
- **Description:** List of per-metric rules

### `metric`

- **Type:** string
- **Requirement:** Required
- **Description:** Metric to evaluate

### `floor`

- **Type:** number
- **Requirement:** Optional
- **Description:** Absolute floor value

### `allowed_delta`

- **Type:** number
- **Requirement:** Optional
- **Description:** Allowed delta from baseline

### `direction`

- **Type:** string
- **Requirement:** Optional
- **Description:** Directionality, e.g., 'higher_is_better'

### `severity`

- **Type:** string
- **Requirement:** Required
- **Description:** Severity of rule failure
- **Allowed Values:** blocker, warning

