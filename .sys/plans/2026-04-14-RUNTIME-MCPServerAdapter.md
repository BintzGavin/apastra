#### 1. Context & Goal
- **Objective**: Design the MCP server adapter to expose apastra evals as discoverable MCP tools for IDE agents.
- **Trigger**: "MCP server adapter" is listed as a proposed expansion in docs/vision.md and README.md.
- **Impact**: Allows IDE agents (like Claude Code or Cursor) to dynamically discover and invoke apastra evaluations directly within the developer's workflow, bridging the gap between local prompt editing and automated testing.

#### 2. File Inventory
- **Create**:
  - promptops/runtime/mcp_server.py: Core MCP server implementation exposing apastra tools.
  - promptops/runtime/mcp_tools.py: Definitions for the specific MCP tools (e.g., run_eval, baseline, scaffold).
- **Modify**:
  - promptops/runtime/cli.py: Add an mcp subcommand to start the MCP server.
- **Read-Only**:
  - docs/vision.md (MCP integration details)
  - README.md (Agent integration concepts)

#### 3. Implementation Spec
- **Resolver Architecture**: The MCP server will not change the resolution chain itself but will wrap the existing ResolverChain and runner logic. It acts as an interactive frontend for agents.
- **Manifest Format**: No direct changes to the manifest format.
- **Pseudo-Code**:
  - Initialize an MCP server instance.
  - Register tool run_eval: takes suite_id, ref as inputs. Internally calls runner.py logic and returns a summary of the scorecard.json and a link to the regression_report.json.
  - Register tool baseline: takes run_id as input. Invokes baseline establishment logic.
  - Register tool scaffold: takes intent as input. Generates boilerplate files for prompts, datasets, and suites.
  - Start the stdio transport loop.
- **Harness Contract Interface**: The MCP server will invoke the harness as defined in harness_adapter.yaml just like the CLI does.
- **Dependencies**: No new CONTRACTS schemas required. Depends on existing scorecard.schema.json and run-manifest.schema.json.

#### 4. Test Plan
- **Verification**: Start the MCP server locally (python -m promptops.runtime.cli mcp). Connect a compatible MCP client (like the reference MCP Inspector) and invoke the run_eval tool with a known test suite.
- **Success Criteria**: The tool execution returns a valid JSON response containing the suite's pass/fail status and key metrics from the scorecard.
- **Edge Cases**: Verify behavior when an invalid suite_id is provided, when the harness fails to execute, and when the promptops directory is not initialized.
