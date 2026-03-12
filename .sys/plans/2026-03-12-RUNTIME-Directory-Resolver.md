#### 1. Context & Goal
- **Objective**: Update WorkspaceResolver and GitRefResolver to support resolving prompts packaged in a `<prompt_id>` directory containing a `prompt.yaml` or `prompt.json` file.
- **Trigger**: The current resolvers look for `<prompt_id>.yaml` directly in `promptops/prompts/`, but prompts created by CONTRACTS are generated in directories (e.g., `promptops/prompts/test-prompt/prompt.yaml`), causing resolution failures.
- **Impact**: Unlocks end-to-end resolution for real prompts created by the CONTRACTS domain.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/resolver/workspace.py`: Update `resolve` to check for `promptops/prompts/<prompt_id>/prompt.yaml` and `promptops/prompts/<prompt_id>/prompt.json` as valid paths.
  - `promptops/resolver/git_ref.py`: Update `resolve` to check for `promptops/prompts/<prompt_id>/prompt.yaml` and `promptops/prompts/<prompt_id>/prompt.json` at the given ref.
- **Read-Only**: `promptops/schemas/prompt-spec.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The resolution chain maintains its order. In `WorkspaceResolver`, after checking for flat files (`<prompt_id>.yaml`), it will check the directory structure `promptops/prompts/<prompt_id>/prompt.yaml` and load from there. In `GitRefResolver`, a similar fallback checks the directory path at the given ref before raising a `RuntimeError`.
- **Manifest Format**: No change required.
- **Pseudo-Code**:
  ```python
  # In WorkspaceResolver
  path = f"promptops/prompts/{prompt_id}/prompt.yaml"
  if exists(path):
      return load(path)
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: CONTRACTS must provide `promptops/schemas/prompt-spec.schema.json` (already exists).

#### 4. Test Plan
- **Verification**: Run `PYTHONPATH=$(pwd) python promptops/runtime/cli.py test-prompt` to verify workspace resolution.
- **Success Criteria**: The command successfully outputs the resolved template string from `test-prompt/prompt.yaml`.
- **Edge Cases**: Missing directory, missing `prompt.yaml` inside directory, invalid JSON/YAML.
