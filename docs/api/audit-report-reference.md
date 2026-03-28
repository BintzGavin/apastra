---
title: "Audit Report Schema"
description: "Schema for an audit report detailing untested and unversioned prompts."
audience: "all"
last_verified: "2024-03-28"
source_files:
  - "promptops/schemas/audit-report.schema.json"
---

# Audit Report Schema

Schema for an audit report detailing untested and unversioned prompts.

## Properties

### `timestamp` (Required)

**Type:** `string`

### `scanned_paths` (Required)

**Type:** `array`

### `total_prompts` (Required)

**Type:** `integer`

### `untested_prompts` (Optional)

**Type:** `integer`

### `unversioned_prompts` (Optional)

**Type:** `integer`

### `severity_score` (Required)

**Type:** `unknown`

### `findings` (Required)

**Type:** `array`
