**Version**: 1.8.0

[v0.2.0] ✅ Completed: CODEOWNERS File Creation - Created .github/CODEOWNERS with required review boundaries.

Blocked: waiting for stable EVALUATION regression report schema
Blocked: waiting for CONTRACTS regression policy schema
[v0.3.0] ✅ Completed: Promotion Record Workflow - Created automated workflow to append promotion records upon governed releases.
Blocked: waiting for CONTRACTS delivery target schema
Blocked: waiting for CONTRACTS promotion record schema
[v0.4.0] ✅ Completed: Immutable Release Workflow - Created .github/workflows/immutable-release.yml to package prompts, compute digest, and create a GitHub Release when tags are pushed.
[v0.5.0] ✅ Completed: Required Status Check - Created regression gate workflow and base regression policy.
[v0.6.0] ✅ Completed: Delivery Target Specs - Implemented delivery target schema configs and a workflow to sync downstream.
[v0.7.0] ✅ Completed: Rulesets - Configured conceptual rulesets for main branch protection and tag immutability.
[v0.8.0] ✅ Completed: Reusable Workflows - Standardized workflows with workflow_call and checkout@v4, gracefully bypassed missing regression engine.
[v0.9.0] ✅ Completed: Artifacts Branch - Spec designed to isolate derived data on promptops-artifacts branch.
[v1.0.0] ✅ Completed: Artifacts Branch Implementation - Configured workflows to isolate derived artifacts on promptops-artifacts branch.
[v1.1.0] ✅ Completed: Approval State Workflow - Created automated workflow to append approval records upon human review.
[v1.2.0] ✅ Completed: Promotion Approval Enforcement - Enforced that promotions require a matching approved Approval State record in promote.yml.
[v1.3.0] ✅ Completed: Enforce Regression Gate - Removed bypass in regression-gate.yml to block merges when regression report is missing.
[v1.4.0] ✅ Completed: Delivery Sync Refactor - Fixed delivery target sync to operate within the promptops-artifacts branch topology.
[v1.5.0] ✅ Completed: Conditional Regression Gate - Bypassed regression check for PRs modifying non-evaluable files using tj-actions/changed-files.
[v1.6.0] ✅ Completed: Rich PR Annotations - Enhanced the regression gate workflow to provide rich PR annotations and a detailed Markdown summary of regression evidence.
[v1.7.0] ✅ Completed: Minimal Plan Exception - Acknowledged all GOVERNANCE vision gaps are complete.
[v1.8.0] ✅ Completed: Promotion Approval Enforcement - Fixed jq logic in promote.yml to properly pipe approvals/*.json contents.
