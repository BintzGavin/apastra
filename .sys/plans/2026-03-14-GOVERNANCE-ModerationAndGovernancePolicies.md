#### 1. Context & Goal
- **Objective**: Implement moderation and governance hardening policies.
- **Trigger**: `docs/vision.md` phase 4 requires moderation and governance hardening, including acceptable use and deprecation policies.
- **Impact**: Provides clear guidelines for acceptable use, deprecation, and ownership disputes, improving overall platform safety and trust.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/acceptable-use.md` (Acceptable Use Policy)
  - `promptops/policies/deprecation.md` (Deprecation Policy)
  - `promptops/policies/ownership-disputes.md` (Ownership Dispute Policy)
  - `.github/workflows/moderation-scan.yml` (Automated moderation scan workflow)
- **Modify**: None
- **Read-Only**: `docs/vision.md` sections on Moderation and governance hardening.

#### 3. Implementation Spec
- **Policy Architecture**:
  - Define clear rules and guidelines in markdown format for acceptable use, deprecation, and ownership disputes.
  - The `moderation-scan.yml` workflow will trigger on pull requests and use a basic text-scanning script or external action to flag potentially inappropriate content based on keywords defined in a configuration file or the workflow itself.
- **Workflow Design**:
  ```yaml
  name: Moderation Scan
  on:
    pull_request:
      paths:
        - 'promptops/prompts/**'
        - 'promptops/datasets/**'
  jobs:
    scan:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Run basic keyword scan
          run: |
            # Pseudo-code for scanning
            grep -i -E "blocked_keyword_1|blocked_keyword_2" promptops/prompts/* promptops/datasets/* || true
  ```
- **CODEOWNERS Patterns**:
  - Add specific reviewers (e.g., `@apastra/trust-and-safety`) for `promptops/policies/acceptable-use.md`, `promptops/policies/deprecation.md`, and `promptops/policies/ownership-disputes.md` to `.github/CODEOWNERS`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Create a test PR containing a blocked keyword in a prompt or dataset and verify that the `moderation-scan.yml` workflow flags it.
- **Success Criteria**: The workflow successfully runs on relevant PRs and correctly identifies policy violations.
- **Edge Cases**: False positives in the moderation scan; ensure there's a clear process for reviewing and overriding flagged content.
