---
title: "Implementation Progress Dashboard"
description: "Implementation timeline and progress across domains"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-11"
source_files:
  - "docs/progress/CONTRACTS.md"
  - "docs/progress/RUNTIME.md"
  - "docs/progress/EVALUATION.md"
  - "docs/progress/GOVERNANCE.md"
---

# Implementation Progress

This dashboard tracks completed and blocked implementation tasks across all active domains.

## Recent Completions

### CONTRACTS
- `v0.9.0`: `run-request.schema.json`, `run-artifact.schema.json`
- `v0.8.0`: `harness-adapter.schema.json`
- `v0.7.0`: `consumption-manifest.schema.json`
- `v0.6.0`: Content digest convention

### RUNTIME
- `v0.4.0`: Git ref resolution in python resolver chain
- `v0.3.0`: Workspace path lookup in resolver chain
- `v0.2.0`: Local override step in resolver chain

### EVALUATION
- `v0.1.1`: Verified schema availability and created domain directories

### GOVERNANCE
- `v0.3.0`: Created automated workflow to append promotion records upon governed releases
- `v0.2.0`: Created `.github/CODEOWNERS` with required review boundaries

## Current Implementation Blockers

| Domain | Blocked On | Dependency |
|---|---|---|
| EVALUATION | `baseline.schema.json` | CONTRACTS |
| EVALUATION | `promptops/policies/regression.yaml` | GOVERNANCE |
| GOVERNANCE | `regression_report.schema.json` | EVALUATION |
| GOVERNANCE | `regression_policy.schema.json` | CONTRACTS |
| GOVERNANCE | `delivery_target.schema.json` | CONTRACTS |
| GOVERNANCE | `promotion_record.schema.json` | CONTRACTS |
