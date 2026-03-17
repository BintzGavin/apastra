---
title: "Consumption Manifest Reference"
description: "API reference for consumption-manifest schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/consumption-manifest.schema.json"
---

# Consumption Manifest Reference

Schema for the apastra PromptOps consumption manifest.

## Properties

### `version`
- **Type**: string
- **Presence**: **Required**
- **Description**: Version of the consumption manifest.

### `prompts`
- **Type**: object
- **Presence**: **Required**
- **Description**: Mapping of local names to resolution configurations.

### `prompts.<additional>.id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable prompt ID.

### `prompts.<additional>.pin`
- **Type**: string
- **Presence**: *Optional*
- **Description**: A semver or git ref to pin to.

### `prompts.<additional>.override`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Path to a local file overriding the prompt.

### `prompts.<additional>.model`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Model to use for this prompt.

### `defaults`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Global fallbacks like default model or provider.

### `defaults.model`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Default model.

### `defaults.provider`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Default provider.
