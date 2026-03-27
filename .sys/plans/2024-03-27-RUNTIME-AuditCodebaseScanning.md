#### 1. Context & Goal
- **Objective**: Implement a runtime capability to scan the codebase for hardcoded, untested prompts and output an audit report detailing "prompt debt."
- **Trigger**: The docs/vision.md expansion section explicitly outlines an "Audit codebase scanning" capability to expose prompt debt and prove value in 60 seconds.
- **Impact**: Unlocks the `apastra-audit` agent skill, allowing users to discover embedded prompts (strings, YAML, env vars) that lack versioning or evals.

#### 2. File Inventory
- **Create**: `promptops/runtime/audit.py` (Script to scan codebase and output the audit report)
- **Modify**: `promptops/runtime/cli.py` (Add an `audit` command)
- **Read-Only**: `docs/vision.md` (Audit skill expansion definition)

#### 3. Implementation Spec
- **Resolver Architecture**: The audit tool operates outside the standard resolution chain. It recursively scans the working directory for source files, applying regex heuristics to identify potential hardcoded prompts (e.g., multiline strings with template variables, AI-related function calls). It does not resolve them; it reports them.
- **Manifest Format**: The audit output format will be a JSON report containing the count of detected prompts, their file locations, line numbers, and a calculated severity score ("prompt debt") based on the absence of corresponding `promptops/prompts/` definitions.
- **Pseudo-Code**:
  ```python
  def scan_codebase(directory):
      # Iterate through supported source files
      # Apply heuristics to find string literals resembling prompts
      # Check if they exist in promptops/prompts/
      # Calculate debt score
      # Return JSON report
  ```
- **Harness Contract Interface**: N/A (Does not execute suites)
- **Dependencies**: None from CONTRACTS at this stage (the output is a report, not a validated artifact, but could eventually be standardized).

#### 4. Test Plan
- **Verification**: Run `python -m promptops.runtime.cli audit .` on a repository containing a known hardcoded prompt in a Python file.
- **Success Criteria**: The output JSON report correctly identifies the file, line number, and content of the hardcoded prompt, and flags it as unversioned prompt debt.
- **Edge Cases**: Should ignore files in `.git/`, `node_modules/`, `venv/`, and `promptops/` itself. Should handle various string formats (multiline, template literals).
