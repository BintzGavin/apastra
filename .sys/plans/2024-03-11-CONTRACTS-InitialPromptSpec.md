#### 1. Context & Goal
- **Objective**: Create the first prompt spec instance in the repository under the standard `promptops/prompts/` directory.
- **Trigger**: The README.md requires prompt specs as the source-of-truth prompt definitions, but `promptops/prompts/` is currently empty.
- **Impact**: Unlocks the ability for RUNTIME to resolve prompts and EVALUATION to evaluate them.

#### 2. File Inventory
- **Create**: A new prompt spec YAML file in `promptops/prompts/`
- **Modify**: None
- **Read-Only**: `promptops/schemas/prompt-spec.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: YAML file conforming to `promptops/schemas/prompt-spec.schema.json`. Must contain `id`, `variables` (defining type), `template` (Jinja2 string), `output_contract` (JSON schema), and `metadata`.
- **Content Digest Convention**: Follows `promptops/schemas/digest-convention.md`, meaning the YAML is canonicalized to JSON before hashing if needed.
- **Pseudo-Code**: N/A for data files.
- **Public Contract Changes**: Exports the prompt ID.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures && echo -e "id: 'test'\nvariables:\n  text:\n    type: 'string'\ntemplate: '{{text}}'" > test-fixtures/sample.yaml && yq . test-fixtures/sample.yaml > test-fixtures/sample.json && npx --yes ajv-cli validate -s promptops/schemas/prompt-spec.schema.json -d test-fixtures/sample.json --spec=draft2020 --strict=false -c ajv-formats && rm test-fixtures/sample.yaml test-fixtures/sample.json`
- **Success Criteria**: `ajv-cli` returns validation passed.
- **Edge Cases**: Missing required fields (`id`, `variables`, `template`) will fail validation.
