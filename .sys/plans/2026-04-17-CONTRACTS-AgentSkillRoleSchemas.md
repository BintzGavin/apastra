#### 1. Context & Goal
- **Objective**: Create the JSON Schema and validator for agent skill roles ("Review", "Red-team", "Optimize").
- **Trigger**: docs/vision.md outlines "Role-based agent skills" as an expansion (Review, Red-team, Optimize) that lack formalized schema representations for their skill definitions or outputs.
- **Impact**: Enables the RUNTIME and EVALUATION domains to orchestrate and execute specialized agent roles using a standardized format.

#### 2. File Inventory
- **Create**:
  - promptops/schemas/agent-skill.schema.json
  - promptops/validators/validate-agent-skill.sh
- **Modify**: []
- **Read-Only**: docs/vision.md

#### 3. Implementation Spec
- **Schema Architecture**:
  - agent-skill.schema.json: JSON Schema defining an agent skill object.
  - Required fields: id (string), role (enum: ["Review", "Red-team", "Optimize"]), description (string), and capabilities (array of strings).
- **Content Digest Convention**: Agent skills follow the standard canonical JSON digest convention.
- **Pseudo-Code**:
  - validate-agent-skill.sh will invoke ajv to validate an agent skill configuration against the schema.
- **Public Contract Changes**: Exports apastra-agent-skill-v1.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run ajv validate -s promptops/schemas/agent-skill.schema.json -d <test-fixture>
- **Success Criteria**: A valid agent skill configuration passes schema validation and a malformed one emits schema errors.
- **Edge Cases**: Missing role, invalid role string.
