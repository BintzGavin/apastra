---
title: "Community Prompt Pack"
description: "Curated starter packs like summarization, extraction to bootstrap the registry."
audience: "all"
last_verified: "2026-04-01"
source_files:
  - "promptops/schemas/community-prompt-pack.schema.json"
---

# Community Prompt Pack

Curated starter packs like summarization, extraction to bootstrap the registry.

## Properties

### `id` (Required)

**Type:** `string`

Stable identifier.

### `name` (Required)

**Type:** `string`

Human-readable name.

### `description` (Required)

**Type:** `string`

Purpose of the pack.

### `custodian` (Required)

**Type:** `string`

The custodian org managing it.

### `prompts` (Optional)

**Type:** `array`

References to the prompt files in the pack.

### `datasets` (Optional)

**Type:** `array`

References to the dataset files in the pack.

### `evaluators` (Optional)

**Type:** `array`

References to the evaluator files in the pack.

### `suites` (Optional)

**Type:** `array`

References to the suite files in the pack.

### `baselines` (Optional)

**Type:** `array`

References to the baseline files in the pack.

### `topics` (Optional)

**Type:** `array`

Topics like summarization, extraction, classification, code review.
