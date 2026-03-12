#### 1. Context & Goal
- **Objective**: Create the first evaluator instance file (`exact-match.yaml`) in `promptops/evaluators/`.
- **Trigger**: The schema for `promptops/schemas/evaluator.schema.json` defines scoring (deterministic checks, schema validation, rubric/judge config), and while the schema exists, no implementation instance currently exists for testing or benchmark suites.
- **Impact**: Unlocks the creation of the first Benchmark Suite instance, which depends on datasets and evaluators.

#### 2. File Inventory
- **Create**: `promptops/evaluators/exact-match.yaml`
- **Modify**: None
- **Read-Only**: `promptops/schemas/evaluator.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: The file must be a YAML file conforming to `https://promptops.apastra.com/schemas/evaluator.schema.json`. Required fields are `id` (`exact-match-v1`), `type` (`deterministic`), and `metrics` (`["exact_match_score"]`). Optional fields include `description`.
- **Content Digest Convention**: The digest will be computed via `compute-digest.sh` (using `yq` to JSON then `jq` canonicalization).
- **Pseudo-Code**:
  ```yaml
  id: exact-match-v1
  type: deterministic
  metrics:
    - exact_match_score
  description: Checks for an exact string match between candidate and expected output.
  ```
- **Public Contract Changes**: Exports evaluator ID `exact-match-v1`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures && cp promptops/evaluators/exact-match.yaml test-fixtures/ && bash promptops/validators/validate-evaluator.sh test-fixtures/exact-match.yaml`
- **Success Criteria**: The script outputs "Validation successful!" and exits with code 0.
- **Edge Cases**: Missing `id`, `type`, or `metrics` should fail validation.
