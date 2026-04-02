# IDENTITY: AGENT CONTRACTS (EXECUTOR)
**Domain**: `promptops/prompts/`, `promptops/datasets/`, `promptops/evaluators/`, `promptops/suites/`, `promptops/schemas/`, `promptops/validators/`
**Status File**: `docs/status/CONTRACTS.md`
**Progress File**: `docs/progress/CONTRACTS.md`
**Journal File**: `.jules/CONTRACTS.md`
**Responsibility**: You are the Contracts Builder. You implement the machine-readable source of truth for the apastra PromptOps system — schemas, validators, prompt specs, datasets, evaluators, and suites — according to the approved plan from your Planner counterpart.

## Section A: Schema Inventory

### `prompt-package.schema.json`
- **$id**: `apastra-prompt-package-v1`
- **Version**: 1.17.0
- **Description**: Immutable bundle of prompt specs with a manifest and content digest.
- **Key Fields**:
  - `id`: Stable identifier for the package.
  - `digest`: Content digest of the package.
  - `specs`: Array of included prompt spec IDs/digests.
  - `version`: Optional semantic version.
  - `public_interface`: Required if `version` is present. Defines API (prompt_id, variables_schema, output_schema, tool_contract).

### `promptops/schemas/mcp-server-adapter.schema.json`
- **ID:** `https://apastra.com/schemas/mcp-server-adapter.schema.json`
- **Description:** JSON Schema for MCP Server Adapters.
- **Required Fields:** `id`, `type`, `entrypoint`
- **Optional Fields:** `capabilities`, `digest`

### `flake-quarantine-record.schema.json`
- **$id**: `apastra-flake-quarantine-record-v1`
- **Version**: 1.11.0
- **Description**: A record that tracks and quarantines a flaky evaluation case.

### `release-descriptor.schema.json`
- **$id**: `https://promptops.com/schemas/release-descriptor.schema.json`
- **Version**: 1.9.0
- **Description**: Schema for a release descriptor, posted to an internal API as part of abstract delivery targets.
- **Key Fields**:
  - `descriptor_id`: Unique identifier for this release descriptor
  - `timestamp`: ISO-8601 timestamp of when the descriptor was created
  - `prompt_digest`: The canonical digest of the prompt package being released
  - `environment`: The environment this release is targeting
  - `signatures`: Digital signatures ensuring the authenticity of the release


- **ID:** `apastra-agent-skill-v1`
  - **Version:** 1.9.0
  - **Description:** Schema defining an agent skill role configuration.

- **ID:** `apastra-approval-state-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for an Approval state record indicating human and machine review results.

- **ID:** `https://apastra.com/schemas/promptops/artifact-refs.schema.json`
  - **Version:** 1.9.0
  - **Description:** No description provided.

- **ID:** `https://promptops.apastra.com/schemas/audit-report.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for an audit report detailing untested and unversioned prompts.

- **ID:** `apastra-automated-scan-record-v1`
  - **Version:** 1.9.0
  - **Description:** A record of an automated scan performed on a prompt package.

- **ID:** `apastra-baseline-v1`
  - **Version:** 1.9.0
  - **Description:** Schema definition for baseline references to unblock Evaluation.

- **ID:** `https://apastra.com/schemas/promptops/canary-suite.schema.json`
  - **Version:** 1.9.0
  - **Description:** Canary benchmark suite declaring schedule, alerts, datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.

- **ID:** `https://promptops.apastra.com/schemas/community-report-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a community report record in the governance system.

- **ID:** `apastra-comparison-scorecard-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for multi-model evaluation scorecards with cost/quality/latency tradeoffs.

- **ID:** `https://apastra.com/schemas/promptops/consumption-manifest.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for the apastra PromptOps consumption manifest.

- **ID:** `https://promptops.apastra.com/schemas/dataset-case.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema defining a single line of a JSONL dataset for evaluating prompt tests.

- **ID:** `https://promptops.apastra.com/schemas/dataset-manifest.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance.

- **ID:** `https://promptops.apastra.com/schemas/delivery-target-receipt.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a delivery target receipt.

- **ID:** `apastra-delivery-target-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for delivery target config.

- **ID:** `https://promptops.apastra.com/schemas/deprecation-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for deprecation records.

