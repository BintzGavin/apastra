#### 1. Context & Goal
- **Objective**: Define the consumption manifest format to allow applications to pin prompt IDs to specific git refs, local overrides, or semantic versions.
- **Trigger**: The consumption manifest is described in the `README.md` "Git-first consumption" section but currently has no format specification or schema.
- **Impact**: Unlocks app-side consumption of managed prompts. Allows developers to map abstract `prompt_id`s in their code to concrete package digests or local developer paths without changing application code.

#### 2. File Inventory
- **Create**: `promptops/manifests/consumption-example.yaml` (example of the format, to be created by the executor)
- **Modify**: None
- **Read-Only**: `README.md` (Git-first consumption section), `promptops/schemas/` (checked for existing schemas)

#### 3. Implementation Spec
- **Resolver Architecture**: The resolver reads the consumption manifest first. When an app asks to `resolve('my-prompt')`, it looks up `my-prompt` in the manifest. The precedence order is: local override -> workspace -> git ref -> packaged artifact.
- **Manifest Format**:
  - Top-level object with `version` (string, e.g., "1.0") and `prompts` (map of prompt ID to resolution rules).
  - Resolution rules for each prompt ID:
    - `local_override`: (Optional, string) A path to a local file or directory for development overrides.
    - `workspace`: (Optional, string) Path relative to the repo root for same-repo resolution.
    - `pin`: (Optional, string) A commit SHA, git tag, or semver tag (e.g., `v1.2.0`).
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, manifest_path="promptops/manifests/consumption.yaml"):
      manifest = load_yaml(manifest_path)
      rules = manifest.prompts.get(prompt_id)

      if not rules:
          raise PromptNotFoundError(prompt_id)

      if rules.local_override:
          return load_from_path(rules.local_override)
      elif rules.workspace:
          return load_from_workspace(rules.workspace)
      elif rules.pin:
          return load_from_git(rules.pin)
      else:
          raise InvalidResolutionRulesError()
  ```
- **Harness Contract Interface**: N/A for this task.
- **Dependencies**: CONTRACTS must create `consumption-manifest.schema.json` and a validator script to validate this format.

#### 4. Test Plan
- **Verification**: Ensure the generated `consumption-example.yaml` is valid according to the future schema once CONTRACTS implements it.
- **Success Criteria**: A clear, unambiguous YAML format is defined that covers local, workspace, and git-pinned scenarios as promised by the README.
- **Edge Cases**: Manifest with missing resolution keys, conflicting keys (e.g., both local override and pin, where local override should take precedence), malformed YAML.
