# apastra Agent Prompts

This folder defines full-length, production-grade role prompts for the apastra PromptOps system.  
The architecture follows a **Black Hole Architecture** planner/executor split with **strict domain ownership** — no two roles ever touch the same files.

---

## Operating Model

### Planning Phase
Planners compare the vision documented in `docs/vision.md` against repository reality.  
They identify the single highest-impact gap and produce one detailed spec file in `/.sys/plans/`.  
**Planners never write implementation code or modify owned domain files.**

### Execution Phase
Executors read the plan written by their planning counterpart and implement it exactly.  
They update status, progress, and context artifacts for their domain only.  
**Executors never plan — they build from approved specs only.**

### Domain Isolation
Every role owns a distinct, non-overlapping set of file paths.  
Ownership is primarily by top-level directory or named subdirectory within `promptops/`.  
No two roles write to the same file. Shared files (e.g., `docs/vision.md`) are **read-only** for all roles.

---

## Domains and Prompt Files

| Domain | Mission | Planner Prompt | Executor Prompt |
|---|---|---|---|
| **CONTRACTS** | Schema, validation, and source-of-truth prompt/dataset/evaluator/suite assets | `planning-contracts.md` | `execution-contracts.md` |
| **RUNTIME** | Git-first resolver, manifest consumption, and prompt loading runtime | `planning-runtime.md` | `execution-runtime.md` |
| **EVALUATION** | Harness execution, run artifacts, baselines, and regression reports | `planning-evaluation.md` | `execution-evaluation.md` |
| **GOVERNANCE** | Policy gates, delivery targets, GitHub workflows, CODEOWNERS, and release/promotion controls | `planning-governance.md` | `execution-governance.md` |
| **DOCS** | Full repository documentation — daily comprehensive sweep of guides, API refs, ADRs, and dashboards | `docs.md` (single prompt) | — |

---

## Ownership Summary (No-Overlap Matrix)

| Top-Level Path | Owner |
|---|---|
| `promptops/prompts/**` | CONTRACTS |
| `promptops/datasets/**` | CONTRACTS |
| `promptops/evaluators/**` | CONTRACTS |
| `promptops/suites/**` | CONTRACTS |
| `promptops/schemas/**` | CONTRACTS |
| `promptops/validators/**` | CONTRACTS |
| `promptops/runtime/**` | RUNTIME |
| `promptops/resolver/**` | RUNTIME |
| `promptops/manifests/**` | RUNTIME |
| `promptops/harnesses/**` | EVALUATION |
| `promptops/runs/**` | EVALUATION |
| `derived-index/baselines/**` | EVALUATION |
| `derived-index/regressions/**` | EVALUATION |
| `promptops/policies/**` | GOVERNANCE |
| `promptops/delivery/**` | GOVERNANCE |
| `derived-index/promotions/**` | GOVERNANCE |
| `.github/workflows/**` | GOVERNANCE |
| `.github/CODEOWNERS` | GOVERNANCE |
| `docs/guides/**` | DOCS |
| `docs/api/**` | DOCS |
| `docs/decisions/**` | DOCS |
| `docs/dashboards/**` | DOCS |
| `docs/status/CONTRACTS.md` | CONTRACTS (planner writes; executor appends) |
| `docs/status/RUNTIME.md` | RUNTIME (planner writes; executor appends) |
| `docs/status/EVALUATION.md` | EVALUATION (planner writes; executor appends) |
| `docs/status/GOVERNANCE.md` | GOVERNANCE (planner writes; executor appends) |
| `docs/status/DOCS.md` | DOCS (planner writes; executor appends) |
| `docs/progress/CONTRACTS.md` | CONTRACTS executor only |
| `docs/progress/RUNTIME.md` | RUNTIME executor only |
| `docs/progress/EVALUATION.md` | EVALUATION executor only |
| `docs/progress/GOVERNANCE.md` | GOVERNANCE executor only |
| `docs/progress/DOCS.md` | DOCS executor only |
| `.sys/plans/YYYY-MM-DD-CONTRACTS-*.md` | CONTRACTS planner only |
| `.sys/plans/YYYY-MM-DD-RUNTIME-*.md` | RUNTIME planner only |
| `.sys/plans/YYYY-MM-DD-EVALUATION-*.md` | EVALUATION planner only |
| `.sys/plans/YYYY-MM-DD-GOVERNANCE-*.md` | GOVERNANCE planner only |
| `.sys/llmdocs/context-contracts.md` | CONTRACTS executor only |
| `.sys/llmdocs/context-runtime.md` | RUNTIME executor only |
| `.sys/llmdocs/context-evaluation.md` | EVALUATION executor only |
| `.sys/llmdocs/context-governance.md` | GOVERNANCE executor only |
| `.sys/llmdocs/context-docs.md` | DOCS executor only |
| `.sys/llmdocs/context-system.md` | All roles (read-only by default; append milestone/boundary summaries only) |
| `.jules/CONTRACTS.md` | CONTRACTS (planner and executor share journal; critical learnings only) |
| `.jules/RUNTIME.md` | RUNTIME journal |
| `.jules/EVALUATION.md` | EVALUATION journal |
| `.jules/GOVERNANCE.md` | GOVERNANCE journal |
| `.jules/DOCS.md` | DOCS journal |
| `docs/vision.md` | **Read-only for all roles** (vision source of truth) |

---

## Shared-File Policy

- **`docs/vision.md`**: read-only for every role. No edits. If a vision gap requires README changes, flag it for human review.
- **`.sys/llmdocs/context-system.md`**: all roles may append their domain's milestone summary or update their own boundary section. Never overwrite another role's section.
- **`.sys/plans/`**: each role creates files prefixed with its domain name. Never open, modify, or delete another role's plan files.
- **`docs/` (cross-domain)**: Each role has its own per-domain status file (`docs/status/DOMAIN.md`) and progress file (`docs/progress/DOMAIN.md`). Never write to another domain's status or progress file.

---

## Full Ownership Reference

See `roles.md` for the exhaustive ownership matrix with read-only constraints.
