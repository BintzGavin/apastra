---
title: "Mcp Server Adapter"
description: "API reference for Mcp Server Adapter"
audience: "all"
last_verified: "2026-04-01"
source_files:
  - "promptops/schemas/mcp-server-adapter.schema.json"
---

# Mcp Server Adapter

API reference for Mcp Server Adapter

## Properties

### `id` (Required)

**Type:** `string`

Stable identifier for the MCP server adapter.

### `type` (Required)

**Type:** `string`

Must be 'mcp_server_adapter'.

### `capabilities` (Optional)

**Type:** `array`

Optional list of capabilities provided by the MCP server.

### `entrypoint` (Required)

**Type:** `string`

The command to start the MCP server.

### `digest` (Optional)

**Type:** `string`

Content digest stored inline.
