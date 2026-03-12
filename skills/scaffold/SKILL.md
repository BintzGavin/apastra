---
name: apastra-scaffold
description: Generate new prompt specs, datasets, evaluators, and suites from templates. Creates correctly-formatted files that pass schema validation.
---

# Apastra Scaffold

Quickly generate new PromptOps files. All generated files follow the apastra schemas and will pass validation.

## When to Use

Use this skill when you want to:
- Create a new prompt spec for a new use case
- Add test cases for an existing prompt
- Create an evaluator for a new scoring rule
- Set up a new suite tying everything together

## Scaffolding a Prompt Spec

When asked to create a new prompt (e.g., "scaffold a prompt for email classification"):

Create `promptops/prompts/<id>.yaml`:

```yaml
id: <kebab-case-id>
variables:
  <var_name>:
    type: string
template: |
  <The actual prompt text with {{var_name}} placeholders>
output_contract:
  type: object
  properties:
    <output_field>:
      type: string
metadata:
  author: <user or team name>
  intent: <what this prompt does>
  tags:
    - <relevant-tags>
```

### Rules for Prompt Specs
- `id` is **required** and must be unique across all prompt specs
- `id` should be kebab-case and include a version suffix (e.g., `classify-email-v1`)
- `variables` is **required** — defines the input schema as a map of variable names to JSON Schema type objects
- `template` is **required** — the prompt text with `{{variable}}` placeholders
- `output_contract` is optional but recommended — defines expected output structure
- `metadata` is optional — use for organization and discovery

## Scaffolding a Dataset

When asked to create test cases (e.g., "create test cases for the email classifier"):

Create `promptops/datasets/<id>.jsonl` — one JSON object per line:

```jsonl
{"case_id": "<unique-case-id>", "inputs": {"<var>": "<value>"}, "expected_outputs": {"<field>": "<expected>"}, "metadata": {"tags": ["<tag>"]}}
```

### Rules for Datasets
- Use `.jsonl` format (one JSON object per line, NOT a JSON array)
- `case_id` is **required** and must be unique within the dataset
- `inputs` is **required** — keys must match the prompt spec's `variables`
- `expected_outputs` is optional — used by evaluators for checking
- `metadata` is optional — useful for tagging difficulty, domain, etc.
- Aim for 5-10 cases in a smoke dataset, 50+ in a regression dataset
- Include edge cases: empty inputs, very long inputs, adversarial inputs

## Scaffolding an Evaluator

When asked to create a scoring rule (e.g., "create an evaluator that checks for JSON output"):

Create `promptops/evaluators/<id>.yaml`:

```yaml
id: <evaluator-id>
type: <deterministic | schema | judge>
metrics:
  - <metric-name>
description: <what this evaluator checks>
config:
  <evaluator-specific configuration>
```

### Evaluator Types

**deterministic** — rule-based checks:
```yaml
id: keyword-check
type: deterministic
metrics:
  - keyword_recall
description: Checks if output contains expected keywords.
config:
  match_field: should_contain
  case_sensitive: false
```

**schema** — validates output structure:
```yaml
id: json-output-valid
type: schema
metrics:
  - schema_valid
description: Validates that model output is valid JSON matching the output contract.
config:
  schema:
    type: object
    required: ["category", "confidence"]
    properties:
      category:
        type: string
      confidence:
        type: number
```

**judge** — AI-graded evaluation:
```yaml
id: quality-judge
type: judge
metrics:
  - coherence
  - relevance
description: Uses AI judgment to score output quality.
config:
  rubric: |
    Score the output on two dimensions (0-1 each):
    - coherence: Is the text well-structured and readable?
    - relevance: Does the output address the input query?
  model: default
```

### Rules for Evaluators
- `id` is **required** and must be unique
- `type` is **required** — must be one of: `deterministic`, `schema`, `judge`
- `metrics` is **required** — array of metric names this evaluator produces (minimum 1)
- For `judge` evaluators: always version the rubric — changing it changes what the metric means

## Scaffolding a Suite

When asked to create a test suite (e.g., "create a smoke suite for the email classifier"):

Create `promptops/suites/<id>.yaml`:

```yaml
id: <suite-id>
name: <Human Readable Name>
description: <what this suite tests>
datasets:
  - <dataset-id>
evaluators:
  - <evaluator-id>
model_matrix:
  - default
trials: 1
thresholds:
  <metric>: <minimum-score>
```

### Suite Tiers (Recommended)

| Tier | When to Run | Cases | Trials |
|---|---|---|---|
| Smoke | Every prompt edit | 5-10 | 1 |
| Regression | Before merging | 20-50 | 3 |
| Full | Nightly / on-demand | 50+ | 5 |
| Release | Before shipping | 100+ | 5 |

### Rules for Suites
- `id` is **required** and must be unique
- `name` is **required** — human-readable
- `datasets` is **required** — at least one dataset reference
- `evaluators` is **required** — at least one evaluator reference
- `model_matrix` is **required** — at least one model identifier
- Use `"default"` in `model_matrix` to test against the current IDE agent's model

## Full Scaffold Example

When asked something like "scaffold a complete PromptOps setup for sentiment analysis," create all four files:

1. `promptops/prompts/sentiment-v1.yaml`
2. `promptops/datasets/sentiment-smoke.jsonl`
3. `promptops/evaluators/sentiment-accuracy.yaml`
4. `promptops/suites/sentiment-smoke.yaml`
