#### 1. Context & Goal
- **Objective**: Align workspace and git ref resolvers with the core repo topology model.
- **Trigger**: The `README.md` defines the same-repo topology as storing prompt specs in `promptops/prompts/`. However, `WorkspaceResolver` and `GitRefResolver` are currently looking for files directly in `promptops/` (e.g., `promptops/{prompt_id}.yaml`).
- **Impact**: Resolvers will correctly find prompt specs in the intended directories according to the architectural vision, unlocking seamless local iteration for same-repo consumers.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/resolver/workspace.py`
  - `promptops/resolver/git_ref.py`
- **Read-Only**: `README.md`

#### 3. Implementation Spec
- **Resolver Architecture**:
  - `WorkspaceResolver`: Update file lookup paths from `promptops/{prompt_id}.yaml` and `.json` to `promptops/prompts/{prompt_id}.yaml` and `.json`.
  - `GitRefResolver`: Update git show command paths from `promptops/{prompt_id}.yaml` and `.json` to `promptops/prompts/{prompt_id}.yaml` and `.json`.
- **Manifest Format**: No changes.
- **Pseudo-Code**:
  ```python
  # In WorkspaceResolver
  workspace_path_yaml = f"promptops/prompts/{prompt_id}.yaml"
  workspace_path_json = f"promptops/prompts/{prompt_id}.json"

  # In GitRefResolver
  ["git", "show", f"{pin}:promptops/prompts/{prompt_id}.yaml"]
  ["git", "show", f"{pin}:promptops/prompts/{prompt_id}.json"]
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: No new CONTRACTS dependencies.

#### 4. Test Plan
- **Verification**: Exact command: `mkdir -p test-fixtures/promptops/prompts && echo '{"template":"topology test"}' > test-fixtures/promptops/prompts/test-prompt.json && cd test-fixtures && python3 -c "import sys; sys.path.append('..'); from promptops.resolver.workspace import WorkspaceResolver; assert WorkspaceResolver().resolve('test-prompt') is not None"`
- **Success Criteria**: The test command exits with code 0 without raising an AssertionError.
- **Edge Cases**: Missing files, non-existent prompts.
