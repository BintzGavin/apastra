#### 1. Context & Goal
- **Objective**: Spec the minimal file structure mode for the EVALUATION domain.
- **Trigger**: "Refinement 1: Simplified minimal file structure" in docs/vision.md requires a minimal mode auto-detected when <=3 prompt specs exist, condensing structure into prompts, evals, and baselines.
- **Impact**: Lowers the barrier to entry for solo builders by reducing the initial directory complexity from 13 subdirectories down to 3 until the project scales.

#### 2. File Inventory
- **Create**:
  - promptops/runs/minimal-shim.sh: A wrapper or utility script that detects whether minimal mode should be active based on prompt spec count and maps minimal mode files to the full architecture transparently.
- **Modify**:
  - promptops/runs/runner-shim.sh: Modify to check for the minimal structure (promptops/evals instead of suites) and route requests correctly if minimal mode is active.
- **Read-Only**:
  - docs/vision.md (for the Minimal mode refinement definition)
  - README.md (for minimal mode description)

#### 3. Implementation Spec
- **Harness Architecture**: Introduce a detection mechanism that checks the count of YAML files in promptops/prompts. If the count is 3 or less and the full structure doesn't exist, activate minimal mode. In minimal mode, suites, datasets, and evaluators are combined or sourced from promptops/evals and run outputs map to promptops/baselines (which may be a symlink or alias for derived-index/baselines).
- **Run Request Format**: No changes to the core format, but the shim will assemble the request by reading the unified evals yaml.
- **Run Artifact Format**: Unchanged.
- **Pseudo-Code**:
  - Count prompts: ls -1 promptops/prompts/*.yaml | wc -l.
  - If count <= 3 and promptops/suites is empty:
    - Set MINIMAL_MODE=true
    - Parse combined evals file to separate suite/dataset/evaluator components in memory or temporary files.
    - Pass generated paths to standard reference adapter runner.
- **Baseline and Regression Flow**: Ensure baseline and regression tools understand minimal mode paths.
- **Dependencies**: CONTRACTS schemas required for combined eval file structure; RUNTIME resolver availability; GOVERNANCE policy files needed.

#### 4. Test Plan
- **Verification**: mkdir -p promptops/evals && touch promptops/evals/dummy-smoke.yaml && promptops/runs/minimal-shim.sh check
- **Success Criteria**: The system successfully detects minimal mode, parses a quick eval file, generates a valid run request, and completes execution using only prompts, evals, and baselines.
- **Edge Cases**: >3 prompts existing but user wants minimal mode (should auto-disable or require manual override), transition from minimal to full structure, missing evals directory.
