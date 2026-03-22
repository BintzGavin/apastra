#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for "delivery target receipt".
- **Trigger**: The `docs/vision.md` explicitly states: "A prompt revision can be traced from source commit → PR review → benchmark runs → regression decision → release tag/release asset → promotion record → delivery target receipt." The schema for delivery target receipt is currently missing.
- **Impact**: This unlocks the ability to trace and record the receipt of a delivery target, allowing evaluation and other tools to definitively know when and where an artifact has been delivered, thus completing the lineage tracking defined in the vision document.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/delivery-target-receipt.schema.json`: The JSON schema defining the required structure for a delivery target receipt.
  - `promptops/validators/validate-delivery-target-receipt.sh`: The validation script to check files against the schema.
- **Modify**:
  - `docs/status/CONTRACTS.md`: Update the current version to Completed.
  - `docs/progress/CONTRACTS.md`: Append the completed task entry.
  - `.jules/CONTRACTS.md`: Append the learning journal entry (if needed).
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/delivery-target.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - **Format**: JSON Schema (Draft 2020-12)
  - **Required Fields**:
    - `receipt_id`: Unique identifier for the receipt.
    - `target_id`: The ID of the delivery target.
    - `package_digest`: The SHA-256 digest of the package delivered.
    - `timestamp`: The ISO 8601 timestamp of when the delivery was received.
    - `status`: The status of the delivery receipt (e.g., success, failed).
  - **Optional Fields**:
    - `message`: Additional information or error message.
    - `metadata`: Key-value pairs of any extra delivery context.
- **Content Digest Convention**:
  - `package_digest` stores the SHA-256 of the delivered package (e.g., `sha256:abc123...`).
- **Pseudo-Code**:
  - The `validate-delivery-target-receipt.sh` script will run `ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/delivery-target-receipt.schema.json -d "$1"`.
- **Public Contract Changes**:
  - Exposes new `delivery-target-receipt` schema.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - Create a temporary valid JSON file `test_valid.json`.
  - Create a temporary invalid JSON file `test_invalid.json`.
  - Run `./promptops/validators/validate-delivery-target-receipt.sh test_valid.json` and expect success.
  - Run `./promptops/validators/validate-delivery-target-receipt.sh test_invalid.json` and expect failure.
- **Success Criteria**:
  - Validation script successfully validates conforming JSONs and rejects malformed JSONs.
- **Edge Cases**:
  - Missing required fields, invalid timestamps, or improperly formatted digests should all trigger validation failures.
