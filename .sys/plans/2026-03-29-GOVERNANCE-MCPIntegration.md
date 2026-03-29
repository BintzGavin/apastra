#### 1. Context & Goal
- **Objective**: Implement governance rules for Model Context Protocol (MCP) integration and specify the MCP server adapter delivery target.
- **Trigger**: `docs/vision.md` (Refinement 3) requires MCP integration to support tool-calling prompt evaluation and an MCP server adapter for agent discovery.
- **Impact**: Establishes the policy for exposing approved prompt assets to agents via MCP and creates a delivery target config to sync approved suites/prompts to an MCP server adapter, creating an auditable trail for tool-calling eval discovery.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/mcp-integration.md`: Governance rules for MCP tool definitions and server adapter exposure.
  - `promptops/delivery/mcp-server-target.yaml`: Declarative delivery config to sync approved prompt packages to the MCP server.
- **Modify**:
  - `.sys/llmdocs/context-governance.md`: Surgically update file tree and inventory with new MCP integration policy and delivery target.
- **Read-Only**:
  - `docs/vision.md` (Refinement 3 section for MCP integration details)
  - `promptops/delivery/observability.yaml` (to match existing declarative delivery target patterns)

#### 3. Implementation Spec
- **Policy Architecture**: The policy `mcp-integration.md` will define rules for including MCP tool definitions in prompt specs, ensuring they include clear schemas and descriptions. It will also stipulate that only approved prompt packages and benchmark suites from the registry can be exposed to agents via the MCP server adapter.
- **Workflow Design**: N/A (policy and declarative config only).
- **CODEOWNERS Patterns**: N/A (inherits existing `promptops/policies/` and `promptops/delivery/` ownership).
- **Promotion Record Format**: N/A (uses existing promotion record format).
- **Delivery Target Format**:
  Fields in `promptops/delivery/mcp-server-target.yaml` will declare how the system syncs to the MCP server:
  `target_type`, `endpoint` (e.g., `${MCP_SERVER_ENDPOINT}`), `sync_on_promotion`, and `channels` (e.g., `[prod, staging]`).
- **Dependencies**: CONTRACTS schemas must support MCP tool definitions inside prompt specs.

#### 4. Test Plan
- **Verification**: Check that `promptops/policies/mcp-integration.md` and `promptops/delivery/mcp-server-target.yaml` are correctly formatted and that `.sys/llmdocs/context-governance.md` accurately lists them in the file tree and policy inventory.
- **Success Criteria**: The MCP governance policy clearly restricts agent discovery to approved prompts, and the delivery target provides a declarative configuration for syncing.
- **Edge Cases**: Handles scenarios where the MCP server adapter endpoint is unavailable during delivery or tool definitions are malformed.
