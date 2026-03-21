---
title: "Consumption Manifest Schema"
description: "Schema for the apastra PromptOps consumption manifest."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/consumption-manifest.schema.json"
---

# Consumption Manifest Schema

Schema for the apastra PromptOps consumption manifest.

## Properties

## `version`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Version of the consumption manifest.

## `prompts`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Mapping of local names to resolution configurations.

## `defaults`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Global fallbacks like default model or provider.
