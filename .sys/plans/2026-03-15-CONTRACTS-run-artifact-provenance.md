#### 1. Context & Goal
- **Objective**: Add SLSA-style provenance metadata schema to the run manifest.
- **Trigger**: `docs/vision.md` explicitly calls for "SLSA-style provenance metadata in run artifacts" under "Validation Requirements" to ensure reproducibility and track where and how runs execute.
- **Impact**: It unlocks supply-chain verifiable artifacts for the EVALUATION and GOVERNANCE domains, enabling auditability and stronger gating based on where the harness ran.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/schemas/run-manifest.schema.json`
- **Read-Only**: `promptops/schemas/run-artifact.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Update `promptops/schemas/run-manifest.schema.json` to include an optional `provenance` field.
  - The `provenance` field should be an object representing the invocation of the evaluation run. At a minimum, it should support fields modeling SLSA Provenance v1.0, such as:
    - `builder`: object with `id` (string URI identifying the builder).
    - `buildType`: string defining the build model.
    - `invocation`: object with `configSource` and `environment`.
    - `metadata`: object for timestamps and build metadata.
- **Content Digest Convention**: N/A. Adding an optional schema property doesn't change the digest calculation convention.
- **Pseudo-Code**:
  - Add the `provenance` property definition into the `properties` block of the `run-manifest.schema.json` file schema.
- **Public Contract Changes**: The schema ID `apastra-run-manifest-v1` will now allow a `provenance` object.
- **Dependencies**: No blocking dependencies on RUNTIME, EVALUATION, or GOVERNANCE.

#### 4. Test Plan
- **Verification**: cat promptops/schemas/run-manifest.schema.json
- **Success Criteria**: The schema allows `npx ajv-cli validate` to pass with valid SLSA provenance JSON data and correctly identifies malformed provenance blocks.
- **Edge Cases**: Empty provenance object or missing optional SLSA fields should still be accepted depending on exact definition.