- **ID:** `https://apastra.com/schemas/promptops/drift-report.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a drift report comparing current results vs a baseline to identify output drift.

- **ID:** `https://promptops.apastra.com/schemas/emergency-takedown-decision.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for an emergency takedown decision.

- **ID:** `https://promptops.apastra.com/schemas/evaluator.schema.json`
  - **Version:** 1.9.0
  - **Description:** Scoring definition (deterministic checks, schema validation, rubric/judge config)

- **ID:** `https://apastra.com/schemas/harness-adapter.schema.json`
  - **Version:** 1.9.0
  - **Description:** No description provided.

- **ID:** `https://promptops.apastra.com/schemas/mcp-tool-definition.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema defining an MCP tool definition object.

- **ID:** `https://promptops.apastra.com/schemas/mirror-sync-receipt.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for mirror sync receipts.

- **ID:** `https://promptops.apastra.com/schemas/moderation-approval-for-public-listing.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for moderation approval for public listing records.

- **ID:** `https://promptops.apastra.com/schemas/moderation-decision-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for moderation decision records.

- **ID:** `https://promptops.apastra.com/schemas/moderation-escalation-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a moderation escalation record.

- **ID:** `https://promptops.apastra.com/schemas/namespace-claim-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a namespace claim record, used to track canonical name registrations, ownership disputes, and deprecations.

- **ID:** `apastra-observability-adapter-config-v1`
  - **Version:** 1.9.0
  - **Description:** Configuration for exporting run artifacts to external observability systems like Langfuse or OpenTelemetry.

- **ID:** `apastra-ownership-dispute-record-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for an ownership dispute record in the governance system.

- **ID:** `https://promptops.apastra.com/schemas/policy-exception-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for policy exception records

- **ID:** `apastra-promotion-record-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for append-only binding records.

- **ID:** `apastra-prompt-package-v1`
  - **Version:** 1.9.0
  - **Description:** Immutable bundle of prompt specs with a manifest and content digest.

- **ID:** `https://promptops.apastra.com/schemas/prompt-spec.schema.json`
  - **Version:** 1.9.0
  - **Description:** Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.

- **ID:** `https://promptops.com/schema/promptops-config.schema.json`
  - **Version:** 1.9.0
  - **Description:** No description provided.

- **ID:** `https://promptops.apastra.com/schemas/provenance-attestation.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for supply-chain provenance attestations (SLSA-style).

- **ID:** `apastra-provider-artifact-v1`
  - **Version:** 1.9.0
  - **Description:** A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper).

- **ID:** `https://promptops.apastra.com/schemas/quick-eval.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema defining a combined quick evaluation file containing prompt, cases, and assertions.

- **ID:** `apastra-regression-policy-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for regression policy definition.

- **ID:** `apastra-regression-report-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for a regression report output.

- **ID:** `https://promptops.com/schemas/release-descriptor.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a release descriptor, posted to an internal API as part of abstract delivery targets.

- **ID:** `apastra-run-artifact-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for a minimal BYO harness run artifact output.

- **ID:** `apastra-run-case-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for a single case in cases.jsonl.

- **ID:** `apastra-run-failures-v1`
  - **Version:** 1.9.0
  - **Description:** Schema defining an array of failure objects.

- **ID:** `apastra-run-manifest-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for a run manifest.

- **ID:** `apastra-run-request-v2`
  - **Version:** 1.9.0
  - **Description:** Schema for a minimal BYO harness run request. Captures all metadata required for reproducible replay of an evaluation run.

- **ID:** `apastra-scorecard-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for the run artifact scorecard.

- **ID:** `apastra-submission-record-v1`
  - **Version:** 1.9.0
  - **Description:** Schema for an append-only artifact structure for package submissions to a public registry.

- **ID:** `https://apastra.com/schemas/promptops/suite.schema.json`
  - **Version:** 1.9.0
  - **Description:** Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.

- **ID:** `apastra-takedown-appeal-record-v1`
  - **Version:** 1.9.0
  - **Description:** A record used to formally process and track appeals to moderation takedowns.

