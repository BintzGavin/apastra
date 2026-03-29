#### 1. Context & Goal
- **Objective**: Implement project config loading and defaults resolution in the runtime.
- **Trigger**: The docs/vision.md explicitly defines "Project config loading" as a runtime feature: "resolve promptops.config.yaml and apply project-level defaults (model, temperature, thresholds, auto-baseline) to suites that don't override them".
- **Impact**: Unlocks reduced configuration boilerplate for users, making the system easier to adopt, and guarantees consistent evaluation parameters across suites unless explicitly overridden.

#### 2. File Inventory
- **Create**: (None)
- **Modify**: `promptops/runtime/config.py` (Add validation and apply_config_defaults method)
- **Modify**: `promptops/runtime/__init__.py` (Export config functions)
- **Modify**: `promptops/runtime/runner.py` (To apply the config to the loaded suite before execution)
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/promptops-config.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The runtime will search for `promptops.config.yaml` at the root of the project workspace. If found, it parses and validates it against `promptops-config.schema.json`.
- **Manifest Format**: The config file schema defines `defaults` (model, temperature, max_tokens), `thresholds` (metric passing criteria), and `baseline` (auto_set behavior).
- **Pseudo-Code**:
  ```python
  def apply_config_defaults(suite: dict, config: dict) -> dict:
      if not config:
          return suite
      if 'defaults' in config:
          defaults = config['defaults']
          if 'model' in defaults and 'model_matrix' not in suite:
              suite['model_matrix'] = [defaults['model']]
      if 'thresholds' in config:
          if 'thresholds' not in suite:
              suite['thresholds'] = config['thresholds']
          else:
              for k, v in config['thresholds'].items():
                  if k not in suite['thresholds']:
                      suite['thresholds'][k] = v
      return suite
  ```
- **Harness Contract Interface**: Downstream harnesses will receive the fully resolved suite, which has project defaults already applied. No changes to the contract format, only the data sent inside it.
- **Dependencies**: Depends on the existence of `promptops/schemas/promptops-config.schema.json` in the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: Create a mock `promptops.config.yaml` and a mock suite. Write a python script to run `load_project_config()` followed by `apply_config_defaults()` on the suite. Check that the values are correctly injected.
- **Success Criteria**: The output suite contains the config's model, temperature, thresholds, etc. where it previously had nothing.
- **Edge Cases**: Missing config file (should silently return defaults/empty dictionary), invalid config file against schema (should raise validation error), suite overriding a default (suite value should win).
