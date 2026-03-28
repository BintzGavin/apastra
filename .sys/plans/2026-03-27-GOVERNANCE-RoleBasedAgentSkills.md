#### 1. Context & Goal
- **Objective**: Establish governance policies and required capabilities for role-based agent skills (Review, Red-team, Optimize) to ensure rigorous and controlled prompt hardening.
- **Trigger**: Expansion 4 from docs/vision.md and README.md regarding role specialization and cognitive modes for agent skills.
- **Impact**: Provides explicit governance parameters for role-aware skills ("Paranoid staff prompt engineer", "Adversarial QA", "Performance engineer"), establishing standard operational metrics and thresholds for prompt quality and security reviews.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/role-based-skills.md` (Governing policy for role-based agent capabilities)
- **Modify**: []
- **Read-Only**: [docs/vision.md, README.md, promptops/policies/regression.yaml]

#### 3. Implementation Spec
- **Policy Architecture**: The policy defines the required parameters for each role:
  - *Review* (Staff Engineer): Checks for injection surface, variable hygiene, format contract completeness, and ambiguity.
  - *Red-team* (Adversarial QA): Requires specific adversarial coverage metrics (e.g., multilingual stress tests, format-breaking inputs) during pre-release scans.
  - *Optimize* (Performance Engineer): Defines constraints and thresholds for token usage compression against cost limits.
- **Workflow Design**: The policy sets the requirements for execution. The actual skills are provided by agent environments, but GOVERNANCE establishes the boundaries and validation thresholds.
- **CODEOWNERS Patterns**: No changes required. The `.github/CODEOWNERS` already covers `promptops/policies/`.
- **Dependencies**: The actual RUNTIME implementation of these skills relies on definitions, but the governance rules act as preconditions for any role-based results to be accepted in regression reports.

#### 4. Test Plan
- **Verification**: Review the newly created policy document.
- **Success Criteria**: The policy details the exact requirements for the Review, Red-team, and Optimize roles to support prompt hardening.
- **Edge Cases**: Handles scenarios where tools/skills lack required capabilities by establishing a strict minimum baseline.
