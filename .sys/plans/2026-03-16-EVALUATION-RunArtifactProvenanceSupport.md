#### 1. Context & Goal
- **Objective**: Implement SLSA-style provenance metadata collection in the reference harness adapter's run manifest.
- **Trigger**: The docs/vision.md and README.md define the "Run Artifact" as needing to be SLSA-style provenance-complete. The CONTRACTS schema for `run-manifest` includes a `provenance` field, but the EVALUATION reference adapter currently does not populate it.
- **Impact**: Unlocks verifiable evaluation runs and trust-building required by GOVERNANCE policies for public/trusted registries.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/harnesses/reference-adapter/run.py` (Add provenance metadata to the generated `manifest` object).
- **Read-Only**: `promptops/schemas/run-manifest.schema.json`, `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: The reference adapter (`run.py`) must be updated to inject a `provenance` object into the `manifest` dictionary before writing it to `run_manifest.json`.
- **Run Request Format**: No changes.
- **Run Artifact Format**: The `run_manifest.json` will now include a `provenance` object adhering to the schema (builder id, buildType, invocation environment, etc.).
- **Baseline and Regression Flow**: Not applicable.
- **Pseudo-Code**:
  - Capture `GITHUB_ACTIONS`, `GITHUB_RUN_ID`, `GITHUB_SHA`, `USER` from `os.environ`.
  - Construct the `provenance` dictionary.
  - Assign it to `manifest["provenance"]`.
- **Dependencies**: CONTRACTS (`run-manifest.schema.json`), RUNTIME (`resolver`).

#### 4. Test Plan
- **Verification**: cat promptops/harnesses/reference-adapter/run.py | grep -A 10 provenance
- **Success Criteria**: The `run.py` script correctly constructs and assigns the `provenance` object.
- **Edge Cases**: Missing environment variables (should handle gracefully with fallbacks or omit optional fields if applicable).
