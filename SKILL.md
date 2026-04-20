---
name: apastra
description: PromptOps skills for versioning, evaluating, and shipping AI prompts as disciplined software assets. Agent-as-harness — your IDE agent runs evals, compares baselines, and gates quality.
---

# Apastra PromptOps Skills

Skills for managing AI prompts with the same discipline as code — versioned files, automated evaluations, regression detection, and baseline tracking. Your IDE agent **is** the harness.

## Installation

### Option 1 — Git clone (language-agnostic)

```bash
git clone --single-branch --depth 1 https://github.com/BintzGavin/apastra.git .agent/skills/apastra
.agent/skills/apastra/setup
```

### Option 2 — npm

```bash
npm install apastra
```

Both methods install the skills to `.agent/skills/apastra/` and the runtime scripts to `.agent/scripts/apastra/`.

## Available Skills

### Getting Started
- [getting-started](getting-started) — Project setup, first prompt spec, first evaluation. Start here.

### Workflow Skills
- [eval](eval) — Run evaluations using your IDE agent as the harness. Compare results against baselines.
- [baseline](baseline) — Establish and manage evaluation baselines for regression detection.
- [scaffold](scaffold) — Generate new prompt specs, datasets, evaluators, and suites from templates.
- [validate](validate) — Validate all promptops files against JSON schemas.
- [red-team](red-team) — Generate adversarial test cases for robustness testing.
- [setup-ci](setup-ci) — Upgrade from local-first evaluation to automated GitHub Actions CI.

## When to Use

Use these skills when:

- Managing AI prompts that need version control and quality gates
- Running evaluations locally without CI or cloud infrastructure
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
> - **Append-only Artifacts**: When you run evaluations, you generate run manifests, scorecards, and evidence records. You never overwrite a baseline; you archive and append.
> 
> **Local-First vs. CI Upgrades:**
> Developers using this project prefer a zero-infrastructure **local-first** approach. They evaluate prompts locally using you as their test runner. However, if they need enterprise-grade governance, they can upgrade to automated pull request gating using the `apastra-setup-ci` skill. The file formats remain exactly the same.
> 
> As an external agent using these skills, your job is to enforce this discipline. Never mutate a file ad-hoc if there is a structured prompt spec for it. If you are told to "evaluate a prompt", follow the exact file-based pipeline defined in the `apastra-eval` skill.
