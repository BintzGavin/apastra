---
name: apastra-eval
description: Run prompt evaluations using your IDE agent as the harness. Load suites, execute test cases, score results, and compare against baselines.
---

# Apastra Eval

Run prompt evaluations locally. Your IDE agent **is** the harness — no external tools, APIs, or CI needed.

Deterministic steps (rendering, scoring, normalization, comparison) are handled by Python scripts in `promptops/`. You handle the LLM-dependent parts: calling the model and grading with judge evaluators.

## When to Use

Use this skill when you want to:
- Evaluate a prompt against test cases
- Run a quick eval file (single-file prompt + cases + assertions)
- Compare results against a baseline to detect regressions
- Get a scorecard with metrics for a prompt change

## Two Evaluation Modes

1. **Suite mode** — the full spec/dataset/evaluator/suite pipeline
2. **Quick eval mode** — a single YAML file in `promptops/evals/`

When asked to "run an eval," check whether the user is referencing a suite ID or a quick eval file. If ambiguous, check `promptops/evals/` first, then `promptops/suites/`.

---

## Suite Mode

### Step 1: Load the Suite

Read `promptops/suites/<suite-id>.yaml`. Extract `datasets`, `evaluators`, `model_matrix`, `trials`, `thresholds`.

### Step 2: Load Dependencies

- For each dataset ID, read `promptops/datasets/<dataset-id>.jsonl`
- For each evaluator ID, read `promptops/evaluators/<evaluator-id>.yaml`
- For the prompt, read `promptops/prompts/<prompt-id>.yaml`

### Step 3: Compute Digests

Run the digest script to fingerprint all inputs:

```bash
python .agent/scripts/apastra/runtime/digest.py promptops/prompts/<prompt-id>.yaml
python .agent/scripts/apastra/runtime/digest.py promptops/datasets/<dataset-id>.jsonl
python .agent/scripts/apastra/runtime/digest.py promptops/suites/<suite-id>.yaml
```

Record these in the run manifest for traceability.

### Step 4: Run Each Case

For each case in the dataset:

1. **Render the template**: The agent substitutes `{{variable}}` placeholders with values from the case's `inputs`. (For reference, this follows the same logic as `.agent/scripts/apastra/runtime/render.py`.)

2. **Call the model**: Send the rendered prompt to the model and capture the response. If `trials > 1`, run multiple times.

3. **Score the output** using two sources:

   **a) Suite evaluators** (from `promptops/evaluators/`):
   - **deterministic** with `keyword_recall`: fraction of `expected_outputs.should_contain` keywords found in output
   - **deterministic** with `exact_match`: output exactly matches expected. Score is 0 or 1.
   - **schema**: validate output against `config.schema`. Score is 0 or 1.
   - **judge**: YOU (the agent) rate the output per `config.rubric` on a 0-1 scale.

   **b) Inline assertions** (if the case has an `assert` array): Write the model output to a temp file and run:

   ```bash
   python .agent/scripts/apastra/runs/evaluate_assertions.py <output.txt> <assertions.json>
   ```

   This returns a JSON array of `{"assert_<type>": 1.0 or 0.0}` results.

4. **Record the result** as one JSONL line in `cases.jsonl`:
```json
{"case_id": "<id>", "inputs": {}, "output": "<response>", "evaluator_outputs": [{"<metric>": <score>}]}
```

### Step 5: Normalize into Scorecard

Run the normalization script to aggregate per-case results into a scorecard:

```bash
python .agent/scripts/apastra/runs/normalize.py <cases.jsonl> <scorecard.json>
```

This computes mean metrics, variance, and flake rates automatically.

### Step 6: Check Thresholds

Compare each metric in `scorecard.json` against the suite's `thresholds`. If any metric falls below its threshold, the suite **fails**.

Report results:
```
Suite: summarize-smoke
Status: PASS ✅ (or FAIL ❌)

Metrics:
  keyword_recall: 0.85 (threshold: 0.60) ✅

Per-case results:
  short-article: keyword_recall=1.00 ✅
  multi-topic: keyword_recall=0.50 ⚠️
```

### Step 7: Compare Against Baseline

If a baseline exists at `derived-index/baselines/<suite-id>.json`:

