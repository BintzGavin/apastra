#### 1. Context & Goal
- **Objective**: Implement role-based agent skills (Review, Red-team, Optimize) for specialized prompt engineering workflows.
- **Trigger**: `docs/vision.md` explicitly calls out "Role-based agent skills" (`Expansion 4`) as a P1 expansion to provide specialized cognitive modes beyond workflow execution.
- **Impact**: Provides users with specialized agent personas ("Paranoid staff prompt engineer", "Adversarial QA", "Performance engineer") that analyze, stress-test, and compress prompts, significantly hardening prompt quality.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/agent_skills.py` (New file to house the specialized agent skill implementations)
- **Modify**:
  - `promptops/runtime/cli.py` (To expose the new agent skills as CLI commands)
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/agent-skill.schema.json`
  - `promptops/schemas/prompt-spec.schema.json`

#### 3. Implementation Spec
- **Architecture**: The `agent_skills.py` module will define the three specialized skills (Review, Red-team, Optimize). Each skill will take a prompt spec as input and apply its specific role-based logic (e.g., generating adversarial cases, analyzing token usage, reviewing for ambiguity).
- **Manifest Format**: Uses existing `prompt-spec` and `dataset-case` schemas. The skills themselves will conform to the `agent-skill` schema if they are defined as configuration.
- **Pseudo-Code**:
  1. Define a `ReviewSkill` that reads a `prompt-spec` and outputs a review report.
  2. Define a `RedTeamSkill` that reads a `prompt-spec` and outputs adversarial `dataset-case`s.
  3. Define an `OptimizeSkill` that reads a `prompt-spec` and outputs compression suggestions and cost estimates.
  4. Register these skills in the CLI so users can invoke them via `apastra-review`, `apastra-red-team`, and `apastra-optimize`.
- **Harness Contract Interface**:
  - Input: Prompt spec file path.
  - Output: Specialized analysis report or generated dataset cases.
- **Dependencies**:
  - `promptops/schemas/agent-skill.schema.json`
  - `promptops/schemas/prompt-spec.schema.json`

#### 4. Test Plan
- **Verification**: Run `apastra-review`, `apastra-red-team`, and `apastra-optimize` on a sample `prompt-spec` using the CLI.
- **Success Criteria**: Each command successfully processes the prompt spec and outputs the expected role-specific artifact (review report, adversarial cases, or optimization suggestions).
- **Edge Cases**: Malformed prompt specs, empty templates, missing variables.
