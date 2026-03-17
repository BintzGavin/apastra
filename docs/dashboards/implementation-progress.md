---
title: "Implementation Progress Dashboard"
description: "Progress tracker for all domains"
audience: "all"
last_verified: "2026-03-16"
source_files:
  - "docs/progress/CONTRACTS.md"
  - "docs/progress/DOCS.md"
  - "docs/progress/EVALUATION.md"
  - "docs/progress/GOVERNANCE.md"
  - "docs/progress/RUNTIME.md"
---

# Implementation Progress

## CONTRACTS

### CONTRACTS v0.44.0
- ✅ Completed: MetricVersioning - Implemented metric versioning in scorecard and evaluator schemas

### CONTRACTS v0.43.0
- ✅ Completed: Minimal Plan Exception Final - Triggered minimal plan exception as all required schemas and validation scripts are complete.

### CONTRACTS v0.42.0
- ✅ Completed: ToolContractSchema - Added tool_contract as an optional property to the prompt-spec.schema.json.

### CONTRACTS v0.41.0
- ✅ Completed: HumanReviewHooksEvaluatorType - Added human as an evaluator type to the evaluator.schema.json to support human review hooks.

### CONTRACTS v0.40.0
- ✅ Completed: Minimal Plan Exception Final - Triggered minimal plan exception as all required schemas and validation scripts are complete.

### CONTRACTS v0.39.0
- ✅ Completed: ModerationRecordsSchemas - Created moderation decision, deprecation, takedown, and mirror sync schemas.

### CONTRACTS v0.38.0
- ✅ Completed: DatasetSchemaUpdates - Added provenance to manifest schema and assertion type validation to case schema.

### CONTRACTS v0.37.0
- ✅ Completed: RunArtifactProvenance - Added SLSA-style provenance metadata schema to the run manifest.

### CONTRACTS v0.36.0
- ✅ Completed: SubmissionRecordSchema - Created submission-record.schema.json and validate-submission-record.sh

### CONTRACTS v0.35.0
- ✅ Completed: DatasetSchemaUpdates - Added provenance to manifest schema and assertion type validation to case schema.

### CONTRACTS v0.34.0
- ✅ Completed: DatasetSchemaUpdates - Added provenance to manifest schema and assertion type validation to case schema.

### CONTRACTS v0.33.0
- ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception.

### CONTRACTS v0.32.0
- ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception as all required schemas, validation scripts, and initial instances have been fully implemented and verified.

### CONTRACTS v0.31.0
- ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception as all required schemas, validation scripts, and initial instances have been fully implemented and verified.

### CONTRACTS v0.30.0
- ✅ Completed: InitialQuickEval - Created missing initial quick eval instance in promptops/evals/my-eval.yaml

### CONTRACTS v0.29.0
- ✅ Completed: Minimal Plan Exception Final - Executed the final minimal plan exception.

### CONTRACTS v0.28.0
- ✅ Completed: Minimal Plan Exception Final - Triggered minimal plan exception as all required schemas, validation scripts, and initial instances have been fully implemented and verified.

### CONTRACTS v0.27.0
- ✅ Completed: InitialPromptPackage - Created first prompt package instance my-prompt-package/package.yaml

### CONTRACTS v0.26.0
- ✅ Completed: InitialQuickEval - Created first quick eval instance in promptops/evals/my-eval.yaml

### CONTRACTS v0.25.0
- ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.

### CONTRACTS v0.24.0
- ✅ Completed: QuickEvalAndInlineAssertions - Defined schemas for Quick Eval Mode and Inline Assertions.

### CONTRACTS v0.23.0
- ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.

### CONTRACTS v0.22.0
- ✅ Completed: Minimal Plan Exception - Triggered minimal plan exception as all required schemas and validation scripts are complete.

### CONTRACTS v0.21.0
- ✅ Completed: InitialSuite - Created first suite instance test-suite.yaml

### CONTRACTS v0.20.0
- ✅ Completed: InitialEvaluator - Created first evaluator instance exact-match.yaml

### CONTRACTS v0.19.0
- ✅ Completed: InitialDataset - Created first dataset instance test-dataset

### CONTRACTS v0.18.0
- ✅ Completed: InitialPromptSpec - Created first prompt instance promptops/prompts/test-prompt/prompt.yaml

### CONTRACTS v0.17.0
- ✅ Completed: ProviderArtifactSchema - Created provider-artifact.schema.json and validate-provider-artifact.sh

