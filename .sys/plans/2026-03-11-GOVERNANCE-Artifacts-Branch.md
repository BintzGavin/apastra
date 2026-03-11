#### 1. Context & Goal
- **Objective**: Design the "artifacts branch" pattern to store derived artifacts without causing merge conflicts on the source-of-truth branch.
- **Trigger**: The `README.md` defines an "Artifacts branch (append-only indices)" to isolate derived data (`runs/`, `reports/`, `promotions/`) while remaining Git-native.
- **Impact**: Reduces repo bloat and merge conflicts by ensuring large, machine-generated artifacts are kept on an isolated branch (`promptops-artifacts`), preserving the cleanliness of `main`.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-11-GOVERNANCE-Artifacts-Branch.md` (Spec for artifacts branch routing logic).
- **Modify**: None.
- **Read-Only**: `README.md` (Artifacts branch topology section).

#### 3. Implementation Spec
- **Policy Architecture**: GitHub Actions workflows generating derived artifacts (run artifacts, regression reports, promotion records) will checkout the `promptops-artifacts` branch instead of the default branch to append records.
- **Workflow Design**:
  1. A worker runner finishes evaluation or a promotion approval occurs.
  2. The workflow step checkouts `promptops-artifacts` branch using `actions/checkout@v4`.
  3. The runner writes the new artifact file (e.g., `artifacts/runs/YYYY/MM/DD/<run_id>/scorecard.json`).
  4. The job commits and pushes the file directly to the `promptops-artifacts` branch.
- **CODEOWNERS Patterns**: None. (Artifacts branch is purely automated append, review boundaries apply on source-of-truth).
- **Promotion Record Format**: No change, just routed to a new destination branch path `artifacts/promotions/...`.
- **Delivery Target Format**: None.
- **Dependencies**: EVALUATION regression report formats and RUNTIME schemas must be stable to ensure the output data being pushed to the artifacts branch is valid.

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures/artifacts/runs/2026/03/11/123 && git init test-fixtures && cd test-fixtures && git checkout -b promptops-artifacts && echo '{"status":"pass"}' > artifacts/runs/2026/03/11/123/scorecard.json && git add . && git commit -m "Add artifact" && cd ..`
- **Success Criteria**: `[ -f test-fixtures/artifacts/runs/2026/03/11/123/scorecard.json ] && echo "Artifact added to artifacts branch"`
- **Edge Cases**: `mkdir -p test-fixtures-edge && cd test-fixtures-edge && git init && git checkout -b main && (git checkout promptops-artifacts 2>/dev/null || git checkout --orphan promptops-artifacts) && git commit --allow-empty -m "Init artifacts branch" && [ "$(git rev-parse --abbrev-ref HEAD)" = "promptops-artifacts" ] && echo "Successfully checked out orphan branch" && cd .. && rm -f test-fixtures/artifacts/runs/2026/03/11/123/scorecard.json && rmdir test-fixtures/artifacts/runs/2026/03/11/123 && rmdir test-fixtures/artifacts/runs/2026/03/11 && rmdir test-fixtures/artifacts/runs/2026/03 && rmdir test-fixtures/artifacts/runs/2026 && rmdir test-fixtures/artifacts/runs && rmdir test-fixtures/artifacts && rm -f test-fixtures/.git/COMMIT_EDITMSG && rm -f test-fixtures/.git/HEAD && rm -f test-fixtures/.git/config && rm -f test-fixtures/.git/description && rm -f test-fixtures/.git/index && rmdir test-fixtures/.git/branches && rmdir test-fixtures/.git/hooks && rmdir test-fixtures/.git/info && rm -f test-fixtures/.git/logs/HEAD && rmdir test-fixtures/.git/logs/refs/heads && rmdir test-fixtures/.git/logs/refs && rmdir test-fixtures/.git/logs && rm -f test-fixtures/.git/objects/pack/* && rmdir test-fixtures/.git/objects/pack && rmdir test-fixtures/.git/objects/info && rmdir test-fixtures/.git/objects && rmdir test-fixtures/.git/refs/heads && rmdir test-fixtures/.git/refs/tags && rmdir test-fixtures/.git/refs && rmdir test-fixtures/.git && rmdir test-fixtures && rmdir test-fixtures-edge/.git/branches && rmdir test-fixtures-edge/.git/hooks && rmdir test-fixtures-edge/.git/info && rmdir test-fixtures-edge/.git/logs/refs/heads && rmdir test-fixtures-edge/.git/logs/refs && rmdir test-fixtures-edge/.git/logs && rmdir test-fixtures-edge/.git/objects/pack && rmdir test-fixtures-edge/.git/objects/info && rmdir test-fixtures-edge/.git/objects && rmdir test-fixtures-edge/.git/refs/heads && rmdir test-fixtures-edge/.git/refs/tags && rmdir test-fixtures-edge/.git/refs && rm -f test-fixtures-edge/.git/COMMIT_EDITMSG && rm -f test-fixtures-edge/.git/HEAD && rm -f test-fixtures-edge/.git/config && rm -f test-fixtures-edge/.git/description && rmdir test-fixtures-edge/.git && rmdir test-fixtures-edge`
