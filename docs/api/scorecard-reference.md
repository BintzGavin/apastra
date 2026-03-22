---
title: "Scorecard Specification"
description: "Schema for the run artifact scorecard."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/scorecard.schema.json"
---

# Scorecard Specification

Schema for the run artifact scorecard.

## Properties

### `normalized_metrics`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Mapping of metric names to their values

### `metric_definitions`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Metadata like metric version and description

### `variance`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Optional variance details if trials were run

### `flake_rates`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Mapping of metric names to their flake rates
