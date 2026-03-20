---
title: "Prompt Specification Reference"
description: "Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/prompt-spec.schema.json"
---

# Prompt Specification Reference

Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.

## Properties

## `id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the prompt (e.g., 'my-app/summarize-v1').

## `variables`

- **Type:** object
- **Requirement:** Required
- **Description:** Map of variable names to their JSON Schema types (e.g., {'text': {'type': 'string'}}).

## `template`

- **Type:** ['string', 'object', 'array']
- **Requirement:** Required
- **Description:** The prompt template content (e.g., Jinja2 string, or array of message objects for chat models).

## `output_contract`

- **Type:** object
- **Requirement:** Optional
- **Description:** JSON Schema defining the expected output structure from the model.

## `metadata`

- **Type:** object
- **Requirement:** Optional
- **Description:** Arbitrary key-value pairs (e.g., author, intent, tags).

## `tool_contract`

- **Type:** object
- **Requirement:** Optional
- **Description:** JSON Schema defining the expected tool calling structure and available tools.

