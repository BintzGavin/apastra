# Promptfoo quick-eval adapter

This adapter executes **Promptfoo 0.124.1** and converts retained provider responses into Apastra's measured evidence contract. It supports inline quick evals with `pass_rate`; it does not implement a provider API or judge model. The selected Promptfoo providers execute the requests.

Install the pinned Promptfoo CLI separately using its [official installation instructions](https://www.promptfoo.dev/docs/installation/). Apastra does not install or download it during a run. The adapter checks the executable's exact version before executing providers.

From this repository, with the pinned CLI available:

```bash
python3 bin/apastra quick-eval path/to/quick-eval.yaml \
  --models file:///absolute/path/to/your_python_provider.py \
  --adapter promptops/harnesses/promptfoo/adapter.yaml
```

For a consumer installed with the project setup, use `.agent/bin/apastra` and create `promptops/harnesses/promptfoo.yaml` with this complete configuration:

```yaml
id: promptfoo
type: harness_adapter
version: 1.0.0
execution_mode: measured
capabilities: [run_suite, model_matrix, trials]
entrypoint: python3 .agent/scripts/apastra/harnesses/promptfoo/run.py --promptfoo-executable /absolute/path/to/promptfoo
```

Then select `--adapter promptops/harnesses/promptfoo.yaml`. This consumer example deliberately omits `implementation` and is admitted as `configuration_only`; it does not pin adapter code. Do not copy the source example's `implementation.files.run.py` entry into a different directory: declared file paths resolve relative to the configuration file. A pinned consumer configuration must place the script under its configuration directory and use the corresponding safe relative path and actual raw-byte digest.

Entry points are split into argument vectors; shell syntax is not executed. A value-free executable wrapper may configure provider authentication through an appropriate secret store. Never put credential values in the configuration or command.

Provider IDs in `--models` are forwarded explicitly, without a default model or fallback. Local provider references currently support Python files, converted to absolute `file://` paths. Other provider IDs use Promptfoo's normal provider resolution. Unknown providers and provider errors fail; the adapter never substitutes an example output. A local Python target can test the integration, but its success does not establish the quality of a hosted LLM.

The adapter does not read or enumerate environment variables. Promptfoo inherits the caller's environment to support operator-managed authentication. Each invocation runs in a new retained output subdirectory with an explicitly empty dotenv file, avoiding an implicit project `.env` load. Do not run untrusted provider code with privileged credentials. Our verification launches the CLI and adapter with an explicit synthetic environment and no provider keys.

## Supported contract

- Only the exact `inline-assertions-v2` deterministic quick-eval evaluator and its `pass_rate` metric are supported.
- Prompt templates use simple `{{variable}}` substitution, including whitespace around variable names. Inputs must supply exactly those variables as strings. Template expressions, structured prompts, and rendered `file://` references are rejected.
- Assertions: `equals`, `contains`, `icontains`, `contains-any`, `contains-all`, `regex`, `starts-with`, `is-json`, `contains-json`, `is-valid-json-schema`, and their `not-` forms. All assertions must pass for a trial to score 1; the scorecard is the mean of actual trial scores. Scoring delegates to Apastra’s existing built-in assertion engine, including its Unicode and embedded-JSON behavior. Regexes use Python semantics. JSON Schema uses draft 2020-12; external references are rejected.
- Model judges, similarity, latency/cost assertions, assertion thresholds, nonempty sampling configuration, run budgets, and unsupported evaluator modes fail explicitly. The run timeout is supported.
- Each requested model receives a separate real `promptfoo eval` invocation. Case/trial combinations are explicit tests, with repeat 1, variable expansion disabled, caching disabled, and no shared conversation state.

```text
quick-eval request
  -> generated config per requested model
  -> real Promptfoo provider calls, cache disabled
  -> retained raw JSONL + exact case/trial/prompt checks
  -> Apastra assertions score each actual response
  -> manifest + scorecard + cases + artifact references
  -> normal runtime admission
```

The parser requires complete, unique test indexes, model labels, case/trial metadata, rendered prompts, and string responses. Error rows fail even if they contain an output. Missing, extra, stale, or cached rows fail. Promptfoo's summary grades and success percentages are never used as Apastra quality scores. Measured costs are retained only when every result supplies a valid cost; unknown cost is never invented as zero.

Generated configuration and raw JSONL exports stay under `promptfoo/` inside the run directory and are referenced by raw-byte SHA-256 hashes. The four core evidence files are written only after every model completes and its raw results validate. A failed run retains diagnostic raw artifacts but cannot be admitted as a complete run. Existing run directories are never reused or overwritten; start a new run to retry.

The sample descriptor pins the raw bytes of `run.py` only. This detects changes to that declared file; it does not pin the imported assertion engine, Python dependencies, Promptfoo installation, provider code, or complete dependency closure. Update the declared file hash deliberately when changing the script.

## Verification and limits

Acceptance tests execute the real pinned CLI with two local Python providers, two cases, and repeated trials. They verify passing responses, quality failure from incorrect responses, provider errors, unknown provider failure, and runtime admission. Protocol tests cover missing/duplicate/mismatched results, cached results, changed prompts, unsupported evaluator/sampling/assertion modes, and deterministic assertion scoring.

Run the real CLI acceptance checks explicitly from this repository:

```bash
python3 -m tests.test_promptfoo_adapter --promptfoo-executable /absolute/path/to/promptfoo
```

Without that option, tests use a repository-local `node_modules/.bin/promptfoo` when available; otherwise the real CLI integration is reported as skipped. Protocol tests always run.

Hosted provider execution, operator authentication wrappers, other Promptfoo releases, and model-based grading remain unverified. Export shape changes require review and updated acceptance tests before changing the version pin.

Official references: [Python providers](https://www.promptfoo.dev/docs/providers/python/), [JSONL exports](https://www.promptfoo.dev/docs/configuration/outputs/), [CLI options](https://www.promptfoo.dev/docs/usage/command-line/), [configuration reference](https://www.promptfoo.dev/docs/configuration/reference/).
