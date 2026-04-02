# Capability Tagging Policy

## 1. Schema Alignment
This policy governs the use of the `tags` array defined in `suite.schema.json`. Every tag applied to a suite maps directly to specific governance, review, and promotion requirements.

## 2. Standard Tag Definitions & Routing
The following standard tags determine review routing:

- **`pii` / `phi` / `pci`**:
  - **Requirement**: Mandatory review by `@promptops-security` and `@promptops-legal`.
  - **Promotion**: Automated promotion to public channels is prohibited; requires manual human approval checkpoint.
- **`financial-advice` / `medical-advice`**:
  - **Requirement**: Mandatory review by specialized domain experts (e.g., `@promptops-medical-reviewers`).
- **`experimental`**:
  - **Requirement**: Bypasses strict threshold regression gates for non-production environments.
  - **Promotion**: Cannot be promoted to `release` or `oci` channels.
- **`code-generation` / `exec`**:
  - **Requirement**: Requires elevated security sandbox checks.

## 3. Unknown or Missing Tags
- If a suite contains **empty** or **unregistered tags** not explicitly documented in this policy, it will default to a **restricted review path**, requiring mandatory approval by `@promptops-governance-admins` before any promotion can occur.

## 4. Enforcement
- Promotion pipelines (e.g., `.github/workflows/promote.yaml`) will dynamically parse the `tags` field from the evaluated `suite.schema.json` and block promotion if the required mapped reviewers have not approved the PR.
