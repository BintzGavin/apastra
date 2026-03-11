**Section A: Architecture**
Gate Enforcement Flow:
- Pull requests targeting protected branches trigger a GitHub Actions workflow. The workflow verifies the pass/fail outcome from `derived-index/regressions/regression_report.json`.

**Section B: File Tree**
- `.github/workflows/deliver.yml`
- `.github/workflows/promote.yml`
- `.github/workflows/regression-gate.yml`
- `.github/workflows/immutable-release.yml`
- `.github/CODEOWNERS`
- `promptops/policies/regression.yaml`
- `promptops/delivery/prod-target.yaml`

**Section C: Policy Inventory**
- `promptops/policies/regression.yaml`: Rules for metrics: `exact_match` (floor: 0.8, blocker), `latency_ms` (floor: 2000, warning).

**Section D: Promotion Record Format**
- `id`: Unique promotion event ID
- `timestamp`: ISO-8601 timestamp of promotion
- `digest`: The content digest of the promoted prompt package
- `channel`: Target distribution channel (e.g., "prod", "staging")
- `approver`: GitHub actor who approved/triggered the promotion
- `evidence_refs`: Array of URIs linking to regression reports or run artifacts

**Section E: Delivery Target Inventory**
- `promptops/delivery/prod-target.yaml`: Target type `github_pr`, channel `prod`

**Section F: CODEOWNERS Summary**
- `promptops/prompts/` @apastra/prompt-engineers
- `promptops/schemas/` @apastra/governance-admins
- `promptops/policies/` @apastra/governance-admins
- `promptops/evaluators/` @apastra/evaluation-team
- `promptops/suites/` @apastra/evaluation-team
- `promptops/delivery/` @apastra/governance-admins
- `derived-index/promotions/` @apastra/governance-admins
- `.github/workflows/` @apastra/infrastructure
- `.github/CODEOWNERS` @apastra/governance-admins
