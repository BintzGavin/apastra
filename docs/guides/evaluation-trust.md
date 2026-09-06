# Measured evaluation and trusted evidence

Apastra is a Git-native EvalOps protocol and skill pack. It resolves evaluation
inputs, invokes an adapter selected by the operator, and checks the resulting
evidence before applying a policy. Execution belongs to the adapter. A provider
SDK, another evaluation framework, or an agent can supply that adapter.

The current acceptance target runs deterministic uppercase/lowercase functions.
Those tests prove the protocol. Live-provider integrations have not been tested
for this candidate, and Apastra ships no production provider adapter.

## Commands

After an opt-in project installation, use `.agent/bin/apastra`. A plain npm
installation exposes `node_modules/.bin/apastra`. Python needs `pyyaml` and
`jsonschema`; the optional MCP server also needs `mcp`.

```bash
.agent/bin/apastra eval smoke --adapter promptops/harnesses/local.yaml --output-dir promptops/runs/candidate
.agent/bin/apastra compare smoke --adapter promptops/harnesses/local.yaml --models model-a model-b --output-dir promptops/runs/comparison
.agent/bin/apastra quick-eval promptops/evals/smoke.yaml --adapter promptops/harnesses/local.yaml --models model-a --output-dir promptops/runs/quick
.agent/bin/apastra gate promptops/runs/candidate --adapter promptops/harnesses/local.yaml
.agent/bin/apastra baseline smoke accepted-001 promptops/runs/candidate --adapter promptops/harnesses/local.yaml
.agent/bin/apastra gate promptops/runs/candidate --baseline promptops/runs/accepted --policy promptops/policies/regression.yaml --adapter promptops/harnesses/local.yaml
.agent/bin/apastra validate suite promptops/suites/smoke.yaml
.agent/bin/apastra digest promptops/suites/smoke.yaml
```

Each output directory must be empty. Baseline names are immutable, so create a
new name when accepting a later run. Baseline records retain the run path and its
digest; moving evidence requires an explicit migration.

Evaluation commands exit zero only for `pass`. A failed criterion exits nonzero
even when the target executed successfully. `error` indicates invalid inputs,
incomplete evidence, or an execution failure. Unsupported capabilities return
`unsupported`. Measurements without thresholds return `not_evaluated` and cannot
establish a baseline.

## Adapter contract

Configure a reviewed executable as an argument string. Apastra splits the string
without invoking a shell, then appends the persisted request path and output
directory. Quote paths that contain spaces. The executable runs in the caller's
working directory and has the caller's privileges. Only invoke trusted code.

```yaml
id: team-harness
type: harness_adapter
version: "2.0.0"
execution_mode: measured
capabilities: [run_suite]
entrypoint: 'python tools/team_harness.py'
```

The request contains the resolved prompt and all dataset cases. Evaluator
definitions and the suite policy are embedded beside their canonical digests.
An adapter must use the requested model IDs and preserve its declared version.
Historical execution requires checking out the desired revision first.

The adapter writes these files:

| File | Required contents |
| --- | --- |
| `run_manifest.json` | `execution_mode: measured`, `status: completed`, resolved input digests, adapter identity/version, model IDs, sampling configuration, valid timestamps |
| `cases.jsonl` | One record per model/case, containing every trial ID, its output, and all declared numeric evaluator scores |
| `scorecard.json` | Finite means matching the per-trial scores and the exact declared metric definitions |
| `artifact_refs.json` | A `references` map, empty when no extra files are retained |

The runner writes `run_request.json`, `invocation.json`, and `evaluation.json`.
These records bind the outcome to the invoked adapter configuration and content
hashes. Admission recomputes the outcome when reading stored evidence.

```mermaid
flowchart LR
  S[Resolved input snapshots] --> H[Declared executable adapter]
  H --> E[Complete model / case / trial evidence]
  E --> V[Validate identity and recompute metrics]
  V --> P[Apply suite policy]
  P --> G[Admit baseline or regression gate]
```

