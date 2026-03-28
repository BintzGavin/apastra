#### 1. Context & Goal
- **Objective**: Implement the `apastra-audit` skill workflow to scan a codebase for hardcoded prompts and generate a prompt debt report.
- **Trigger**: The "Proposed expansions" section in `docs/vision.md` outlines an `apastra-audit` feature to scan codebases for untested, hardcoded prompts and report "prompt debt".
- **Impact**: This unlocks the ability for users to quantify their prompt debt, driving adoption by proving value in 60 seconds.

#### 2. File Inventory
- **Create**:
  - `promptops/runs/audit-shim.sh`: Script to execute the audit scan.
- **Modify**: []
- **Read-Only**:
  - `docs/vision.md`: Provides the vision for the audit feature.
  - `promptops/schemas/audit-report.schema.json`: Schema for the audit report artifact.

#### 3. Implementation Spec
- **Harness Architecture**: The audit workflow acts as a specialized harness. It takes a target directory as input, scans for common prompt patterns (strings, template literals, YAML, env vars), and outputs an `audit_report.json` artifact.
- **Run Request Format**: N/A - triggered directly via CLI.
- **Run Artifact Format**: `audit_report.json` conforming to `audit-report.schema.json`. Contains total prompt count, untested count, severity score, and specific locations.
- **Pseudo-Code**:
  ```bash
  # audit-shim.sh
  # 1. Accept target directory argument
  # 2. Use grep/rg to scan for common prompt keywords or large string literals
  # 3. Aggregate findings
  # 4. Calculate severity score based on findings
  # 5. Output audit_report.json
  ```
- **Baseline and Regression Flow**: N/A for audit reports.
- **Dependencies**:
  - CONTRACTS schema: `promptops/schemas/audit-report.schema.json`

#### 4. Test Plan
- **Verification**: Run `bash promptops/runs/audit-shim.sh .` and verify `audit_report.json` is generated.
- **Success Criteria**: `audit_report.json` exists, is valid JSON, and matches the expected schema.
- **Edge Cases**: Empty codebase, codebase with no prompts, codebase with many prompts.
