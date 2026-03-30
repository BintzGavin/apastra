#### 1. Context & Goal
- **Objective**: Implement project-level defaults and auto-detect minimal mode.
- **Trigger**: "Refinement 1: Simplified minimal file structure" and "Refinement 2: Project-level defaults via config file" from docs/vision.md.
- **Impact**: Reduces onboarding friction and simplifies project configuration.

#### 2. File Inventory
- **Create**: `promptops/runs/apply_project_config.py` (Script to load and apply `promptops.config.yaml`).
- **Modify**: `promptops/harnesses/reference-adapter/run.py` (Update reference adapter to load defaults from config if not present in suite).
- **Modify**: `promptops/runs/quick-eval.sh` (Update quick eval to use `promptops.config.yaml` defaults).
- **Read-Only**: `docs/vision.md`, `README.md`.

#### 3. Implementation Spec
- **Harness Architecture**: Adapter should first check for explicit suite parameters (model, temperature, etc). If missing, it checks `promptops.config.yaml`.
- **Run Request Format**: No changes.
- **Run Artifact Format**: No changes.
- **Pseudo-Code**:
  - Read `promptops.config.yaml` using Python's `yaml` module.
  - If `defaults` section exists, use as fallback for suite matrix, config, and thresholds.
  - Minimal mode check: count files in `promptops/prompts/`. If <= 3, operate in simplified directory mode.
- **Baseline and Regression Flow**: No changes.
- **Dependencies**: CONTRACTS must specify schema for `promptops.config.yaml` (optional but recommended).

#### 4. Test Plan
- **Verification**: Run `promptops/runs/apply_project_config.py` against a sample `promptops.config.yaml` and verify values are correctly parsed. Execute `promptops/harnesses/reference-adapter/run.py` with an empty suite config to ensure defaults are applied.
- **Success Criteria**: Evaluator outputs reflect the defaults specified in `promptops.config.yaml`.
- **Edge Cases**: Missing config file, malformed YAML, overriding defaults with explicit suite configs.
