---
name: apastra-validate
description: Validate all promptops files against JSON schemas. Catch formatting errors before running evaluations.
---

# Apastra Validate

Validate PromptOps files against the apastra JSON schemas. Uses the shell validators in `promptops/validators/` for deterministic schema checks, plus agent-driven cross-reference checks.

## When to Use

Use this skill when you want to:
- Check that prompt specs, datasets, evaluators, suites, and quick eval files are correctly formatted
- Validate files after scaffolding or manual edits
- Debug why an evaluation run is failing

## Validation Process

### Step 1: Run Schema Validators

Use the shell scripts in `promptops/validators/` to validate each file against its JSON schema. These use `npx ajv-cli` under the hood.

| File Pattern | Validator Script |
|---|---|
| `promptops/prompts/*.yaml` | `bash .agent/scripts/apastra/validators/validate-prompt-spec.sh <file>` |
| `promptops/datasets/*.jsonl` | `bash .agent/scripts/apastra/validators/validate-dataset.sh <file>` |
| `promptops/evaluators/*.yaml` | `bash .agent/scripts/apastra/validators/validate-evaluator.sh <file>` |
| `promptops/suites/*.yaml` | `bash .agent/scripts/apastra/validators/validate-suite.sh <file>` |
| `promptops/evals/*.yaml` | `bash .agent/scripts/apastra/validators/validate-quick-eval.sh <file>` |
| `promptops/policies/*.yaml` | `bash .agent/scripts/apastra/validators/validate-regression-policy.sh <file>` |

Run each validator for every file matching the pattern. Exit code 0 = pass, 1 = fail. Collect all results before reporting.

To validate everything at once:

```bash
for f in promptops/prompts/*.yaml; do bash .agent/scripts/apastra/validators/validate-prompt-spec.sh "$f"; done
for f in promptops/datasets/*.jsonl; do bash .agent/scripts/apastra/validators/validate-dataset.sh "$f"; done
for f in promptops/evaluators/*.yaml; do bash .agent/scripts/apastra/validators/validate-evaluator.sh "$f"; done
for f in promptops/suites/*.yaml; do bash .agent/scripts/apastra/validators/validate-suite.sh "$f"; done
for f in promptops/evals/*.yaml; do bash .agent/scripts/apastra/validators/validate-quick-eval.sh "$f"; done
for f in promptops/policies/*.yaml; do bash .agent/scripts/apastra/validators/validate-regression-policy.sh "$f"; done
```

### Step 2: Compute Digests

After schema validation passes, compute digests for all validated files:

```bash
python .agent/scripts/apastra/runtime/digest.py <file>
```

Report the digest alongside each file so the user can track content changes.

### Step 3: Cross-Reference Checks

These checks require reading file contents — the agent performs them after schema validation:

- Suites reference datasets that exist in `promptops/datasets/`
- Suites reference evaluators that exist in `promptops/evaluators/`
- Dataset `inputs` keys match prompt spec `variables` keys
- Evaluator `metrics` match suite `thresholds` keys (if thresholds are defined)
- Quick eval `{{variable}}` placeholders match case `inputs` keys
- `case_id` values are unique within each dataset

### Step 4: Report

```
Validation Report
=================

Schema Validation (via promptops/validators/):
  ✅ promptops/prompts/summarize.yaml
  ✅ promptops/datasets/summarize-smoke.jsonl — 5 cases
  ❌ promptops/evaluators/broken.yaml
     └── ajv error: must have required property 'metrics'

Cross-References:
  ✅ Suite summarize-smoke → dataset summarize-smoke exists
  ⚠️ Dataset classify-smoke → inputs.category not in prompt spec variables

Digests:
  promptops/prompts/summarize.yaml       sha256:abc123...
  promptops/datasets/summarize-smoke.jsonl sha256:def456...

Summary: 4 passed, 1 error, 1 warning
```

## Tips

- Run validation after scaffolding to catch typos
- Run validation before eval to avoid confusing errors
- Schema validation (Step 1) is authoritative — do not reimplement schema checks yourself
- Cross-reference checks (Step 3) are warnings, not blockers
