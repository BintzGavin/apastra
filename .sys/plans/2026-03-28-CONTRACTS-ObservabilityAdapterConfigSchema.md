#### 1. Context & Goal
- **Objective**: Create the JSON schema and validator for Observability Adapter Configs to support emitting artifacts to observability systems like Langfuse and OpenTelemetry.
- **Trigger**: We need to define validation schemas for observability delivery targets as outlined in docs/vision.md (Expansion 6).
- **Impact**: Enables the GOVERNANCE and RUNTIME domains to correctly configure and validate observability bridge adapters.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/observability-adapter.schema.json`
  - `promptops/validators/validate-observability-adapter.sh`
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`
  - `README.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Create `promptops/schemas/observability-adapter.schema.json` to define the configuration for observability bridges.
  - Required fields: `type` (string, e.g., `langfuse`, `opentelemetry`), `endpoint` (string), and `emit` (array of strings, e.g., `scorecard`, `regression_report`, `run_manifest`, `cases`).
  - Additional optional fields may include authentication parameters or specific payload mappings based on the `type`.
- **Content Digest Convention**: Adapters are configured declaratively, typically within delivery targets, and should be validated against this schema.
- **Pseudo-Code**:
  - Define JSON schema for the adapter configuration.
  - Write a bash script (`validate-observability-adapter.sh`) using `ajv` to validate instances against the schema.
- **Public Contract Changes**:
  - Introduces a new public schema: `observability-adapter.schema.json`.
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: Run `./promptops/validators/validate-observability-adapter.sh test-fixtures/valid-observability-adapter.yaml` (assuming a fixture is created).
- **Success Criteria**: Valid configurations pass schema validation, while invalid ones (e.g., missing `type` or `endpoint`) are rejected.
- **Edge Cases**: Reject configurations with unsupported `emit` artifact types or malformed endpoints.
