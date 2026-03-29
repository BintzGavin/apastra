---
title: "MCP Tool Definition Reference"
description: "Schema defining an MCP tool definition object."
audience: "developers | platform-teams | agents"
last_verified: "2024-05-24"
source_files:
  - "promptops/schemas/mcp-tool-definition.schema.json"
---

# MCP Tool Definition Reference

Schema defining an MCP tool definition object.

## Schema Details

### `name`

- **Type**: string
- **Required**: Yes
- **Description**: The name of the tool.

### `description`

- **Type**: string
- **Required**: Yes
- **Description**: A description of what the tool does and when it should be used.

### `inputSchema`

- **Type**: object
- **Required**: Yes
- **Description**: A JSON Schema defining the input arguments for the tool.

### `type`

- **Type**: string
- **Required**: No
- **Description**: The type of the tool. Defaults to 'function'.
