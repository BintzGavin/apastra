#### 1. Context & Goal
- **Objective**: Define the execution architecture for the Audit Skill to scan codebases for prompt debt.
- **Trigger**: The vision outlines Expansion 1 Audit skill zero-config first contact which requires a mechanism to scan projects, discover unversioned/untested prompts, and emit an audit report.
- **Impact**: Unlocks the zero-config onboarding wedge by proving value immediately, satisfying a critical expansion goal.

#### 2. File Inventory
- **Create**:
  - promptops/harnesses/audit-shim.sh: The execution script that runs the audit logic and emits the report.
- **Modify**: []
- **Read-Only**:
  - promptops/schemas/audit-report.schema.json
  - docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: The audit-shim.sh acts as a specialized harness. It takes a target directory as input, scans for common prompt patterns, and checks if they have corresponding specs/tests in the promptops directories.
- **Run Request Format**: N/A - Audit is a zero-config first contact tool, it runs directly on a directory path.
- **Run Artifact Format**: Emits an audit_report.json conforming to audit-report.schema.json containing total prompts found, untested count, and severity score.
- **Pseudo-Code**:
  # audit-shim.sh target_dir
  scan target_dir for prompt patterns -> hardcoded_prompts
  scan promptops/prompts/ for existing specs -> managed_prompts
  compare lists to find unversioned/untested
  calculate severity score
  emit audit_report.json
- **Dependencies**: CONTRACTS audit-report.schema.json must exist.

#### 4. Test Plan
- **Verification**: Run audit-shim.sh on a dummy directory and validate the output against audit-report.schema.json.
- **Success Criteria**: The shim successfully produces a valid audit_report.json with the correct schema fields.
- **Edge Cases**: Empty target directory, no prompts found, all prompts already managed.
