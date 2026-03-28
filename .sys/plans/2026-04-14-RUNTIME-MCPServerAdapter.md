#### 1. Context & Goal
- **Objective**: Provide an MCP server adapter to expose evaluations as discoverable MCP tools.
- **Trigger**: The docs/vision.md file specifies "MCP integration — support MCP tool definitions in prompt specs and provide an MCP server adapter for agent discovery".
- **Impact**: Enables external IDE agents to easily discover and invoke prompt evaluations natively via the Model Context Protocol, drastically reducing friction for autonomous quality checking.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/mcp_server.py` (New module implementing the MCP server adapter and exposing evaluation tools)
- **Modify**:
  - `promptops/runtime/cli.py` (Update CLI to add an `mcp` command that starts the server)
- **Read-Only**:
  - `docs/vision.md` (MCP integration specifications)
  - `promptops/schemas/run-request.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The `mcp_server.py` will define an MCP server using an appropriate MCP Python SDK or implementing the JSON-RPC protocol over stdio. It will expose tools such as `run_evaluation` (taking a `suite_id` and `prompt_id`) and `list_evaluations`. When the `run_evaluation` tool is invoked, it will internally construct a run request and trigger the `RunnerShim` to execute it, then return a summary of the scorecard and any regression alerts to the calling agent.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  ```python
  # promptops/runtime/mcp_server.py
  import sys
  import json
  # import mcp_sdk (hypothetical or stdio handling)

  class MCPServer:
      def __init__(self):
          self.tools = {
              "run_evaluation": self.run_evaluation,
              "list_suites": self.list_suites
          }

      def run_evaluation(self, params):
          suite_id = params.get("suite_id")
          # Construct run request
          # Invoke runner.py logic
          # Return scorecard summary
          return {"status": "success", "scorecard": {...}}

      def serve_stdio(self):
          # Read from stdin, write to stdout using JSON-RPC
          pass

  def start_mcp_server():
      server = MCPServer()
      server.serve_stdio()

  # promptops/runtime/cli.py
  # Add handling for `promptops.runtime.cli mcp` to call start_mcp_server()
  ```
- **Harness Contract Interface**: No changes to the harness contract interface.
- **Dependencies**: Depends on existing RUNTIME runner and resolver logic to execute the requested suites.

#### 4. Test Plan
- **Verification**:
  1. Start the MCP server via `python -m promptops.runtime.cli mcp`.
  2. Send a mock JSON-RPC request for `list_suites` via stdin.
- **Success Criteria**: The server responds with a valid JSON-RPC response containing the list of available suites discovered in the workspace.
- **Edge Cases**:
  - Malformed JSON-RPC requests.
  - Requested suite does not exist.
  - Harness execution failure during `run_evaluation` tool invocation.
