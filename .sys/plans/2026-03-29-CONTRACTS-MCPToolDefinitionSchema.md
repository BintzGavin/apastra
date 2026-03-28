#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for MCP tool definitions to be embedded within prompt specs.
- **Trigger**: The docs/vision.md lists "MCP tool definition: MCP tool definitions as part of prompt specs for tool-calling evaluation" as an Expansion Noun Requiring Schema.
- **Impact**: Enables EVALUATION and RUNTIME domains to process, validate, and execute tool-calling evaluations using standard Model Context Protocol formats.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/mcp-tool-definition.schema.json` (JSON schema for MCP tool definitions)
  - `promptops/validators/validate-mcp-tool-definition.sh` (Bash script to validate MCP tool definitions)
- **Modify**: None
- **Read-Only**: `promptops/schemas/prompt-spec.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - The schema will define an MCP tool definition object.
  - Required fields: `name` (string), `description` (string), `inputSchema` (object containing JSON schema for tool arguments).
  - Optional fields: `type` (defaults to "function", though MCP is protocol-agnostic, often used for functions).
- **Content Digest Convention**: The digest will be computed over the canonicalized JSON representation of the tool definition.
- **Pseudo-Code**:
  - The validation script will load the schema and target JSON, using `ajv` to validate the target against the schema.
- **Public Contract Changes**: Exports `mcp-tool-definition.schema.json` and its corresponding validator.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `ajv validate -s promptops/schemas/mcp-tool-definition.schema.json -d <test-fixture>`
- **Success Criteria**: The validator passes a valid MCP tool definition and rejects one missing `name` or `inputSchema`.
- **Edge Cases**: Empty inputSchema, missing description, invalid types.
