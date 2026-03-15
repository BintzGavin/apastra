---
title: "Domain Status Overview"
description: "Overview of status for all domains"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "docs/status/CONTRACTS.md"
  - "docs/status/DOCS.md"
  - "docs/status/EVALUATION.md"
  - "docs/status/GOVERNANCE.md"
  - "docs/status/RUNTIME.md"
---

# Domain Status Overview

## CONTRACTS

**Version**: 0.33.0

[v0.2.0] ✅ Completed: prompt-spec-schema - Created prompt-spec.schema.json and validate-prompt-spec.sh
[v0.3.0] ✅ Completed: dataset-schema - Created dataset-manifest.schema.json, dataset-case.schema.json, and validate-dataset.sh
[v0.4.0] ✅ Completed: evaluator-schema - Created evaluator.schema.json and validate-evaluator.sh
[v0.5.0] ✅ Completed: suite-schema - Created suite.schema.json and validate-suite.sh
[v0.6.0] ✅ Completed: content-digest-convention - Created digest-convention.md and compute-digest.sh
[v0.7.0] ✅ Completed: ConsumptionManifestSchema - Created consumption-manifest.schema.json and validate-consumption-manifest.sh
[v0.8.0] ✅ Completed: HarnessAdapterSchema - Created harness-adapter.schema.json and validate-harness-adapter.sh
[v0.9.0] ✅ Completed: run-request-and-artifact - Created run-request.schema.json, run-artifact.schema.json, validate-run-request.sh, and validate-run-artifact.sh
[v0.10.0] ✅ Completed: ScorecardAndRegressionReport - Created scorecard.schema.json, regression-report.schema.json, and validators
[v0.11.0] ✅ Completed: GovernanceSchemas - Created regression-policy.schema.json, promotion-record.schema.json, delivery-target.schema.json and validators
[v0.12.0] ✅ Completed: BaselineSchema - Created baseline.schema.json and validate-baseline.sh
[v0.13.0] ✅ Completed: PromptPackage - Created prompt-package.schema.json and validate-prompt-package.sh
[v0.14.0] ✅ Completed: ArtifactRefsSchema - Created artifact-refs.schema.json and validate-artifact-refs.sh
[v0.15.0] ✅ Completed: ApprovalStateSchema - Created approval-state.schema.json and validate-approval-state.sh
[v0.16.0] ✅ Completed: RunArtifactFiles - Created schemas and validators for run-manifest, run-case, and run-failures.
[v0.17.0] ✅ Completed: ProviderArtifactSchema - Created provider-artifact.schema.json and validate-provider-artifact.sh
[v0.18.0] ✅ Completed: InitialPromptSpec - Created first prompt instance prompt.yaml
[v0.19.0] ✅ Completed: InitialDataset - Created first dataset instance test-dataset
[v0.20.0] ✅ Completed: InitialEvaluator - Created first evaluator instance exact-match.yaml
[v0.21.0] ✅ Completed: InitialSuite - Created first suite instance test-suite.yaml
[v0.22.0] ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.
[v0.23.0] ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.
[v0.23.0] ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.
[v0.24.0] ✅ Completed: QuickEvalAndInlineAssertions - Defined schemas for Quick Eval Mode and Inline Assertions.
[v0.25.0] ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.
[v0.26.0] ✅ Completed: InitialQuickEval - Created first quick eval instance in promptops/evals/my-eval.yaml
[v0.27.0] ✅ Completed: InitialPromptPackage - Created first prompt package instance my-prompt-package/package.yaml
[v0.28.0] ✅ Completed: Minimal Plan Exception Final - Triggered minimal plan exception as all required schemas, validation scripts, and initial instances have been fully implemented and verified.
[v0.29.0] ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception.
[v0.30.0] ✅ Completed: InitialQuickEval - Created missing initial quick eval instance in promptops/evals/my-eval.yaml
[v0.31.0] ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception as all required schemas, validation scripts, and initial instances have been fully implemented and verified.
[v0.32.0] ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception as all required schemas, validation scripts, and initial instances have been fully implemented and verified.
[v0.33.0] ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception.