Every metric definition includes `version`, `direction`, and `unit`:

```yaml
metric_definitions:
  accuracy:
    version: "1.0.0"
    direction: higher_is_better
    unit: ratio
```

For quick evals, the declared metric is `pass_rate`: each trial scores 1 only
when all its inline assertions pass, followed by an arithmetic mean across
trials. The adapter must implement those assertions. The built-in assertion
helper requires a callable judge for model-assisted assertions, and missing cost
or latency measurements produce an evaluator error. Negation applies only after
a valid evaluation, so errors never become numeric passes.

## Identity and budgets

The [digest convention](../../promptops/schemas/digest-convention.md) defines
semantic identity for structured assets. Formatting-only edits preserve those
digests, and JSONL order remains significant. Duplicate keys and nonfinite
numbers are invalid.

Extra artifact references must use relative local paths within the retained run
directory. Their digests cover raw file bytes. Admission rejects unavailable or
altered files, including external URLs that this runtime cannot verify.

`budgets.cost_budget` requires measured total cost. A genuine zero is valid.
Comparison applies the budget to the combined requested model set. Its optional
`budgets.time` is a wall-clock deadline shared across sequential model runs.
Cost limits are checked after measurement, so one invocation can overspend before
the failure is known. Provider-level spending controls remain the operator's
responsibility.

Regression policies need at least one explicit metric rule. A rule declares its
direction and severity plus a floor/ceiling or allowed delta. Boundaries are
inclusive. Metric versions and units must match between runs, and a claimed
flake rate does not waive a blocking rule. Warnings exit nonzero.

Hashes detect changed content. They do not authenticate a producer or prove that
a dishonest adapter executed what it claims. Operators must obtain run files
from a trusted producer and explicitly approve the adapter used for admission.
Signature verification remains unsupported, including requests made through
cached resolution. Unsigned prompt resolution reports `unverified`.

## CI status for this candidate

The local `ci-gate` command supports explicit execution and evidence modes:

```bash
.agent/bin/apastra ci-gate smoke --adapter promptops/harnesses/local.yaml --revision FULL_COMMIT_SHA --mode execute --run-dir promptops/runs/ci
.agent/bin/apastra ci-gate smoke --adapter promptops/harnesses/local.yaml --revision FULL_COMMIT_SHA --mode evidence --run-dir promptops/runs/ci
```

It checks the checkout revision and compares retained input digests against the
current workspace. Missing evidence blocks admission. Regression mode also
requires `--baseline` and `--policy` together.

CI is optional. Local evaluation and comparison use the runtime checks without
installing a workflow. This candidate leaves repository workflows and distributed
templates unchanged, including their check names and release permissions.

The existing report gate can pass without evidence and does not bind a report to
the tested revision. Treat those templates as unsuitable for required evaluation
checks until the separate repair is complete. Passing local software tests does
not establish that GitHub enforces evaluation results.

## Migration and scope

Version 2.0.0 changes the execution protocol incompatibly. Legacy `success`
manifests, empty scorecards, and scorecard-only baselines remain historical
records. They cannot acquire trusted status through relabeling. Re-execute the
target to produce complete current evidence.

Runtime imports use explicit modules, for example
`from promptops.runtime.suite import evaluate_suite`; the runtime package no
longer eagerly imports every public command.

The following capabilities remain outside the supported executable surface:

- Hosted execution and a provider abstraction layer.
- Automatic optimization or model-generated prompt review through legacy CLI commands.
- Cryptographic verification of signed packages.
- Scheduled canaries, alert delivery, and automated rollback.
- Provider-compatible observability delivery.
- Unresolved community baselines and automatic promotion from a scorecard.
- Judge calibration, confidence intervals, and statistical significance tests.

Schema files for several of these concepts describe proposed records. Their
presence does not establish an implemented integration.