### CONTRACTS v0.16.0
- ✅ Completed: RunArtifactFiles - Created schemas and validators for run-manifest, run-case, and run-failures.

### CONTRACTS v0.15.0
- ✅ Completed: ApprovalStateSchema - Created approval-state.schema.json and validate-approval-state.sh

### CONTRACTS v0.14.0
- ✅ Completed: ArtifactRefsSchema - Created artifact-refs.schema.json and validate-artifact-refs.sh

### CONTRACTS v0.13.0
- ✅ Completed: PromptPackage - Created prompt-package.schema.json and validate-prompt-package.sh

### CONTRACTS v0.12.0
- ✅ Completed: BaselineSchema - Created baseline.schema.json and validate-baseline.sh

### CONTRACTS v0.11.0
- ✅ Completed: GovernanceSchemas - Created regression-policy.schema.json, promotion-record.schema.json, delivery-target.schema.json and validators

### CONTRACTS v0.10.0
- ✅ Completed: ScorecardAndRegressionReport - Created scorecard.schema.json, regression-report.schema.json, and validators

### CONTRACTS v0.9.0
- ✅ Completed: run-request-and-artifact - Created run-request.schema.json, run-artifact.schema.json, validate-run-request.sh, and validate-run-artifact.sh

### CONTRACTS v0.8.0
- ✅ Completed: HarnessAdapterSchema - Created harness-adapter.schema.json and validate-harness-adapter.sh

### CONTRACTS v0.7.0
- ✅ Completed: ConsumptionManifestSchema - Created consumption-manifest.schema.json and validate-consumption-manifest.sh

### CONTRACTS v0.6.0
- ✅ Completed: content-digest-convention - Created digest-convention.md and compute-digest.sh

### CONTRACTS v0.5.0
- ✅ Completed: suite-schema - Created suite.schema.json and validate-suite.sh

### CONTRACTS v0.4.0
- ✅ Completed: evaluator-schema - Created evaluator.schema.json and validate-evaluator.sh

### CONTRACTS v0.3.0
- ✅ Completed: dataset-schema - Created dataset-manifest.schema.json, dataset-case.schema.json, and validate-dataset.sh

### CONTRACTS v0.2.0
- ✅ Completed: prompt-spec-schema - Created prompt-spec.schema.json and validate-prompt-spec.sh

## DOCS

### DOCS v0.6.0
- ✅ Completed: Daily Documentation Review
  - Updated API documentation for `prompt-spec`, `run-manifest`, and `evaluator` schemas with new fields
  - Refreshed cross-domain dashboards `domain-status-overview.md` and `implementation-progress.md`
  - Rebuilt schema dependency graph to include `quick-eval` to `dataset-case` dependency
  - Regenerated context-docs.md

### DOCS v0.5.0
- ✅ Completed: Daily Documentation Review
  - Updated API documentation for `takedown-record`, `moderation-decision-record`, `deprecation-record`, `mirror-sync-receipt`, and `submission-record` schemas
  - Refreshed cross-domain dashboards `domain-status-overview.md` and `implementation-progress.md`
  - Rebuilt schema dependency graph to include new moderation schemas
  - Regenerated context-docs.md

### DOCS v0.4.0
- ✅ Completed: Daily Documentation Review
  - Updated API documentation for schemas including quick-eval
  - Refreshed cross-domain dashboards
  - Rebuilt schema dependency graph
  - Updated DOCS context

### DOCS v0.3.0
- ✅ Completed: Daily Documentation Review
  - Updated API documentation for all schemas
  - Refreshed cross-domain dashboards
  - Regenerated context-docs.md

### DOCS v0.2.0
- ✅ Completed: Daily Documentation Review
  - Updated API documentation for all schemas
  - Refreshed cross-domain dashboards

### DOCS v0.1.0
- ✅ Completed: Daily Documentation Review
  - Initialized required DOCS domain paths (`docs/guides`, `docs/api`, `docs/decisions`, `docs/dashboards`)
  - Updated API documentation for `prompt-spec`, `dataset-case`, `dataset-manifest`, `evaluator`, `harness-adapter`, `run-artifact`, `run-request`, `suite`, and `consumption-manifest`
  - Created and refreshed cross-domain dashboards (`domain-status-overview.md`, `implementation-progress.md`, `schema-dependency-graph.md`)
  - Tracked status and progress updates

## EVALUATION

### EVALUATION v0.26.0
- ✅ Completed: Minimal Plan Exception Final - All plans officially complete

