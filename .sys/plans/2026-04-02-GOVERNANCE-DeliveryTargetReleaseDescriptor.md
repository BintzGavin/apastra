#### 1. Context & Goal
- **Objective**: Implement a delivery target config for posting signed release descriptors to an internal API.
- **Trigger**: `docs/vision.md` explicitly lists "Post a signed 'release descriptor' to an internal API" as an abstract delivery target primitive that does not yet exist in `promptops/delivery/`.
- **Impact**: Enables automated delivery workflows to sync approved prompt packages to internal, custom API endpoints via cryptographically verifiable release descriptors.

#### 2. File Inventory
- **Create**: `promptops/delivery/release-descriptor-target.yaml` (Delivery target configuration for internal API webhook)
- **Modify**: N/A
- **Read-Only**: `docs/vision.md` (Delivery targets section), `promptops/schemas/delivery-target.schema.json`

#### 3. Implementation Spec
- **Policy Architecture**: The delivery target will define the endpoint, authentication method (e.g., token injected via Actions secrets), and payload configuration (enabling the `release-descriptor` payload format) for the webhook.
- **Workflow Design**: The existing `deliver.yml` workflow will read this target and issue the authenticated POST request using the generic delivery actions.
- **CODEOWNERS Patterns**: Handled by existing `promptops/delivery/` mapping.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: Add a new `type: internal_api` target with fields for `endpoint`, `auth_header`, and `payload_format: release_descriptor`.
- **Dependencies**: CONTRACTS must have `release-descriptor.schema.json` (Assumed fulfilled or planned independently).

#### 4. Test Plan
- **Verification**: Run `npx ajv-cli validate -s promptops/schemas/delivery-target.schema.json -d <(yq . promptops/delivery/release-descriptor-target.yaml > target.json && cat target.json) --spec=draft2020 --strict=false`.
- **Success Criteria**: The `release-descriptor-target.yaml` configuration is valid against the existing delivery target schema and successfully describes the internal API endpoint.
- **Edge Cases**: Missing secrets for API authentication must cause the delivery workflow to fail closed.
