# Role Definitions and File Ownership

Use these boundaries for all planning/execution prompts in this repository.

## CONTRACTS
- **Mission**: Define and evolve machine-readable source-of-truth assets and their validation rules.
- **Owns**:
  - `promptops/prompts/**`
  - `promptops/datasets/**`
  - `promptops/evaluators/**`
  - `promptops/suites/**`
  - `promptops/schemas/**`
  - `promptops/validators/**`

## RUNTIME
- **Mission**: Build Git-first resolution and minimal prompt consumption runtime.
- **Owns**:
  - `promptops/runtime/**`
  - `promptops/resolver/**`
  - `promptops/manifests/consumption.yaml`
  - `promptops/manifests/**` (except immutable run requests/artifacts)

## EVALUATION
- **Mission**: Implement harness execution flow and regression comparison.
- **Owns**:
  - `promptops/harnesses/**`
  - `promptops/runs/**`
  - `derived-index/baselines/**`
  - `derived-index/regressions/**`

## GOVERNANCE
- **Mission**: Control merge/promotion gates, release boundaries, and delivery contracts.
- **Owns**:
  - `promptops/policies/**`
  - `promptops/delivery/**`
  - `derived-index/promotions/**`
  - `.github/workflows/**`
  - `.github/CODEOWNERS` and related review-policy files

## Shared Files
- `README.md` is vision source and read-only by default for all roles.
- Cross-domain changes require explicit dependency notes in plan files.