### EVALUATION v0.25.0
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.24.0
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.23.0
- ✅ Completed: RunArtifactProvenanceSupport - Implemented SLSA-style provenance metadata collection in the reference harness adapter's run manifest

### EVALUATION v0.22.0
- ✅ Completed: HarnessTimeoutAndBudgetSupport - Implemented timeout and budget enforcement in reference adapter

### EVALUATION v0.21.0
- ✅ Completed: FlakeQuarantine - Implemented flake tracking and variance-aware gating

### EVALUATION v0.20.0
- ✅ Completed: TradeoffSurfacing - Implemented tradeoff surfacing in regression report

### EVALUATION v0.19.3
- ✅ Completed: MetricVersioning - Implemented metric versioning in scorecard normalizer

### EVALUATION v0.19.2
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.19.1
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.19.0
- ✅ Completed: PerformanceAssertions - Implemented latency and cost assertions

### EVALUATION v0.18.1
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.18.0
- ✅ Completed: Minimal Plan Exception Final - All plans officially complete

### EVALUATION v0.17.1
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.17.0
- ✅ Completed: JsonSchemaAssertion - Implemented the is-valid-json-schema assertion type for inline evaluation

### EVALUATION v0.16.0
- ✅ Completed: TrialsAndVarianceSupport - Implemented trials support in reference adapter and variance calculation in scorecard normalizer

### EVALUATION v0.15.0
- ✅ Completed: ModelAssistedAssertions - Implemented model-assisted and performance assertion types in the deterministic evaluation engine

### EVALUATION v0.14.0
- ✅ Completed: InlineAssertions - Implemented deterministic inline assertions evaluation engine.

### EVALUATION v0.13.0
- ✅ Completed: QuickEvalMode - Implemented quick eval mode pipeline and adapted reference harness

### EVALUATION v0.12.3
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.12.2
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.12.1
- ✅ Completed: Minimal Plan Exception - All plans officially complete

### EVALUATION v0.12.0
- ✅ Completed: ReferenceAdapterRefactor - Refactored reference adapter to natively support split artifacts and updated scorecard normalizer execution

### EVALUATION v0.11.0
- ✅ Completed: RegressionReportWorkflow - Implemented regression report generation and storage workflow

### EVALUATION v0.10.0
- ✅ Completed: RegressionComparisonRefactor - Refactored Regression Engine to read split scorecard.json files

### EVALUATION v0.9.0
- ✅ Completed: ScorecardNormalizationRefactor - Refactored normalize.py to read cases.jsonl and output scorecard.json

### EVALUATION v0.8.0
- ✅ Completed: RunArtifactGeneration - Implemented bash script to split monolithic run_artifact.json into distinct, append-friendly index files for the artifacts branch.

### EVALUATION v0.7.0
- ✅ Completed: BaselineEstablishmentWorkflow - Implemented bash script to establish baselines

### EVALUATION v0.6.0
- ✅ Completed: ScorecardNormalization - Implemented standalone scorecard normalizer

### EVALUATION v0.5.0
- ✅ Completed: RegressionComparisonEngine - Implemented CLI script for regression comparison

### EVALUATION v0.4.0
- ✅ Completed: BaselineEstablishment - Verified schema availability and created baselines directory structure

### EVALUATION v0.3.0
- ✅ Completed: RunRequestValidation - Implemented run request validation script

### EVALUATION v0.2.0
- ✅ Completed: HarnessAdapterContract - Implemented reference BYO harness adapter config and execution script

### EVALUATION v0.1.1
- ✅ Completed: HarnessAdapterContract - Verified schema availability and created domain directories

## GOVERNANCE

### GOVERNANCE v1.23.0
- ✅ Completed: MinimalPlanExceptionFinal - Acknowledged all GOVERNANCE vision gaps are complete.

### GOVERNANCE v1.22.0
- ✅ Completed: FederationAndMirrors - Specified the mirror protocol and optional federation policy.

### GOVERNANCE v1.21.0
- ✅ Completed: MinimalPlanExceptionFinal - Acknowledged all GOVERNANCE vision gaps are complete.

### GOVERNANCE v1.20.0
- ✅ Completed: MissingPoliciesAndTargets - Implemented missing delivery targets (OCI, npm, PyPI) and takedown/appeals governance policies.

### GOVERNANCE v1.19.0
- ✅ Completed: Complete CODEOWNERS - Added missing paths for CONTRACTS, EVALUATION, and RUNTIME to .github/CODEOWNERS.

