#### 1. Context & Goal
- **Objective**: Design the workspace path resolution phase for the apastra prompt resolver chain.
- **Trigger**: The Git-first resolver chain from `README.md` requires falling back to the workspace path when no local `override` is present.
- **Impact**: This unlocks same-repo consumption, allowing downstream applications to resolve prompts located within the `promptops/` workspace.

#### 2. File Inventory
- **Create**: `test-fixtures/valid-workspace-prompt.yaml` (Test fixture containing valid prompt format).
- **Modify**: `promptops/resolver/chain.py` to add workspace path lookup logic.
- **Read-Only**: `promptops/schemas/consumption-manifest.schema.json` and `README.md`.

#### 3. Implementation Spec
- **Resolver Architecture**: The resolution chain evaluates local `override` first. If missing, it checks for a workspace path configuration. If the prompt exists at `promptops/` + `id` + `.yaml` (or `.json`), that file is resolved. If neither exists, it will fall back to git ref resolution (future).
- **Manifest Format**: The manifest format relies on the `id` property from `promptops/schemas/consumption-manifest.schema.json` to map to the workspace path.
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, ref_config):
      # 1. Local Override
      if 'override' in ref_config:
          return load_from_path(ref_config['override'])
      # 2. Workspace Path
      workspace_path = f"promptops/{prompt_id}.yaml"
      if exists(workspace_path):
          return load_from_path(workspace_path)
      workspace_path_json = f"promptops/{prompt_id}.json"
      if exists(workspace_path_json):
          return load_from_path(workspace_path_json)
      # 3. Fallback
      raise NotImplementedError("Git ref resolution not yet implemented")
  ```
- **Harness Contract Interface**: N/A.
- **Dependencies**: Requires `promptops/schemas/consumption-manifest.schema.json` (exists) and `promptops/schemas/prompt-spec.schema.json` (exists) to validate resolved content.

#### 4. Test Plan
- **Verification**: Run `cp test-fixtures/valid-workspace-prompt.yaml promptops/valid-workspace-prompt.yaml && python -c "from promptops.resolver.chain import resolve; print(resolve('valid-workspace-prompt', {}))"`.
- **Success Criteria**: The function returns the parsed content of the workspace prompt file.
- **Edge Cases**: Missing workspace directory, missing file extension (yaml vs json), invalid prompt format in workspace.