## DOCS

**Version**: 0.4.0

[v0.1.0] ✅ Completed: Daily Documentation Review - Initialized comprehensive daily documentation review process. Created all required dashboards, generated API references for all existing schemas, and verified documentation completeness against implemented features.

[v0.2.0] ✅ Completed: Daily Documentation Review - Updated API documentation, guides, ADRs, and cross-domain dashboards based on latest implementation.

[v0.3.0] ✅ Completed: Daily Documentation Review - Updated API documentation, dashboards, and domain contexts based on current implementation.

[v0.4.0] ✅ Completed: Daily Documentation Review - Updated API documentation, dashboards, and schema dependency graph based on current implementation.


## EVALUATION

**Version**: 0.19.3

[v0.1.1] ✅ Completed: HarnessAdapterContract - Verified schema availability and created domain directories
Blocked: waiting for GOVERNANCE policy promptops/policies/regression.yaml
[v0.2.0] ✅ Completed: HarnessAdapterContract - Implemented reference BYO harness adapter config and execution script
[v0.3.0] ✅ Completed: RunRequestValidation - Implemented run request validation script
[v0.4.0] ✅ Completed: BaselineEstablishment - Verified schema availability and created baselines directory structure
[v0.5.0] ✅ Completed: RegressionComparisonEngine - Implemented CLI script for regression comparison
[v0.6.0] ✅ Completed: ScorecardNormalization - Implemented standalone scorecard normalizer
[v0.7.0] ✅ Completed: BaselineEstablishmentWorkflow - Implemented bash script to establish baselines
[v0.8.0] ✅ Completed: RunArtifactGeneration - Implemented script to split monolithic run_artifact.json into distinct, append-friendly files.
[v0.9.0] ✅ Completed: ScorecardNormalizationRefactor - Refactored normalize.py to read cases.jsonl and output scorecard.json

[v0.10.0] ✅ Completed: RegressionComparisonRefactor - Refactored Regression Engine to read split scorecard.json files
[v0.11.0] ✅ Completed: RegressionReportWorkflow - Implemented regression report generation and storage workflow
[v0.12.0] ✅ Completed: ReferenceAdapterRefactor - Refactored reference adapter to natively support split artifacts and updated scorecard normalizer execution
[v0.12.1] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.12.2] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.12.3] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.13.0] ✅ Completed: QuickEvalMode - Implemented quick eval mode pipeline and adapted reference harness
[v0.14.0] ✅ Completed: InlineAssertions - Implemented deterministic inline assertions evaluation engine.
[v0.15.0] ✅ Completed: ModelAssistedAssertions - Implemented model-assisted and performance assertion types in the deterministic evaluation engine
[v0.16.0] ✅ Completed: TrialsAndVarianceSupport - Implemented trials support in reference adapter and variance calculation in scorecard normalizer
[v0.17.0] ✅ Completed: JsonSchemaAssertion - Implemented the is-valid-json-schema assertion type for inline evaluation
[v0.17.1] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.18.0] ✅ Completed: Minimal Plan Exception Final - All plans officially complete
[v0.18.1] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.19.0] ✅ Completed: PerformanceAssertions - Implemented latency and cost assertions
[v0.19.1] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.19.2] ✅ Completed: Minimal Plan Exception - All plans officially complete
[v0.19.3] ✅ Completed: MetricVersioning - Implemented metric versioning in scorecard normalizer


## GOVERNANCE

