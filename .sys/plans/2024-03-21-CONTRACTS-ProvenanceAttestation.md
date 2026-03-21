#### 1. Context & Goal
- **Objective**: Create a JSON Schema and bash validator for provenance attestations.
- **Trigger**: `docs/vision.md` outlines "Provenance attestations" as an append-only artifact to establish build provenance (SLSA-style) for optional governed releases, but no schema exists in `promptops/schemas/`.
- **Impact**: Unlocks the ability for the RUNTIME and GOVERNANCE domains to issue, attach, and verify supply-chain provenance for prompt packages and run artifacts.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/provenance-attestation.schema.json`: JSON schema defining the provenance attestation format.
  - `promptops/validators/validate-provenance-attestation.sh`: Bash script using `ajv` to validate attestations against the schema.
- **Modify**: None.
- **Read-Only**:
  - `docs/vision.md`: To reference required fields and structure for provenance attestations (e.g., SLSA-style builder, invocation, materials).

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema defining `attestation_id`, `subject` (with `name` and `digest`), `predicateType` (specifying SLSA or custom format), and `predicate` (containing `builder`, `buildType`, `invocation`, and `metadata` such as timestamps).
- **Content Digest Convention**: The attestation itself should be immutable. Its digest can be computed as a SHA-256 of its canonical JSON representation, though the attestation acts as a wrapper around the subject's digest.
- **Pseudo-Code**: Validate the JSON input against `provenance-attestation.schema.json` using `ajv`. If valid, exit 0; else, exit 1.
- **Public Contract Changes**: Exports `https://promptops.apastra.com/schemas/provenance-attestation.schema.json`.
- **Dependencies**: None.
