#### 1. Context & Goal
- **Objective**: Implement an automated secret scanning workflow.
- **Trigger**: The docs/vision.md and README.md requires "(a) automated scanning (schema validation, secrets detection, obvious policy checks)" as part of the public registry governance.
- **Impact**: Enforces safety by preventing hardcoded API keys and secrets from being committed or promoted, providing an auditable safety gate.

#### 2. File Inventory
- **Create**: `.github/workflows/secret-scan.yml` (Automated secret scanning workflow triggered on PRs)
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `promptops/prompts/`, `promptops/datasets/`

#### 3. Implementation Spec
- **Policy Architecture**: The workflow triggers on PRs modifying `promptops/prompts/**` or `promptops/datasets/**`. It uses a basic scanner (like grep) to detect common secret keywords and fails the check if secrets are found.
- **Workflow Design**:
  - Trigger: `pull_request` on `promptops/prompts/**`, `promptops/datasets/**`
  - Jobs: `scan-secrets` runs on `ubuntu-latest`, checks out the repo, and runs a bash script to grep for secrets.
  - Decision logic: If a secret keyword matches, `exit 1` to fail the status check.
- **CODEOWNERS Patterns**: Handled by existing `.github/CODEOWNERS` (governance-admins).
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Relies on basic grep tools available on GitHub Actions Ubuntu runners.

#### 4. Test Plan
- **Verification**: Run `mkdir -p promptops/prompts/ && echo 'api_key: secret-test-key' > promptops/prompts/test-secret.yaml && grep -i -r -E "secret-test-key" promptops/prompts/ && rm promptops/prompts/test-secret.yaml` to ensure the pattern matches and cleanup succeeds.
- **Success Criteria**: The test command successfully finds the mock secret and returns a non-zero exit code if no secrets are found in the actual codebase.
- **Edge Cases**: False positives on example strings that look like secrets but aren't.
