#### 1. Context & Goal
- **Objective**: Create JSON schemas and validators for canary-suite and drift-report.
- **Trigger**: docs/vision.md and README.md propose "Canary suite and drift report schemas" for drift detection. These schemas do not exist yet.
- **Impact**: Unlocks the ability for RUNTIME to execute canary suites on a schedule and for EVALUATION/GOVERNANCE to track post-ship quality erosion via drift reports.

#### 2. File Inventory
- **Create**:
  - promptops/schemas/canary-suite.schema.json
  - promptops/schemas/drift-report.schema.json
  - promptops/validators/validate-canary-suite.sh
  - promptops/validators/validate-drift-report.sh
- **Modify**: None
- **Read-Only**:
  - promptops/schemas/suite.schema.json
  - promptops/schemas/regression-report.schema.json

#### 3. Implementation Spec
- **Schema Architecture**:
  - canary-suite.schema.json: JSON Schema extending or mirroring the standard suite but adding schedule (cron string) and alert (notification routing) fields.
  - drift-report.schema.json: JSON Schema comparing current results vs production baseline to identify output drift.
- **Content Digest Convention**: Consistent with other schema assets (SHA-256 of canonical JSON).
- **Pseudo-Code**:
  - Validator loads schema and instance.
  - Returns exit code 0 if valid, >0 if not.
- **Public Contract Changes**: Exports canary-suite.schema.json and drift-report.schema.json.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - Create mock valid/invalid canary-suite and drift-report JSON/YAML files.
  - Run validate-canary-suite.sh and validate-drift-report.sh against them.
- **Success Criteria**: Validators successfully enforce schema rules (passing valid files and rejecting invalid ones).
- **Edge Cases**: Missing schedule in canary suite, malformed drift report comparisons.
