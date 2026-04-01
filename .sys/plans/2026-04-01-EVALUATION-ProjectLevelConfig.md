#### 1. Context & Goal
- **Objective**: Spec the project-level config defaults support for the evaluation framework.
- **Trigger**: "Refinement 2: Project-level defaults via config file" from `docs/vision.md`.
- **Impact**: Reduces onboarding friction and simplifies project configuration by preventing repetitive configuration across suites and accelerating initial onboarding.

#### 2. File Inventory
- **Create**: `promptops/runs/apply_project_config.py`
- **Modify**: `promptops/harnesses/reference-adapter/run.py`
- **Read-Only**: []

#### 3. Implementation Spec
- **Harness Architecture**: Introduce `apply_project_config.py` to parse `promptops.config.yaml` using Python's `yaml` module and extract `defaults` and `thresholds`. Update `reference-adapter/run.py` to first check for explicit suite parameters; if missing, invoke the script to fall back to the config defaults for model, temperature, max_tokens, and policy thresholds.
- **Run Request Format**: No changes.
- **Scorecard Normalizer**: No changes.
- **Regression Comparison**: Ensure regression tools use the default policy thresholds from the project config if no suite-specific thresholds are set.
- **Dependencies**: CONTRACTS schemas required (`promptops-config.schema.json`); GOVERNANCE policies.

#### 4. Test Plan
- **Verification**: Run `promptops/runs/apply_project_config.py` against a sample `promptops.config.yaml` file and verify the parsed JSON output. Modify `run.py` and execute with an empty suite config to ensure defaults are correctly applied.
- **Success Criteria**: Project-level defaults are successfully extracted and applied by the reference adapter during a run.
- **Edge Cases**: Missing config file, malformed YAML, overriding defaults with explicit suite configs.
