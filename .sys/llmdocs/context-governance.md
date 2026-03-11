**Section A: Architecture**
Gate Enforcement Flow:
- Pull requests targeting protected branches trigger a GitHub Actions workflow. The workflow verifies the pass/fail outcome from `reports/regression_report.json` retrieved from the `promptops-artifacts` branch (gracefully skipping if missing).
- Promotions enforce that a matching Approval State record with decision="approved" and checks_passed=true exists on the `promptops-artifacts` branch before generating a promotion record.
- Reusable workflows: `regression-gate.yml` and `immutable-release.yml` can be invoked via `workflow_call` by other repositories.
- Rulesets / Branch Protection: Enforces required status checks (e.g., `gate` check) on pull requests to the `main` branch, and immutability (no updates/deletions) on tags.
- Artifacts Branch Topology: All derived, machine-generated artifacts (run artifacts, regression reports, and promotion records, and approval states) are isolated on the `promptops-artifacts` branch instead of the main branch to reduce repo bloat and avoid merge conflicts.

**Section B: File Tree**
- `.github/workflows/deliver.yml`
- `.github/workflows/promote.yml`
- `.github/workflows/regression-gate.yml`
- `.github/workflows/immutable-release.yml`
- `.github/workflows/record-approval.yml`
- `.github/CODEOWNERS`
- `.github/rulesets/main-protection.json`
- `.github/rulesets/tag-immutability.json`
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
- `promptops/evaluator/` @apastra/evaluation-team
- `promptops/suites/` @apastra/evaluation-team
- `promptops/delivery/` @apastra/governance-admins
- `.github/workflows/` @apastra/infrastructure
- `.github/CODEOWNERS` @apastra/governance-admins
- `.github/rulesets/` @apastra/governance-admins
