---
name: apastra-baseline
description: Establish and manage evaluation baselines for regression detection. A baseline is a known-good scorecard that future runs are compared against.
---

# Apastra Baseline

Establish baselines from evaluation runs. A baseline is a snapshot of a scorecard that represents "known good" — future evaluations compare against it to detect regressions.

## When to Use

Use this skill when you want to:
- Establish the first baseline after running an initial evaluation
- Update the baseline after a prompt improvement has been verified
- Roll back to a prior baseline

## Establishing a Baseline

When asked to establish a baseline (e.g., "set the current results as the baseline for summarize-smoke"):

### Step 1: Locate the Scorecard

Find the most recent run for the target suite in `promptops/runs/`. Look for the latest directory matching `<suite-id>-*` and read its `scorecard.json`.

If no recent run exists, tell the user to run the **eval** skill first.

### Step 2: Create the Baseline File

Write the baseline to `derived-index/baselines/<suite-id>.json`:

```json
{
  "suite_id": "summarize-smoke",
  "established_at": "2026-03-11T12:00:00Z",
  "source_run": "summarize-smoke-2026-03-11-120000",
  "scorecard": {
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
}
```

### Step 3: Confirm

Report what was established:

```
Baseline established ✅

Suite: summarize-smoke
Source run: summarize-smoke-2026-03-11-120000
Metrics:
  keyword_recall: 0.85

Saved to: derived-index/baselines/summarize-smoke.json
```

## Overwriting a Baseline

Baselines follow an **append-friendly** model. When updating a baseline:

1. Rename the existing baseline to `<suite-id>-<timestamp>.json` (e.g., `summarize-smoke-2026-03-10.json`) as an archive
2. Write the new baseline to `derived-index/baselines/<suite-id>.json`
3. Report both the old and new metric values so the change is visible

```
Baseline updated ✅

Suite: summarize-smoke
Previous baseline: keyword_recall=0.80 (archived to summarize-smoke-2026-03-10.json)
New baseline: keyword_recall=0.85

The eval skill will now compare future runs against the new baseline.
```

## Rolling Back a Baseline

If needed, restore a prior baseline by copying an archived baseline file back to `<suite-id>.json`.

## Rules

- **Never delete a baseline** — archive it with a timestamp suffix
- **Only establish baselines from passing runs** — don't baseline a failing scorecard
- **One baseline per suite** — the active baseline is always `<suite-id>.json`
- **Baselines are immutable once set** — updating means archiving the old one and writing a new file
