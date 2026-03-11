#### 1. Context & Goal
- **Objective**: Define the promotion record format and an automated workflow to append records upon governed releases.
- **Trigger**: The README.md requires an append-only promotion record binding an approved digest/version to a channel to enable auditable deployments and explicit rollbacks.
- **Impact**: Establishes a machine-readable audit trail in `derived-index/promotions/`, enabling downstream delivery targets to sync approved versions and rollback via re-promotion.

#### 2. File Inventory
- **Create**: `.github/workflows/promote.yml` (GitHub Actions workflow to append promotion records to the index)
- **Modify**: N/A
- **Read-Only**: `README.md` (for Black Hole Architecture mapping)

#### 3. Implementation Spec
- **Policy Architecture**: Promotion records are append-only records. The workflow is triggered via `workflow_dispatch` (manual human checkpoint) or `release` events. It generates a standardized JSON record and commits it to the promotion index.
- **Workflow Design**:
  - Event: `workflow_dispatch` with inputs for `digest`, `channel`, and `evidence_refs`.
  - Jobs: `record-promotion`
  - Steps:
    - Checkout repository.
    - Generate JSON file `derived-index/promotions/<timestamp>-<id>.json` containing the provided inputs, timestamp, and GitHub actor.
    - Commit and push to the repository.
- **Promotion Record Format**:
  - `id`: Unique promotion event ID (e.g., generated UUID or timestamp-based)
  - `timestamp`: ISO-8601 timestamp of promotion
  - `digest`: The content digest of the promoted prompt package
  - `channel`: Target distribution channel (e.g., "prod", "staging")
  - `approver`: GitHub actor who approved/triggered the promotion
  - `evidence_refs`: Array of URIs linking to regression reports or run artifacts
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: No automated tests required for this architectural plan. The executor will validate the workflow syntax.
- **Success Criteria**: The `.github/workflows/promote.yml` file is created and adheres to the proposed schema format for records.
- **Edge Cases**: Missing inputs on dispatch, concurrent promotions (handled by unique timestamp filenames).
