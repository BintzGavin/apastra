## 0.2.0 - Initial setup
**Learning:** CODEOWNERS review boundaries require specific syntax.
**Action:** Always test CODEOWNERS syntax with GitHub's path matching rules.
## 0.4.0 - Dependency Blockers
**Learning:** Required status checks and Regression policy files are blocked because EVALUATION and CONTRACTS have not produced the necessary dependencies (regression report schema, regression policy schema).
**Action:** Proceed to the next unblocked task (Delivery target specs and sync workflows) until dependencies are resolved.

## 0.4.0 - Dependency Blockers (Continued)
**Learning:** Delivery target sync workflows are blocked because CONTRACTS has not produced the delivery target schema or promotion record schema.
**Action:** Proceed to the next unblocked task until dependencies are resolved.

## 0.8.0 - CI Workflow Refinement
**Learning:** Required status checks fail and block merges if they expect an artifact (like regression_report.json) from an engine that is unimplemented by another domain.
**Action:** Always verify if a dependency's engine is implemented before enforcing a hard failure on missing artifacts; gracefully bypass with a warning if unimplemented.
## 1.3.0 - Delivery Sync Artifact Branch Topology Mismatch
**Learning:** Workflows configured to trigger on `push` events for paths like `derived-index/promotions/` on the main branch completely break when artifacts are relocated to an isolated `promptops-artifacts` branch, because the push event happens on a branch without workflows, and the path has changed to `promotions/`.
**Action:** Use `workflow_call` to chain governance workflows (like triggering `deliver.yml` directly from `promote.yml`) to reliably pass artifact paths across branch boundaries while retaining access to main branch configuration specs.

## 1.4.0 - Delivery Sync Refactored
**Learning:** Outputs mapped from github action jobs need to be specifically defined at the job level in order to be referenced in a dependent job via `needs.<job_name>.outputs.<output_name>`.
**Action:** Add the `outputs:` block mapping to `record-promotion` job before calling `deliver.yml` in `promote.yml`.
