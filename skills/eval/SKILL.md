---
name: apastra-eval
description: Run prompt evaluations using your IDE agent as the harness. Load suites, execute test cases, score results, and compare against baselines.
---

# Apastra Eval

Run prompt evaluations locally. Your IDE agent **is** the harness — no external tools, APIs, or CI needed.

## When to Use

Use this skill when you want to:
- Evaluate a prompt against test cases
- Run a quick eval file (single-file prompt + cases + assertions)
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

## Two Evaluation Modes

Apastra supports two modes. Use whichever fits the situation:

1. **Suite mode** — the full spec/dataset/evaluator/suite pipeline (best for structured, reusable test suites)
2. **Quick eval mode** — a single YAML file in `promptops/evals/` that combines prompt, cases, and inline assertions (best for smoke tests and rapid iteration)

When asked to "run an eval," check whether the user is referencing:
- A suite ID → use Suite mode
- A quick eval file → use Quick eval mode
- If ambiguous, check `promptops/evals/` first, then `promptops/suites/`

---

## Suite Mode

When asked to run a suite (e.g., "run the summarize-smoke suite"), follow these steps:

### Step 1: Load the Suite

Read the suite file from `promptops/suites/<suite-id>.yaml`. Extract:
- `datasets` — list of dataset IDs
- `evaluators` — list of evaluator IDs
- `model_matrix` — list of models (use "default" to mean your own model)
- `harness` — (optional) identifier for the execution environment (e.g., `claude-code`, `antigravity`, `cursor`, `api`, `github-actions`). If omitted, the agent should auto-detect and record it.
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

3. **Score the output**: Apply scoring from two sources:

   **a) Suite evaluators** (from `promptops/evaluators/`):
   - **deterministic** evaluator with `keyword_recall` metric: Check what fraction of the `expected_outputs.should_contain` keywords appear in the model response. Score = (keywords found) / (total keywords). If `should_contain` is empty, score is 1.0.
   - **deterministic** evaluator with `exact_match` metric: Check if the model output exactly matches the expected output. Score is 0 or 1.
   - **schema** evaluator: Validate the model output against the evaluator's `config.schema`. Score is 0 or 1.
   - **judge** evaluator: Use your own judgment to rate the output according to the evaluator's `config.rubric`. Score on a 0-1 scale.

   **b) Inline assertions** (if the case has an `assert` array): Apply each assertion from the case's `assert` field using the assertion types listed below. Each assertion contributes a pass/fail. The case's `assert_pass_rate` = (assertions passed) / (total assertions).

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
- `run_manifest.json` — metadata: timestamp, model used, harness used, suite ID, prompt digest

The `run_manifest.json` should include:
```json
{
  "suite_id": "summarize-smoke",
  "timestamp": "2026-03-16T09:00:00Z",
  "model": "claude-sonnet-4-20250514",
  "harness": "antigravity",
  "prompt_digest": "sha256:abc123...",
  "status": "pass"
}
```

**Harness values:** Use a short identifier for the execution environment. Common values:
- `claude-code` — Claude Code CLI/IDE
- `antigravity` — Antigravity by Google DeepMind
- `cursor` — Cursor IDE agent
- `copilot` — GitHub Copilot agent
- `api` — Direct API call (no IDE agent)
- `github-actions` — CI/CD pipeline
- `jules` — Jules by Google

The harness matters because the same model can produce different results in different environments (system prompts, tool availability, context window handling, etc.).

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

---

## Quick Eval Mode

When asked to run a quick eval (e.g., "run the summarize-quick eval"), follow these steps:

### Step 1: Load the Quick Eval File

Read `promptops/evals/<eval-id>.yaml`. It contains:
- `id` — eval identifier
- `prompt` — the prompt template (with `{{variable}}` placeholders)
- `cases` — array of test cases, each with `id`, `inputs`, and `assert`
- `thresholds` — e.g., `pass_rate: 1.0`

### Step 2: Run Each Case

For each case:
1. Render the prompt template with the case's `inputs`
2. Call the model
3. Apply each assertion from the case's `assert` array (see Assertion Types below)
4. Record pass/fail for each assertion

### Step 3: Report Results

