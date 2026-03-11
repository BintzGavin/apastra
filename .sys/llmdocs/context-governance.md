**Section A: Schema Inventory**
- N/A

**Section B: Validator Inventory**
- N/A

**Section C: Source File Conventions**
- `.github/CODEOWNERS`:
  - `promptops/prompts/` @apastra/prompt-engineers
  - `promptops/schemas/` @apastra/governance-admins
  - `promptops/policies/` @apastra/governance-admins
  - `promptops/evaluators/` @apastra/evaluation-team
  - `promptops/suites/` @apastra/evaluation-team
  - `promptops/delivery/` @apastra/governance-admins
  - `derived-index/promotions/` @apastra/governance-admins
  - `.github/workflows/` @apastra/infrastructure
  - `.github/CODEOWNERS` @apastra/governance-admins
- `promptops/policies/regression.yaml`: Rules for metrics: `exact_match` (floor: 0.8, blocker), `latency_ms` (floor: 2000, warning).
- `.github/workflows/regression-gate.yml`: GitHub Actions workflow gating pull requests on regression outcomes.

**Section D: Digest Convention**
- N/A

**Section E: Integration Points**
Promotion Record Format:
- `id`: Unique promotion event ID
- `timestamp`: ISO-8601 timestamp of promotion
- `digest`: The content digest of the promoted prompt package
- `channel`: Target distribution channel (e.g., "prod", "staging")
- `approver`: GitHub actor who approved/triggered the promotion
- `evidence_refs`: Array of URIs linking to regression reports or run artifacts
Immutable Release Workflow:
- Triggers on tag push events (`refs/tags/*`)
- Packages `promptops/` into a `tar.gz` archive.
- Computes SHA256 digest of the archive.
- Creates an immutable GitHub Release using `gh release create`.
Gate Enforcement Flow:
- Pull requests targeting protected branches trigger a GitHub Actions workflow. The workflow verifies the pass/fail outcome from `derived-index/regressions/regression_report.json`.