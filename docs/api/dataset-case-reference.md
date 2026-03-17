---
title: "Dataset Case Reference"
description: "API reference for dataset-case schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/dataset-case.schema.json"
---

# Dataset Case Reference

Schema defining a single line of a JSONL dataset for evaluating prompt tests.

## Properties

### `case_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the specific test case.

### `inputs`
- **Type**: object
- **Presence**: **Required**
- **Description**: Map of variable names to values, mapping to the variables required by the prompt spec.

### `expected_outputs`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Map of expected output values (e.g., exact matches, substrings).

### `assert`
- **Type**: array of object
- **Presence**: *Optional*
- **Description**: Array of inline assertions to evaluate the case output against.

### `assert[].type`
- **Type**: string
- **Presence**: **Required**
- **Description**: The type of assertion (e.g., contains, equals, regex, icontains).

### `assert[].value`
- **Type**: any
- **Presence**: **Required**
- **Description**: The value or condition the output is asserted against.

### `metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Arbitrary metadata for the specific test case (e.g., tags, difficulty, domain).
