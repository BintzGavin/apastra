#### 1. Context & Goal
- **Objective**: Implement the Audit Skill execution flow to scan codebases for prompt debt and generate a standardized audit report.
- **Trigger**: The vision document proposes an "Audit skill" (Expansion 1) to scan for hardcoded prompts and emit a severity score report. The RUNTIME domain has a basic scanning module (`promptops/runtime/audit.py`), but EVALUATION needs a runnable workflow that ties this into an emitted `audit_report.json` validated against `promptops/schemas/audit-report.schema.json`.
- **Impact**: Unlocks the zero-config first contact wedge, allowing users (and agents) to run a single script that exposes prompt debt in their codebase, accelerating onboarding and fulfilling a P0 expansion priority.

#### 2. File Inventory
- **Create**: `promptops/runs/audit-shim.sh` (Bash script to execute the audit scan and format the output into a valid `audit-report.json`)
- **Modify**: None.
- **Read-Only**: `promptops/schemas/audit-report.schema.json` (for output validation), `promptops/runtime/audit.py` (runtime execution), `docs/vision.md` (Expansion 1 specification).

#### 3. Implementation Spec
- **Harness Architecture**:
  - The script (`audit-shim.sh`) will act as an executable workflow.
  - It will invoke `promptops/runtime/audit.py` (or a brief inline python snippet that wraps it) to perform the codebase scan.
  - It will capture the results and transform them into the exact structure required by `audit-report.schema.json`:
    - `timestamp`: Current ISO 8601 date-time.
    - `scanned_paths`: The directories scanned (e.g., `["."]`).
    - `total_prompts`: The count of detected prompts.
    - `untested_prompts`: For this wedge, defaults to the total count of unversioned prompts.
    - `unversioned_prompts`: The count of detected prompts.
    - `severity_score`: The computed debt score.
    - `findings`: A list of objects containing `file_path`, `issue_type` (e.g., "hardcoded_prompt"), and `suggestion`.
- **Run Request Format**: N/A (this is a direct execution script, not a suite runner).
- **Run Artifact Format**: The script will output an `audit_report.json` file to the specified output directory.
- **Pseudo-Code**:
  1. Accept an output directory argument.
  2. Run a Python wrapper around `promptops/runtime/audit.py` to get the raw findings.
  3. Format the raw findings into the `audit-report.json` structure.
  4. Save the formatted JSON to the output directory.
  5. Validate the generated JSON using `ajv-cli` against `promptops/schemas/audit-report.schema.json`.
- **Baseline and Regression Flow**: N/A.
- **Dependencies**: `promptops/schemas/audit-report.schema.json` (CONTRACTS), `promptops/runtime/audit.py` (RUNTIME).

#### 4. Test Plan
- **Verification**: Run `bash promptops/runs/audit-shim.sh ./test-audit-output`.
- **Success Criteria**: The script exits with 0, produces an `audit_report.json` in `./test-audit-output`, and the file passes schema validation against `audit-report.schema.json`.
- **Edge Cases**: Empty codebase (no prompts found), missing output directory (should create it).
