### GOVERNANCE v0.2.0
- ✅ Completed: CODEOWNERS File Creation - Created .github/CODEOWNERS with required review boundaries.

### GOVERNANCE v0.3.0
- ✅ Completed: Promotion Record Workflow - Created automated workflow to append promotion records upon governed releases.

### GOVERNANCE v0.4.0
- ✅ Completed: Immutable Release Workflow - Created .github/workflows/immutable-release.yml to package prompts, compute digest, and create a GitHub Release when tags are pushed.

### GOVERNANCE v0.5.0
- ✅ Completed: Required Status Check - Created regression gate workflow and base regression policy.

### GOVERNANCE v0.6.0
- ✅ Completed: Delivery Target Specs - Implemented delivery target schema configs and a workflow to sync downstream.

### GOVERNANCE v0.7.0
- ✅ Completed: Rulesets - Configured conceptual rulesets for main branch protection and tag immutability.

### GOVERNANCE v0.8.0
- ✅ Completed: Reusable Workflows - Standardized workflows with workflow_call and checkout@v4, gracefully bypassed missing regression engine.

### GOVERNANCE v0.9.0
- ✅ Completed: Artifacts Branch - Spec designed to isolate derived data on promptops-artifacts branch.

### GOVERNANCE v1.0.0
- ✅ Completed: Artifacts Branch Implementation - Configured workflows to isolate derived artifacts on promptops-artifacts branch.

### GOVERNANCE v1.1.0
- ✅ Completed: Approval State Workflow - Created automated workflow to append approval records upon human review.

### GOVERNANCE v1.2.0
- ✅ Completed: Promotion Approval Enforcement - Enforced that promotions require a matching approved Approval State record in promote.yml.

### GOVERNANCE v1.3.0
- ✅ Completed: Enforce Regression Gate - Removed bypass in regression-gate.yml to block merges when regression report is missing.

### GOVERNANCE v1.4.0
- ✅ Completed: Delivery Sync Refactor - Fixed delivery target sync to operate within the promptops-artifacts branch topology.

### GOVERNANCE v1.5.0
- ✅ Completed: Conditional Regression Gate - Bypassed regression check for PRs modifying non-evaluable files using tj-actions/changed-files.

### GOVERNANCE v1.6.0
- ✅ Completed: Rich PR Annotations - Enhanced the regression gate workflow to provide rich PR annotations and a detailed Markdown summary of regression evidence.

### GOVERNANCE v1.7.0
- ✅ Completed: Minimal Plan Exception - Acknowledged all GOVERNANCE vision gaps are complete.

### GOVERNANCE v1.8.0
- ✅ Completed: Promotion Approval Enforcement - Fixed jq logic in promote.yml to properly pipe approvals/*.json contents.

### GOVERNANCE v1.9.0
- ✅ Completed: ModerationAndGovernancePolicies - Implemented acceptable use, deprecation, and ownership dispute policies and automated moderation scan workflow.

### GOVERNANCE v1.10.0
- ✅ Completed: ArtifactAttestations - Added build provenance attestations to immutable-release.yml.

### GOVERNANCE v1.11.0
- ✅ Completed: SecretScan - Implemented automated secret scanning workflow.

### GOVERNANCE v1.12.0
- ✅ Completed: CommunityReportingWorkflow - Implemented an automated workflow and issue template for handling community moderation reports.

### GOVERNANCE v1.13.0
- ✅ Completed: Consolidated CI - Implemented simplified two-workflow setup.

### GOVERNANCE v1.14.0
- ✅ Completed: Node20DeprecationFix - Injected FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 into GitHub Actions workflows.

### GOVERNANCE v1.15.0
- ✅ Completed: Minimal Plan Exception Final - Acknowledged all GOVERNANCE vision gaps are complete.
- ✅ Completed: Naming Policy - Implemented naming and rename policy.

### GOVERNANCE v1.16.0
- ✅ Completed: ArtifactAttestations - Minimal Plan Exception. Changes already present.

### GOVERNANCE v1.17.0
- ✅ Completed: TrustedPublisherBadges - Added trusted-publisher.md policy and codeowners.

### GOVERNANCE v1.18.0
- ✅ Completed: ArtifactAttestations - Pinned GitHub Action SHA in immutable-release.yml

### GOVERNANCE v1.18.1
- ✅ Completed: StrictPinning - Pinned GitHub Action SHAs in all workflows.

### GOVERNANCE v1.19.0
- ✅ Completed: Complete CODEOWNERS - Added missing paths for CONTRACTS, EVALUATION, and RUNTIME to .github/CODEOWNERS.

### GOVERNANCE v1.20.0
- ✅ Completed: MissingPoliciesAndTargets - Implemented missing delivery targets (OCI, npm, PyPI) and takedown/appeals governance policies.

### GOVERNANCE v1.21.0
- ✅ Completed: MinimalPlanExceptionFinal - Acknowledged all GOVERNANCE vision gaps are complete.

### GOVERNANCE v1.22.0
- ✅ Completed: FederationAndMirrors - Specified the mirror protocol and optional federation policy.

### GOVERNANCE v1.23.0
- ✅ Completed: MinimalPlanExceptionFinal - Acknowledged all GOVERNANCE vision gaps are complete.