```
Quick Eval: summarize-quick
Status: PASS ✅ (or FAIL ❌)

Cases:
  short: 2/2 assertions passed ✅
  empty-input: 1/1 assertions passed ✅

Pass rate: 1.00 (threshold: 1.00) ✅
```

### Step 4: Save Results

Write results to `promptops/runs/<eval-id>-<timestamp>/` using the same format as suite runs.

---

## Assertion Types Reference

Use these when processing inline `assert` blocks on dataset cases or quick eval cases.

### Deterministic Assertions

| Type | What to Check | Value |
|---|---|---|
| `equals` | Output exactly matches value | `"expected string"` |
| `contains` | Output contains substring (case-sensitive) | `"substring"` |
| `icontains` | Output contains substring (case-insensitive) | `"substring"` |
| `contains-any` | Output contains at least one value | `["a", "b", "c"]` |
| `contains-all` | Output contains every value | `["x", "y", "z"]` |
| `regex` | Output matches regex pattern | `"\\d{3}-\\d{4}"` |
| `starts-with` | Output begins with value | `"Dear "` |
| `is-json` | Output is valid JSON | _(no value needed)_ |
| `contains-json` | Output contains a JSON block | _(no value needed)_ |
| `is-valid-json-schema` | Output matches a JSON Schema | `{schema object}` |

### Model-Assisted Assertions

| Type | What to Check | Value |
|---|---|---|
| `similar` | Semantic similarity to reference (use threshold 0-1) | `"reference text"` |
| `llm-rubric` | AI grades output using rubric | `"rubric text"` |
| `factuality` | Output is factually consistent with reference | `"reference facts"` |
| `answer-relevance` | Output is relevant to the input | _(no value needed)_ |

### Performance Assertions

| Type | What to Check | Threshold |
|---|---|---|
| `latency` | Response time in ms | `500` |
| `cost` | Token cost in dollars | `0.01` |

### Negation

Any assertion type can be negated by prepending `not-`. For example:
- `not-contains` — output must NOT contain the value
- `not-regex` — output must NOT match the regex
- `not-is-json` — output must NOT be valid JSON

### How to Apply Each Assertion

For each assertion in a case's `assert` array:
1. Read `type` and `value` (and optionally `threshold` for `similar`, `latency`, `cost`)
2. Run the check against the model output
3. Record pass (1) or fail (0)
4. If the type starts with `not-`, invert the result

---

## Writing Good Evals

This section teaches you how to write effective evaluations — not just how to run them. These best practices come from Anthropic, Hamel Husain, OpenAI, and production teams running evals at scale.

### The Eval Maturity Ladder

Start at Level 1 and graduate upward as your prompt matures:

| Level | What | When to use | Apastra tools |
|---|---|---|---|
| **1. Deterministic checks** | Assertions like `contains`, `is-json`, `regex` | Always — these are fast, free, and run on every change | Inline assertions, quick eval files |
| **2. AI-graded checks** | `llm-rubric`, `similar`, `factuality` | When deterministic checks can't capture quality (tone, coherence, reasoning) | Judge evaluators, `llm-rubric` assertions |
| **3. Baseline comparison** | Compare scorecards against a known-good run | When you need regression detection across prompt changes | Baseline skill, regression policies |
| **4. Human review** | Periodic spot-checks of model outputs | When you need to calibrate AI judges or validate subjective quality | Manual scorecard review |

**Start at Level 1.** Most teams get enormous value from 10-20 deterministic checks before they ever need AI grading.

### Designing Test Cases

**1. Start from real failures, not hypotheticals**
- Look at actual bad outputs your prompt has produced. Turn each one into a test case.
- If you don't have failures yet, try the prompt with adversarial inputs and edge cases to find them.

**2. Break your prompt into features and scenarios**
- Decompose what your prompt does into discrete capabilities.
- Write separate test cases for each capability. Example for a "classify email" prompt:
  - ✅ Correctly classifies obvious spam
  - ✅ Handles ambiguous emails (could be sales or support)
  - ✅ Returns valid JSON
  - ✅ Doesn't expose internal IDs or metadata
  - ✅ Handles empty input gracefully

**3. Cover these categories:**

