#### 1. Context & Goal
- **Objective**: Define JSON Schema formats and validators for `promptops/policies/regression.yaml`, promotion records in `derived-index/promotions/`, and delivery targets in `promptops/delivery/`.
- **Trigger**: The GOVERNANCE domain is blocked waiting for regression policy, promotion record, and delivery target schemas.
- **Impact**: Unlocks the GOVERNANCE domain's required status check workflows, promotion record workflows, and delivery target sync workflows.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/regression-policy.schema.json`
  - `promptops/schemas/promotion-record.schema.json`
  - `promptops/schemas/delivery-target.schema.json`
  - `promptops/validators/validate-regression-policy.sh`
  - `promptops/validators/validate-promotion-record.sh`
  - `promptops/validators/validate-delivery-target.sh`
- **Modify**: []
- **Read-Only**: [`README.md`, `docs/status/GOVERNANCE.md`]

#### 3. Implementation Spec
- **Schema Architecture**:
  - `regression-policy.schema.json`: JSON Schema defining baseline reference rules (e.g. "prod current"), per-metric thresholds (absolute floors, allowed deltas, directionality), and severity (blockers vs. warnings).
  - `promotion-record.schema.json`: JSON Schema defining append-only binding records (digest/version bound to a channel), with evidence links (e.g., release candidate run ID) and timestamps.
  - `delivery-target.schema.json`: JSON Schema defining target sync config for approved versions (e.g., downstream app repo PRs, OCI registry namespaces, runtime config stores).
- **Content Digest Convention**: Compute SHA-256 over canonicalized JSON (`jq -cSM .`). YAML files (`.yaml`, `.yml`) must first be converted via `yq .`.
- **Pseudo-Code**: Validation scripts will load the target file, apply YAML-to-JSON conversion if needed, and execute `npx ajv-cli validate` against the respective schema in `promptops/schemas/`.
- **Public Contract Changes**: Exports IDs `regression-policy.schema.json`, `promotion-record.schema.json`, `delivery-target.schema.json`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - `echo '{"baseline": "latest", "rules": []}' > test-fixtures/valid-regression-policy.json`
  - `npx ajv-cli validate -s promptops/schemas/regression-policy.schema.json -d test-fixtures/valid-regression-policy.json --spec=draft2020 --strict=false`
  - `[ $? -eq 0 ]`
  - `echo '{"version": "1.0", "channel": "prod", "digest": "sha256:abc"}' > test-fixtures/valid-promotion-record.json`
  - `npx ajv-cli validate -s promptops/schemas/promotion-record.schema.json -d test-fixtures/valid-promotion-record.json --spec=draft2020 --strict=false`
  - `[ $? -eq 0 ]`
  - `echo '{"type": "github_pr", "repo": "app-repo"}' > test-fixtures/valid-delivery-target.json`
  - `npx ajv-cli validate -s promptops/schemas/delivery-target.schema.json -d test-fixtures/valid-delivery-target.json --spec=draft2020 --strict=false`
  - `[ $? -eq 0 ]`
- **Success Criteria**:
  - `[ $? -eq 0 ]`
- **Edge Cases**:
  - `echo '{"baseline": "latest"}' > test-fixtures/invalid-regression-policy.json`
  - `npx ajv-cli validate -s promptops/schemas/regression-policy.schema.json -d test-fixtures/invalid-regression-policy.json --spec=draft2020 --strict=false`
  - `[ $? -ne 0 ]`
  - `echo '{"version": "1.0"}' > test-fixtures/invalid-promotion-record.json`
  - `npx ajv-cli validate -s promptops/schemas/promotion-record.schema.json -d test-fixtures/invalid-promotion-record.json --spec=draft2020 --strict=false`
  - `[ $? -ne 0 ]`
  - `echo '{"type": "github_pr"}' > test-fixtures/invalid-delivery-target.json`
  - `npx ajv-cli validate -s promptops/schemas/delivery-target.schema.json -d test-fixtures/invalid-delivery-target.json --spec=draft2020 --strict=false`
  - `[ $? -ne 0 ]`