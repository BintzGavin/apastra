#### 1. Context & Goal
- **Objective**: Implement project-level defaults resolution by loading `promptops.config.yaml`.
- **Trigger**: The docs/vision.md file specifies "Project config loading" and "Project-level defaults via config file" to apply project-level defaults (model, temperature, thresholds, auto-baseline) to suites that don't override them.
- **Impact**: Accelerates initial onboarding and prevents repetitive configuration across suites by allowing a central `promptops.config.yaml` to define defaults. This impacts downstream EVALUATION harnesses and consumers.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/config.py` (New module to handle locating, loading, and validating the `promptops.config.yaml` file)
- **Modify**:
  - `promptops/runtime/resolve.py` (Update `resolve()` to load project defaults and merge them with manifest rules)
  - `promptops/resolver/chain.py` (Potentially update `ResolverChain` context to inject project defaults)
- **Read-Only**:
  - `docs/vision.md` (Project config loading specifications)
  - `README.md` (Repo topology and vision concepts)
  - `promptops/schemas/suite.schema.json` (Understand how defaults might affect suites)

#### 3. Implementation Spec
- **Resolver Architecture**: The runtime will search for `promptops.config.yaml` in the current working directory, or traverse upwards to find it at the project root. When `resolve()` is called, it will load this configuration (caching it in memory to avoid redundant disk reads). The project defaults (e.g. `defaults.model`, `defaults.temperature`) will be merged into the resolution context as a fallback layer. The resolution precedence will be: 1. Suite/Manifest explicit override, 2. Project config defaults (`promptops.config.yaml`), 3. Hardcoded runtime defaults.
- **Manifest Format**: The consumption manifest validation remains the same, but the internal `resolve()` function will incorporate the `defaults` section from `promptops.config.yaml`. The config format is:
  ```yaml
  defaults:
    model: string
    temperature: float
    max_tokens: integer
  thresholds:
    keyword_recall: float
    pass_rate: float
  baseline:
    auto_set: boolean
  ```
- **Pseudo-Code**:
  ```python
  # promptops/runtime/config.py
  def load_project_config():
      # 1. Search for promptops.config.yaml in CWD and up to root
      # 2. If found, load YAML and return dict
      # 3. Else return empty dict {}

  # promptops/runtime/resolve.py
  def resolve(prompt_id, ref_context=None, ...):
      manifest = load_manifest(ref_context)
      project_config = load_project_config()

      rules = manifest.get_rules(prompt_id) if hasattr(manifest, 'get_rules') else {}
      manifest_defaults = manifest.data.get('defaults', {}) if hasattr(manifest, 'data') and isinstance(manifest.data, dict) else {}
      project_defaults = project_config.get('defaults', {})

      # Fallback logic: manifest specific rule -> manifest default -> project config default
      model = rules.get('model', manifest_defaults.get('model', project_defaults.get('model')))
      ...
  ```
- **Harness Contract Interface**: No changes to the harness contract interface.
- **Dependencies**: No new CONTRACTS schemas required for the config file format at this stage (though one could be added in the future). Depends on existing schemas for validation.

#### 4. Test Plan
- **Verification**:
  1. Create a mock `promptops.config.yaml` with `defaults: { model: 'gpt-4o' }`.
  2. Create a prompt spec `promptops/prompts/test-config.yaml`.
  3. Run the python module that invokes `resolve('test-config')`.
- **Success Criteria**: The metadata returned from `resolve()` should include `model_ids: ['gpt-4o']` sourced from the `promptops.config.yaml` file, without it being explicitly set in a consumption manifest or suite.
- **Edge Cases**:
  - Missing `promptops.config.yaml` (should gracefully default to empty).
  - Invalid YAML format in config file.
  - Conflict resolution: ensuring explicit manifest rules override the project config.
