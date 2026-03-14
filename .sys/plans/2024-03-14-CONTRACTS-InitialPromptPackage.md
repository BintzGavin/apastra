#### 1. Context & Goal
- **Objective**: Create an initial `prompt-package` instance file in the `promptops/prompts/` directory to serve as a concrete example of a prompt package bundle.
- **Trigger**: The Vision Document (`docs/vision.md`) defines a "Prompt package" as an "Immutable bundle of prompt specs with a manifest and content digest". While the `prompt-package.schema.json` and its validator exist (`docs/status/CONTRACTS.md` v0.13.0), there is no actual instance of a prompt package in the repository.
- **Impact**: Provides a concrete, testable instance of a prompt package for other domains (like RUNTIME for materialization/resolution, or GOVERNANCE for distribution wrappers like `provider-artifact`) to consume.

#### 2. File Inventory
- **Create**:
  - `promptops/prompts/my-prompt-package/package.yaml`: The concrete instance of the prompt package.
- **Modify**: None
- **Read-Only**:
  - `promptops/schemas/prompt-package.schema.json`
  - `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**: The prompt package file will be named `package.yaml` (or JSON equivalent) and strictly conform to `promptops/schemas/prompt-package.schema.json`.
- **Required Fields**:
  - `id`: Stable identifier (e.g., `my-first-package`).
  - `digest`: A SHA-256 digest string (`^sha256:[a-f0-9]{64}$`).
  - `specs`: An array of included prompt spec IDs/digests (e.g., `["my-prompt"]`).
- **Optional Fields**:
  - `version`: A semantic version (e.g., `1.0.0`).
  - `metadata`: A metadata object (e.g., `{"author": "Contracts Team"}`).
- **Dependencies**: The `prompt-package.schema.json` and `validate-prompt-package.sh` scripts are already completed. No dependencies on other domains.

#### 4. Test Plan
- **Verification**: Run `bash promptops/validators/validate-prompt-package.sh promptops/prompts/my-prompt-package/package.yaml`.
- **Success Criteria**: The script exits successfully (exit code 0), indicating the prompt package instance is valid against the schema.
- **Edge Cases**: Malformed inputs such as invalid digest string pattern, missing `specs` field, or missing `id` field should be correctly rejected.