#### 1. Context & Goal
- **Objective**: Create the schema and validator for multi-model comparison scorecards.
- **Trigger**: Fulfills the "Expansion 3: Multi-model comparison" vision gap defined in `docs/vision.md`.
- **Impact**: Enables the system to compare the performance of a suite across N models simultaneously, producing a normalized view of cost, quality, and latency tradeoffs, which is a required artifact for the EVALUATION domain.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/comparison-scorecard.schema.json`: JSON Schema for the comparison scorecard.
  - `promptops/validators/validate-comparison-scorecard.sh`: Bash script to validate comparison scorecards against the schema.
- **Modify**:
  - None
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/scorecard.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (draft-07)
  - Required fields: `suite_id` (string), `models` (array of strings), `comparison_metrics` (object mapping metric names to a per-model breakdown), `tradeoff_surface` (object detailing cost vs quality vs latency).
  - Optional fields: `promotion_candidate` (string, which model+prompt combo is recommended to ship).
- **Content Digest Convention**:
  - Digest is computed over the canonicalized JSON of the comparison scorecard.
- **Pseudo-Code**:
  - Validate JSON input against `comparison-scorecard.schema.json` using `ajv`.
- **Public Contract Changes**:
  - Exported schema ID: `apastra-comparison-scorecard-v1`
- **Dependencies**:
  - None

#### 4. Test Plan
- **Verification**: Run `ajv validate -s promptops/schemas/comparison-scorecard.schema.json -d <test-fixture>`
- **Success Criteria**: A valid multi-model comparison scorecard JSON passes validation, while invalid structures (e.g., missing per-model breakdowns) fail.
- **Edge Cases**: Malformed input, missing required fields.
