---
title: "Scorecard Reference"
description: "API reference for scorecard schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/scorecard.schema.json"
---

# Scorecard Reference

Schema for the run artifact scorecard.

## Properties

### `normalized_metrics`
- **Type**: object
- **Presence**: **Required**
- **Description**: Mapping of metric names to their values

### `metric_definitions`
- **Type**: object
- **Presence**: **Required**
- **Description**: Metadata like metric version and description

### `metric_definitions.<additional>.version`
- **Type**: string
- **Presence**: **Required**

### `metric_definitions.<additional>.description`
- **Type**: string
- **Presence**: *Optional*

### `variance`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Optional variance details if trials were run

### `flake_rates`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Mapping of metric names to their flake rates
