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

## [v1.17.0] - Local Name Mapping
**Learning:** The consumption manifest allows mapping local app aliases to stable backend IDs and injecting specific model configurations directly from the manifest. This breaks the 1:1 strict parity assumption of prompt_id, meaning resolvers must handle mapped IDs.
**Action:** Always use rules.get('id', prompt_id) to extract the mapped ID.

## [v1.23.0] - PackagedResolver Caching
**Learning:** The `PackagedResolver` was missing implementation for local caching, offline fallback, and signature verification, which are critical for the 'Packaged artifact' vision requirement.
**Action:** Implement local caching, offline fallback, and signature verification within the `PackagedResolver` to enable offline resilience and enhanced artifact security.

## [v1.59.0] - MinimalPlanExceptionFinal
**Learning:** Executed MinimalPlanExceptionFinal to clear pending state for the RUNTIME domain.
**Action:** Always strictly increment logical sequential version numbers even for MinimalPlanException exceptions.

## 1.61.0 - Local Resolver Caching
**Learning:** Local resolution was a potential bottleneck because it re-read files from disk on every `resolve()` call.
**Action:** Implement memory caching based on the file's modification time in `LocalResolver`.

## 1.64.0 - GitRef Resolver Caching
**Learning:** Similar to Local and Workspace resolvers, GitRef resolution creates redundant I/O bottlenecks (subprocess calls) when resolving identical remote refs.
**Action:** Implement memory caching based on the pin and prompt ID tuple in `GitRefResolver`.

## 1.67.0 - MinimalPlanExceptionFinal
**Learning:** Executed MinimalPlanExceptionFinal to clear pending state for the RUNTIME domain.
**Action:** Always strictly increment logical sequential version numbers even for MinimalPlanException exceptions.

## 1.68.0 - MinimalPlanExceptionFinal
**Learning:** Executed MinimalPlanExceptionFinal to clear pending state for the RUNTIME domain.
**Action:** Always strictly increment logical sequential version numbers even for MinimalPlanException exceptions.
