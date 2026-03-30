#### 1. Context & Goal
- **Objective**: Identify the missing "Role-based agent skills" (`Expansion 4`) from the vision document, specifically Review, Red-team, and Optimize skills.
- **Trigger**: The vision document explicitly lists Role-based agent skills as a P1 expansion to provide specialized cognitive modes beyond basic workflow execution.
- **Impact**: Provides users with specialized agent personas ("Paranoid staff prompt engineer", "Adversarial QA", "Performance engineer") that analyze, stress-test, and compress prompts, significantly hardening prompt quality. This satisfies the Expansion 4 requirement for the runtime domain.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/agent_skills.py` (New file for the specialized agent skills)
- **Modify**:
  - `promptops/runtime/cli.py` (To expose new CLI commands for the skills)
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/agent-skill.schema.json`

#### 3. Implementation Spec
- **Architecture**: The `agent_skills.py` module will define the three specialized skills (Review, Red-team, Optimize). Each skill reads a prompt spec and applies role-based logic (e.g., generating adversarial cases, analyzing token usage, reviewing for ambiguity).
- **Manifest Format**: Uses existing `prompt-spec` and `dataset-case` schemas. The skills conform to the `agent-skill` schema.
- **Pseudo-Code**:
  1. Define a `ReviewSkill` that reads a `prompt-spec` and outputs a review report.
  2. Define a `RedTeamSkill` that reads a `prompt-spec` and outputs adversarial `dataset-case`s.
  3. Define an `OptimizeSkill` that reads a `prompt-spec` and outputs compression suggestions.
  4. Register these skills in the CLI (`apastra-review`, `apastra-red-team`, `apastra-optimize`).
- **Harness Contract Interface**:
  - Input: Prompt spec file path.
  - Output: Specialized analysis report or generated dataset cases.
- **Dependencies**:
  - `promptops/schemas/agent-skill.schema.json`

#### 4. Test Plan
- **Verification**: Run `apastra-review`, `apastra-red-team`, and `apastra-optimize` on a sample `prompt-spec` using the CLI.
- **Success Criteria**: Each command successfully processes the prompt spec and outputs the expected role-specific artifact.
- **Edge Cases**: Malformed prompt specs, empty templates, missing variables.
