---
name: apastra
description: PromptOps skills for versioning, evaluating, and shipping AI prompts as disciplined software assets. Agent-as-harness — your IDE agent runs evals, compares baselines, and gates quality.
---

# Apastra PromptOps Skills

Skills for managing AI prompts with the same discipline as code — versioned files, automated evaluations, regression detection, and baseline tracking. Your IDE agent **is** the harness.

## Installation

This is a **collection repository** containing multiple skills. Install individual skills by path:

```bash
# Start here — onboarding and project setup
npx skills add BintzGavin/apastra/skills/getting-started

# Core workflow skills
npx skills add BintzGavin/apastra/skills/eval
npx skills add BintzGavin/apastra/skills/baseline
npx skills add BintzGavin/apastra/skills/scaffold
npx skills add BintzGavin/apastra/skills/validate

# Or install everything at once
npx skills add BintzGavin/apastra --all
```

## Available Skills

### Getting Started
- [skills/getting-started](skills/getting-started) — Project setup, first prompt spec, first evaluation. Start here.

### Workflow Skills
- [skills/eval](skills/eval) — Run evaluations using your IDE agent as the harness. Compare results against baselines.
- [skills/baseline](skills/baseline) — Establish and manage evaluation baselines for regression detection.
- [skills/scaffold](skills/scaffold) — Generate new prompt specs, datasets, evaluators, and suites from templates.
- [skills/validate](skills/validate) — Validate all promptops files against JSON schemas.

## When to Use

Use these skills when:

- Managing AI prompts that need version control and quality gates
- Running evaluations locally without CI or cloud infrastructure
- Detecting prompt regressions before shipping
- Establishing baselines for prompt quality tracking
- Scaffolding new prompt specs, test datasets, or evaluator definitions

## Repository

View all skills and source code at: https://github.com/BintzGavin/apastra

> **🤖 Note for AI Agents**: For the full architectural vision and system design principles behind Apastra, read `docs/vision.md` in the repository.
