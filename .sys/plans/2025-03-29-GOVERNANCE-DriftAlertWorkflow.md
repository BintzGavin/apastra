#### 1. Context & Goal
- **Objective**: Implement the scheduled GitHub Actions workflow for canary suites and drift detection.
- **Trigger**: `docs/vision.md` requires a "drift detection" capability where canary suites run on a schedule to catch output drift, and failures trigger drift alerts and auto-rollback rules.
- **Impact**: Enables post-ship quality monitoring by automatically scheduling canary suites, detecting drift against baselines, and enforcing escalation paths/auto-rollbacks via the drift alert policy.

#### 2. File Inventory
- **Create**:
  - `.github/workflows/canary-drift-detection.yml` (Scheduled workflow to run canary suites and enforce drift alerts)
- **Modify**:
  - `.sys/llmdocs/context-governance.md` (Update File Tree and Policy Inventory to include drift alerts workflow)
- **Read-Only**:
  - `promptops/policies/drift-alerts.md` (For escalation and auto-rollback rules)
  - `promptops/schemas/canary-suite.schema.json` (For canary suite schedule and thresholds)
  - `promptops/schemas/drift-report.schema.json` (For parsing drift detection results)

#### 3. Implementation Spec
- **Policy Architecture**: The workflow triggers on a schedule (e.g., cron) or manual dispatch. It executes canary suites against production baselines. If the harness emits a drift report with `drift_detected: true` (failing the `pass_rate` threshold), the workflow logs a drift alert to the registry, posts to the designated on-call channel, and triggers an auto-rollback if the failure is consecutive across trials.
- **Workflow Design**:
  ```yaml
  on:
    schedule:
      - cron: '0 * * * *'
    workflow_dispatch:
  jobs:
    run-canary:
      steps:
        - Checkout code
        - Run canary suite harness
        - Parse reports/drift_report.json
        - Check drift_detected field
        - If drift_detected == true:
            - Create issue or post alert to Slack/Teams channel
            - Trigger auto-rollback promotion record if failures exceed trial threshold
  ```
- **CODEOWNERS Patterns**: No changes to CODEOWNERS required; workflows are already owned by `@apastra/infrastructure`.
- **Promotion Record Format**: N/A for this spec (auto-rollback promotion records use existing schema with drift alert ID as justification).
- **Delivery Target Format**: N/A
- **Dependencies**: EVALUATION domain must provide a harness capable of executing canary suites and emitting `drift_report.json` based on `canary-suite.schema.json`.

#### 4. Test Plan
- **Verification**: Manually trigger the `.github/workflows/canary-drift-detection.yml` workflow with a mock canary suite that is guaranteed to fail its `pass_rate` threshold.
- **Success Criteria**: The workflow correctly detects the `drift_detected: true` field from the drift report, logs the drift alert, and initiates the escalation/auto-rollback path without failing the CI pipeline silently.
- **Edge Cases**: Missing baseline references, transient provider errors (handled via consecutive trial failures), or missing drift report output from the harness.
