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

## 1.70.0 - Remote Git URL Resolution Plan
**Learning:** The vision document explicitly outlines the need for remote git URL resolution, enabling the separate-repo consumption topology, but current implementation relies only on local refs.
**Action:** Draft spec to extend GitRefResolver to correctly resolve remote 'git+' URLs, implementing caching and avoiding full repo clones.

## 1.71.0 - Registry Protocol Resolution
**Learning:** The `PackagedResolver` currently throws errors for `oci://`, `npm:`, and `pypi:` protocols because the implementations were stubbed, preventing downstream consumers from using enterprise distribution methods outlined in the vision.
**Action:** Always verify that explicit protocol schemes mentioned in the vision document have concrete fetch logic implemented rather than placeholders.

## 1.78.0 - MinimalPlanExceptionFinal
**Learning:** Discovered that the RegistryProtocolResolution plan was already fully implemented in the codebase.
**Action:** Always verify if a feature is already present before attempting to re-implement it, and use the Minimal Plan Exception protocol when it is.

## 1.79.0 - Remote Git SHA Cloning Fix
**Learning:** The fallback logic for remote git URLs `git clone --depth 1 --branch <ref>` fails when the ref is a commit SHA. Remote SHAs require a full clone followed by a checkout.
**Action:** Draft spec to fix the `GitRefResolver` remote checkout fallback path to support commit SHAs alongside branches and tags.

## 1.80.0 - Remote Git Semver Resolution Plan
**Learning:** The `GitRefResolver` supports `semver:` resolution locally, but remote git URLs with `semver:` prefixes fail because the existing fallback logic only handles direct branches or tags. The vision states "Apps can pin prompts by commit SHA, tag, or semver", which implies this should work for remote repositories as well.
**Action:** Draft spec to fetch tags from remote repositories using `git ls-remote --tags` and resolve semver ranges before attempting `git archive` or `git clone`.

## 1.81.0 - MinimalPlanExceptionFinal
**Learning:** Verified that all vision gaps in docs/vision.md and README.md for the RUNTIME domain have been addressed. No remaining features to plan.
**Action:** Execute MinimalPlanExceptionFinal to clear pending state.

## 1.82.0 - MinimalPlanExceptionFinal
**Learning:** Verified that all vision gaps in docs/vision.md and README.md for the RUNTIME domain have been addressed. No remaining features to plan.
**Action:** Execute MinimalPlanExceptionFinal to clear pending state.

## 1.83.0 - MinimalPlanExceptionFinal
**Learning:** Verified that all vision gaps in docs/vision.md and README.md for the RUNTIME domain have been addressed. No remaining features to plan.
**Action:** Execute MinimalPlanExceptionFinal to clear pending state.

## 1.84.0 - MinimalPlanExceptionFinal
**Learning:** Verified that all vision gaps in docs/vision.md and README.md for the RUNTIME domain have been addressed. No remaining features to plan.
**Action:** Execute MinimalPlanExceptionFinal to clear pending state.

## 1.85.0 - MinimalPlanExceptionFinal
**Learning:** Verified that all vision gaps in docs/vision.md and README.md for the RUNTIME domain have been addressed. No remaining features to plan.
**Action:** Execute MinimalPlanExceptionFinal to clear pending state.

## 1.86.0 - MinimalPlanExceptionFinal
**Learning:** Verified that all vision gaps in docs/vision.md and README.md for the RUNTIME domain have been addressed. No remaining features to plan.
**Action:** Execute MinimalPlanExceptionFinal to clear pending state.
