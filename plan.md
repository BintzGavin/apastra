#### 1. Context & Goal
- **Objective**: Implement auto-detection for the "simplified minimal mode" file structure in the workspace resolver when the repository contains ≤3 prompt specs.
- **Trigger**: The docs/vision.md file specifies a "Simplified minimal mode" refinement: "auto-detected when ≤3 prompt specs exist; only `prompts/`, `evals/`, and `baselines/` directories".
- **Impact**: Reduces intimidation and friction for solo builders and new projects by allowing them to use a flat, simplified file structure initially, automatically graduating to the full structure later.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/workspace.py` (Update `WorkspaceResolver.resolve()` to detect and handle minimal mode)
- **Read-Only**: `docs/vision.md` (Simplified minimal mode definition)

#### 3. Implementation Spec
- **Resolver Architecture**: The `WorkspaceResolver` will check for the total number of prompt specs in the repository's prompt path. If there are 3 or fewer prompts (in either the `prompts/` directory or the legacy `promptops/prompts/` directory), it operates in minimal mode. In minimal mode, it will first look in the root-level `prompts/` and `evals/` directories for prompt specs, allowing users to skip the `promptops/` nesting completely.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  ```python
  import os
  import glob

  class WorkspaceResolver:
      def __init__(self):
          self.cache = {}

      def _detect_minimal_mode(self):
          # Count prompt specs in standard locations
          prompt_files = glob.glob('prompts/*.yaml') + glob.glob('prompts/*.json') + \
                         glob.glob('promptops/prompts/*.yaml') + glob.glob('promptops/prompts/*.json') + \
                         glob.glob('promptops/prompts/*/prompt.yaml') + glob.glob('promptops/prompts/*/prompt.json')

          # Count unique prompt ids roughly
          return len(prompt_files) <= 3

      def resolve(self, prompt_id):
          paths_to_try = [
              (f"promptops/prompts/{prompt_id}.yaml", False),
              (f"promptops/prompts/{prompt_id}.json", False),
              (f"promptops/prompts/{prompt_id}/prompt.yaml", False),
              (f"promptops/prompts/{prompt_id}/prompt.json", False),
              (f"promptops/evals/{prompt_id}.yaml", True),
              (f"promptops/evals/{prompt_id}.json", True)
          ]

          if self._detect_minimal_mode():
              minimal_paths = [
                  (f"prompts/{prompt_id}.yaml", False),
                  (f"prompts/{prompt_id}.json", False),
                  (f"evals/{prompt_id}.yaml", True),
                  (f"evals/{prompt_id}.json", True)
              ]
              paths_to_try = minimal_paths + paths_to_try

          # Rest of resolve logic...
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  1. `mkdir -p prompts && echo 'id: minimal-prompt\ntemplate: "Hello"' > prompts/minimal-prompt.yaml`
  2. `python3 -c "from promptops.resolver.workspace import WorkspaceResolver; print(WorkspaceResolver().resolve('minimal-prompt'))"`
- **Success Criteria**: Returns the parsed minimal-prompt data dictionary correctly from the root `prompts/` directory without requiring the `promptops/` folder.
- **Edge Cases**: More than 3 prompts (should ignore root directories and only look in `promptops/`). Mixed file extensions.
