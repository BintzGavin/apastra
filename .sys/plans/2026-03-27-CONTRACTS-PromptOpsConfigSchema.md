#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for `promptops.config.yaml` to establish project-level defaults for models, thresholds, and baselines.
- **Trigger**: `docs/vision.md` explicitly calls for "Project-level config (`promptops.config.yaml`)" under "Expansion Nouns Requiring Schema", which currently lacks a schema in `promptops/schemas/`.
- **Impact**: Unlocks onboarding velocity by removing repetitive configurations across test suites. The configuration is essential for system-wide standardization.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/promptops-config.schema.json`: The schema definition for project-level configurations.
  - `promptops/validators/validate-promptops-config.sh`: The validation script using ajv.
- **Modify**: None.
- **Read-Only**: `docs/vision.md` (to align on config noun specification).

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (Draft-07), matching the structure of other schemas.
  - Root type: `object`.
  - Properties:
    - `defaults` (object, optional): `model` (string), `temperature` (number, 0-2), `max_tokens` (integer).
    - `thresholds` (object, optional): key-value pairs of metrics (string) to their minimum acceptable values (number, typically 0-1).
    - `baseline` (object, optional): `auto_set` (boolean) to determine if passing results should automatically be set as the new baseline.
- **Content Digest Convention**: N/A for project configs since they are not independently tracked immutable artifacts in the same way as prompt packages or datasets.
- **Pseudo-Code**:
  ```bash
  # Inside validate-promptops-config.sh
  #!/bin/bash
  set -e
  ajv validate -s promptops/schemas/promptops-config.schema.json -d "$1"
  ```
- **Public Contract Changes**: Exports `https://promptops.com/schema/promptops-config.schema.json`.
- **Dependencies**: None from other domains.

#### 4. Test Plan
- **Verification**: Run `promptops/validators/validate-promptops-config.sh` against a valid mock JSON representing a valid config file.
- **Success Criteria**: Validation script succeeds without errors on a well-formed JSON matching the schema.
- **Edge Cases**: Reject negative temperatures, reject string values for thresholds instead of numbers.
