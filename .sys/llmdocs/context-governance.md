**Section A: Architecture**
Gate Enforcement Flow:
- Pull requests targeting protected branches trigger a GitHub Actions workflow. The workflow verifies the pass/fail outcome from `reports/regression_report.json` retrieved from the `promptops-artifacts` branch (fails if missing). It extracts metrics from the regression report to add PR annotations and step summaries. The check is gracefully skipped for PRs that do not modify evaluable assets (prompts, harnesses, datasets, policies).
- Promotions enforce that a matching Approval State record with decision="approved" and checks_passed=true exists on the `promptops-artifacts` branch before generating a promotion record. A successful promotion record triggers a delivery target sync via `deliver.yml`.
- Reusable workflows: `regression-gate.yml`, `immutable-release.yml` (generates provenance attestations for release assets), and `deliver.yml` can be invoked via `workflow_call`.
- Rulesets / Branch Protection: Enforces required status checks (e.g., `gate` check) on pull requests to the `main` branch, and immutability (no updates/deletions) on tags. Automated secret scanning runs on PRs modifying prompts or datasets to fail if secret keywords are found.
- Artifacts Branch Topology: All derived, machine-generated artifacts (run artifacts, regression reports, and promotion records, and approval states) are isolated on the `promptops-artifacts` branch instead of the main branch to reduce repo bloat and avoid merge conflicts.

**Section B: File Tree**
- `.github/CODEOWNERS`
- `.github/workflows/prompt-eval.yml`
- `.github/workflows/prompt-release.yml`
- `.github/rulesets/main-protection.json`
- `.github/rulesets/tag-immutability.json`
- `.github/workflows/auto-merge.yml`
- `.github/workflows/deliver.yml`
- `.github/workflows/immutable-release.yml`
- `.github/workflows/promote.yml`
- `.github/workflows/record-approval.yml`
- `.github/workflows/regression-gate.yml`
- `.github/workflows/moderation-scan.yml`
- `.github/workflows/secret-scan.yml`
- `.github/workflows/community-reporting.yml`
- `.github/ISSUE_TEMPLATE/moderation_report.yml`
- `promptops/delivery/prod-target.yaml`
- `promptops/policies/regression.yaml`
- `promptops/policies/acceptable-use.md`
- `promptops/policies/deprecation.md`
- `promptops/policies/ownership-disputes.md`
- `promptops/policies/naming.md`
- `promptops/policies/trusted-publisher.md`
- `promptops/policies/federation.md`
- `promptops/policies/mirroring.md`

**Section C: Policy Inventory**
- `promptops/policies/acceptable-use.md`: Acceptable use constraints.
- `promptops/policies/deprecation.md`: Deprecation guidelines.
- `promptops/policies/ownership-disputes.md`: Ownership and takedown appeal process.
- `promptops/policies/naming.md`: Naming rules for prompts, packages, and metrics.
- `promptops/policies/trusted-publisher.md`: Trusted publisher requirements based on build provenance.
- `promptops/policies/takedowns.md`: Takedown procedure for content removal.
- `promptops/policies/appeals.md`: Moderation decision appeals process.
- `promptops/policies/federation.md`: Governance rules for cross-custodian trust and namespace resolution.
- `promptops/policies/mirroring.md`: Requirements and processes for establishing read-only mirrors.
- `promptops/policies/regression.yaml`: Rules for metrics: `exact_match` (floor: 0.8, blocker), `latency_ms` (floor: 2000, warning).

**Section D: Promotion Record Format**
- `id`: Unique promotion event ID
- `timestamp`: ISO-8601 timestamp of promotion
- `channel`: Target distribution channel (e.g., "prod", "staging")
- `prompt_id`: ID of the prompt being promoted
- `approved_digest`: The content digest of the promoted prompt package
- `regression_report_id`: The ID of the regression report justifying the promotion
- `approver`: GitHub actor who approved/triggered the promotion
- `evidence_links`: Array of URIs linking to regression reports or run artifacts

**Section E: Delivery Target Inventory**
- `promptops/delivery/prod-target.yaml`: Target type `github_pr`, channel `prod`
- `promptops/delivery/oci-target.yaml`: Target type `oci`
- `promptops/delivery/npm-target.yaml`: Target type `npm`
- `promptops/delivery/pypi-target.yaml`: Target type `pypi`

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
- `promptops/datasets/` @apastra/contracts-team
- `promptops/evals/` @apastra/contracts-team
- `promptops/validators/` @apastra/contracts-team
- `promptops/harnesses/` @apastra/evaluation-team
- `promptops/runs/` @apastra/evaluation-team
- `derived-index/baselines/` @apastra/evaluation-team
- `derived-index/regressions/` @apastra/evaluation-team
- `promptops/manifests/` @apastra/runtime-team
- `promptops/resolver/` @apastra/runtime-team
- `promptops/runtime/` @apastra/runtime-team