**Version**: 1.18.0

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
[v1.9.0] ✅ Completed: ModerationAndGovernancePolicies - Implemented acceptable use, deprecation, and ownership dispute policies and automated moderation scan workflow.
[v1.10.0] ✅ Completed: ArtifactAttestations - Added build provenance attestations to immutable-release.yml.
[v1.11.0] ✅ Completed: SecretScan - Implemented automated secret scanning workflow.
[v1.12.0] ✅ Completed: CommunityReportingWorkflow - Implemented an automated workflow and issue template for handling community moderation reports.
[v1.13.0] ✅ Completed: Consolidated CI - Implemented simplified two-workflow setup.
[v1.14.0] ✅ Completed: Node20DeprecationFix - Injected FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 into GitHub Actions workflows.
[v1.15.0] ✅ Completed: Minimal Plan Exception Final - Acknowledged all GOVERNANCE vision gaps are complete.
[v1.15.0] ✅ Completed: Naming Policy - Implemented naming and rename policy.
[v1.16.0] ✅ Completed: ArtifactAttestations - Minimal Plan Exception. Changes already present.
[v1.17.0] ✅ Completed: TrustedPublisherBadges - Added trusted-publisher.md policy and codeowners.
[v1.18.0] ✅ Completed: ArtifactAttestations - Pinned GitHub Action SHA in immutable-release.yml


## RUNTIME

**Version**: 1.16.0
[v1.16.0] ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.
[v1.15.0] ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.
[v1.14.0] ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.
[v1.13.0] ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.
[v1.12.0] ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.
[v1.11.0] ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.
[v1.10.0] ✅ Completed: QuickEvalLocalOverrideResolution - Implement quick eval format resolution in the LocalResolver.
[v1.9.0] ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.
[v1.7.0] ✅ Completed: SemverTagResolution - Implement semver tag resolution in the GitRefResolver.
[v1.6.0] ✅ Completed: DirectoryResolver - Update WorkspaceResolver and GitRefResolver to support resolving prompts packaged in a <prompt_id> directory.
[v1.5.0] ✅ Completed: ReferenceCLI - Implemented reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.
[v1.4.1] ✅ Completed: LocalOverrideFix - Fix the LocalResolver in the resolver chain to parse prompt packages instead of returning stub strings.
[v1.4.0] ✅ Completed: ReferenceCLI - Spec the reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.
[v1.3.1] ✅ Completed: ResolverTopologyAlignment - Aligned workspace and git ref resolvers with core repo topology model
[v1.3.0] ✅ Completed: PromptTemplateRendering - Implemented variable injection in the resolve() function
[v0.2.0] ✅ Completed: ConsumptionManifestFormat - Defined schema example format
[v0.2.0] ✅ Completed: LocalOverrideResolution - Implemented local override step in python resolver chain
[v0.3.0] ✅ Completed: WorkspacePathResolution - Implemented workspace path lookup in resolver chain
[v0.4.0] ✅ Completed: GitRefResolution - Implemented git ref resolution in python resolver chain
[v0.5.0] ✅ Completed: MinimalResolveInterface - Implemented resolve() function as minimal runtime interface
[v0.6.0] ✅ Completed: PackagedArtifactResolution - Implemented packaged artifact fallback in resolver chain
[v0.7.0] ✅ Completed: RunnerShim - Implemented runner shim script
[v0.8.0] ✅ Completed: DeterministicDigestTooling - Implemented canonicalization and digest computation for prompts and datasets
[v0.9.0] ✅ Completed: ConsumptionManifestValidation - Implemented schema validation for consumption manifests during load_manifest
[v1.0.0] ✅ Completed: ConsumptionManifestFormat - Re-wrote consumption manifest format to be more realistic and validate
[v1.1.0] ✅ Completed: PromptSpecValidation - Implemented schema validation for resolved prompt specifications against prompt-spec.schema.json
[v1.2.0] ✅ Completed: HarnessContractValidation - Implemented runner shim validation against CONTRACTS schemas
[v1.7.1] ✅ Completed: MinimalPlanException - Executed minimal plan exception to unlock completion of current run.
[v1.8.0] ✅ Completed: QuickEvalWorkspaceResolution - Implement quick eval format resolution in the WorkspaceResolver.
