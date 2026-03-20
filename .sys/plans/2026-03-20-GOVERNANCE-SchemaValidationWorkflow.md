#### 1. Context & Goal
- **Objective**: Implement an automated schema validation GitHub Actions workflow for pull requests modifying promptops paths.
- **Trigger**: `docs/vision.md` and `README.md` require automated scanning (schema validation) for moderation and policy enforcement.
- **Impact**: Enforces structural validity against the 23 JSON schemas before merges are allowed.

#### 2. File Inventory
- **Create**: `.github/workflows/schema-validation.yml` (GitHub Actions workflow to trigger schema validators)
- **Modify**: None
- **Read-Only**: `README.md`, `docs/vision.md`, `promptops/validators/` directory schemas

#### 3. Implementation Spec
- **Policy Architecture**: Workflow triggers on pull requests targeting `promptops/prompts/` and `promptops/datasets/`. It invokes the shell scripts inside `promptops/validators/` for changed files.
- **Workflow Design**: Trigger on pull_request paths. Use actions/checkout. For each changed file, check if a corresponding validate-<type>.sh exists, and run it. Fail the job if any validation fails.
- **CODEOWNERS Patterns**: Not applicable
- **Promotion Record Format**: Not applicable
- **Delivery Target Format**: Not applicable
- **Dependencies**: CONTRACTS schemas and validators must be stable.
