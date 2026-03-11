#### 1. Context & Goal
- **Objective**: Design the declarative configuration schema for delivery targets and the workflow architecture to sync approved versions to downstream systems.
- **Trigger**: The README.md promises declarative delivery target configs in `promptops/delivery/` to describe how to sync approved versions, but no specs or sync workflows exist yet.
- **Impact**: Establishes the standard for syncing promotions to actual delivery targets, ensuring that downstream systems only receive approved digests, enabling robust promotion and rollback.

#### 2. File Inventory
- **Create**:
  - A new workflow file in `.github/workflows/` (GitHub Actions workflow to trigger sync based on target spec)
  - A new schema in `promptops/schemas/` (JSON schema defining the delivery target configuration format)
- **Modify**: []
- **Read-Only**: `derived-index/promotions/` (to understand what triggers a delivery), `README.md` (delivery targets section)

#### 3. Implementation Spec
- **Policy Architecture**: Delivery is configuration, not code. The delivery target spec defines *where* and *how* to deliver a promoted digest. A sync workflow reads new promotion records, finds matching delivery targets by channel, and executes the delivery adapters (e.g., updating a consumption manifest in a downstream repo or pushing to an OCI registry).
- **Workflow Design**:
  - Triggered by push events on promotion records in `derived-index/promotions/`
  - Read the parsed promotion record for `channel` and `digest`
  - Iterate through specs in `promptops/delivery/`
  - If a spec matches the `channel`, execute the corresponding delivery logic
- **Delivery Target Format**:
  - `target_id`: Unique identifier for the target.
  - `channel`: The channel this target listens to (e.g., `prod`, `staging`).
  - `type`: The adapter type (e.g., `github_pr`, `oci_registry`, `webhook`).
  - `config`: Type-specific configuration (e.g., repo name, branch, endpoint).
- **Dependencies**: Promotion record format must be stable; requires CONTRACTS domain to implement the schema and validation logic.

#### 4. Test Plan
- **Verification**: This is a blueprint planning task; no tests are required for the plan itself.
  ```bash
  echo 'No tests required'
  ```
- **Success Criteria**: The delivery target schema blueprint is defined and a sync workflow is conceptually designed to react to promotion records.
- **Edge Cases**: Missing target configurations, unsupported target types, and network failures during delivery.
