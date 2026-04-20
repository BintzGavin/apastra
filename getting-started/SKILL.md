---
name: apastra-getting-started
description: Quick setup guide for apastra PromptOps. Create your first prompt spec, dataset, evaluator, and suite in 5 minutes.
---

# Apastra Getting Started

Set up prompt versioning and evaluation in any project. No CI, no cloud, no framework — just files and your IDE agent.

## What Is Apastra?

Apastra treats AI prompts as versioned software assets. Prompts, test cases, and scoring rules are files in your repo. Your IDE agent runs evaluations, compares results against baselines, and catches regressions — all locally.

## Quick Setup

### 1. Create the promptops directory

```bash
mkdir -p promptops/prompts promptops/datasets promptops/evaluators promptops/suites promptops/schemas promptops/policies derived-index/baselines derived-index/regressions
```

### 2. Create your first prompt spec

Create `promptops/prompts/summarize.yaml`:

```yaml
id: summarize-v1
variables:
  text:
    type: string
  max_length:
    type: string
template: |
  Summarize the following text in {{max_length}} or fewer words.
  Be concise and capture the key points.

  Text: {{text}}
output_contract:
  type: object
  properties:
    summary:
      type: string
metadata:
  author: your-name
  intent: text-summarization
  tags:
    - summarization
    - core
```

A prompt spec has:
- **id**: stable identifier (never rename, create a new version instead)
- **variables**: the inputs the prompt template expects, with JSON Schema types
- **template**: the actual prompt text with `{{variable}}` placeholders
- **output_contract** (optional): JSON Schema describing expected output structure
- **metadata** (optional): tags, author, intent for organization

### 3. Create test cases

Create `promptops/datasets/summarize-smoke.jsonl` — one JSON object per line:

```jsonl
{"case_id": "short-article", "inputs": {"text": "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for typing practice.", "max_length": "20"}, "expected_outputs": {"should_contain": ["fox", "dog"]}}
{"case_id": "technical-paragraph", "inputs": {"text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can access data and use it to learn for themselves.", "max_length": "30"}, "expected_outputs": {"should_contain": ["machine learning", "algorithms"]}}
{"case_id": "empty-edge-case", "inputs": {"text": "", "max_length": "10"}, "expected_outputs": {"should_contain": []}}
{"case_id": "long-document", "inputs": {"text": "Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to the burning of fossil fuels like coal, oil, and gas, which produces heat-trapping gases.", "max_length": "25"}, "expected_outputs": {"should_contain": ["climate"]}}
{"case_id": "multi-topic", "inputs": {"text": "Python is a programming language. JavaScript runs in browsers. Rust focuses on memory safety. Go was created at Google for systems programming.", "max_length": "20"}, "expected_outputs": {"should_contain": ["programming"]}}
```

Each case has:
- **case_id**: stable identifier for tracking results across runs
- **inputs**: values for the prompt template variables
- **expected_outputs** (optional): values for evaluators to check against

### 4. Create an evaluator

Create `promptops/evaluators/contains-keywords.yaml`:

```yaml
id: contains-keywords
type: deterministic
metrics:
  - keyword_recall
description: Checks if the model output contains expected keywords from the test case.
config:
  match_field: should_contain
  case_sensitive: false
```

Evaluator types:
- **deterministic**: exact match, substring check, regex, keyword recall
- **schema**: validates output against a JSON Schema
- **judge**: uses another AI model to grade output (version the judge prompt!)

### 5. Create a smoke suite

Create `promptops/suites/summarize-smoke.yaml`:

```yaml
id: summarize-smoke
name: Summarize Smoke Suite
description: Quick sanity check for the summarization prompt.
datasets:
  - summarize-smoke
evaluators:
  - contains-keywords
model_matrix:
  - default
trials: 1
thresholds:
  keyword_recall: 0.6
```

A suite ties everything together:
- **datasets**: which test case files to use
- **evaluators**: which scoring rules to apply
- **model_matrix**: which models to test against (use "default" for your IDE agent's model)
- **thresholds**: minimum scores to pass

### 6. Run your first evaluation

Use the **eval** skill:
> Tell your agent: "Use the eval skill to run the summarize-smoke suite"

Or if you have the eval skill installed, your agent already knows how.

### Alternative: Quick Eval (Single File)

If you want to skip creating 4 separate files, use a quick eval instead. Create `promptops/evals/summarize-quick.yaml`:

```yaml
id: summarize-quick
prompt: "Summarize in {{max_length}} words: {{text}}"
cases:
  - id: short
    inputs: { text: "The fox jumps over the dog.", max_length: "10" }
    assert:
      - type: icontains
        value: "fox"
thresholds:
  pass_rate: 1.0
```

Then tell your agent: "Run the summarize-quick eval". This is the fastest way to test a prompt.

## File Structure

After setup, your project should look like:

```
promptops/
├── prompts/
│   └── summarize.yaml          # Prompt specs (source of truth)
├── datasets/
│   └── summarize-smoke.jsonl   # Test cases (with optional inline assertions)
├── evaluators/
│   └── contains-keywords.yaml  # Scoring rules (optional if using inline assertions)
├── evals/
│   └── summarize-quick.yaml    # Quick eval files (prompt + cases + assertions)
├── suites/
│   └── summarize-smoke.yaml    # Test configurations
├── schemas/                    # JSON schemas (from apastra)
├── policies/                   # Regression policies
├── runtime/                    # Deterministic scripts (digest, render, runner)
├── runs/                       # Run scripts (normalize, evaluate_assertions, compare)
└── validators/                 # Shell scripts for schema validation
derived-index/
├── baselines/                  # Known-good scorecards
└── regressions/                # Regression reports
```

The `runtime/`, `runs/`, and `validators/` directories are shipped with apastra and contain deterministic scripts. The skills call these scripts — you don't need to write or modify them.

## Next Steps

1. Use the **eval** skill to run your first evaluation
2. Use the **baseline** skill to establish your first baseline
3. Use the **scaffold** skill to quickly generate new prompt specs
4. Use the **validate** skill to check file formatting
5. **Upgrade to CI**: Use the **setup-ci** skill to add GitHub Actions for PR gating and releases

## Checklist

- [ ] Created `promptops/` directory structure
- [ ] Created at least one prompt spec in `promptops/prompts/`
- [ ] Created at least one dataset in `promptops/datasets/`
- [ ] Created at least one evaluator in `promptops/evaluators/`
- [ ] Created at least one suite in `promptops/suites/`
- [ ] Ran first evaluation using the eval skill
