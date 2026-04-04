# GOVERNANCE Context

## Section A: Architecture
- The core governance loop requires all releases to satisfy a series of validation gates.
- A PR containing evaluation reports must be reviewed according to the established CODEOWNERS thresholds based on risk categories before being securely promoted to downstream targets using append-only promotion records.

## Section B: File Tree
```
promptops/policies/
├── capability-tagging.md
└── holdout-sets.md
promptops/delivery/
derived-index/promotions/
.github/
├── workflows/
└── CODEOWNERS
```

## Section C: Policy Inventory
- **capability-tagging.md**: Maps execution tier capabilities to required reviews and bypass constraints.
  - Metrics: risk, execution, domain
  - Thresholds: Varies by specific tag combination
- **holdout-sets.md**: Establishes requirements for holdout datasets during validation.
  - Metrics: holdout_pass
  - Thresholds: true (must pass against holdout set)

## Section D: Promotion Record Format
- id: string
- timestamp: datetime
- channel: string
- prompt_id: string
- approved_digest: string
- regression_report_id: string
- approver: string
- evidence_links: array

## Section E: Delivery Target Inventory
- N/A

## Section F: CODEOWNERS Summary
- `promptops/policies/capability-tagging.md` -> `@promptops-governance`
- `promptops/policies/holdout-sets.md` -> `@promptops-governance`
