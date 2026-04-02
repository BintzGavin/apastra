#### 1. Context & Goal
- **Objective**: Add `tier` and `tags` capability fields to `suite.schema.json`.
- **Trigger**: GOVERNANCE domain is blocked from implementing TieredSuitesPolicy and CapabilityTaggingPolicy. docs/vision.md specifies "Suite tiers" (Smoke, Regression, Full, Release candidate) and "capability tagging".
- **Impact**: Unblocks GOVERNANCE domain. Allows suites to declare their execution tier and capability tags, enabling policy-driven execution and filtering.

#### 2. File Inventory
- **Create**: []
- **Modify**: [promptops/schemas/suite.schema.json]
- **Read-Only**: []

#### 3. Implementation Spec
- **Schema Architecture**: Add `tier` (string, enum: ["smoke", "regression", "full", "release-candidate"], default: "smoke") and `tags` (array of strings, uniqueItems: true) to the properties of `suite.schema.json`.
- **Content Digest Convention**: N/A
- **Pseudo-Code**: N/A
- **Public Contract Changes**: `suite.schema.json` adds `tier` and `tags` properties.
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: Run `ajv-cli validate --spec=draft2020 --strict=false -s promptops/schemas/suite.schema.json -d promptops/suites/test-suite.yaml`. (May need to convert test-suite.yaml to JSON first: `yq . promptops/suites/test-suite.yaml > tmp.json && npx ajv-cli validate --spec=draft2020 --strict=false -s promptops/schemas/suite.schema.json -d tmp.json`)
- **Success Criteria**: Validation succeeds for valid suites with and without the new fields.
- **Edge Cases**: Reject invalid tier names. Reject non-array tags.
