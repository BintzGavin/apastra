# MCP Integration Governance Policy

## Purpose
This policy governs the integration of Model Context Protocol (MCP) tool definitions within prompt specs and controls how approved prompts are exposed to agents via MCP server adapters.

## Tool Definitions in Prompt Specs
- **Schema Requirements**: Any prompt spec incorporating MCP tool definitions must explicitly define the tool's input schema using the CONTRACTS JSON Schema standards.
- **Descriptions**: Each tool must include a clear, human-readable description explaining its function, expected inputs, and potential side-effects.
- **Review**: Tool definitions are subject to the same review and approval processes as the base prompt spec.

## Agent Exposure via MCP Server Adapters
- **Approval Gate**: Only prompt packages and benchmark suites that have successfully passed the regression gate and received formal promotion approval may be synced to the MCP server adapter.
- **Isolation**: Experimental or unapproved prompts must not be exposed to the production MCP server.
- **Auditability**: The sync process to the MCP server must be declarative, using the defined delivery target configuration, ensuring an auditable trail of what is available to agents.
