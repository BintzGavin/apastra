# Role Definitions and File Ownership

This document is the authoritative ownership matrix for all apastra agent roles.  
No two roles share writable files. Read-only access is noted explicitly.

---

## CONTRACTS

**Mission**: Define and evolve machine-readable source-of-truth assets — prompt specs, datasets, evaluators, suites, schemas, and validators.

**Owns (Writable)**:
- `promptops/prompts/**`
- `promptops/datasets/**`
- `promptops/evaluators/**`
- `promptops/suites/**`
- `promptops/schemas/**`
- `promptops/validators/**`
- `docs/status/CONTRACTS.md`
- `docs/progress/CONTRACTS.md`
- `.jules/CONTRACTS.md`
- `.sys/plans/YYYY-MM-DD-CONTRACTS-*.md` (planner writes only)
- `.sys/llmdocs/context-contracts.md` (executor writes only)

**Read-Only**:
- `docs/vision.md and README.md`
- `.sys/llmdocs/context-system.md` (may append CONTRACTS milestone/boundary summary only)

**Never Touches**:
- `promptops/runtime/**`, `promptops/resolver/**`, `promptops/manifests/**`
- `promptops/harnesses/**`, `promptops/runs/**`
- `derived-index/**`
- `promptops/policies/**`, `promptops/delivery/**`
- `.github/**`
- Any other domain's status, progress, journal, or context files

---

## RUNTIME

**Mission**: Build and maintain the Git-first prompt resolution chain, consumption manifest handling, and minimal prompt-loading runtime.

**Owns (Writable)**:
- `promptops/runtime/**`
- `promptops/resolver/**`
- `promptops/manifests/**`
- `docs/status/RUNTIME.md`
- `docs/progress/RUNTIME.md`
- `.jules/RUNTIME.md`
- `.sys/plans/YYYY-MM-DD-RUNTIME-*.md` (planner writes only)
- `.sys/llmdocs/context-runtime.md` (executor writes only)

**Read-Only**:
- `docs/vision.md and README.md`
- `promptops/schemas/**` (reads CONTRACTS schemas to validate manifest)
- `.sys/llmdocs/context-system.md` (may append RUNTIME milestone/boundary summary only)

**Never Touches**:
- `promptops/prompts/**`, `promptops/datasets/**`, `promptops/evaluators/**`, `promptops/suites/**`, `promptops/schemas/**`, `promptops/validators/**`
- `promptops/harnesses/**`, `promptops/runs/**`
- `derived-index/**`
- `promptops/policies/**`, `promptops/delivery/**`
- `.github/**`
- Any other domain's status, progress, journal, or context files

---

## EVALUATION

**Mission**: Implement harness execution flow, run-artifact generation, baseline management, and regression comparison.

**Owns (Writable)**:
- `promptops/harnesses/**`
- `promptops/runs/**`
- `derived-index/baselines/**`
- `derived-index/regressions/**`
- `docs/status/EVALUATION.md`
- `docs/progress/EVALUATION.md`
- `.jules/EVALUATION.md`
- `.sys/plans/YYYY-MM-DD-EVALUATION-*.md` (planner writes only)
- `.sys/llmdocs/context-evaluation.md` (executor writes only)

**Read-Only**:
- `docs/vision.md and README.md`
- `promptops/schemas/**` (reads CONTRACTS schemas for run artifact validation)
- `promptops/manifests/**` (reads RUNTIME consumption manifest for test fixtures)
- `.sys/llmdocs/context-system.md` (may append EVALUATION milestone/boundary summary only)

**Never Touches**:
- `promptops/prompts/**`, `promptops/datasets/**`, `promptops/evaluators/**`, `promptops/suites/**`, `promptops/schemas/**`, `promptops/validators/**`
- `promptops/runtime/**`, `promptops/resolver/**`, `promptops/manifests/**`
- `derived-index/promotions/**`
- `promptops/policies/**`, `promptops/delivery/**`
- `.github/**`
- Any other domain's status, progress, journal, or context files

---

## GOVERNANCE