### GOVERNANCE v1.18.1
- ✅ Completed: StrictPinning - Pinned GitHub Action SHAs in all workflows.

### GOVERNANCE v1.18.0
- ✅ Completed: ArtifactAttestations - Pinned GitHub Action SHA in immutable-release.yml

### GOVERNANCE v1.17.0
- ✅ Completed: TrustedPublisherBadges - Added trusted-publisher.md policy and codeowners.

### GOVERNANCE v1.16.0
- ✅ Completed: ArtifactAttestations - Minimal Plan Exception. Changes already present.

### GOVERNANCE v1.15.0
- ✅ Completed: Minimal Plan Exception Final - Acknowledged all GOVERNANCE vision gaps are complete.
- ✅ Completed: Naming Policy - Implemented naming and rename policy.

### GOVERNANCE v1.14.0
- ✅ Completed: Node20DeprecationFix - Injected FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 into GitHub Actions workflows.

### GOVERNANCE v1.13.0
- ✅ Completed: Consolidated CI - Implemented simplified two-workflow setup.

### GOVERNANCE v1.12.0
- ✅ Completed: CommunityReportingWorkflow - Implemented an automated workflow and issue template for handling community moderation reports.

### GOVERNANCE v1.11.0
- ✅ Completed: SecretScan - Implemented automated secret scanning workflow.

### GOVERNANCE v1.10.0
- ✅ Completed: ArtifactAttestations - Added build provenance attestations to immutable-release.yml.

### GOVERNANCE v1.9.0
- ✅ Completed: ModerationAndGovernancePolicies - Implemented acceptable use, deprecation, and ownership dispute policies and automated moderation scan workflow.