1. Read the baseline scorecard
2. Read `promptops/policies/regression.yaml`
3. For each rule, compare candidate vs baseline:
   - `higher_is_better`: fail if candidate < (baseline - allowed_delta) or candidate < floor
   - `lower_is_better`: fail if candidate > (baseline + allowed_delta) or candidate > floor
4. Report the comparison

If no baseline exists, suggest running the **baseline** skill.

### Step 8: Save Results

Write to `promptops/runs/<suite-id>-<YYYY-MM-DD-HHmmss>/`:
- `scorecard.json` — aggregated metrics (output of normalize.py)
- `cases.jsonl` — per-case results
- `run_manifest.json` — metadata: timestamp, model, harness, suite ID, prompt digest

---

## Quick Eval Mode

### Step 1: Load the Quick Eval File

Read `promptops/evals/<eval-id>.yaml`. It contains `id`, `prompt`, `cases`, and `thresholds`.

### Step 2: Run Each Case

For each case:
1. Render the prompt template with the case's `inputs`
2. Call the model
3. Write the output to a temp file and run assertions:
   ```bash
   python .agent/scripts/apastra/runs/evaluate_assertions.py <output.txt> <assertions.json>
   ```
4. Record pass/fail for each assertion

### Step 3: Report Results

```
Quick Eval: summarize-quick
Status: PASS ✅

Cases:
  short: 2/2 assertions passed ✅
  empty-input: 1/1 assertions passed ✅

Pass rate: 1.00 (threshold: 1.00) ✅
```

### Step 4: Save Results

Write results to `promptops/runs/<eval-id>-<timestamp>/` using the same format as suite runs.

---

## Script Reference

| Script | Purpose | CLI Usage |
|---|---|---|
| `promptops/runtime/digest.py` | Compute content digest | `python .agent/scripts/apastra/runtime/digest.py <file>` |
| `promptops/runs/evaluate_assertions.py` | Evaluate inline assertions | `python .agent/scripts/apastra/runs/evaluate_assertions.py <output.txt> <assertions.json>` |
| `promptops/runs/normalize.py` | Aggregate cases into scorecard | `python .agent/scripts/apastra/runs/normalize.py <cases.jsonl> <scorecard.json>` |
| `.agent/scripts/apastra/runtime/runner.py` | Full harness runner (adapter mode) | `python .agent/scripts/apastra/runtime/runner.py <request.json> <adapter.yaml> <outdir>` |
| `.agent/scripts/apastra/runs/compare.py` | Cross-model comparison | `python .agent/scripts/apastra/runs/compare.py <suite-id> [models...]` |
| `.agent/scripts/apastra/runtime/render.py` | Template rendering (importable) | Used as reference for `{{var}}` substitution |

## Harness Values

Use a short identifier for the execution environment in `run_manifest.json`:
- `claude-code`, `cursor`, `copilot`, `antigravity`, `jules`, `api`, `github-actions`

The harness matters because the same model can produce different results in different environments.

---

## Writing Good Evals

### The Eval Maturity Ladder

| Level | What | When | Apastra tools |
|---|---|---|---|
| 1. Deterministic checks | `contains`, `is-json`, `regex` | Always | Inline assertions, quick eval |
| 2. AI-graded checks | `llm-rubric`, `similar` | When deterministic can't capture quality | Judge evaluators |
| 3. Baseline comparison | Compare scorecards | When you need regression detection | Baseline skill, policies |
| 4. Human review | Spot-checks | To calibrate AI judges | Manual review |

### Designing Test Cases

- Start from **real failures**, not hypotheticals
- Cover: happy path, edge cases, adversarial, format compliance, safety
- Prioritize **volume over perfection**: 50 cases with automated grading > 10 with careful review

### Assertion Types

**Deterministic**: `equals`, `contains`, `icontains`, `contains-any`, `contains-all`, `regex`, `starts-with`, `is-json`, `contains-json`, `is-valid-json-schema`

**Model-assisted**: `similar`, `llm-rubric`, `factuality`, `answer-relevance`

**Performance**: `latency`, `cost`

Negate any type with `not-` prefix (e.g., `not-contains`).

All assertion evaluation is handled by `promptops/runs/evaluate_assertions.py` — do not reimplement assertion logic yourself.