**Mission**: Control merge/promotion gates, release boundaries, delivery contracts, GitHub workflow enforcement, and CODEOWNERS policy.

**Owns (Writable)**:
- `promptops/policies/**`
- `promptops/delivery/**`
- `derived-index/promotions/**`
- `.github/workflows/**`
- `.github/CODEOWNERS`
- `docs/status/GOVERNANCE.md`
- `docs/progress/GOVERNANCE.md`
- `.jules/GOVERNANCE.md`
- `.sys/plans/YYYY-MM-DD-GOVERNANCE-*.md` (planner writes only)
- `.sys/llmdocs/context-governance.md` (executor writes only)

**Read-Only**:
- `docs/vision.md and README.md`
- `derived-index/baselines/**` (reads EVALUATION baselines to wire regression-gate checks)
- `derived-index/regressions/**` (reads EVALUATION regression reports for policy evaluation)
- `.sys/llmdocs/context-system.md` (may append GOVERNANCE milestone/boundary summary only)

**Never Touches**:
- `promptops/prompts/**`, `promptops/datasets/**`, `promptops/evaluators/**`, `promptops/suites/**`, `promptops/schemas/**`, `promptops/validators/**`
- `promptops/runtime/**`, `promptops/resolver/**`, `promptops/manifests/**`
- `promptops/harnesses/**`, `promptops/runs/**`
- `derived-index/baselines/**`, `derived-index/regressions/**` (read-only; created by EVALUATION)
- Any other domain's status, progress, journal, or context files

---

## DOCS

**Mission**: Maintain full, current documentation of the repository — architecture guides, API references, ADRs (Architecture Decision Records), onboarding docs, and cross-domain dashboards. Runs as a **single daily comprehensive sweep** (no planner/executor split).

**Prompt**: `docs.md` (unified)

**Owns (Writable)**:
- `docs/guides/**`
- `docs/api/**`
- `docs/decisions/**`
- `docs/dashboards/**`
- `docs/status/DOCS.md`
- `docs/progress/DOCS.md`
- `.jules/DOCS.md`
- `.sys/llmdocs/context-docs.md`

**Read-Only** (unique cross-domain read privilege):
- `docs/vision.md and README.md`
- `promptops/**` (all domains — for documenting schemas, source files, contracts)
- `derived-index/**` (all domains — for documenting baselines, regressions, promotions)
- `.github/**` (for documenting workflows, CODEOWNERS)
- `.sys/llmdocs/context-*.md` (all domain context files — for cross-domain dashboards)
- `docs/status/*.md` and `docs/progress/*.md` (all domains — for cross-domain dashboards)
- `.sys/llmdocs/context-system.md` (may append DOCS milestone/boundary summary only)

**Never Touches**:
- Any implementation file owned by CONTRACTS, RUNTIME, EVALUATION, or GOVERNANCE (write)
- Other domains' status, progress, journal, or context files (write)

---

## Shared Files — Strict Access Rules

| File | Rule |
|---|---|
| `docs/vision.md and README.md` | **Read-only for all roles.** No role may edit it. Flag vision-vs-README mismatches for human review. |
| `.sys/plans/` | Each role creates/owns files prefixed by its domain (`CONTRACTS-`, `RUNTIME-`, `EVALUATION-`, `GOVERNANCE-`). DOCS does not use the plan system. Never open, modify, or delete another role's plan. |
| `.sys/llmdocs/context-system.md` | Append-only for each role. Each role may update only its own named section. Never overwrite another role's section. |
| `docs/status/` | Each domain has its own file (`CONTRACTS.md`, `RUNTIME.md`, `EVALUATION.md`, `GOVERNANCE.md`, `DOCS.md`). No cross-domain writes. DOCS may **read** all status files for dashboards. |
| `docs/progress/` | Each domain has its own file. No cross-domain writes. DOCS may **read** all progress files for dashboards. |
| `.jules/` journals | Each domain has its own journal file (`CONTRACTS.md`, `RUNTIME.md`, `EVALUATION.md`, `GOVERNANCE.md`, `DOCS.md`). No cross-domain writes. |
