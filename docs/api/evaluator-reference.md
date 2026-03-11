---
title: "Evaluator Specification Reference"
description: "Scoring definition (deterministic checks, schema validation, rubric/judge config)"
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/evaluator.schema.json"
---

# Evaluator Specification Reference

Scoring definition (deterministic checks, schema validation, rubric/judge config)

## Properties

## `id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the evaluator.

## `type`

- **Type:** string
- **Requirement:** Required
- **Description:** The type of the evaluator.
- **Allowed Values:** deterministic, schema, judge

## `metrics`

- **Type:** array of string
- **Requirement:** Required
- **Description:** Array of metrics produced by this evaluator.

## `description`

- **Type:** string
- **Requirement:** Optional
- **Description:** Optional human-readable description of the evaluator.

## `config`

- **Type:** object
- **Requirement:** Optional
- **Description:** Configuration specific to the evaluator type, such as model details or target values.

## `digest`

- **Type:** string
- **Requirement:** Optional
- **Description:** SHA-256 hash of the evaluator content.
