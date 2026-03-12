#### 1. Context & Goal
- **Objective**: Fix the `LocalResolver` in the resolver chain to parse prompt packages instead of returning stub strings.
- **Trigger**: The current implementation of `promptops/resolver/local.py` contains a stub `load_prompt_package` that simply returns a string (`f"Loaded prompt from {path}"`) instead of parsing the actual YAML or JSON prompt specification. This breaks the expected minimal runtime contract, as `resolve()` expects structured output.
- **Impact**: Unlocks the ability for consumers and testing tools to seamlessly use local overrides by loading correct prompt specifications from their paths.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/local.py` (update `load_prompt_package` to actually load the YAML/JSON file instead of returning a stub string).
- **Read-Only**: `promptops/resolver/workspace.py` (consulting its `load_prompt_package` implementation for reference), `README.md` (for the "Local override for development" section).

#### 3. Implementation Spec
- **Resolver Architecture**: The local override step (`LocalResolver`) currently correctly identifies if the file exists, but its helper `load_prompt_package` just returns a string. It must be updated to read the file, detect the extension (`.yaml`/`.yml` vs `.json`), and parse its contents.
- **Manifest Format**: Unchanged (the schema defines `override` which correctly maps to the path).
- **Pseudo-Code**:
  ```python
  import os
  import json
  import yaml

  def load_prompt_package(path):
      if path.endswith('.yaml') or path.endswith('.yml'):
          with open(path, 'r') as f:
              return yaml.safe_load(f)
      elif path.endswith('.json'):
          with open(path, 'r') as f:
              return json.load(f)
      return None

  class LocalResolver:
      def resolve(self, prompt_id, override_path):
          if not os.path.exists(override_path):
              raise FileNotFoundError(f"Local override path not found: {override_path}")
          return load_prompt_package(override_path)
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: No new CONTRACTS schemas required. Depends on `yaml` and `json` standard parsing libraries.

#### 4. Test Plan
- **Verification**: Run `python -c "from promptops.resolver.local import LocalResolver; print(LocalResolver().resolve('my-prompt', 'test-fixtures/test-prompt.json'))"`
- **Success Criteria**: The command should output a parsed python dictionary containing the prompt configuration rather than a stub string.
- **Edge Cases**: Missing file (should raise FileNotFoundError), unsupported extension (should return None).