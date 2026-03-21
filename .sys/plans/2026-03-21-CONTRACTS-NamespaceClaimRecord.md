#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for namespace claim records.
- **Trigger**: `docs/vision.md` mandates governance policies for "naming" alongside ownership disputes and deprecation, which requires a formalized schema for the GOVERNANCE domain to track canonical name registrations.
- **Impact**: Enables the GOVERNANCE domain to programmatically process and validate requests to claim or transfer canonical namespaces in the registry, preventing state hallucination.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/namespace-claim-record.schema.json`
  - `promptops/validators/validate-namespace-claim-record.sh`
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema defining a namespace claim record. Required fields: `claim_id` (string), `namespace` (string, pattern matching canonical name requirements), `requester_id` (string), `timestamp` (string, date-time), `status` (string, enum: pending, approved, rejected, disputed), and `evidence_uri` (string, optional URI providing proof of trademark or ownership).
- **Content Digest Convention**: N/A for this schema (append-only registry metadata, digest computed externally if needed).
- **Pseudo-Code**:
  - Validator script reads a JSON file as input.
  - Calls `ajv validate -c ajv-formats -s promptops/schemas/namespace-claim-record.schema.json -d <input_file>`.
  - Exits with 0 on success, non-zero on failure.
- **Public Contract Changes**: Exports a new schema ID `https://promptops.apastra.com/schemas/namespace-claim-record.schema.json`.
- **Dependencies**: None.
