---
name: apastra-eval
description: Run prompt evaluations using your IDE agent as the harness. Load suites, execute test cases, score results, and compare against baselines.
---

# Apastra Eval

Run prompt evaluations locally. Your IDE agent **is** the harness — no external tools, APIs, or CI needed.

## When to Use

Use this skill when you want to:
- Evaluate a prompt against test cases
- Compare results against a baseline to detect regressions
- Get a scorecard with metrics for a prompt change

## How Evaluation Works

```
Suite → Dataset (cases) → For each case:
  1. Render prompt template with case inputs
  2. Call the model with the rendered prompt
  3. Score the output using evaluators
  4. Record per-case results
→ Aggregate into scorecard
→ Compare against baseline (if exists)
→ Produce regression report
```

## Running an Evaluation

When asked to run an eval (e.g., "run the summarize-smoke suite"), follow these steps exactly:

### Step 1: Load the Suite

Read the suite file from `promptops/suites/<suite-id>.yaml`. Extract:
- `datasets` — list of dataset IDs
- `evaluators` — list of evaluator IDs
- `model_matrix` — list of models (use "default" to mean your own model)
- `trials` — number of times to run each case (default: 1)
- `thresholds` — minimum metric scores to pass

### Step 2: Load Dependencies

For each dataset ID, read `promptops/datasets/<dataset-id>.jsonl` (one JSON object per line).
For each evaluator ID, read `promptops/evaluators/<evaluator-id>.yaml`.
For the prompt being evaluated, read the prompt spec from `promptops/prompts/<prompt-id>.yaml`.

If the suite does not specify which prompt to evaluate, look for a prompt whose `id` matches the suite name prefix, or ask the user which prompt to evaluate.

### Step 3: Run Each Case

For each case in the dataset:

1. **Render the template**: Take the prompt spec's `template` field and substitute `{{variable}}` placeholders with values from the case's `inputs` object.

2. **Call the model**: Send the rendered prompt to the model and capture the full response. If `trials > 1`, run this multiple times.

3. **Score the output**: Apply each evaluator to the model's response:
   - **deterministic** evaluator with `keyword_recall` metric: Check what fraction of the `expected_outputs.should_contain` keywords appear in the model response. Score = (keywords found) / (total keywords). If `should_contain` is empty, score is 1.0.
   - **deterministic** evaluator with `exact_match` metric: Check if the model output exactly matches the expected output. Score is 0 or 1.
   - **schema** evaluator: Validate the model output against the evaluator's `config.schema`. Score is 0 or 1.
   - **judge** evaluator: Use your own judgment to rate the output according to the evaluator's `config.rubric`. Score on a 0-1 scale.

4. **Record the result** for each case:
```json
{
  "case_id": "<from dataset>",
  "inputs": {},
  "output": "<model response>",
  "evaluator_scores": {
    "<metric_name>": <score>
  }
}
```

### Step 4: Aggregate Scorecard

Compute normalized metrics by averaging each metric across all cases:

```json
{
  "normalized_metrics": {
    "keyword_recall": 0.85
  },
  "metric_definitions": {
    "keyword_recall": {
      "description": "Fraction of expected keywords found in output",
      "version": "1.0",
      "direction": "higher_is_better"
    }
  }
}
```

### Step 5: Check Thresholds

Compare each metric against the suite's `thresholds`. If any metric falls below its threshold, the suite **fails**.

Report the results clearly:
```
Suite: summarize-smoke
Status: PASS ✅ (or FAIL ❌)

Metrics:
  keyword_recall: 0.85 (threshold: 0.60) ✅

Per-case results:
  short-article: keyword_recall=1.00 ✅
  technical-paragraph: keyword_recall=1.00 ✅
  empty-edge-case: keyword_recall=1.00 ✅
  long-document: keyword_recall=1.00 ✅
  multi-topic: keyword_recall=0.50 ⚠️
```

### Step 6: Compare Against Baseline (If Exists)

Check if a baseline exists at `derived-index/baselines/<suite-id>.json`.

If a baseline exists:
1. Read the baseline scorecard
2. Read the regression policy from `promptops/policies/regression.yaml`
3. For each rule in the policy, compare the candidate metric against the baseline metric:
   - If `direction` is `higher_is_better`: fail if candidate < (baseline - allowed_delta) or candidate < floor
   - If `direction` is `lower_is_better`: fail if candidate > (baseline + allowed_delta) or candidate > floor
4. Report the regression comparison:

```
Regression Report:
  Baseline: derived-index/baselines/summarize-smoke.json
  Status: PASS ✅ (or REGRESSION DETECTED ❌)

  keyword_recall: 0.85 (baseline: 0.80, delta: +0.05) ✅
```

If no baseline exists, note that no baseline comparison was performed and suggest running the **baseline** skill to establish one.

### Step 7: Save Results

Write the run results to `promptops/runs/<run-id>/`:
- `scorecard.json` — the aggregated metrics
- `cases.jsonl` — per-case results (one JSON object per line)
- `run_manifest.json` — metadata: timestamp, model used, suite ID, prompt digest

Use a run ID like `<suite-id>-<YYYY-MM-DD-HHmmss>` for readability.

## File Reference

| File | Location | Purpose |
|---|---|---|
| Suite | `promptops/suites/<id>.yaml` | Test configuration |
| Dataset | `promptops/datasets/<id>.jsonl` | Test cases (one JSON per line) |
| Evaluator | `promptops/evaluators/<id>.yaml` | Scoring rules |
| Prompt spec | `promptops/prompts/<id>.yaml` | Prompt template + variables |
| Baseline | `derived-index/baselines/<suite-id>.json` | Known-good scorecard |
| Regression policy | `promptops/policies/regression.yaml` | Allowed deltas and severity rules |
| Run output | `promptops/runs/<run-id>/` | Scorecard, cases, manifest |

## Schema Reference

### Scorecard Format
```json
{
  "normalized_metrics": { "<metric>": <number> },
  "metric_definitions": {
    "<metric>": {
      "description": "<string>",
      "version": "<string>",
      "direction": "higher_is_better | lower_is_better"
    }
  },
  "variance": {}
}
```

### Regression Policy Format
```yaml
baseline: "prod-current"
rules:
  - metric: keyword_recall
    floor: 0.5
    allowed_delta: 0.1
    direction: higher_is_better
    severity: blocker
```

## Tips

- Start with small datasets (5-10 cases). You can always add more.
- Use `trials: 1` for smoke suites, `trials: 3+` for regression suites to account for variance.
- If a metric is flaky (varies a lot between runs), increase trials and widen `allowed_delta`.
- Use `thresholds` in the suite for pass/fail. Use `regression.yaml` for comparison against baselines.
