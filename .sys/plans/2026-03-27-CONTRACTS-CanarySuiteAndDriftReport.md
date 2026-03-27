#### 1. Context & Goal
- **Objective**: Create JSON schemas and shell validators for Canary Suites and Drift Reports.
- **Trigger**: The docs/vision.md outlines "Drift detection" capabilities requiring a canary suite (with schedule and alert blocks) and a drift report output, which currently lack schema representations in promptops/schemas/.
- **Impact**: Enables the EVALUATION and RUNTIME domains to orchestrate scheduled canary runs and reliably detect production prompt quality erosion over time.

#### 2. File Inventory
- **Create**:
  - promptops/schemas/canary-suite.schema.json
  - promptops/schemas/drift-report.schema.json
  - promptops/validators/validate-canary-suite.sh
  - promptops/validators/validate-drift-report.sh
- **Modify**: None
- **Read-Only**: docs/vision.md

#### 3. Implementation Spec
- **Schema Architecture**:
  - canary-suite.schema.json: JSON Schema defining a scheduled evaluation. Must include $id, id (string), schedule (cron string), suite_ref (string reference to target suite), and alert (object containing on_regression boolean and channel string).
  - drift-report.schema.json: JSON Schema for the output of a canary run. Must include $id, canary_ref (string), baseline_ref (string), timestamp (date-time), drift_detected (boolean), and metrics_delta (object capturing variance).
- **Content Digest Convention**: Canary suite specifications are hashed via the canonical JSON ordering convention. Drift reports are append-only artifacts and hashable using the standard digest-convention.
- **Pseudo-Code**: Validation scripts will use ajv validate -s <schema> -d <fixture> exactly as in other validator scripts to enforce JSON schemas.
- **Public Contract Changes**: Introduces apastra-canary-suite-v1 and apastra-drift-report-v1 to the schema registry.
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: Run ./promptops/validators/validate-canary-suite.sh and ./promptops/validators/validate-drift-report.sh with valid and invalid JSON fixtures corresponding to the schema requirements.
- **Success Criteria**: The ajv CLI successfully accepts valid payloads and correctly rejects malformed canary suite or drift report documents (e.g., missing required fields like schedule).
- **Edge Cases**: Ensure the cron format for schedule is loosely validated as string, and metrics_delta correctly accommodates dynamic object keys for varying metrics.
