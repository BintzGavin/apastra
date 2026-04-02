#### 1. Context & Goal
- **Objective**: Identify a new, uncompleted vision gap for EVALUATION and create an execution plan for it.
- **Trigger**: `docs/vision.md` outlines "Drift detection" (canary suites that run on a schedule to catch post-ship quality erosion when model providers update silently).
- **Impact**: Enables teams to catch post-ship quality erosion and drift silently caused by model updates, bringing "day 2" operations into the evaluation fold.

#### 2. File Inventory
- **Create**:
  - `.sys/plans/2026-04-02-EVALUATION-DriftDetection.md`: The spec file for the Executor to implement drift detection via canary suites.
- **Modify**: []
- **Read-Only**:
  - `docs/vision.md`: To reference the requirements for drift detection and canary suites.

#### 3. Implementation Spec
- **Harness Architecture**:
  - Define a new "canary" runner or modify existing harness adapter runner to support scheduled runs against specific deployed baselines.
- **Run Request Format**:
  - Needs a way to flag a run as a "canary" run and link it to a specific production baseline or deployment tag instead of an active PR.
- **Run Artifact Format**:
  - `regression_report.json` or a new `drift_report.json` must be able to compare canary results against the production baseline.
- **Pseudo-Code**:
  - `load canary suite schedule -> invoke harness adapter -> compare run artifact vs prod baseline -> alert if drifted`
- **Baseline and Regression Flow**:
  - Canary runs must explicitly compare against the current active "prod" baseline (found via promotion record).
- **Dependencies**:
  - CONTRACTS: May need a new `canary-suite.schema.json` or extension to existing suite schema.
  - RUNTIME: Resolver needs to support scheduled trigger resolution.

#### 4. Test Plan
- **Verification**: Ensure the generated spec file adheres to the planning template and describes actionable steps for the Executor.
- **Success Criteria**: The spec file is successfully created in `.sys/plans/` and is actionable for the Executor.
- **Edge Cases**: Ensure the spec handles the scenario where a baseline doesn't exist yet for a canary to test against.
