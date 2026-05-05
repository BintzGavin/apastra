# PromptOps in this repo (Apastra)

This directory holds **prompt specifications**, **evaluation datasets**, **scorers**, **suites**, and **policies** for the [Apastra](https://github.com/BintzGavin/apastra) workflow. Your IDE agent is usually the **harness** that calls models and executes judge-style evaluators; deterministic plumbing lives under `.agent/scripts/apastra/`.

Replace every `TODO_*` marker below with repo-specific truth as you adopt Apastra.

## Quick map

| Path | Purpose |
| --- | --- |
| `promptops/prompts/` | Versioned prompt specs (`id`, variables, template, optional `output_contract`). |
| `promptops/datasets/` | `.jsonl` case files (`case_id`, `inputs`, optional `expected_outputs` / `assert`). |
| `promptops/evaluators/` | Scoring definitions (deterministic, schema, judge). |
| `promptops/suites/` | Which datasets + evaluators + thresholds compose a runnable suite. |
| `promptops/evals/` | Optional **quick eval** single-file YAML workflows. |
| `promptops/schemas/` | JSON schemas (often mirrored from `.agent/scripts/apastra/` after install). |
| `promptops/policies/` | Regression tolerance policies once baselines exist. |
| `promptops/runs/` | Ephemeral artifacts from eval runs (**default gitignore target** — keep noise out of git). |
| `derived-index/baselines/` | Stored scorecards for regression comparison (**normally committed** once you baseline). |
| `derived-index/regressions/` | Regression reports emitted by tooling (policy-dependent; clarify what your team commits). |

## Naming & IDs

| Concept | Guidance |
| --- | --- |
| Prompt `id` | Treat IDs as immutable contracts. Prefer **derived slugs from `source_relpath`** + collision suffixes. Mint **new IDs** rather than repurposing old ones. |
| Case `case_id` | Stable slug per behavioral scenario (`happy`, `ambiguous-input`, …). |
| `source_relpath` | When cases map to originating instruction files, keep the relative path explicit for traceability. |
| Suites | Name after behavior + breadth (`skills-smoke`, `rules-heavy`, …). |

Maintain a lightweight **mapping table** (here or beside suites) tying **source files ↔ prompt IDs ↔ suites**:

| Suite | Sources covered | Prompt spec IDs | Dataset files |
| --- | --- | --- | --- |
| `TODO_SUITE` | `TODO_PATH_GLOB` | `TODO_IDS` | `TODO_DATASETS.jsonl` |

## How to run workflows

Ask your IDE agent explicitly (examples):

- **Validate PromptOps YAML/JSONL:** “Use **`apastra-validate`** to validate everything under `promptops/`.”  
- **Run a suite:** “Use **`apastra-eval`** against suite `YOUR_SUITE_ID`.”  
- **Quick eval shortcut:** Point the agent at `promptops/evals/<file>.yaml` if you standardized on quick-mode for prototyping.  
- **Baseline regression:** Only after deliberate choice — “Use **`apastra-baseline`** …”  

Always mention which **model**/temperature assumptions apply so future readers know why flaky judge scores shifted.

Concrete command stubs (adapt to whichever shell automation you standardized):

```bash
# Typical validation entry (exact flags depend on your installed validator scripts)
# python .agent/scripts/apastra/validators/validate-all.sh promptops/

# Typical digest fingerprints (helps manifests / audits)
# python .agent/scripts/apastra/runtime/digest.py promptops/prompts/YOUR_PROMPT.yaml
```

## Harness metadata

Runs should record **`harness`** in manifests (`claude-code`, `cursor`, `copilot`, `antigravity`, `api`, `github-actions`, …) because identical models behave differently across clients.

## Assert & scoring philosophy

Follow the **deterministic-first maturity ladder**:

1. Start with deterministic checks (`contains`, `is-json`, `regex`, …).  
2. Introduce **`llm-rubric` / `similar`** when nuance demands it — **version judge prompts** aggressively.  
3. Once stable, freeze **baselines** and compare future scorecards (`apastra-baseline` + regression policies).

Never fork assertion evaluation logic manually — defer to **`python .agent/scripts/apastra/runs/evaluate_assertions.py`** as documented in **`apastra-eval`**.

Canonical public reference: [`https://bintzgavin-apastra-14.mintlify.app/guides/writing-evals`](https://bintzgavin-apastra-14.mintlify.app/guides/writing-evals)

## What belongs in Git?

| Artifact | Typical stance | Reason |
| --- | --- | --- |
| `promptops/` specs (prompts, datasets, evaluators, suites, policies) | **Commit** | Source of truth; reviewable PR diffs |
| `promptops/runs/` | **Ignore** locally | Huge / noisy timestamps |
| `derived-index/baselines/` | **Commit once baselined** | CI / regression anchors |
| Scratch experiments | **`*.local.*` conventions or tmp dirs** — ignore | Avoid polluting teammate workflows |

Tune `.gitignore` deliberately when you oscillate between “sandbox play” versus “regulated CI.” Discuss with your coding agent:

> “Recommend `.gitignore` rules for PromptOps noisy outputs; patch only after I approve.”

## CI upgrade path (optional)

When local evals stabilize, automate PR gating via GitHub Actions using the **`apastra-setup-ci`** skill’s workflow templates (`regression-gate.yml`, companions). Only adopt once:

- Thresholds encode real quality expectations (**not placeholders**).
- Baselines represent an actually acceptable product state.

## FAQ / Troubleshooting (`TODO_TEAM`)

### Flaky numeric judge scores?

- Narrow rubrics, shorten outputs, tighten temperature ceilings, diversify deterministic checks.

### Huge repo with dozens of SKILL files?

- Use **family harness prompts** parameterized by path + excerpts; datasets carry `source_relpath`.

### PEP 668 blocking Python installs?

- Follow **`setup`/post-install** guidance emitted by Apastra installers—don’t improvisationally mix system Python tooling.

---

**Maintainers:** regenerate this handbook after major scaffolding events; drift here causes silent confusion for collaborators.
