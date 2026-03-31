#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validator for MCP Server Adapters.
- **Trigger**: `docs/vision.md` specifies under "MCP integration" the need to "Provide an MCP server adapter so agents can discover and invoke evals as MCP tools."
- **Impact**: Enables the ecosystem to integrate deeply with MCP clients, allowing AI agents to dynamically discover and run evaluation suites via standard tool-calling interfaces.

#### 2. File Inventory
- **Create**: `promptops/schemas/mcp-server-adapter.schema.json`, `promptops/validators/validate-mcp-server-adapter.sh`
- **Modify**: None.
- **Read-Only**: `docs/vision.md`, `promptops/schemas/harness-adapter.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: A JSON schema definition defining the required structure for an `mcp-server-adapter`. Requires fields: `id`, `type` (const: `mcp_server_adapter`), `entrypoint` (the command to start the MCP server), and optionally `capabilities` and `digest`.
- **Validator Logic**: Validation script will use `ajv` to validate an example `mcp-server-adapter.yaml` fixture against the schema, utilizing the `--spec=draft2020` flag.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `promptops/validators/validate-mcp-server-adapter.sh` against a valid and invalid JSON payload in a temp file.
- **Success Criteria**: The validator passes on valid payloads and fails on invalid payloads (e.g. missing `entrypoint` or wrong `type`).
- **Edge Cases**: Empty fields or missing required dependencies.
