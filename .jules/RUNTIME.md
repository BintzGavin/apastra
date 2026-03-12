**Version**: 0.1.0

## 0.1.0 - Consumption Manifest Format Blocked
**Learning:** The consumption manifest format task was blocked because the `consumption-manifest.schema.json` dependency from the CONTRACTS domain had not been implemented yet.
**Action:** Always explicitly document required CONTRACTS schemas as dependencies in the spec file and check their existence before proceeding.
## 0.2.0 - Local override schema key
**Learning:** The schema uses 'override' instead of 'local_override' for the local path pin.
**Action:** Use 'override' in the python resolver implementation.

## 1.3.0 - Resolver topology misalignment
**Learning:** The initial implementations of WorkspaceResolver and GitRefResolver searched for prompts in the root `promptops/` directory instead of the `promptops/prompts/` directory defined in the `README.md` repo topology model.
**Action:** Always cross-reference directory lookup logic with the Example Repo Trees section in the vision document.
