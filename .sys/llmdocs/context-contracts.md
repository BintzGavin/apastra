# Context: CONTRACTS

## Section A: Schema Inventory
- **ID:** `https://promptops.apastra.com/schemas/prompt-spec.schema.json`
  - **Version:** 0.2.0
  - **Description:** Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.

## Section B: Validator Inventory
- **Validator:** `validate-prompt-spec.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-prompt-spec.sh <prompt-spec.json|yaml>`
  - **Validates:** JSON or YAML files against the `prompt-spec.schema.json` schema.

## Section C: Source File Conventions
- **Prompts:**
  - Naming: `prompt.yaml` or `prompt.json`
  - Structure: Lives in `promptops/prompts/<id>/`
  - Required fields: `id` (string), `variables` (object), `template` (string, object, array).

## Section D: Digest Convention
- Computed across the canonicalized JSON of the file.
- Format: `sha256:<hex>`
- The digest is managed by the registry/packager, not held in the prompt spec file itself.

## Section E: Integration Points
- **RUNTIME:** Reads manifests schema.
- **EVALUATION:** Reads run request schema, dataset schema.
- **GOVERNANCE:** Reads policy schema.
