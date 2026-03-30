#### 1. Context & Goal
- **Objective**: Implement the Red-team adversarial generation role-based agent skill.
- **Trigger**: `docs/vision.md` describes a "Red-team" role ("Adversarial QA") that generates adversarial test cases including prompt injection attempts, edge-case inputs, multilingual stress tests, and format-breaking inputs.
- **Impact**: This unlocks automated hardening of prompts by providing developers with pre-generated adversarial datasets to test their prompts against before releasing them.

#### 2. File Inventory
- **Create**: `skills/red-team/SKILL.md` (Defines the Red-team agent skill role and instructions).
- **Modify**: None.
- **Read-Only**: `docs/vision.md`, `promptops/schemas/agent-skill.schema.json`, `promptops/runs/generate_adversarial_cases.py`.

#### 3. Implementation Spec
- **Harness Architecture**: The `generate_adversarial_cases.py` script already exists and fulfills the technical requirement of generating adversarial cases from a prompt spec. The gap is the missing `SKILL.md` definition to expose this capability as a role-based agent skill as defined in `docs/vision.md`.
- **Run Request Format**: N/A for this task.
- **Run Artifact Format**: N/A for this task.
- **Pseudo-Code**: Create a `SKILL.md` file in `skills/red-team/` that instructs the agent to assume the "Adversarial QA" role, read the target prompt spec, and utilize the `generate_adversarial_cases.py` script to generate an adversarial dataset.
- **Baseline and Regression Flow**: N/A
- **Dependencies**: CONTRACTS (`promptops/schemas/agent-skill.schema.json`), RUNTIME (Agent environment to execute the skill).

#### 4. Test Plan
- **Verification**: Check if the `skills/red-team/SKILL.md` file exists and contains the correct role definition.
- **Success Criteria**: `ls -la skills/red-team/SKILL.md` returns successfully.
- **Edge Cases**: Ensure the skill instructions correctly guide the agent to handle prompt specs with and without defined variables.
