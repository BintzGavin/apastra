---
title: "Regression Policy Reference"
description: "API reference for regression-policy schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/regression-policy.schema.json"
---

# Regression Policy Reference

Schema for regression policy definition.

## Properties

### `baseline`
- **Type**: string
- **Presence**: **Required**
- **Description**: Baseline reference rules, e.g., 'prod current'

### `rules`
- **Type**: array of object
- **Presence**: **Required**
- **Description**: List of per-metric rules

### `rules[].metric`
- **Type**: string
- **Presence**: **Required**
- **Description**: Metric to evaluate

### `rules[].floor`
- **Type**: number
- **Presence**: *Optional*
- **Description**: Absolute floor value

### `rules[].allowed_delta`
- **Type**: number
- **Presence**: *Optional*
- **Description**: Allowed delta from baseline

### `rules[].direction`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Directionality, e.g., 'higher_is_better'

### `rules[].severity`
- **Type**: enum (`blocker`, `warning`)
- **Presence**: **Required**
- **Description**: Severity of rule failure