- **ID:** `https://promptops.apastra.com/schemas/takedown-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for takedown records.

- **ID:** `apastra-trusted-publisher-provenance-v1`
  - **Version:** 1.9.0
  - **Description:** Provenance record to verify and grant trusted publisher badges for packages and providers.

- **ID:** `https://promptops.apastra.com/schemas/vulnerability-flag-record.schema.json`
  - **Version:** 1.9.0
  - **Description:** Schema for a vulnerability flag record appended to prompt packages.

### `release-descriptor.schema.json`
- **$id**: `https://promptops.com/schemas/release-descriptor.schema.json`
- **Version**: 1.12.0
- **Description**: Schema for a release descriptor, posted to an internal API as part of abstract delivery targets.
- **Key Fields**:
  - `descriptor_id`: Unique identifier for this release descriptor
  - `timestamp`: ISO-8601 timestamp of when the descriptor was created
  - `prompt_digest`: The canonical digest of the prompt package being released
  - `environment`: The environment this release is targeting
  - `signatures`: Digital signatures ensuring the authenticity of the release


## Section B: Validator Inventory

### `validate-mcp-server-adapter.sh`
- **Validator:** `validate-mcp-server-adapter.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-mcp-server-adapter.sh <target.json>`
  - **What it Validates:** Validates `mcp-server-adapter.schema.json`.

### `validate-flake-quarantine-record.sh`
- **Validates**: `flake-quarantine-record.schema.json`
- **Syntax**: `./promptops/validators/validate-flake-quarantine-record.sh <path/to/record.json>`

### `validate-release-descriptor.sh`
- **Validates**: `release-descriptor.schema.json`
- **Syntax**: `./promptops/validators/validate-release-descriptor.sh <path/to/descriptor.json>`


- **Validator:** `validate-agent-skill.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-agent-skill.sh <target.json>`
  - **What it Validates:** Validates `agent-skill.schema.json`.

- **Validator:** `validate-approval-state.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-approval-state.sh <target.json>`
  - **What it Validates:** Validates `approval-state.schema.json`.

- **Validator:** `validate-artifact-refs.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-artifact-refs.sh <target.json>`
  - **What it Validates:** Validates `artifact-refs.schema.json`.

- **Validator:** `validate-audit-report.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-audit-report.sh <target.json>`
  - **What it Validates:** Validates `audit-report.schema.json`.

- **Validator:** `validate-automated-scan-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-automated-scan-record.sh <target.json>`
  - **What it Validates:** Validates `automated-scan-record.schema.json`.

- **Validator:** `validate-baseline.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-baseline.sh <target.json>`
  - **What it Validates:** Validates `baseline.schema.json`.

- **Validator:** `validate-canary-suite.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-canary-suite.sh <target.json>`
  - **What it Validates:** Validates `canary-suite.schema.json`.

- **Validator:** `validate-community-report-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-community-report-record.sh <target.json>`
  - **What it Validates:** Validates `community-report-record.schema.json`.

- **Validator:** `validate-comparison-scorecard.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-comparison-scorecard.sh <target.json>`
  - **What it Validates:** Validates `comparison-scorecard.schema.json`.

- **Validator:** `validate-consumption-manifest.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-consumption-manifest.sh <target.json>`
  - **What it Validates:** Validates `consumption-manifest.schema.json`.

- **Validator:** `validate-dataset.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-dataset.sh <target.json>`
  - **What it Validates:** Validates `dataset.schema.json`.

- **Validator:** `validate-delivery-target-receipt.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-delivery-target-receipt.sh <target.json>`
  - **What it Validates:** Validates `delivery-target-receipt.schema.json`.

- **Validator:** `validate-delivery-target.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-delivery-target.sh <target.json>`
  - **What it Validates:** Validates `delivery-target.schema.json`.

- **Validator:** `validate-deprecation-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-deprecation-record.sh <target.json>`
  - **What it Validates:** Validates `deprecation-record.schema.json`.

- **Validator:** `validate-drift-report.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-drift-report.sh <target.json>`
  - **What it Validates:** Validates `drift-report.schema.json`.

- **Validator:** `validate-emergency-takedown-decision.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-emergency-takedown-decision.sh <target.json>`
  - **What it Validates:** Validates `emergency-takedown-decision.schema.json`.

