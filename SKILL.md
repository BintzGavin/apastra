---
name: apastra
description: PromptOps skills for versioning, evaluating, tracing, and shipping AI prompts as disciplined software assets. Agent-as-harness — your IDE agent runs evals, compares baselines, surfaces trace evidence, and gates quality.
---

# Apastra PromptOps Skills

Skills for managing AI prompts with the same discipline as code — versioned files, automated evaluations, trace evidence, regression detection, and baseline tracking. Your IDE agent **is** the harness.

## Installation

### Option 1 — Git clone (language-agnostic)

```bash
git clone --single-branch --depth 1 https://github.com/BintzGavin/apastra.git .agent/skills/apastra
.agent/skills/apastra/setup --dry-run
.agent/skills/apastra/setup
```

### Option 2 — npm

```bash
APASTRA_POSTINSTALL_SETUP=1 npm install apastra
```

Plain `npm install apastra` is disclosure-only: it installs the package and prints what setup would create, but does not mutate the consumer repo. Use `APASTRA_POSTINSTALL_SETUP=1` for npm-managed project setup.

Setup creates or updates `.agent/skills/apastra/`, `.agent/scripts/apastra/`, and discovery symlinks under `.claude/skills/` and `.agents/skills/` unless `APASTRA_NO_SKILL_SYMLINKS=1`.

Opt-in actions:

- `APASTRA_INSTALL_AGENT_HOOKS=1` writes project-local Codex/Claude Code hook config.
- `APASTRA_INSTALL_PY_DEPS=1` allows setup/postinstall to invoke `pip` for `pyyaml` and `jsonschema`; otherwise Apastra only checks and prints manual guidance.
- `APASTRA_ASSUME_YES=1` lets the git-clone setup proceed non-interactively after printing the preflight manifest.

## Available Skills

### Getting Started

- [getting-started](getting-started) — Project setup, first prompt spec, first evaluation. Start here.
- [getting-started/onboarding.md](getting-started/onboarding.md) — Copy/paste onboarding playbook for adopting Apastra in **other repositories**.

### Workflow Skills

- [writing-evals](writing-evals) — Design evals interactively (paired workflow; link-sharing discipline to the Writing evals article).
- [eval](eval) — Run evaluations using your IDE agent as the harness. Compare results against baselines.
- [trace](trace) — Inspect agent traces and convert tool-call evidence into eval cases or artifact refs.
- [baseline](baseline) — Establish and manage evaluation baselines for regression detection.
- [scaffold](scaffold) — Generate new prompt specs, datasets, evaluators, and suites from templates.
- [validate](validate) — Validate all promptops files against JSON schemas.
- [red-team](red-team) — Generate adversarial test cases for robustness testing.
- [setup-ci](setup-ci) — Upgrade from local-first evaluation to automated GitHub Actions CI.

## When to Use

Use these skills when:

- Managing AI prompts that need version control and quality gates
- **Designing evals** interactively before generating suites (use `apastra-writing-evals`)
- Running evaluations locally without CI or cloud infrastructure
- Debugging agent behavior from traces, hook feedback, or saved tool-call logs
- Detecting prompt regressions before shipping
- Establishing baselines for prompt quality tracking
- Scaffolding new prompt specs, test datasets, or evaluator definitions

## Repository

View all skills and source code at: https://github.com/BintzGavin/apastra

---

> **🤖 OVERARCHING CONTEXT FOR AI AGENTS**
> 
> You are operating within **Apastra**, a state-of-the-art PromptOps architecture.
> 
> **The Core Philosophy:**
> Prompts must be treated like disciplined software assets. Apastra is a **file-based protocol**. There is no hidden database, no mandatory SaaS platform, and no forced framework. 
> - **Durable state lives in Git**: Prompts, test datasets, evaluator scoring rules, benchmark suites, baselines, and regression policies are all defined as flat files (YAML/JSON).
> - **The Agent is the Harness**: You (the external IDE agent) perform the computation. You read the suites, run the test cases, apply the scoring rules, and compare the results to the baselines.
> - **Trace Evidence Matters**: Hooks expose useful evidence about prompts, tool calls, validation failures, and stopping conditions. Use that evidence to debug agent behavior and create regression cases, but do not persist raw secrets or full private transcripts by default.
> - **Append-only Artifacts**: When you run evaluations, you generate run manifests, scorecards, and evidence records. You never overwrite a baseline; you archive and append.
> 
> **Local-First vs. CI Upgrades:**
> Developers using this project prefer a zero-infrastructure **local-first** approach. They evaluate prompts locally using you as their test runner. However, if they need enterprise-grade governance, they can upgrade to automated pull request gating using the `apastra-setup-ci` skill. The file formats remain exactly the same.
> 
> As an external agent using these skills, your job is to enforce this discipline. Never mutate a file ad-hoc if there is a structured prompt spec for it. If you need to **design or refine what an eval measures**, follow **`apastra-writing-evals`**. If you are told to **run** an evaluation, follow the **`apastra-eval`** skill exactly.
