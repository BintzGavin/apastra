---
title: "Dataset Case Reference"
description: "Schema defining a single line of a JSONL dataset for evaluating prompt tests."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/dataset-case.schema.json"
---

# Dataset Case Reference

Schema defining a single line of a JSONL dataset for evaluating prompt tests.

## Properties

## `case_id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the specific test case.

## `inputs`

- **Type:** object
- **Requirement:** Required
- **Description:** Map of variable names to values, mapping to the variables required by the prompt spec.

## `expected_outputs`

- **Type:** object
- **Requirement:** Optional
- **Description:** Map of expected output values (e.g., exact matches, substrings).

## `assert`

- **Type:** array of object
- **Requirement:** Optional
- **Description:** Array of inline assertions to evaluate the case output against.

### `type`

- **Type:** string
- **Requirement:** Required
- **Description:** The type of assertion (e.g., contains, equals, regex, icontains).

### `value`

- **Type:** any
- **Requirement:** Required
- **Description:** The value or condition the output is asserted against.

## `metadata`

- **Type:** object
- **Requirement:** Optional
- **Description:** Arbitrary metadata for the specific test case (e.g., tags, difficulty, domain).

