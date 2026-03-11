---
title: "Domain Status Overview"
description: "Current status of all system domains"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-11"
source_files:
  - "docs/status/CONTRACTS.md"
  - "docs/status/RUNTIME.md"
  - "docs/status/EVALUATION.md"
  - "docs/status/GOVERNANCE.md"
---

# Domain Status Overview

This dashboard summarizes the current status across all functional domains in the PromptOps architecture.

## CONTRACTS
- **Version**: 0.9.0
- **Status**: Stable
- **Latest Updates**:
  - Run request and artifact schemas completed
  - Harness adapter schema completed
  - Consumption manifest schema completed
  - Digest convention established

## EVALUATION
- **Version**: 0.1.1
- **Status**: Blocked
- **Blockers**:
  - Waiting for CONTRACTS baseline schema (`baseline.schema.json`)
  - Waiting for GOVERNANCE policy (`promptops/policies/regression.yaml`)
- **Latest Updates**:
  - Harness adapter contract structure verified

## GOVERNANCE
- **Version**: 0.3.0
- **Status**: Blocked
- **Blockers**:
  - Waiting for EVALUATION regression report schema
  - Waiting for CONTRACTS regression policy schema
  - Waiting for CONTRACTS delivery target schema
  - Waiting for CONTRACTS promotion record schema
- **Latest Updates**:
  - Promotion record workflow established
  - CODEOWNERS boundaries defined

## RUNTIME
- **Version**: 0.4.0
- **Status**: Active
- **Latest Updates**:
  - Git ref resolution implemented
  - Workspace path resolution implemented
  - Local override resolution implemented
