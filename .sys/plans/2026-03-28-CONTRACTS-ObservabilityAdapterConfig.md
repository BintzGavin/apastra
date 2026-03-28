#### 1. Context & Goal
- **Objective**: Create the JSON schema and validator for an Observability adapter config.
- **Trigger**: The docs/vision.md identifies "Observability adapter config" as a missing expansion noun.
- **Impact**: Unlocks the ability to format and emit execution artifacts to external observability systems like Langfuse or OpenTelemetry securely and consistently.

#### 2. File Inventory
- **Create**: promptops/schemas/observability-adapter-config.schema.json (JSON schema for the config)
- **Create**: promptops/validators/validate-observability-adapter-config.sh (Shell script wrapper to validate configs against the schema using ajv)
- **Modify**: docs/status/CONTRACTS.md (Update completion status)
- **Modify**: docs/progress/CONTRACTS.md (Append progress entry)
- **Read-Only**: docs/vision.md, README.md, promptops/schemas/*, promptops/validators/*

#### 3. Implementation Spec
- **Schema Architecture**: A JSON Schema representing the Observability adapter config. Required fields include id (string), type (e.g. enum: langfuse, opentelemetry), endpoint (URL string), and optionally credentials (or reference to them) and mapping_rules.
- **Content Digest Convention**: N/A for this simple config initially.
- **Pseudo-Code**: Validation script calls ajv validate -s promptops/schemas/observability-adapter-config.schema.json -d <data>
- **Public Contract Changes**: Exports the observability-adapter-config schema ID.
- **Dependencies**: No immediate runtime dependencies, but GOVERNANCE/RUNTIME will use this to configure telemetry emitting later.

#### 4. Test Plan
- **Verification**: ajv validate -s promptops/schemas/observability-adapter-config.schema.json -d test-fixtures/valid-observability-adapter-config.json
- **Success Criteria**: Validation exits with 0 for a valid config file mapping correctly.
- **Edge Cases**: Missing endpoint or unsupported adapter type should fail validation.
