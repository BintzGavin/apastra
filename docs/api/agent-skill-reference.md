---
title: "Agent Skill Reference"
description: "Schema defining an agent skill role configuration."
audience: "developers | platform-teams | agents"
last_verified: "2024-05-24"
source_files:
  - "promptops/schemas/agent-skill.schema.json"
---

# Agent Skill Reference

Schema defining an agent skill role configuration.

## Schema Details

### `id`

- **Type**: string
- **Required**: Yes
- **Description**: Stable identifier for the agent skill.

### `role`

- **Type**: string
- **Required**: Yes
- **Description**: The specific role the agent skill performs.

### `description`

- **Type**: string
- **Required**: Yes
- **Description**: A human-readable description of what the agent skill does.

### `capabilities`

- **Type**: array of string
- **Required**: Yes
- **Description**: A list of capabilities or sub-skills the agent possesses.
