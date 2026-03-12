---
name: apastra-validate
description: Validate all promptops files against JSON schemas. Catch formatting errors before running evaluations.
---

# Apastra Validate

Validate PromptOps files against the apastra JSON schemas. Catches formatting errors, missing required fields, and invalid values before you run evaluations.

## When to Use

Use this skill when you want to:
- Check that prompt specs, datasets, evaluators, and suites are correctly formatted
- Validate files after scaffolding or manual edits
- Debug why an evaluation run is failing

## Validation Process

When asked to validate (e.g., "validate my promptops files"):

### Step 1: Discover Files

Scan the `promptops/` directory for files to validate:

| File Pattern | Schema |
|---|---|
| `promptops/prompts/*.yaml` or `*.json` | Prompt Spec |
| `promptops/datasets/*.jsonl` | Dataset Case (per line) |
| `promptops/evaluators/*.yaml` or `*.json` | Evaluator |
| `promptops/suites/*.yaml` or `*.json` | Suite |
| `promptops/policies/*.yaml` | Regression Policy |

### Step 2: Validate Each File

For each file, check against the corresponding schema rules:

**Prompt Spec** (`promptops/prompts/`):
- ✅ Has `id` (string, required)
- ✅ Has `variables` (object, required) — each value should have a `type` field
- ✅ Has `template` (string, object, or array — required)
- ✅ `output_contract` if present is a valid object
- ✅ `metadata` if present is a valid object
- ⚠️ Template uses `{{variable}}` placeholders that match keys in `variables`

**Dataset** (`promptops/datasets/*.jsonl`):
- ✅ Each line is valid JSON
- ✅ Each line has `case_id` (string, required)
- ✅ Each line has `inputs` (object, required)
- ✅ `case_id` values are unique within the file
- ⚠️ `inputs` keys should match the target prompt spec's `variables`

**Evaluator** (`promptops/evaluators/`):
- ✅ Has `id` (string, required)
- ✅ Has `type` (required, must be one of: `deterministic`, `schema`, `judge`)
- ✅ Has `metrics` (array of strings, required, minimum 1 item)
- ✅ `config` if present is a valid object

**Suite** (`promptops/suites/`):
- ✅ Has `id` (string, required)
- ✅ Has `name` (string, required)
- ✅ Has `datasets` (array of strings, required, minimum 1)
- ✅ Has `evaluators` (array of strings, required, minimum 1)
- ✅ Has `model_matrix` (array of strings, required, minimum 1)
- ✅ `trials` if present is an integer >= 1
- ⚠️ Referenced `datasets` exist in `promptops/datasets/`
- ⚠️ Referenced `evaluators` exist in `promptops/evaluators/`

**Regression Policy** (`promptops/policies/`):
- ✅ Has `baseline` (string, required)
- ✅ Has `rules` (array, required)
- ✅ Each rule has `metric` (string) and `severity` (`blocker` or `warning`)

### Step 3: Cross-Reference Check

After individual file validation, check cross-references:
- Suites reference datasets that exist
- Suites reference evaluators that exist
- Dataset `inputs` keys match prompt spec `variables` keys
- Evaluator `metrics` match suite `thresholds` keys (if thresholds are defined)

### Step 4: Report

Output a clear validation report:

```
Validation Report
=================

Prompt Specs:
  ✅ summarize-v1 (promptops/prompts/summarize.yaml)
  ❌ classify-v1 (promptops/prompts/classify.yaml)
     └── Missing required field: variables

Datasets:
  ✅ summarize-smoke (promptops/datasets/summarize-smoke.jsonl) — 5 cases
  ⚠️ classify-smoke (promptops/datasets/classify-smoke.jsonl) — 3 cases
     └── Warning: inputs.category not in prompt spec variables

Evaluators:
  ✅ contains-keywords (promptops/evaluators/contains-keywords.yaml)

Suites:
  ✅ summarize-smoke (promptops/suites/summarize-smoke.yaml)
  ❌ classify-smoke (promptops/suites/classify-smoke.yaml)
     └── Referenced dataset 'classify-full' not found

Summary: 3 passed, 2 issues (1 error, 1 warning)
```

## Using Shell Validators (Optional)

If the project has `promptops/validators/` with shell scripts, you can also run those for strict JSON Schema validation:

```bash
# Validate a prompt spec
bash promptops/validators/validate-prompt-spec.sh <file.json>

# Validate a suite
bash promptops/validators/validate-suite.sh <file.json>

# Validate an evaluator
bash promptops/validators/validate-evaluator.sh <file.json>
```

These require `npx ajv-cli` and validate against the JSON schemas in `promptops/schemas/`.

## Tips

- Run validation after scaffolding to catch typos
- Run validation before eval to avoid confusing errors
- The ⚠️ warnings are non-blocking but worth fixing
- The ❌ errors will cause evaluation failures