- **Validator:** `validate-evaluator.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-evaluator.sh <target.json>`
  - **What it Validates:** Validates `evaluator.schema.json`.

- **Validator:** `validate-harness-adapter.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-harness-adapter.sh <target.json>`
  - **What it Validates:** Validates `harness-adapter.schema.json`.

- **Validator:** `validate-mcp-tool-definition.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-mcp-tool-definition.sh <target.json>`
  - **What it Validates:** Validates `mcp-tool-definition.schema.json`.

- **Validator:** `validate-mirror-sync-receipt.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-mirror-sync-receipt.sh <target.json>`
  - **What it Validates:** Validates `mirror-sync-receipt.schema.json`.

- **Validator:** `validate-moderation-approval-for-public-listing.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-moderation-approval-for-public-listing.sh <target.json>`
  - **What it Validates:** Validates `moderation-approval-for-public-listing.schema.json`.

- **Validator:** `validate-moderation-decision-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-moderation-decision-record.sh <target.json>`
  - **What it Validates:** Validates `moderation-decision-record.schema.json`.

- **Validator:** `validate-moderation-escalation-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-moderation-escalation-record.sh <target.json>`
  - **What it Validates:** Validates `moderation-escalation-record.schema.json`.

- **Validator:** `validate-namespace-claim-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-namespace-claim-record.sh <target.json>`
  - **What it Validates:** Validates `namespace-claim-record.schema.json`.

- **Validator:** `validate-observability-adapter-config.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-observability-adapter-config.sh <target.json>`
  - **What it Validates:** Validates `observability-adapter-config.schema.json`.

- **Validator:** `validate-ownership-dispute-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-ownership-dispute-record.sh <target.json>`
  - **What it Validates:** Validates `ownership-dispute-record.schema.json`.

- **Validator:** `validate-policy-exception-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-policy-exception-record.sh <target.json>`
  - **What it Validates:** Validates `policy-exception-record.schema.json`.

- **Validator:** `validate-promotion-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-promotion-record.sh <target.json>`
  - **What it Validates:** Validates `promotion-record.schema.json`.

- **Validator:** `validate-prompt-package.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-prompt-package.sh <target.json>`
  - **What it Validates:** Validates `prompt-package.schema.json`.

- **Validator:** `validate-prompt-spec.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-prompt-spec.sh <target.json>`
  - **What it Validates:** Validates `prompt-spec.schema.json`.

- **Validator:** `validate-promptops-config.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-promptops-config.sh <target.json>`
  - **What it Validates:** Validates `promptops-config.schema.json`.

- **Validator:** `validate-provenance-attestation.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-provenance-attestation.sh <target.json>`
  - **What it Validates:** Validates `provenance-attestation.schema.json`.

- **Validator:** `validate-provider-artifact.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-provider-artifact.sh <target.json>`
  - **What it Validates:** Validates `provider-artifact.schema.json`.

- **Validator:** `validate-quick-eval.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-quick-eval.sh <target.json>`
  - **What it Validates:** Validates `quick-eval.schema.json`.

- **Validator:** `validate-regression-policy.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-regression-policy.sh <target.json>`
  - **What it Validates:** Validates `regression-policy.schema.json`.

- **Validator:** `validate-regression-report.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-regression-report.sh <target.json>`
  - **What it Validates:** Validates `regression-report.schema.json`.

- **Validator:** `validate-release-descriptor.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-release-descriptor.sh <target.json>`
  - **What it Validates:** Validates `release-descriptor.schema.json`.

- **Validator:** `validate-run-artifact.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-artifact.sh <target.json>`
  - **What it Validates:** Validates `run-artifact.schema.json`.

- **Validator:** `validate-run-case.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-case.sh <target.json>`
  - **What it Validates:** Validates `run-case.schema.json`.

- **Validator:** `validate-run-failures.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-failures.sh <target.json>`
  - **What it Validates:** Validates `run-failures.schema.json`.

- **Validator:** `validate-run-manifest.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-manifest.sh <target.json>`
  - **What it Validates:** Validates `run-manifest.schema.json`.

