# apastra Agent Prompts

This folder defines role prompts for a Black Hole Architecture workflow modeled after the Helios planning/execution split.

## Operating Model

- **Planning phase**: planners compare `README.md` vision vs repository reality and write implementation specs in `/.sys/plans/`.
- **Execution phase**: executors implement only the approved plan in their owned files, verify changes, and update status/context artifacts.
- **Domain isolation**: each role owns specific file paths to avoid conflicts.

## Roles and Prompt Files

### Contracts Role
- Planning: `.jules/prompts/planning-contracts.md`
- Execution: `.jules/prompts/execution-contracts.md`
- Focus: schemas, validators, prompt/dataset/evaluator/suite source-of-truth assets.

### Runtime Role
- Planning: `.jules/prompts/planning-runtime.md`
- Execution: `.jules/prompts/execution-runtime.md`
- Focus: resolver, digest-based prompt loading, and minimal consumption runtime.

### Evaluation Role
- Planning: `.jules/prompts/planning-evaluation.md`
- Execution: `.jules/prompts/execution-evaluation.md`
- Focus: harness adapter runner and regression engine artifacts.

### Governance Role
- Planning: `.jules/prompts/planning-governance.md`
- Execution: `.jules/prompts/execution-governance.md`
- Focus: GitHub checks/workflows, CODEOWNERS patterns, release/promotion and delivery controls.

## Ownership Reference

For full ownership boundaries, see `.jules/prompts/roles.md`.
