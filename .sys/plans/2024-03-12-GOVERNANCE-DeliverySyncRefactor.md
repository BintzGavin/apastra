#### 1. Context & Goal
- **Objective**: Refactor the Delivery Target Sync workflow to correctly operate within the Artifacts Branch topology by using `workflow_call` and fetching promotion records from the `promptops-artifacts` branch.
- **Trigger**: The Delivery Target primitive promises declarative sync to downstream systems, but the current `deliver.yml` is broken because it listens for pushes to `derived-index/promotions/` on the main branch, whereas promotion records are now written to `promotions/` on the `promptops-artifacts` branch.
- **Impact**: Restores the automated audit trail and delivery sync loop, ensuring approved and governed prompt packages actually reach downstream delivery targets.

#### 2. File Inventory
- **Create**: `.sys/plans/2024-03-12-GOVERNANCE-DeliverySyncRefactor.md`
- **Modify**: `.github/workflows/deliver.yml` (Change to `workflow_call` and read from `promptops-artifacts`)
- **Modify**: `.github/workflows/promote.yml` (Trigger `deliver.yml` on successful promotion)
- **Read-Only**: `promptops/delivery/prod-target.yaml`, `README.md`

#### 3. Implementation Spec
- **Policy Architecture**: The `promote.yml` workflow writes a promotion record to `promptops-artifacts`. Upon success, it passes the generated `filepath` to `deliver.yml` via `workflow_call`. The `deliver.yml` workflow runs on the `main` branch to read declarative target specs (`promptops/delivery/*.yaml`), fetches the specific promotion record from `promptops-artifacts`, and executes sync logic for matching channels.
- **Workflow Design**:
  - `deliver.yml`: Change `on: push` to `on: workflow_call: inputs: promotion_record_path: required: true type: string`. Add steps to `git fetch origin promptops-artifacts` and `git checkout origin/promptops-artifacts -- promotions/`. Read the `channel` and `digest` from the passed file path using `jq`.
  - `promote.yml`: Add outputs to the `record-promotion` job. Add a new `deliver` job that uses `needs: record-promotion` and `uses: ./.github/workflows/deliver.yml@main` with `with: promotion_record_path`.
- **CODEOWNERS Patterns**: No changes needed, `promptops/delivery/` is correctly owned by `@apastra/governance-admins`.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: No changes.
- **Dependencies**: Depends on the existing `promptops-artifacts` branch and the JSON structure of promotion records appended by `promote.yml`.

#### 4. Test Plan
- **Verification**: Dispatch the `promote.yml` workflow manually to generate a promotion record. Verify that the `deliver` job triggers automatically.
- **Success Criteria**: The `deliver.yml` workflow successfully reads the promotion record from `promptops-artifacts`, matches the channel to `prod-target.yaml`, and echoes the sync execution.
- **Edge Cases**: Handles missing `promptops-artifacts` gracefully. Handles cases where no delivery targets match the promoted channel.
