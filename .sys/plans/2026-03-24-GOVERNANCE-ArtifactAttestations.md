#### 1. Context & Goal
- **Objective**: Implement GitHub artifact attestations in the release workflow to establish build provenance for prompt packages.
- **Trigger**: The 'Publishing, provenance, and signing' section in `docs/vision.md` discusses SLSA provenance, stating that the "Registry verifies provenance attestations if provided".
- **Impact**: Creates a cryptographically verifiable audit trail proving that a specific prompt package asset was built by a specific GitHub Actions workflow run.

#### 2. File Inventory
- **Create**: None
- **Modify**: `.github/workflows/immutable-release.yml` (add build provenance attestation step)
- **Read-Only**: `docs/vision.md` (Publishing, provenance, and signing)

#### 3. Implementation Spec
- **Policy Architecture**: The release workflow will sign the packaged artifact (`promptops.tar.gz`) using a GitHub Action for build provenance, attaching the provenance attestation to the release.
- **Workflow Design**:
  - In `.github/workflows/immutable-release.yml`, update the `release` job permissions to include the required permissions for generating an OIDC token and writing attestations.
  - Add a step after the package creation to run the official GitHub Action for build provenance.
  - Pass the path to the packaged artifact (`promptops.tar.gz`) to the action.
- **CODEOWNERS Patterns**: None
- **Promotion Record Format**: None
- **Delivery Target Format**: None
- **Dependencies**: Requires GitHub Actions OIDC integration and artifact attestations capability.

#### 4. Test Plan
- **Verification**: Use the GitHub CLI to verify the release attestations for the generated artifact.
- **Success Criteria**: The `immutable-release.yml` workflow file is successfully updated conceptually and the GitHub CLI verification command passes for the generated artifact.
- **Edge Cases**: If the necessary write permissions are missing, the attestation step will fail.
