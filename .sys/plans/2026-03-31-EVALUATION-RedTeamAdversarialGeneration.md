#### 1. Context & Goal
- **Objective**: Spec the creation of a Red-team adversarial generation skill for agents.
- **Trigger**: `docs/vision.md` outlines "Role-based agent skills" including "Red-team" ("Adversarial QA") to generate adversarial test cases like prompt injection, edge cases, and format breaks.
- **Impact**: Enables automated prompt hardening by giving agents a specialized role for adversarial QA generation, feeding into robust evaluations.

#### 2. File Inventory
- **Create**: `skills/red-team/SKILL.md` (Role definition and execution instructions)
- **Modify**: None.
- **Read-Only**: `docs/vision.md`, `promptops/schemas/agent-skill.schema.json`, `promptops/runs/generate_adversarial_cases.py`

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Pseudo-Code**: Create `skills/red-team/SKILL.md`. The instructions should define the agent's role as "Adversarial QA". It should instruct the agent to read a target prompt spec and utilize the existing `promptops/runs/generate_adversarial_cases.py` script to output a dataset containing adversarial inputs (e.g., prompt injections, boundary violations, multilingual edge cases, empty values). The skill should conform implicitly or explicitly to the `agent-skill.schema.json`.
- **Baseline and Regression Flow**: N/A
- **Dependencies**: CONTRACTS (`promptops/schemas/agent-skill.schema.json`)

#### 4. Test Plan
- **Verification**: Run `ls -la skills/red-team/SKILL.md` to ensure the file is created. Run `npx ajv-cli validate -s promptops/schemas/agent-skill.schema.json -d skills/red-team/SKILL.md` if the markdown contains a frontmatter JSON/YAML block conforming to the schema.
- **Success Criteria**: The skill file exists and correctly instructs an agent to use `generate_adversarial_cases.py`.
- **Edge Cases**: The target prompt spec has no variables (the script handles this by creating a global injection case).