- **Validator:** `validate-run-request.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-request.sh <target.json>`
  - **What it Validates:** Validates `run-request.schema.json`.

- **Validator:** `validate-scorecard.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-scorecard.sh <target.json>`
  - **What it Validates:** Validates `scorecard.schema.json`.

- **Validator:** `validate-submission-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-submission-record.sh <target.json>`
  - **What it Validates:** Validates `submission-record.schema.json`.

- **Validator:** `validate-suite.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-suite.sh <target.json>`
  - **What it Validates:** Validates `suite.schema.json`.

- **Validator:** `validate-takedown-appeal-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-takedown-appeal-record.sh <target.json>`
  - **What it Validates:** Validates `takedown-appeal-record.schema.json`.

- **Validator:** `validate-takedown-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-takedown-record.sh <target.json>`
  - **What it Validates:** Validates `takedown-record.schema.json`.

- **Validator:** `validate-trusted-publisher-provenance.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-trusted-publisher-provenance.sh <target.json>`
  - **What it Validates:** Validates `trusted-publisher-provenance.schema.json`.

- **Validator:** `validate-vulnerability-flag-record.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-vulnerability-flag-record.sh <target.json>`
  - **What it Validates:** Validates `vulnerability-flag-record.schema.json`.

- **Validator:** `validate-release-descriptor.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-release-descriptor.sh <target.json>`
  - **What it Validates:** Validates `release-descriptor.schema.json`.


## Section C: Source File Conventions
- **Quick Evals:**
  - Naming: `*.yaml`
  - Structure: Lives in `promptops/evals/` (e.g., `my-eval.yaml`)
  - Required fields: `id` (string), `prompt` (string), `cases` (array).
- **Prompts:**
  - Naming: `prompt.yaml` or `prompt.json`
  - Structure: Lives in `promptops/prompts/<id>/`
  - Required fields: `id` (string), `variables` (object), `template` (string, object, array).
  - Optional fields: `tool_contract` (object).
- **Prompt Packages:**
  - Naming: `package.yaml` or `package.json`
  - Structure: Lives in `promptops/prompts/<package-id>/`
  - Required fields: `id` (string), `digest` (string), `specs` (array).
- **Suites:**
  - Naming: `suite.yaml` or `suite.json`
  - Structure: Lives in `promptops/suites/<suite-id>/`
  - Required fields: `id` (string), `name` (string), `datasets` (array), `evaluators` (array), `model_matrix` (array).
  - Optional fields: `description`, `trials`, `budgets`, `thresholds`, `tier` (string), `tags` (array).

  - Naming: `manifest.json` or `manifest.yaml` and `cases.jsonl`
  - Structure: Lives in `promptops/datasets/<dataset-id>/`
  - Required fields in manifest: `id`, `version`, `schema_version`, `digest`
  - Optional fields in manifest: `provenance` (object)
  - Required fields in case: `case_id`, `inputs`
  - Optional fields in case: `assert` (array of assertions with restricted built-in `type` strings and `value`)

- **Evaluators:**
  - Naming:  `evaluator.yaml` or `evaluator.json`
  - Structure: Lives in `promptops/evaluators/<evaluator-id>/`
  - Required fields: `id` (string), `type` (string: "deterministic", "schema", "judge", "human"), `metrics` (array of strings).
- **Suites:**
  - Naming: `suite.yaml` or `suite.json`
  - Structure: Lives in `promptops/suites/<suite-id>/`
  - Required fields: `id` (string), `name` (string), `datasets` (array), `evaluators` (array), `model_matrix` (array).

## Section D: Digest Convention
- Computed across the canonical representation of the file.
- YAML files are converted to JSON and canonicalized.
- JSON files are canonicalized with sorted keys and insignificant whitespace removed (e.g. `jq -cSM .`).
- JSONL files are canonicalized line by line and joined with newlines.
- The output format is `sha256:<hex>`.
- For dataset cases, the digest is held in the `digest` field of the dataset manifest, which is computed across the `cases.jsonl` file.

## Section E: Integration Points
- **RUNTIME:** Reads manifests schema, dataset manifest schema.
- **EVALUATION:** Reads run request schema, dataset schema.
- **GOVERNANCE:** Reads policy schema.
