---
name: apastra-baseline
description: Establish an immutable named baseline from a complete passing evaluation run and an explicitly approved adapter.
---

# Apastra baseline

Locate the intended run directory and the adapter that produced it. Confirm the
suite and model set with the user when several runs fit their request. A scorecard
alone is insufficient.

Run the admission command before accepting evidence:

```bash
.agent/bin/apastra gate promptops/runs/candidate --adapter promptops/harnesses/local.yaml
.agent/bin/apastra baseline smoke accepted-001 promptops/runs/candidate --adapter promptops/harnesses/local.yaml
```

The baseline command revalidates the retained evidence. It creates
`derived-index/baselines/smoke-accepted-001.json` using exclusive creation and
records the resolved run path and its digest.

Report the path produced by the command and its measured metrics. Preserve
existing baseline names. Accept a later run under a new name, then explicitly
select its run directory when comparing:

```bash
.agent/bin/apastra gate promptops/runs/candidate --baseline promptops/runs/accepted --policy promptops/policies/regression.yaml --adapter promptops/harnesses/local.yaml
```

A failed run, unverified producer, or unresolved digest cannot establish a
baseline. A missing baseline requires an explicit bootstrap choice. Retain
historical scorecard-only records without promoting them to current evidence.

For model comparison, use the measured comparison command:

```bash
.agent/bin/apastra compare smoke --adapter promptops/harnesses/local.yaml --models model-a model-b
```

The [evaluation contract](../docs/guides/evaluation-trust.md) describes the required
files and supported policy semantics.
