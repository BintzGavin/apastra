#### 1. Context & Goal
- **Objective**: Implement an MCP (Model Context Protocol) server adapter to expose evaluations as discoverable MCP tools.
- **Trigger**: `docs/vision.md` explicitly calls for MCP integration to support tool-calling prompt evaluation and enable agents to discover and invoke evals as MCP tools.
- **Impact**: Unlocks the ability for agents to natively interact with the evaluation system via the standard Model Context Protocol, allowing seamless tool-calling and evaluation workflows.

#### 2. File Inventory
- **Create**:
  - `promptops/harnesses/mcp_server_adapter.py`: An executable python script functioning as the MCP server adapter. It exposes the evaluation suites as MCP tools and invokes the underlying runner.
- **Modify**:
  - `docs/status/EVALUATION.md`: Update to version 0.32.0 reflecting the completion of MCP integration.
- **Read-Only**:
  - `docs/vision.md`: To understand the MCP integration requirement.
  - `promptops/schemas/mcp-tool-definition.schema.json`: For reference on MCP tool structure.
  - `promptops/runs/runner-shim.sh`: For executing runs.

#### 3. Implementation Spec
- **Harness Architecture**:
  - The adapter will act as an MCP server conforming to the MCP JSON-RPC protocol over stdio.
  - It handles `tools/list` by returning tool definitions conforming to `mcp-tool-definition.schema.json` (e.g., a `run_eval` tool).
  - It handles `tools/call` by parsing the parameters, constructing a `run_request.json`, and executing the underlying harness adapter or `runner-shim.sh`.
  - It collects the run artifacts and formats a human-readable summary back to the agent as the tool response.
- **Run Request Format**: Uses existing schema (suite ID, model matrix, etc.) populated from the MCP tool call arguments.
- **Run Artifact Format**: Standard append-only artifacts are emitted to disk. The MCP tool response summarizes the `scorecard.json`.
- **Pseudo-Code**:
  - Read lines from `sys.stdin`.
  - Parse JSON-RPC request.
  - If `method == "tools/list"`, return the `run_eval` tool definition.
  - If `method == "tools/call"`, extract `suite_id`, execute `promptops/runs/runner-shim.sh` via subprocess, parse the output scorecard, and return the formatted result in the JSON-RPC response.
- **Baseline and Regression Flow**: The adapter strictly invokes the runner, which natively handles baseline comparison and regression reports. The adapter returns these outcomes in its response.
- **Dependencies**: Depends on CONTRACTS schemas (MCP tool definition, run request, scorecard) and the RUNTIME resolver for materializing prompts during the harness execution.

#### 4. Test Plan
- **Verification**: Execute `echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python3 promptops/harnesses/mcp_server_adapter.py` and verify it returns the `run_eval` tool. Then execute a `tools/call` request and observe the harness execution and JSON-RPC response.
- **Success Criteria**: The adapter successfully implements the MCP JSON-RPC protocol over stdio, allows discovery of the eval tool, and correctly delegates tool calls to the evaluation runner, returning a valid MCP response.
- **Edge Cases**: Handling malformed JSON-RPC requests, missing tool arguments, harness execution failures, and missing suites.
