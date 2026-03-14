#### 1. Context & Goal
- **Objective**: Implement a community reporting workflow to support issue triage for public registry content.
- **Trigger**: The `docs/vision.md` explicitly requires "(b) community reporting" as part of the moderation procedures for a public registry custodian model.
- **Impact**: Establishes an auditable and actionable path for users to report moderation issues via GitHub issues, fulfilling the governance requirements for public content hosting.

#### 2. File Inventory
- **Create**:
  - `.github/workflows/community-reporting.yml` (Automated workflow for handling community reports)
  - `.github/ISSUE_TEMPLATE/moderation_report.yml` (Issue template for community reporting)
- **Modify**: None
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Policy Architecture**: Provide a structured `.github/ISSUE_TEMPLATE/moderation_report.yml` template to guide reporters. A new GitHub Actions workflow (`.github/workflows/community-reporting.yml`) triggers on the creation of new issues with the label assigned by the template. It automatically assigns the issue to the governance team and posts an initial acknowledgment comment.
- **Workflow Design**:
  - Issue Template: Create a YAML-based issue form with fields for package name, version, and reason for report. Assign the `moderation-report` label automatically.
  - Workflow Trigger: `issues` event with types `[opened]`
  - Conditional: Check if the issue has the label `moderation-report`.
  - Jobs: `triage-report` runs on `ubuntu-latest`.
  - Steps:
    - Add a comment acknowledging receipt of the report using a script.
    - Automatically assign the issue to `@apastra/governance-admins` or defined maintainers based on the CODEOWNERS file.
- **CODEOWNERS Patterns**: Handled by existing `.github/CODEOWNERS`.
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Relies on standard GitHub Actions configurations and GitHub Issue forms.

#### 4. Test Plan
- **Verification**: Run `grep -q "moderation-report" .github/workflows/community-reporting.yml` to verify the label condition is present in the workflow, and check for the issue template's existence using `ls .github/ISSUE_TEMPLATE/moderation_report.yml`.
- **Success Criteria**: The `grep` command returns a 0 exit code, and the `ls` command confirms the issue template is present.
- **Edge Cases**: Issues opened manually without the template or label will not trigger the automated triage workflow.
