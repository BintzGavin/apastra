---
title: "Prompt Spec Reference"
description: "API reference for prompt-spec schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/prompt-spec.schema.json"
---

# Prompt Spec Reference

Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the prompt (e.g., 'my-app/summarize-v1').

### `variables`
- **Type**: object
- **Presence**: **Required**
- **Description**: Map of variable names to their JSON Schema types (e.g., {'text': {'type': 'string'}}).

### `template`
- **Type**: string or object or array
- **Presence**: **Required**
- **Description**: The prompt template content (e.g., Jinja2 string, or array of message objects for chat models).

### `output_contract`
- **Type**: object
- **Presence**: *Optional*
- **Description**: JSON Schema defining the expected output structure from the model.

### `metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Arbitrary key-value pairs (e.g., author, intent, tags).

### `tool_contract`
- **Type**: object
- **Presence**: *Optional*
- **Description**: JSON Schema defining the expected tool calling structure and available tools.
