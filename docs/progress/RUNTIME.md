### RUNTIME v0.2.0
- ✅ Completed: ConsumptionManifestFormat - Defined schema example format
- ✅ Completed: LocalOverrideResolution - Implemented local override step in python resolver chain
### RUNTIME v0.3.0
- ✅ Completed: WorkspacePathResolution - Implemented workspace path lookup in resolver chain
### RUNTIME v0.4.0
- ✅ Completed: GitRefResolution - Implemented git ref resolution in python resolver chain

### RUNTIME v0.5.0
- ✅ Completed: MinimalResolveInterface - Implemented resolve() function as minimal runtime interface

### RUNTIME v0.6.0
- ✅ Completed: PackagedArtifactResolution - Implemented packaged artifact fallback in resolver chain

### RUNTIME v0.7.0
- ✅ Completed: RunnerShim - Implemented runner shim script

### RUNTIME v0.8.0
- ✅ Completed: DeterministicDigestTooling - Implemented canonicalization and digest computation for prompts and datasets

### RUNTIME v0.9.0
- ✅ Completed: ConsumptionManifestValidation - Implemented schema validation for consumption manifests during load_manifest

### RUNTIME v1.0.0
- ✅ Completed: ConsumptionManifestFormat - Re-wrote consumption manifest format to be more realistic and validate

### RUNTIME v1.1.0
- ✅ Completed: PromptSpecValidation - Implemented schema validation for resolved prompt specifications against prompt-spec.schema.json

### RUNTIME v1.2.0
- ✅ Completed: HarnessContractValidation - Implemented runner shim validation against CONTRACTS schemas

### RUNTIME v1.3.0
- ✅ Completed: PromptTemplateRendering - Implemented variable injection in the resolve() function

### RUNTIME v1.3.1
- ✅ Completed: ResolverTopologyAlignment - Aligned workspace and git ref resolvers with core repo topology model

### RUNTIME v1.4.0
- ✅ Completed: ReferenceCLI - Spec the reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.

### RUNTIME v1.4.1
- ✅ Completed: LocalOverrideFix - Fix the LocalResolver in the resolver chain to parse prompt packages instead of returning stub strings.

### RUNTIME v1.5.0
- ✅ Completed: ReferenceCLI - Implemented reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.

### RUNTIME v1.6.0
- ✅ Completed: DirectoryResolver - Update WorkspaceResolver and GitRefResolver to support resolving prompts packaged in a <prompt_id> directory.

### RUNTIME v1.7.0
- ✅ Completed: SemverTagResolution - Implement semver tag resolution in the GitRefResolver.

### RUNTIME v1.7.1
- ✅ Completed: MinimalPlanException - Executed minimal plan exception to unlock completion of current run.

### RUNTIME v1.8.0
- ✅ Completed: QuickEvalWorkspaceResolution - Implement quick eval format resolution in the WorkspaceResolver.

### RUNTIME v1.9.0
- ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.

### RUNTIME v1.10.0
- ✅ Completed: QuickEvalLocalOverrideResolution - Implement quick eval format resolution in the LocalResolver.

### RUNTIME v1.11.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.12.0
- ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.

### RUNTIME v1.13.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.14.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.15.0
- ✅ Completed: MinimalPlanExceptionFinal - Executed the final minimal plan exception for the RUNTIME domain.

### RUNTIME v1.16.0
- ✅ Completed: QuickEvalGitRefResolution - Implement quick eval format resolution in the GitRefResolver.

### RUNTIME v1.17.0
- ✅ Completed: LocalNameMappingResolution - Implement local alias mapping to stable IDs and model metadata propagation in the resolver chain.

### RUNTIME v1.18.0
- ✅ Completed: PackagedResolver - Implemented packaged artifact resolution for sha256 and oci refs with schema validation.
