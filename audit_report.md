# Codebase Audit Report

## Execution Context

The repository is a PromptOps architecture, `Apastra`. It uses an agent-as-harness mechanism to enforce disciplines across prompt implementations via file-based protocols. The architecture is segregated into multiple domains: `GOVERNANCE`, `RUNTIME`, `CONTRACTS`, and `EVALUATION`.

There exists an artifact branch topology to store artifacts appendingly rather than modifying existing states.

## Missing Execution Plans

During the codebase exploration, a domain backlog script was utilized to compare `.sys/plans` with `docs/status/*.md` and identified several UNEXECUTED plans that reside in the `.sys/plans` directory but are not properly marked as completed or blocked in their respective domain's status file. Some of them might already be implemented.

**GOVERNANCE**
- `2026-04-06-GOVERNANCE-CostBudgetGovernanceCheck.md` (Implementation already exists in `.github/workflows/regression-gate.yml`)
- `2026-04-04-GOVERNANCE-MinimalPlanExceptionFinal23.md`
- `2026-03-15-GOVERNANCE-PromotionApprovalEnforcement.md`
- `2026-03-22-GOVERNANCE-v1.91.0-TrustedPublisherProvenancePolicy.md`
- `2026-03-22-GOVERNANCE-v1.93.0-AutomatedScanRecordsPolicy.md`
- `2026-03-22-GOVERNANCE-v1.92.0-ModerationEscalationPathPolicy.md`
- `2026-03-22-GOVERNANCE-v1.94.0-CommunityReportRecordsPolicy.md`
- `2026-03-16-GOVERNANCE-DeliveryAndPolicies.md`
- `2026-03-11-GOVERNANCE-ImmutableReleaseWorkflow.md`
- `2026-03-15-GOVERNANCE-Delivery-Target-Specs.md`
- `2024-03-25-GOVERNANCE-ConsolidatedCI.md`
- `2026-04-04-GOVERNANCE-MinimalPlanExceptionFinal24.md`
- `2026-03-26-GOVERNANCE-DriftAlertPolicies2.md`
- `2026-03-11-GOVERNANCE-Artifacts-Branch.md`
- `2026-03-12-GOVERNANCE-Conditional-Regression-Gate.md`
- `2026-04-04-GOVERNANCE-MinimalPlanExceptionFinal25.md`
- `2026-03-11-GOVERNANCE-Delivery-Target-Specs.md`
- `2026-03-12-GOVERNANCE-ReusableWorkflows.md`
- `2026-03-15-GOVERNANCE-Complete-CODEOWNERS.md`
- `2026-03-12-GOVERNANCE-Rich-PR-Annotations.md`
- `2026-03-22-GOVERNANCE-v1.90.0-TakedownAppealsPolicy.md`
- `2026-03-10-GOVERNANCE-CODEOWNERS.md`
- `2026-03-15-GOVERNANCE-DeliveryAndPolicies.md`
- `2026-03-15-GOVERNANCE-Delivery-OCI-NPM-Targets-and-Policies.md`
- `2026-03-14-GOVERNANCE-ApprovalStateWorkflow.md`
- `2026-03-14-GOVERNANCE-Minimal-Plan-Exception.md`
- `2024-03-12-GOVERNANCE-DeliverySyncRefactor.md`
- `2026-03-11-GOVERNANCE-Promotion-Record-Workflow.md`
- `2026-03-11-GOVERNANCE-RequiredStatusCheck.md`
- `2026-03-11-GOVERNANCE-EnforceRegressionGate.md`
- `2026-03-10-GOVERNANCE-RequiredStatusCheck.md`
- `2026-11-21-GOVERNANCE-MinimalPlanExceptionFinal26.md`
- `2024-05-20-GOVERNANCE-ArtifactsBranchImplementation.md`
- `2026-04-06-GOVERNANCE-MinimalPlanExceptionFinal27.md`

**CONTRACTS**
- `2026-04-06-CONTRACTS-MinimalPlanExceptionFinal27.md`
- `2024-03-10-CONTRACTS-prompt-spec-schema.md`
- `2026-03-22-CONTRACTS-v0.99.0-ModerationApprovalForPublicListing.md`
- `2026-04-04-CONTRACTS-MinimalPlanExceptionFinal26.md`
- `2026-03-10-CONTRACTS-evaluator-schema.md`
- `2026-11-21-CONTRACTS-MinimalPlanExceptionFinal28.md`
- `2026-11-21-CONTRACTS-MinimalPlanExceptionFinal26.md`
- `2025-04-04-CONTRACTS-MinimalPlanExceptionFinal26.md`
- `2026-03-22-CONTRACTS-v1.0.0-DeliveryTargetReceipt.md`
- `2026-03-10-CONTRACTS-content-digest-convention.md`
- `2026-03-28-CONTRACTS-ObservabilityAdapterConfig.md`
- `2026-03-15-CONTRACTS-run-artifact-provenance.md`
- `2026-03-10-CONTRACTS-suite-schema.md`
- `2026-03-11-CONTRACTS-run-request-and-artifact.md`
- `2026-03-10-CONTRACTS-dataset-schema.md`
- `2024-03-14-CONTRACTS-QuickEval.md`

**RUNTIME**
- `2026-03-20-RUNTIME-v1.69.0-PackagedResolverInMemoryCaching.md`
- `2026-03-27-RUNTIME-AuditCodebaseScanning-v2.md`
- `2026-03-12-RUNTIME-Directory-Resolver.md`
- `2026-04-04-RUNTIME-MinimalPlanExceptionFinal30.md`
- `2026-03-20-RUNTIME-v1.66.0-ResolverProvenanceMetadata.md`
- `2026-04-04-RUNTIME-MinimalPlanExceptionFinal29.md`
- `2024-04-04-RUNTIME-MinimalPlanExceptionFinal47.md`
- `2026-03-15-RUNTIME-NPM-PyPI-Resolver.md`

**EVALUATION**
- `2026-11-21-EVALUATION-MinimalPlanExceptionFinal31.md`
- `2026-11-21-EVALUATION-MinimalPlanExceptionFinal30.md`
- `2026-03-19-EVALUATION-Minimal-Plan-Exception.md`