| Category | Examples |
|---|---|
| Happy path | Normal inputs that should work correctly |
| Edge cases | Empty input, very long input, special characters, Unicode |
| Adversarial | Prompt injection, jailbreak attempts, off-topic requests |
| Format compliance | JSON output, length limits, required fields |
| Safety | Refusal of harmful requests, PII handling |

**4. Use your agent to generate test cases**
- Ask your IDE agent: "Generate 20 test cases for this prompt, including edge cases and adversarial inputs."
- Review and curate the generated cases — don't blindly trust synthetic data.

**5. Prioritize volume over perfection** (Anthropic's recommendation)
- 50 cases with automated grading > 10 cases with careful human review.
- You can always improve case quality later; you can't retroactively add coverage.

### Choosing the Right Assertion Type

| If you want to check... | Use this assertion | Example |
|---|---|---|
| Output contains specific keywords | `contains` / `icontains` | `{"type": "icontains", "value": "summary"}` |
| Output is valid JSON | `is-json` | `{"type": "is-json"}` |
| Output matches a specific structure | `is-valid-json-schema` | `{"type": "is-valid-json-schema", "value": {"type": "object", "required": ["category"]}}` |
| Output doesn't leak internal data | `not-regex` | `{"type": "not-regex", "value": "[0-9a-f]{8}-[0-9a-f]{4}"}` |
| Output is semantically similar to a reference | `similar` | `{"type": "similar", "value": "expected answer", "threshold": 0.8}` |
| Output quality requires judgment | `llm-rubric` | `{"type": "llm-rubric", "value": "Is the response helpful, accurate, and concise?"}` |
| Output mentions at least one of several options | `contains-any` | `{"type": "contains-any", "value": ["yes", "correct", "affirmative"]}` |

### Writing Good Judge Rubrics

When using `llm-rubric` or judge evaluators:

1. **Be specific, not vague.** ❌ "Is the output good?" → ✅ "Does the output mention the company name in the first sentence? Does it use a professional tone? Is it under 100 words?"
2. **Use binary or numeric scales.** Ask for "correct/incorrect" or a 1-5 scale, not open-ended qualitative feedback.
3. **Ask the judge to reason first.** "Think step by step about whether this output meets the criteria, then give a score." This improves grading accuracy.
4. **Version your rubrics.** Changing the rubric text changes what the metric means. Treat rubric edits as new evaluator versions.
5. **Calibrate against human judgment.** Periodically score 25-50 outputs yourself and compare against the judge. If they diverge, refine the rubric.

### Common Eval Mistakes

| Mistake | Why it's bad | Fix |
|---|---|---|
| Only testing happy paths | You miss the failures that matter most | Add edge cases and adversarial inputs |
| Using `equals` for free-text outputs | LLM output is non-deterministic — exact match almost always fails | Use `contains`, `icontains`, or `similar` instead |
| Thresholds set too high | Flaky evals erode trust — people start ignoring failures | Start with achievable thresholds (e.g., 0.6), tighten over time |
| No baseline comparison | You can't tell if a prompt change made things worse | Establish a baseline after your first passing run |
| Ignoring flaky cases | Random noise masks real regressions | Increase `trials`, quarantine consistently flaky cases |
| Overfitting to test cases | Prompt works for tests but fails in production | Maintain a holdout set, add cases from real production failures |

### Evolving Your Evals Over Time

1. **Week 1**: Start with a quick eval file — 5 cases, deterministic assertions only.
2. **Week 2-3**: Graduate to a full suite. Add 20+ cases. Establish your first baseline.
3. **Month 2+**: Add judge evaluators for subjective quality. Set up regression policies.
4. **Ongoing**: Promote real production failures into your "never again" regression suite. Periodically calibrate AI judges against human judgment.

---

## Tips

- Start with small datasets (5-10 cases). You can always add more.
- Use quick eval files for smoke tests and rapid iteration. Graduate to full suites as complexity grows.
- Use `trials: 1` for smoke suites, `trials: 3+` for regression suites to account for variance.
- If a metric is flaky (varies a lot between runs), increase trials and widen `allowed_delta`.
- Use `thresholds` in the suite for pass/fail. Use `regression.yaml` for comparison against baselines.
- Inline assertions and evaluator files can both apply to the same case — they complement each other.
- When stuck on what to test, ask your agent: "What are the failure modes of this prompt?" Use the answer to write cases.

