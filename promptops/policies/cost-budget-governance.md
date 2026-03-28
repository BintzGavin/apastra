# Cost Budget Governance Policy

## Purpose
To enforce cost control on evaluation suites by setting limits and preventing the promotion of prompts or configurations that exceed defined budget thresholds.

## Scope
This policy applies to all evaluation suites run within the repository that report cost metrics.

## Policy Rules
1. Budget Definition: Evaluation suites SHOULD define a `cost_budget` specifying the maximum allowable cost (in USD) for a full run of the suite.
2. Enforcement Gate: Automated CI checks (e.g., the regression gate) MUST compare the actual run `cost` reported in the `run_manifest.json` or `scorecard.json` against the defined `cost_budget`.
3. Threshold Violations: If a run's actual cost exceeds its `cost_budget`:
   - The run MUST fail the required status check.
   - The associated prompt/configuration MUST NOT be promoted without explicit human override.
4. Escalation Path: Overrides for cost budget failures require explicit approval from the `@apastra/governance-admins` team or designated budget owners, creating an auditable trail.

## Implementation Requirements
- EVALUATION/RUNTIME: Must calculate and report the total cost in run artifacts.
- CONTRACTS: Must support a `cost_budget` field in suite schemas.
- GOVERNANCE: Must enforce the check via GitHub Actions workflows evaluating the artifacts.