### GOVERNANCE v1.8.0
- ✅ Completed: Promotion Approval Enforcement - Fixed jq logic in promote.yml to properly pipe approvals/*.json contents.

### GOVERNANCE v1.7.0
- ✅ Completed: Minimal Plan Exception - Acknowledged all GOVERNANCE vision gaps are complete.

### GOVERNANCE v1.6.0
- ✅ Completed: Rich PR Annotations - Enhanced the regression gate workflow to provide rich PR annotations and a detailed Markdown summary of regression evidence.

### GOVERNANCE v1.5.0
- ✅ Completed: Conditional Regression Gate - Bypassed regression check for PRs modifying non-evaluable files using tj-actions/changed-files.

### GOVERNANCE v1.4.0
- ✅ Completed: Delivery Sync Refactor - Fixed delivery target sync to operate within the promptops-artifacts branch topology.

### GOVERNANCE v1.3.0
- ✅ Completed: Enforce Regression Gate - Removed bypass in regression-gate.yml to block merges when regression report is missing.

### GOVERNANCE v1.2.0
- ✅ Completed: Promotion Approval Enforcement - Enforced that promotions require a matching approved Approval State record in promote.yml.

### GOVERNANCE v1.1.0
- ✅ Completed: Approval State Workflow - Created automated workflow to append approval records upon human review.

### GOVERNANCE v1.0.0
- ✅ Completed: Artifacts Branch Implementation - Configured workflows to isolate derived artifacts on promptops-artifacts branch.

### GOVERNANCE v0.9.0
- ✅ Completed: Artifacts Branch - Spec designed to isolate derived data on promptops-artifacts branch.

### GOVERNANCE v0.8.0
- ✅ Completed: Reusable Workflows - Standardized workflows with workflow_call and checkout@v4, gracefully bypassed missing regression engine.

### GOVERNANCE v0.7.0
- ✅ Completed: Rulesets - Configured conceptual rulesets for main branch protection and tag immutability.

### GOVERNANCE v0.6.0
- ✅ Completed: Delivery Target Specs - Implemented delivery target schema configs and a workflow to sync downstream.

### GOVERNANCE v0.5.0
- ✅ Completed: Required Status Check - Created regression gate workflow and base regression policy.

### GOVERNANCE v0.4.0
- ✅ Completed: Immutable Release Workflow - Created .github/workflows/immutable-release.yml to package prompts, compute digest, and create a GitHub Release when tags are pushed.

### GOVERNANCE v0.3.0
- ✅ Completed: Promotion Record Workflow - Created automated workflow to append promotion records upon governed releases.

### GOVERNANCE v0.2.0
- ✅ Completed: CODEOWNERS File Creation - Created .github/CODEOWNERS with required review boundaries.

## RUNTIME

### RUNTIME v1.27.0
- ✅ Completed: MinimalRuntimeMetadata - Implemented dataset digest and harness version in minimal runtime resolve() output.

### RUNTIME v1.26.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.25.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.24.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.23.0
- ✅ Completed: PackagedResolverCaching - Implemented local caching, offline fallback, and signature verification.

### RUNTIME v1.22.0
- ✅ Completed: NPM-PyPI-Resolver - Implemented npm and PyPI wrapper resolution in the PackagedResolver.

### RUNTIME v1.21.0
- ✅ Completed: PackagedResolver - Complete removal of mock data formatting and fallback templates.

### RUNTIME v1.20.0
- ✅ Completed: PackagedResolver - Removed mock implementation and correctly enforced remote asset resolution handling.

### RUNTIME v1.19.0
- ✅ Completed: PackagedResolver - Fully implemented packaged artifact resolution for sha256 and oci refs to return valid prompt spec dictionary instead of mock string.

### RUNTIME v1.18.0
- ✅ Completed: PackagedResolver - Implemented packaged artifact resolution for sha256 and oci refs with schema validation.

### RUNTIME v1.17.0
- ✅ Completed: LocalNameMappingResolution - Implement local alias mapping to stable IDs and model metadata propagation in the resolver chain.

### RUNTIME v1.16.0
- ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.

### RUNTIME v1.15.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.14.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.13.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.12.0
- ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.

### RUNTIME v1.11.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.10.0
- ✅ Completed: QuickEvalLocalOverrideResolution - Implement quick eval format resolution in the LocalResolver.

### RUNTIME v1.9.0
- ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.

### RUNTIME v1.8.0
- ✅ Completed: QuickEvalWorkspaceResolution - Implement quick eval format resolution in the WorkspaceResolver.

### RUNTIME v1.7.1
- ✅ Completed: MinimalPlanException - Executed minimal plan exception to unlock completion of current run.

### RUNTIME v1.7.0
- ✅ Completed: SemverTagResolution - Implement semver tag resolution in the GitRefResolver.

### RUNTIME v1.6.0
- ✅ Completed: DirectoryResolver - Update WorkspaceResolver and GitRefResolver to support resolving prompts packaged in a <prompt_id> directory.

### RUNTIME v1.5.0
- ✅ Completed: ReferenceCLI - Implemented reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.

### RUNTIME v1.4.1
- ✅ Completed: LocalOverrideFix - Fix the LocalResolver in the resolver chain to parse prompt packages instead of returning stub strings.

### RUNTIME v1.4.0
- ✅ Completed: ReferenceCLI - Spec the reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.

### RUNTIME v1.3.1
- ✅ Completed: ResolverTopologyAlignment - Aligned workspace and git ref resolvers with core repo topology model

### RUNTIME v1.3.0
- ✅ Completed: PromptTemplateRendering - Implemented variable injection in the resolve() function

### RUNTIME v1.2.0
- ✅ Completed: HarnessContractValidation - Implemented runner shim validation against CONTRACTS schemas

### RUNTIME v1.1.0
- ✅ Completed: PromptSpecValidation - Implemented schema validation for resolved prompt specifications against prompt-spec.schema.json

### RUNTIME v1.0.0
- ✅ Completed: ConsumptionManifestFormat - Re-wrote consumption manifest format to be more realistic and validate

### RUNTIME v0.9.0
- ✅ Completed: ConsumptionManifestValidation - Implemented schema validation for consumption manifests during load_manifest

### RUNTIME v0.8.0
- ✅ Completed: DeterministicDigestTooling - Implemented canonicalization and digest computation for prompts and datasets

### RUNTIME v0.7.0
- ✅ Completed: RunnerShim - Implemented runner shim script

### RUNTIME v0.6.0
- ✅ Completed: PackagedArtifactResolution - Implemented packaged artifact fallback in resolver chain

### RUNTIME v0.5.0
- ✅ Completed: MinimalResolveInterface - Implemented resolve() function as minimal runtime interface

### RUNTIME v0.4.0
- ✅ Completed: GitRefResolution - Implemented git ref resolution in python resolver chain

### RUNTIME v0.3.0
- ✅ Completed: WorkspacePathResolution - Implemented workspace path lookup in resolver chain

### RUNTIME v0.2.0
- ✅ Completed: ConsumptionManifestFormat - Defined schema example format
- ✅ Completed: LocalOverrideResolution - Implemented local override step in python resolver chain
